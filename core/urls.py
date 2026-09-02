"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

import os

urlpatterns = []

service_type = os.environ.get('SERVICE_TYPE', 'all')

if service_type in ['admin', 'all']:
    urlpatterns += [
        path('admin/', admin.site.urls),
        path('control-panel/', include('admin_panel.urls', namespace='admin_panel')),
    ]

if service_type in ['storefront', 'all']:
    urlpatterns += [
        path('', include('shop.urls', namespace='shop')),
    ]

# Accounts are needed by both
urlpatterns += [
    path('accounts/', include('accounts.urls', namespace='accounts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

