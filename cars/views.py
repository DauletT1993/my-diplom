from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import AddPostForm
from .models import Cars, TagPost, AboutDev, Contact
from .utils import DataMixin
from django.contrib.auth.decorators import login_required


class CarHome(DataMixin, ListView):
    '''Представление главной странице'''
    model = Cars
    template_name = 'cars/index.html'
    context_object_name = 'posts'  # для перебора циклом в index.html и отображение всех данных из Cars
    title_page = 'Главная страница'
    cat_selected = 0


    def get_queryset(self):
        return Cars.published.all().select_related('cat')  # Представление только опубликованных статей


'''@login_required - направит по указанному URL в settings
     или (login_url='/home/') перенаправит по указанному url'''
@login_required
def about(request):
    form = AboutDev.objects.all()
    return render(request, 'cars/about.html',
                  {'title': 'Не много обо мне', 'page_obj': form})



class ShowPost(DataMixin, DetailView):
    '''Представление статьи на странице post.html
    Класс DataMixin отвечает за наполнение стандартной информации,
    что бы сократить дублирование кода
    '''
    template_name = 'cars/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):  # Отображение только опубликованных статей
        return get_object_or_404(Cars.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    '''
    Представление добавления новой статьи в базу данных
    LoginRequiredMixin только авторизованный может добавить статью
    '''
    form_class = AddPostForm
    template_name = 'cars/addpage.html'
    title_page = 'Добавление статьи'
    permission_required = 'cars.add_cars' # Разрешение которым обладает пользователь

    def form_valid(self, form):
        c = form.save(commit=False)
        c.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    '''
    Редактирование статьи с сохранением в базу данны
    '''
    model = Cars
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'cars/addpage.html'
    title_page = 'Редактирование статьи'
    permission_required = 'cars.change_cars'


def login(request):
    return HttpResponse("Авторизация")


class CarCategory(DataMixin, ListView):
    '''Представление статей по категориям'''
    template_name = 'cars/index.html'
    context_object_name = 'posts'  # для перебора циклом в index.html и отображение всех данных из Cars
    allow_empty = False


    def get_queryset(self):
        return Cars.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категории - ' + cat.name,
                                      cat_selected=cat.pk)


class TagPostList(DataMixin, ListView):
    '''Представление статей по тегам'''
    template_name = 'cars/index.html'
    context_object_name = 'posts'  # для перебора циклом в index.html и отображение всех данных из Cars
    allow_empty =True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Cars.published.filter(tags__slug=self.kwargs['tag_slug']).select_related()


class Contact_View(DataMixin, ListView):
    model = Contact
    template_name = 'cars/contact.html'
    title_page = 'Контакты'
    context_object_name = 'contact'


@login_required
def contact(request):
    data = Contact.objects.all()
    return render(request, 'cars/contact.html',  {'title': 'Контакты', 'cont': data})

#
# data = {
#       'title': 'Контакты',
#       'city': 'г.Кокшетау',
#       'num_tel': '+77071884493',
#       'name': 'Темиржанов Даулет',
#   }