from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.index, name='index'),
    path('post-create/', views.post_create, name='post-create'),
    path('login/', views.auth_login, name='login'),
    path('logout/', views.logoutControl, name='logout'),
    path('post-edit/<slug:slug>', views.edit, name="post-edit"),
    path('profile/<int:id>', views.profile, name="profile"),
    path('post-setting/', views.p_setting, name='post-setting'),
    path('detail-setting/', views.d_setting, name='detail-setting'),
    path('post-detail/<slug:slug>', views.post_detail, name="post-detail"),
    path('remove-confirm/<slug:slug>', views.remove_confirm, name="remove-confirm"),
    path('remove/<slug:slug>', views.remove, name="remove"),
    path('member-list/', views.member_list, name='member-list'),
    path('member-create/', views.signup, name="member-create"),
    
]