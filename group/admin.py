from django.contrib import admin
from group import models
# Register your models here.

class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember

admin.site.register(models.GroupInfo)