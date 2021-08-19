from django.urls import path
from . import views

urlpatterns = [
    path("<slug:category>/<slug:thread>/", views.forum_thread, name="forum_thread"),
    path("<slug:category>/", views.forum_category, name="forum_category"),
    path("", views.forum, name="forum"),
]
