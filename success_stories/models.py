# success_stories/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class SuccessStory(models.Model):
    """Başarı hikayeleri"""
    GENDER_CHOICES = [
        ('male', 'Erkek'),
        ('female', 'Kadın'),
    ]
    
    AGE_RANGE_CHOICES = [
        ('18-25', '18-25 yaş'),
        ('26-35', '26-35 yaş'),
        ('36-45', '36-45 yaş'),
        ('46-55', '46-55 yaş'),
        ('56+', '56+ yaş'),
    ]
    
    # Kişi Bilgileri
    client_name = models.CharField(max_length=100, verbose_name="Müşteri Adı")
    slug = models.SlugField(unique=True, blank=True)
    age_range = models.CharField(
        max_length=10, 
        choices=AGE_RANGE_CHOICES,
        verbose_name="Yaş Aralığı"
    )
    gender = models.CharField(
        max_length=10, 
        choices=GENDER_CHOICES,
        verbose_name="Cinsiyet"
    )
    occupation = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Meslek"
    )
    
    # Başarı Verileri
    initial_weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name="Başlangıç Kilosu (kg)"
    )
    final_weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name="Son Kilo (kg)"
    )
    weight_lost = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name="Verilen Kilo (kg)"
    )
    duration_months = models.PositiveIntegerField(verbose_name="Süre (ay)")
    
    # İçerik
    title = models.CharField(max_length=200, verbose_name="Başlık")
    summary = models.TextField(verbose_name="Özet")
    story_content = RichTextField(verbose_name="Hikaye İçeriği")
    
    # Resimler
    before_image = models.ImageField(
        upload_to='success_stories/before/', 
        verbose_name="Öncesi Resmi"
    )
    after_image = models.ImageField(
        upload_to='success_stories/after/', 
        verbose_name="Sonrası Resmi"
    )
    profile_image = models.ImageField(
        upload_to='success_stories/profiles/', 
        blank=True,
        verbose_name="Profil Resmi"
    )
    
    # Hedefler ve Zorluklar
    initial_goals = models.TextField(verbose_name="Başlangıç Hedefleri")
    challenges_faced = models.TextField(
        blank=True, 
        verbose_name="Karşılaştığı Zorluklar"
    )
    key_changes = models.TextField(verbose_name="Yapılan Ana Değişiklikler")
    
    # Müşteri Yorumu
    client_testimonial = models.TextField(verbose_name="Müşteri Yorumu")
    
    # Ek Başarılar
    health_improvements = models.TextField(
        blank=True, 
        verbose_name="Sağlık İyileştirmeleri"
    )
    lifestyle_changes = models.TextField(
        blank=True, 
        verbose_name="Yaşam Tarzı Değişiklikleri"
    )
    
    # Sistem Alanları
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Yazar"
    )
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan")
    is_published = models.BooleanField(default=True, verbose_name="Yayınlanmış")
    allow_comments = models.BooleanField(default=True, verbose_name="Yorum Kabul Et")
    views = models.PositiveIntegerField(default=0, verbose_name="Görüntülenme")
    
    # Tarihler
    success_date = models.DateField(verbose_name="Başarı Tarihi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Başarı Hikayesi"
        verbose_name_plural = "Başarı Hikayeleri"
        ordering = ['-success_date', '-created_at']
    
    def __str__(self):
        return f"{self.client_name} - {self.weight_lost}kg"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.client_name}-{self.weight_lost}kg")
        
        # Verilen kiloyu otomatik hesapla
        if self.initial_weight and self.final_weight:
            self.weight_lost = self.initial_weight - self.final_weight
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('success_stories:story_detail', kwargs={'slug': self.slug})
    
    @property
    def weight_loss_percentage(self):
        """Kilo kaybı yüzdesi"""
        if self.initial_weight:
            return round((self.weight_lost / self.initial_weight) * 100, 1)
        return 0
    
    @property
    def monthly_average_loss(self):
        """Aylık ortalama kilo kaybı"""
        if self.duration_months:
            return round(self.weight_lost / self.duration_months, 2)
        return 0
    
    def increment_views(self):
        """Görüntülenme sayısını artır"""
        self.views += 1
        self.save(update_fields=['views'])

class SuccessStoryComment(models.Model):
    """Başarı hikayesi yorumları"""
    story = models.ForeignKey(
        SuccessStory, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    name = models.CharField(max_length=100, verbose_name="İsim")
    email = models.EmailField(verbose_name="E-posta")
    comment = models.TextField(verbose_name="Yorum")
    is_approved = models.BooleanField(default=False, verbose_name="Onaylanmış")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Hikaye Yorumu"
        verbose_name_plural = "Hikaye Yorumları"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.story.client_name} - {self.name}"

class WeightLossCategory(models.Model):
    """Kilo verme kategorileri"""
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    min_weight_loss = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name="Minimum Kilo Kaybı"
    )
    max_weight_loss = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Maksimum Kilo Kaybı"
    )
    color = models.CharField(
        max_length=7, 
        default="#28a745",
        verbose_name="Renk"
    )
    description = models.TextField(blank=True, verbose_name="Açıklama")
    
    class Meta:
        verbose_name = "Kilo Kaybı Kategorisi"
        verbose_name_plural = "Kilo Kaybı Kategorileri"
        ordering = ['min_weight_loss']
    
    def __str__(self):
        if self.max_weight_loss:
            return f"{self.name} ({self.min_weight_loss}-{self.max_weight_loss}kg)"
        return f"{self.name} ({self.min_weight_loss}kg+)"

class BeforeAfterComparison(models.Model):
    """Önce-sonra karşılaştırmaları"""
    story = models.OneToOneField(
        SuccessStory, 
        on_delete=models.CASCADE, 
        related_name='comparison'
    )
    
    # Vücut ölçüleri - Öncesi
    before_chest = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Göğüs (cm) - Öncesi"
    )
    before_waist = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Bel (cm) - Öncesi"
    )
    before_hip = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Kalça (cm) - Öncesi"
    )
    
    # Vücut ölçüleri - Sonrası
    after_chest = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Göğüs (cm) - Sonrası"
    )
    after_waist = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Bel (cm) - Sonrası"
    )
    after_hip = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Kalça (cm) - Sonrası"
    )
    
    # Sağlık göstergeleri
    before_bmi = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="BMI - Öncesi"
    )
    after_bmi = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="BMI - Sonrası"
    )
    
    class Meta:
        verbose_name = "Önce-Sonra Karşılaştırması"
        verbose_name_plural = "Önce-Sonra Karşılaştırmaları"
    
    def __str__(self):
        return f"{self.story.client_name} - Karşılaştırma"
    
    @property
    def chest_difference(self):
        if self.before_chest and self.after_chest:
            return self.before_chest - self.after_chest
        return None
    
    @property
    def waist_difference(self):
        if self.before_waist and self.after_waist:
            return self.before_waist - self.after_waist
        return None
    
    @property
    def hip_difference(self):
        if self.before_hip and self.after_hip:
            return self.before_hip - self.after_hip
        return None
    
    @property
    def bmi_difference(self):
        """BMI farkını hesapla"""
        if self.before_bmi and self.after_bmi:
            return self.before_bmi - self.after_bmi
        return None
    
    class Meta:
        verbose_name = "Önce-Sonra Karşılaştırması"
        verbose_name_plural = "Önce-Sonra Karşılaştırmaları"
    
    def __str__(self):
        return f"{self.story.client_name} - Karşılaştırma"
    
    @property
    def chest_difference(self):
        if self.before_chest and self.after_chest:
            return self.before_chest - self.after_chest
        return None
    
    @property
    def waist_difference(self):
        if self.before_waist and self.after_waist:
            return self.before_waist - self.after_waist
        return None
    
    @property
    def hip_difference(self):
        if self.before_hip and self.after_hip:
            return self.before_hip - self.after_hip
        return None