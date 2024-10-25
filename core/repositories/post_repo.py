from core.schemas.post_schema import PostSchema
from core.models import Post
from redis import Redis
from .base_repo import BaseRepo
from core.schemas.user_schema import UserSchema
from django.db.transaction import atomic
import json
from injector import inject
from django.contrib.auth import authenticate
from core.injector.injector import BaseInjector
from .user_repo import UserRepo

class PostRepo(BaseRepo):
    user_repo = BaseInjector.get(UserRepo)
    @inject
    def __init__(self, redis: Redis):
        super().__init__(redis)

    @atomic
    def create_post(self,data:PostSchema):
        user = self.user_repo.get_usr_by_id(data.author_user)
        if not user:
            return None

        post_data = data.dict()
        post_data['author_user'] = user

        post = Post.objects.create(**post_data)

        return post if post else None
    
    @atomic
    def fetch_all_posts(self):
        posts = Post.objects.all()
        return posts if posts else None
    
    @atomic
    def fetch_post_by_id(self,post_id):
        post = Post.objects.filter(id=post_id).first()
        return post if post else None
    
    @atomic
    def fetch_post_by_user_id(self,user_id):
        posts = Post.objects.filter(author_user_id = user_id)
        return posts if posts else None
    

    @atomic
    def update_post_score(self, post_id , score , score_count):
        post = Post.objects.filter(id=post_id).first()
        if post and post.score_count + score_count > 0:
            if score_count > 1000 : # 1000 is a big number for 2 hour of rating to post, more than this number could be abnormal or rating spam
                return
            if (score > post.score + 1 or score < post.score - 1) and post.score_count > 0: # if the score is more than 1 point away from the current score, it could be abnormal or rating spam 
                return
            new_average = (post.score * post.score_count + score * score_count) \
            / (post.score_count + score_count)

            Post.objects.filter(id=post_id).update(
                score = new_average , score_count = score_count + post.score_count)
