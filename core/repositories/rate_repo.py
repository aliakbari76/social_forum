from typing import Optional
from core.schemas.rate_schema import RateSchema
from core.models import Rating
from redis import Redis
from .base_repo import BaseRepo
from core.schemas.user_schema import UserSchema
from django.db.transaction import atomic
import json
from injector import inject
from django.contrib.auth import authenticate
from core.injector.injector import BaseInjector
from .user_repo import UserRepo
from .post_repo import PostRepo
from core.services.redis_services import RedisService
class RateRepo(BaseRepo):
    user_repo = BaseInjector.get(UserRepo)
    post_repo = BaseInjector.get(PostRepo)
    redis_service = BaseInjector.get(RedisService)
    @inject
    def __init__(self, redis: Redis):
        super().__init__(redis)

    @atomic
    def create_or_update_rate(self,data:RateSchema):

        # for small amount of users
        # user = self.user_repo.get_usr_by_id(data.author_user)
        # if not user:
        #     return None

        # post = self.post_repo.get_post_by_id(data.post_id)
        # if not post:
        #     return None

        # rating = Rating.objects.update_or_create(user=user,post=post,defaults={'rate':data.rate})
        # return rating if rating else None

        # using redis for large amount of users
        rating = self.redis_service.save_vote(post_id=data.post_id,user_id= data.user_id,rate= data.rate)
        return rating
        