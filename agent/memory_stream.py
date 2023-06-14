from typing import List
from memory import MemoryObject

class MemoryStream:
    def __init__(self):
        self.memories: List[MemoryObject] = []