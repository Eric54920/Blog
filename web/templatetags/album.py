from django.template import Library
from django.conf import settings

register = Library()


@register.simple_tag
def album_desc():
    """相册描述"""
    return settings.ALBUM_DESC


@register.simple_tag
def bgimg(url):
    """背景图片"""
    ext = url.split('.')[-1]
    if ext == 'mp4' or ext == 'MP4':
        return 'https://s21.ax1x.com/2024/06/07/pktYEBn.jpg'
    return url


@register.simple_tag
def album_headimg():
    """相册头图"""
    return settings.ALBUM_HEADIMG if settings.ALBUM_HEADIMG else 'https://s21.ax1x.com/2024/06/07/pktYEBn.jpg'
