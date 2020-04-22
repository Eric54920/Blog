"""
分页组件应用：
1. 在视图函数中
    queryset = models.Issues.objects.filter(project_id=project_id)
    page_object = Pagination(
        current_page=request.GET.get('page'),
        all_count=queryset.count(),
        base_url=request.path_info,
        query_params=request.GET
    )
    issues_object_list = queryset[page_object.start:page_object.end]

    context = {
        'issues_object_list': issues_object_list,
        'page_html': page_object.page_html()
    }
    return render(request, 'issues.html', context)
2. 前端
    {% for item in issues_object_list %}
        {{item.xxx}}
    {% endfor %}

     <nav aria-label="...">
        <ul class="pagination" style="margin-top: 0;">
            {{ page_html|safe }}
        </ul>
    </nav>
"""


class Pagination(object):
    def __init__(self, current_page, all_count, base_url, query_params, per_page=30, pager_page_count=11):
        """
        分页初始化
        :param current_page: 当前页码
        :param per_page: 每页显示数据条数
        :param all_count: 数据库中总条数
        :param base_url: 基础URL
        :param query_params: QueryDict对象，内部含所有当前URL的原条件
        :param pager_page_count: 页面上最多显示的页码数量
        """
        self.base_url = base_url
        try:
            self.current_page = int(current_page)
            if self.current_page <= 0:
                self.current_page = 1
        except Exception as e:
            self.current_page = 1
        query_params = query_params.copy()
        query_params._mutable = True
        self.query_params = query_params
        self.per_page = per_page
        self.all_count = all_count
        self.pager_page_count = pager_page_count
        pager_count, b = divmod(all_count, per_page)
        if b != 0:
            pager_count += 1
        self.pager_count = pager_count

        half_pager_page_count = int(pager_page_count / 2)
        self.half_pager_page_count = half_pager_page_count

    @property
    def start(self):
        """
        数据获取值起始索引
        :return:
        """
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        """
        数据获取值结束索引
        :return:
        """
        return self.current_page * self.per_page

    def page_html(self):
        """
        生成HTML页码
        :return:
        """
        if self.all_count == 0:
            return ""

        # 如果数据总页码pager_count<11 pager_page_count
        if self.pager_count < self.pager_page_count:
            pager_start = 1
            pager_end = self.pager_count
        else:
            # 数据页码已经超过11
            # 判断： 如果当前页 <= 5 half_pager_page_count
            if self.current_page <= self.half_pager_page_count:
                pager_start = 1
                pager_end = self.pager_page_count
            else:
                # 如果： 当前页+5 > 总页码
                if (self.current_page + self.half_pager_page_count) > self.pager_count:
                    pager_end = self.pager_count
                    pager_start = self.pager_count - self.pager_page_count + 1
                else:
                    pager_start = self.current_page - self.half_pager_page_count
                    pager_end = self.current_page + self.half_pager_page_count

        page_list = []

        if self.current_page <= 1:
            prev = ' <li class="page-item"><a class="page-link" href="#">上一页</a></li>'
        else:
            self.query_params['page'] = self.current_page - 1
            prev = '<li class="page-item"><a class="page-link" href="%s?%s">上一页</a></li>' % (self.base_url, self.query_params.urlencode())
        page_list.append(prev)
        for i in range(pager_start, pager_end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                tpl = '<li class="page-item active"><a class="page-link" href="%s?%s">%s</a></li>' % (
                    self.base_url, self.query_params.urlencode(), i,)
            else:
                tpl = '<li class="page-item"><a class="page-link" href="%s?%s">%s</a></li>' % (self.base_url, self.query_params.urlencode(), i,)
            page_list.append(tpl)

        if self.current_page >= self.pager_count:
            nex = '<li class="page-item"><a class="page-link" href="#">下一页</a></li>'
        else:
            self.query_params['page'] = self.current_page + 1
            nex = '<li class="page-item"><a class="page-link" href="%s?%s">下一页</a></li>' % (self.base_url, self.query_params.urlencode(),)
        page_list.append(nex)

        if self.all_count:
            tpl = "<li class='page-item disabled'><a class='page-link'>共%s条数据，页码%s/%s页</a></li>" % (
            self.all_count, self.current_page, self.pager_count,)
            page_list.append(tpl)
        page_str = "".join(page_list)
        return page_str