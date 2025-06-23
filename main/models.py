# main/models.py

from django.db import models
from ckeditor.fields import RichTextField

class SiteSettings(models.Model):
    """Site genel ayarları"""
    site_title = models.CharField(max_length=200, default="Diyetisyen")
    site_description = models.TextField(default="Profesyonel beslenme danışmanlığı hizmetleri")
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = "Site Ayarları"
        verbose_name_plural = "Site Ayarları"
    
    def __str__(self):
        return self.site_title
    
    def save(self, *args, **kwargs):
        # Sadece bir tane site ayarı objesi olması için
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('Sadece bir site ayarı objesi olabilir.')
        return super().save(*args, **kwargs)

class HomePage(models.Model):
    """Ana sayfa içeriği"""
    hero_title = models.CharField(max_length=200, default="Sağlıklı Yaşam Başlar")
    hero_subtitle = models.CharField(max_length=300, default="Profesyonel beslenme danışmanlığı ile ideal kilonuza ulaşın")
    hero_image = models.ImageField(upload_to='hero/', blank=True)
    
    about_title = models.CharField(max_length=200, default="Hakkımda")
    about_content = RichTextField(default="Profesyonel diyetisyen hizmetleri...")
    about_image = models.ImageField(upload_to='about/', blank=True)
    
    services_title = models.CharField(max_length=200, default="Hizmetlerim")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Ana Sayfa"
        verbose_name_plural = "Ana Sayfa"
    
    def __str__(self):
        return "Ana Sayfa İçeriği"
    
    def save(self, *args, **kwargs):
        # Sadece bir tane ana sayfa objesi olması için
        if not self.pk and HomePage.objects.exists():
            raise ValueError('Sadece bir ana sayfa objesi olabilir.')
        return super().save(*args, **kwargs)

class Service(models.Model):
    """Hizmetler"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class", blank=True)
    image = models.ImageField(upload_to='services/', blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Hizmet"
        verbose_name_plural = "Hizmetler"
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    """Müşteri yorumları"""
    name = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    image = models.ImageField(upload_to='testimonials/', blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Müşteri Yorumu"
        verbose_name_plural = "Müşteri Yorumları"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.rating} yıldız"

class ContactMessage(models.Model):
    """İletişim mesajları"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "İletişim Mesajı"
        verbose_name_plural = "İletişim Mesajları"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"