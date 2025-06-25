#!/usr/bin/env python3
"""
Test script to check if .env file is being loaded properly
"""

import os
from dotenv import load_dotenv

print("🔍 Testing .env file loading...")

# Check if .env file exists
if os.path.exists('.env'):
    print("✅ .env file found")
    
    # Load .env file
    load_dotenv()
    
    # Check environment variables
    api_key = os.getenv('OPENROUTER_API_KEY')
    model = os.getenv('LLM_MODEL')
    
    print(f"   OPENROUTER_API_KEY: {'***' if api_key else 'NOT SET'}")
    print(f"   LLM_MODEL: {model}")
    
    if api_key:
        print("✅ Environment variables loaded successfully")
    else:
        print("❌ OPENROUTER_API_KEY not found in .env file")
else:
    print("❌ .env file not found")
    print("Please create a .env file with your OpenRouter API key:")
    print("OPENROUTER_API_KEY=your_api_key_here")
    print("LLM_MODEL=deepseek/deepseek-r1:free") 