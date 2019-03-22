from django.test import TestCase
from eventsoc.models import UserProfile, Society, Category, Event
from eventsoc.forms import SocietyForm, StudentForm, EditSocietyForm, EditStudentForm
from django.template.defaultfilters import slugify
from django.urls import reverse
from eventsoc.form_functions import check_email, check_password

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

    def test_fully_booked(self):
        s = self.create_society().user
        c = self.create_category()
        e = self.create_event(s, c)
        self.assertTrue(isinstance(e, Event))
        self.assertEqual(Event.is_fully_booked(e), (Event.remaining_capacity(e) < 1))

    def test_fully_booked(self):
        s = self.create_society().user
        c = self.create_category()
        e = self.create_event(s, c)
        self.assertTrue(isinstance(e, Event))
        # is_past doesn't work, may not even be needed in the models
        self.assertEqual(Event.is_past(e), (timezone.now() > e.date))

class TestViews(TestCase):
    def create_society(self, is_user=True, username="TestUser", password="testpassword12", email="test@test.com"):
        user = UserProfile.objects.create(is_society=True, username=username, password=password, email=email)
        return Society.objects.create(user=user)

    def create_category(self, name="testCat"):
        return Category.objects.create(name=name)

    def create_event(self, creator, category, title="testEvent", description="desc", date="2019-12-12 00:00:00", address="testAddr", room="1", price=5, capacity=9, bookings=2, popularity=2):
        return Event.objects.create(title=title, creator=creator, category=category, description=description, date=date, address=address, room=room, price=price, capacity=capacity, bookings=bookings, popularity=popularity)

    # Causes errors with username being unique
    # def setUp(self, s, c):
    #     # s = self.create_society().user
    #     # c = self.create_category()
    #     Event.objects.create(title="testEvent", creator=s, category=c, description="testdesc", date="2019-12-12 00:00:00", address="testAddr1", room="3", price=6, capacity=50, bookings=37, popularity=32)
    #     Event.objects.create(title="testEvent2", creator=s, category=c, description="anothertest", date="2029-02-01 05:30:10", address="testAddr2", room="room", price=7, capacity=2, bookings=2, popularity=0)
    #     Event.objects.create(title="testEvent3", creator=s, category=c, description="description", date="2020-03-22 12:00:00", address="testAddr3", room="room 4", price=0, capacity=42, bookings=21, popularity=12)

    # Can't get values from t and v, meaning the order by code may not work in the index view
    # def test_index(self):
    #     s = self.create_society().user
    #     c = self.create_category()
    #     Event.objects.create(title="testEvent", creator=s, category=c, description="testdesc", date="2019-12-12 00:00:00", address="testAddr1", room="3", price=6, capacity=50, bookings=37, popularity=32)
    #     Event.objects.create(title="testEvent2", creator=s, category=c, description="anothertest", date="2029-02-01 05:30:10", address="testAddr2", room="room", price=7, capacity=2, bookings=2, popularity=0)
    #     Event.objects.create(title="testEvent3", creator=s, category=c, description="description", date="2020-03-22 12:00:00", address="testAddr3", room="room 4", price=0, capacity=42, bookings=21, popularity=12)
    #     # self.setUp(soc, cat)
    #     t = Event.objects.order_by('-popularity')[:5]
    #     u = Event.objects.order_by('date')
    #     url = reverse("index")
    #     resp = self.client.get(url)
    #
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn(t.values()['eventid'], resp.content)
    #     self.assertIn(u.values(), resp.content)

    def test_login(self):
        UserProfile.objects.create(is_society=True, username="TestUser", password="password12", email="test@test.com")
        self.client.login(username="TestUser", password="password12")
        resp = self.client.get('eventsoc/login.html')
        # resp = self.client.get('eventsoc:login') Says eventsoc is not a registered namespace, should make commented assertion work if fixed
        # self.assertEqual(resp.status_code, 200)
        # self.assertTemplateUsed(resp, 'user_login.html') No templates used?


class TestForms(TestCase):
    def create_society(self, is_user=True, username="TestUser", password="testpassword12", email="test@test.com"):
        user = UserProfile.objects.create(is_society=True, username=username, password=password, email=email)
        return Society.objects.create(user=user)

    def create_category(self, name="testCat"):
        return Category.objects.create(name=name)

    def create_event(self, creator, category, title="testEvent", description="desc", date="2019-12-12 00:00:00", address="testAddr", room="1", price=5, capacity=9, bookings=2, popularity=2):
        return Event.objects.create(title=title, creator=creator, category=category, description=description, date=date, address=address, room=room, price=price, capacity=capacity, bookings=bookings, popularity=popularity)

    # Student form tests
    def test_student_clean_email(self):
        user = UserProfile.objects.create(username="TestUser", password="password12", email="test@test.com")
        data = {'username': user.username, 'email': user.email}
        form = StudentForm(data=data)
        # User, data and form don't have attribute cleaned data
        self.assertEqual(StudentForm.clean_email(data), check_email(user))

    def test_student_clean_password(self):
        # Will have the same problems as above
        form = StudentForm(data=data)

    def test_student_save(self):
        user = UserProfile.objects.create(username="TestUser", password="password12", email="test@test.com")
        data = {'username': user.username, 'password1': user.password,'password1': user.password, 'email': user.email}
        form = StudentForm(data=data)
        self.assertTrue(form.is_valid()) # Form not valid for some reason
        self.assertEqual(form.save(), self.save())
