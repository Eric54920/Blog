from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
from web.forms.login import LoginForm
from web.forms.article import ArticleForm
from web.forms.album import AlbumForm
from web.forms.about import AboutForm
from web import models
from web.utils.pagination import Pagination
from web.utils.qiniu import upload, get_token, delete_file

def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'admin/login.html', {'form': form})

    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        curr_user = models.User.objects.filter(username=username, password=password).first()
        if not curr_user:
            form.add_error('username', '用户不存在')
            return render(request, 'admin/login.html', {'form': form})
        request.session['user'] = curr_user.username
        request.session.set_expiry(60 * 60 * 24 * 14)
        return redirect('dashboard')
    return render(request, 'admin/login.html', {'status': False, 'form': form})

def logout(request):
    request.session['user'] = ""
    request.session.set_expiry(0)
    return redirect(reverse('login'))

def dashboard(request):
    article = models.Article.objects.all()
    context = {
        "article_count": article.count(),
        "topic_count": models.Album.objects.all().count(),
        "picture_count": models.Pictures.objects.all().count(),
        "sort_count": len(set(article.values_list('sort'))),
        "prev_pub_date": article.order_by('create_time').last().create_time,
        "comment_count": models.ArticleComments.objects.all().count()
    }

    return render(request, 'admin/dashboard.html', {'context': context})

def article(request):
    """文章"""
    article = models.Article.objects.all().order_by('-create_time').values('pk', 'title', 'sort', 'create_time', 'is_show')
    page_object = Pagination(
        current_page=request.GET.get('page'),
        all_count=article.count(),
        base_url=request.path_info,
        query_params=request.GET
    )
    articel_list = article[page_object.start:page_object.end]
    result = {
        'article': articel_list,
        'count': article.count(),
        'page_html': page_object.page_html()
    }
    return render(request, 'admin/article.html', {'data': result})

def article_edit(request, *args, **kwargs):
    """文章创建 & 编辑"""
    if request.method == 'GET':
        pk = request.GET.get('id')
        if not pk:
            form = ArticleForm()
            return render(request, 'admin/article_edit.html', {'form': form})
        article = models.Article.objects.filter(pk=pk).first()
        form = ArticleForm(instance=article)
        return render(request, 'admin/article_edit.html', {'form': form})

    # POST 请求不带id为创建，带为更新
    pk = request.GET.get('id', '')
    if pk:
        article = models.Article.objects.filter(pk=pk).first()
        form = ArticleForm(data=request.POST, instance=article)
    else:
        form = ArticleForm(data=request.POST)
    if form.is_valid():
        user = models.User.objects.filter(username=request.session.get('user')).first()
        form.instance.author = user
        form.save()
        return redirect('article')
    return render(request, 'admin/article_edit.html', {'status': False, 'form': form})

@csrf_exempt
def article_hide(request, *args, **kwargs):
    """隐藏文章"""
    msg = ""
    article = models.Article.objects.filter(pk=kwargs.get('id')).first()
    if article.is_show:
        article.is_show = False
        msg = "hide"
    else:
        article.is_show = True
        msg = "show"
    article.save()
    return JsonResponse({'status': 200, 'msg': msg})

@csrf_exempt
def article_delete(request, *args, **kwargs):
    """删除文章"""
    models.Article.objects.filter(pk=kwargs.get('id')).first().delete()
    return JsonResponse({'status': 200})

@csrf_exempt
def file_upload(request):
    """文件上传"""
    result = {
        'success': 0,
        'massage': None,
        'url': None
    }
    image_object = request.FILES.get('editormd-image-file')
    if not image_object:
        result['message'] = '文件不存在'
        return JsonResponse(result)
    ext = image_object.name.split('.')[-1]
    key = "{}.{}".format(uuid.uuid4(), ext)
    # qiniu upload method
    ret, info = upload(key, image_object, image_object.name, image_object.size)
    result['success'] = 1
    result['url'] = "http://q90vhkwl9.bkt.clouddn.com/" + key
    return JsonResponse(result)

def comment(request):
    """评论"""
    comments = models.ArticleComments.objects.all().order_by('-create_time')
    page_object = Pagination(
        current_page=request.GET.get('page'),
        all_count=comments.count(),
        base_url=request.path_info,
        query_params=request.GET
    )
    comment_list = comments[page_object.start:page_object.end]
    result = {
        'comments': comment_list,
        'page_html': page_object.page_html()
    }
    return render(request, 'admin/comments.html', {'data': result})

@csrf_exempt
def comment_delete(request):
    """删除评论"""
    id = request.POST.get('id')
    models.ArticleComments.objects.filter(pk=id).first().delete()
    return JsonResponse({'status': 200})

def comment_reply(request):
    """回复评论"""
    if int(request.POST.get('parent')):
        parent = request.POST.get('parent')
        reply = request.POST.get('reply')
    else:
        parent = request.POST.get('reply')
        reply = 0
    content = request.POST.get('content')
    article = request.POST.get('article')
    user = models.User.objects.filter(username=request.session.get('user')).first()
    models.ArticleComments.objects.create(parent=parent, reply=reply, content=content, 
    article_id=article, user=user.pk, nic_name=user.nic_name, web_site=user.web_site, email=user.email)
    return JsonResponse({'status': 200})

def album(request):
    """相册"""
    topic = models.Album.objects.all().values('pk', 'title', 'create_time', 'is_show')
    page_object = Pagination(
        current_page=request.GET.get('page'),
        all_count=topic.count(),
        base_url=request.path_info,
        query_params=request.GET
    )
    topic_list = topic[page_object.start:page_object.end]
    context = {
        "topic": topic_list,
        'count': topic.count(),
        'page_html': page_object.page_html()
    }
    return render(request, 'admin/album.html', {'data': context})

def album_edit(request):
    """专题创建 & 修改"""
    if request.method == 'GET':
        pk = request.GET.get('id')
        if not pk:
            form = AlbumForm()
            return render(request, 'admin/album_edit.html', {'form': form})
        album = models.Album.objects.filter(pk=pk).first()
        form = AlbumForm(instance=album)
        return render(request, 'admin/album_edit.html', {'form': form})

    # POST 请求不带id为创建，带为更新
    pk = request.GET.get('id', '') # 从路径中获取id
    if pk:
        album = models.Album.objects.filter(pk=pk).first()
        form = AlbumForm(data=request.POST, instance=album)
    else:
        form = AlbumForm(data=request.POST)
    if form.is_valid():
        user = models.User.objects.filter(username=request.session.get('user')).first()
        form.instance.poster = user
        topic = form.save()
        return redirect(reverse('album_upload', args=(topic.pk,)))
    return render(request, 'admin/album_edit.html', {'form': form})

@csrf_exempt
def album_upload(request, *args, **kwargs):
    """上传照片到相册专题"""
    album_id = kwargs.get('id')
    if request.method == "GET":
        pictures = models.Pictures.objects.filter(album=album_id).values('pk', 'url', 'intro', 'is_show')
        return render(request, 'admin/upload.html', {'data': pictures})

    data = []
    for i in request.POST.lists():
        data.append(i)
    for i in range(len(data[0][1])):
        # 判断是否已经存在此照片
        pic = models.Pictures.objects.filter(album_id=album_id, url=data[0][1][i])
        # 不存在则创建
        if not pic:
            models.Pictures.objects.create(album_id=album_id, url=data[0][1][i], intro=data[1][1][i])
        # 存在则更新
        else:
            models.Pictures.objects.filter(album_id=album_id, url=data[0][1][i]).update(intro=data[1][1][i])
    pictures = models.Pictures.objects.filter(album=album_id).values('pk', 'url', 'intro', 'is_show')
    return render(request, 'admin/upload.html', {'data': pictures})

@csrf_exempt
def picture_upload(request):
    """文件上传"""
    result = {
        'success': 0,
        'massage': None,
        'url': None
    }
    image_object = request.FILES.get('file')
    if not image_object:
        result['message'] = '文件不存在'
        return JsonResponse(result)
    ext = image_object.name.split('.')[-1]
    key = "{}.{}".format(uuid.uuid4(), ext)
    # qiniu upload method
    ret, info = upload(key, image_object, image_object.name, image_object.size)
    result['success'] = 1
    result['url'] = "http://q90vhkwl9.bkt.clouddn.com/" + key
    return JsonResponse(result)

@csrf_exempt
def album_hide(request, *args, **kwargs):
    """隐藏专题"""
    msg = ""
    album = models.Album.objects.filter(pk=kwargs.get('id')).first()
    if album.is_show:
        album.is_show = False
        msg = "hide"
    else:
        album.is_show = True
        msg = "show"
    album.save()
    return JsonResponse({'status': 200, 'msg': msg})

@csrf_exempt
def album_delete(request, *args, **kwargs):
    """删除专题"""
    album = models.Album.objects.filter(pk=kwargs.get('id')).first()
    # 删除专题下所有文件
    pictures = models.Pictures.objects.filter(album_id=album.pk)
    for picture in pictures:
        key = picture.url.split('com/')[-1]
        ret, info = delete_file(key)
        picture.delete()
    album.delete()
    return JsonResponse({'status': 200})

@csrf_exempt
def picture_hide(request, *args, **kwargs):
    """隐藏专题"""
    msg = ""
    picture = models.Pictures.objects.filter(pk=kwargs.get('id')).first()
    if picture.is_show:
        picture.is_show = False
        msg = "hide"
    else:
        picture.is_show = True
        msg = "show"
    picture.save()
    return JsonResponse({'status': 200, 'msg': msg})

@csrf_exempt
def picture_delete(request, *args, **kwargs):
    """删除照片"""
    picture = models.Pictures.objects.filter(pk=kwargs.get('id')).first()
    key = picture.url.split('com/')[-1]
    ret, info = delete_file(key)
    picture.delete()
    return JsonResponse({'status': 200})

def settings(request):
    """关于"""
    user = models.User.objects.filter(username=request.session.get('user')).first()
    if request.method == "GET":
        form = AboutForm(instance=user)
        return render(request, 'admin/about.html', {'form': form})
    form = AboutForm(instance=user, data=request.POST)
    if form.is_valid():
        form.save()
        return render(request, 'admin/about.html', {'form': form})