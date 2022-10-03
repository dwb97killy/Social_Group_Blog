from django import forms
from . import models
from django.db.models import Q


class BlogForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'tag', 'content', "group")
        model = models.Blog

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(BlogForm, self).__init__(*args, **kwargs)
        # Q() | Q() 用来设置多个过滤条件，逻辑为或
        self.fields["group"].queryset = models.GroupInfo.objects.filter(Q(pk__in=user.user_groups.values_list("group__pk")) | Q(create_user=user))


class CommentsForm(forms.ModelForm):
    class Meta:
        model = models.Comments
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }