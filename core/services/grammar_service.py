import os
from typing import Optional, Dict, List, Any
from pathlib import Path
import logging

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener


class GrammarService:
    """Service for managing ANTLR grammar files and parsing"""
    
    def __init__(self, grammars_dir: str = "grammars"):
        self.grammars_dir = Path(grammars_dir)
        self._grammar_cache: Dict[str, str] = {}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._load_grammars()
    
    def _load_grammars(self):
        """Load grammar files from the grammars directory"""
        if not self.grammars_dir.exists():
            self._create_default_grammars()
        
        for grammar_file in self.grammars_dir.glob("*.g4"):
            try:
                with open(grammar_file, 'r', encoding='utf-8') as f:
                    grammar_content = f.read()
                    language = grammar_file.stem.lower()
                    self._grammar_cache[language] = grammar_content
                    self.logger.info(f"Loaded grammar for {language}")
            except Exception as e:
                self.logger.error(f"Error loading grammar {grammar_file}: {e}")
    
    def _create_default_grammars(self):
        """Create default grammar files"""
        self.grammars_dir.mkdir(parents=True, exist_ok=True)
        
        # Sample DSL Grammar
        sample_dsl_grammar = """grammar SampleDSL;

// Lexer rules
ID : [a-zA-Z]+ ;
INT : [0-9]+ ;
WS : [ \\t\\r\\n]+ -> skip ;

// Parser rules
program : statement+ ;

statement : assignment
          | printStatement
          ;

assignment : ID '=' expression ';' ;

printStatement : 'print' expression ';';

expression : ID
           | INT
           | expression '+' expression
           | expression '-' expression
           | '(' expression ')'
           ;"""
        
        # Classroom DSL Grammar
        classroom_grammar = """grammar Classroom;

// Lexer rules
PROGRAM : 'program' ;
ACTION : 'action' ;
MAIN : 'main' ;
VALUE : 'value' ;
NOTE : 'note' ;
NOTES : 'Notes' ;
TAKE : 'take' ;
ID : [a-zA-Z_][a-zA-Z0-9_]* ;
STRING : '"' .*? '"' ;
NUMBER : [0-9]+ ;
WS : [ \\t\\r\\n]+ -> skip ;

// Parser rules
program : PROGRAM ID '{' action+ '}' ;

action : ACTION MAIN '{' statement+ '}' ;

statement : assignment
          | printStatement
          ;

assignment : (VALUE | NOTE) ID '=' (NUMBER | STRING) ';' ;

printStatement : NOTES '.' TAKE '(' STRING ')' ';' ;"""
        
        # Save grammar files
        with open(self.grammars_dir / "SampleDSL.g4", 'w', encoding='utf-8') as f:
            f.write(sample_dsl_grammar)
        
        with open(self.grammars_dir / "Classroom.g4", 'w', encoding='utf-8') as f:
            f.write(classroom_grammar)
    
    async def get_grammar(self, language: str) -> Optional[str]:
        """Get grammar content for a language"""
        return self._grammar_cache.get(language.lower())
    
    def validate_code_with_grammar(self, code: str, language: str) -> Dict[str, Any]:
        """Validate code using ANTLR grammar parser"""
        grammar_content = self._grammar_cache.get(language.lower())
        if not grammar_content:
            return {
                "is_valid": False,
                "errors": [f"No grammar found for language: {language}"]
            }
        
        try:
            # This is a simplified validation - in a real implementation,
            # you would generate the parser from the grammar and use it
            errors = self._simple_grammar_validation(code, language)
            
            return {
                "is_valid": len(errors) == 0,
                "errors": errors
            }
        except Exception as e:
            return {
                "is_valid": False,
                "errors": [f"Grammar validation error: {str(e)}"]
            }
    
    def _simple_grammar_validation(self, code: str, language: str) -> List[str]:
        """Simple grammar validation without full ANTLR parsing"""
        errors = []
        
        if "classroom" in language.lower():
            # Basic Classroom DSL validation
            if "program" not in code:
                errors.append("Missing 'program' declaration")
            if "action main" not in code:
                errors.append("Missing 'action main'")
            if code.count("{") != code.count("}"):
                errors.append("Mismatched braces")
        
        elif "sampledsl" in language.lower():
            # Basic SampleDSL validation
            if ";" not in code:
                errors.append("Missing semicolons")
            if code.count("(") != code.count(")"):
                errors.append("Mismatched parentheses")
        
        # Generic validation
        if code.count("{") != code.count("}"):
            errors.append("Mismatched braces")
        if code.count("(") != code.count(")"):
            errors.append("Mismatched parentheses")
        
        return errors
    
    def get_available_grammars(self) -> List[str]:
        """Get list of available grammar languages"""
        return list(self._grammar_cache.keys())
    
    def add_grammar(self, language: str, grammar_content: str) -> bool:
        """Add a new grammar for a language"""
        try:
            self._grammar_cache[language.lower()] = grammar_content
            
            # Save to file
            grammar_file = self.grammars_dir / f"{language}.g4"
            with open(grammar_file, 'w', encoding='utf-8') as f:
                f.write(grammar_content)
            
            self.logger.info(f"Added grammar for {language}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding grammar for {language}: {e}")
            return False 