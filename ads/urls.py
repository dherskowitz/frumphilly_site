from django.urls import path
from . import views

urlpatterns = [
    path("out/<slug:id>/", views.redirect_ad, name="redirect_ad"),
    path("ads/create/", views.create_ad, name="create_ad"),
]
