import os
from datetime import datetime, timedelta

class Config:
    DATA_DIR = "data"
    INPUT_DIR = os.path.join(DATA_DIR, "input")
    OUTPUT_DIR = os.path.join(DATA_DIR, "output")
    
    POSTS_PER_WEEK = 3
    COMMENTS_PER_POST_MIN = 2
    COMMENTS_PER_POST_MAX = 4
    COMMENT_THREAD_DEPTH_MAX = 2
    
    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M"
    
    WEEK_START_DAY = 0


