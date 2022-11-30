from django.contrib.auth import get_user
from .models import CustomUser as User
from django.test import TestCase
from django.urls import reverse


# Create your tests here.


class RegistrationTestCase(TestCase):
    def test_account_is_created(self):
        self.client.post(
            reverse('account:register'),
            data={
                'username': 'Network_Warrior',
                'first_name': 'ismoil',
                'last_name': 'abdumajidov',
                'email': 'example@gmail.com',
                'password': 'somepassword'
            }
        )
        user = User.objects.get(username='Network_Warrior')
        self.assertEqual(user.first_name, 'ismoil')
        self.assertEqual(user.last_name, 'abdumajidov')
        self.assertEqual(user.email, 'example@gmail.com')
        self.assertNotEqual(user.password, 'somepassword')
        self.assertTrue(user.check_password('somepassword'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('account:register'),
            data={
                'first_name': 'Network_Warrior',
                'email': 'somethin@gmail.com'
            }
        )

        user = User.objects.count()
        self.assertEqual(user, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_invalid_emails(self):
        response = self.client.post(
            reverse('account:register'),
            data={
                'username': 'Network_Warrior',
                'first_name': 'ismoil',
                'last_name': 'abdumajidov',
                'email': 'example@gmailcom',
                'password': 'somepassword'
            }
        )

        user = User.objects.count()
        self.assertEqual(user, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_same_User(self):
        self.client.post(
            reverse('account:register'),
            data={
                'username': 'Network_Warrior',
                'first_name': 'ismoil',
                'last_name': 'abdumajidov',
                'email': 'example@gmail.com',
                'password': 'somepassword'
            }
        )

        respond = self.client.post(
            reverse('account:register'),
            data={
                'username': 'Network_Warrior',
                'first_name': 'ismoill',
                'last_name': 'abdumajidovv',
                'email': 'examplee@gmail.com',
                'password': 'somepassword'
            }
        )

        user = User.objects.count()
        self.assertEqual(user, 1)
        self.assertFormError(respond, 'form', 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = User.objects.create(username='Network', email='some123@gmail.com')
        self.db_user.set_password('greatsuper')
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse('account:login'),
            data={
                'username': 'Network',
                'password': 'greatsuper'
            }
        )
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('account:login'),
            data={
                'username': 'Network',
                'password': 'somepassword'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('account:login'),
            data={
                'username': 'Networkk',
                'password': 'greatsuper'
            }
        )
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username='Network', password='greatsuper')
        self.client.get(reverse('account:logout'))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_profile_view(self):
        user = User.objects.create(username='Warrior', first_name='Ismoil', last_name='Abdumajidov',
                                   email='example@gmail.com', )
        user.set_password('Ismoiljon2003')
        user.save()
        response = self.client.get(reverse('account:profile', kwargs={'id':user.id}))
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

        self.client.login(username='Warrior', password='Ismoiljon2003')
        response = self.client.get(reverse('account:profile', kwargs={'id': user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_profile_updated(self):
        user = User.objects.create(username='Warrior', first_name='Ismoil', last_name='Abdumajidov',
                                   email='example@gmail.com', )
        user.set_password('Ismoiljon2003')
        user.save()
        self.client.login(username='Warrior', password='Ismoiljon2003')
        response = self.client.post(
            reverse('account:profile-edit'),
            data={
                'username':'Warrior',
                'first_name':'Ismoil',
                'last_name':'Grimm',
                'email':'example23@gmail.com'
            }
        )
        user.refresh_from_db()
        self.assertEqual(user.last_name, 'Grimm')
        self.assertEqual(user.email, 'example23@gmail.com')
        self.assertEqual(response.url, reverse('account:profile', kwargs={'id':user.id}))



