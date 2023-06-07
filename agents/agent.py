"""
Contains the Agent class representing a generative agent.
This module is based on the methods described in:

Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior.
[https://arxiv.org/abs/2304.03442]

Author: Donny Sanders
"""
import os
import pygame
from agents.agent_state import IdleState
from agents.memory_stream import MemoryStream
from agents.planning import Planning
from agents.reflection import Reflection
from environment.grid import Grid


class Agent:

    def __init__(self, x, y, name):
        """
        Initialize agent with given position, name, occupation, and relationships.
        - x, y: initial position of the agent in the environment.
        - name: name of the agent.
        """
        self.x = x
        self.y = y
        self.name = name
        self.memory_stream = MemoryStream()
        self.reflection = Reflection()
        self.planning = Planning()
        self.state = IdleState()
        self.direction = "down"
        self.sprite_sheet = self.load_sprite_sheet()

    def draw(self, window, grid_size):
        """
        Draw agent in the provided window.
        - window: pygame window object where the agent needs to be drawn.
        - grid_size: size of each grid cell.
        """
        screen_x, screen_y = Grid.board_to_screen(self.x, self.y, grid_size)

        direction_index = {
            'down': 0,
            'up': 1,
            'right': 2,
            'left': 3,
        }.get(self.direction, 0)

        frame_index = self.state.current_frame if not isinstance(self.state, IdleState) else 0
        sprite = self.sprite_sheet[direction_index][frame_index]

        if sprite is not None: 
            sprite = pygame.transform.scale(sprite, (grid_size, grid_size))  # Scale the sprite
            window.blit(sprite, (screen_x, screen_y))
        else:
            raise Exception("Agent sprite is None")

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

    def change_state(self, new_state):
        """
        Changes the agent's state to the given new state.
        """
        self.state.exit(self)
        self.state = new_state
        self.state.enter(self)

    def load_sprite_sheet(self):
        """
        Load the sprite sheet for the agent.
        """
        sprite_width, sprite_height = 32, 32
        sprite_sheet = []

        # Remove spaces from the name for file parsing
        sprite_name = self.name.replace(" ", "")
        try:
            sheet = pygame.image.load(os.path.join("resources", "images", "agents", f"{sprite_name}.png"))
        except pygame.error:
            raise ValueError(f"Failed to load sprite sheet for agent '{self.name}'")

        for row in range(4):
            frames = []
            for col in range(8):
                x = col * sprite_width
                y = row * sprite_height
                sprite = sheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))
                frames.append(sprite)
            sprite_sheet.append(frames)

        return sprite_sheet