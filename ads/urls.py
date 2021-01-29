from django.urls import path
from . import views

urlpatterns = [
    path("out/<slug:id>/", views.redirect_ad, name="redirect_ad"),
    path("ads/create/", views.create_ad, name="create_ad"),
    path("ads/edit/<slug:uuid>/", views.edit_ad, name="edit_ad"),
    path("ads/review/", views.review_ad, name="review_ad"),
    path("ad/activate/<slug:uuid>/", views.activate_ad, name="activate_ad"),
    path("managment/review-ads/", views.admin_review_ads, name="admin_review_ads",),
    path("managment/review-ad/<slug:uuid>/", views.admin_review_ad, name="admin_review_ad",),
    path("managment/ads/", views.admin_all_ads, name="admin_all_ads",),
]
