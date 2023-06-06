"""
Contains the Reflection class.
This module is based on the methods described in:

Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior.
[https://arxiv.org/abs/2304.03442]

Author: Donny Sanders
"""
class Reflection:
    def __init__(self):
        """
        Initializes an empty list to store conclusions drawn from memories.
        """
        self.conclusions = []

    def synthesize_memory(self, memory_stream):
        """
        Synthesizes memories into higher-level inferences. This function is called when the sum of the 
        importance scores for the latest events exceeds a certain threshold.

        Args:
            memory_stream (list): the list of experiences from the MemoryStream class.
        """
        pass

    def draw_conclusions(self):
        """
        Draws conclusions about the agent and others based on synthesized memories.
        """
        pass

    def generate_questions(self, recent_experiences):
        """
        Generates questions that can be asked given the agent’s recent experiences.

        Args:
            recent_experiences (list): the list of recent experiences.

        Returns:
            A list of questions.
        """
        pass