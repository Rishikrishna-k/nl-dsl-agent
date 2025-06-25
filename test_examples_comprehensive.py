#!/usr/bin/env python3
"""
Comprehensive test script for DSL code generation using test examples.
Runs all example queries and compares generated DSL code with expected answers.
"""

import yaml
import re
from typing import Dict, List, Any
from app.main_workflow import run_workflow
from app.utils.example_loader import ExampleLoader
import time

def load_test_examples() -> List[Dict[str, Any]]:
    """Load test examples from the YAML file."""
    try:
        with open('examples/test_examples/example_1.0.yaml', 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('examples', [])
    except Exception as e:
        print(f"❌ Error loading test examples: {e}")
        return []

def extract_dsl_code(text: str) -> str:
    """Extract DSL code from LLM response."""
    # Look for DSL code blocks
    dsl_pattern = r'```dsl\s*\n(.*?)\n```'
    matches = re.findall(dsl_pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()
    
    # Look for RULE patterns without code blocks
    rule_pattern = r'RULE\s+\w+.*?END'
    matches = re.findall(rule_pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()
    
    return text.strip()

def normalize_dsl_code(dsl_code: str) -> str:
    """Normalize DSL code for comparison by removing extra whitespace and comments."""
    # Remove comments and extra whitespace
    lines = dsl_code.split('\n')
    normalized_lines = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            normalized_lines.append(line)
    
    return '\n'.join(normalized_lines)

def calculate_similarity(generated: str, expected: str) -> float:
    """Calculate similarity between generated and expected DSL code."""
    gen_norm = normalize_dsl_code(generated)
    exp_norm = normalize_dsl_code(expected)
    
    if gen_norm == exp_norm:
        return 1.0
    
    # Simple word-based similarity
    gen_words = set(gen_norm.split())
    exp_words = set(exp_norm.split())
    
    if not gen_words or not exp_words:
        return 0.0
    
    intersection = gen_words.intersection(exp_words)
    union = gen_words.union(exp_words)
    
    return len(intersection) / len(union)

def run_comprehensive_test():
    """Run comprehensive test on all example queries."""
    print("🧪 Comprehensive DSL Code Generation Test")
    print("=" * 60)
    
    # Load test examples
    examples = load_test_examples()
    if not examples:
        print("❌ No test examples found!")
        return
    
    print(f"📋 Loaded {len(examples)} test examples")
    print()
    
    # Test results
    results = {
        'total': len(examples),
        'successful': 0,
        'failed': 0,
        'high_similarity': 0,  # > 80% similarity
        'medium_similarity': 0,  # 50-80% similarity
        'low_similarity': 0,   # < 50% similarity
        'errors': []
    }
    
    # Run each test
    for i, example in enumerate(examples, 1):
        prompt = example.get('prompt', '')
        expected_response = example.get('response', '')
        description = example.get('description', '')
        category = example.get('category', '')
        complexity = example.get('complexity', '')
        
        print(f"🔍 Test {i}/{len(examples)}: {description}")
        print(f"   Category: {category}, Complexity: {complexity}")
        print(f"   Prompt: {prompt}")
        
        try:
            # Run the workflow
            start_time = time.time()
            result = run_workflow(prompt)
            end_time = time.time()
            
            # Extract generated DSL code
            generated_code = result.get('codegen_result', '')
            generated_dsl = extract_dsl_code(generated_code)
            
            # Extract expected DSL code
            expected_dsl = extract_dsl_code(expected_response)
            
            # Calculate similarity
            similarity = calculate_similarity(generated_dsl, expected_dsl)
            
            # Categorize result
            if similarity >= 0.8:
                results['high_similarity'] += 1
                status = "✅ HIGH"
            elif similarity >= 0.5:
                results['medium_similarity'] += 1
                status = "⚠️  MEDIUM"
            else:
                results['low_similarity'] += 1
                status = "❌ LOW"
            
            results['successful'] += 1
            
            print(f"   {status} Similarity: {similarity:.2%}")
            print(f"   ⏱️  Time: {end_time - start_time:.2f}s")
            print(f"   📝 Generated DSL:")
            print(f"   {generated_dsl}")
            print(f"   📋 Expected DSL:")
            print(f"   {expected_dsl}")
            
        except Exception as e:
            results['failed'] += 1
            error_msg = f"Test {i} failed: {str(e)}"
            results['errors'].append(error_msg)
            print(f"   ❌ Error: {str(e)}")
        
        print("-" * 60)
        print()
        
        # Add delay to avoid rate limiting
        time.sleep(1)
    
    # Print summary
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {results['total']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")
    print(f"High Similarity (>80%): {results['high_similarity']}")
    print(f"Medium Similarity (50-80%): {results['medium_similarity']}")
    print(f"Low Similarity (<50%): {results['low_similarity']}")
    
    if results['errors']:
        print("\n❌ ERRORS:")
        for error in results['errors']:
            print(f"   - {error}")
    
    # Calculate success rate
    success_rate = results['successful'] / results['total'] * 100
    high_similarity_rate = results['high_similarity'] / results['total'] * 100
    
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")
    print(f"🎯 High Quality Rate: {high_similarity_rate:.1f}%")
    
    if high_similarity_rate >= 70:
        print("🎉 EXCELLENT: System is performing very well!")
    elif high_similarity_rate >= 50:
        print("👍 GOOD: System is performing well with room for improvement")
    else:
        print("⚠️  NEEDS IMPROVEMENT: System needs optimization")

if __name__ == "__main__":
    run_comprehensive_test() 