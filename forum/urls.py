from django.urls import path
from . import views

urlpatterns = [
    path("<slug:category>/add/", views.forum_thread_create, name="forum_thread_create"),
    path("<slug:category>/<slug:thread>/add", views.forum_post_create, name="forum_post_create"),
    path("<slug:category>/<slug:thread>/", views.forum_thread, name="forum_thread"),
    path("<slug:category>/", views.forum_category, name="forum_category"),
    path("<str:user>/", views.forum_user_posts, name="forum_user_posts"),
    path("", views.forum, name="forum"),
]
