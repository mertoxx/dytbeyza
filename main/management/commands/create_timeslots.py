# appointments/management/commands/create_timeslots.py
# Önce bu klasör yapısını oluşturun:
# appointments/
#   management/
#     __init__.py
#     commands/
#       __init__.py
#       create_timeslots.py

from django.core.management.base import BaseCommand
from appointments.models import TimeSlot
from datetime import time

class Command(BaseCommand):
    help = 'TimeSlot verilerini oluşturur'

    def handle(self, *args, **options):
        # Mevcut verileri temizle
        TimeSlot.objects.all().delete()
        
        # Yeni veriler
        time_slots = [
            time(9, 0),   # 09:00
            time(10, 0),  # 10:00
            time(11, 0),  # 11:00
            time(14, 0),  # 14:00
            time(15, 0),  # 15:00
            time(16, 0),  # 16:00
        ]
        
        for t in time_slots:
            TimeSlot.objects.create(time=t, is_active=True)
            self.stdout.write(f'TimeSlot {t} oluşturuldu')
        
        self.stdout.write(
            self.style.SUCCESS('Tüm TimeSlot\'lar başarıyla oluşturuldu!')
        )