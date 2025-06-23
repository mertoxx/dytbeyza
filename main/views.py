# main/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import HomePage, Service, Testimonial, ContactMessage, SiteSettings
from .forms import ContactForm
from success_stories.models import SuccessStory
from recipes.models import Recipe

def home(request):
    """Ana sayfa"""
    try:
        homepage = HomePage.objects.first()
    except HomePage.DoesNotExist:
        homepage = None
    
    # Aktif hizmetler
    services = Service.objects.filter(is_active=True)[:6]
    
    # Son başarı hikayeleri
    success_stories = SuccessStory.objects.filter(
        is_published=True
    ).order_by('-created_at')[:3]
    
    # Öne çıkan tarifler
    featured_recipes = Recipe.objects.filter(
        is_published=True, 
        is_featured=True
    )[:4]
    
    # Müşteri yorumları
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    context = {
        'homepage': homepage,
        'services': services,
        'success_stories': success_stories,
        'featured_recipes': featured_recipes,
        'testimonials': testimonials,
    }
    
    return render(request, 'main/home.html', context)

def about(request):
    """Hakkımda sayfası"""
    try:
        homepage = HomePage.objects.first()
    except HomePage.DoesNotExist:
        homepage = None
    
    # Tüm hizmetler
    services = Service.objects.filter(is_active=True)
    
    # İstatistikler
    stats = {
        'total_success_stories': SuccessStory.objects.filter(is_published=True).count(),
        'total_recipes': Recipe.objects.filter(is_published=True).count(),
        'total_weight_lost': sum([
            story.weight_lost for story in SuccessStory.objects.filter(is_published=True)
        ]),
        'happy_clients': SuccessStory.objects.filter(is_published=True).count(),
    }
    
    context = {
        'homepage': homepage,
        'services': services,
        'stats': stats,
    }
    
    return render(request, 'main/about.html', context)

def services(request):
    """Hizmetler sayfası"""
    services = Service.objects.filter(is_active=True)
    
    context = {
        'services': services,
    }
    
    return render(request, 'main/services.html', context)

def service_detail(request, service_id):
    """Hizmet detay sayfası"""
    service = get_object_or_404(Service, id=service_id, is_active=True)
    
    # İlgili başarı hikayeleri
    related_stories = SuccessStory.objects.filter(
        is_published=True
    )[:3]
    
    context = {
        'service': service,
        'related_stories': related_stories,
    }
    
    return render(request, 'main/service_detail.html', context)

def contact(request):
    """İletişim sayfası"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Form verilerini kaydet
            contact_message = form.save()
            
            # E-posta gönder (isteğe bağlı)
            try:
                send_mail(
                    subject=f'Yeni İletişim: {contact_message.subject}',
                    message=f"""
                    Ad: {contact_message.name}
                    E-posta: {contact_message.email}
                    Konu: {contact_message.subject}
                    
                    Mesaj:
                    {contact_message.message}
                    """,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=True,
                )
            except:
                pass
            
            messages.success(
                request, 
                'Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.'
            )
            return redirect('main:contact')
    else:
        form = ContactForm()
    
    # Site ayarları
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    context = {
        'form': form,
        'site_settings': site_settings,
    }
    
    return render(request, 'main/contact.html', context)

def search(request):
    """Arama sayfası"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Tariflerde ara
        recipe_results = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query),
            is_published=True
        )[:10]
        
        # Başarı hikayelerinde ara
        story_results = SuccessStory.objects.filter(
            Q(title__icontains=query) |
            Q(client_name__icontains=query) |
            Q(summary__icontains=query),
            is_published=True
        )[:10]
        
        # Hizmetlerde ara
        service_results = Service.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query),
            is_active=True
        )[:5]
        
        # Sonuçları birleştir
        results = {
            'recipes': recipe_results,
            'stories': story_results,
            'services': service_results,
            'total_count': len(recipe_results) + len(story_results) + len(service_results)
        }
    
    context = {
        'query': query,
        'results': results,
    }
    
    return render(request, 'main/search.html', context)

def privacy_policy(request):
    """Gizlilik politikası"""
    return render(request, 'main/privacy_policy.html')

def terms_of_service(request):
    """Kullanım şartları"""
    return render(request, 'main/terms_of_service.html')