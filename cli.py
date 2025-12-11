import argparse
from datetime import datetime, timedelta
from calendar_algorithm import ContentCalendarGenerator
from data_loader import DataLoader
from output_formatter import OutputFormatter
from config import Config
import os

def main():
    parser = argparse.ArgumentParser(description='Generate Reddit content calendars')
    parser.add_argument('--week-offset', type=int, default=0, 
                       help='Week offset from current week (0 = current week)')
    parser.add_argument('--num-weeks', type=int, default=1,
                       help='Number of weeks to generate')
    parser.add_argument('--posts-per-week', type=int, default=None,
                       help='Number of posts per week (overrides config)')
    
    args = parser.parse_args()
    
    input_file = os.path.join(Config.INPUT_DIR, "input_data.json")
    
    if not os.path.exists(input_file):
        print(f"Error: Input data file not found at {input_file}")
        return
    
    data_loader = DataLoader()
    data = data_loader.load_from_file(input_file)
    
    company = data_loader.load_company(data["company"])
    personas = data_loader.load_personas(data["personas"])
    keywords = data_loader.load_keywords(data["keywords"])
    
    posts_per_week = args.posts_per_week or data["company"].get("posts_per_week", Config.POSTS_PER_WEEK)
    
    generator = ContentCalendarGenerator(company, personas, keywords)
    formatter = OutputFormatter()
    
    base_week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    base_week_start = base_week_start - timedelta(days=base_week_start.weekday())
    base_week_start = base_week_start + timedelta(weeks=args.week_offset)
    
    print(f"Generating {args.num_weeks} week(s) of content calendars...")
    print(f"Posts per week: {posts_per_week}\n")
    
    for i in range(args.num_weeks):
        week_start = base_week_start + timedelta(weeks=i)
        calendar = generator.generate_week_calendar(week_start, posts_per_week)
        calendar_dict = formatter.calendar_to_dict(calendar)
        
        week_number = args.week_offset + i + 1
        output_path = data_loader.save_calendar(calendar_dict, week_number)
        formatter.calendar_to_csv(calendar, Config.OUTPUT_DIR)
        
        print(f"Week {week_number} ({calendar.week_start} to {calendar.week_end}):")
        print(f"  - {len(calendar.posts)} posts")
        print(f"  - {len(calendar.comments)} comments")
        print(f"  - Saved to: {output_path}\n")
    
    print("✓ Calendar generation complete!")

if __name__ == '__main__':
    main()


