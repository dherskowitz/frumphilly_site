from django.urls import path
from . import views

urlpatterns = [
    path("", views.listings, name="listings"),
    path("<slug:slug>-<int:pk>", views.listing_single, name="listing_single"),
]
