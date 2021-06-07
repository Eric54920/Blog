## 简介
这是一个基于Django开发的博客系统，包含前端和后台管理系统，支持Markdown编辑，前端使用了Bootstrap 4，样式简洁，风格类似GitHub。

## 为何开发这款博客
之前使用过WordPress、Hexo等博客框架，由于功能繁重，样式不喜欢，或Hexo访问速度太慢的原因，所以自己动手写了一款。

## 功能列表
### 前台
- 首页
    - 搜索
    - 文章详细
    - 匿名评论
- 归档
- 相册
    - 相册详细
- 关于
### 后台管理
- 概览
- 文章增删改、隐藏、批量删除
- 相册专题添加，照片视频增删、隐藏、批量删除
- 评论回复、删除
- 个人信息修改

## 如何使用

- 创建虚拟环境保证项目不被污染，并激活
- 克隆项目：`https://github.com/Eric54920/Blog.git`
- `pip install -r requirement.txt`安装项目所需依赖
- 修改settings.py配置文件
```conf
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'HOST': '',
        'PORT': ,
        'USER': '',
        'PASSWORD': ''
    }
}

# 部署时的静态资源存储位置
STATIC_ROOT= 'xxx'

# 基本配置
# 站点LOGO、标签icon
LOGO = "logo cdn地址"
# 头像
AVATAR = "头像 cdn地址"
# 站点名称
SITE_NAME = "博客名称"
# 作者
AUTHOR = "作者名称"
# 签名
SIGNATURE = "签名"
# 站点关键字
KEYWORDS = ""
# 站点描述
DESC = ""
# 相册描述
ALBUM_DESC = ""
# 相册头图
ALBUM_HEADIMG = "cdn地址"

# 社交信息
SOCIAL = {
    "GITHUB": {
        "icon": "fa xxx", # 示例：fa-github
        "url": "xxx" # 示例：https://github.com/用户名
    }
    ...
}

# 提交链接
# meta标签中的值，例："pDDOXfDq08OO3V-4AKWqEJw6S04QHJORgY6sDXKLjiQ"
SITE_VERIFICATION = {
    # Google
    "google": "",
    # 百度
    "baidu": ""
}


# 版权信息 以下为示例
COPY_RIGHT = "Copyright © 2017-2021 作者名 All Reversed 备案号"
```
- 初始化数据库

    创建迁移：`python manage.py makemigrations`
    迁移：`python manage.py migrate`

    **须知**：要想让数据库支持`emoji`表情，则需要对数据库的编码设置为utf8mb4，可参考：[https://blog.51cto.com/suifu/1853864](https://blog.51cto.com/suifu/1853864)

- 向数据库添加管理员账号，这里没有做管理员注册的功能，所以要手动向数据库写入：
    ```sql
    insert into web_user ('username', 'password', 'nic_name') values (用户名, 密码(md5值), 昵称);
    ```
- 启动项目
    
    `python(3) manage.py runserver`
    ```
    首页地址：/
    管理员登录地址：/login
    ```

## 须知
撰写文章时，标题要用h3，也就是`###`，以便于生成目录。
