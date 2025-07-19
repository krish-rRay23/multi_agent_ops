class MemoryStore:
    def __init__(self):
        self._memory = {}

    def save(self, key, value):
        self._memory[key] = value

    def retrieve(self, key):
        return self._memory.get(key, None)

    def all(self):
        return self._memory

# 🔥 Add this line
memory = MemoryStore()
