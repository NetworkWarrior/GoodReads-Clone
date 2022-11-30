from books.models import Author, BookAuthor, BookReview
from django.test import TestCase
from django.urls import reverse
from .models import Book
from account.models import CustomUser
# Create your tests here.


class BookTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, 'No books found.')

    def test_books_title(self):
        b1 = Book.objects.create(title='hero', description='great', isbn='11111')
        b2 = Book.objects.create(title='hero2', description='great2', isbn='111112')
        b3 = Book.objects.create(title='hero3', description='great3', isbn='111113')

        response = self.client.get(reverse('books:list')+'?page_size=2')

        for book in [b1, b2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, b3.title)

        response = self.client.get(reverse('books:list')+'?page=2&page_size=2')

        self.assertContains(response, b3.title)

    def test_detail_page(self):
        book = Book.objects.create(title='hero', description='great', isbn='11111')
        author = Author.objects.create(first_name='Coolen', last_name='Hoover', email="example@gmail.com", bio="very good")
        BookAuthor.objects.create(book=book, author=author)

        response = self.client.get(reverse('books:detail', kwargs={'id':book.id}))
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        self.assertContains(response, author.full_name())

    def test_search_books(self):
        b1 = Book.objects.create(title='hero', description='great', isbn='11111')
        b2 = Book.objects.create(title='legends', description='great2', isbn='111112')
        b3 = Book.objects.create(title='gamers', description='great3', isbn='111113')

        response = self.client.get(reverse('books:list')+'?q=hero')
        self.assertContains(response, b1.title)
        self.assertNotContains(response, b2.title)
        self.assertNotContains(response, b3.title)

        response = self.client.get(reverse('books:list')+'?q=legends')
        self.assertContains(response, b2.title)
        self.assertNotContains(response, b1.title)
        self.assertNotContains(response, b3.title)

        response = self.client.get(reverse('books:list')+'?q=gamers')
        self.assertContains(response, b3.title)
        self.assertNotContains(response, b2.title)
        self.assertNotContains(response, b1.title)


class BookReviewsTestCase(TestCase):
    def test_add_reviews(self):
        b1 = Book.objects.create(title='hero', description='great', isbn='11111')
        user = CustomUser.objects.create(username='Warrior', first_name='Ismoil', last_name='Abdumajidov',
                                   email='example@gmail.com', )
        user.set_password('Ismoiljon2003')
        user.save()
        self.client.login(username='Warrior', password='Ismoiljon2003')
        self.client.post(reverse('books:reviews', kwargs={'id':b1.id}), data={
            'stars_given':5,
            'comment':'Greatest of all the time'
        })
        book_reviews = b1.bookreview_set.all()
        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 5)
        self.assertEqual(book_reviews[0].comment, 'Greatest of all the time')
        self.assertEqual(book_reviews[0].book, b1)
        self.assertEqual(book_reviews[0].user, user)


class BookAuthorTestCase(TestCase):
    def test_author_detail(self):
        book = Book.objects.create(title='hero', description='great', isbn='11111')
        author = Author.objects.create(
            first_name='Name', last_name='LastName', bio='Very nice author', born='December 12 , 1987'
        )
        BookAuthor.objects.create(book=book, author=author)
        response = self.client.get(reverse('books:author', kwargs={'book_id':book.id, 'author_id':author.id}))
        self.assertContains(response, author.author_image)
        self.assertContains(response, author.bio)
        self.assertContains(response, author.born)

    def test_author_books(self):
        book1 = Book.objects.create(title='hero1', description='great', isbn='11111')
        book2 = Book.objects.create(title='hero2', description='great', isbn='11111')
        book3 = Book.objects.create(title='hero3', description='great', isbn='11111')
        book4 = Book.objects.create(title='hero4', description='great', isbn='11111')
        book5 = Book.objects.create(title='hero5', description='great', isbn='11111')
        book6 = Book.objects.create(title='hero6', description='great', isbn='11111')
        book7 = Book.objects.create(title='hero7', description='great', isbn='11111')
        book8 = Book.objects.create(title='hero8', description='great', isbn='11111')
        book9 = Book.objects.create(title='hero9', description='great', isbn='11111')
        author = Author.objects.create(
            first_name='Name', last_name='LastName', bio='Very nice author', born='December 12 , 1987'
        )

        list = [book1, book2, book3, book4, book5, book6, book7, book8, book9]
        list2 = [book1, book2, book3, book4, book5, book6, book7, book8]
        for book in list:
            BookAuthor.objects.create(book=book, author=author)
        response = self.client.get(reverse('books:author', kwargs={'book_id': book1.id, 'author_id': author.id}))
        for book in list2:
            self.assertContains(response, book.title)
            self.assertContains(response, book.book_cover)
        response = self.client.get(reverse('books:author', kwargs={'book_id':book1.id, 'author_id':author.id}) + '?page=2')
        self.assertContains(response, book9.title)
        self.assertContains(response, book9.book_cover)


class EditReviewsTestCase(TestCase):
    def test_edit_review(self):
        b1 = Book.objects.create(title='hero', description='great', isbn='11111')
        user = CustomUser.objects.create(username='Warrior', first_name='Ismoil', last_name='Abdumajidov',
                                         email='example@gmail.com', )
        user.set_password('Ismoiljon2003')
        user.save()
        self.client.login(username='Warrior', password='Ismoiljon2003')
        review = BookReview.objects.create(user=user, book=b1, comment='nice book', stars_given=5)
        self.client.post(
            reverse('books:edit_review', kwargs={'book_id':b1.id, 'review_id':review.id}),
            data={
                'stars_given':4,
                'comment':'not bad'
            }
        )
        book_reviews = b1.bookreview_set.all()
        self.assertEqual(book_reviews[0].stars_given, 4)
        self.assertEqual(book_reviews[0].comment, 'not bad')

    def test_delete_review(self):
        b1 = Book.objects.create(title='hero', description='great', isbn='11111')
        user = CustomUser.objects.create(username='Warrior', first_name='Ismoil', last_name='Abdumajidov',
                                         email='example@gmail.com', )
        user.set_password('Ismoiljon2003')
        user.save()
        self.client.login(username='Warrior', password='Ismoiljon2003')
        review = BookReview.objects.create(user=user, book=b1, comment='nice book', stars_given=5)
        response = self.client.get(reverse('books:delete_review', kwargs={'book_id':b1.id, 'review_id':review.id}))
        self.assertContains(response, review.comment)
        self.assertContains(response, review.stars_given)

    def test_delete_complete(self):
        b1 = Book.objects.create(title='hero', description='great', isbn='11111')
        user = CustomUser.objects.create(username='Warrior', first_name='Ismoil', last_name='Abdumajidov',
                                         email='example@gmail.com', )
        user.set_password('Ismoiljon2003')
        user.save()
        self.client.login(username='Warrior', password='Ismoiljon2003')
        review = BookReview.objects.create(user=user, book=b1, comment='nice book', stars_given=5)
        review1 = BookReview.objects.create(user=user, book=b1, comment='great book', stars_given=4)

        review.delete()
        book_review = b1.bookreview_set.all()
        response = self.client.get(reverse('books:detail', kwargs={'id': b1.id}))

        self.assertEqual(book_review.count(), 1)
        self.assertEqual(book_review[0], review1)
        self.assertContains(response, review1.comment)
        self.assertContains(response, review1.stars_given)







