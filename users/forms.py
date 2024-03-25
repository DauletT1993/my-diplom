from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUsersForm(AuthenticationForm):
    '''Отображение формы авторизации'''
    username = forms.CharField(label='Логин или E-mail',
                        widget=forms.TextInput(attrs={'class' : 'form-input'}))
    password = forms.CharField(label='Пароль',
                        widget=forms.PasswordInput(attrs={'class' : 'form-input'}))

    class Meta:
        '''Связка с моделью user    '''
        model = get_user_model()#Возвращает модель юзера
        feilds =    ['username', 'password']


class RegisterUserForm(UserCreationForm ):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class' : 'form-input'}))
    password1  = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class' : 'form-input'}))
    password2  = forms.CharField(label='Повтор пароль', widget=forms.PasswordInput(attrs={'class' : 'form-input'}))

    class Meta:
        '''Связка с моделью user    '''
        model = get_user_model()#Возвращает модель юзера
        fields =    ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email' : 'E-mail',
            'first_name' : 'Имя',
            'last_name' : 'Фамилия'
        }
        widgets = {
            'email': forms.TextInput(attrs={'class' : 'form-input'})    ,
            'first_name': forms.TextInput(attrs={'class' : 'form-input'}),
            'last_name': forms.TextInput(attrs={'class' : 'form-input'})
        }


        def clean_email(self):
            '''Проверка на уникальность E-mail'''
            email = self.cleaned_data['email']
            if get_user_model().objects.filter(email=email).exists():
                raise forms.ValidationError('Такой E-mail уже существует')


class ProfileUserForm(forms.ModelForm):
    '''Редактирование личных данных'''
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class' : 'form-input'}))
    email  = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class' : 'form-input'}))
    '''disabled=True - поля которые не редактируются'''

    class Meta:
        '''Связка с моделью user    '''
        model = get_user_model()#Возвращает модель юзера
        fields =    ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name' : 'Имя',
            'last_name' : 'Фамилия'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class' : 'form-input'}),
            'last_name': forms.TextInput(attrs={'class' : 'form-input'})
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class' : 'form-input'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class' : 'form-input'}))
    new_password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class' : 'form-input'}))