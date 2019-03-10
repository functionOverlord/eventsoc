from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.template.defaultfilters import slugify
from django.utils import timezone


class UserProfile(AbstractUser):
    is_user = models.BooleanField('student status', default=False)
    is_society = models.BooleanField('society status', default=False)
    email = models.EmailField(max_length=254, blank=False, help_text='Required. Inform a valid email address.')

    # class Meta:
    #     permissions = (
    #     ('is_user', "" )
    #     )


class Society(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='society_user', default = 'null')
    logo = models.ImageField(upload_to='logos')

    # class Meta:
    #     permissions = (
    #     ('is_society', "A society user" )
    #     )

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=40, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    #def get_absolute_url(self):
    #    return "/categories/%s/" % self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Event(models.Model):
    title = models.CharField(max_length=100, unique=True)
    creator = models.ForeignKey(Society, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(help_text="Please use the format: YYYY-MM-DD")
    time = models.TimeField(help_text='Please use the format: <em>HH:MM:SS<em')
    price = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=10000)
    picture = models.ImageField(upload_to='events')
    place_name = models.CharField(max_length=50)
    room = models.CharField(max_length=10)
    address = models.CharField(max_length=50, blank=True)
    capacity = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def is_past(self):
        return timezone.now() > self.event_date # TODO test it's the right import


class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_booking')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_booking')
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='society_booking')


class Bookmark(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_bookmarked')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_bookmarked')
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='society_bookmarked')
