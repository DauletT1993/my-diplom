from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse


def trunlin_to_eng(slug: str):
    cirilic = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'eo', 'ж': 'gh', 'з': 'z',
        'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'sch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    }
    text = slug.replace(' ', '-').lower()
    tmp = ''

    for i in text:
        tmp += cirilic.get(i, i)
    return tmp


class PublishedMeneger(models.Manager):
    ''' Возвращаем только опубликованные статьи'''

    def get_queryset(self):
        return super().get_queryset().filter(is_published=Cars.Status.PUBLISHED)


class Cars(models.Model):
    class Status(models.IntegerChoices):
        '''Переопределение булевого значения is_published'''
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')  # verbose_name='...' для отображения в админ панеле
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='slug',
                            validators=[
                                MinLengthValidator(5, 'Минимум 5 символов'),
                                MaxLengthValidator(100, 'Максимум 100 символов'),
                            ])
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', default=None, blank=True,
                              null=True, verbose_name='Фото')
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категории')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Теги')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True,
                               default=None)

    objects = models.Manager()
    published = PublishedMeneger()

    def __str__(self):
        return self.title

    class Meta:
        '''Сортировка по дате добавления от раннего к более позднему '''
        verbose_name = 'Автомобиль'  # Переименование заголовков в админ панеле
        verbose_name_plural = 'Автомобили'  # Переименование заголовков в админ панеле
        ordering = ['-time_create']  # Сортировка по убыванию
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = trunlin_to_eng(str(self.title))  # Самостоятельное формирование slug в поле добавления статьи
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolut_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        '''Сортировка по дате добавления от раннего к более позднему '''
        verbose_name = 'Категорию'  # Переименование заголовков в админ панеле
        verbose_name_plural = 'Катагории'  # Переименование заголовков в админ панеле


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolut_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')  # Загружать все файлы в директорию 'uploads_model'


class AboutDev(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.CharField(max_length=500, blank=True, verbose_name='О себе')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', default=None, blank=True,
                              null=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Создатель сайта'
        verbose_name_plural = 'Создатель сайта'



class Contact(models.Model):
    company = models.CharField(max_length=50, verbose_name='Компания')
    city = models.CharField(max_length=50, blank=True, verbose_name='Город')
    street = models.CharField(max_length=50, verbose_name='Улица')
    name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    telephone = models.IntegerField(unique=True,verbose_name='Номер телефона')
    email = models.EmailField(unique=True, null=True, verbose_name='E-mail')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.name