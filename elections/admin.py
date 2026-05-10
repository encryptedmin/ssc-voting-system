from django.contrib import admin
from .models import Election

try:
    admin.site.unregister(Election)
except:
    pass

admin.site.register(Election)