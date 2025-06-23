from django import forms
from django.utils import timezone
from django.core.validators import RegexValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Fieldset, HTML
from .models import Appointment, TimeSlot

class AppointmentForm(forms.ModelForm):
    """Randevu formu"""
    
    # TimeSlot alanını manuel olarak tanımlayın
    appointment_time = forms.ModelChoiceField(
        queryset=TimeSlot.objects.none(),
        empty_label="Önce tarih seçin",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Randevu Saati"
    )
    
    class Meta:
        model = Appointment
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'appointment_date', 'appointment_time', 'appointment_type',
            'age', 'gender', 'height', 'weight',
            'medical_history', 'medications', 'dietary_restrictions', 'goals'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adınız',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Soyadınız',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-posta adresiniz',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+90 555 123 45 67',
                'required': True
            }),
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': timezone.now().date().strftime('%Y-%m-%d'),
                'required': True
            }),
            'appointment_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 15,
                'max': 100,
                'required': True
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 100,
                'max': 250,
                'placeholder': 'cm',
                'required': True
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 30,
                'max': 300,
                'step': '0.1',
                'placeholder': 'kg',
                'required': True
            }),
            'medical_history': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Kronik hastalıklar, alerji vb. (isteğe bağlı)'
            }),
            'medications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Kullandığınız ilaçlar (isteğe bağlı)'
            }),
            'dietary_restrictions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Beslenme kısıtlamalarınız (isteğe bağlı)'
            }),
            'goals': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Hedeflerinizi detaylı olarak açıklayın',
                'required': True
            }),
        }
        
        labels = {
            'first_name': 'Ad *',
            'last_name': 'Soyad *',
            'email': 'E-posta *',
            'phone': 'Telefon *',
            'appointment_date': 'Randevu Tarihi *',
            'appointment_type': 'Randevu Türü *',
            'age': 'Yaş *',
            'gender': 'Cinsiyet *',
            'height': 'Boy (cm) *',
            'weight': 'Kilo (kg) *',
            'medical_history': 'Medikal Geçmiş',
            'medications': 'Kullandığınız İlaçlar',
            'dietary_restrictions': 'Beslenme Kısıtlamaları',
            'goals': 'Hedefleriniz *',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        print("=== FORM INIT DEBUG ===")
        
        # TimeSlot queryset'ini ayarla - hata durumunda varsayılan değerler oluştur
        try:
            timeslots = TimeSlot.objects.filter(is_active=True).order_by('time')
            print(f"Available TimeSlots: {timeslots.count()}")
            
            # Eğer hiç TimeSlot yoksa, varsayılan olanları oluştur
            if timeslots.count() == 0:
                print("No TimeSlots found, creating default ones...")
                self.create_default_timeslots()
                timeslots = TimeSlot.objects.filter(is_active=True).order_by('time')
                
            for ts in timeslots:
                print(f"- TimeSlot ID: {ts.id}, Time: {ts.time}")
            
            self.fields['appointment_time'].queryset = timeslots
            
        except Exception as e:
            print(f"TimeSlot queryset hatası: {e}")
            # Hata durumunda varsayılan timeslot'ları oluşturmaya çalış
            try:
                self.create_default_timeslots()
                timeslots = TimeSlot.objects.filter(is_active=True).order_by('time')
                self.fields['appointment_time'].queryset = timeslots
            except Exception as e2:
                print(f"Default timeslot creation failed: {e2}")
                self.fields['appointment_time'].queryset = TimeSlot.objects.none()
        
        # Tüm zorunlu alanları işaretle
        required_fields = [
            'first_name', 'last_name', 'email', 'phone',
            'appointment_date', 'appointment_time', 'appointment_type',
            'age', 'gender', 'height', 'weight', 'goals'
        ]
        
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                # Widget'a required attribute ekle
                if hasattr(self.fields[field_name].widget, 'attrs'):
                    self.fields[field_name].widget.attrs['required'] = True
        
        # Form helper'ı sadeleştir
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Kişisel Bilgiler',
                Row(
                    Column('first_name', css_class='form-group col-md-6 mb-3'),
                    Column('last_name', css_class='form-group col-md-6 mb-3'),
                ),
                Row(
                    Column('email', css_class='form-group col-md-6 mb-3'),
                    Column('phone', css_class='form-group col-md-6 mb-3'),
                ),
            ),
            Fieldset(
                'Randevu Detayları',
                Row(
                    Column('appointment_date', css_class='form-group col-md-4 mb-3'),
                    Column('appointment_time', css_class='form-group col-md-4 mb-3'),
                    Column('appointment_type', css_class='form-group col-md-4 mb-3'),
                ),
            ),
            Fieldset(
                'Sağlık Bilgileri',
                Row(
                    Column('age', css_class='form-group col-md-3 mb-3'),
                    Column('gender', css_class='form-group col-md-3 mb-3'),
                    Column('height', css_class='form-group col-md-3 mb-3'),
                    Column('weight', css_class='form-group col-md-3 mb-3'),
                ),
                'medical_history',
                'medications', 
                'dietary_restrictions',
            ),
            Fieldset(
                'Hedefleriniz',
                'goals',
            ),
            HTML('<div class="text-center mt-4">'),
            Submit('submit', 'Randevu Talebini Gönder', css_class='btn btn-primary btn-lg px-5'),
            HTML('</div>'),
        )
        
        print("=== REQUIRED FIELDS CHECK ===")
        for field_name, field in self.fields.items():
            print(f"{field_name}: required={field.required}")
    
    def create_default_timeslots(self):
        """Varsayılan zaman dilimlerini oluştur"""
        from datetime import time
        
        default_times = [
            '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
            '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00'
        ]
        
        for time_str in default_times:
            hour, minute = map(int, time_str.split(':'))
            time_obj = time(hour, minute)
            
            timeslot, created = TimeSlot.objects.get_or_create(
                time=time_obj,
                defaults={'is_active': True}
            )
            if created:
                print(f"Created TimeSlot: {time_str}")
    
    def clean_appointment_date(self):
        """Randevu tarihi validasyonu"""
        date = self.cleaned_data.get('appointment_date')
        print(f"DEBUG: Cleaning appointment_date: {date}")
        
        if not date:
            raise forms.ValidationError("Randevu tarihi zorunludur.")
        
        if date < timezone.now().date():
            print(f"DEBUG: Date validation failed - date {date} is in the past")
            raise forms.ValidationError("Geçmiş bir tarihe randevu alınamaz.")
        
        return date
    
    def clean_appointment_time(self):
        """Randevu saati validasyonu"""
        appointment_time = self.cleaned_data.get('appointment_time')
        print(f"DEBUG: Cleaning appointment_time: {appointment_time}")
        
        if not appointment_time:
            print("DEBUG: appointment_time validation failed - no time selected")
            raise forms.ValidationError("Lütfen bir saat seçin.")
        
        return appointment_time
    
    def clean_phone(self):
        """Telefon numarası validasyonu"""
        phone = self.cleaned_data.get('phone')
        if phone:
            import re

            # Tüm rakam dışı karakterleri temizle (parantez, boşluk, tire vb.)
            cleaned_phone = re.sub(r'\D', '', phone)

            # Geçerli telefon numarası uzunluğu ve başlangıcı kontrolü
            if cleaned_phone.startswith('90'):
                cleaned_phone = cleaned_phone[2:]
            elif cleaned_phone.startswith('0'):
                cleaned_phone = cleaned_phone[1:]

            # Son durumda 10 haneli ve 5 ile başlıyor olmalı
            if len(cleaned_phone) != 10 or not cleaned_phone.startswith('5'):
                raise forms.ValidationError("Geçerli bir telefon numarası girin. Örneğin: 05321234567")

            # Temizlenmiş değeri form verisine geri yaz
            self.cleaned_data['phone'] = cleaned_phone

        return self.cleaned_data.get('phone')

    
    def clean_email(self):
        """E-posta validasyonu"""
        email = self.cleaned_data.get('email')
        if email:
            # E-posta formatı kontrolü
            import re
            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                raise forms.ValidationError("Geçerli bir e-posta adresi girin.")
        return email
    
    def clean(self):
        """Form genel validasyonu"""
        cleaned_data = super().clean()
        print(f"DEBUG: Form clean method called")
        print(f"DEBUG: Cleaned data keys: {list(cleaned_data.keys())}")
        
        # Zorunlu alanları kontrol et
        required_fields = [
            'first_name', 'last_name', 'email', 'phone',
            'appointment_date', 'appointment_time', 'appointment_type',
            'age', 'gender', 'height', 'weight', 'goals'
        ]
        
        errors = {}
        
        for field in required_fields:
            value = cleaned_data.get(field)
            if not value:
                errors[field] = f"{field} alanı zorunludur."
                print(f"DEBUG: Required field missing: {field}")
        
        if errors:
            for field, error in errors.items():
                self.add_error(field, error)
        
        # Randevu çakışması kontrolü
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        
        if appointment_date and appointment_time:
            existing = Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=['pending', 'confirmed']
            )
            
            # Güncelleme durumunda mevcut randevuyu hariç tut
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
                
            if existing.exists():
                raise forms.ValidationError("Bu tarih ve saatte başka bir randevu bulunmaktadır.")
        
        print(f"DEBUG: Form validation completed. Errors: {bool(self.errors)}")
        return cleaned_data