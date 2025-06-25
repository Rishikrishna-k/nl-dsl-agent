#!/usr/bin/env python3
"""
Script to create .env file with proper UTF-8 encoding
"""

env_content = """# OpenRouter API Configuration
OPENROUTER_API_KEY=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

# LLM Model Configuration
LLM_MODEL=deepseek/deepseek-r1:free

# App Configuration
DEBUG=true
APP_NAME=DSL LangChain API
API_PORT=8003
"""

# Write .env file with UTF-8 encoding
with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print("✅ .env file created with proper UTF-8 encoding")
print("📄 File contents:")
print(env_content) 