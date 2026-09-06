import re
from django.shortcuts import redirect, reverse
from django.conf import settings


class AuthMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        username = request.session.get("user", "")
        path = request.path_info

        # 判断是否在白名单中
        for pattern in settings.WHITE_REGEX_URL_LIST:
            if re.match(r"^{}".format(pattern), path):
                return self.get_response(request)

        # 判断是否登录
        if not username:
            return redirect(reverse('login'))
        return self.get_response(request)
