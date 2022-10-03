from django.db import models
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()
# import misaka
from blog import models as blog_models
# https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
register = template.Library()

# Create your models here.
class GroupInfo(models.Model):
    name = models.CharField(max_length=255, unique=True)
    create_user = models.ForeignKey(User, related_name='create_user', on_delete=models.CASCADE)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through="GroupMember")
    create_time = models.DateTimeField(default=timezone.now)  # 创建时间

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("group:group_detail", kwargs={"slug": self.slug})

    def published_blog(self):
        return blog_models.Blog.objects.filter(group__exact=self, publish_time__isnull=False).count()

    class Meta:
        ordering = ["-create_time"]


class GroupMember(models.Model):
    group = models.ForeignKey(GroupInfo, related_name='memberships', on_delete=models.CASCADE)
    member = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)
    join_time = models.DateTimeField(default=timezone.now)  # 创建时间

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("group", "member")


