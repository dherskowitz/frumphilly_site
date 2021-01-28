from django.urls import path
from . import views

urlpatterns = [
    path("out/<slug:id>/", views.redirect_ad, name="redirect_ad"),
    path("ads/create/", views.create_ad, name="create_ad"),
    path("ads/edit/<slug:uuid>/", views.edit_ad, name="edit_ad"),
    path("ads/review/", views.review_ad, name="review_ad"),
    path("ad/activate/<slug:uuid>/", views.activate_ad, name="activate_ad"),
]
