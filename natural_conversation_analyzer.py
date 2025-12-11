from typing import List, Dict
from models import Post, Comment
from collections import Counter
import re

class NaturalConversationAnalyzer:
    def analyze_naturalness(self, posts: List[Post], comments: List[Comment]) -> Dict:
        return {
            "conversation_quality": self._analyze_conversations(posts, comments),
            "comment_diversity": self._analyze_comment_diversity(comments),
            "persona_voice_consistency": self._analyze_persona_voices(comments),
            "realism_score": self._calculate_realism_score(posts, comments),
            "red_flags": self._find_red_flags(posts, comments)
        }
    
    def _analyze_conversations(self, posts: List[Post], comments: List[Comment]) -> Dict:
        scores = []
        issues = []
        
        for post in posts:
            post_comments = [c for c in comments if c.post_id == post.post_id]
            
            if not post_comments:
                issues.append(f"Post {post.post_id} has no engagement")
                scores.append(0)
                continue
            
            score = 50
            
            unique_personas = len(set([c.username for c in post_comments]))
            if unique_personas == len(post_comments):
                score += 20
            
            reply_rate = len([c for c in post_comments if c.parent_comment_id]) / len(post_comments)
            if 0.2 <= reply_rate <= 0.6:
                score += 15
            elif reply_rate < 0.1 or reply_rate > 0.8:
                issues.append(f"Post {post.post_id} has unnatural reply rate: {reply_rate:.0%}")
            
            comment_lengths = [len(c.comment_text) for c in post_comments]
            avg_length = sum(comment_lengths) / len(comment_lengths) if comment_lengths else 0
            if 20 <= avg_length <= 200:
                score += 15
            else:
                issues.append(f"Post {post.post_id} comments too short/long (avg: {avg_length:.0f} chars)")
            
            scores.append(min(100, score))
        
        return {
            "average_score": sum(scores) / len(scores) if scores else 0,
            "issues": issues
        }
    
    def _analyze_comment_diversity(self, comments: List[Comment]) -> Dict:
        if not comments:
            return {"score": 0, "issues": ["No comments to analyze"]}
        
        text_similarity = self._check_text_similarity(comments)
        duplicate_phrases = self._find_duplicate_phrases(comments)
        
        issues = []
        score = 100
        
        if text_similarity > 0.3:
            issues.append(f"High text similarity: {text_similarity:.0%}")
            score -= 30
        
        if duplicate_phrases:
            issues.append(f"Duplicate phrases found: {len(duplicate_phrases)}")
            score -= 20
        
        unique_starts = len(set([c.comment_text[:20].lower() for c in comments]))
        if unique_starts < len(comments) * 0.7:
            issues.append("Too many comments start similarly")
            score -= 15
        
        return {
            "score": max(0, score),
            "issues": issues,
            "text_similarity": text_similarity,
            "duplicate_phrases": len(duplicate_phrases)
        }
    
    def _analyze_persona_voices(self, comments: List[Comment]) -> Dict:
        persona_comments = {}
        for comment in comments:
            if comment.username not in persona_comments:
                persona_comments[comment.username] = []
            persona_comments[comment.username].append(comment.comment_text)
        
        issues = []
        score = 100
        
        for persona, texts in persona_comments.items():
            if len(texts) < 2:
                continue
            
            avg_length = sum(len(t) for t in texts) / len(texts)
            length_variance = sum((len(t) - avg_length) ** 2 for t in texts) / len(texts)
            
            if length_variance < 100:
                issues.append(f"Persona {persona} comments too similar in length")
                score -= 10
        
        return {
            "score": max(0, score),
            "issues": issues
        }
    
    def _calculate_realism_score(self, posts: List[Post], comments: List[Comment]) -> int:
        score = 100
        
        for post in posts:
            post_comments = [c for c in comments if c.post_id == post.post_id]
            
            if len(post_comments) == 0:
                score -= 5
                continue
            
            if len(post_comments) == len(set([c.username for c in post_comments])):
                score -= 3
            
            comment_texts = [c.comment_text.lower() for c in post_comments]
            if len(comment_texts) != len(set(comment_texts)):
                score -= 10
        
        return max(0, score)
    
    def _find_red_flags(self, posts: List[Post], comments: List[Comment]) -> List[str]:
        red_flags = []
        
        for post in posts:
            post_comments = [c for c in comments if c.post_id == post.post_id]
            
            for comment in post_comments:
                if comment.username == post.author_username:
                    red_flags.append(f"Persona {comment.username} commented on own post")
            
            comment_texts = [c.comment_text for c in post_comments]
            if len(comment_texts) != len(set(comment_texts)) and len(post_comments) > 2:
                red_flags.append(f"Post {post.post_id} has duplicate comments")
            
            if all("slideforge" in c.comment_text.lower() for c in post_comments):
                red_flags.append(f"Post {post.post_id} comments all mention company (too obvious)")
        
        return red_flags
    
    def _check_text_similarity(self, comments: List[Comment]) -> float:
        if len(comments) < 2:
            return 0.0
        
        texts = [c.comment_text.lower() for c in comments]
        similarities = []
        
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                similarity = self._text_similarity(texts[i], texts[j])
                similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _find_duplicate_phrases(self, comments: List[Comment], min_length: int = 10) -> List[str]:
        phrases = []
        for comment in comments:
            text = comment.comment_text.lower()
            for i in range(len(text) - min_length):
                phrase = text[i:i+min_length]
                phrases.append(phrase)
        
        phrase_counts = Counter(phrases)
        duplicates = [phrase for phrase, count in phrase_counts.items() if count > 2]
        
        return duplicates

