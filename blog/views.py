from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from braces.views import SelectRelatedMixin
from . import forms
from . import models
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
User = get_user_model()


class BlogList(SelectRelatedMixin, generic.ListView):
    model = models.Blog
    select_related = ("user", "group")


class UserBlog(generic.ListView):
    model = models.Blog
    template_name = "blog/user_post_list.html"

    def get_queryset(self):
        try:
            self.user = User.objects.prefetch_related("posts").get(username__iexact=self.kwargs.get("username"))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


'''class BlogDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )'''


class BlogDetail(generic.DetailView):
    model = models.Blog
    template_name = 'blog/blog_detail.html'


class CreateBlog(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    redirect_field_name = '/'  # 如果没有登录，则自动跳转到登录界面
    fields = ('title', 'tag', 'content', "group")
    # form_class = forms.BlogForm
    model = models.Blog
    template_name = "blog/create_blog.html"
    success_url = reverse_lazy("blog:blog_create_success")
    '''
    # dispatch方法接受请求并最终返回响应。通常，它通过调用另一个方法(如get)来返回响应。把它看作是请求和响应之间的中间人。
    def dispatch(self, *args, **kwargs):
        return super(CreateBlog, self).dispatch(*args, **kwargs)'''

    # get_form_kwargs()：由FormMixin定义，执行表单类实例化过程
    '''def get_form_kwargs(self):
        kwargs = super(CreateBlog, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})  # 将user信息通过kwargs传入forms中，这样forms就能通过重写__init__来获得kwargs传入的参数，在这里也就是user      
        return kwargs'''
    # 或者也可以调用get_form()：由FormMixin定义，调用get_form_kwargs()完成表单类的实例化
    # 调用get_form()就不需要在forms里面重写__init__函数来传递request参数
    # 所以可以不用倒入forms.py中的表格并设置form_class，直接用fields就行
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(CreateBlog, self).get_form()
        # Q() | Q() 用来设置多个过滤条件，逻辑为或
        form.fields["group"].queryset = models.GroupInfo.objects.filter(Q(pk__in=self.request.user.user_groups.values_list("group__pk")) | Q(create_user=self.request.user))
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.publisher = self.request.user
        self.object.save()
        return super().form_valid(form)


class CreateBlogSuccess(generic.TemplateView):
    template_name = 'blog/blog_create_success.html'


class DeleteBlog(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Blog
    select_related = ("publisher", "group")
    template_name = 'blog/delete_blog.html'
    message = 'You deleted this blog successfully'

    def get_object(self, queryset=None):
        object = super(DeleteBlog, self).get_object(queryset=queryset)
        if object.publisher.username != self.request.user.username:
            # if object.user != self.request.user:
            raise PermissionDenied
            # raise Http404()
        return object

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(publisher_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('account:user_profile_login', kwargs={'pk': self.request.user.pk})


class UpdateBlog(LoginRequiredMixin, generic.UpdateView):
    redirect_field_name = '/'  # 如果没有登录，则自动跳转到登录界面
    form_class = forms.BlogForm
    model = models.Blog
    template_name = "blog/update_blog.html"  # template会有预设的名称，但还是要显式的定义出来更直观一点

    def form_valid(self, form):  # 设置外键的值，将目前用户和发的blog关联起来
        self.object = form.save(commit=False)
        self.object.modify_time = timezone.now()
        self.object.save()
        return super().form_valid(form)
        # form.instance.modify_time = timezone.now()

    def get_form_kwargs(self):
        kwargs = super(UpdateBlog, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})  # 将user信息通过kwargs传入forms中，这样forms就能通过重写__init__来获得kwargs传入的参数，在这里也就是user
        return kwargs


class DraftBlog(LoginRequiredMixin, generic.ListView):
    redirect_field_name = '/'  # 如果没有登录，则自动跳转到登录界面
    model = models.Blog
    template_name = "blog/draft_list.html"  # template会有预设的名称，但还是要显式的定义出来更直观一点
    def get_queryset(self):
        return models.Blog.objects.filter(publish_time__isnull=True, publisher__exact=self.request.user.pk).order_by('-create_time')


@login_required
def approve_comment(request, username, pk):
    blog = get_object_or_404(models.Blog, pk=pk)
    blog.approve()
    return redirect('blog:blog_detail', username=username, pk=blog.pk)


@login_required
def notapprove_comment(request, username, pk):
    blog = get_object_or_404(models.Blog, pk=pk)
    blog.notapprove()
    return redirect('blog:blog_detail', username=username, pk=blog.pk)


@login_required
def add_comment(request, username, pk):
    blog = get_object_or_404(models.Blog, pk=pk)
    if request.method == 'POST':
        form = forms.CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.publisher = request.user
            comment.relatedblog = blog
            comment.save()
            return redirect('blog:blog_detail', username=username, pk=blog.pk)
    else:
        form = forms.CommentsForm()
    return render(request, 'blog/comment.html', {'form': form})


@login_required
def publish_blog(request, username, pk):
    blog = get_object_or_404(models.Blog, pk=pk)
    blog.publish()
    return redirect('blog:blog_detail', username=username, pk=pk)


@login_required
def delete_comment(request, username, pk):
    comment = get_object_or_404(models.Comments, pk=pk)
    blog_pk = comment.relatedblog.pk
    comment.delete()
    return redirect('blog:blog_detail', username=username, pk=blog_pk)