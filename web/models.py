from django.db import models

# Create your models here.

class User(models.Model):
    """用户表"""
    username = models.CharField(max_length=128, verbose_name="用户名")
    password = models.CharField(max_length=256, verbose_name="密码")
    nic_name = models.CharField(max_length=128, verbose_name="昵称")
    email = models.EmailField(null=True, blank=True, verbose_name="邮箱")
    web_site = models.URLField(null=True, blank=True, verbose_name="网址")
    avatar = models.URLField(null=True, blank=True, verbose_name="头像")
    intro = models.TextField(null=True, blank=True, verbose_name="简介")
    skill = models.TextField(null=True, blank=True, verbose_name="技能")
    
class Article(models.Model):
    """文章表"""
    author = models.ForeignKey(to="User", on_delete=models.CASCADE, verbose_name="作者")
    title = models.CharField(max_length=256, verbose_name="文章标题")
    abstract = models.TextField(verbose_name="文章摘要")
    content = models.TextField(verbose_name="md文章内容")
    content_html = models.TextField(verbose_name="html文章内容")
    sort = models.CharField(max_length=128, verbose_name="分类")
    tags = models.CharField(max_length=256, verbose_name="标签")
    create_time = models.DateField(verbose_name="创建时间")
    is_show = models.BooleanField(default=1, verbose_name="是否显示")

class ArticleComments(models.Model):
    user = models.CharField(max_length=128, verbose_name="评论用户ID")
    nic_name = models.CharField(max_length=128, verbose_name="昵称")
    email = models.EmailField(verbose_name="邮箱")
    web_site = models.URLField(verbose_name="网址")
    parent = models.BigIntegerField(default=0, verbose_name="父级评论")
    reply = models.BigIntegerField(default=0, verbose_name="被回复评论")
    article = models.ForeignKey(to="Article", on_delete=models.CASCADE, verbose_name="文章")
    content = models.TextField(verbose_name="评论内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")

class Album(models.Model):
    """相册专题表"""
    poster = models.ForeignKey(to="User", on_delete=models.CASCADE, verbose_name="发布者")
    title = models.CharField(max_length=256, verbose_name="专题标题")
    intro = models.TextField(verbose_name="描述")
    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    is_show = models.BooleanField(default=1, verbose_name="是否展示")

class Pictures(models.Model):
    """照片表"""
    album = models.ForeignKey(to="Album", on_delete=models.CASCADE, verbose_name="所属专题")
    url = models.URLField(verbose_name="照片路径")
    intro = models.TextField(null=True, blank=True, verbose_name="照片描述")
    upload_time = models.DateField(auto_now_add=True, verbose_name="上传时间")
    is_show = models.BooleanField(default=1, verbose_name="是否显示")

