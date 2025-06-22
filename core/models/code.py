from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class CodeBlock(BaseModel):
    language: str = Field(..., description="Programming language")
    code: str = Field(..., description="Code content")
    filename: Optional[str] = Field(None, description="Optional filename")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class CodeExample(BaseModel):
    prompt: str = Field(..., description="User prompt")
    additional_details: Optional[str] = Field(None, description="Additional context")
    response: str = Field(..., description="Generated code response")
    language: str = Field(..., description="Programming language")
    rating: Optional[int] = Field(None, ge=1, le=5, description="User rating (1-5)")
    feedback: Optional[str] = Field(None, description="User feedback")


class LanguageExamples(BaseModel):
    language: str = Field(..., description="Programming language")
    prompts: List[CodeExample] = Field(default_factory=list, description="Code examples")
    
    def add_example(self, example: CodeExample) -> None:
        """Add a new code example"""
        self.prompts.append(example)
    
    def get_examples_by_prompt(self, query: str, max_results: int = 5) -> List[CodeExample]:
        """Get examples that match the query (simple keyword matching)"""
        query_lower = query.lower()
        matches = []
        
        for example in self.prompts:
            if (query_lower in example.prompt.lower() or 
                (example.additional_details and query_lower in example.additional_details.lower())):
                matches.append(example)
        
        return matches[:max_results] 