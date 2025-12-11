import json
import os
from typing import Dict, List
from models import Company, Persona, Keyword
from config import Config

class DataLoader:
    @staticmethod
    def load_company(data: Dict) -> Company:
        return Company(
            name=data["name"],
            website=data["website"],
            description=data["description"],
            icp=data.get("icp", {}),
            subreddits=data["subreddits"]
        )
    
    @staticmethod
    def load_personas(data: List[Dict]) -> List[Persona]:
        return [Persona(username=p["username"], info=p["info"]) for p in data]
    
    @staticmethod
    def load_keywords(data: List[Dict]) -> List[Keyword]:
        return [Keyword(keyword_id=k["keyword_id"], keyword=k["keyword"]) for k in data]
    
    @staticmethod
    def load_from_file(filepath: str) -> Dict:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def save_calendar(calendar_data: Dict, week_number: int = None):
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        
        if week_number is not None:
            filename = f"calendar_week_{week_number}.json"
        else:
            filename = "calendar_current.json"
        
        filepath = os.path.join(Config.OUTPUT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(calendar_data, f, indent=2, ensure_ascii=False)
        
        return filepath


