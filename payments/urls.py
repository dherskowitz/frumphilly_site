from django.urls import path

from . import views

urlpatterns = [
    path('', views.payments_test, name='payments_test'),
    path('config/', views.stripe_config, name='stripe_config'),
]
