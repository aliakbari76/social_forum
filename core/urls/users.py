from django.urls import path
from core.api.v1.users import Register , Login

user_url = [
    path('users/register', Register.as_view(), name = 'register_user'),
    path('users/login', Login.as_view() , name = 'login_user'),
]