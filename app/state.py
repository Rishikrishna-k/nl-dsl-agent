from typing import Dict, Any, List, Optional
from app.context.context import Context

class WorkflowState:
    def __init__(
        self,
        user_query: str = "",
        context: Optional[Context] = None,
        examples: Optional[List[Dict]] = None,
        prompt: Optional[str] = None,
        codegen_result: Optional[str] = None,
    ):
        self.user_query = user_query
        self.context = context or Context()
        self.examples = examples or []
        self.prompt = prompt or ""
        self.codegen_result = codegen_result

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_query": self.user_query,
            "context": self.context.as_dict() if self.context else {},
            "examples": self.examples,
            "prompt": self.prompt,
            "codegen_result": self.codegen_result,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowState":
        context_data = data.get("context", {})
        context = Context(**context_data) if context_data else None
        return cls(
            user_query=data.get("user_query", ""),
            context=context,
            examples=data.get("examples", []),
            prompt=data.get("prompt", ""),
            codegen_result=data.get("codegen_result"),
        ) 