# appointments/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Appointment, TimeSlot, AppointmentSettings

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['time', 'is_active']
    list_filter = ['is_active']
    list_editable = ['is_active']
    ordering = ['time']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'appointment_date', 'appointment_time', 
        'appointment_type', 'status', 'created_at'
    ]
    list_filter = [
        'status', 'appointment_type', 'gender', 
        'appointment_date', 'created_at'
    ]
    search_fields = [
        'first_name', 'last_name', 'email', 'phone'
    ]
    readonly_fields = ['created_at', 'updated_at', 'bmi']
    list_editable = ['status']
    date_hierarchy = 'appointment_date'
    actions = ['confirm_appointments', 'cancel_appointments']
    
    fieldsets = (
        ('Kişisel Bilgiler', {
            'fields': (
                ('first_name', 'last_name'),
                ('email', 'phone')
            )
        }),
        ('Randevu Detayları', {
            'fields': (
                ('appointment_date', 'appointment_time'),
                ('appointment_type', 'status')
            )
        }),
        ('Sağlık Bilgileri', {
            'fields': (
                ('age', 'gender'),
                ('height', 'weight', 'bmi'),
                'medical_history',
                'medications',
                'dietary_restrictions'
            )
        }),
        ('Hedefler ve Notlar', {
            'fields': ('goals', 'notes')
        }),
        ('Sistem Bilgileri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def confirm_appointments(self, request, queryset):
        queryset.update(status='confirmed')
    confirm_appointments.short_description = "Seçili randevuları onayla"
    
    def cancel_appointments(self, request, queryset):
        queryset.update(status='cancelled')
    cancel_appointments.short_description = "Seçili randevuları iptal et"

@admin.register(AppointmentSettings)
class AppointmentSettingsAdmin(admin.ModelAdmin):
    list_display = ['max_days_ahead', 'min_hours_ahead', 'working_days']