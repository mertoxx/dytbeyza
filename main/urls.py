# main/urls.py

from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Ana sayfalar
    path('', views.home, name='home'),
    path('hakkimda/', views.about, name='about'),
    path('iletisim/', views.contact, name='contact'),
    
    # Hizmetler
    path('hizmetler/', views.services, name='services'),
    path('hizmet/<int:service_id>/', views.service_detail, name='service_detail'),
    
    # Arama
    path('ara/', views.search, name='search'),
    
    # Yasal sayfalar
    path('gizlilik-politikasi/', views.privacy_policy, name='privacy_policy'),
    path('kullanim-sartlari/', views.terms_of_service, name='terms_of_service'),
]