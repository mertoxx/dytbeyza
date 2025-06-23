# main/management/commands/create_sample_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import SiteSettings, HomePage, Service, Testimonial
from appointments.models import TimeSlot, AppointmentSettings
from recipes.models import RecipeCategory
from success_stories.models import WeightLossCategory

class Command(BaseCommand):
    help = 'Creates sample data for the website'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Site ayarları
        site_settings, created = SiteSettings.objects.get_or_create(
            defaults={
                'site_title': 'Diyetisyen Uzmanı',
                'site_description': 'Profesyonel beslenme danışmanlığı hizmetleri',
                'phone': '+90 555 123 45 67',
                'email': 'info@diyetisyen.com',
                'address': 'İstanbul, Türkiye',
                'whatsapp_number': '+905551234567',
            }
        )
        if created:
            self.stdout.write('✓ Site ayarları oluşturuldu')
        
        # Ana sayfa
        homepage, created = HomePage.objects.get_or_create(
            defaults={
                'hero_title': 'Sağlıklı Yaşam Başlar',
                'hero_subtitle': 'Profesyonel beslenme danışmanlığı ile ideal kilonuza ulaşın',
                'about_title': 'Hakkımda',
                'about_content': '''
                <p>Beslenme ve Diyetetik alanında uzman olarak, her bireyin özgün ihtiyaçlarına uygun beslenme programları hazırlıyorum.</p>
                <p>Bilimsel veriler ışığında, sürdürülebilir ve sağlıklı yaşam tarzı oluşturmanıza yardımcı oluyorum.</p>
                ''',
                'services_title': 'Hizmetlerim',
            }
        )
        if created:
            self.stdout.write('✓ Ana sayfa içeriği oluşturuldu')
        
        # Hizmetler
        services_data = [
            {
                'title': 'Bireysel Beslenme Danışmanlığı',
                'description': 'Size özel hazırlanmış beslenme programı ile hedeflerinize ulaşın.',
                'icon': 'fas fa-user-md',
                'order': 1
            },
            {
                'title': 'Online Konsültasyon',
                'description': 'Uzaktan beslenme danışmanlığı hizmeti ile evden çıkmadan destek alın.',
                'icon': 'fas fa-video',
                'order': 2
            },
            {
                'title': 'Grup Seansları',
                'description': 'Grup halinde motivasyon artırıcı beslenme eğitimleri.',
                'icon': 'fas fa-users',
                'order': 3
            },
            {
                'title': 'Spor Beslenmesi',
                'description': 'Atletler ve sporcular için özel performans artırıcı beslenme programları.',
                'icon': 'fas fa-dumbbell',
                'order': 4
            }
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'✓ Hizmet oluşturuldu: {service.title}')
        
        # Randevu saatleri
        time_slots = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00']
        for time_str in time_slots:
            time_slot, created = TimeSlot.objects.get_or_create(
                time=time_str,
                defaults={'is_active': True}
            )
            if created:
                self.stdout.write(f'✓ Randevu saati oluşturuldu: {time_str}')
        
        # Randevu ayarları
        appointment_settings, created = AppointmentSettings.objects.get_or_create(
            defaults={
                'max_days_ahead': 30,
                'min_hours_ahead': 24,
                'working_days': '1,2,3,4,5',
            }
        )
        if created:
            self.stdout.write('✓ Randevu ayarları oluşturuldu')
        
        # Tarif kategorileri
        recipe_categories = [
            {'name': 'Kahvaltı', 'color': '#ff6b6b'},
            {'name': 'Ana Yemek', 'color': '#4ecdc4'},
            {'name': 'Ara Öğün', 'color': '#45b7d1'},
            {'name': 'Tatlı', 'color': '#f9ca24'},
            {'name': 'Smoothie', 'color': '#6c5ce7'},
            {'name': 'Salata', 'color': '#00b894'},
        ]
        
        for cat_data in recipe_categories:
            category, created = RecipeCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'color': cat_data['color'],
                    'is_active': True,
                    'order': recipe_categories.index(cat_data) + 1
                }
            )
            if created:
                self.stdout.write(f'✓ Tarif kategorisi oluşturuldu: {category.name}')
        
        # Kilo kaybı kategorileri
        weight_categories = [
            {'name': '5-10 kg', 'min_weight_loss': 5, 'max_weight_loss': 10, 'color': '#28a745'},
            {'name': '10-20 kg', 'min_weight_loss': 10, 'max_weight_loss': 20, 'color': '#ffc107'},
            {'name': '20-30 kg', 'min_weight_loss': 20, 'max_weight_loss': 30, 'color': '#fd7e14'},
            {'name': '30+ kg', 'min_weight_loss': 30, 'max_weight_loss': None, 'color': '#dc3545'},
        ]
        
        for cat_data in weight_categories:
            category, created = WeightLossCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'✓ Kilo kaybı kategorisi oluşturuldu: {category.name}')
        
        # Müşteri yorumları
        testimonials_data = [
            {
                'name': 'Ayşe Yılmaz',
                'content': '3 ayda 12 kilo verdiğim için çok mutluyum. Programı kolayca takip edebildim.',
                'rating': 5
            },
            {
                'name': 'Mehmet Kaya',
                'content': 'Beslenme alışkanlıklarım tamamen değişti. Kendimi çok daha enerjik hissediyorum.',
                'rating': 5
            },
            {
                'name': 'Zeynep Demir',
                'content': 'Online konsültasyon çok praktikti. Evden çıkmadan profesyonel destek aldım.',
                'rating': 5
            }
        ]
        
        for test_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=test_data['name'],
                defaults=test_data
            )
            if created:
                self.stdout.write(f'✓ Müşteri yorumu oluşturuldu: {testimonial.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )