# appointments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from .models import Appointment, TimeSlot, AppointmentSettings
from .forms import AppointmentForm
import json
import logging

# Logger oluştur
logger = logging.getLogger(__name__)

def appointment_create(request):
    """Randevu oluşturma"""
    print(f"=== APPOINTMENT CREATE VIEW ===")
    print(f"Request method: {request.method}")
    print(f"Request POST data: {request.POST}")
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        
        print("=== FORM PROCESSING ===")
        print(f"Form data: {form.data}")
        print(f"Form is valid: {form.is_valid()}")
        
        if not form.is_valid():
            print("=== FORM ERRORS ===")
            print(f"Form errors: {form.errors}")
            print(f"Non-field errors: {form.non_field_errors()}")
            
            # Her alan için hataları detaylı logla
            for field_name, field in form.fields.items():
                if field_name in form.errors:
                    print(f"Field '{field_name}' errors: {form.errors[field_name]}")
                    
            # Hata mesajlarını kullanıcıya göster
            messages.error(request, 'Form verilerinde hatalar var. Lütfen kontrol edin.')
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f'Genel hata: {error}')
                    else:
                        messages.error(request, f'{form.fields[field].label}: {error}')
        else:
            try:
                print("=== SAVING APPOINTMENT ===")
                appointment = form.save()
                print(f"Appointment saved successfully: ID={appointment.id}")
                
                # E-posta bildirimi gönderme işlemi
                try:
                    print("=== SENDING EMAIL NOTIFICATIONS ===")
                    
                    # Admin'e bildirim e-postası
                    admin_subject = f'Yeni Randevu Talebi - {appointment.full_name}'
                    admin_message = f"""
Yeni randevu talebi alındı:

Ad Soyad: {appointment.full_name}
Telefon: {appointment.phone}
E-posta: {appointment.email}
Tarih: {appointment.appointment_date}
Saat: {appointment.appointment_time}
Randevu Türü: {appointment.get_appointment_type_display()}

Kişisel Bilgiler:
Yaş: {appointment.age}
Cinsiyet: {appointment.get_gender_display()}
Boy: {appointment.height} cm
Kilo: {appointment.weight} kg
BMI: {appointment.bmi}

Medikal Geçmiş: {appointment.medical_history or 'Belirtilmemiş'}
İlaçlar: {appointment.medications or 'Belirtilmemiş'}
Beslenme Kısıtlamaları: {appointment.dietary_restrictions or 'Belirtilmemiş'}
Hedefler: {appointment.goals}

Randevu ID: {appointment.id}
Oluşturulma Tarihi: {appointment.created_at}
"""
                    
                    # Admin e-postası gönder
                    if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
                        send_mail(
                            subject=admin_subject,
                            message=admin_message,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[settings.EMAIL_HOST_USER],
                            fail_silently=True,
                        )
                        print("Admin email sent successfully")
                    
                    # Müşteriye onay e-postası
                    customer_subject = 'Randevu Talebiniz Alındı - Diyetisyen'
                    customer_message = f"""
Sayın {appointment.full_name},

Randevu talebiniz başarıyla alındı. Randevu detaylarınız:

📅 Tarih: {appointment.appointment_date.strftime('%d.%m.%Y')}
🕐 Saat: {appointment.appointment_time}
📋 Randevu Türü: {appointment.get_appointment_type_display()}

Randevunuz 24 saat içinde onaylandığında size bilgi verilecektir.

Randevu Referans No: #{appointment.id}

Herhangi bir sorunuz olursa bizimle iletişime geçebilirsiniz:
📞 Telefon: +90 555 123 45 67
📱 WhatsApp: https://wa.me/905551234567

Sağlıklı günler dileriz.

Diyetisyen Ekibi
"""
                    
                    if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
                        send_mail(
                            subject=customer_subject,
                            message=customer_message,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[appointment.email],
                            fail_silently=True,
                        )
                        print("Customer email sent successfully")
                    
                except Exception as e:
                    print(f"Email sending error: {e}")
                    logger.error(f"Email sending failed: {e}")
                    # E-posta hatası randevu kaydını etkilemez
                
                # Başarı mesajı
                messages.success(
                    request, 
                    f'Randevu talebiniz başarıyla alındı! Referans No: #{appointment.id}. Size en kısa sürede dönüş yapılacaktır.'
                )
                
                print("=== REDIRECTING TO SUCCESS PAGE ===")
                return redirect('appointments:appointment_success')
                
            except Exception as e:
                print(f"=== ERROR SAVING APPOINTMENT ===")
                print(f"Error: {e}")
                logger.error(f"Appointment save error: {e}")
                messages.error(request, f'Randevu kaydedilirken hata oluştu. Lütfen tekrar deneyin.')
                
    else:
        print("=== GET REQUEST - CREATING NEW FORM ===")
        form = AppointmentForm()
    
    context = {
        'form': form,
    }
    
    print(f"=== RENDERING TEMPLATE ===")
    print(f"Context keys: {list(context.keys())}")
    
    return render(request, 'appointments/appointment_form.html', context)

def appointment_success(request):
    """Randevu başarı sayfası"""
    return render(request, 'appointments/appointment_success.html')

@require_http_methods(["GET"])
def get_available_times(request):
    """AJAX ile müsait saatleri getir"""
    print(f"=== GET AVAILABLE TIMES ===")
    
    date_str = request.GET.get('date')
    print(f"Requested date: {date_str}")
    
    if not date_str:
        print("No date provided")
        return JsonResponse({'times': [], 'error': 'Tarih belirtilmedi'})
    
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        print(f"Parsed date: {selected_date}")
    except ValueError as e:
        print(f"Date parsing error: {e}")
        return JsonResponse({'times': [], 'error': 'Geçersiz tarih formatı'})
    
    # Bugünden önceki tarihler için boş liste
    if selected_date < timezone.now().date():
        print("Date is in the past")
        return JsonResponse({'times': [], 'error': 'Geçmiş tarih seçilemez'})
    
    try:
        # Randevu ayarları
        try:
            settings_obj = AppointmentSettings.objects.first()
            working_days = settings_obj.get_working_days_list() if settings_obj else [1, 2, 3, 4, 5]
        except:
            working_days = [1, 2, 3, 4, 5]  # Varsayılan: Pazartesi-Cuma
        
        print(f"Working days: {working_days}")
        
        # Seçilen günün hafta günü kontrolü (1=Pazartesi, 7=Pazar)
        weekday = selected_date.isoweekday()
        print(f"Selected weekday: {weekday}")
        
        if weekday not in working_days:
            print("Selected day is not a working day")
            return JsonResponse({'times': [], 'error': 'Seçilen gün çalışma günü değil'})
        
        # Tüm aktif saat dilimlerini al
        all_times = TimeSlot.objects.filter(is_active=True).order_by('time')
        print(f"Total active timeslots: {all_times.count()}")
        
        # Bu tarihte dolu olan saatleri al
        busy_time_ids = Appointment.objects.filter(
            appointment_date=selected_date,
            status__in=['pending', 'confirmed']
        ).values_list('appointment_time_id', flat=True)
        
        print(f"Busy time IDs: {list(busy_time_ids)}")
        
        # Müsait saatleri filtrele
        available_times = []
        current_time = timezone.now().time()
        
        for time_slot in all_times:
            # Bu saat dolu mu?
            if time_slot.id in busy_time_ids:
                print(f"Time {time_slot.time} is busy")
                continue
            
            # Bugün ise, geçmiş saatleri gösterme
            if selected_date == timezone.now().date():
                if time_slot.time <= current_time:
                    print(f"Time {time_slot.time} is in the past")
                    continue
            
            available_times.append({
                'id': time_slot.id,
                'time': time_slot.time.strftime('%H:%M')
            })
            print(f"Added available time: {time_slot.time}")
        
        print(f"Total available times: {len(available_times)}")
        
        return JsonResponse({
            'times': available_times,
            'total': len(available_times),
            'date': date_str
        })
        
    except Exception as e:
        print(f"Error in get_available_times: {e}")
        logger.error(f"get_available_times error: {e}")
        return JsonResponse({'times': [], 'error': 'Sunucu hatası'})

def get_available_times_simple(request):
    """Basit müsait saatler - test için"""
    print("=== GET AVAILABLE TIMES SIMPLE ===")
    
    try:
        # Tüm aktif saatleri döndür
        available_times = TimeSlot.objects.filter(is_active=True).order_by('time')
        print(f"Found {available_times.count()} timeslots")
        
        times_data = []
        for slot in available_times:
            times_data.append({
                'id': slot.id,
                'time': slot.time.strftime('%H:%M')
            })
            print(f"Added: {slot.time}")
        
        return JsonResponse({'times': times_data})
        
    except Exception as e:
        print(f"Error in simple times: {e}")
        return JsonResponse({'times': []})

# Management command için helper function
def create_default_timeslots():
    """Varsayılan zaman dilimlerini oluştur"""
    from datetime import time
    
    default_times = [
        '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
        '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00'
    ]
    
    created_count = 0
    for time_str in default_times:
        try:
            hour, minute = map(int, time_str.split(':'))
            time_obj = time(hour, minute)
            
            timeslot, created = TimeSlot.objects.get_or_create(
                time=time_obj,
                defaults={'is_active': True}
            )
            
            if created:
                created_count += 1
                print(f"Created TimeSlot: {time_str}")
        except Exception as e:
            print(f"Error creating timeslot {time_str}: {e}")
    
    print(f"Created {created_count} new timeslots")
    return created_count

# Debug view - sadece development için
def debug_appointment_form(request):
    """Debug için form durumunu kontrol et"""
    if not settings.DEBUG:
        return JsonResponse({'error': 'Only available in debug mode'})
    
    debug_info = {
        'timeslots': [],
        'form_fields': [],
        'settings': {}
    }
    
    # TimeSlot'ları kontrol et
    timeslots = TimeSlot.objects.all()
    for ts in timeslots:
        debug_info['timeslots'].append({
            'id': ts.id,
            'time': str(ts.time),
            'is_active': ts.is_active
        })
    
    # Form alanlarını kontrol et
    form = AppointmentForm()
    for field_name, field in form.fields.items():
        debug_info['form_fields'].append({
            'name': field_name,
            'required': field.required,
            'label': str(field.label),
            'widget': str(type(field.widget))
        })
    
    # Ayarları kontrol et
    debug_info['settings'] = {
        'DEBUG': settings.DEBUG,
        'EMAIL_CONFIGURED': hasattr(settings, 'EMAIL_HOST_USER') and bool(settings.EMAIL_HOST_USER),
        'TIMEZONE': str(timezone.get_current_timezone()),
        'NOW': timezone.now().isoformat()
    }
    
    return JsonResponse(debug_info)