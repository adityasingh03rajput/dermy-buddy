import json
import re
import random
from difflib import get_close_matches

class DermatologyExpert:
    def __init__(self):
        self.knowledge = self.load_knowledge()
        self.emergency_terms = [
            "trouble breathing", "swelling face", "high fever",
            "severe pain", "rapid spreading", "skin peeling"
        ]
        self.off_topic_phrases = [
            "I specialize in skin health only",
            "Let's focus on dermatology concerns",
            "I can only advise on skin-related matters"
        ]
    
    def load_knowledge(self):
        with open('dermatology_knowledge.json', 'r') as f:
            return json.load(f)
    
    def is_emergency(self, text):
        text = text.lower()
        return any(term in text for term in self.emergency_terms)
    
    def handle_emergency(self):
        return (
            "🚨 POTENTIAL MEDICAL EMERGENCY 🚨\n"
            "1. Stop all current treatments\n"
            "2. Call emergency services or go to ER if:\n"
            "   - Difficulty breathing/swallowing\n"
            "   - Swelling of face/lips\n"
            "   - High fever with rash\n"
            "3. Take photos for documentation\n"
            "4. Avoid scratching/touching affected areas"
        )
    
    def is_off_topic(self, text):
        text = text.lower()
        if re.search(r"\b(politic|sport|celebr|financ|stock|movie)\b", text):
            return True
        return False
    
    def find_condition(self, text):
        text = text.lower()
        for condition in self.knowledge['conditions']:
            if condition['name'].lower() in text:
                return condition
            if any(kw in text for kw in condition['keywords']):
                return condition
        
        condition_names = [c['name'].lower() for c in self.knowledge['conditions']]
        matches = get_close_matches(text, condition_names, n=1, cutoff=0.6)
        if matches:
            matched_name = matches[0]
            for condition in self.knowledge['conditions']:
                if condition['name'].lower() == matched_name:
                    return condition
        return None
    
    def get_condition_info(self, condition_name):
        """Get structured information about a specific condition"""
        for condition in self.knowledge['conditions']:
            if condition['name'].lower() == condition_name.lower():
                return self.generate_response(condition)
        return None
    
    def generate_response(self, condition):
        response = f"**{condition['name'].title()}**\n"
        response += f"*Description*: {condition['description']}\n\n"
        response += "*Symptoms*:\n- " + "\n- ".join(condition['symptoms'].split(", ")) + "\n\n"
        response += "*Recommended Treatments*:\n- " + "\n- ".join(condition['treatments']) + "\n\n"
        
        if 'red_flags' in condition:
            response += "🚩 *Red Flags/Warning Signs*:\n- " + "\n- ".join(condition['red_flags']) + "\n"
        
        return response
    
    def handle_general_question(self, text):
        text = text.lower()
        
        if any(word in text for word in ["routine", "daily care", "prevent"]):
            return "**Daily Skin Care Advice**:\n- " + "\n- ".join(self.knowledge['general_advice']['daily_care'])
        
        if any(word in text for word in ["sun", "uv", "sunscreen"]):
            return (
                "**Sun Protection Guidelines**:\n"
                "- Use broad-spectrum SPF 30+ daily\n"
                "- Reapply every 2 hours outdoors\n"
                "- Wear UPF clothing and wide-brim hats\n"
                "- Seek shade 10AM-4PM\n"
                "- Check skin monthly for changes"
            )
        
        if any(word in text for word in ["mole", "ABCDE"]):
            abcde = self.knowledge['diagnostic_tools']['ABCDE_of_moles']
            return (
                "**Mole Evaluation (ABCDE Rule)**:\n"
                f"A: {abcde['A']}\n"
                f"B: {abcde['B']}\n"
                f"C: {abcde['C']}\n"
                f"D: {abcde['D']}\n"
                f"E: {abcde['E']}\n\n"
                "⚠️ See a dermatologist if any of these apply"
            )
        
        return None
    
    def respond(self, user_input):
        if self.is_emergency(user_input):
            return self.handle_emergency()
        
        if self.is_off_topic(user_input):
            return random.choice(self.off_topic_phrases)
        
        condition = self.find_condition(user_input)
        if condition:
            return self.generate_response(condition)
        
        general_response = self.handle_general_question(user_input)
        if general_response:
            return general_response
        
        return (
            "I specialize in dermatology. Could you clarify your skin concern?\n"
            "For example:\n"
            "- 'I have a red itchy rash'\n"
            "- 'What's the best treatment for acne?'\n"
            "- 'How to evaluate a suspicious mole?'"
        )
