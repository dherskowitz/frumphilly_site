import stripe
from django.shortcuts import render
from decouple import config
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


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
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        domain_url = config("DOMAIN_URL")
        stripe.api_key = config("STRIPE_SECRET_KEY")
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                client_reference_id=request.user.id
                if request.user.is_authenticated
                else None,
                success_url=domain_url
                + "/payments/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=f"{domain_url}/payments/cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[{
                    'price': 'price_1Hhfk5G3pTnNZwrhlGv4DMHY',
                    'quantity': 1,
                }],
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
        # pass
        print("==============")
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(payload)

    return HttpResponse(status=200)
