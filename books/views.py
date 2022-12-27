from books.models import BookReview, Book, Author
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import BookReviewsForm
from django.views.generic import ListView, DetailView



# Create your views here.

# class BooksView(ListView):
#   template_name = 'books/list.html'
#  queryset = Book.objects.all()
#  context_object_name = 'books'
#  paginate_by = 2


class BooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)
        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)
        return render(
            request,
            'books/list.html',
            {'page_obj': page_obj, 'search': search_query}
        )


class BooksDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewsForm()
        return render(request, 'books/detail.html', {'book': book, 'form': review_form})


class BooksAuthorView(View):
    def get(self, request, book_id, author_id):
        book = Book.objects.get(id=book_id)
        author = Author.objects.get(id=author_id)
        book_author = author.bookauthor_set.all().order_by('id')
        page_size = request.GET.get('page_size', 8)
        paginator = Paginator(book_author, page_size)
        page_num = request.GET.get('page', 1)
        page_ob = paginator.get_page(page_num)
        return render(request, 'books/author.html', {'book':book, 'author':author, 'page_obj':page_ob})


class BooksReviewsView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewsForm(data=request.POST)
        if review_form.is_valid():
            BookReview.objects.create(
                user = request.user,
                book = book,
                stars_given = review_form.cleaned_data['stars_given'],
                comment = review_form.cleaned_data['comment']
            )
            return redirect(reverse('books:detail', kwargs={'id':book.id}))
        return render(request, 'books/detail.html', {'book': book, 'form': review_form, 'num':4})


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewsForm(instance=review)
        return render(request, 'books/edit_review.html', {'book':book, 'review':review, 'form':review_form})

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewsForm(instance=review, data=request.POST)
        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('books:detail', kwargs={'id':book.id}))

        return render(request, 'books/edit_review.html', {'book':book, 'review':review, 'form':review_form})


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        return render(request, 'books/delete_review.html', {'book':book, 'review':review})


class DeleteCompleteReview(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review.delete()
        messages.success(request, f"Review has been successfully deleted")
        return redirect(reverse('books:detail', kwargs={'id':book.id}))
