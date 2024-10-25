
from functools import wraps
from django.core.cache import cache
from core.utils.messages import APIResponse
import json
def cache_post_view(timeout=3600):  # Default timeout of 3600 seconds equal to 1 hour
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(view_instance, request, *args, **kwargs):

            user_id = request.user.id
            cache_key = f'post_list_user_{user_id}'
            
            # Try to get data from cache
            cached_data = cache.get(cache_key)
            
            if cached_data is not None:
                return APIResponse(status=200, data=cached_data)
            
            # If no cached data, call the original view
            response = view_func(view_instance, request, *args, **kwargs)
            
            # Only cache successful responses
            if response.status_code == 200:
                data = json.loads(response.content)['data']
                cache.set(cache_key, data, timeout=timeout)
            
            return response
        return wrapped_view
    return decorator


def invalidate_posts_cache(): # whenever a new post created or updated or deleted delete the cache
    cache.delete('post_list_all')