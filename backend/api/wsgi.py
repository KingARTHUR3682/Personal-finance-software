import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

application = get_wsgi_application()

# --- START TEMPORARY SUPERUSER CREATION ---
# This code creates a superuser automatically
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'arthurkbx@gmail.com', 'admin123')
        print("✅ Superuser 'admin' created successfully!")
    else:
        print("ℹ️ Superuser 'admin' already exists.")
except Exception as error:
    print(f"❌ Error creating superuser: {error}")
# --- END TEMPORARY SUPERUSER CREATION ---