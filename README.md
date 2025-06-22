# Python DSL Copilot

A Python implementation of the DSL Copilot project that provides AI-powered code generation and validation for Domain-Specific Languages (DSLs).

## Overview

This project enables developers to generate code for custom Domain-Specific Languages using AI agents. It leverages Azure OpenAI, Semantic Kernel, and ANTLR for grammar parsing to provide intelligent code generation and validation.

## Features

- **AI-Powered Code Generation**: Uses OpenAI models to generate code based on user prompts
- **Grammar-Based Validation**: Validates generated code using ANTLR grammar parsers
- **Multi-Agent Architecture**: Implements a multi-agent system with code generation and validation agents
- **Web Interface**: FastAPI-based web application with real-time chat interface
- **Azure Integration**: Seamless integration with Azure services (OpenAI, AI Search, Blob Storage)
- **Fine-tuning Pipeline**: Support for creating fine-tuned models with custom training data

## Architecture

### Core Components

1. **Web Application** (`app/`): FastAPI-based web server with chat interface
2. **Core Engine** (`core/`): Multi-agent system for code generation and validation
3. **Services** (`services/`): Azure service integrations and utilities
4. **Models** (`models/`): Data models and configurations
5. **Examples** (`examples/`): Sample DSL grammars and code examples

### Agent Flow

1. **Code Generation Agent**: Generates initial code based on user prompt and context
2. **Code Validation Agent**: Validates generated code using grammar parsers
3. **Retry Logic**: Automatically retries with compiler feedback if validation fails
4. **User Feedback**: Collects user feedback for continuous improvement

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd python-dsl-copilot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Azure OpenAI and other service credentials
```

5. Run the application:
```bash
python -m uvicorn app.main:app --reload
```

## Configuration

Create a `.env` file with the following variables:

```env
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=your_openai_endpoint
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure AI Search
AZURE_SEARCH_ENDPOINT=your_search_endpoint
AZURE_SEARCH_API_KEY=your_search_key

# Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING=your_storage_connection_string

# Application Settings
LOG_LEVEL=INFO
ENVIRONMENT=development
```

## Usage

1. Start the application and navigate to `http://localhost:8000`
2. Select a language from the dropdown
3. Enter your code generation prompt
4. The system will generate code and validate it automatically
5. Provide feedback to improve future generations

## Project Structure

```
python-dsl-copilot/
├── app/                    # FastAPI web application
│   ├── main.py            # Application entry point
│   ├── routes/            # API routes
│   ├── templates/         # HTML templates
│   └── static/            # Static assets
├── core/                  # Core business logic
│   ├── agents/            # AI agents
│   ├── models/            # Data models
│   └── services/          # Core services
├── services/              # External service integrations
│   ├── azure/             # Azure service clients
│   └── openai/            # OpenAI service
├── examples/              # Sample DSLs and examples
├── grammars/              # ANTLR grammar files
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black .
isort .
```

### Type Checking
```bash
mypy .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 