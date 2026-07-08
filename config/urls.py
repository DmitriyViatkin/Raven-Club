"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.template.backends import django
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path ('', include('django.contrib.auth.urls')),
    path ('', include('authentication.urls')),
    path ('', include('core.urls')),
    path ('predictions/', include('src.leagues.urls')),
    path ('users/', include('src.users.urls')),
    path ('tournaments/', include('src.tournaments.urls')),
    path ('admin/', admin.site.urls),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
