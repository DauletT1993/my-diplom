from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import LoginUsersForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    '''Авторизация пользователем на сайте на сйте'''
    form_class = LoginUsersForm
    template_name = 'users/login.html'
    extra_context = {'title' : 'Авторизация'}
    '''Перенаправление на главную прописано в settings.py'''

    # def get_success_url(self):
    #     return reverse_lazy('home') Можно указать нужный url для перенаправления

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title' : 'Регистрация'}
    success_url = reverse_lazy('users:login')# Перенаправить, если всё ок


class ProfileUser(LoginRequiredMixin, UpdateView):
    '''LoginRequiredMixin - профайл могут просматривать только
        авторизованные пользователи. UpdateView - изменение текущей записи'''
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title' : 'Профиль пользователя'}


    def get_success_url(self):
        '''Перенаправления пользователя после изменения'''
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        '''Позволяет отбирать ту звпись которая бууде редактироваться'''
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"

# Viktor password - qwqwqw@@@