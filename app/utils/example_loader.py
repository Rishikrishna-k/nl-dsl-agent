import os
import re
import yaml
import json
from typing import List, Dict, Any, Optional

EXAMPLES_BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..')
CORE_EXAMPLES_DIR = os.path.join(EXAMPLES_BASE_DIR, 'examples', 'core_examples')
RAG_EXAMPLES_DIR = os.path.join(EXAMPLES_BASE_DIR, 'examples', 'rag_examples')

class ExampleLoader:
    """
    Utility to load code examples from core_examples/ and rag_examples/ directories.
    Each file should be named example_<version>.yaml or example-<version>.yaml
    The version is extracted from the filename, e.g., example_1.0.yaml or example-1.0.yaml -> 1.0
    """
    def __init__(self, core_examples_dir: Optional[str] = None, rag_examples_dir: Optional[str] = None):
        self.core_examples_dir = core_examples_dir or CORE_EXAMPLES_DIR
        self.rag_examples_dir = rag_examples_dir or RAG_EXAMPLES_DIR
        # Cache: (version, example_type) -> List[examples]
        self._cache: Dict[tuple, List[Dict[str, Any]]] = {}
        self._load_all_examples()

    def _extract_version(self, fname: str) -> Optional[str]:
        # Match example_1.0.yaml or example-1.0.yaml
        match = re.match(r"example[_-]([\w.]+)\.(yaml|yml|json)$", fname)
        if match:
            return match.group(1)
        return None

    def _load_examples_from_dir(self, directory: str, example_type: str):
        if not os.path.exists(directory):
            return
        for fname in os.listdir(directory):
            if fname.endswith((".yaml", ".yml", ".json")):
                version = self._extract_version(fname)
                if not version:
                    continue
                path = os.path.join(directory, fname)
                with open(path, 'r', encoding='utf-8') as f:
                    if fname.endswith((".yaml", ".yml")):
                        data = yaml.safe_load(f)
                    elif fname.endswith('.json'):
                        data = json.load(f)
                    else:
                        continue
                    self._cache[(version, example_type)] = data.get('examples', [])

    def _load_all_examples(self):
        self._load_examples_from_dir(self.core_examples_dir, 'core')
        self._load_examples_from_dir(self.rag_examples_dir, 'rag')

    def get_core_examples(self, version: str) -> List[Dict[str, Any]]:
        """Return all core examples for a given version."""
        return self._cache.get((version, 'core'), [])

    # def get_rag_examples(self, version: str) -> List[Dict[str, Any]]:
    #     """Return all RAG examples for a given version."""
    #     return self._cache.get((version, 'rag'), [])

    def search_core_examples(self, version: str, keyword: str) -> List[Dict[str, Any]]:
        """Return core examples for a version where the prompt contains the keyword."""
        examples = self.get_core_examples(version)
        keyword_lower = keyword.lower()
        return [ex for ex in examples if keyword_lower in ex.get('prompt', '').lower()]

    # def search_rag_examples(self, version: str, keyword: str) -> List[Dict[str, Any]]:
    #     """Return RAG examples for a version where the prompt contains the keyword."""
    #     examples = self.get_rag_examples(version)
    #     keyword_lower = keyword.lower()
    #     return [ex for ex in examples if keyword_lower in ex.get('prompt', '').lower()]

    def get_all_core_versions(self) -> List[str]:
        """Return a list of all available core example versions."""
        return [ver for (ver, typ) in self._cache.keys() if typ == 'core']

    # def get_all_rag_versions(self) -> List[str]:
    #     """Return a list of all available RAG example versions."""
    #     return [ver for (ver, typ) in self._cache.keys() if typ == 'rag'] 