from django.urls import path

from . import views

urlpatterns = [
    path('', views.payments_test, name='payments_test'),
    path('success/', views.payments_success, name='payments_success'),
    path('cancelled/', views.payments_cancelled, name='payments_cancelled'),
    path('config/', views.stripe_config, name='stripe_config'),
    # path('create-checkout-session/', views.create_checkout_session),
    path('create-ad-checkout-session/', views.create_ad_checkout_session),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]
