from django.contrib import admin
from .models import Vote, Election

admin.site.register(Vote)
admin.site.register(Election)