"""
Contains the MemoryStream class. Contains a memory stream database to store agent experiences as memory objects.
To produce context-aware responses, a retrieval function selects top-ranked memories based on their recency, importance, and relevance
to the current situation. These memories are normalized, scored, and incorporated into the agent's prompt for a more relevant
and timely response.

This module is based on the methods described in:

Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior.
[https://arxiv.org/abs/2304.03442]

Author: Donny Sanders
"""
class MemoryStream:
    def __init__(self):
        """
        Initializes an empty list to store experiences of an agent. Each experience is a dictionary with a 
        description, creation timestamp, and a recent access timestamp.
        """
        self.experiences = []

    def store_experience(self, experience):
        """
        Stores an experience of the agent. An experience is represented as a dictionary with a description, 
        creation timestamp, and recent access timestamp.

        Args:
            experience (dict): a dictionary representing an experience.
        """
        pass

    def retrieve_experience(self, current_situation):
        """
        Retrieves a subset of experiences based on the current situation of the agent. The function uses 
        relevance, recency, and importance of each experience to decide which ones to retrieve.

        Args:
            current_situation (str): the current situation of the agent.

        Returns:
            A subset of the memory stream.
        """
        pass

    def update_importance(self, experience_id, score):
        """
        Updates the importance score of a particular experience.

        Args:
            experience_id (int): the id of the experience.
            score (int): the importance score assigned by the language model.
        """
        pass