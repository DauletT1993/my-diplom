from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Cars, Category, AboutDev, Contact


@admin.register(Cars)
class WomenAdmin(admin.ModelAdmin):
    '''Отображения модели на странице администратора сайта'''
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'tags']
    readonly_fields = ['post_photo']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    list_display = (
    'title', 'post_photo', 'time_create', 'is_published', 'cat')  # Отображения полей из базы данных в админке
    list_display_links = ('title',)  # Превращение в сылку для переходя к статье
    ordering = ('-time_create', 'title')  # Сортировка по времени добабления или заголовку
    list_editable = ('is_published',)  # Возможность админу менять статус статья на черновик или опубликованно
    list_per_page = 10  # Количество отображаемых статей на странице админа
    actions = ['set_published', 'set_draft']  # Для отображения этой функции в админке
    search_fields = ['title__startswith',
                     'cat__name']  # Панель поиска по заголовку по первым буквам, и связанным категориям
    list_filter = ['cat__name', 'is_published']  # Фильтр по статусу опубликования
    save_on_top = True  # Добавления кнопок сохранить в верх траницыы

    @admin.display(description='Изображение',
                   ordering='content')  # Переименование функции для отображения в админке на русском языке
    def post_photo(self, car: Cars):
        if car.photo:
            return mark_safe(f"<img src='{car.photo.url}' width=60>")
        return "Без фото."

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):  # Возможность выбрать несколько записей и опубликовать их
        count = queryset.update(is_published=Cars.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей')  # Уведомление о выполнении

    @admin.action(description='Снять с публикации')
    def set_draft(self, request, queryset):  # Возможность выбрать несколько записей и снять их с публикации
        count = queryset.update(is_published=Cars.Status.DRAFT)
        self.message_user(request, f'{count} записей снято  с публикации', messages.WARNING)
        # Уведомление о выполнении, messages.WARNING - добавляет значок к уведомлению


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    ordering = ['-name']  # Сортировка по имени категории
    prepopulated_fields = {'slug': ('name',)}  # автоматическаое созание slug английскими буквами
    list_per_page = 10


@admin.register(AboutDev)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'photo')
    list_display_links = ('title',)
    readonly_fields = ['post_photo']

    @admin.display(description='Изображение',
                   ordering='content')  # Переименование функции для отображения в админке на русском языке
    def post_photo(self, dev: AboutDev):
        if dev.photo:
            return mark_safe(f"<img src='{dev.photo.url}' width=60>")
        return "Без фото."

@admin.register(Contact)
class Contact_Admin(admin.ModelAdmin):
    list_display = ('last_name', 'name', 'city',)