import stripe
from django.shortcuts import render
from decouple import config
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# config("SECRET_KEY")
def payments_test(request):
    return render(request, 'payments/test.html')


def payments_success(request):
    return render(request, 'payments/success.html')


def payments_cancelled(request):
    return render(request, 'payments/cancelled.html')


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {
            "public_key": config("STRIPE_PUBLISHABLE_KEY")
        }
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        domain_url = config("DOMAIN_URL")
        stripe.api_key = config("STRIPE_SECRET_KEY")
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + '/payments/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=f'{domain_url}/payments/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'T-shirt',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
