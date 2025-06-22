import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from core.agents.agent_factory import AgentFactory
from core.agents.code_generator import CodeGeneratorAgent
from core.agents.code_validator import CodeValidatorAgent
from core.models.agent import AgentConfig, AgentContext


class TestAgentFactory:
    """Test cases for AgentFactory"""
    
    def test_create_code_generator(self):
        """Test creating a code generator agent"""
        factory = AgentFactory()
        agent = factory.create_code_generator()
        
        assert isinstance(agent, CodeGeneratorAgent)
        assert agent.config.name == "code-generator"
    
    def test_create_code_validator(self):
        """Test creating a code validator agent"""
        factory = AgentFactory()
        agent = factory.create_code_validator()
        
        assert isinstance(agent, CodeValidatorAgent)
        assert agent.config.name == "code-validator"
    
    def test_get_agent_config(self):
        """Test getting agent configuration"""
        factory = AgentFactory()
        config = factory.get_agent_config("code-generator")
        
        assert config is not None
        assert config.name == "code-generator"


class TestCodeGeneratorAgent:
    """Test cases for CodeGeneratorAgent"""
    
    @pytest.fixture
    def agent(self):
        """Create a test agent"""
        config = AgentConfig(
            name="test-generator",
            description="Test generator",
            instructions="Generate test code",
            model="gpt-4o",
            temperature=0.7,
            max_tokens=None
        )
        example_service = Mock()
        grammar_service = Mock()
        return CodeGeneratorAgent(config, example_service, grammar_service)
    
    @pytest.mark.asyncio
    async def test_execute_success(self, agent):
        """Test successful code generation"""
        context = AgentContext(
            session_id="test-session",
            language="classroom",
            user_message="Create a simple program",
            chat_history=[],
            examples=None,
            grammar=None,
            max_iterations=3
        )
        
        response = await agent.execute(context)
        
        assert response.success is True
        assert "classroom" in response.content.lower()
        assert "program" in response.content.lower()
    
    @pytest.mark.asyncio
    async def test_execute_with_error(self, agent):
        """Test code generation with error"""
        # Mock the example service to raise an exception
        agent.example_service.get_relevant_examples = AsyncMock(side_effect=Exception("Test error"))
        
        context = AgentContext(
            session_id="test-session",
            language="classroom",
            user_message="Create a simple program",
            chat_history=[],
            examples=None,
            grammar=None,
            max_iterations=3
        )
        
        response = await agent.execute(context)
        
        assert response.success is False
        assert "Test error" in response.error_message


class TestCodeValidatorAgent:
    """Test cases for CodeValidatorAgent"""
    
    @pytest.fixture
    def agent(self):
        """Create a test agent"""
        config = AgentConfig(
            name="test-validator",
            description="Test validator",
            instructions="Validate test code",
            model="gpt-4o",
            temperature=0.3,
            max_tokens=None
        )
        return CodeValidatorAgent(config)
    
    @pytest.mark.asyncio
    async def test_validate_classroom_code_success(self, agent):
        """Test successful classroom code validation"""
        context = AgentContext(
            session_id="test-session",
            language="classroom",
            user_message="test",
            chat_history=[
                {"role": "assistant", "content": "program TestProgram { action main { value x = 10; } }"}
            ],
            examples=None,
            grammar=None,
            max_iterations=3
        )
        
        response = await agent.execute(context)
        
        assert response.success is True
        assert "::success::" in response.content
    
    @pytest.mark.asyncio
    async def test_validate_classroom_code_failure(self, agent):
        """Test failed classroom code validation"""
        context = AgentContext(
            session_id="test-session",
            language="classroom",
            user_message="test",
            chat_history=[
                {"role": "assistant", "content": "invalid code without program declaration"}
            ],
            examples=None,
            grammar=None,
            max_iterations=3
        )
        
        response = await agent.execute(context)
        
        assert response.success is True
        assert "Missing 'program' declaration" in response.content
    
    def test_extract_code_from_context(self, agent):
        """Test code extraction from context"""
        context = AgentContext(
            session_id="test-session",
            language="classroom",
            user_message="test",
            chat_history=[
                {"role": "assistant", "content": "```classroom\nprogram Test { action main { } }\n```"}
            ],
            examples=None,
            grammar=None,
            max_iterations=3
        )
        
        code = agent._extract_code_from_context(context)
        assert code == "program Test { action main { } }"
    
    def test_validate_classroom_code(self, agent):
        """Test classroom code validation logic"""
        valid_code = "program Test { action main { value x = 10; } }"
        invalid_code = "invalid code"
        
        # Test valid code
        result = asyncio.run(agent._validate_code(valid_code, "classroom"))
        assert result["is_valid"] is True
        
        # Test invalid code
        result = asyncio.run(agent._validate_code(invalid_code, "classroom"))
        assert result["is_valid"] is False
        assert len(result["errors"]) > 0 