class Context:
    def __init__(self, prompt=None, local_examples=None, rag_examples=None, docs=None, **kwargs):
        self.prompt = prompt
        self.local_examples = local_examples or []
        self.rag_examples = rag_examples or []
        self.docs = docs
        self.extra = kwargs  # For future extensibility

    def set_prompt(self, prompt):
        self.prompt = prompt

    def add_local_example(self, example):
        self.local_examples.append(example)

    def add_rag_example(self, example):
        self.rag_examples.append(example)

    def set_docs(self, docs):
        self.docs = docs

    def set_extra(self, key, value):
        self.extra[key] = value

    def as_dict(self):
        # Convert examples to strings if they are dicts
        local_examples_str = []
        for example in self.local_examples:
            if isinstance(example, dict):
                local_examples_str.append(str(example))
            else:
                local_examples_str.append(str(example))
        
        rag_examples_str = []
        for example in self.rag_examples:
            if isinstance(example, dict):
                rag_examples_str.append(str(example))
            else:
                rag_examples_str.append(str(example))
        
        return {
            "prompt": self.prompt or "",
            "local_examples": "\n".join(local_examples_str),
            "rag_examples": "\n".join(rag_examples_str),
            "docs": self.docs or "",
            **self.extra
        } 