from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from .models import Ad
from .forms import AdForm
from payments.views import stripe_config


def redirect_ad(request, id):
    ad = Ad.objects.get(redirect_uuid=id)
    return redirect(ad.redirect_to)


@login_required
def create_ad(request):
    form = AdForm()
    context = {"form": form}
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES)
        context["form"] = form

        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect(f"/ads/review/?ad={ad.redirect_uuid}")

    return render(request, 'ads/create.html', context)


@login_required
def review_ad(request):
    uuid = request.GET['ad']
    ad = Ad.objects.filter(redirect_uuid=uuid).first()
    if request.user != ad.user:
        return render(request, "403.html")
    context = {
        "ad": ad,
        "stripe": stripe_config(request)
    }
    return render(request, 'ads/review.html', context)
