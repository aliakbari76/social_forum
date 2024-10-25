from core.models import Users
from redis import Redis
from .base_repo import BaseRepo
from core.schemas.user_schema import UserSchema
from django.db.transaction import atomic
import json
from injector import inject
from django.contrib.auth import authenticate

class UserRepo(BaseRepo):
    @inject
    def __init__(self, redis: Redis):
        super().__init__(redis)

    @atomic
    def create_user(self,data:UserSchema):
        # Extract password
        password = data.pop('password')
        # Create user instance 
        user = Users(
            username=data['username'],
            first_name=data.get('firstname', ''),
            last_name=data.get('lastname', '')
        )
        user.set_password(password)
        user.save()
        
        # Set profile in redis
        redis_key = f"user:{user.id}:profile"
        self.redis.set(
            redis_key,
            json.dumps({
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            })
        )
        return user
    
    @atomic
    def get_usr_by_id(self,user_id):
        user = Users.objects.filter(id = user_id).first()
        return user if user else None