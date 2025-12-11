import json
import os
from datetime import datetime, timedelta
from calendar_algorithm import ContentCalendarGenerator
from data_loader import DataLoader
from quality_evaluator import QualityEvaluator
from natural_conversation_analyzer import NaturalConversationAnalyzer
from models import Company, Persona, Keyword
from config import Config

class TestFramework:
    def __init__(self):
        self.evaluator = QualityEvaluator()
        self.conversation_analyzer = NaturalConversationAnalyzer()
        self.results = []
    
    def run_all_tests(self):
        print("Running test suite...\n")
        
        self.test_basic_generation()
        self.test_edge_cases()
        self.test_different_inputs()
        self.test_quality_scenarios()
        
        self.print_summary()
    
    def test_basic_generation(self):
        print("=" * 60)
        print("TEST 1: Basic Generation")
        print("=" * 60)
        
        data_loader = DataLoader()
        input_file = os.path.join(Config.INPUT_DIR, "input_data.json")
        
        if not os.path.exists(input_file):
            print("ERROR: Input data not found")
            return
        
        data = data_loader.load_from_file(input_file)
        company = data_loader.load_company(data["company"])
        personas = data_loader.load_personas(data["personas"])
        keywords = data_loader.load_keywords(data["keywords"])
        
        generator = ContentCalendarGenerator(company, personas, keywords)
        week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = week_start - timedelta(days=week_start.weekday())
        
        calendar = generator.generate_week_calendar(week_start, 3)
        evaluation = self.evaluator.evaluate_calendar(calendar)
        naturalness = self.conversation_analyzer.analyze_naturalness(calendar.posts, calendar.comments)
        
        self._print_evaluation(evaluation)
        self._print_naturalness(naturalness)
        self.results.append(("Basic Generation", evaluation))
    
    def test_edge_cases(self):
        print("\n" + "=" * 60)
        print("TEST 2: Edge Cases")
        print("=" * 60)
        
        test_cases = [
            ("Too many posts", self._test_too_many_posts),
            ("Too few personas", self._test_few_personas),
            ("Single subreddit", self._test_single_subreddit),
            ("Many keywords", self._test_many_keywords),
        ]
        
        for name, test_func in test_cases:
            print(f"\n--- {name} ---")
            try:
                calendar, evaluation = test_func()
                self._print_evaluation(evaluation)
                self.results.append((name, evaluation))
            except Exception as e:
                print(f"ERROR: {e}")
    
    def test_different_inputs(self):
        print("\n" + "=" * 60)
        print("TEST 3: Different Company/Persona Inputs")
        print("=" * 60)
        
        test_companies = [
            ("Small Company", self._create_small_company()),
            ("Large Company", self._create_large_company()),
        ]
        
        for name, company_data in test_companies:
            print(f"\n--- {name} ---")
            try:
                company = company_data["company"]
                personas = company_data["personas"]
                keywords = company_data["keywords"]
                
                generator = ContentCalendarGenerator(company, personas, keywords)
                week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                week_start = week_start - timedelta(days=week_start.weekday())
                
                calendar = generator.generate_week_calendar(week_start, 3)
                evaluation = self.evaluator.evaluate_calendar(calendar)
                
                self._print_evaluation(evaluation)
                self.results.append((name, evaluation))
            except Exception as e:
                print(f"ERROR: {e}")
    
    def test_quality_scenarios(self):
        print("\n" + "=" * 60)
        print("TEST 4: Quality Scenarios (3/10 vs 9/10)")
        print("=" * 60)
        
        print("\n--- Scenario: High Quality (should score 8-10/10) ---")
        high_quality = self._create_high_quality_scenario()
        if high_quality:
            self._print_evaluation(high_quality)
            self.results.append(("High Quality Scenario", high_quality))
        
        print("\n--- Scenario: Low Quality (should score 2-4/10) ---")
        low_quality = self._create_low_quality_scenario()
        if low_quality:
            self._print_evaluation(low_quality)
            self.results.append(("Low Quality Scenario", low_quality))
    
    def _test_too_many_posts(self):
        data_loader = DataLoader()
        input_file = os.path.join(Config.INPUT_DIR, "input_data.json")
        data = data_loader.load_from_file(input_file)
        
        company = data_loader.load_company(data["company"])
        personas = data_loader.load_personas(data["personas"])
        keywords = data_loader.load_keywords(data["keywords"])
        
        generator = ContentCalendarGenerator(company, personas, keywords)
        week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = week_start - timedelta(days=week_start.weekday())
        
        calendar = generator.generate_week_calendar(week_start, 10)
        evaluation = self.evaluator.evaluate_calendar(calendar)
        
        return calendar, evaluation
    
    def _test_few_personas(self):
        company = Company(
            name="TestCo",
            website="test.com",
            description="Test",
            icp={},
            subreddits=["r/test1", "r/test2"]
        )
        
        personas = [
            Persona(username="user1", info="Test persona 1"),
            Persona(username="user2", info="Test persona 2")
        ]
        
        keywords = [
            Keyword(keyword_id="K1", keyword="test keyword")
        ]
        
        generator = ContentCalendarGenerator(company, personas, keywords)
        week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = week_start - timedelta(days=week_start.weekday())
        
        calendar = generator.generate_week_calendar(week_start, 5)
        evaluation = self.evaluator.evaluate_calendar(calendar)
        
        return calendar, evaluation
    
    def _test_single_subreddit(self):
        company = Company(
            name="TestCo",
            website="test.com",
            description="Test",
            icp={},
            subreddits=["r/test"]
        )
        
        personas = [
            Persona(username="user1", info="Test"),
            Persona(username="user2", info="Test"),
            Persona(username="user3", info="Test")
        ]
        
        keywords = [Keyword(keyword_id="K1", keyword="test")]
        
        generator = ContentCalendarGenerator(company, personas, keywords)
        week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = week_start - timedelta(days=week_start.weekday())
        
        calendar = generator.generate_week_calendar(week_start, 3)
        evaluation = self.evaluator.evaluate_calendar(calendar)
        
        return calendar, evaluation
    
    def _test_many_keywords(self):
        data_loader = DataLoader()
        input_file = os.path.join(Config.INPUT_DIR, "input_data.json")
        data = data_loader.load_from_file(input_file)
        
        company = data_loader.load_company(data["company"])
        personas = data_loader.load_personas(data["personas"])
        
        keywords = [Keyword(keyword_id=f"K{i}", keyword=f"keyword {i}") for i in range(50)]
        
        generator = ContentCalendarGenerator(company, personas, keywords)
        week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = week_start - timedelta(days=week_start.weekday())
        
        calendar = generator.generate_week_calendar(week_start, 3)
        evaluation = self.evaluator.evaluate_calendar(calendar)
        
        return calendar, evaluation
    
    def _create_small_company(self):
        return {
            "company": Company(
                name="SmallCo",
                website="small.com",
                description="Small company",
                icp={},
                subreddits=["r/small1", "r/small2"]
            ),
            "personas": [
                Persona(username="p1", info="Persona 1"),
                Persona(username="p2", info="Persona 2")
            ],
            "keywords": [
                Keyword(keyword_id="K1", keyword="keyword1"),
                Keyword(keyword_id="K2", keyword="keyword2")
            ]
        }
    
    def _create_large_company(self):
        return {
            "company": Company(
                name="LargeCo",
                website="large.com",
                description="Large company",
                icp={},
                subreddits=[f"r/sub{i}" for i in range(30)]
            ),
            "personas": [
                Persona(username=f"user{i}", info=f"Persona {i}") for i in range(10)
            ],
            "keywords": [
                Keyword(keyword_id=f"K{i}", keyword=f"keyword {i}") for i in range(30)
            ]
        }
    
    def _create_high_quality_scenario(self):
        company = Company(
            name="QualityCo",
            website="quality.com",
            description="High quality company",
            icp={},
            subreddits=["r/sub1", "r/sub2", "r/sub3", "r/sub4", "r/sub5"]
        )
        
        personas = [
            Persona(username=f"user{i}", info=f"Persona {i}") for i in range(6)
        ]
        
        keywords = [
            Keyword(keyword_id=f"K{i}", keyword=f"keyword {i}") for i in range(10)
        ]
        
        generator = ContentCalendarGenerator(company, personas, keywords)
        week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = week_start - timedelta(days=week_start.weekday())
        
        calendar = generator.generate_week_calendar(week_start, 3)
        evaluation = self.evaluator.evaluate_calendar(calendar)
        
        return evaluation
    
    def _create_low_quality_scenario(self):
        company = Company(
            name="BadCo",
            website="bad.com",
            description="Bad company",
            icp={},
            subreddits=["r/bad"]
        )
        
        personas = [
            Persona(username="user1", info="Only one persona")
        ]
        
        keywords = [
            Keyword(keyword_id="K1", keyword="only keyword")
        ]
        
        generator = ContentCalendarGenerator(company, personas, keywords)
        week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = week_start - timedelta(days=week_start.weekday())
        
        try:
            calendar = generator.generate_week_calendar(week_start, 5)
            evaluation = self.evaluator.evaluate_calendar(calendar)
            return evaluation
        except:
            return None
    
    def _print_evaluation(self, evaluation: dict):
        print(f"Score: {evaluation['score']}/100")
        print(f"Quality Level: {evaluation['quality_level']}")
        
        if evaluation['issues']:
            print(f"\nIssues ({len(evaluation['issues'])}):")
            for issue in evaluation['issues']:
                print(f"  - {issue}")
        
        if evaluation['warnings']:
            print(f"\nWarnings ({len(evaluation['warnings'])}):")
            for warning in evaluation['warnings']:
                print(f"  - {warning}")
        
        print(f"\nDetails:")
        for key, value in evaluation['details'].items():
            print(f"  {key}: {value}")
    
    def _print_naturalness(self, naturalness: dict):
        print(f"\nNaturalness Analysis:")
        print(f"  Conversation Quality: {naturalness['conversation_quality']['average_score']:.1f}/100")
        if naturalness['conversation_quality']['issues']:
            for issue in naturalness['conversation_quality']['issues'][:3]:
                print(f"    - {issue}")
        print(f"  Comment Diversity: {naturalness['comment_diversity']['score']:.1f}/100")
        print(f"  Realism Score: {naturalness['realism_score']}/100")
        if naturalness['red_flags']:
            print(f"  Red Flags ({len(naturalness['red_flags'])}):")
            for flag in naturalness['red_flags'][:3]:
                print(f"    - {flag}")
    
    def print_summary(self):
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        if not self.results:
            print("No tests completed")
            return
        
        scores = [r[1]['score'] for r in self.results]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        print(f"\nAverage Score: {avg_score:.1f}/100")
        print(f"Tests Run: {len(self.results)}")
        
        print("\nIndividual Results:")
        for name, evaluation in self.results:
            print(f"  {name}: {evaluation['score']}/100 ({evaluation['quality_level']})")

if __name__ == '__main__':
    framework = TestFramework()
    framework.run_all_tests()

