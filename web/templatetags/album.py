from django.template import Library
from django.conf import settings

register = Library()

@register.simple_tag
def album_desc():
    return settings.ALBUM_DESC

@register.simple_tag
def bgimg(url):
    ext = url.split('.')[-1]
    if ext == 'mp4' or ext == 'MP4':
        return 'http://q90vhkwl9.bkt.clouddn.com/Xnip2020-04-21_00-06-23.jpg'
    return url

@register.simple_tag
def album_headimg():
    return settings.ALBUM_HEADIMG if settings.ALBUM_HEADIMG else 'http://q90vhkwl9.bkt.clouddn.com/norway-4230682_1920.jpg'