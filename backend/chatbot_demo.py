import asyncio
import httpx
import json
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
WEBSITE_ID = "db32e4bb-4e43-4a35-af5c-444eeb1c6ee4"  # Your Go Glass website ID

class ChatbotDemo:
    def __init__(self):
        self.conversation_id = None
        self.backend_url = BACKEND_URL
        self.website_id = WEBSITE_ID
        
    async def send_message(self, message: str):
        """Send a message to the chatbot"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.backend_url}/api/chat/test",
                    json={
                        "message": message,
                        "website_id": self.website_id,
                        "conversation_id": self.conversation_id
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.conversation_id = data.get('conversation_id')
                    return {
                        'success': True,
                        'message': data['message'],
                        'sources': data.get('sources', []),
                        'confidence': data.get('confidence', 0.0)
                    }
                else:
                    return {
                        'success': False,
                        'error': f"Error {response.status_code}: {response.text}"
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'error': f"Exception: {e}"
            }
    
    def print_welcome(self):
        """Print welcome message"""
        print("🤖" + "="*60 + "🤖")
        print("           WELCOME TO THE GO GLASS CHATBOT DEMO")
        print("🤖" + "="*60 + "🤖")
        print()
        print("This chatbot can answer questions about Go Glass and Aluminium services.")
        print("Ask me about:")
        print("  • Aluminium windows and doors")
        print("  • Frameless glass balustrades")
        print("  • Contact information and quotes")
        print("  • Services and areas served")
        print()
        print("Type 'quit' or 'exit' to end the conversation.")
        print("Type 'help' for suggested questions.")
        print("-" * 70)
    
    def print_help(self):
        """Print help with suggested questions"""
        print("\n💡 Suggested Questions:")
        print("1. What services does Go Glass offer?")
        print("2. Do they install aluminium windows?")
        print("3. What types of doors do they sell?")
        print("4. Do they offer frameless glass balustrades?")
        print("5. What is their contact information?")
        print("6. Do they provide free quotes?")
        print("7. What areas do they serve?")
        print("8. What are their business hours?")
        print("9. Tell me about their sliding doors")
        print("10. What glass options do they offer?")
        print("-" * 70)
    
    async def run_demo(self):
        """Run the interactive chatbot demo"""
        self.print_welcome()
        
        while True:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Thanks for chatting! Goodbye!")
                    break
                
                # Check for help command
                if user_input.lower() == 'help':
                    self.print_help()
                    continue
                
                # Skip empty input
                if not user_input:
                    continue
                
                print("🤖 AI is thinking...")
                
                # Send message to chatbot
                result = await self.send_message(user_input)
                
                if result['success']:
                    print(f"\n🤖 Assistant: {result['message']}")
                    
                    # Show sources if available
                    if result['sources']:
                        print(f"\n📚 Sources: {', '.join(result['sources'])}")
                    
                    # Show confidence score
                    if result['confidence']:
                        confidence_percent = result['confidence'] * 100
                        print(f"🎯 Confidence: {confidence_percent:.1f}%")
                        
                else:
                    print(f"\n❌ Error: {result['error']}")
                    print("💡 Make sure the backend is running with: python -m uvicorn app.main:app --reload")
                
            except KeyboardInterrupt:
                print("\n\n👋 Demo interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")

async def main():
    """Main function to run the demo"""
    print("🚀 Starting Chatbot Demo...")
    
    # Check if backend is running
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BACKEND_URL}/docs", timeout=5.0)
            if response.status_code == 200:
                print("✅ Backend is running!")
            else:
                print("⚠️  Backend might not be running properly")
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Please start the backend first:")
        print("   python -m uvicorn app.main:app --reload")
        return
    
    # Run the demo
    demo = ChatbotDemo()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main()) 