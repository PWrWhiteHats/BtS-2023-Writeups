from django import forms

from main.models import User, Profile, Post


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=User.username.field.max_length
    )

    password = forms.CharField(
        max_length=User.password.field.max_length
    )


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('location', 'birth_date',)


class PostForm(forms.Form):
    message = forms.CharField(max_length=Post.message.field.max_length)
