"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from bot import views
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myproject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.catalog, name='catalog'),
    path('catalog/', views.catalog, name='catalog'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('create_account/', views.create_account, name='create_account'),
    path('save_payment/', views.save_payment, name='save_payment'),
    path('payment/', views.payment, name='payment'),
    path('faqs/', views.faqs, name='faqs')
]

urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
