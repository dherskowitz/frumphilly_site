"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from ckeditor_uploader import views


urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('manage/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    # path("payments/", include("payments.urls"), name="payments"),
    path("", include("pages.urls"), name="pages"),
    path("", include("events.urls"), name="events"),
    path("", include("users.urls"), name="users"),
    path("listings/", include("listings.urls"), name="listings"),
    path("", include("ads.urls"), name="ads"),
    path("payments/", include("payments.urls"), name="payments"),
    path("forum/", include("forum.urls"), name="forum"),
    path("ads.txt", TemplateView.as_view(template_name="ads.txt", content_type="text/plain")),
    path('summernote/', include('django_summernote.urls')),
]
