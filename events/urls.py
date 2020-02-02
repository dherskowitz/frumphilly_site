from django.urls import path
from . import views

urlpatterns = [
    path("events", views.events_all, name="events_all"),
    path("events/create", views.events_create, name="events_create"),
    path("events/<int:event_id>", views.events_single, name="events_single"),
]
