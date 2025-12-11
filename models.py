from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Company:
    name: str
    website: str
    description: str
    icp: dict
    subreddits: List[str]

@dataclass
class Persona:
    username: str
    info: str

@dataclass
class Keyword:
    keyword_id: str
    keyword: str

@dataclass
class Post:
    post_id: str
    subreddit: str
    title: str
    body: str
    author_username: str
    timestamp: str
    keyword_ids: List[str] = field(default_factory=list)

@dataclass
class Comment:
    comment_id: str
    post_id: str
    parent_comment_id: Optional[str]
    comment_text: str
    username: str
    timestamp: str

@dataclass
class ContentCalendar:
    week_start: str
    week_end: str
    posts: List[Post] = field(default_factory=list)
    comments: List[Comment] = field(default_factory=list)


