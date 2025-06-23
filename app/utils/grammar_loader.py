import os
import re
from typing import Dict, Optional

GRAMMARS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'grammars')

class GrammarLoader:
    """
    Utility to load ANTLR grammar files (.g4) from the grammars/ directory.
    Each file should be named grammar_<version>.g4 or grammar-<version>.g4
    The version is extracted from the filename, e.g., grammar_1.0.g4 or grammar-1.0.g4 -> 1.0
    """
    def __init__(self, grammars_dir: Optional[str] = None):
        self.grammars_dir = grammars_dir or GRAMMARS_DIR
        self._cache: Dict[str, str] = {}
        self._load_all_grammars()

    def _extract_version(self, fname: str) -> Optional[str]:
        # Match grammar_1.0.g4 or grammar-1.0.g4
        match = re.match(r"grammar[_-]([\w.]+)\.g4$", fname)
        if match:
            return match.group(1)
        return None

    def _load_all_grammars(self):
        if not os.path.exists(self.grammars_dir):
            return
        for fname in os.listdir(self.grammars_dir):
            if fname.endswith('.g4'):
                version = self._extract_version(fname)
                if not version:
                    continue
                path = os.path.join(self.grammars_dir, fname)
                with open(path, 'r', encoding='utf-8') as f:
                    self._cache[version] = f.read()

    def get_grammar(self, version: str) -> Optional[str]:
        """Return the grammar string for a given version (extracted from file name)."""
        return self._cache.get(version)

    def get_all_versions(self) -> list:
        """Return a list of all available grammar versions (from file names)."""
        return list(self._cache.keys()) 