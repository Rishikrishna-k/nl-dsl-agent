import os
import yaml
from app.utils.example_loader import ExampleLoader
from app.utils.grammar_loader import GrammarLoader

# Setup dummy directories and files
os.makedirs('examples/core_examples', exist_ok=True)
os.makedirs('examples/rag_examples', exist_ok=True)
os.makedirs('grammars', exist_ok=True)

# Dummy core example
core_example = {
    'examples': [
        {'prompt': 'core prompt 1', 'response': 'core response 1'},
        {'prompt': 'core prompt 2', 'response': 'core response 2'}
    ]
}
with open('examples/core_examples/example_1.0.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(core_example, f)

# Dummy rag example
rag_example = {
    'examples': [
        {'prompt': 'rag prompt 1', 'response': 'rag response 1'},
        {'prompt': 'rag prompt 2', 'response': 'rag response 2'}
    ]
}
with open('examples/rag_examples/example_1.0.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(rag_example, f)

# Dummy grammar file
with open('grammars/grammar_1.0.g4', 'w', encoding='utf-8') as f:
    f.write('// grammar for version 1.0')

# Test ExampleLoader
example_loader = ExampleLoader()
print('Core Examples:', example_loader.get_core_examples('1.0'))
print('RAG Examples:', example_loader.get_rag_examples('1.0'))
print('Search Core:', example_loader.search_core_examples('1.0', 'core'))
print('Search RAG:', example_loader.search_rag_examples('1.0', 'rag'))
print('All Core Versions:', example_loader.get_all_core_versions())
print('All RAG Versions:', example_loader.get_all_rag_versions())

# Test GrammarLoader
grammar_loader = GrammarLoader()
print('Grammar 1.0:', grammar_loader.get_grammar('1.0'))
print('All Grammar Versions:', grammar_loader.get_all_versions()) 