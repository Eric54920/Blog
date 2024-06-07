from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from web import models
from collections import Counter
from web.utils.pagination import Pagination
from lxml import etree
from web.forms.comment import CommentForm
import uuid

# Create your views here.
def home(request, *args, **kwargs):
    """获取所有文章和分类"""
    articles = models.Article.objects.filter(is_show=True)
    sort_by = request.GET.get('sort', '')
    query = request.GET.get('query', '').strip()
    if query:
        article = articles.filter(Q(title__icontains=query)|Q(content_html__icontains=query)|Q(abstract__icontains=query))
    elif sort_by:
        article = articles.filter(sort=request.GET.get('sort'))
    else:
        article = articles
    article = article.order_by('-create_time').values('pk', 'title', 'abstract', 'sort', 'tags', 'create_time')

    page_object = Pagination(
        current_page=request.GET.get('page'),
        all_count=article.count(),
        base_url=request.path_info,
        query_params=request.GET
    )
    articel_list = article[page_object.start:page_object.end]

    result = {
        # 文章列表
        'article': articel_list,
        # 分类
        'sort': sorted(Counter(articles.values_list('sort')).items(), key=lambda x:x[1], reverse=True),
        # 文章总数量
        'article_count': articles.count(),
        # 当前搜索或分类下的总数
        'article_curr_count': article.count(),
        # 搜索内容
        'query': query if query else None,
        # 照片总户数量
        'picture_count': models.Pictures.objects.all().count(),
        # 分页
        'page_html': page_object.page_html()
    }
    return render(request, 'index.html', {'data': result})

def article_detail(request, *args, **kwargs):
    """文章详情"""
    pk = kwargs.get('id')
    article = models.Article.objects.filter(pk=pk).first()

    if not article:
        return redirect("/")

    # 获取目录
    html = etree.HTML(article.content_html)
    h3_list = html.xpath('//h3')
    catelog = []
    for h3 in h3_list:
        try:
            catelog.append({'id': h3.xpath('./@id')[0], 'title': h3.xpath('./text()')[0]})
        except Exception:
            catelog = []
    # 获取评论
    # {
    #   pk: {
    #       user: {},
    #       content: ....,
    #       sub_com: [
    #           {
    #               user: ...,
    #               content: ...
    #           },
    #           {
    #               user: ...,
    #               content: ....
    #           }
    #       ]
    #   }
    # }
    comment_dic = {}
    comments = models.ArticleComments.objects.filter(article_id=pk).order_by('create_time')
    for comment in comments:
        if comment.parent:
            comment_dic[comment.parent].setdefault('sub_comments', [])
            comment_dic[comment.parent]['sub_comments'].append({
                "pk": comment.pk,
                "user": comment.user,
                "nic_name": comment.nic_name,
                "web_site": comment.web_site,
                "email": comment.email,
                "content": comment.content,
                "ctime": comment.create_time,
                "reply_to": models.ArticleComments.objects.filter(pk=comment.reply).first().nic_name if comment.reply else None,
                "reply_web_site": models.ArticleComments.objects.filter(pk=comment.reply).first().web_site if comment.reply else None,
                "reply_user": models.ArticleComments.objects.filter(pk=comment.reply).first().user if comment.reply else None
            })
        else:
            comment_dic[comment.pk] = {
                "pk": comment.pk,
                "user": comment.user,
                "nic_name": comment.nic_name,
                "web_site": comment.web_site,
                "email": comment.email,
                "content": comment.content,
                "ctime": comment.create_time,
            }
    context = {
        'article': article,
        'catelog': catelog,
        'comment_form': CommentForm(),
        'comments': comment_dic.values()
    }
    return render(request, 'article.html', {'data': context})

@csrf_exempt
def article_comment(request, *args, **kwargs):
    """创建评论"""
    article = kwargs.get('id')
    form = CommentForm(data=request.POST)
    if form.is_valid():
        form.instance.user = uuid.uuid4()
        form.instance.article_id = article
        form.instance.parent = request.POST.get('parent', 0)
        form.instance.reply = request.POST.get('reply', 0)
        comment = form.save()
        context = {
            "pk": comment.pk,
            "nic_name": comment.nic_name,
            "web_site": comment.web_site,
            "email": comment.email,
            "content": comment.content,
            "ctime": comment.create_time,
            "parent": comment.parent,
            "reply": comment.reply,
            "reply_user": models.ArticleComments.objects.filter(reply=comment.reply).first().user,
        }
        # 如果是回复子评论的
        if not int(comment.reply) == 0:
            reply_to = models.ArticleComments.objects.filter(pk=comment.reply).first()
            context['reply_to'] = {
                "nic_name": reply_to.nic_name,
                "web_site": reply_to.web_site,
                "user": reply_to.user,
            }
        return JsonResponse({'status': 200, 'comment': context})
    return JsonResponse({'status': 400})

def archives(request):
    """归档"""
    article = models.Article.objects.filter(is_show=True).order_by('-create_time').values('pk', 'title', 'sort', 'create_time')
    # {
    #     '2020': [article, ...],
    #     '2021': [article, ...]
    # }
    archives = {}
    for article in list(article):
        archives.setdefault(str(article['create_time'])[:4], [])
        archives[str(article['create_time'])[:4]].append(article)
    return render(request, 'archives.html', {'archives': archives.items()})

def album(request):
    """相册"""
    topic = models.Album.objects.filter(is_show=True).values('pk', 'title')
    for tpc in list(topic):
        try:
            tpc['url'] = models.Pictures.objects.filter(album_id=tpc['pk']).first().url
        except:
            continue
    return render(request, 'album/album.html', {'data': topic})

def album_detail(request, *args, **kwargs):
    pictures = models.Pictures.objects.filter(album_id=kwargs.get('id'), is_show=True).values('pk', 'intro', 'url')
    topic = models.Album.objects.filter(pk=kwargs.get('id')).first()
    context = {
        "pictures": pictures,
        "topic": {
            'title': topic.title,
            'intro': topic.intro,
            'create_time': topic.create_time
        }
    }
    return render(request, 'album/picture.html', {'data': context})

def about(request):
    obj = models.User.objects.all().first()
    user = {
        'intro': obj.intro,
        'skill': obj.skill,
    }
    return render(request, 'about.html', {'user': user})
