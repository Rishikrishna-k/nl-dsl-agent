from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import logging
from typing import Dict, Any

from core.models.chat import MessageRole

# Templates
templates = Jinja2Templates(directory="app/templates")

# Router
router = APIRouter()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
    
    async def send_message(self, session_id: str, message: str):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_text(message)

manager = ConnectionManager()
logger = logging.getLogger(__name__)


@router.get("/", response_class=HTMLResponse)
async def chat_interface(request: Request):
    """Main chat interface"""
    return templates.TemplateResponse("chat.html", {"request": request})


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket, session_id)
    logger.info(f"WebSocket connected for session: {session_id}")
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process the message
            response = await process_chat_message(session_id, message_data)
            
            # Send response back to client
            await manager.send_message(session_id, json.dumps(response))
            
    except WebSocketDisconnect:
        manager.disconnect(session_id)
        logger.info(f"WebSocket disconnected for session: {session_id}")


async def process_chat_message(session_id: str, message_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process a chat message and return response"""
    try:
        user_message = message_data.get("message", "")
        language = message_data.get("language", "classroom")
        
        # Get the DSL AI service from the application state
        # This would need to be passed in or accessed differently in a real implementation
        dsl_ai_service = None  # Placeholder
        
        if dsl_ai_service:
            response = await dsl_ai_service.ask_ai(user_message, language, session_id)
        else:
            # Placeholder response for demonstration
            response = f"Generated code for {language}: {user_message}\n\n```{language}\n// Placeholder code\n// TODO: Implement actual code generation\n```"
        
        return {
            "type": "response",
            "content": response,
            "session_id": session_id,
            "language": language
        }
        
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        return {
            "type": "error",
            "content": f"Error: {str(e)}",
            "session_id": session_id
        }


@router.post("/send")
async def send_message(request: Request):
    """Send a message via HTTP POST (fallback)"""
    try:
        body = await request.json()
        user_message = body.get("message", "")
        language = body.get("language", "classroom")
        session_id = body.get("session_id", "default")
        
        # Get the DSL AI service from the application state
        dsl_ai_service = request.app.state.dsl_ai_service
        
        response = await dsl_ai_service.ask_ai(user_message, language, session_id)
        
        return {
            "success": True,
            "response": response,
            "session_id": session_id,
            "language": language
        }
        
    except Exception as e:
        logger.error(f"Error in send_message: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/languages")
async def get_languages(request: Request):
    """Get available programming languages"""
    try:
        dsl_ai_service = request.app.state.dsl_ai_service
        languages = await dsl_ai_service.get_available_languages()
        
        return {
            "success": True,
            "languages": languages
        }
        
    except Exception as e:
        logger.error(f"Error getting languages: {e}")
        return {
            "success": False,
            "error": str(e),
            "languages": ["classroom", "csharp", "python"]  # Fallback
        } 