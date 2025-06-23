# success_stories/admin.py

from django.contrib import admin
from .models import SuccessStory, SuccessStoryComment, WeightLossCategory, BeforeAfterComparison

@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'weight_lost', 'duration_months', 'gender', 'is_published', 'is_featured']
    list_filter = ['gender', 'age_range', 'is_published', 'is_featured', 'success_date']
    search_fields = ['client_name', 'title', 'summary']
    
    # Bu alanlar otomatik hesaplanıyor, readonly yapalım
    readonly_fields = ['weight_lost', 'slug', 'views']
    
    # prepopulated_fields'ı tamamen kaldırıyoruz
    # prepopulated_fields = {}  # Bu satırı da kaldırabilirsiniz
    
    fieldsets = (
        ('Kişi Bilgileri', {
            'fields': ('client_name', 'slug', 'age_range', 'gender', 'occupation')
        }),
        ('Kilo Bilgileri', {
            'fields': ('initial_weight', 'final_weight', 'weight_lost', 'duration_months')
        }),
        ('İçerik', {
            'fields': ('title', 'summary', 'story_content')
        }),
        ('Resimler', {
            'fields': ('before_image', 'after_image', 'profile_image')
        }),
        ('Detaylar', {
            'fields': ('initial_goals', 'challenges_faced', 'key_changes', 'client_testimonial', 'health_improvements', 'lifestyle_changes')
        }),
        ('Sistem', {
            'fields': ('author', 'is_featured', 'is_published', 'allow_comments', 'views', 'success_date')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Model kaydedilirken otomatik alanları ayarla"""
        if not change:  # Yeni kayıt ise
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(SuccessStoryComment)
class SuccessStoryCommentAdmin(admin.ModelAdmin):
    list_display = ['story', 'name', 'email', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'comment']
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Seçili yorumları onayla"

@admin.register(WeightLossCategory)
class WeightLossCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'min_weight_loss', 'max_weight_loss', 'color']
    ordering = ['min_weight_loss']

@admin.register(BeforeAfterComparison)
class BeforeAfterComparisonAdmin(admin.ModelAdmin):
    list_display = ['story', 'chest_difference', 'waist_difference', 'hip_difference']