from django.urls import path
from . import views

urlpatterns = [
    path("review-ad/<slug:uuid>/", views.admin_review_ad, name="admin_review_ad", ),
    path("ads/", views.admin_all_ads, name="admin_all_ads", ),
    path("contacts/", views.contact_submissions, name="contact_submissions", ),
    path("contacts/<int:contact_id>", views.contact_message, name="contact_message", ),
    path("contacts/contact_toggle_status/", views.toggle_status, name="contact_toggle_status", ),
    path("contacts/delete-message/<int:message_id>", views.delete_message, name="contact_delete_message", ),

    path("reported-posts/", views.reported_posts, name="reported_posts", ),
    path("reported-posts/<int:post_id>", views.reported_post, name="reported_post", ),
]
