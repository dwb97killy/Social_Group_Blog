from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from group.models import GroupInfo, GroupMember
from group import models
from blog import models as blog_models
from group.forms import GroupInfoForm
from django.urls import reverse_lazy


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    redirect_field_name = '/'  # 如果没有登录，则自动跳转到登录界面

    # fields = ("name", "description")
    form_class = GroupInfoForm
    model = GroupInfo
    template_name = 'group/create_group.html'
    success_url = reverse_lazy("group:create_group_success")

    def form_valid(self, form):
        form.instance.create_user = self.request.user
        return super().form_valid(form)


class CreateGroupSuccess(generic.TemplateView):
    template_name = 'group/group_create_success.html'


class GroupDetail(generic.DetailView):
    model = GroupInfo
    template_name = 'group/group_detail.html'


class AllGroup(generic.ListView):
    model = GroupInfo
    template_name = 'group/group_list.html'


class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("group:group_detail", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(GroupInfo, slug=self.kwargs.get("slug"))
        try:
            GroupMember.objects.create(member=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, ("Warning, already a member of {}".format(group.name)))
        else:
            messages.success(self.request, "You are now a member of the {} group.".format(group.name))
        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("group:group_detail", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(member=self.request.user, group__slug=self.kwargs.get("slug")).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, "You can't leave this group because you aren't in it.")
        else:
            membership.delete()
            messages.success(self.request, "You have successfully left this group.")
        return super().get(request, *args, **kwargs)


class DeleteGroup(LoginRequiredMixin, generic.DeleteView):
    model = GroupInfo
    template_name = "group/delete_confirm.html"
    success_url = reverse_lazy('group:all_group')