# 基本配置
# 站点LOGO、标签icon
LOGO = "http://q90vhkwl9.bkt.clouddn.com/010a2b564548466ac7259e0fe9566e.jpg%402o.jpg"
# 头像
AVATAR = "http://q90vhkwl9.bkt.clouddn.com/010a2b564548466ac7259e0fe9566e.jpg%402o.jpg"
# 站点名称
SITE_NAME = "马国栋的博客"
# 作者
AUTHOR = "马国栋"
# 签名
SIGNATURE = "We.changeWorld(code);"
# 站点关键字
KEYWORDS = "马国栋博客,果冻的博客,技术博客,博客,技术文章,maguodong.com,maguodong,python,Django,WEB开发,前端开发,爬虫,机器学习,相册"
# 站点描述
DESC = "分享学习心得，技术要点，记录生活点滴。"
# 相册描述
ALBUM_DESC = "我们如同一棵大树的枝叶，尽自己所能开得繁茂一些、再繁茂一些，长长地伸出去，去触碰云朵，去扰乱风儿。我们贪恋阳光和雨露，挽留唱歌的黄鹂鸟，也在暴雨雷电中抖落着身躯。但，我一回头，就看见了你呀。同根同脉，生生不息。"
# 相册头图
ALBUM_HEADIMG = "https://ae01.alicdn.com/kf/Ud979da36a7aa4cb6809c564818e4c8c0q.jpg"


# 社交信息
SOCIAL = {
    "GITHUB": {
        "icon": "fa fa-github",
        "url": "https://github.com/Eric54920"
    },
    "WEIBO": {
        "icon": "fa fa-weibo",
        "url": "https://weibo.com/u/2141997680"
    },
    "EMAIL": {
        "icon": "fa fa-envelope",
        "url": "mailto:realmaguodong@outlook.com"
    },
    "INSTAGRAM": {
        "icon": "fa fa-instagram",
        "url": "https://www.instagram.com/guodong_ma/"
    },
    "TWITTER": {
        "icon": "fa fa-twitter",
        "url": "https://twitter.com/realmaguodong"
    },
    "FACEBOOK": {
        "icon": "fa fa-facebook-square",
        "url": "https://www.facebook.com/profile.php?id=100014614991188"
    }
}

# 提交链接
SITE_VERIFICATION = {
    # Google
    "google": "pDDOXfDq08OO3V-4AKWqEJw6S04QHJORgY68WYKLjiQ",
    # 百度
    "baidu": "7k6U0ihM6b"
}

# 版权信息
COPY_RIGHT = "Copyright © 2017-2020 马国栋 All Reversed 京ICP备12314256号"

# 调试
DEBUG = False

# 七牛相关配置
QINIU = {
    "ACCESS_KEY": "Li7g8EG8gxycH_-AFSwhGLKXcp1N-2CoALtUevWK",
    "SECRET_KEY": "xRpgLFbR6tTwpCIdCnyxT6U2xu7EYD8Y1f-4fDde",
    "BUCKET": "maguodong"
}

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'BlogDB',
        'HOST': '182.92.99.3',
        'PORT': 3306,
        'USER': 'Eric',
        'PASSWORD': ''
    }
}

# 部署时的静态资源存储位置
STATIC_ROOT= '/opt/pro/static/blog/static'
