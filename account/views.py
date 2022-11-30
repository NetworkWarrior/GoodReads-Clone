from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import UserCreateForm, UserUpdateForm
from django.views.generic import ListView
from .models import CustomUser


class RegisterView(View):
    def get(self, request):
        return render(request, 'account/register.html', {'form': UserCreateForm()})

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('account:login')
        else:
            return render(request, 'account/register.html', {'form': create_form})


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'account/login.html', {'form': login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'Successfully logged in !')
            return redirect('books:list')
        else:
            return render(request, 'account/login.html', {'form': login_form})


class ProfileView(View):
    def get(self, request, id):
        view_profile = CustomUser.objects.get(id=id)
        if view_profile == request.user:
            user = request.user
        else:
            user = view_profile
        return render(request, 'account/profile.html', {'user':user})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You successfully logged out!')
        return redirect('landing')


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        update_form = UserUpdateForm(instance=request.user)
        return render(request, 'account/profile-edit.html', {'form':update_form})

    def post(self, request):
        update_form = UserUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )
        if update_form.is_valid():
            current = request.user
            messages.success(request, 'Successfully update')
            update_form.save()
            return redirect(reverse('account:profile', kwargs={'id':current.id}))
        else:
            return render(request, 'account/profile-edit.html', {'form':update_form})


class ProfilesView(ListView):
    model = CustomUser
    template_name = 'account/main.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return CustomUser.objects.all().exclude(id=self.request.user.id)








