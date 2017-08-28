from django.contrib import admin
from .models import Post, Category, Tag, Timeline

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author', 'status']
    # 侧边栏加入分类导航
    list_filter = ['status', 'category', 'author']
    # 搜索范围加入标题
    search_fields = ['title']
    # 为创建时间添加面包削导航
    date_hierarchy = 'created_time'
    # 新建用户时选择作者变为搜索ID而不是下拉框
    raw_id_fields = ['author']


class TimeLineAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time']


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Timeline, TimeLineAdmin)
