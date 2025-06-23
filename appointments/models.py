# appointments/models.py

from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime, timedelta

# appointments/models.py
class TimeSlot(models.Model):
    time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['time']
    
    def __str__(self):
        return self.time.strftime('%H:%M')
        
class Appointment(models.Model):
    """Randevular"""
    STATUS_CHOICES = [
        ('pending', 'Onay Bekliyor'),
        ('confirmed', 'Onaylandı'),
        ('cancelled', 'İptal Edildi'),
        ('completed', 'Tamamlandı'),
    ]
    
    APPOINTMENT_TYPE_CHOICES = [
        ('first_consultation', 'İlk Konsültasyon'),
        ('follow_up', 'Kontrol Randevusu'),
        ('online', 'Online Görüşme'),
        ('group_session', 'Grup Seansı'),
    ]
    
    # Kişisel Bilgiler
    first_name = models.CharField(max_length=50, verbose_name="Ad")
    last_name = models.CharField(max_length=50, verbose_name="Soyad")
    email = models.EmailField(verbose_name="E-posta")
    phone_regex = RegexValidator(
        regex=r'^(?:\+90|0)?\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2}$',
        message="Telefon numarası '+90 5xx xxx xx xx' veya '05xx xxx xx xx' formatında olmalıdır."
    )

    phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        verbose_name="Telefon"
    )
    
    # Randevu Detayları
    appointment_date = models.DateField(verbose_name="Randevu Tarihi")
    appointment_time = models.ForeignKey(
        TimeSlot, 
        on_delete=models.CASCADE,
        null=True,  # Bu önemli
        blank=True  # Bu da önemli
    )
    appointment_type = models.CharField(
        max_length=20, 
        choices=APPOINTMENT_TYPE_CHOICES,
        default='first_consultation',
        verbose_name="Randevu Türü"
    )
    
    # Sağlık Bilgileri
    age = models.PositiveIntegerField(verbose_name="Yaş")
    gender = models.CharField(
        max_length=10, 
        choices=[('male', 'Erkek'), ('female', 'Kadın')],
        verbose_name="Cinsiyet"
    )
    height = models.PositiveIntegerField(verbose_name="Boy (cm)")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Kilo (kg)")
    
    # Medikal Geçmiş
    medical_history = models.TextField(
        blank=True, 
        verbose_name="Medikal Geçmiş",
        help_text="Kronik hastalıklar, alerji vb."
    )
    medications = models.TextField(
        blank=True, 
        verbose_name="Kullandığı İlaçlar"
    )
    dietary_restrictions = models.TextField(
        blank=True, 
        verbose_name="Beslenme Kısıtlamaları"
    )
    
    # Hedefler
    goals = models.TextField(verbose_name="Hedefler")
    
    # Sistem Alanları
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Durum"
    )
    notes = models.TextField(blank=True, verbose_name="Notlar")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Randevu"
        verbose_name_plural = "Randevular"
        ordering = ['-appointment_date', '-appointment_time__time']
        unique_together = ['appointment_date', 'appointment_time']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.appointment_date} {self.appointment_time}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def bmi(self):
        """BMI hesaplama"""
        height_m = self.height / 100
        return round(float(self.weight) / (height_m ** 2), 2)
    
    @property
    def is_past_due(self):
        """Randevu geçmiş mi?"""
        if not self.appointment_time:
            return False  # Randevu saati yoksa geçmiş değildir
        
        appointment_datetime = datetime.combine(
            self.appointment_date,
            self.appointment_time.time
        )
        return timezone.now() > timezone.make_aware(appointment_datetime)

    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Geçmiş tarih kontrolü
        if self.appointment_date < timezone.now().date():
            raise ValidationError("Geçmiş bir tarihe randevu alınamaz.")
        
        # Aynı gün ve saatte başka randevu var mı?
        existing = Appointment.objects.filter(
            appointment_date=self.appointment_date,
            appointment_time=self.appointment_time,
            status__in=['pending', 'confirmed']
        ).exclude(pk=self.pk)
        
        if existing.exists():
            raise ValidationError("Bu tarih ve saatte başka bir randevu bulunmaktadır.")

class AppointmentSettings(models.Model):
    """Randevu ayarları"""
    max_days_ahead = models.PositiveIntegerField(
        default=30, 
        verbose_name="Kaç gün öncesinden randevu alınabilir"
    )
    min_hours_ahead = models.PositiveIntegerField(
        default=24, 
        verbose_name="Kaç saat öncesinden randevu alınabilir"
    )
    working_days = models.CharField(
        max_length=50, 
        default="1,2,3,4,5",  # Pazartesi-Cuma
        verbose_name="Çalışma Günleri",
        help_text="1=Pazartesi, 2=Salı, ... 7=Pazar"
    )
    
    class Meta:
        verbose_name = "Randevu Ayarları"
        verbose_name_plural = "Randevu Ayarları"
    
    def __str__(self):
        return "Randevu Ayarları"
    
    def get_working_days_list(self):
        return [int(day) for day in self.working_days.split(',')]