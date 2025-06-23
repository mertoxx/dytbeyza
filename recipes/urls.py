from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('kategori/<slug:category_slug>/', views.recipe_list, name='recipe_list_by_category'),
    path('tarif/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('ara/', views.recipe_search, name='recipe_search'),
]