import stripe
import json
from django.shortcuts import render
from decouple import config
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ads.models import Ad, ad_prices
from .models import Payment


# config("SECRET_KEY")
def payments_test(request):
    return render(request, "payments/test.html")


def payments_success(request):
    return render(request, "payments/success.html")


def payments_cancelled(request):
    return render(request, "payments/cancelled.html")


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"public_key": config("STRIPE_PUBLISHABLE_KEY")}
        return stripe_config


@csrf_exempt
def create_ad_checkout_session(request):
    uuid = request.GET['ad']
    ad = Ad.objects.filter(redirect_uuid=uuid).first()
    price = ad_prices[f"{ad.contract_length}"]["price"]

    if request.method == "GET":
        domain_url = config("DOMAIN_URL")
        stripe.api_key = config("STRIPE_SECRET_KEY")
        try:
            checkout_session = stripe.checkout.Session.create(
                # customer_email=request.user.email,
                client_reference_id=request.user.id
                if request.user.is_authenticated
                else None,
                success_url=domain_url
                + "/payments/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=f"{domain_url}/payments/cancelled/",
                payment_method_types=["card"],
                mode="payment",
                metadata={
                    "purchase_type": "ad",
                    "uuid": uuid
                },
                line_items=[
                    {
                        'name': f'{ad.type.title()} Ad',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': f'{price}00',
                    }
                ],
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = config("STRIPE_SECRET_KEY")
    endpoint_secret = config("STRIPE_ENDPOINT_SECRET")
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        # convert payload to dict 
        response = json.loads(payload)

        # get payment info from response
        stripe_checkout_id = response['id']
        amount_paid = response['data']['object']['amount_total']
        email = response['data']['object']['customer_details']['email']
        payment_status = response['data']['object']['payment_status']
        purchase_type = response['data']['object']['metadata']['purchase_type']
        uuid = response['data']['object']['metadata']['uuid']

        # save info to local payments table
        if purchase_type == 'ad':
            ad = Ad.objects.get(redirect_uuid=uuid)
            ad.status = "review"
            ad.save()

            p = Payment()
            p.stripe_checkout_id = stripe_checkout_id
            p.amount_paid = amount_paid
            p.email = email
            p.payment_status = payment_status
            p.purchase_type = purchase_type
            p.purchase_choice = ad.type
            p.ad_uuid = uuid
            p.user = ad.user
            p.save()

    return HttpResponse(status=200)
