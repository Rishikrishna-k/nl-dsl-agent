#!/usr/bin/env python3
"""
Simple test script for the DSL Code Generator workflow
"""

from app.main_workflow import run_workflow

def test_workflow():
    """Test the workflow with a hardcoded medical claims query"""
    
    # Hardcoded test query
    test_query = "Create a DSL rule to validate that a patient has active insurance coverage"
    
    print("🧪 Testing DSL Code Generator Workflow")
    print("=" * 50)
    print(f"Query: {test_query}")
    print("-" * 50)
    
    try:
        # Run the workflow
        result = run_workflow(test_query)
        
        # Display results
        print("✅ Workflow completed successfully!")
        print("\n📋 Full Response:")
        print(f"User Query: {result.get('user_query', 'N/A')}")
        print(f"Examples Loaded: {len(result.get('examples', []))}")
        print(f"Prompt: {result.get('prompt', 'N/A')[:100]}...")
        
        print("\n🎯 Generated DSL Code:")
        print("-" * 30)
        codegen_result = result.get('codegen_result', 'No result generated')
        print(codegen_result)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_workflow() 