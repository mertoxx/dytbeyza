import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diyetisyen_website.settings')

application = get_wsgi_application()

# Vercel için zorunlu
app = application