from django.template import Library
from django.conf import settings
import random

register = Library()
@register.filter
def toLst(str):
    lst = str.split('|')
    return lst

@register.filter
def color(string):
    return settings.COLOR_LIST.get(string, '')

@register.filter
def avatarColor(string):
    return "rgb("+ str(random.randrange(50, 200)) +", "+ str(random.randrange(50, 200)) +", "+ str(random.randrange(50, 200)) +")"