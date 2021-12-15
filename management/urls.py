from django.urls import path
from . import views

urlpatterns = [
    path("review-ads/", views.admin_review_ads, name="admin_review_ads", ),
    path("review-ad/<slug:uuid>/", views.admin_review_ad, name="admin_review_ad", ),
    path("ads/", views.admin_all_ads, name="admin_all_ads", ),
]
