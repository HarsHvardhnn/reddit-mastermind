from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
from calendar_algorithm import ContentCalendarGenerator
from data_loader import DataLoader
from output_formatter import OutputFormatter
from models import Company, Persona, Keyword
from config import Config
import os

app = Flask(__name__)

data_loader = DataLoader()
formatter = OutputFormatter()

generator = None
current_week = 0

def initialize_generator():
    global generator
    input_file = os.path.join(Config.INPUT_DIR, "input_data.json")
    
    if not os.path.exists(input_file):
        return None
    
    data = data_loader.load_from_file(input_file)
    
    company = data_loader.load_company(data["company"])
    personas = data_loader.load_personas(data["personas"])
    keywords = data_loader.load_keywords(data["keywords"])
    
    generator = ContentCalendarGenerator(company, personas, keywords)
    return generator

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-week', methods=['POST'])
def generate_week():
    global current_week
    
    if generator is None:
        if initialize_generator() is None:
            return jsonify({"error": "Input data not found"}), 404
    
    data = request.json or {}
    week_offset = data.get('week_offset', current_week)
    
    week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = week_start - timedelta(days=week_start.weekday())
    week_start = week_start + timedelta(weeks=week_offset)
    
    posts_per_week = data.get('posts_per_week', Config.POSTS_PER_WEEK)
    
    calendar = generator.generate_week_calendar(week_start, posts_per_week)
    calendar_dict = formatter.calendar_to_dict(calendar)
    
    week_number = week_offset + 1
    output_path = data_loader.save_calendar(calendar_dict, week_number)
    formatter.calendar_to_csv(calendar, Config.OUTPUT_DIR)
    
    return jsonify({
        "calendar": calendar_dict,
        "output_path": output_path,
        "week_number": week_number
    })

@app.route('/api/generate-subsequent', methods=['POST'])
def generate_subsequent():
    global current_week
    
    if generator is None:
        if initialize_generator() is None:
            return jsonify({"error": "Input data not found"}), 404
    
    data = request.json or {}
    num_weeks = data.get('num_weeks', 4)
    
    results = []
    base_week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    base_week_start = base_week_start - timedelta(days=base_week_start.weekday())
    base_week_start = base_week_start + timedelta(weeks=current_week + 1)
    
    posts_per_week = data.get('posts_per_week', Config.POSTS_PER_WEEK)
    
    for i in range(num_weeks):
        week_start = base_week_start + timedelta(weeks=i)
        calendar = generator.generate_week_calendar(week_start, posts_per_week)
        calendar_dict = formatter.calendar_to_dict(calendar)
        
        week_number = current_week + i + 2
        output_path = data_loader.save_calendar(calendar_dict, week_number)
        formatter.calendar_to_csv(calendar, Config.OUTPUT_DIR)
        
        results.append({
            "calendar": calendar_dict,
            "output_path": output_path,
            "week_number": week_number
        })
    
    return jsonify({"weeks": results})

@app.route('/api/status', methods=['GET'])
def status():
    if generator is None:
        initialize_generator()
    
    has_data = generator is not None
    return jsonify({
        "initialized": has_data,
        "current_week": current_week
    })

if __name__ == '__main__':
    os.makedirs(Config.INPUT_DIR, exist_ok=True)
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    initialize_generator()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


