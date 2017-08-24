from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_published_num(self):
        return self.post_set.filter(status=1).count()


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=1)


class Post(models.Model):
    STATUS_CHOICES = (
        (0, '未发表'),
        (1, '已发表')
    )
    title = models.CharField(max_length=70, verbose_name='标题')
    body = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='摘要')
    category = models.ForeignKey(Category, verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签云')
    author = models.ForeignKey(User, verbose_name='作者')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览数')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='发布状态')
    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']