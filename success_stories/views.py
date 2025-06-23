# success_stories/views.py

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import SuccessStory, SuccessStoryComment, WeightLossCategory
from .forms import SuccessStoryCommentForm

def story_list(request):
    """Başarı hikayesi listesi"""
    stories = SuccessStory.objects.filter(is_published=True)
    
    # Filtreleme
    gender = request.GET.get('gender')
    age_range = request.GET.get('age_range')
    weight_category = request.GET.get('weight_category')
    
    if gender:
        stories = stories.filter(gender=gender)
    
    if age_range:
        stories = stories.filter(age_range=age_range)
    
    if weight_category:
        category = get_object_or_404(WeightLossCategory, id=weight_category)
        stories = stories.filter(
            weight_lost__gte=category.min_weight_loss,
            weight_lost__lte=category.max_weight_loss or 999
        )
    
    # Sıralama
    sort_by = request.GET.get('sort', '-success_date')
    if sort_by == 'weight_lost':
        stories = stories.order_by('-weight_lost')
    elif sort_by == 'duration':
        stories = stories.order_by('duration_months')
    else:
        stories = stories.order_by(sort_by)
    
    # Sayfalama
    paginator = Paginator(stories, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Kategoriler
    weight_categories = WeightLossCategory.objects.all()
    
    # İstatistikler
    stats = {
        'total_stories': stories.count(),
        'total_weight_lost': sum([story.weight_lost for story in stories]),
        'average_duration': sum([story.duration_months for story in stories]) / stories.count() if stories.count() > 0 else 0,
    }
    
    context = {
        'page_obj': page_obj,
        'weight_categories': weight_categories,
        'stats': stats,
        'gender': gender,
        'age_range': age_range,
        'weight_category': weight_category,
        'sort_by': sort_by,
    }
    
    return render(request, 'success_stories/story_list.html', context)

def story_detail(request, slug):
    """Başarı hikayesi detayı"""
    story = get_object_or_404(SuccessStory, slug=slug, is_published=True)
    
    # Görüntülenme sayısını artır
    story.increment_views()
    
    # İlgili hikayeler
    related_stories = SuccessStory.objects.filter(
        Q(gender=story.gender) | Q(age_range=story.age_range),
        is_published=True
    ).exclude(id=story.id)[:3]
    
    # Yorumlar
    comments = story.comments.filter(is_approved=True).order_by('-created_at')
    
    # Yorum formu
    comment_form = SuccessStoryCommentForm()
    
    if request.method == 'POST' and story.allow_comments:
        comment_form = SuccessStoryCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.story = story
            comment.save()
            messages.success(request, 'Yorumunuz başarıyla gönderildi. Onaylandıktan sonra yayınlanacaktır.')
            return redirect('success_stories:story_detail', slug=story.slug)
    
    context = {
        'story': story,
        'related_stories': related_stories,
        'comments': comments,
        'comment_form': comment_form,
    }
    
    return render(request, 'success_stories/story_detail.html', context)

def story_search(request):
    """Hikaye arama"""
    query = request.GET.get('q', '')
    stories = []
    
    if query:
        stories = SuccessStory.objects.filter(
            Q(client_name__icontains=query) |
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(story_content__icontains=query),
            is_published=True
        ).order_by('-success_date')
    
    # Sayfalama
    paginator = Paginator(stories, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    
    return render(request, 'success_stories/story_search.html', context)