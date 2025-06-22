#!/usr/bin/env python3
"""
DSL Copilot - AI-Powered Code Generation for Domain-Specific Languages

This script runs the DSL Copilot web application.
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def main():
    """Main entry point for the application"""
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    print(f"🚀 Starting DSL Copilot on {host}:{port}")
    print(f"📝 Debug mode: {debug}")
    print(f"📊 Log level: {log_level}")
    print(f"🌐 Web interface: http://{host}:{port}")
    print(f"📚 API documentation: http://{host}:{port}/docs")
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level=log_level,
        access_log=True
    )

if __name__ == "__main__":
    main() 