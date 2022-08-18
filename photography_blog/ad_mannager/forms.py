from cProfile import label
from dataclasses import field, fields
from django import forms
from .models import Category, Post, Profile, Status
from django_summernote.widgets import SummernoteWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('user','title', 'category', 'content', 'thumbnail', 'status', 'tags')
        widgets = {
            'content' : SummernoteWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'summernote'}),
            'category': forms.Select(attrs={'class': 'form-control selectric'}),
            'user': forms.Select(attrs={'class': 'form-control selectric'}),
            'status': forms.Select(attrs={'class': 'form-control selectric'}),
            'thumbnail': forms.FileInput(attrs={'id': 'image-upload'}),  
            'tags': forms.TextInput(attrs={'class': 'form-control inputtags'}),
        }
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = True
        
        self.fields['user'].label = '記者'
        self.fields['title'].label = 'タイトル'  
        self.fields['category'].label = 'カテゴリー'
        self.fields['content'].label = 'コンテンツ'
        self.fields['status'].label = '状態'
        

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
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields['email'].required = True

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'task', 'avatar', 'address', 'birthday']

    
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.required = False
        self.fields['bio'].widget.attrs["class"] = "summernote"
            

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='任意。', label='名')
    last_name = forms.CharField(max_length=30, required=False, help_text='任意。', label='苗字')
    email = forms.EmailField(max_length=254, help_text='必要。有効な電子メール アドレスを通知します。', label='メール')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
       
class CreateCategorys(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']
    def __init__(self, *args, **kwargs):
        super(CreateCategorys, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields['category_name'].required = True

class CreateStatus(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status_name']
    def __init__(self, *args, **kwargs):
        super(CreateStatus, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields['status_name'].required = True