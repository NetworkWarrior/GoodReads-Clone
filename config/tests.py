from django.test import TestCase
from account.models import CustomUser
from books.models import Book
from books.models import BookReview
from django.urls import reverse


class HomePageTestCase(TestCase):
    def test_home_page(self):
        user = CustomUser.objects.create(username='Warrior', first_name='Ismoil', last_name='Abdumajidov',email='example@gmail.com',)
        user.set_password('Ismoiljon2003')
        user.save()
        b1 = Book.objects.create(title='hero', description='great', isbn='11111')
        review1 = BookReview.objects.create(user=user, book=b1, comment='Unbelievable', stars_given=5)
        review2 = BookReview.objects.create(user=user, book=b1, comment='Very Nice book', stars_given=4)
        review3= BookReview.objects.create(user=user, book=b1, comment='Super book', stars_given=5)
        response = self.client.get(reverse('home_page') + "?page_size=2")
        self.assertContains(response, review2.comment)
        self.assertContains(response, review3.comment)
        self.assertNotContains(response, review1.comment)


class LandingPageTestCase(TestCase):
    def test_user_info(self):
        user_list = ['great1', 'madboy2', 'magic_master3']
        for user in user_list:
            CustomUser.objects.create(username=user, password='greatestever')
        user4 = CustomUser.objects.create(username='super', password='greatestever')
        response = self.client.get(reverse('landing')+"?page_size=3")
        for username in user_list:
            user = CustomUser.objects.get(username=username)
            self.assertContains(response, user.username)
            self.assertContains(response, user.profile_picture.url)
        self.assertNotContains(response, user4.username)





