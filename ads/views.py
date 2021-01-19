from django.shortcuts import redirect, render
from .models import Ad
from .forms import AdForm


def redirect_ad(request, id):
    ad = Ad.objects.get(redirect_uuid=id)
    return redirect(ad.redirect_to)


def create_ad(request):
    context = {
        'form': AdForm()
    }
    return render(request, 'ads/create.html', context)
