from .base_memory import BaseMemory

class CustomMemory(BaseMemory):
    def __init__(self, data=None):
        self.data = data or []

    def load(self):
        return self.data

    def save(self, item):
        self.data.append(item)

    def clear(self):
        self.data = []

    def to_data(self):
        return self.data

    @classmethod
    def from_data(cls, data):
        return cls(data=data) 