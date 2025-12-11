# Algorithm Notes

So I built this thing that generates Reddit content calendars. Here's how it works, more or less.

The basic idea is you give it company info, some personas (fake Reddit accounts), keywords, and it figures out when to post, where to post, what to say, and who should comment.

## Loading Data

First it reads the input file. Company name, description, subreddits they care about. Then the personas - each one has a username and a backstory. Then keywords - what we're trying to rank for. Plus config stuff like how many posts per week.

Nothing fancy here, just loading JSON.

## Generating Posts

This is the interesting part. For each post it needs to decide:

When to post - spreads them across the week. If you have 3 posts they'll be on different days. If you have 10 it tries to space them out but with randomness so it doesn't look too perfect.

Where to post - keeps track of which subreddits it's used and tries not to repeat them right away. If it runs out it resets. The goal is variety, don't spam the same subreddit.

Who posts it - rotates through personas so one person doesn't post everything. Makes sure each persona gets used before cycling back. Also prevents the post author from commenting on their own post, though actually on Reddit sometimes OPs do reply so maybe we should change this.

What keywords - picks 1-3 keywords per post randomly. Tracks which ones have been used. The matching to subreddits is pretty basic, just looks at subreddit name and keyword text. Could be smarter.

What to say - there are three types of posts. Comparison posts like "Slideforge vs Canva for slides?" when it's a competitive subreddit. Best tool posts like "Best AI Presentation Maker?" when the keyword has "best" in it. Question posts as a default fallback. The templates are pretty basic, real Reddit posts have way more nuance but this covers the common patterns.

## Generating Comments

Comments are trickier. They need to feel like real conversation.

How many - 2-4 comments per post, randomly. Feels like enough engagement without being obvious.

Who comments - excludes the post author, rotates through other personas. Tries to get variety.

Threading - about 40% of comments are replies to other comments, 60% are top-level. Creates conversation flow. Replies only attach to top-level comments, not other replies. Keeps it simple.

Timing - comments show up 15-60 minutes after the post, with jitter so they don't land at perfect intervals. The jitter is -10 to +25 minutes on top of the base timing. Makes it feel more natural.

Comment content - this is where it's weakest. Top-level comments mention the company organically and compare to other tools. Reply comments are super generic, just "+1" or "Same here!" type stuff. Need to make these way better.

## Design Choices

I made a bunch of decisions that might not be perfect.

Natural engagement - comments don't all appear at once, there's a mix of top-level and threaded, different personas engage. But honestly the content itself is still too formulaic.

Keyword distribution - keywords get matched to subreddits (basic matching), multiple keywords per post for SEO, tracks usage. But all keywords are treated equally, no weighting system.

Persona rotation - prevents one persona from dominating, ensures variety. But all personas sound the same because they use the same comment templates. The backstories aren't being used at all.

Subreddit variety - avoids posting to same subreddit consecutively, distributes across all available. But maybe some subreddits are more valuable and should get more posts? Don't know.

## Output Format

Posts have an ID (P1, P2, etc), subreddit, title and body, author persona, timestamp, and keyword IDs.

Comments have an ID (C1, C2, etc), post ID (which post it's on), parent comment ID if it's a reply, comment text, username (persona), and timestamp.

## What Could Be Better

The algorithm works but there's room for improvement. Comment templates are too limited (only 8 variations). Personas all sound identical. Reply comments are too generic. No persona voice differentiation. Keyword matching is basic. Content could be more sophisticated.

But for now it generates reasonable calendars. The quality evaluator catches most of the obvious issues.
