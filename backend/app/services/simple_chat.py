import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SimpleChatbot:
    """Simple rule-based chatbot that can answer questions based on scraped content"""
    
    def __init__(self):
        self.rules = {
            'hours': {
                'keywords': ['hour', 'time', 'open', 'close', 'schedule', 'when', 'operating'],
                'response_template': 'Based on the available information, {context}. For the most accurate and up-to-date information, please check the website directly or contact the business.'
            },
            'pricing': {
                'keywords': ['price', 'cost', 'fee', 'charge', 'rate', 'how much', 'costs'],
                'response_template': 'I can see some pricing information in the content: {context}. For the most current and accurate pricing, please check the website directly or contact the business.'
            },
            'contact': {
                'keywords': ['contact', 'phone', 'email', 'address', 'location', 'where', 'call'],
                'response_template': 'Contact information found: {context}. For the most up-to-date contact details, please check the website directly.'
            },
            'services': {
                'keywords': ['service', 'product', 'offer', 'provide', 'what do you', 'do you offer'],
                'response_template': 'Based on the available content, here are the services and offerings: {context}. For more detailed information, please check the website directly.'
            },
            'general': {
                'keywords': ['what', 'how', 'why', 'when', 'where', 'who'],
                'response_template': 'I found some relevant information: {context}. For more detailed information, please check the website directly.'
            }
        }
    
    def generate_response(self, user_message: str, context: str) -> str:
        """Generate a response based on user message and context"""
        if not context.strip():
            return "I don't have enough information to answer your question. Please check the website directly or contact the business for more details."
        
        user_message_lower = user_message.lower()
        
        # Find the best matching rule
        best_rule = None
        best_score = 0
        
        for rule_name, rule_data in self.rules.items():
            score = sum(1 for keyword in rule_data['keywords'] if keyword in user_message_lower)
            if score > best_score:
                best_score = score
                best_rule = rule_name
        
        if best_rule and best_score > 0:
            # Extract relevant information from context
            relevant_info = self._extract_relevant_info(context, best_rule)
            template = self.rules[best_rule]['response_template']
            return template.format(context=relevant_info)
        else:
            # Fallback response
            return self._generate_fallback_response(context)
    
    def _extract_relevant_info(self, context: str, rule_type: str) -> str:
        """Extract relevant information from context based on rule type"""
        context_lower = context.lower()
        
        if rule_type == 'hours':
            # Look for time patterns
            time_patterns = [
                r'\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)',
                r'\d{1,2}\s*(?:AM|PM|am|pm)',
                r'(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
                r'(?:open|closed|hours|time)'
            ]
            
            relevant_lines = []
            lines = context.split('\n')
            for line in lines:
                line_lower = line.lower()
                if any(re.search(pattern, line_lower) for pattern in time_patterns):
                    relevant_lines.append(line.strip())
            
            if relevant_lines:
                return '; '.join(relevant_lines[:3])  # Limit to 3 lines
            else:
                return "some operating hours information is available"
        
        elif rule_type == 'pricing':
            # Look for price patterns
            price_patterns = [
                r'\$\d+(?:\.\d{2})?',
                r'\d+(?:\.\d{2})?\s*(?:dollars?|euros?|pounds?)',
                r'(?:price|cost|fee|charge)',
                r'(?:free|complimentary)'
            ]
            
            relevant_lines = []
            lines = context.split('\n')
            for line in lines:
                line_lower = line.lower()
                if any(re.search(pattern, line_lower) for pattern in price_patterns):
                    relevant_lines.append(line.strip())
            
            if relevant_lines:
                return '; '.join(relevant_lines[:3])
            else:
                return "pricing information is available"
        
        elif rule_type == 'contact':
            # Look for contact patterns
            contact_patterns = [
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # Phone numbers
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
                r'(?:phone|email|contact|address)',
                r'(?:call|email|reach)'
            ]
            
            relevant_lines = []
            lines = context.split('\n')
            for line in lines:
                line_lower = line.lower()
                if any(re.search(pattern, line_lower) for pattern in contact_patterns):
                    relevant_lines.append(line.strip())
            
            if relevant_lines:
                return '; '.join(relevant_lines[:3])
            else:
                return "contact information is available"
        
        elif rule_type == 'services':
            # Extract service-related information
            service_keywords = ['service', 'product', 'offer', 'provide', 'specialize', 'expertise']
            relevant_lines = []
            lines = context.split('\n')
            for line in lines:
                line_lower = line.lower()
                if any(keyword in line_lower for keyword in service_keywords):
                    relevant_lines.append(line.strip())
            
            if relevant_lines:
                return '; '.join(relevant_lines[:3])
            else:
                return "various services and offerings are available"
        
        else:
            # General information extraction
            return context[:200] + "..." if len(context) > 200 else context
    
    def _generate_fallback_response(self, context: str) -> str:
        """Generate a fallback response when no specific rule matches"""
        if context.strip():
            # Extract first few sentences
            sentences = re.split(r'[.!?]+', context)
            relevant_sentences = [s.strip() for s in sentences if len(s.strip()) > 20][:2]
            
            if relevant_sentences:
                return f"I found some relevant information: {' '.join(relevant_sentences)}. For more detailed information, please check the website directly."
            else:
                return "I have some information available, but for the most accurate and up-to-date details, please check the website directly or contact the business."
        else:
            return "I don't have enough information to answer your question. Please check the website directly or contact the business for more details."

# Global instance
simple_chatbot = SimpleChatbot()

def generate_simple_response(user_message: str, context: str = "") -> str:
    """Generate a response using the simple chatbot"""
    return simple_chatbot.generate_response(user_message, context) 