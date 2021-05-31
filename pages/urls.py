from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("advertising/", views.advertising, name="advertising"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),
    path("report/", views.report_post, name="report_post"),
    path("advertising/terms/", views.ad_terms, name="ad_terms"),
]
