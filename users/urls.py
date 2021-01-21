from django.urls import path
from . import views

urlpatterns = [
    path("user/settings/", views.user_settings, name="user_settings",),
    path("user/account/", views.user_account, name="user_account",),
    path("user/events/", views.user_events, name="user_events",),
    path("user/listings/", views.user_listings, name="user_listings",),
    path("user/ads/", views.user_ads, name="user_ads",),
    path("manage/review-ads/", views.admin_review_ads, name="admin_review_ads",),
]
