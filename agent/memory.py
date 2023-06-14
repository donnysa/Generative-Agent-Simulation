import re
from datetime import datetime 

from util import embedding 
from completions import complete

DIGIT_PATTERN = re.compile("\d+")

class MemoryObject:
    IMPORTANCE_PROMPT = """On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following piece of memory.
Memory: {}
Rating: <fill in>"""

    def __init__(self, description: str):
        current_time = datetime.now()
        self.description = description
        self.creation_timestamp = current_time
        self.most_recent_access_timestamp = self.creation_timestamp
        self.importance = None
        self.embedding = embedding(description)
        self._rate_importance()
    
    def __repr__(self):
        return self.description

    def access(self):
        self.most_recent_access_timestamp = datetime.now()
    
    def _rate_importance(self):
        prompt = self.IMPORTANCE_PROMPT.format(self.description)
        while self.importance is None:
            try:
                completion = complete(prompt, 2)
                matches = DIGIT_PATTERN.findall(completion)
                if len(matches) != 1:
                    raise ValueError("Invalid importance rating")
                self.importance = float(matches[0])
            except Exception as e:
                # For debugging
                print(completion)
                print(f"Error rating importance: {e}")
