"""
URL configuration for trainforge project.

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
from django.urls import path, include

urlpatterns = [
    path('trainforge/admin/', admin.site.urls),

    path('trainforge/', include('core.urls')),
    path('trainforge/users/', include('users.urls')),
    path('trainforge/training/', include('training.urls')),
    path('trainforge/schedule/', include('scheduling.urls')),
    path('trainforge/progress/', include('progress.urls')),
    path('trainforge/accounts/', include('allauth.urls')),
]
