# Reddit Content Calendar Generator

This tool generates weekly content calendars for Reddit. You give it company info, personas, keywords, and it spits out a plan for posts and comments across different subreddits.

## What It Does

Generates weekly calendars with posts and threaded comments. Distributes content across multiple Reddit personas. Matches keywords to relevant subreddits. Creates comment threads that look somewhat natural. Can generate calendars for current week or future weeks. Exports to JSON and CSV.

## Files

app.py is the Flask web app. calendar_algorithm.py has the main algorithm. config.py has settings. data_loader.py loads and saves data. models.py has the data structures. output_formatter.py formats output. requirements.txt has the Python packages needed. templates/index.html is the web UI. data/input is where you put your data. data/output is where generated calendars go.

## Setup

Install the Python packages: pip install -r requirements.txt

Put your input data in data/input/input_data.json (there's a sample file already).

## How to Use

### Web Interface

Start the server: python app.py

Go to http://localhost:5000 in your browser.

Click "Generate This Week" for current week. Click "Generate Next 4 Weeks" for future weeks.

### Command Line

python cli.py --num-weeks 1 for current week. python cli.py --num-weeks 4 for next 4 weeks. python cli.py --week-offset 1 for week 2.

## How It Works

You give it company info (name, description, subreddits), personas (Reddit accounts with backstories), keywords (what you want to rank for), posts per week (how many to generate).

It gives you posts distributed across subreddits, comments from different personas, realistic timestamps, keywords matched to posts.

The algorithm spreads posts across different days, ensures variety in subreddits and personas, matches keywords. Generates 2-4 comments per post, creates reply chains (about 40% are replies), uses different personas. Makes comparison posts, "best tool" posts, or question posts depending on the subreddit/keyword.

## Output

Calendars get saved as JSON in data/output/calendar_week_N.json and CSV in data/output/posts.csv and comments.csv.

## Configuration

Edit config.py to change posts per week, comments per post range, comment thread depth, timestamp format.

## Sample Data

There's sample data for Slideforge (fake company) with 6 personas, 20 subreddits, 16 keywords, 3 posts per week.

## The Goal

Create posts and comments that get upvotes and views, drive inbound leads, build Reddit presence, rank on Google, get cited in LLM answers (ChatGPT, etc).

## Testing

Run the test suite to check quality: python run_tests.py

This will show you quality scores, naturalness analysis, and catch edge cases.

## Known Issues

Comment templates are limited (only 8 variations). All personas sound the same. Comments are too repetitive. Reply comments are too generic.

See QUALITY_REPORT.md for more details on what needs fixing.
