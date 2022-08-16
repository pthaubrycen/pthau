from cProfile import label
from django import forms
from .models import Post, Profile
from django_summernote.widgets import SummernoteWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('user', 'title', 'category', 'content', 'thumbnail', 'status', 'tags', 'slug')
        widgets = {
            'content' : SummernoteWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'summernote'}),
            'category': forms.Select(attrs={'class': 'form-control selectric'}),
            'status': forms.Select(attrs={'class': 'form-control selectric'}),
            'thumbnail': forms.FileInput(attrs={'id': 'image-upload'}),  
            'tags': forms.TextInput(attrs={'class': 'form-control inputtags'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'password' : forms.PasswordInput(attrs={'class':'form-control'})
        }

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={'class':'form-control'}),
        }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'task', 'avatar', 'address', 'birthday']
        widgets = {
            'bio' : SummernoteWidget(),
            'bio' : forms.Textarea(attrs={'class': 'summernote'}),
            'phone' : forms.TextInput(attrs={'class':'form-control'}),
            'task' : forms.TextInput(attrs={'class':'form-control'}),
            'address' : forms.TextInput(attrs={'class':'form-control'}),
            'birthday' : forms.DateInput(attrs={'class':'form-control'}), 
            'avatar' : forms.FileInput(attrs={'class':'form-control'}),  
             
        }

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='任意。')
    last_name = forms.CharField(max_length=30, required=False, help_text='任意。')
    email = forms.EmailField(max_length=254, help_text='必要。有効な電子メール アドレスを通知します。')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields['username'].label = 'ユーザ名'
        self.fields['first_name'].label = '名前'
        self.fields['last_name'].label = '苗字'
        self.fields['email'].label = 'メール'