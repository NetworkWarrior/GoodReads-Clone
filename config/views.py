from django.core.paginator import Paginator
from django.shortcuts import render
from books.models import BookReview
from account.models import CustomUser


def landing_page(request):
    user = CustomUser.objects.all().order_by('id')
    page_size = request.GET.get('page_size', 8)
    paginator = Paginator(user, page_size)
    pag_num = request.GET.get('page',1)
    user_obj = paginator.get_page(pag_num)
    return render(request, 'landing.html', {'user_obj':user_obj})


def home_page(request):
    reviews = BookReview.objects.all().order_by('-created_at')
    page_size = request.GET.get('page_size', 5)
    paginator = Paginator(reviews, page_size)

    page_num = request.GET.get('page', 1)
    page_object = paginator.get_page(page_num)
    return render(request, 'home.html', {'page_obj':page_object})
