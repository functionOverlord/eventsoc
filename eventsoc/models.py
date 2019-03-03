from django.db import models
from django.contrib.auth.models import User

class Place(models.Model):
    place_name = models.CharField(max_length=50)
    room = models.CharField(max_length=10)
    address = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.place_name

class Category(models.Model):
    """
    A category of the Event such as "Workshops", "Talks", "Sports",
    etc.
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Society(models.Model):
    society_id = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logos')

    def __str__(self):
       return self.username

class Event(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    event_id = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    event_date = models.DateTimeField(help_text="Please use the format: YYYY-MM-DD")
    time = models.TimeField(help_text='Please use the format: <em>HH:MM:SS<em')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=10000)
    picture = models.ImageField(upload_to='events')
    creator = models.ForeignKey(Society, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def is_past(self):
        if timezone.now() > self.event_date:
            return True
        return False

class UserProfile(models.Model):
    # Links UserProfile to aUser model instance
    user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)

class Bookmark(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
