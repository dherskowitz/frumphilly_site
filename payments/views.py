from django.shortcuts import render
from decouple import config
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# config("SECRET_KEY")
def payments_test(request):
    return render(request, 'payments/test.html')


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {
            "public_key": config("STRIPE_PUBLISHABLE_KEY")
        }
        return JsonResponse(stripe_config, safe=False)
