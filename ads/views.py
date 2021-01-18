from django.shortcuts import redirect, render
from .models import Ad


def redirect_ad(request, id):
    ad = Ad.objects.get(redirect_uuid=id)
    return redirect(ad.redirect_to)
