"""lime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

from django.conf.urls.static import static

from lime import settings
from mainpage import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('login/', views.login_),
    path('signup/', views.signup_),
    path('home/', views.home),
    path('logout/', views.logout_),
    path('profile/', views.user_profile),
    path('home/<int:accept>/', views.home),
    path('contact/', views.contact),
    path('change/', views.change),
    path('search/', views.search),
    path('get_profile/<str:username>/', views.get_profile, name='get_profile'),
    path('delete_profile/', views.delete_profile())
] + static(settings.STATIC_URL, document_root= settings.STATICFILES_DIRS)

