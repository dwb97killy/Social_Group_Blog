from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
# from accounts.models import UserProfile
from django import forms

class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'User Name'
        self.fields['email'].label = 'Email'

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")


'''class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('profile_pic',)'''