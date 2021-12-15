from django.urls import path
from . import views

urlpatterns = [
    path("review-ads/", views.admin_review_ads, name="admin_review_ads", ),
    path("review-ad/<slug:uuid>/", views.admin_review_ad, name="admin_review_ad", ),
    path("ads/", views.admin_all_ads, name="admin_all_ads", ),
    path("contacts/", views.contact_submissions, name="contact_submissions", ),
    path("contacts/<int:contact_id>", views.contact_message, name="contact_message", ),
    path("contacts/contact_toggle_status/", views.toggle_status, name="contact_toggle_status", ),
]
