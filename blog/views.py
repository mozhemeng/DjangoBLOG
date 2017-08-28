from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Category, Tag, Timeline
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
from .forms import EmailForm
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib import messages
from blog.tasks import sendemail


class IndexView(ListView):
    # model = Post
    queryset = Post.published.all()
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number-3) if (page_number-3)>0 else 0:page_number-1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=['markdown.extensions.extra',
                                           'markdown.extensions.codehilite',
                                           TocExtension(slugify=slugify)])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        # 相似博文推荐 TODO:这里逻辑还不清楚
        tag_list = self.object.tags.values_list('pk', flat=True)
        sim_post = Post.published.filter(tags__in=tag_list).exclude(pk=self.object.pk)
        sim_post = sim_post.annotate(same_tag=Count('tags')).order_by('-same_tag', '-created_time')[:5]
        context.update({
            'form': form,
            'comment_list': comment_list,
            'sim_post': sim_post
        })
        return context


class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month)


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def email_share(request, pk):
    post = get_object_or_404(Post, pk=pk, status=1)
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            # cleaned_data只会包含验证通过的字段
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = "{}分享给您来自 MZM's Blog 的文章:{}".format(data['name'], post.title)
            message = "文章题目：{}\n阅读地址：{} \n分享留言:{}".format(post.title, post_url, data['comment'])
            send_mail(subject, message, 'moflasky@163.com', [data['to']])
            #sendemail.delay(subject, message, [data['to']])
            messages.success(request, '邮件已发送，分享成功！')
            return redirect(post)
    else:
        form = EmailForm()
    return render(request, 'blog/emailshare.html', {'form': form, 'post': post})


def about_me(request):
    timelines = Timeline.objects.all()
    return render(request, 'blog/aboutme.html', {'timelines': timelines})
