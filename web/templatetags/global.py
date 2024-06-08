from django.utils.safestring import mark_safe
from django.template import Library
from django.conf import settings

register = Library()


@register.filter
def logo(string):
    """logo"""
    if string in ['icon', 'logo']:
        return settings.LOGO
    elif string == 'avatar':
        return settings.AVATAR


@register.simple_tag
def site_name():
    """站点名称"""
    return settings.SITE_NAME


@register.simple_tag
def author():
    """作者"""
    return settings.AUTHOR


@register.simple_tag
def signature():
    """签名"""
    return settings.SIGNATURE


@register.simple_tag
def copy_right():
    """版权信息"""
    return settings.COPY_RIGHT


@register.simple_tag
def desc():
    """网站描述"""
    return settings.DESC


@register.simple_tag
def keywords():
    """网站关键字"""
    return settings.KEYWORDS


@register.simple_tag
def social():
    """社交信息"""
    social_media = ""
    for name, value in settings.SOCIAL.items():
        social_media += '<a href=' + \
            value['url'] + ' class="center-y d-inline-block mx-2 rounded-circle text-light"><i class="' + \
            value['icon'] + '"></i></a>'
    return mark_safe(social_media)


@register.simple_tag
def site_verification():
    """网站验证"""
    meta_tag = ""
    for name, id in settings.SITE_VERIFICATION.items():
        meta_tag += f"<meta name = '{ name }-site-verification' content='{ id }'/>"
    return mark_safe(meta_tag)
