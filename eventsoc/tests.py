from django.test import TestCase
from eventsoc.models import UserProfile, Society, Category, Event
from eventsoc.forms import SocietyForm
from django.template.defaultfilters import slugify
from django.contrib.staticfiles import finders
from django.urls import reverse

# class TestUserProfile(TestCase):
#     def create_user(self, is_user=True, username="TestUser", password1="testpassword12", password2="testpassword12", email="test@test.com")
#         return UserProfile.objects.create(is_user=is_user, username=username, password1=password1, password2=password2, email=email)
#
#     def test_user_creation(self):
#         u=self.create_user()
#         self.assertTrue(isInstance(u, UserProfile))
#         self.assertEqual(u.__unicode__(), u.username)
#         self.assertEqual(u.__unicode__(), u.password1)
#         self.assertEqual(u.__unicode)


class GeneralTests(TestCase):
    # Check if files exist in static media folder
    # Returns None if file is not found
    def test_static_files(self):
        static_media = finders.find('images/logo.png')
        self.assertIsNotNone(static_media)

    # Check if user successfully gets to the index page
    def test_urls(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class TestModels(TestCase):
    def create_society(self, is_user=True, username="TestUser", password="testpassword12", email="test@test.com", ):
        user = UserProfile.objects.create(is_society=True, username=username, password=password, email=email)
        return Society.objects.create(user=user)

    def test_society__str__(self):
        s = self.create_society()
        self.assertTrue(isinstance(s, Society))
        self.assertEqual(str(s), s.user.username)

    # Category tests
    def create_category(self, name="testCat"):
        return Category.objects.create(name=name)

    def test_category__str__(self):
        c = self.create_category()
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(str(c), c.name)

    def test_category_save(self):
        c = self.create_category()
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(slugify(c.save.__self__.name), slugify(c.name))

    # Event tests
    def create_event(self, creator, category, title="testEvent", description="desc", date="2019-12-12 00:00:00", address="testAddr", room="1", price=5, capacity=9, bookings=2, popularity=2):
        return Event.objects.create(title=title, creator=creator, category=category, description=description, date=date, address=address, room=room, price=price, capacity=capacity, bookings=bookings, popularity=popularity)

    def test_event__str__(self):
        s = self.create_society().user
        c = self.create_category()
        e = self.create_event(s, c)
        self.assertTrue(isinstance(e, Event))
        self.assertEqual(str(e), e.title)

    def test_remaining_capacity(self):
        s = self.create_society().user
        c = self.create_category()
        e = self.create_event(s, c)
        self.assertTrue(isinstance(e, Event))
        self.assertEqual(Event.remaining_capacity(e), (e.capacity-e.bookings))
