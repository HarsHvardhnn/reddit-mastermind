# Testing and Quality

This is about how we test the algorithm and evaluate whether the calendars look natural or fake.

## Quality Evaluator

The quality_evaluator.py file scores calendars from 0-100. It checks subreddit distribution (catches overposting in same subreddit, flags when more than 2 posts in same subreddit), persona distribution (makes sure one persona doesn't dominate, checks post and comment distribution), comment quality (finds duplicate comment text, flags too many short comments), post quality (checks title and body length, makes sure keywords are present), conversation flow (looks at reply rates which should be 20-60%, catches multiple comments from same persona on one post), keyword distribution (prevents keyword overuse), timing patterns (detects suspiciously regular comment timing), overposting (flags posts too close together, less than 2 hours), awkward interactions (catches persona commenting on own post, finds duplicate comments), content variety (makes sure post titles aren't too similar).

Quality levels: 90-100 is excellent (9-10/10), 75-89 is good (7-8/10), 60-74 is fair (5-6/10), 40-59 is poor (3-4/10), 0-39 is very poor (1-2/10).

## Natural Conversation Analyzer

The natural_conversation_analyzer.py looks at how natural conversations feel. Conversation quality (0-100) checks unique personas per post, reply rate should be 20-60%, comment length 20-200 chars is good. Comment diversity (0-100) does text similarity detection, duplicate phrase finding, unique comment starts. Persona voice consistency checks if personas have consistent writing styles, validates comment length variance. Realism score (0-100) is overall naturalness, flags obvious patterns. Red flags include persona commenting on own post, duplicate comments, all comments mention company which is too obvious.

## Test Framework

The test_framework.py runs a bunch of tests. Test 1 is basic generation - tests with sample Slideforge data, makes sure the standard workflow works. Test 2 is edge cases - too many posts (10 in one week), too few personas (only 2), single subreddit (all posts in one place), many keywords (50 keywords). Test 3 is different inputs - small company (2 personas, 2 subreddits), large company (10 personas, 30 subreddits). Test 4 is quality scenarios - high quality should score 8-10/10, low quality should score 2-4/10.

Running tests: python run_tests.py

## Current Results

Average Score: 74.6/100.

Best: basic generation 100/100, high quality scenario 100/100, large company 100/100, many keywords 100/100.

Worst: small company 35/100 (very poor), too few personas 42/100 (poor), too many posts 60/100 (fair), single subreddit 60/100 (fair).

## Problems We Found

Critical red flags: all comments mention company (every comment mentions Slideforge, super obvious it's fake, fix is to add comments that don't mention company), duplicate comment text (same comment appears multiple times, very obvious pattern, fix is to track used comments and ensure uniqueness), too few personas (with only 2 personas same person comments multiple times, looks fake, fix is to require minimum 3 personas).

Major issues: unnatural reply rates (many posts have 0% replies, all top-level, doesn't look like real conversation, fix is to ensure 20-60% reply rate), overposting in same subreddit (algorithm allows 3+ posts in same subreddit, looks like spam, fix is to enforce max 2 per subreddit per week), posts too close together (posts can be less than 2 hours apart, suspicious timing, fix is to enforce minimum gap).

Minor issues: comment length (some too short, some too long), similar post titles (need more variety).

## Naturalness: 6/10

What makes it look fake: limited comment templates (only 8), all personas sound identical, predictable patterns, generic replies, all comments mention company.

What's working: good distribution logic, edge case detection, quality scoring is accurate, timing has jitter which is more natural.

## What We Should Do

High priority: expand comment templates (target 30+), add comments that don't mention company, more variety in phrasing, context-aware comments. Fix duplicate comments by tracking used comments per post and ensuring uniqueness. Improve reply comments with context-aware replies that reference parent comment content. Enforce reply rate to ensure 20-60% of comments are replies.

Medium priority: persona voice differentiation using backstories to generate persona-specific content (riley_ops more formal and structured, emily_econ more casual and student-like, jordan_consults narrative-focused). Content uniqueness to detect overlapping topics and prevent similar posts. Reddit compliance to flag overly promotional content and ensure self-promotion rules followed.

Future: LLM integration to generate unique natural comments using persona backstories for authentic voice. Performance tracking to track which posts/comments perform well and learn from real engagement data.

## How to Use

Evaluate a calendar: from quality_evaluator import QualityEvaluator, evaluator = QualityEvaluator(), calendar = generate calendar, evaluation = evaluator.evaluate_calendar(calendar), print score and quality level.

Analyze naturalness: from natural_conversation_analyzer import NaturalConversationAnalyzer, analyzer = NaturalConversationAnalyzer(), analysis = analyzer.analyze_naturalness(calendar.posts, calendar.comments), print conversation quality and red flags.

Run tests: python run_tests.py

## Goals

Current: 6.5/10. Target: 9/10.

To reach 9/10: quality evaluation system done, testing framework done, naturalness analysis done, 30+ comment templates in progress, persona voice differentiation planned, context-aware replies planned, content uniqueness validation planned, Reddit compliance checking planned.
