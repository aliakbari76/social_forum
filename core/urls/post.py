from django.urls import path
from core.api.v1.posts import PostView , PostViewByUser , PostCreateView , PostDetailedView

post_url = [
    path('posts/all' , PostView.as_view()),
    path('posts/user/<int:user_id>' , PostViewByUser.as_view()),
    path('posts/create' , PostCreateView.as_view()),
    path('posts/<int:post_id>' , PostDetailedView.as_view()),
]