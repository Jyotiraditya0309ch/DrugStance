from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    UserProfileView,
    FlaggedPostsView,
)
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('posts/', PostListView.as_view(), name='post-list'),  # List all posts
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # Retrieve a specific post
    path('flagged/', FlaggedPostsView.as_view(), name='flagged-posts'),  # List flagged posts
    path('scan-all/', views.scan_all_content, name='scan-all'), 
    path('user-profile/<int:userId>/', views.get_user_info, name='user_profile'), 
    path('profile-analysis/', views.get_user_profile, name='get_user_profile'),
    path('analytics/', views.get_all_users, name='analytics'),
    path('get-comments/',views.get_comments,name='get-comments')
]

