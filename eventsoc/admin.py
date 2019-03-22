from django.contrib import admin
from eventsoc.models import UserProfile, Event, Category, Booking, Bookmark

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Booking)
admin.site.register(Bookmark)
