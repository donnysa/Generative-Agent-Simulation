"""
Contains the Agent class representing a generative agent.
This module is based on the methods described in:

Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior.
[https://arxiv.org/abs/2304.03442]

Author: Donny Sanders
"""
import pygame

from agent.memory_stream import MemoryStream
from agent.planning import Planning
from agent.reflection import Reflection


class Agent:
    def __init__(self, x, y, name):
        """
        Initialize agent with given position, name, occupation, and relationships.
        - x, y: initial position of the agent in the environment.
        - name: name of the agent.
        - occupation: occupation of the agent.
        - relationships: dictionary containing relationships of the agent with others.
        """
        self.x = x
        self.y = y
        self.name = name
        self.memory_stream = MemoryStream()
        self.reflection = Reflection()
        self.planning = Planning()

    def draw(self, window):
        """
        Draw agent in the provided window.
        - window: pygame window object where the agent needs to be drawn.
        """
        # pygame.draw.rect(window, AGENT_COLOR, (self.x*GRID_SIZE, self.y*GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def move(self, dx, dy, environment):
        """
        Move agent in the environment.
        - dx, dy: change in x and y coordinates.
        - environment: Environment object representing the world.
        """
        new_x = self.x + dx
        new_y = self.y + dy

        self.x = new_x
        self.y = new_y

    def interact(self, other_agent):
        """
        Define interaction between this agent and another agent.
        - other_agent: The agent with which the interaction happens.
        """
        pass

    def reflect(self):
        """
        Synthesize agent's memories.
        """
        pass

    def plan(self):
        """
        Create plan based on agent's reflection and memories.
        """
        pass

    def perform_action(self):
        """
        Perform action based on agent's plan.
        """
        pass

    def communicate(self, other_agent):
        """
        Communicate with other agents in natural language.
        - other_agent: The agent with which communication happens.
        """
        pass