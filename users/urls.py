from django.urls import path
from . import views

urlpatterns = [
    path("user/account/", views.user_account, name="user_account",),
    path("user/events/", views.user_events, name="user_events",),
    path("user/listings/", views.user_listings, name="user_listings",),
]
