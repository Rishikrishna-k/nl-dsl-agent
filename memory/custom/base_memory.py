from abc import ABC, abstractmethod

class BaseMemory(ABC):
    @abstractmethod
    def load(self, *args, **kwargs):
        pass

    @abstractmethod
    def save(self, *args, **kwargs):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def to_data(self):
        """Return a serializable representation of the memory."""
        pass

    @classmethod
    @abstractmethod
    def from_data(cls, data):
        """Reconstruct a memory object from data."""
        pass 