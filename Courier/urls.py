"""Courier URL Configuration

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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from DrugSystem.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^contanctUs$', contactUs),
    url(r'^cancelOrder$', cancelOrder),
    url(r'^confirmOrder$', confirmOrderDelivery),
    url(r'^checkUserName$', checkUserName),
    url(r'^trackOrder', getOrderLocation),
    url(r'^login', logIn, name='login'),
    url(r'^logout$', logOut, name='logout'),
    url(r'^makeDrugs$', makeDrugs), 
    url(r'^makeOrder$', makeOrder),
    url(r'^pastOrders$', getPastOrders),
    url(r'^register', register),
    url(r'^NDCsearch$', searchNDC),
    url(r'^updateDEA$', updateDEALevel),
    url(r'^updateLocation$', updateOrderLocation),
    url(r'^', home, name='home'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
