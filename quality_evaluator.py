from typing import List, Dict
from models import ContentCalendar, Post, Comment
from collections import Counter

class QualityEvaluator:
    def __init__(self):
        self.issues = []
        self.warnings = []
    
    def evaluate_calendar(self, calendar: ContentCalendar) -> Dict:
        self.issues = []
        self.warnings = []
        
        score = 100
        
        score -= self._check_subreddit_distribution(calendar.posts) * 10
        score -= self._check_persona_distribution(calendar.posts, calendar.comments) * 8
        score -= self._check_comment_quality(calendar.comments) * 5
        score -= self._check_post_quality(calendar.posts) * 7
        score -= self._check_conversation_flow(calendar.posts, calendar.comments) * 10
        score -= self._check_keyword_distribution(calendar.posts) * 5
        score -= self._check_timing_patterns(calendar.posts, calendar.comments) * 5
        score -= self._check_overposting(calendar.posts) * 15
        score -= self._check_awkward_interactions(calendar.posts, calendar.comments) * 10
        score -= self._check_content_variety(calendar.posts) * 5
        
        score = max(0, min(100, score))
        
        quality_level = self._get_quality_level(score)
        
        return {
            "score": score,
            "quality_level": quality_level,
            "issues": self.issues,
            "warnings": self.warnings,
            "details": self._get_evaluation_details(calendar)
        }
    
    def _check_subreddit_distribution(self, posts: List[Post]) -> int:
        subreddit_counts = Counter([p.subreddit for p in posts])
        max_count = max(subreddit_counts.values()) if subreddit_counts else 0
        
        if max_count > 2:
            self.issues.append(f"Overposting: {max_count} posts in same subreddit")
            return 2
        elif max_count == 2 and len(posts) <= 3:
            self.warnings.append("Multiple posts in same subreddit (might be okay for small weeks)")
            return 1
        return 0
    
    def _check_persona_distribution(self, posts: List[Post], comments: List[Comment]) -> int:
        post_authors = Counter([p.author_username for p in posts])
        comment_authors = Counter([c.username for c in comments])
        
        max_post_author = max(post_authors.values()) if post_authors else 0
        max_comment_author = max(comment_authors.values()) if comment_authors else 0
        
        issues = 0
        
        if max_post_author > len(posts) * 0.6:
            self.issues.append(f"One persona posting too much: {max_post_author}/{len(posts)} posts")
            issues += 1
        
        if max_comment_author > len(comments) * 0.4:
            self.issues.append(f"One persona commenting too much: {max_comment_author}/{len(comments)} comments")
            issues += 1
        
        return issues
    
    def _check_comment_quality(self, comments: List[Comment]) -> int:
        if not comments:
            return 0
        
        issues = 0
        duplicate_texts = Counter([c.comment_text.lower().strip() for c in comments])
        
        for text, count in duplicate_texts.items():
            if count > 2:
                self.issues.append(f"Duplicate comment text appears {count} times")
                issues += 1
        
        short_comments = [c for c in comments if len(c.comment_text.strip()) < 5]
        if len(short_comments) > len(comments) * 0.3:
            self.warnings.append("Too many very short comments (might look spammy)")
            issues += 1
        
        return min(issues, 2)
    
    def _check_post_quality(self, posts: List[Post]) -> int:
        issues = 0
        
        for post in posts:
            if len(post.title) < 10:
                self.issues.append(f"Post {post.post_id} has very short title")
                issues += 1
            
            if len(post.body) < 20:
                self.issues.append(f"Post {post.post_id} has very short body")
                issues += 1
            
            if not post.keyword_ids:
                self.warnings.append(f"Post {post.post_id} has no keywords")
        
        return min(issues, 2)
    
    def _check_conversation_flow(self, posts: List[Post], comments: List[Comment]) -> int:
        issues = 0
        
        for post in posts:
            post_comments = [c for c in comments if c.post_id == post.post_id]
            
            if len(post_comments) == 0:
                self.warnings.append(f"Post {post.post_id} has no comments")
                continue
            
            reply_rate = len([c for c in post_comments if c.parent_comment_id]) / len(post_comments)
            
            if reply_rate > 0.7:
                self.warnings.append(f"Post {post.post_id} has too many replies ({reply_rate:.0%})")
            elif reply_rate < 0.2:
                self.warnings.append(f"Post {post.post_id} has too few replies ({reply_rate:.0%})")
            
            comment_usernames = [c.username for c in post_comments]
            if len(set(comment_usernames)) == 1 and len(comment_usernames) > 1:
                self.issues.append(f"Post {post.post_id} has multiple comments from same persona")
                issues += 1
        
        return min(issues, 2)
    
    def _check_keyword_distribution(self, posts: List[Post]) -> int:
        all_keywords = []
        for post in posts:
            all_keywords.extend(post.keyword_ids)
        
        keyword_counts = Counter(all_keywords)
        
        if not keyword_counts:
            return 0
        
        max_keyword = max(keyword_counts.values())
        if max_keyword > len(posts):
            self.issues.append(f"Keyword overuse: one keyword appears {max_keyword} times")
            return 1
        
        return 0
    
    def _check_timing_patterns(self, posts: List[Post], comments: List[Comment]) -> int:
        issues = 0
        
        for post in posts:
            post_comments = [c for c in comments if c.post_id == post.post_id]
            if len(post_comments) < 2:
                continue
            
            timestamps = sorted([c.timestamp for c in post_comments])
            gaps = []
            for i in range(1, len(timestamps)):
                from datetime import datetime
                t1 = datetime.strptime(timestamps[i-1], "%Y-%m-%d %H:%M")
                t2 = datetime.strptime(timestamps[i], "%Y-%m-%d %H:%M")
                gap = (t2 - t1).total_seconds() / 60
                gaps.append(gap)
            
            if len(set([round(g, -1) for g in gaps])) == 1 and len(gaps) > 2:
                self.warnings.append(f"Post {post.post_id} has suspiciously regular comment timing")
                issues += 1
        
        return min(issues, 1)
    
    def _check_overposting(self, posts: List[Post]) -> int:
        from datetime import datetime, timedelta
        
        if len(posts) < 2:
            return 0
        
        timestamps = sorted([datetime.strptime(p.timestamp, "%Y-%m-%d %H:%M") for p in posts])
        
        for i in range(1, len(timestamps)):
            gap = (timestamps[i] - timestamps[i-1]).total_seconds() / 3600
            
            if gap < 2:
                self.issues.append(f"Posts too close together: {gap:.1f} hours apart")
                return 2
        
        return 0
    
    def _check_awkward_interactions(self, posts: List[Post], comments: List[Comment]) -> int:
        issues = 0
        
        for post in posts:
            post_comments = [c for c in comments if c.post_id == post.post_id]
            
            for comment in post_comments:
                if comment.username == post.author_username:
                    self.issues.append(f"Persona {comment.username} commented on their own post {post.post_id}")
                    issues += 1
            
            comment_texts = [c.comment_text.lower() for c in post_comments]
            if len(comment_texts) != len(set(comment_texts)) and len(post_comments) > 2:
                self.warnings.append(f"Post {post.post_id} has duplicate comment text")
        
        return min(issues, 2)
    
    def _check_content_variety(self, posts: List[Post]) -> int:
        if len(posts) < 2:
            return 0
        
        titles = [p.title.lower() for p in posts]
        if len(set(titles)) < len(titles) * 0.7:
            self.issues.append("Too many similar post titles")
            return 1
        
        return 0
    
    def _get_quality_level(self, score: int) -> str:
        if score >= 90:
            return "Excellent (9-10/10)"
        elif score >= 75:
            return "Good (7-8/10)"
        elif score >= 60:
            return "Fair (5-6/10)"
        elif score >= 40:
            return "Poor (3-4/10)"
        else:
            return "Very Poor (1-2/10)"
    
    def _get_evaluation_details(self, calendar: ContentCalendar) -> Dict:
        return {
            "total_posts": len(calendar.posts),
            "total_comments": len(calendar.comments),
            "subreddits_used": len(set([p.subreddit for p in calendar.posts])),
            "personas_used": len(set([p.author_username for p in calendar.posts] + [c.username for c in calendar.comments])),
            "avg_comments_per_post": len(calendar.comments) / len(calendar.posts) if calendar.posts else 0
        }


