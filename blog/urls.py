from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    url(r'^post/(?P<pk>[0-9]+)/email_share/$', views.email_share, name='email_share'),
    url(r'^about_me/$', views.about_me, name='about_me'),
]