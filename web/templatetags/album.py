from django.template import Library
from django.conf import settings
from django.templatetags.static import static

register = Library()

ALBUM_BG = "images/bg.jpg"


@register.simple_tag
def album_desc():
    """相册描述"""
    return settings.ALBUM_DESC


@register.simple_tag
def bgimg(url):
    """背景图片"""
    ext = url.split(".")[-1]
    if ext in ("mp4", "MP4"):
        return static(ALBUM_BG)
    return url


@register.simple_tag
def album_headimg():
    """相册头图"""
    return settings.ALBUM_HEADIMG if settings.ALBUM_HEADIMG else static(ALBUM_BG)
