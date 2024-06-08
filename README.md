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
- 添加`local_settings.py`配置文件

```conf
DEBUG = True

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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 基本配置
# 站点LOGO、标签icon
LOGO = "https://s21.ax1x.com/2024/06/07/pktJ4Tx.png"
# 头像
AVATAR = "https://s21.ax1x.com/2024/06/07/pktJ4Tx.png"
# 站点名称
SITE_NAME = "我的小站"
# 作者
AUTHOR = "Eric"
# 签名
SIGNATURE = "千里之行，始于足下"
# 站点关键字
KEYWORDS = ""
# 站点描述
DESC = ""
# 相册描述
ALBUM_DESC = ""
# 相册头图
ALBUM_HEADIMG = "https://s21.ax1x.com/2024/06/07/pktYEBn.jpg"

# 社交信息
SOCIAL = {
    "GITHUB": {
        "icon": "fa", # 示例：fa-github
        "url": "" # 示例：https://github.com/用户名
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
    - 创建数据库：
  
    ```sql
    CREATE DATABASE your_db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```
    - web目录下新建migrations包
    - 迁移数据库：
  
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

- 向数据库添加管理员账号，这里没有做管理员注册的功能，所以要手动向数据库写入：
    ```sql
    INSERT into web_user(username, `password`, nic_name) values (用户名, 密码(sha256值), 昵称);
    ```
- 启动项目
    
    ```bash
    python3 manage.py runserver`
    ```
    首页地址：`/`

    管理员登录地址：`/login`

## 须知
撰写文章时，标题要用h3，也就是`###`，以便于生成目录。
