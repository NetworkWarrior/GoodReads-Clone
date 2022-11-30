from django.urls import path
from .views import DetailReviewAPIView, ReviewListAPIView

app_name='api'
urlpatterns = [
    path('reviews/', ReviewListAPIView.as_view(), name="review_list"),
    path('reviews/<int:id>/', DetailReviewAPIView.as_view(), name="review_detail")
]