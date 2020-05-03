from django.utils.safestring import mark_safe
from django.template import Library
from django.conf import settings

register = Library()

@register.filter
def logo(string):
    if string in ['icon', 'logo']:
        return settings.LOGO
    elif string == 'avatar':
        return settings.AVATAR

@register.simple_tag
def site_name():
    return settings.SITE_NAME

@register.simple_tag
def author():
    return settings.AUTHOR

@register.simple_tag
def signature():
    return settings.SIGNATURE

@register.simple_tag
def copy_right():
    return settings.COPY_RIGHT

@register.simple_tag
def desc():
    return settings.DESC

@register.simple_tag
def keywords():
    return settings.KEYWORDS

@register.simple_tag
def social():
    SOCIAL_MEDIA = ""
    for name, value in settings.SOCIAL.items():
        SOCIAL_MEDIA += '<a href='+ value['url'] +' class="center-y d-inline-block mx-2 rounded-circle text-light"><i class="'+ value['icon'] +'"></i></a>'
    return mark_safe(SOCIAL_MEDIA)

@register.simple_tag
def site_verification():
    meta_tag = ""
    for name, id in settings.SITE_VERIFICATION.items():
        print(name, id)
        meta_tag += f"<meta name = '{ name }-site-verification' content='{ id }'/>"
    return mark_safe(meta_tag)
