#!/usr/bin/env python3
"""
Test the simple chatbot functionality
"""

import sys
import os
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Load environment variables
load_dotenv()

from app.services.simple_chat import generate_simple_response

def test_simple_chat():
    """Test the simple chatbot with various questions"""
    
    print("=== Simple Chatbot Test ===\n")
    
    # Test context
    test_context = """
    GoGlass is a premium eyewear store located in Johannesburg, South Africa.
    We are open Monday to Friday from 9:00 AM to 6:00 PM, and Saturday from 10:00 AM to 4:00 PM.
    We are closed on Sundays and public holidays.
    
    Our services include:
    - Comprehensive eye examinations
    - Prescription glasses and sunglasses
    - Contact lens fitting and sales
    - Designer frames from top brands
    - Lens coatings and treatments
    
    Contact us:
    Phone: +27 11 555 0123
    Email: info@goglass.co.za
    Address: 123 Main Street, Johannesburg, 2000
    
    Prices start from R500 for basic frames and R800 for designer frames.
    Eye examinations cost R350.
    """
    
    # Test questions
    test_questions = [
        "What are the operating hours?",
        "How much do glasses cost?",
        "What is your phone number?",
        "Do you offer contact lenses?",
        "What services do you provide?",
        "Are you open on Sundays?",
        "What is the address?",
        "How much does an eye exam cost?"
    ]
    
    for question in test_questions:
        print(f"Q: {question}")
        response = generate_simple_response(question, test_context)
        print(f"A: {response}")
        print("-" * 50)
    
    # Test with empty context
    print("\n=== Testing with empty context ===")
    response = generate_simple_response("What are your hours?", "")
    print(f"Q: What are your hours?")
    print(f"A: {response}")

if __name__ == "__main__":
    test_simple_chat() 