# main/admin.py - Debug versiyonu

from django.contrib import admin
from .models import SiteSettings, HomePage, Service, Testimonial, ContactMessage

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_title', 'phone', 'email']
    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('site_title', 'site_description')
        }),
        ('İletişim Bilgileri', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Sosyal Medya', {
            'fields': ('facebook_url', 'instagram_url', 'linkedin_url', 'whatsapp_number')
        }),
    )

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    # Verbose name ekleyelim
    verbose_name = "Ana Sayfa İçeriği"
    verbose_name_plural = "Ana Sayfa İçeriği"
    
    list_display = ['hero_title', 'about_title', 'updated_at']
    
    fieldsets = (
        ('Hero Bölümü', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image'),
            'description': 'Ana sayfanın üst bölümündeki içerikler'
        }),
        ('Hakkımda Bölümü', {
            'fields': ('about_title', 'about_content', 'about_image'),
            'description': 'Hakkımda bölümünün içerikleri - Bu bölümü düzenleyebilirsiniz'
        }),
        ('Hizmetler Bölümü', {
            'fields': ('services_title',),
            'description': 'Hizmetler bölümünün başlığı'
        }),
    )
    
    # Sadece bir HomePage olmasını sağla
    def has_add_permission(self, request):
        if HomePage.objects.exists():
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    # Eğer HomePage yoksa otomatik oluştur
    def changelist_view(self, request, extra_context=None):
        if not HomePage.objects.exists():
            HomePage.objects.create(
                hero_title="Sağlıklı Yaşam Başlar",
                hero_subtitle="Profesyonel beslenme danışmanlığı ile ideal kilonuza ulaşın",
                about_title="Hakkımda",
                about_content="""
                <h3>Merhaba!</h3>
                <p>Beslenme ve Diyetetik alanında uzman olarak, her bireyin özgün ihtiyaçlarına uygun beslenme programları hazırlıyorum.</p>
                <p>Bilimsel veriler ışığında, sürdürülebilir ve sağlıklı yaşam tarzı oluşturmanıza yardımcı oluyorum.</p>
                <h4>Neden Benimle Çalışmalısınız?</h4>
                <ul>
                    <li><strong>5+ Yıl Deneyim:</strong> Beslenme alanında geniş tecrübe</li>
                    <li><strong>Kişiselleştirilmiş Programlar:</strong> Size özel çözümler</li>
                    <li><strong>Bilimsel Yaklaşım:</strong> Kanıta dayalı beslenme önerileri</li>
                    <li><strong>7/24 Destek:</strong> WhatsApp üzerinden sürekli iletişim</li>
                </ul>
                <p>Sağlıklı yaşam yolculuğunuzda size rehberlik etmek için buradayım.</p>
                """,
                services_title="Hizmetlerim"
            )
        return super().changelist_view(request, extra_context)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'title']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['name', 'content']
    list_editable = ['is_active']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Seçilenleri okundu olarak işaretle"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Seçilenleri okunmadı olarak işaretle"

# Debug: Admin'de kayıtlı modelleri yazdır
print("Admin'de kayıtlı modeller:")
for model, admin_class in admin.site._registry.items():
    print(f"- {model.__name__}: {admin_class.__class__.__name__}")