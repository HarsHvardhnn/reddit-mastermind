from typing import Dict, List
from models import ContentCalendar, Post, Comment
import csv
import os
from config import Config

class OutputFormatter:
    @staticmethod
    def calendar_to_dict(calendar: ContentCalendar) -> Dict:
        return {
            "week_start": calendar.week_start,
            "week_end": calendar.week_end,
            "posts": [
                {
                    "post_id": p.post_id,
                    "subreddit": p.subreddit,
                    "title": p.title,
                    "body": p.body,
                    "author_username": p.author_username,
                    "timestamp": p.timestamp,
                    "keyword_ids": p.keyword_ids
                }
                for p in calendar.posts
            ],
            "comments": [
                {
                    "comment_id": c.comment_id,
                    "post_id": c.post_id,
                    "parent_comment_id": c.parent_comment_id,
                    "comment_text": c.comment_text,
                    "username": c.username,
                    "timestamp": c.timestamp
                }
                for c in calendar.comments
            ]
        }
    
    @staticmethod
    def calendar_to_csv(calendar: ContentCalendar, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        
        posts_path = os.path.join(output_dir, "posts.csv")
        comments_path = os.path.join(output_dir, "comments.csv")
        
        with open(posts_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["post_id", "subreddit", "title", "body", "author_username", "timestamp", "keyword_ids"])
            for post in calendar.posts:
                writer.writerow([
                    post.post_id,
                    post.subreddit,
                    post.title,
                    post.body,
                    post.author_username,
                    post.timestamp,
                    ", ".join(post.keyword_ids)
                ])
        
        with open(comments_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["comment_id", "post_id", "parent_comment_id", "comment_text", "username", "timestamp"])
            for comment in calendar.comments:
                writer.writerow([
                    comment.comment_id,
                    comment.post_id,
                    comment.parent_comment_id or "",
                    comment.comment_text,
                    comment.username,
                    comment.timestamp
                ])
        
        return posts_path, comments_path


