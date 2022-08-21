import os
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from ad_mannager.forms import CreateCategorys, LoginForm, PostForm, SignUpForm, UpdateProfileForm, UpdateUserForm
from .models import Category, Post, Status
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model

# Create your views here.

@login_required()
def index(request):
    posts = Post.objects.order_by('-id')
    len_all = 0
    len_public_post = 0
    len_pending_post = 0
    len_draft_post = 0
    len_removed_post = 0
    
    len_all = len(posts)
    
    for post in posts:
        if post.isDelete == True:
            len_removed_post += 1
        
        if post.status.status_name == "公衆":
            len_public_post += 1
        elif post.status.status_name == "保留中":
            len_pending_post += 1
        elif post.status.status_name == "下書き":
            len_draft_post += 1
   
    context = {
        'posts': posts,
        'len_all' : len_all,
        'len_public_post' : len_public_post,
        'len_pending_post' : len_pending_post,
        'len_draft_post' : len_draft_post,
        'len_removed_post' : len_removed_post
    }
    
    return render(request, 'ad_mannager/posts.html', context)

@login_required()
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post:index')
        else:
            return render(request, 'ad_mannager/post-create.html', {'form':form})
    else:
        form = PostForm()
        return render(request, 'ad_mannager/post-create.html', {'form':form})

def auth_login(request):
    lf = LoginForm
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST['next']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect(next_url)
            ...
        else:
            request_form = LoginForm(request.POST)
            # Return an 'invalid login' error message.
            mess="パスワードまたはアカウント名が間違っているので、再試行してください。"
            ...
            return render(request, 'ad_mannager/login.html', {'mess':mess, 'form':request_form, 'next':next_url})

            
    else:
        return render(request, 'ad_mannager/login.html', {'form':lf})

@login_required()
def logoutControl(request):
    logout(request)
    return redirect('post:login')


@login_required()
def edit_post(request, slug):
    post = get_object_or_404(Post, slug = slug)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            if post.isDelete == True and form['status'] != "消去済":
                post.isDelete = False
            form.save()
            return redirect('post:index')
        else:
            return render(request, 'ad_mannager/post-edit.html', {'form':form, 'post' : post})
    else:
        tags = post.tags.all()
        form = PostForm(instance=post)
        return render(request, 'ad_mannager/post-edit.html', {'form':form, 'post': post, 'tags':tags})

@login_required()
def profile(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        profile_form = UpdateProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            path_old_img = (user.profile.avatar.url).lstrip("/")
            
            new_avatar = request.FILES.get('avatar', None)
            user_form.save()
            profile_form.save()
            
            if new_avatar != None and path_old_img != 'media/default.png':
                try:
                    os.remove(path_old_img)
                except Exception as e:
                    print('Exception in removing old profile image: ', e)
                user.profile.avatar = request.FILES.get('avatar', None)
                user.profile.save()
            elif new_avatar != None:
                user.profile.avatar = request.FILES.get('avatar', None)
                user.profile.save()
                
            messages.success(request, 'Your profile is updated successfully')
            return redirect('post:profile', id=user.id)
    else:
      
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=user.profile)

    return render(request, 'ad_mannager/profile.html', {'user_form': user_form, 'profile_form': profile_form, 'uf':user})

@login_required()
def p_setting(request):
    category_all = Category.objects.all()
    if request.method == 'POST':
       create_categoryForm = CreateCategorys(request.POST)
       if create_categoryForm.is_valid():
           create_categoryForm.save()
           return redirect('post:post-setting')
    else:
        create_categoryForm = CreateCategorys()
    return render(request, 'ad_mannager/post-setting.html', {'create_categoryForm':create_categoryForm, 'category_all':category_all})
        
    
@login_required()
def d_setting(request):
    if request.method == 'GET':
        return render(request, 'ad_mannager/detail-setting.html')

@login_required()  
def post_detail(request, slug):
    post = get_object_or_404(Post, slug = slug)
    return render(request, 'ad_mannager/review.html', {'post':post})

@login_required()
def remove_confirm(request, slug): 
    return render(request, 'ad_mannager/remove-confirm.html', {'slug':slug})

@login_required()
def remove(request, slug):
    post = get_object_or_404(Post, slug = slug)
    post.isDelete = True
    stus = get_object_or_404(Status, id=5)
    post.status = stus
    post.save()
    return redirect('post:index')

@login_required()
def member_list(request):
    User = get_user_model()
    member_list = User.objects.all()
    len_members = len(member_list)

    context = {
        'member_list' : member_list,
        'len_members' : len_members,
    }
    return render(request, 'ad_mannager/member-list.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post:member-list')
    else:
        form = SignUpForm()
    return render(request, 'ad_mannager/member-create.html', {'form':form})