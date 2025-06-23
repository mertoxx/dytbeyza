# recipes/admin.py

from django.contrib import admin
from .models import RecipeCategory, Recipe, RecipeImage, RecipeRating

class RecipeImageInline(admin.TabularInline):
    model = RecipeImage
    extra = 1

@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'is_active', 'order']
    list_editable = ['color', 'is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'difficulty', 'meal_type', 
        'is_featured', 'is_published', 'views', 'created_at'
    ]
    list_filter = [
        'category', 'difficulty', 'meal_type', 'is_featured', 
        'is_published', 'is_vegetarian', 'is_vegan', 'is_gluten_free'
    ]
    search_fields = ['title', 'description', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']
    list_editable = ['is_featured', 'is_published']
    inlines = [RecipeImageInline]
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': (
                'title', 'slug', 'category', 'description', 'image'
            )
        }),
        ('Tarif İçeriği', {
            'fields': ('ingredients', 'instructions')
        }),
        ('Tarif Detayları', {
            'fields': (
                ('prep_time', 'cook_time', 'servings'),
                ('difficulty', 'meal_type')
            )
        }),
        ('Beslenme Bilgileri', {
            'fields': (
                'calories_per_serving',
                ('protein', 'carbs', 'fat', 'fiber')
            ),
            'classes': ('collapse',)
        }),
        ('Etiketler ve Özellikler', {
            'fields': (
                'tags',
                ('is_vegetarian', 'is_vegan'),
                ('is_gluten_free', 'is_low_carb', 'is_high_protein')
            )
        }),
        ('Yayın Ayarları', {
            'fields': (
                ('author', 'is_featured', 'is_published'),
                ('views', 'created_at', 'updated_at')
            )
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Yeni kayıt
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(RecipeRating)
class RecipeRatingAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'name', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['recipe__title', 'name', 'comment']
    list_editable = ['is_approved']