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

```python
import os


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get("DB_NAME", "xxx"),
        'HOST': os.environ.get("DB_HOST", "xxx"),
        'PORT': os.environ.get("DB_PORT", 3306),
        'USER': os.environ.get("DB_USER", "xxx"),
        'PASSWORD': os.environ.get("DB_PASSWORD", "xxx")
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
KEYWORDS = "关键字1,关键字2..."
# 站点描述
DESC = "这是一个blog网站"
# 相册描述
ALBUM_DESC = "分享点滴，记录美好"
# 相册头图
ALBUM_HEADIMG = "https://s21.ax1x.com/2024/06/07/pktYEBn.jpg"

# 社交信息
SOCIAL = {
    "GITHUB": {
        "icon": "fa", # 示例：fa-github，所有icon：https://www.runoob.com/font-awesome/fontawesome-reference.html
        "url": "" # 示例：https://github.com/用户名
    }
    ...
}

# 网站验证
# meta标签中的值，例："pDDOXfDq08OO3V-4AKWqEJw6S04QHJORgY6sDXKLjiQ"
SITE_VERIFICATION = {
    # Google，https://search.google.com/search-console/welcome?hl=zh-cn
    "google": "",
    # 百度，https://ziyuan.baidu.com/site/index#/
    "baidu": ""
}

# 版权信息 以下为示例
COPY_RIGHT = "Copyright © 2024 作者名 All Reversed 备案号"
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

- 向数据库添加管理员账号，这里没有做管理员注册的功能，所以要手动向数据库写入，默认密码：admin12345，请在后台及时修改：
    ```sql
    INSERT into web_user(username, `password`, nic_name) values (账号, "166e668071a25539bf48c3ae50dbd8922f9981d25b5a5fc83a33f822c1c34dfe", 昵称);
    ```

- 启动项目
    
    ```bash
    python3 manage.py runserver
    ```
    首页地址：`/`

    管理员登录地址：`/login`

## 须知
撰写文章时，标题要用h3，也就是`###`，以便于生成目录。
