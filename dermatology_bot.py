import json
import re
import random
from difflib import get_close_matches

class DermatologyExpert:
    def __init__(self):
        self.knowledge = self._load_knowledge()
        self.emergency_terms = [
            "trouble breathing", "swelling face", "high fever",
            "severe pain", "rapid spreading", "skin peeling"
        ]
    
    def _load_knowledge(self):
        with open('dermatology_knowledge.json', 'r') as f:
            return json.load(f)
    
    def _is_emergency(self, text):
        return any(term in text.lower() for term in self.emergency_terms)
    
    def get_condition_info(self, condition_name):
        """Get structured info about a condition"""
        for condition in self.knowledge['conditions']:
            if condition['name'].lower() == condition_name.lower():
                return self._format_response(condition)
        return None
    
    def respond(self, user_input):
        if self._is_emergency(user_input):
            return self._emergency_response()
        
        condition = self._match_condition(user_input)
        if condition:
            return self._format_response(condition)
        
        return self._general_response(user_input)
    
    def _match_condition(self, text):
        text = text.lower()
        for condition in self.knowledge['conditions']:
            if (condition['name'].lower() in text or 
                any(kw in text for kw in condition['keywords'])):
                return condition
        
        condition_names = [c['name'].lower() for c in self.knowledge['conditions']]
        matches = get_close_matches(text, condition_names, n=1, cutoff=0.6)
        if matches:
            return next(c for c in self.knowledge['conditions'] 
                      if c['name'].lower() == matches[0])
        return None
    
    def _format_response(self, condition):
        response = f"**{condition['name']}**\n\n"
        response += f"*Description*: {condition['description']}\n\n"
        response += "*Common Symptoms*:\n- " + "\n- ".join(condition['symptoms']) + "\n\n"
        response += "*Recommended Treatments*:\n- " + "\n- ".join(condition['treatments']['topical'][:3])
        
        if 'red_flags' in condition:
            response += "\n\n⚠️ *Seek Immediate Care For*:\n- " + "\n- ".join(condition['red_flags'])
        
        return response
    
    def _emergency_response(self):
        return (
            "🚨 **Potential Medical Emergency** 🚨\n\n"
            "1. Stop all current treatments\n"
            "2. Call emergency services if:\n"
            "   - Difficulty breathing/swallowing\n"
            "   - Swelling of face/lips\n"
            "   - High fever with rash\n"
            "3. Take photos for documentation\n"
            "4. Avoid scratching affected areas"
        )
    
    def _general_response(self, text):
        text = text.lower()
        if any(word in text for word in ["routine", "prevent"]):
            return "**Daily Skin Care**:\n- " + "\n- ".join(self.knowledge['general_advice']['daily_care'])
        
        if any(word in text for word in ["sun", "uv"]):
            return (
                "**Sun Protection** ☀️\n"
                "- Use SPF 30+ broad spectrum\n"
                "- Reapply every 2 hours outdoors\n"
                "- Wear UPF clothing and hats\n"
                "- Seek shade 10AM-4PM"
            )
        
        return (
            "I specialize in skin health. Try asking about:\n"
            "- Specific conditions (acne, eczema)\n"
            "- Skin care routines\n"
            "- Treatment options\n"
            "- Symptom explanations"
        )
