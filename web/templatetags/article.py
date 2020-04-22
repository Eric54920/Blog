from django.template import Library
import random

register = Library()
@register.filter
def toLst(str):
    lst = str.split('|')
    return lst

@register.filter
def color(string):
    return "rgb("+ str(random.randrange(50, 255)) +", "+ str(random.randrange(50, 255)) +", "+ str(random.randrange(50, 255)) +")"

@register.filter
def avatar(string):
    return string[0]

@register.filter
def avatarColor(string):
    return "rgb("+ str(random.randrange(50, 200)) +", "+ str(random.randrange(50, 200)) +", "+ str(random.randrange(50, 200)) +")"