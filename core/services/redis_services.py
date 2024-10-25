# services/redis_service.py
from injector import inject
import redis
from django.conf import settings

class RedisService:
    @inject
    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host="127.0.0.1", #TODO change this FROM HARDCODED VALUE TO ENV VAR
                port="6379", #TODO change this FROM HARDCODED VALUE TO ENV VAR
                db=1,
                decode_responses=True
            )
            self.redis_client.ping()
        except Exception as e:
            return False
    def save_vote(self, post_id: int, user_id: int, rate: int):
        """
        Save vote in format: {post_id}:{user_id}:{rate}:{is_processed}
        """
        try:
            key = f"vote:{post_id}:{user_id}"
            value = f"{post_id}:{user_id}:{rate}:0"
            self.redis_client.set(key, value)
            return True
        except Exception as e:
            # capture exception with a tool like sentry
            return False
    def get_unprocessed_votes(self):
        """Get all unprocessed votes"""
        # Get all vote keys
        vote_keys = self.redis_client.keys("vote:*")
        unprocessed_votes = []
        
        for key in vote_keys:
            vote_data = self.redis_client.get(key)
            if vote_data and vote_data.endswith(":0"):  # unprocessed
                post_id, user_id, rate, _ = vote_data.split(":")
                unprocessed_votes.append({
                    'post_id': int(post_id),
                    'user_id': int(user_id),
                    'rate': int(rate)
                })
        
        return unprocessed_votes
    
    def mark_votes_as_processed(self, post_id: int):
        """Mark all votes for a post as processed"""
        vote_keys = self.redis_client.keys(f"vote:{post_id}:*")
        
        for key in vote_keys:
            vote_data = self.redis_client.get(key)
            if vote_data:
                post_id, user_id, rate, _ = vote_data.split(":")
                new_value = f"{post_id}:{user_id}:{rate}:1"  # 1 means processed
                self.redis_client.set(key, new_value)
    
    def get_post_votes(self, post_id: int):
        """Get all votes for a specific post"""
        vote_keys = self.redis_client.keys(f"vote:{post_id}:*")
        votes = []
        
        for key in vote_keys:
            vote_data = self.redis_client.get(key)
            if vote_data:
                post_id, user_id, rate, is_processed = vote_data.split(":")
                votes.append({
                    'post_id': int(post_id),
                    'user_id': int(user_id),
                    'rate': int(rate),
                    'is_processed': bool(int(is_processed))
                })
        
        return votes