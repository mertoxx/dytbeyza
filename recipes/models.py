# recipes/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class RecipeCategory(models.Model):
    """Tarif kategorileri"""
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Açıklama")
    color = models.CharField(
        max_length=7, 
        default="#007bff",
        verbose_name="Renk",
        help_text="Hex renk kodu (#ffffff)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tarif Kategorisi"
        verbose_name_plural = "Tarif Kategorileri"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Recipe(models.Model):
    """Yemek tarifleri"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Kolay'),
        ('medium', 'Orta'),
        ('hard', 'Zor'),
    ]
    
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Kahvaltı'),
        ('lunch', 'Öğle Yemeği'),
        ('dinner', 'Akşam Yemeği'),
        ('snack', 'Atıştırmalık'),
        ('dessert', 'Tatlı'),
        ('drink', 'İçecek'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Tarif Adı")
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        RecipeCategory, 
        on_delete=models.CASCADE, 
        verbose_name="Kategori"
    )
    description = models.TextField(verbose_name="Kısa Açıklama")
    image = models.ImageField(upload_to='recipes/', verbose_name="Ana Resim")
    
    # Tarif Detayları
    ingredients = RichTextField(verbose_name="Malzemeler")
    instructions = RichTextField(verbose_name="Yapılışı")
    
    # Numerik Bilgiler
    prep_time = models.PositiveIntegerField(verbose_name="Hazırlık Süresi (dakika)")
    cook_time = models.PositiveIntegerField(verbose_name="Pişirme Süresi (dakika)")
    servings = models.PositiveIntegerField(verbose_name="Kaç Kişilik")
    difficulty = models.CharField(
        max_length=10, 
        choices=DIFFICULTY_CHOICES,
        default='easy',
        verbose_name="Zorluk"
    )
    meal_type = models.CharField(
        max_length=15, 
        choices=MEAL_TYPE_CHOICES,
        verbose_name="Öğün Türü"
    )
    
    # Beslenme Bilgileri
    calories_per_serving = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name="Porsiyon Başı Kalori"
    )
    protein = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Protein (g)"
    )
    carbs = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Karbonhidrat (g)"
    )
    fat = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Yağ (g)"
    )
    fiber = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Lif (g)"
    )
    
    # Etiketler ve Özellikler
    tags = models.CharField(
        max_length=300, 
        blank=True,
        verbose_name="Etiketler",
        help_text="Virgülle ayırın (ör: vegan, glutensiz, düşük kalorili)"
    )
    is_vegetarian = models.BooleanField(default=False, verbose_name="Vejetaryen")
    is_vegan = models.BooleanField(default=False, verbose_name="Vegan")
    is_gluten_free = models.BooleanField(default=False, verbose_name="Glutensiz")
    is_low_carb = models.BooleanField(default=False, verbose_name="Düşük Karbonhidratlı")
    is_high_protein = models.BooleanField(default=False, verbose_name="Yüksek Proteinli")
    
    # Sistem Alanları
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Yazar"
    )
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan")
    is_published = models.BooleanField(default=True, verbose_name="Yayınlanmış")
    views = models.PositiveIntegerField(default=0, verbose_name="Görüntülenme")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Tarif"
        verbose_name_plural = "Tarifler"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'slug': self.slug})
    
    @property
    def total_time(self):
        """Toplam süre"""
        return self.prep_time + self.cook_time
    
    @property
    def tag_list(self):
        """Etiket listesi"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def increment_views(self):
        """Görüntülenme sayısını artır"""
        self.views += 1
        self.save(update_fields=['views'])

class RecipeImage(models.Model):
    """Tarif ek resimleri"""
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='additional_images'
    )
    image = models.ImageField(upload_to='recipes/gallery/')
    caption = models.CharField(max_length=200, blank=True, verbose_name="Açıklama")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    
    class Meta:
        verbose_name = "Tarif Resmi"
        verbose_name_plural = "Tarif Resimleri"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.recipe.title} - Resim {self.order}"

class RecipeRating(models.Model):
    """Tarif değerlendirmeleri"""
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='ratings'
    )
    name = models.CharField(max_length=100, verbose_name="İsim")
    email = models.EmailField(verbose_name="E-posta")
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)], 
        verbose_name="Puan"
    )
    comment = models.TextField(blank=True, verbose_name="Yorum")
    is_approved = models.BooleanField(default=False, verbose_name="Onaylanmış")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tarif Değerlendirmesi"
        verbose_name_plural = "Tarif Değerlendirmeleri"
        ordering = ['-created_at']
        unique_together = ['recipe', 'email']
    
    def __str__(self):
        return f"{self.recipe.title} - {self.name} ({self.rating}/5)"