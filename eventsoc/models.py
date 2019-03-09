from django.db import models
from django.contrib.auth.models import User, AbstractUser

class NewUser(AbstractUser):
    is_user = models.BooleanField('student status', default=False)
    is_society = models.BooleanField('society status', default=False)
    email = models.EmailField(max_length=254, blank=False, help_text='Required. Inform a valid email address.')

    # class Meta:
    #     permissions = (
    #     ('is_user', "" )
    #     )

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
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, related_name='society_user', default = 'null')
    logo = models.ImageField(upload_to='logos')


    # class Meta:
    #     permissions = (
    #     ('is_society', "A society user" )
    #     )

    def __str__(self):
        return self.user.username

class Event(models.Model):
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    event_id = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    event_date = models.DateTimeField(help_text="Please use the format: YYYY-MM-DD")
    time = models.TimeField(help_text='Please use the format: <em>HH:MM:SS<em')
    # place = models.ForeignKey(Place, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=10000)
    picture = models.ImageField(upload_to='events')
    place_name = models.CharField(max_length=50)
    room = models.CharField(max_length=10)
    capacity = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True)
    creator = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='society_event')

    def __str__(self):
        return self.title

    def is_past(self):
        if timezone.now() > self.event_date:
            return True
        return False


class Booking(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='user_booking')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_booking')
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='society_booking')

class Bookmark(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='user_bookmarked')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_bookmarked')
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='society_bookmarked')
