from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse
from django.conf import settings
import re

class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        username = request.session.get('user', '')
        path = request.path_info

        # 判断是否在白名单中
        for i in settings.WHITE_REGEX_URL_LIST:
            if re.match(r'^{}'.format(i), path):
                return

        # 判断是否登录
        if not username:
            return redirect(reverse('login'))