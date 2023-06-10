"""
MemoryStream and MemoryObject Classes

This file contains two main classes: MemoryObject and MemoryStream. 

The MemoryObject class represents individual memory entries in the agent's memory stream. 
Each memory object holds a natural language description of an event, the time the event 
was created, and the most recent time the event was accessed. 

The MemoryStream class serves as the agent's memory, maintaining a comprehensive record 
of the agent's experiences as a list of MemoryObject instances. The MemoryStream class 
also includes methods to add new memories and to retrieve relevant memories based on 
recency, importance, and relevance to the current situation.

The retrieval process uses a scoring system that weights memories based on their recency,
importance, and relevance. The scoring function is a weighted combination of these 
three factors, and the top-ranked memories are returned by the retrieve_memories function.

Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior.
[https://arxiv.org/abs/2304.03442]

Author: Robert Phillips
"""

from scipy.spatial.distance import cosine

from typing import List

import numpy as np



"""
instructions to implement, currently set as placeholder: the importance score is generated at the time the memory object is created by 
asking the language model to output an integer score. 
"""
class MemoryObject:
    def __init__(self, description, creation_time, importance):
        """
        Initializes a memory object.
    
        A memory object includes a description of the event (as natural language), 
        a creation timestamp, a most recent access timestamp, and an importance score.
        Parameters:
        - description (str): A natural language description of the event being remembered.
        - creation_time (float): The time the memory was created, represented as a UNIX timestamp.
        - importance (int): The importance of the memory, on a scale from 1 to 10.
        """
        self.description = description
        self.creation_time = creation_time
        self.last_access_time = creation_time
        self.importance = importance

    def access(self, current_time):
        """
        Updates the last access time of the memory object to the current time.

        Parameters:
        - current_time (float): The current time.

        This method should be called every time the memory object is accessed, 
        to ensure that the `last_access_time` attribute accurately reflects the 
        most recent time the memory was accessed.
        """
        self.last_access_time = current_time

class LanguageModel:
    def rate_importance(self, description: str) -> int:
        """
        Hypothetical function to get the importance rating of a description.
        Here we assume it's a trained model that outputs a score from 1 to 10.
        """
        # This is a placeholder for an actual implementation of a language model.
        pass

    def get_embedding(self, text: str) -> np.array:
        """
        Hypothetical function to get the embedding of a text.
        Here we assume it's a trained model that outputs a text embedding.
        """
        # This is a placeholder for an actual implementation of a language model.
        pass

class MemoryStream:
    """
    Maintains a comprehensive record of an agent's experience.

    Memory stream is a list of MemoryObject instances, each representing an event 
    perceived by the agent. The memory stream is used to plan the agent's actions and react 
    appropriately to the environment.
    """
    def __init__(self):
        """
        Initializes an empty list to store memories (i.e. memory objects) of an agent. Each experience is a memory object with a 
        description, creation timestamp, and a recent access timestamp.
        """
        self.memory_stream = []
        self.decay_factor = 0.99
        self.language_model = LanguageModel()

    def add_memory(self, memory: MemoryObject):
        """
        Adds a new memory to the memory stream.

        Parameters:
        - memory (MemoryObject): The memory to add.

        The `memory` parameter should be an instance of the MemoryObject class, 
        representing an event that the agent has perceived and wishes to remember.
        """
        self.memory_stream.append(memory)

    def calculate_recency(self, memory: MemoryObject, current_time):
        """
        Calculates the recency score of a memory object. We treat recency as an exponential decay function
        over the number of sandbox game hours since the memory was last retrieved. Our decay factor is 0.99.

        Parameters:
        - memory (MemoryObject): The memory object to calculate the recency score for.
        - current_time (float): The current time.

        Returns:
        - float: The recency score of the memory object.
        """
        hours_since_last_access = (current_time - memory.last_access_time) / 3600
        decay_factor = 0.99
        recency = decay_factor ** hours_since_last_access
        return recency
    def calculate_importance(self, memory: MemoryObject) -> float:
        """
        Returns the importance score of a memory, which has been defined at the creation time of the memory.
        The importance score is an integer between 1 and 10, where 1 signifies a mundane event and 10 signifies an extremely poignant event. 
        Use language model to output this integer score based on an input prompt.

        Parameters:
        - memory (MemoryObject): The memory whose importance score is to be returned.

        Returns:
        - importance (float): The importance score of the memory.
        """
        importance = self.language_model.rate_importance(memory.description)
        return importance
        

    def calculate_relevance(self, memory: MemoryObject, query_embedding: np.array):
        """
        Calculates the relevance of a memory to the current situation by calculating the cos similarity between the 
        memory's description embedding and the current situation's description embedding.


        Parameters:
        - memory (MemoryObject): The memory to calculate a relevance score for.
        - query_embedding (np.array): The embedding of the current situation.

        Returns:
        - A float representing the relevance score of the memory.
        """
        memory_embedding = self.language_model.get_embedding(memory.description)
        relevance = 1 - cosine(memory_embedding, query_embedding) # cosine similarity
        return relevance

    def normalize(self, value, min_value, max_value):
        """Helper function to normalize a value to the range [0, 1]."""
        return (value - min_value) / (max_value - min_value)
    
    
    def retrieve_memories(self, current_situation: str, current_situation_embedding, current_time: float) -> List[MemoryObject]:
        """
        Retrieves the most relevant memories based on the current situation.
        The relevance of a memory is calculated as a combination of the memory's recency, importance, and relevance to the current situation.

        Parameters:
        - current_situation (str): The description of the current situation.
        - current_situation_embedding (ndarray): The embedding of the current situation description.
        - current_time (float): The current time.

        Returns:
        - retrieved_memories (List[MemoryObject]): The most relevant memories.
        """
        scored_memories = []
        for memory in self.memory_stream:
            recency = self.calculate_recency(memory, current_time)
            importance = self.calculate_importance(memory)
            relevance = self.calculate_relevance(memory, current_situation_embedding)
            
            # weighted combination of scores, with all weights set to 1
            score = recency + importance + relevance
            scored_memories.append((memory, recency, importance, relevance))
            
        # Normalize the recency, importance, and relevance scores
        min_recency, max_recency = min(score[1] for score in scored_memories), max(score[1] for score in scored_memories)
        min_importance, max_importance = min(score[2] for score in scored_memories), max(score[2] for score in scored_memories)
        min_relevance, max_relevance = min(score[3] for score in scored_memories), max(score[3] for score in scored_memories)

        normalized_scores = []
        for memory, recency, importance, relevance in scored_memories:
            recency = self.normalize(recency, min_recency, max_recency)
            importance = self.normalize(importance, min_importance, max_importance)
            relevance = self.normalize(relevance, min_relevance, max_relevance)
            
            # Weighted combination of normalized scores, with all weights set to 1
            score = recency + importance + relevance
            normalized_scores.append((memory, score))
            
        # Sort memories based on their normalized scores, in descending order
        sorted_scores = sorted(normalized_scores, key=lambda x: x[1], reverse=True)

        # Assuming the context window size is 10
        retrieved_memories = [score[0] for score in sorted_scores[:10]]
        return retrieved_memories
        





