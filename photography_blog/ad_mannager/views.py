from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from ad_mannager.forms import LoginForm, PostForm, SignUpForm, UpdateProfileForm, UpdateUserForm
from .models import Post, Status
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
            # Return an 'invalid login' error message.
            mess="パスワードまたはアカウント名が間違っているので、再試行してください。"
            ...
            return render(request, 'ad_mannager/login.html', {'mess':mess, 'form':lf, 'next':next_url})

            
    else:
        form = lf
        return render(request, 'ad_mannager/login.html', {'form':form})

@login_required()
def logoutControl(request):
    logout(request)
    return redirect('post:login')


@login_required()
def edit(request, slug):
    post = get_object_or_404(Post, slug = slug)
    if request.method == "GET":
        form = PostForm(instance=post)
        tags = post.tags.names()
        return render(request, 'ad_mannager/post-edit.html', {'post':post, 'form':form, 'tags':tags})
    else:
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post:index')

@login_required()
def profile(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        profile_form = UpdateProfileForm(request.POST, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('post:index')
    else:
      
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=user.profile)

    return render(request, 'ad_mannager/profile.html', {'user_form': user_form, 'profile_form': profile_form, 'uf':user.profile})

@login_required()
def p_setting(request):
    if request.method == 'GET':
        return render(request, 'ad_mannager/page-setting.html')
    
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