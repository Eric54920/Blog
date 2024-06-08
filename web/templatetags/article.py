from django.template import Library
from django.conf import settings
import random

register = Library()


@register.filter
def toLst(string):
    """文章标签分割"""
    lst = string.split('|')
    return lst


@register.filter
def color(string):
    """文章分类颜色"""
    return settings.COLOR_LIST.get(string, '')


@register.filter
def avatarColor(string):
    """评论头像颜色"""
    return "rgb(" + str(random.randrange(50, 200)) + ", " + str(random.randrange(50, 200)) + ", " + str(random.randrange(50, 200)) + ")"
