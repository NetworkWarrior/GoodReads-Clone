from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from account.models import CustomUser
from books.models import Book, BookReview


class DetailReviewAPITestCase(APITestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='Network', email='some123@gmail.com')
        self.db_user.set_password('greatsuper')
        self.db_user.save()
        self.client.login(username='Network', password='greatsuper')

    def test_book_review_detail(self):
        book = Book.objects.create(title='book1', description='scientific', isbn='123453aa')
        br = BookReview.objects.create(user=self.db_user, book=book, stars_given=4, comment='very nice book')
        response = self.client.get(reverse('api:review_detail', kwargs={'id': br.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data["stars_given"], 4)
        self.assertEqual(response.data['comment'], 'very nice book')
        self.assertEqual(response.data['book']["id"], br.book.id)
        self.assertEqual(response.data['book']["title"], 'book1')
        self.assertEqual(response.data['book']["isbn"], '123453aa')
        self.assertEqual(response.data['book']["description"], 'scientific')
        self.assertEqual(response.data['user']["id"], self.db_user.id)
        self.assertEqual(response.data['user']["username"], 'Network')
        self.assertEqual(response.data['user']['email'], 'some123@gmail.com')

    def test_delete_review(self):
        book = Book.objects.create(title='book1', description='scientific', isbn='123453aa')
        br = BookReview.objects.create(user=self.db_user, book=book, stars_given=4, comment='very nice book')
        response = self.client.delete(reverse("api:review_detail", kwargs={"id": br.id}))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title='book1', description='scientific', isbn='123453aa')
        br = BookReview.objects.create(user=self.db_user, book=book, stars_given=4, comment='very nice book')
        response = self.client.patch(reverse("api:review_detail", kwargs={"id": br.id}),
                                     data={'stars_given': 5})
        br.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 5)

    def test_put_review(self):
        book = Book.objects.create(title='book1', description='scientific', isbn='123453aa')
        br = BookReview.objects.create(user=self.db_user, book=book, stars_given=4, comment='very nice book')
        response = self.client.put(
            reverse("api:review_detail", kwargs={'id':br.id}), data={
                'stars_given':5, 'comment':'very enjoyable!', 'user_id':self.db_user.id, 'book_id':book.id
            }
        )
        br.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 5)
        self.assertEqual(br.comment, 'very enjoyable!')

    def test_create_review(self):
        book = Book.objects.create(title='book1', description='scientific', isbn='123453aa')
        data = {
            'stars_given':2,
            'comment':'bad book',
            'user_id': self.db_user.id,
            'book_id': book.id
        }
        response = self.client.post(reverse('api:review_list'), data=data)
        br = BookReview.objects.get(book=book)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars_given, 2)
        self.assertEqual(br.comment, 'bad book')

    def test_bad_requests(self):
        book = Book.objects.create(title='book1', description='scientific', isbn='123453aa')
        data = {
            'stars_given': 2,
            'comment': 'bad book',
            'user_id': self.db_user.id,
        }
        response = self.client.post(reverse('api:review_list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_book_review_list(self):
        user2 = CustomUser.objects.create(username='Ismoil', first_name='Ismoil')
        book = Book.objects.create(title='book1', description='scientific', isbn='123453aa')
        br = BookReview.objects.create(user=self.db_user, book=book, stars_given=4, comment='very nice book')
        br2 = BookReview.objects.create(user=user2, book=book, stars_given=2, comment='very bad')

        response = self.client.get(reverse('api:review_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(response.data['results'][0]['id'], br2.id)
        self.assertEqual(response.data['results'][0]['stars_given'], br2.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], br2.comment)
        self.assertEqual(response.data['results'][1]['id'], br.id)
        self.assertEqual(response.data['results'][1]['stars_given'], br.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], br.comment)
