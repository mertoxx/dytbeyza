# success_stories/urls.py

from django.urls import path
from . import views

app_name = 'success_stories'

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('hikaye/<slug:slug>/', views.story_detail, name='story_detail'),
    path('ara/', views.story_search, name='story_search'),
]