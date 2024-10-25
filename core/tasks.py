# tasks.py
from celery import shared_task
from django.db.models import Avg
from collections import defaultdict

from core.repositories.post_repo import PostRepo
from .models import Post
from .services.redis_services import RedisService
from .injector.injector import BaseInjector
@shared_task
def process_post_votes(post_id: int):
    #Process votes for a specific post
    redis_service = BaseInjector.get(RedisService)
    post_repo = BaseInjector.get(PostRepo)

    votes = redis_service.get_post_votes(post_id)
    
    if votes:
        # Calculate new average
        vote_counter = 0
        sum_of_vote = 0
        for vote in votes:
            if not vote['is_processed']:
               sum_of_vote += vote['rate']
               vote_counter += 1
               vote['is_processed'] = True

        # Update vote_count in database
        # Calculate new average
        new_average = sum_of_vote / vote_counter
        
        # Update post in database
        post_repo.update_post_score(post_id, new_average, vote_counter)
        
        # Mark votes as processed
        redis_service.mark_votes_as_processed(post_id)

@shared_task
def process_all_unprocessed_votes():
    #Process all unprocessed votes
    redis_service = RedisService()
    unprocessed_votes = redis_service.get_unprocessed_votes()
    # Group votes by post_id
    post_votes = defaultdict(list)
    for vote in unprocessed_votes:
        post_votes[vote['post_id']].append(vote)
    # Process votes for each post
    for post_id in post_votes:
        process_post_votes.delay(post_id)