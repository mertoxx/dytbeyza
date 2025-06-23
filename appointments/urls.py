# appointments/urls.py
from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment_create, name='appointment_create'),
    path('create/', views.appointment_create, name='appointment_create'),
    path('success/', views.appointment_success, name='appointment_success'),
    path('get-available-times/', views.get_available_times, name='get_available_times'),
    path('get-available-times-simple/', views.get_available_times_simple, name='get_available_times_simple'),
    # Debug endpoint - sadece development için
    path('debug/', views.debug_appointment_form, name='debug_appointment_form'),
]