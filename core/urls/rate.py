from django.urls import path
from core.api.v1.rate import RatePostView

rate_url = [
    path('rate/create' , RatePostView.as_view()),
]