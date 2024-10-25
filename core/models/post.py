from django.db import models
from .users import Users

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    score = models.FloatField(default=0)
    score_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author_user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_vote = None
    
    @property
    def user_vote(self):
        return self._user_vote
    
    @user_vote.setter
    def user_vote(self, value):
        self._user_vote = value