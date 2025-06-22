import yaml
import os
from typing import Dict, Optional
from pathlib import Path

from .code_generator import CodeGeneratorAgent
from .code_validator import CodeValidatorAgent
from ..models.agent import AgentConfig


class AgentFactory:
    """Factory for creating and configuring AI agents"""
    
    def __init__(self, config_dir: str = "config/agents"):
        self.config_dir = Path(config_dir)
        self._agent_configs: Dict[str, AgentConfig] = {}
        self._load_agent_configs()
    
    def _load_agent_configs(self):
        """Load agent configurations from YAML files"""
        if not self.config_dir.exists():
            self._create_default_configs()
        
        for config_file in self.config_dir.glob("*.yaml"):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                    agent_name = config_data.get("name", config_file.stem)
                    self._agent_configs[agent_name] = AgentConfig(**config_data)
            except Exception as e:
                print(f"Error loading agent config {config_file}: {e}")
    
    def _create_default_configs(self):
        """Create default agent configurations"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Code Generator Agent
        code_gen_config = {
            "name": "code-generator",
            "description": "Generates code snippets based on user input",
            "instructions": """You are a Senior Principal Software Engineer with over ten years of experience in development.
You wrote a DSL for a rules engine and are fluent in that language.
The goal is to provide only code with the provided few shot examples and ANTLR grammar to answer the question.

You must execute the below steps in order.
1. Get indexed examples for a given input and language using the GetIndexedExamples plugin.
2. Get local examples for a given language using the GetLocalExamples plugin.

Only provide code for your response.
You're laser focused on the goal at hand.""",
            "model": "gpt-4o",
            "temperature": 0.7
        }
        
        # Code Validator Agent
        code_validator_config = {
            "name": "code-validator",
            "description": "Validates code snippets based on a provided grammar",
            "instructions": """You are a tool for validating the correctness of a custom DSL.
Provide descriptive feedback on code snippets provided by the user.
Consider the previous attempts described by the conversation history
and provide feedback to ensure previous mistakes aren't reimplemented.

If the code is incorrect, provide feedback on the error from the tools and suggest a correction.
If the code is correct, just respond with a success message that contains the string literal "::success::".""",
            "model": "gpt-4o",
            "temperature": 0.3
        }
        
        # Save configurations
        with open(self.config_dir / "code_generator.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(code_gen_config, f, default_flow_style=False)
        
        with open(self.config_dir / "code_validator.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(code_validator_config, f, default_flow_style=False)
    
    def create_code_generator(self, example_service=None, grammar_service=None) -> CodeGeneratorAgent:
        """Create a code generator agent"""
        config = self._agent_configs.get("code-generator")
        if not config:
            # Create default config if not found
            config = AgentConfig(
                name="code-generator",
                description="Generates code snippets based on user input",
                instructions="Generate code based on user prompts",
                model="gpt-4o",
                temperature=0.7
            )
        
        return CodeGeneratorAgent(config, example_service, grammar_service)
    
    def create_code_validator(self) -> CodeValidatorAgent:
        """Create a code validator agent"""
        config = self._agent_configs.get("code-validator")
        if not config:
            # Create default config if not found
            config = AgentConfig(
                name="code-validator",
                description="Validates code snippets based on a provided grammar",
                instructions="Validate code and provide feedback",
                model="gpt-4o",
                temperature=0.3
            )
        
        return CodeValidatorAgent(config)
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Get agent configuration by name"""
        return self._agent_configs.get(agent_name)
    
    def list_available_agents(self) -> list:
        """List all available agent names"""
        return list(self._agent_configs.keys()) 