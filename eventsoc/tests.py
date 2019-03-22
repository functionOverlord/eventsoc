from django.test import TestCase
from eventsoc.models import UserProfile, Society, Category, Event
from eventsoc.forms import SocietyForm, StudentForm, EditSocietyForm, EditStudentForm
from django.template.defaultfilters import slugify
from django.urls import reverse
from eventsoc.form_functions import check_email, check_password
from django.contrib.staticfiles import finders


class TestStudentUser(TestCase):
    # Set up Student account
    def setUp(self):
        user = UserProfile.objects.create(username="monkey", email="monkey@gmail.com")
        user.set_password("pepsikola5")
        user.save()

    # Check if created Student account exists and if there's only one profile for it
    def test_student_exists(self):
        UserProfile.objects.get(username="monkey")
        self.assertEqual(1, UserProfile.objects.count(), "Number of Profiles must be 1")

    # Check if Student can log in with their credentials
    def test_student_login(self):
        login = self.client.login(username='monkey', password="pepsikola5")
        self.assertTrue(login)

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
    # Creates society for testing
    def create_society(self, is_user=True, username="TestUser", password="testpassword12", email="test@test.com", ):
        user = UserProfile.objects.create(is_society=True, username=username, password=password, email=email)
        return Society.objects.create(user=user)

    def test_society__str__(self):
        s = self.create_society()
        self.assertTrue(isinstance(s, Society))
        self.assertEqual(str(s), s.user.username)

    # Category tests
    # Creates category for testing
    def create_category(self, name="testCat"):
        return Category.objects.create(name=name)

    def test_category__str__(self):
        c = self.create_category()
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(str(c), c.name)

    # Checks name is saved properly
    def test_category_save(self):
        c = self.create_category()
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(slugify(c.save.__self__.name), slugify(c.name))

    # Event tests
    # Creates event for testing
    def create_event(self, creator, category, title="testEvent", description="desc", date="2019-12-12 00:00:00", address="testAddr", room="1", price=5, capacity=9, bookings=2, popularity=2):
        return Event.objects.create(title=title, creator=creator, category=category, description=description, date=date, address=address, room=room, price=price, capacity=capacity, bookings=bookings, popularity=popularity)

    def test_event__str__(self):
        s = self.create_society().user
        c = self.create_category()
        e = self.create_event(s, c)
        self.assertTrue(isinstance(e, Event))
        self.assertEqual(str(e), e.title)

    # Checks that remaining_capacity is calulated correctly
    def test_remaining_capacity(self):
        s = self.create_society().user
        c = self.create_category()
        e = self.create_event(s, c)
        self.assertTrue(isinstance(e, Event))
        self.assertEqual(Event.remaining_capacity(e), (e.capacity-e.bookings))

    def test_fully_booked(self):
        s = self.create_society().user
        c = self.create_category()
        e = self.create_event(s, c)
        self.assertTrue(isinstance(e, Event))
        self.assertEqual(Event.is_fully_booked(e), (Event.remaining_capacity(e) < 1))
