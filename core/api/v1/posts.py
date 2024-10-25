from rest_framework import  generics
from rest_framework.views import APIView
from core.repositories import PostRepo 
from core.utils.messages import APIResponse
from core.utils.validate import validate_serializer
from rest_framework.schemas import AutoSchema
from core.injector.injector import BaseInjector
from core.serializers import PostResponseSerializer , CreatePostSerializer , PostListSerializer 
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.schemas.post_schema import PostSchema
from core.services.cache import cache_post_view , invalidate_posts_cache
from core.services.redis_services import RedisService

class CommonPostView(AutoSchema , APIView):
    post_repo = BaseInjector.get(PostRepo)
    redis_service = BaseInjector.get(RedisService)

class PostView(CommonPostView , generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    def get_user_votes(self, posts, user_id):
        user_votes = {}
        try:
            vote_keys = [f"vote:{post.id}:{user_id}" for post in posts]

            pipe = self.redis_service.redis_client.pipeline()
            for key in vote_keys:
                pipe.get(key)

            vote_values = pipe.execute()
            # Process the votes
            for post_id, vote_value in zip([post.id for post in posts], vote_values):
                if vote_value:
                    # Parse the vote value: "{post_id}:{user_id}:{rate}:0"
                    _, _, rate, _ = vote_value.split(':')
                    user_votes[post_id] = int(rate)
                else:
                    user_votes[post_id] = None
                    
            return user_votes
        except Exception as e:
            # Log the error but don't fail the whole request
            # capture exception with a tool like sentry
            return {}
        

    @cache_post_view(timeout=3600)
    def get(self , request):
        try:
            posts = self.post_repo.fetch_all_posts()
            if posts:
                user_votes = {}
                
                user_votes = self.get_user_votes(posts, request.user.id)
                # Add user_vote to each post before serialization
                for post in posts:
                    post.user_vote = user_votes.get(post.id)

                post_list = PostListSerializer(posts, many=True).data
                return APIResponse(status = 200 , data=post_list)
            
            return APIResponse(status=404 , error_code= 1013)
        
        except Exception as e:
            #capture exception with a tool like sentry
            return APIResponse(status=400 , error_code= 1011 , data = str(e))    

class PostViewByUser(CommonPostView , generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    
    def get(self , request, *args, **kwargs):
        try:
            posts = self.post_repo.fetch_post_by_user_id(self.kwargs['user_id'])
            if posts:
                post_list = PostListSerializer(posts, many=True).data
                return APIResponse(status = 200 , data=post_list)
            
            return APIResponse(status=404 , error_code= 1013)
        
        except Exception as e:
            #capture exception with a tool like sentry
            return APIResponse(status=400 , error_code= 1011 , data = str(e))

class PostDetailedView(CommonPostView , generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    def get(self , request , *args, **kwargs):
        try:
            post = self.post_repo.fetch_post_by_id(self.kwargs['post_id'])
            if post:
                post_list = PostResponseSerializer(post).data
                return APIResponse(status = 200 , data=post_list)
            
            return APIResponse(status=404 , error_code= 1013)
        
        except Exception as e:
            #capture exception with a tool like sentry
            return APIResponse(status=400 , error_code= 1011 , data = str(e))
        
class PostCreateView(CommonPostView , generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = CreatePostSerializer

    @validate_serializer()
    def post(self , request):
        try:
            # invalidate posts cache
            invalidate_posts_cache()
            post = self.post_repo.create_post(data=PostSchema(title=request.data.get('title') , content=request.data.get('content') , author_user=int(request.user.id)))
            if post:
                serilized_post = PostResponseSerializer(post).data
                return APIResponse(status = 201 , data=serilized_post)
            
            return APIResponse(status=404 , error_code= 1013)
        
        except Exception as e:
            #capture exception with a tool like sentry
            return APIResponse(status=400 , error_code= 1011 , data = str(e))