from django.template import Library

register = Library()

@register.filter
def bgimg(url):
    ext = url.split('.')[-1]
    if ext == 'mp4' or ext == 'MP4':
        return 'http://q90vhkwl9.bkt.clouddn.com/Xnip2020-04-21_00-06-23.jpg'
    return url