from .users import user_url
from django.urls import path , include
from .post import post_url
from .rate import rate_url

urlpatterns = [
    path('', include(user_url)),
    path('', include(post_url)),
    path('', include(rate_url)),
]