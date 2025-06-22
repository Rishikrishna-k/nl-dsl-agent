from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging

from core.models.chat import MessageRole

# Router
router = APIRouter()
logger = logging.getLogger(__name__)


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    language: str = "classroom"
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    success: bool
    response: str
    session_id: str
    language: str
    error: Optional[str] = None


class SessionInfo(BaseModel):
    session_id: str
    language: Optional[str]
    message_count: int
    created_at: str
    last_activity: str


class LanguageInfo(BaseModel):
    name: str
    description: Optional[str] = None
    examples_count: int = 0


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    """Send a chat message and get AI response"""
    try:
        dsl_ai_service = request.app.state.dsl_ai_service
        
        # Use provided session_id or create new one
        session_id = chat_request.session_id or "default"
        
        response = await dsl_ai_service.ask_ai(
            chat_request.message,
            chat_request.language,
            session_id
        )
        
        return ChatResponse(
            success=True,
            response=response,
            session_id=session_id,
            language=chat_request.language
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/languages", response_model=List[LanguageInfo])
async def get_languages_endpoint(request: Request):
    """Get available programming languages"""
    try:
        dsl_ai_service = request.app.state.dsl_ai_service
        example_service = request.app.state.example_service
        
        languages = await dsl_ai_service.get_available_languages()
        
        language_info = []
        for lang in languages:
            examples = example_service.get_all_examples(lang)
            language_info.append(LanguageInfo(
                name=lang,
                description=f"Code generation for {lang}",
                examples_count=len(examples.prompts) if examples else 0
            ))
        
        return language_info
        
    except Exception as e:
        logger.error(f"Error getting languages: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}", response_model=SessionInfo)
async def get_session_info(request: Request, session_id: str):
    """Get information about a chat session"""
    try:
        dsl_ai_service = request.app.state.dsl_ai_service
        session_info = dsl_ai_service.get_session_info(session_id)
        
        if not session_info:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return SessionInfo(**session_info)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions/{session_id}")
async def delete_session(request: Request, session_id: str):
    """Delete a chat session"""
    try:
        chat_service = request.app.state.chat_service
        success = chat_service.delete_session(session_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"success": True, "message": "Session deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/examples/{language}")
async def get_examples(request: Request, language: str):
    """Get code examples for a language"""
    try:
        example_service = request.app.state.example_service
        examples = example_service.get_all_examples(language)
        
        if not examples:
            raise HTTPException(status_code=404, detail=f"No examples found for {language}")
        
        return {
            "language": language,
            "examples": [
                {
                    "prompt": example.prompt,
                    "additional_details": example.additional_details,
                    "response": example.response
                }
                for example in examples.prompts
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting examples: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/grammars/{language}")
async def get_grammar(request: Request, language: str):
    """Get grammar for a language"""
    try:
        grammar_service = request.app.state.grammar_service
        grammar = await grammar_service.get_grammar(language)
        
        if not grammar:
            raise HTTPException(status_code=404, detail=f"No grammar found for {language}")
        
        return {
            "language": language,
            "grammar": grammar
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting grammar: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate")
async def validate_code(request: Request):
    """Validate code using grammar"""
    try:
        body = await request.json()
        code = body.get("code", "")
        language = body.get("language", "classroom")
        
        grammar_service = request.app.state.grammar_service
        validation_result = grammar_service.validate_code_with_grammar(code, language)
        
        return {
            "success": True,
            "is_valid": validation_result["is_valid"],
            "errors": validation_result.get("errors", [])
        }
        
    except Exception as e:
        logger.error(f"Error validating code: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats(request: Request):
    """Get application statistics"""
    try:
        chat_service = request.app.state.chat_service
        example_service = request.app.state.example_service
        grammar_service = request.app.state.grammar_service
        
        return {
            "active_sessions": chat_service.get_session_count(),
            "available_languages": len(example_service.get_available_languages()),
            "available_grammars": len(grammar_service.get_available_grammars()),
            "total_examples": sum(
                len(examples.prompts) if examples else 0
                for examples in [example_service.get_all_examples(lang) 
                               for lang in example_service.get_available_languages()]
            )
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 