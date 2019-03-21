from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.template.defaultfilters import slugify
from django.utils import timezone


class UserProfile(AbstractUser):
    is_user = models.BooleanField('student status', default=False)
    is_society = models.BooleanField('society status', default=False)
    logo = models.ImageField(upload_to='logos', blank=True)


class Society(models.Model):
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='society_user',
        default='null')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=40, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #    return "/categories/%s/" % self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Event(models.Model):
    title = models.CharField(max_length=100, unique=True)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=10000)
    date = models.DateTimeField(
        help_text="Please use the format: YYYY-MM-DD HH:MM:SS",
        null=True)
    address = models.CharField(max_length=50, blank=True)
    room = models.CharField(max_length=25, blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True, default=0)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    bookings = models.PositiveIntegerField(blank=True, null=True, editable=False, default=0)
    picture = models.ImageField(upload_to='events')
    popularity = models.IntegerField(blank=True, null=True, editable=False)
    slug = models.SlugField(max_length=40, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Events'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    def remaining_capacity(self):
        return self.capacity - self.bookings

    def is_fully_booked(self):
        return self.remaining_capacity() < 1

    def is_past(self):
        return timezone.now() > self.date  # TODO test it's the right import


class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_booking')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_booking')
    booked = models.BooleanField(default=False)


class Bookmark(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_bookmarked')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_bookmarked')
    bookmarked = models.BooleanField(default=False)
