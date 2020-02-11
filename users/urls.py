from django.urls import path
from . import views

urlpatterns = [
    path("user/events/", views.user_events, name="user_events",),
]
