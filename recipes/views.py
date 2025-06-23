# recipes/views.py

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Recipe, RecipeCategory, RecipeRating
from .forms import RecipeRatingForm

def recipe_list(request, category_slug=None):
    """Tarif listesi"""
    recipes = Recipe.objects.filter(is_published=True)
    
    # Kategori filtresi
    category = None
    if category_slug:
        category = get_object_or_404(RecipeCategory, slug=category_slug, is_active=True)
        recipes = recipes.filter(category=category)
    
    # Filtreleme
    meal_type = request.GET.get('meal_type')
    difficulty = request.GET.get('difficulty')
    dietary_filters = request.GET.getlist('dietary')
    
    if meal_type:
        recipes = recipes.filter(meal_type=meal_type)
    
    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)
    
    if 'vegetarian' in dietary_filters:
        recipes = recipes.filter(is_vegetarian=True)
    if 'vegan' in dietary_filters:
        recipes = recipes.filter(is_vegan=True)
    if 'gluten_free' in dietary_filters:
        recipes = recipes.filter(is_gluten_free=True)
    
    # Sıralama
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'popular':
        recipes = recipes.order_by('-views')
    elif sort_by == 'rating':
        recipes = recipes.order_by('-id')  # Rating sistem geliştirildiğinde değişir
    else:
        recipes = recipes.order_by(sort_by)
    
    # Sayfalama
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Kategoriler
    categories = RecipeCategory.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'category': category,
        'categories': categories,
        'meal_type': meal_type,
        'difficulty': difficulty,
        'dietary_filters': dietary_filters,
        'sort_by': sort_by,
    }
    
    return render(request, 'recipes/recipe_list.html', context)

def recipe_detail(request, slug):
    """Tarif detayı"""
    recipe = get_object_or_404(Recipe, slug=slug, is_published=True)
    
    # Görüntülenme sayısını artır
    recipe.increment_views()
    
    # İlgili tarifler
    related_recipes = Recipe.objects.filter(
        category=recipe.category,
        is_published=True
    ).exclude(id=recipe.id)[:4]
    
    # Yorumlar
    ratings = recipe.ratings.filter(is_approved=True).order_by('-created_at')
    
    # Yorum formu
    rating_form = RecipeRatingForm()
    
    if request.method == 'POST':
        rating_form = RecipeRatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.recipe = recipe
            rating.save()
            messages.success(request, 'Yorumunuz başarıyla gönderildi. Onaylandıktan sonra yayınlanacaktır.')
            return redirect('recipes:recipe_detail', slug=recipe.slug)
    
    context = {
        'recipe': recipe,
        'related_recipes': related_recipes,
        'ratings': ratings,
        'rating_form': rating_form,
    }
    
    return render(request, 'recipes/recipe_detail.html', context)

def recipe_search(request):
    """Tarif arama"""
    query = request.GET.get('q', '')
    recipes = []
    
    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(tags__icontains=query),
            is_published=True
        ).order_by('-created_at')
    
    # Sayfalama
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    
    return render(request, 'recipes/recipe_search.html', context)
