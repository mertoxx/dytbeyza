# diyetisyen_website/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('randevular/', include('appointments.urls')),
    path('tarifler/', include('recipes.urls')),
    path('basari-hikayeleri/', include('success_stories.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Media files için URL pattern (development için)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])