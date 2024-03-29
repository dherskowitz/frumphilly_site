from django.urls import path
from . import views

urlpatterns = [
    path("select/", views.listings_select, name="listings_select"),
    path("create/<slug:slug>/", views.listings_create, name="listings_create"),
    path("<slug:slug>-<int:pk>/edit/", views.listings_edit, name="listings_edit"),
    path("<slug:slug>-<int:pk>/delete/", views.listings_delete, name="listings_delete"),
    path("<slug:slug>-<int:pk>/", views.listing_single, name="listing_single"),
    path("like/<int:listing_id>/", views.listing_like, name="listing_like"),
    # path("<slug:slug>/", views.listings, name="listings"),
    path("", views.listings_all, name="listings_all"),
]
