from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.events_all, name="events_all"),
    path("events/create/", views.events_create, name="events_create"),
    path("events/<slug>/", views.events_single, name="events_single"),
    path("events/<slug>/edit/", views.events_edit, name="events_edit"),
]
