#!/usr/bin/env python3
"""
Interactive testing for memvid agent
Run this to test your agent with custom queries
"""

import os
from memvid_agent import load_memvid_memory, get_chatgpt_response
from memvid import quick_chat

def main():
    print("🎯 Interactive Memvid Agent Tester")
    print("=" * 40)
    print("This simulates how your agent will respond to GitHub issues.")
    print("Type 'quit' to exit.\n")
    
    # Initialize memvid
    try:
        video_path, index_path = load_memvid_memory()
        print("✅ Memvid agent initialized successfully!\n")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Check for OpenAI API key
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print("🤖 ChatGPT integration enabled")
    else:
        print("⚠️  ChatGPT integration disabled (no OPENAI_API_KEY)")
    print()
    
    # Interactive loop
    while True:
        try:
            # Get user input
            print("Enter a test issue (like a GitHub issue title/description):")
            user_input = input("Issue: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not user_input:
                continue
            
            print(f"\n🔍 Processing issue: '{user_input}'")
            print("-" * 50)
            
            # Get memvid response
            print("📚 Searching knowledge base...")
            memvid_response = quick_chat(video_path, index_path, f"What information is relevant to this issue: {user_input}")
            print(f"Knowledge base context: {memvid_response}")
            
            # Get ChatGPT response if available
            if openai_key:
                print("\n🤖 Generating AI response...")
                try:
                    chatgpt_response = get_chatgpt_response(user_input, memvid_response, openai_key)
                    print(f"AI Assistant Response:")
                    print(f"{chatgpt_response}")
                except Exception as e:
                    print(f"❌ ChatGPT error: {e}")
            else:
                print("\n💡 AI Response Preview:")
                print("Set OPENAI_API_KEY to see full AI-generated responses.")
                print("The agent would combine the knowledge base context with AI to create a helpful response.")
            
            print("\n" + "=" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
