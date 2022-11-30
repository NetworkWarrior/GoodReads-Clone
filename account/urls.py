from django.urls import path
from . views import RegisterView, LoginView, ProfileView, LogoutView, ProfileEditView, ProfilesView

app_name = 'account'
urlpatterns = [
    path('', ProfilesView.as_view(), name='profile-list-view'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:id>', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile-edit'),
]