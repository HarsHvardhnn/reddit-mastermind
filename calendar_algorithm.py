import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from models import Company, Persona, Keyword, Post, Comment, ContentCalendar
from config import Config

class ContentCalendarGenerator:
    def __init__(self, company: Company, personas: List[Persona], keywords: List[Keyword]):
        self.company = company
        self.personas = personas
        self.keywords = keywords
        self.keyword_map = {kw.keyword_id: kw.keyword for kw in keywords}
        
    def generate_week_calendar(self, week_start: datetime, posts_per_week: int) -> ContentCalendar:
        posts = self._generate_posts(week_start, posts_per_week)
        comments = self._generate_comments(posts, week_start)
        
        week_end = week_start + timedelta(days=6)
        return ContentCalendar(
            week_start=week_start.strftime(Config.TIMESTAMP_FORMAT),
            week_end=week_end.strftime(Config.TIMESTAMP_FORMAT),
            posts=posts,
            comments=comments
        )
    
    def _generate_posts(self, week_start: datetime, num_posts: int) -> List[Post]:
        posts = []
        subreddits_pool = self.company.subreddits.copy()
        keywords_pool = self.keywords.copy()
        personas_pool = self.personas.copy()
        
        used_subreddits = set()
        used_keywords = set()
        used_personas = set()
        
        days = self._distribute_posts_across_week(num_posts)
        
        for i, day_offset in enumerate(days):
            post_date = week_start + timedelta(days=day_offset)
            hour = random.randint(9, 17)
            minute = random.randint(0, 59)
            timestamp = post_date.replace(hour=hour, minute=minute)
            
            subreddit = self._select_subreddit(subreddits_pool, used_subreddits)
            persona = self._select_persona(personas_pool, used_personas, i)
            selected_keywords = self._select_keywords(keywords_pool, used_keywords, subreddit)
            
            post_content = self._generate_post_content(subreddit, selected_keywords)
            
            post = Post(
                post_id=f"P{i+1}",
                subreddit=subreddit,
                title=post_content["title"],
                body=post_content["body"],
                author_username=persona.username,
                timestamp=timestamp.strftime(Config.TIMESTAMP_FORMAT),
                keyword_ids=[kw.keyword_id for kw in selected_keywords]
            )
            posts.append(post)
        
        return posts
    
    def _distribute_posts_across_week(self, num_posts: int) -> List[int]:
        if num_posts <= 7:
            days = sorted(random.sample(range(7), num_posts))
        else:
            base = num_posts // 7
            extra = num_posts % 7
            days = []
            for day in range(7):
                count = base + (1 if day < extra else 0)
                days.extend([day] * count)
            random.shuffle(days)
        return days
    
    def _select_subreddit(self, pool: List[str], used: set) -> str:
        available = [s for s in pool if s not in used]
        if not available:
            available = pool
            used.clear()
        
        subreddit = random.choice(available)
        used.add(subreddit)
        return subreddit
    
    def _select_persona(self, pool: List[Persona], used: set, index: int) -> Persona:
        if len(used) < len(pool):
            available = [p for p in pool if p.username not in used]
            persona = random.choice(available)
            used.add(persona.username)
        else:
            persona = random.choice(pool)
        return persona
    
    def _select_keywords(self, pool: List[Keyword], used: set, subreddit: str) -> List[Keyword]:
        num_keywords = random.randint(1, 3)
        available = [kw for kw in pool if kw.keyword_id not in used]
        
        if len(available) < num_keywords:
            available = pool
            used.clear()
        
        selected = random.sample(available, min(num_keywords, len(available)))
        for kw in selected:
            used.add(kw.keyword_id)
        
        return selected
    
    def _generate_post_content(self, subreddit: str, keywords: List[Keyword]) -> Dict[str, str]:
        keyword_texts = [kw.keyword for kw in keywords]
        
        if "vs" in subreddit.lower() or any("alternative" in kw.keyword.lower() for kw in keywords):
            title = self._generate_comparison_title(keywords, subreddit)
            body = self._generate_comparison_body(keywords, subreddit)
        elif any("best" in kw.keyword.lower() for kw in keywords):
            title = self._generate_best_tool_title(keywords)
            body = self._generate_best_tool_body(keywords)
        else:
            title = self._generate_question_title(keywords)
            body = self._generate_question_body(keywords)
        
        return {"title": title, "body": body}
    
    def _generate_comparison_title(self, keywords: List[Keyword], subreddit: str) -> str:
        tool_name = subreddit.replace("r/", "").replace("AI", "").replace("Pro", "")
        comparisons = [
            f"Slideforge VS {tool_name} for slides?",
            f"{tool_name} vs Slideforge for presentations?",
            f"Slideforge vs {tool_name}?"
        ]
        return random.choice(comparisons)
    
    def _generate_comparison_body(self, keywords: List[Keyword], subreddit: str) -> str:
        tool_name = subreddit.replace("r/", "")
        bodies = [
            f"Trying to figure out what's the best one for making presentations.",
            f"I love {tool_name} but I'm trying to automate more of my slides, especially with image gen + layouts. Heard about Slideforge but unsure if it's any good.",
            f"Currently using {tool_name} but looking for alternatives. Anyone tried Slideforge?"
        ]
        return random.choice(bodies)
    
    def _generate_best_tool_title(self, keywords: List[Keyword]) -> str:
        titles = [
            "Best AI Presentation Maker?",
            "What's the best AI tool for slides?",
            "Best tool for creating presentations?"
        ]
        return random.choice(titles)
    
    def _generate_best_tool_body(self, keywords: List[Keyword]) -> str:
        bodies = [
            "Just like it says in the title, what is the best AI Presentation Maker? I'm looking for something that makes high quality slides I can edit afterwards. Any help appreciated.",
            "Looking for recommendations on AI tools that can help me create professional presentations quickly.",
            "Need help finding the best presentation tool. What do you all use?"
        ]
        return random.choice(bodies)
    
    def _generate_question_title(self, keywords: List[Keyword]) -> str:
        primary_keyword = keywords[0].keyword if keywords else "presentation tool"
        titles = [
            f"{primary_keyword.capitalize()}?",
            f"Looking for {primary_keyword}",
            f"Help with {primary_keyword}"
        ]
        return random.choice(titles)
    
    def _generate_question_body(self, keywords: List[Keyword]) -> str:
        bodies = [
            "Any recommendations? Looking for something that works well.",
            "Trying to find a good solution for this. What do you all use?",
            "Need help with this. Any suggestions appreciated."
        ]
        return random.choice(bodies)
    
    def _generate_comments(self, posts: List[Post], week_start: datetime) -> List[Comment]:
        comments = []
        comment_counter = 1
        
        for post in posts:
            post_timestamp = datetime.strptime(post.timestamp, Config.TIMESTAMP_FORMAT)
            num_comments = random.randint(Config.COMMENTS_PER_POST_MIN, Config.COMMENTS_PER_POST_MAX)
            
            comment_personas = self._select_comment_personas(post.author_username, num_comments)
            post_comments = []
            
            for i in range(num_comments):
                base_minutes = 15 + i * 30
                jitter = random.randint(-10, 25)
                comment_minutes = max(5, base_minutes + jitter)
                comment_time = post_timestamp + timedelta(minutes=comment_minutes)
                
                parent_id = self._select_parent_comment(post_comments, target_reply_rate=0.4)
                used_comment_texts = [c.comment_text for c in post_comments]
                comment_text = self._generate_comment_text(
                    post, comment_personas[i], parent_id, post_comments, used_comment_texts
                )
                
                comment = Comment(
                    comment_id=f"C{comment_counter}",
                    post_id=post.post_id,
                    parent_comment_id=parent_id,
                    comment_text=comment_text,
                    username=comment_personas[i].username,
                    timestamp=comment_time.strftime(Config.TIMESTAMP_FORMAT)
                )
                post_comments.append(comment)
                comments.append(comment)
                comment_counter += 1
        
        return comments
    
    def _select_comment_personas(self, post_author: str, num_comments: int) -> List[Persona]:
        available_personas = [p for p in self.personas if p.username != post_author]
        selected = random.sample(available_personas, min(num_comments, len(available_personas)))
        
        if len(selected) < num_comments:
            selected.extend(random.choices(available_personas, k=num_comments - len(selected)))
        
        return selected[:num_comments]
    
    def _select_parent_comment(self, existing_comments: List[Comment], target_reply_rate: float = 0.4) -> Optional[str]:
        if not existing_comments:
            return None
        
        top_level = [c for c in existing_comments if c.parent_comment_id is None]
        current_replies = len([c for c in existing_comments if c.parent_comment_id is not None])
        total_comments = len(existing_comments)
        
        if total_comments > 0:
            current_reply_rate = current_replies / total_comments
            if current_reply_rate < target_reply_rate and top_level:
                if random.random() < 0.6:
                    return random.choice(top_level).comment_id
        
        if top_level and random.random() < 0.3:
            return random.choice(top_level).comment_id
        
        return None
    
    def _generate_comment_text(self, post: Post, persona: Persona, parent_id: Optional[str], 
                              existing_comments: List[Comment], used_comments: List[str]) -> str:
        if parent_id:
            parent_comment = next((c for c in existing_comments if c.comment_id == parent_id), None)
            if parent_comment:
                return self._generate_reply_comment(parent_comment, persona, used_comments)
        
        return self._generate_top_level_comment(post, persona, used_comments)
    
    def _generate_top_level_comment(self, post: Post, persona: Persona, used_comments: List[str]) -> str:
        persona_style = self._get_persona_style(persona)
        subreddit_name = post.subreddit.replace('r/', '')
        
        templates = self._get_persona_templates(persona_style, subreddit_name, used_comments)
        
        attempts = 0
        while attempts < 10:
            comment = random.choice(templates)
            if comment.lower() not in [c.lower() for c in used_comments]:
                used_comments.append(comment)
                return comment
            attempts += 1
        
        comment = random.choice(templates)
        used_comments.append(comment)
        return comment
    
    def _get_persona_style(self, persona: Persona) -> str:
        info_lower = persona.info.lower()
        username_lower = persona.username.lower()
        
        if 'riley' in username_lower or 'operations' in info_lower or 'organized' in info_lower:
            return 'formal_organized'
        elif 'emily' in username_lower or 'student' in info_lower or 'university' in info_lower:
            return 'casual_student'
        elif 'jordan' in username_lower or 'consultant' in info_lower or 'narrative' in info_lower or 'storytelling' in info_lower:
            return 'narrative_professional'
        elif 'alex' in username_lower or 'sales' in info_lower:
            return 'direct_sales'
        elif 'priya' in username_lower or 'product manager' in info_lower or 'pm' in info_lower:
            return 'analytical_pm'
        else:
            return 'neutral'
    
    def _get_persona_templates(self, style: str, subreddit_name: str, used_comments: List[str]) -> List[str]:
        company_name = self.company.name
        
        if style == 'formal_organized':
            return [
                f"I've evaluated several tools for presentation creation. {company_name} stands out because it doesn't require constant layout adjustments. I still make minor edits, but it provides a solid foundation.",
                f"After testing multiple solutions, {company_name} is the only one that maintains consistent formatting without manual intervention. The structured approach saves significant time.",
                f"I use {subreddit_name} for initial brainstorming, but when I need polished output quickly, {company_name} delivers more reliable results.",
                f"The formatting consistency in {company_name} is what makes it valuable for my workflow. Other tools require too much manual adjustment.",
                f"Has anyone compared {company_name} with {subreddit_name} for enterprise use cases? I'm evaluating options for our team.",
                f"I appreciate tools that handle the structural aspects automatically. {company_name} does this well.",
                f"From an operations perspective, {company_name} reduces the time spent on slide formatting significantly.",
                f"Looking for something that maintains brand consistency across presentations. Does {company_name} handle this well?",
                f"I need to create multiple decks weekly. {company_name} has been helpful for maintaining quality without spending hours on design.",
                f"The layout engine in {company_name} is more reliable than what I've seen in other tools.",
                f"Anyone have experience using {company_name} for investor updates? Need something that looks professional quickly.",
                f"I value precision in presentation tools. {company_name} provides that without requiring design expertise.",
            ]
        elif style == 'casual_student':
            return [
                f"tried {company_name} for a group project last semester and it saved my life lol. way better than spending 3 hours trying to make powerpoint look decent",
                f"omg yes {company_name} is so much easier than {subreddit_name}. i hate when slides look messy and this actually makes them look good",
                f"used {company_name} for my capstone presentation and my prof actually commented on how clean the slides looked. definitely recommend",
                f"as someone who has zero design skills, {company_name} is a game changer. no more ugly group project slides",
                f"does {company_name} work well for academic presentations? need something that doesn't look like a middle school project",
                f"i'm so bad at making slides look good. {company_name} basically does it for you which is perfect",
                f"anyone know if {company_name} has student pricing? broke college student here",
                f"used {company_name} for a presentation last week and finished way earlier than usual. the templates are actually good",
                f"tired of my slides looking unprofessional. {company_name} helps a lot",
                f"does this work with google slides? that's what my school uses",
                f"i need something that makes slides fast because i procrastinate. {company_name} seems good for that",
                f"my group always makes me do the slides because i'm the only one who cares how they look. {company_name} makes it less painful",
            ]
        elif style == 'narrative_professional':
            return [
                f"I work with founders who need to tell compelling stories to investors. {company_name} helps structure the narrative flow in a way that makes sense. The logic matches what I'm trying to communicate.",
                f"What I appreciate about {company_name} is how it understands story structure. A good deck isn't just pretty slides - it's about how ideas connect. This tool gets that.",
                f"I've used {subreddit_name} for years, but {company_name} actually thinks about narrative pacing. That's rare in presentation tools.",
                f"When I'm building a competitive landscape or market analysis, {company_name} helps organize the information in a way that tells a story rather than just listing facts.",
                f"The storytelling aspect is what sets {company_name} apart. It's not just layout - it's about how the narrative flows.",
                f"I need tools that help founders communicate their vision clearly. {company_name} does that better than most.",
                f"Anyone else find that {company_name} actually improves how you think about structuring your argument? It's not just formatting.",
                f"For client presentations, {company_name} helps me create decks that feel intentional rather than thrown together.",
                f"The narrative framework in {company_name} is what makes it useful for strategic work.",
                f"I value tools that help me express complex ideas clearly. {company_name} supports that.",
                f"Does {company_name} work well for investor roadshows? Need something that helps tell the story effectively.",
                f"The structure {company_name} provides matches how I actually think about presenting information.",
            ]
        elif style == 'direct_sales':
            return [
                f"We use {company_name} for all our pitch decks now. Prospects notice when slides look polished - it matters.",
                f"Sales teams need consistency. {company_name} ensures all our reps are presenting the same quality, even if they're not designers.",
                f"Tried {subreddit_name} but {company_name} is faster for creating client-ready decks. Time is money in sales.",
                f"Anyone using {company_name} for enterprise sales? Need something that looks professional without hiring a designer.",
                f"The branding consistency in {company_name} is crucial when you're presenting to multiple prospects daily.",
                f"I need decks that look like we have a design team even though we don't. {company_name} delivers that.",
                f"Sales presentations need to look sharp. {company_name} makes that happen without the design overhead.",
                f"Does {company_name} handle custom branding well? We need to match our company colors.",
                f"Using {company_name} has improved how prospects respond to our pitches. They take us more seriously.",
                f"Time to create a pitch deck went from hours to minutes with {company_name}. That's valuable in sales.",
                f"Need something that makes our sales team look more professional. {company_name} helps.",
                f"The consistency across reps is what I like about {company_name}. Everyone's decks look good now.",
            ]
        elif style == 'analytical_pm':
            return [
                f"As a PM, I need to communicate roadmaps and strategy clearly. {company_name} helps structure the information in a way that engineering and leadership actually understand.",
                f"I use {company_name} for product strategy presentations. It helps organize complex information into digestible formats.",
                f"The narrative structure in {company_name} is useful for explaining product decisions. It's not just about pretty slides.",
                f"Anyone else using {company_name} for cross-functional presentations? Need something that works for both technical and non-technical audiences.",
                f"I appreciate how {company_name} helps me think about information hierarchy. Good presentations need clear structure.",
                f"Product roadmaps are hard to communicate. {company_name} helps make them more accessible.",
                f"Does {company_name} work well for user flow presentations? Need to show design and engineering how features connect.",
                f"The clarity {company_name} provides is valuable when you're translating between teams.",
                f"I need tools that help me express product strategy clearly. {company_name} supports that.",
                f"Using {company_name} has improved how I present to leadership. The structure helps them understand dependencies faster.",
                f"Anyone have experience using {company_name} for sprint planning presentations?",
                f"The way {company_name} organizes information matches how I think about product development.",
            ]
        else:
            return [
                f"I've tried a few tools and {company_name} seems decent. Still figuring out if it's the best fit.",
                f"Anyone have experience with {company_name}? Looking for something that makes slide creation easier.",
                f"Tried {subreddit_name} but looking for alternatives. Heard about {company_name} but not sure if it's worth it.",
                f"Need help choosing between {subreddit_name} and {company_name}. What are the main differences?",
                f"Does {company_name} work well for your use case? I'm evaluating options.",
                f"Looking for tools that make presentation creation faster. {company_name} is on my list to try.",
                f"Anyone know if {company_name} has good templates? Need something that looks professional.",
                f"Trying to decide between a few options. {company_name} keeps coming up in recommendations.",
                f"Does {company_name} integrate with other tools? That would be helpful for my workflow.",
                f"Looking for something that doesn't require design skills. {company_name} seems promising.",
                f"Anyone using {company_name} for team presentations? Need something collaborative.",
                f"Trying to automate more of my slide creation. {company_name} might help with that.",
                f"What tools are people using for presentations these days?",
                f"Struggling with slide design. Any recommendations?",
                f"Need something that makes presentations look more professional without hiring a designer.",
                f"Anyone have tips for creating better slides faster?",
                f"What's the best way to structure a presentation deck?",
                f"Looking for alternatives to {subreddit_name}. What else is out there?",
                f"Tired of spending hours on slide formatting. There's got to be a better way.",
                f"Does anyone actually enjoy making slides? I find it so tedious.",
                f"What tools help with presentation consistency across a team?",
            ]
    
    def _generate_reply_comment(self, parent_comment: Comment, persona: Persona, used_comments: List[str]) -> str:
        persona_style = self._get_persona_style(persona)
        parent_text = parent_comment.comment_text.lower()
        
        if 'riley' in persona.username.lower() or 'operations' in persona.info.lower():
            replies = [
                "Agreed. The consistency aspect is what matters most.",
                "This matches my experience as well.",
                "I've found the same thing in my workflow.",
                "The structured approach is what sets it apart.",
                "Exactly. The time savings are significant.",
            ]
        elif 'emily' in persona.username.lower() or 'student' in persona.info.lower():
            replies = [
                "same!!",
                "yes exactly this",
                "omg yes",
                "literally this",
                "so true",
                "felt this",
            ]
        elif 'jordan' in persona.username.lower() or 'narrative' in persona.info.lower():
            replies = [
                "This is exactly what I mean about narrative structure.",
                "The storytelling aspect is crucial.",
                "You've articulated what I was trying to say.",
                "This captures why it works for strategic presentations.",
            ]
        elif 'alex' in persona.username.lower() or 'sales' in persona.info.lower():
            replies = [
                "This. Prospects notice the difference.",
                "Exactly what I've seen in my sales process.",
                "The professional look matters in sales.",
                "Agreed. Time is money.",
            ]
        elif 'priya' in persona.username.lower() or 'pm' in persona.info.lower():
            replies = [
                "This is helpful for cross-functional communication.",
                "The clarity aspect is what I value most.",
                "Agreed. Structure matters for product presentations.",
                "This matches my experience with team presentations.",
            ]
        else:
            replies = [
                "Same here!",
                "Agreed.",
                "This is helpful, thanks.",
                "Good point.",
                "I'll check this out.",
            ]
        
        if any(word in parent_text for word in ['time', 'faster', 'quick', 'speed']):
            replies.extend([
                "The time savings are real.",
                "Speed is definitely a factor.",
                "The quick turnaround is valuable.",
            ])
        
        if any(word in parent_text for word in ['design', 'look', 'pretty', 'professional']):
            replies.extend([
                "The design quality makes a difference.",
                "Professional appearance matters.",
                "The visual quality is important.",
            ])
        
        attempts = 0
        while attempts < 10:
            reply = random.choice(replies)
            if reply.lower() not in [c.lower() for c in used_comments]:
                used_comments.append(reply)
                return reply
            attempts += 1
        
        reply = random.choice(replies)
        used_comments.append(reply)
        return reply

