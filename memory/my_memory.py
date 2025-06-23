class MyMemory:
    """
    Modular memory interface.

    Args:
        backend: 'langchain' (default) or 'custom'.
        **kwargs: Additional config for LangChain or custom memory.
    """
    def __init__(self, backend='langchain', **kwargs):
        self.backend = backend
        if backend == 'langchain':
            from langchain.memory import ConversationBufferMemory
            self._mem = ConversationBufferMemory(**kwargs)
            self._type = 'langchain'
        elif backend == 'custom':
            from memory.custom.custom_memory import CustomMemory
            self._mem = CustomMemory(**kwargs)
            self._type = 'custom'
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def load(self, *args, **kwargs):
        if hasattr(self._mem, 'load'):
            return self._mem.load(*args, **kwargs)
        if hasattr(self._mem, 'load_memory_variables'):
            return self._mem.load_memory_variables(*args, **kwargs)
        raise NotImplementedError

    def save(self, *args, **kwargs):
        if hasattr(self._mem, 'save'):
            return self._mem.save(*args, **kwargs)
        if hasattr(self._mem, 'save_context'):
            return self._mem.save_context(*args, **kwargs)
        raise NotImplementedError

    def clear(self):
        if hasattr(self._mem, 'clear'):
            return self._mem.clear()
        raise NotImplementedError

    def to_data(self):
        if hasattr(self._mem, 'to_data'):
            return self._mem.to_data()
        if hasattr(self._mem, 'chat_memory'):
            return getattr(self._mem, 'chat_memory').messages
        raise NotImplementedError

    @classmethod
    def from_data(cls, data, backend='langchain', **kwargs):
        if backend == 'langchain':
            from langchain.memory import ConversationBufferMemory
            mem = ConversationBufferMemory(**kwargs)
            mem.chat_memory.messages = data
            return cls(backend=backend, **kwargs)
        elif backend == 'custom':
            from memory.custom.custom_memory import CustomMemory
            return cls(backend=backend, data=data, **kwargs)
        else:
            raise ValueError(f"Unknown backend: {backend}")

    @property
    def lc(self):
        if self._type == 'langchain':
            return self._mem
        raise AttributeError("No LangChain memory backend.") 