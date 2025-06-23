# main/context_processors.py

from .models import SiteSettings, Service
from recipes.models import RecipeCategory
from success_stories.models import SuccessStory

def site_context(request):
    """Global site context"""
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    # Navigation için kategoriler
    recipe_categories = RecipeCategory.objects.filter(is_active=True)[:6]
    
    # Footer için son başarı hikayeleri
    recent_stories = SuccessStory.objects.filter(
        is_published=True
    ).order_by('-created_at')[:3]
    
    return {
        'site_settings': site_settings,
        'recipe_categories': recipe_categories,
        'recent_stories': recent_stories,
    }