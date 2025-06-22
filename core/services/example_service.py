import yaml
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

from ..models.code import LanguageExamples, CodeExample


class ExampleService:
    """Service for managing code examples and examples"""
    
    def __init__(self, examples_dir: str = "examples"):
        self.examples_dir = Path(examples_dir)
        self._examples_cache: Dict[str, LanguageExamples] = {}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._load_examples()
    
    def _load_examples(self):
        """Load examples from YAML files"""
        if not self.examples_dir.exists():
            self._create_default_examples()
        
        for yaml_file in self.examples_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    language = data.get("language", yaml_file.stem)
                    examples = LanguageExamples(language=language)
                    
                    for prompt_data in data.get("prompts", []):
                        example = CodeExample(
                            prompt=prompt_data.get("prompt", ""),
                            additional_details=prompt_data.get("additionalDetails"),
                            response=prompt_data.get("response", ""),
                            language=language
                        )
                        examples.add_example(example)
                    
                    self._examples_cache[language] = examples
                    self.logger.info(f"Loaded {len(examples.prompts)} examples for {language}")
                    
            except Exception as e:
                self.logger.error(f"Error loading examples from {yaml_file}: {e}")
    
    def _create_default_examples(self):
        """Create default example files"""
        self.examples_dir.mkdir(parents=True, exist_ok=True)
        
        # C# examples
        csharp_examples = {
            "language": "csharp",
            "prompts": [
                {
                    "prompt": "Create a person POCO",
                    "additionalDetails": "The greeting method should take a string parameter and write a greeting to the console.",
                    "response": """class Person
{
    public string Name { get; set; }
}"""
                },
                {
                    "prompt": "Create a person with a greeting method",
                    "additionalDetails": "The greeting method should take a string parameter and write a greeting to the console.",
                    "response": """class Person
{
    public string Name { get; set; }
    public void Greeting(string name)
    {
        System.Console.WriteLine("Hello, {0}. I'm {1}! Nice to meet you!", name, Name);
    }
}"""
                }
            ]
        }
        
        # Classroom DSL examples
        classroom_examples = {
            "language": "classroom",
            "prompts": [
                {
                    "prompt": "Create a Classroom program with a main action",
                    "additionalDetails": "Initialize a value variable with 10.",
                    "response": """program ClassroomProgram {
    action main {
        value x = 10;
    }
}"""
                },
                {
                    "prompt": "Create a Classroom program that prints a message",
                    "additionalDetails": "Use Notes.take to print 'Hello World'.",
                    "response": """program ClassroomProgram {
    action main {
        Notes.take("Hello World");
    }
}"""
                }
            ]
        }
        
        # Save example files
        with open(self.examples_dir / "csharp.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(csharp_examples, f, default_flow_style=False)
        
        with open(self.examples_dir / "classroom.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(classroom_examples, f, default_flow_style=False)
    
    async def get_relevant_examples(self, language: str, message: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Get relevant examples for a given language and message"""
        examples = self._examples_cache.get(language)
        if not examples:
            return []
        
        # Simple keyword-based matching
        relevant_examples = examples.get_examples_by_prompt(message, max_results)
        
        return [
            {
                "prompt": example.prompt,
                "additional_details": example.additional_details,
                "response": example.response
            }
            for example in relevant_examples
        ]
    
    def get_all_examples(self, language: str) -> Optional[LanguageExamples]:
        """Get all examples for a language"""
        return self._examples_cache.get(language)
    
    def add_example(self, language: str, example: CodeExample) -> bool:
        """Add a new example for a language"""
        if language not in self._examples_cache:
            self._examples_cache[language] = LanguageExamples(language=language)
        
        self._examples_cache[language].add_example(example)
        
        # Save to file
        self._save_examples_to_file(language)
        return True
    
    def _save_examples_to_file(self, language: str):
        """Save examples for a language to YAML file"""
        examples = self._examples_cache.get(language)
        if not examples:
            return
        
        data = {
            "language": language,
            "prompts": [
                {
                    "prompt": example.prompt,
                    "additionalDetails": example.additional_details,
                    "response": example.response
                }
                for example in examples.prompts
            ]
        }
        
        file_path = self.examples_dir / f"{language}.yaml"
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False)
    
    def get_available_languages(self) -> List[str]:
        """Get list of languages with examples"""
        return list(self._examples_cache.keys()) 