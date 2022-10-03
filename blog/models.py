from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
# import misaka
from group.models import GroupInfo
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class Blog(models.Model):
    publisher = models.ForeignKey(User, related_name="blog_publisher", on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    tag = models.CharField(max_length=256)
    create_time = models.DateTimeField(default=timezone.now)  # 创建时间
    publish_time = models.DateTimeField(blank=True, null=True)  # 发布时间
    content = models.TextField()
    content_html = models.TextField(editable=False)
    group = models.ForeignKey(GroupInfo, related_name="blog_group", on_delete=models.CASCADE)
    modify_time = models.DateTimeField(default=timezone.now)  # 修改时间
    approve_comments = models.BooleanField(default=True)  # 是否允许评论

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # self.content_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def publish(self):
        self.publish_time = timezone.now()
        self.save()

    def modify(self):
        self.modify_time = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("blog:blog_detail", kwargs={"username": self.publisher.username, "pk": self.pk})

    def approve(self):
        self.approve_comments = True
        self.save()

    def notapprove(self):
        self.approve_comments = False
        self.save()

    def count_comments(self):
        if self.approve_comments == True:
            return self.comments.filter(create_time__isnull=False)
        else:
            return self.comments.filter(create_time__isnull=True)

    def get_comments(self):
        return self.filter(approve_comments=True)  # 挑选出允许comment的blog

    class Meta:
        ordering = ["-create_time"]
        # unique_together = ["publisher", "content"]


class Comments(models.Model):
    relatedblog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')  # 外键连接相关Blog
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.publisher

    def get_absolute_url(self):  # 获得每个blog的域名
        return reverse('blog_content', kwargs={'pk': self.relatedblog})