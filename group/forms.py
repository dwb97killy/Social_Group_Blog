from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from group.models import GroupInfo
# from django.contrib.auth.models import User


class GroupInfoForm(forms.ModelForm):
    class Meta:
        model = GroupInfo
        # fields = ('title', 'tag', 'content')
        fields = ('name', 'description')
        widgets = {
            # 'publisher': forms.TextInput(attrs={'class': 'textinputclass'}),
            'name': forms.TextInput(attrs={'class': 'textinputclass'}),
            'description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }
        error_messages = {
            'name': {'required': "please give the group a title",},
        }
