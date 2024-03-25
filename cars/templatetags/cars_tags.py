from django import template
from cars.models import Category, TagPost
from django.db.models import Count

from cars.utils import menu

register = template.Library()


@register.simple_tag
def get_menu():
    '''Что бы пробросить коллекцию меню черtз тег get_menu'''
    return menu

@register.inclusion_tag('cars/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count('posts')).filter(total__gt= 0)
    return {'cats' : cats, 'cat_selected' : cat_selected}

@register.inclusion_tag('cars/list_tags.html')
def show_all_tags(cat_selected=0):
    return {'tags' : TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}