import logging
from typing import Dict, Any, List, Optional, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.context.context import Context
from app.state import WorkflowState
from app.utils.example_loader import ExampleLoader
from app.utils.prompt_util import load_prompt_from_file
from agents.langchain.simple_llm_agent import SimpleLLMAgent
from agents.langchain.code_validator_agent import CodeValidatorAgent
from app.openrouter_client import get_openrouter_api_key
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType

# ---- Logging Setup ----
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main_workflow")

# ---- Node 1: Build Context ----
def build_context_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Building context: loading examples and prompt.")
    try:
        example_loader = ExampleLoader()
        version = "1.0"  # You can make this dynamic
        core_examples = example_loader.get_core_examples(version)
        
        # Create context
        context = Context()
        for example in core_examples:
            context.add_local_example(example)  # Pass as dict, not string

        prompt_path = "agents/prompts/default_prompt.txt"
        prompt = load_prompt_from_file(prompt_path)
        if prompt:
            context.set_prompt(prompt)
        else:
            context.set_prompt("You are a helpful AI assistant.")
        
        logger.info("Context built successfully.")
        
        return {
            "user_query": state.get("user_query", ""),
            "context": context.as_dict(),
            "examples": core_examples,
            "prompt": context.prompt,
            "codegen_result": state.get("codegen_result")
        }
    except Exception as e:
        logger.error(f"Error in build_context_node: {e}", exc_info=True)
        return {
            "user_query": state.get("user_query", ""),
            "context": {},
            "examples": [],
            "prompt": f"Error: {e}",
            "codegen_result": state.get("codegen_result")
        }

# ---- Node 2: Code Generator Agent ----
def code_generator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Initializing SimpleLLMAgent for code generation.")
    try:
        llm = ChatOpenAI(
            model="deepseek/deepseek-r1:free",  # Updated to use the correct model
            temperature=0.7,
            openai_api_key=get_openrouter_api_key(),
            openai_api_base="https://openrouter.ai/api/v1"
        )
        tools = []  # No tools needed
        memory = None
        agent_type = None  # Not used for SimpleLLMAgent
        verbose = True

        agent = SimpleLLMAgent(llm=llm, tools=tools, memory=memory, agent_type=agent_type, verbose=verbose)
        logger.info("Calling agent.query with user_query, prompt, and context.")
        
        context_data = state.get("context", {})
        prompt = context_data.get("prompt", "")
        examples = context_data.get("local_examples", [])
        
        result = agent.query(
            query=state.get("user_query", ""),
            prompt=prompt,
            context=examples  # Pass examples as context
        )
        logger.info("Code generation successful.")
        
        return {
            "user_query": state.get("user_query", ""),
            "context": state.get("context", {}),
            "examples": state.get("examples", []),
            "prompt": state.get("prompt", ""),
            "codegen_result": result
        }
    except Exception as e:
        logger.error(f"Error in code_generator_node: {e}", exc_info=True)
        return {
            "user_query": state.get("user_query", ""),
            "context": state.get("context", {}),
            "examples": state.get("examples", []),
            "prompt": state.get("prompt", ""),
            "codegen_result": f"Error: {e}"
        }

# ---- (Future) Node: Validator Agent ----
# def code_validator_node(state: WorkflowState) -> WorkflowState:
#     logger.info("Initializing LangChainAgent for code validation.")
#     try:
#         llm = None  # Provide your LLM instance here
#         if llm is None:
#             raise ValueError("LLM instance must be provided for LangChainAgent.")
#         tools = []
#         memory = None
#         agent_type = None
#         verbose = True
#
#         agent = LangChainAgent(llm=llm, tools=tools, memory=memory, agent_type=agent_type, verbose=verbose)
#         logger.info("Calling agent.query for validation.")
#         result = agent.query(
#             query=state.codegen_result,  # or whatever needs validation
#             prompt=state.context.prompt,
#             context=state.context.local_examples
#         )
#         state.validation_result = result
#         logger.info("Code validation successful.")
#     except Exception as e:
#         logger.error(f"Error in code_validator_node: {e}", exc_info=True)
#         state.validation_result = f"Error: {e}"
#     return state

# ---- Workflow Definition ----
def create_workflow() -> StateGraph:
    # Create the workflow with dictionary state
    workflow = StateGraph(dict)
    
    # Add nodes
    workflow.add_node("build_context", build_context_node)
    workflow.add_node("code_generator", code_generator_node)
    # workflow.add_node("code_validator", code_validator_node)  # for future

    # Define the flow
    workflow.set_entry_point("build_context")
    workflow.add_edge("build_context", "code_generator")
    workflow.add_edge("code_generator", END)
    # workflow.add_edge("code_validator", END)  # for future

    # Compile without checkpointer for now to avoid configuration issues
    app = workflow.compile()
    return app

# ---- Convenience Runner ----
def run_workflow(user_query: str) -> Dict[str, Any]:
    app = create_workflow()
    initial_state = {"user_query": user_query}
    result = app.invoke(initial_state)
    return result

# ---- Example Usage ----
if __name__ == "__main__":
    user_query = "Generate a Python function to add two numbers."
    result_state = run_workflow(user_query)
    print("Codegen Result:", result_state.get("codegen_result")) 