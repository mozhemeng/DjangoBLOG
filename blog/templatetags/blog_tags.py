from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count


register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.published.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    return Post.published.dates('created_time', 'month', order='DESC')


# TODO:计算post的数量时，能否对post进行filter过滤
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)