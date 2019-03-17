from django.contrib import admin
from eventsoc.models import UserProfile, Event, Category

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Category)
