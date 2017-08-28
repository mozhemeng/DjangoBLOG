from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm
from django.contrib import messages


def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # commit=False  创建后先不提交到数据库，方便做修改
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, '回复成功！')
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list}
            return render(request, 'blog/detail.html', context=context)
    return redirect(post)

