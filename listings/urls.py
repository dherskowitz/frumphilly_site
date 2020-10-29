from django.urls import path
from . import views

urlpatterns = [
    path("", views.listings, name="listings"),
    path("create/<slug:slug>/", views.listings_create, name="listings_create"),
    path("select/", views.listings_select, name="listings_select"),
    path("<slug:slug>-<int:pk>/", views.listing_single, name="listing_single"),
    path("<slug:slug>-<int:pk>/edit/", views.listings_edit, name="listings_edit"),
    path("<slug:slug>-<int:pk>/delete/", views.listings_delete, name="listings_delete"),
]
