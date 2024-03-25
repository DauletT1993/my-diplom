from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Cars


class AddPostForm(forms.ModelForm):
    '''Создаём формы для отправки новых статей в базу данных Cars '''

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана',
                                 label='Категории')  # Подтягиваем в выпадающий список "категории" все данные из модели Category


    class Meta:
        model = Cars
        fields = ['title', 'slug', 'content', 'photo','is_published', 'cat', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        '''Создаём собственный валидатор для проверки длины заголовка
        для одноразового использования подойдёт такой метод'''
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')
