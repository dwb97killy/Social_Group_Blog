from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views import generic
from accounts import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
# from accounts.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Blog
from group.models import GroupInfo, GroupMember

# Create your views here.

class SignUp(generic.CreateView):
    form_class = forms.UserForm
    success_url = reverse_lazy("login")
    template_name = "account/signup.html"


class DraftBlog(LoginRequiredMixin, generic.ListView):
    redirect_field_name = '/'  # 如果没有登录，则自动跳转到登录界面
    model = Blog
    template_name = "blog/draft_list.html"  # template会有预设的名称，但还是要显式的定义出来更直观一点

    def get_queryset(self):
        return Blog.objects.filter(publish_time__isnull=True, publisher__exact=self.request.user.pk).order_by('-create_time')


def user_profile_customer(request, pk):
    user = get_object_or_404(User, pk=pk)
    published_blogs = Blog.objects.filter(publisher__exact=pk, publish_time__isnull=False).order_by('-create_time')
    return render(request, 'account/profile_customer.html', {'blog_user': user, 'user': request.user, 'published_blogs': published_blogs})


@login_required
def user_profile_login(request, pk):
    user = get_object_or_404(User, pk=pk)
    published_blogs = Blog.objects.filter(publisher__exact=pk, publish_time__isnull=False).order_by('-create_time')
    created_blogs = Blog.objects.filter(publisher__exact=pk, publish_time__isnull=True).order_by('-create_time')
    created_groups = GroupInfo.objects.filter(create_user__exact=request.user)
    joined_groups = GroupMember.objects.filter(member__exact=request.user)
    return render(request, 'account/profile.html', {'user': user, 'published_blogs': published_blogs, 'created_blogs': created_blogs, 'create_groups': created_groups, 'joined_groups': joined_groups})



