from django.urls import path
from .views import BooksView, BooksDetailView, BooksReviewsView, EditReviewView, DeleteReviewView, \
    DeleteCompleteReview, BooksAuthorView

app_name='books'
urlpatterns = [
    path('', BooksView.as_view(), name='list'),
    path('<int:id>/', BooksDetailView.as_view(), name='detail'),
    path('<int:book_id>/author/<int:author_id>', BooksAuthorView.as_view(), name='author'),
    path('<int:id>/reviews/', BooksReviewsView.as_view(), name='reviews'),
    path('<int:book_id>/reviews/<int:review_id>/edit/', EditReviewView.as_view(), name='edit_review'),
    path('<int:book_id>/reviews/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete_review'),
    path('<int:book_id>/reviews/<int:review_id>/delete/complete/', DeleteCompleteReview.as_view(), name='delete_complete'),
]