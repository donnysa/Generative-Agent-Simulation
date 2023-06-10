"""
Contains the Agent class representing a generative agent.
This module is based on the methods described in:

Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior.
[https://arxiv.org/abs/2304.03442]

Author: Donny Sanders
"""
import os
import time
import pygame
from heapq import heappop, heappush
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
        # self.x = Grid.screen_to_board(x)
        # self.y = Grid.screen_to_board(y)
        screenToBoard = Grid.screen_to_board(x,y,100)
        self.x = screenToBoard[0]
        self.y = screenToBoard[1]

        self.screen_x = x
        self.screen_y = y

        self.name = name

        self.memory_stream = MemoryStream()
        self.reflection = Reflection()
        self.planning = Planning()
        self.state = IdleState()

        self.can_move = True
        self.speed = 50.0

        self.direction = "down"
        
        self.sprite_sheet = self.load_sprite_sheet()

        # Timestamp of the last update for smooth animation
        self.last_update = time.time()
        

    def move(self, dx, dy):
        """
        Move agent in the environment.
        """
        if not self.can_move or (dx != 0 and dy != 0):
            return
        
        self.x += dx
        self.y += dy

        # Set direction based on movement
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
        elif dy > 0:
            self.direction = "down"
        elif dy < 0:
            self.direction = "up"

    def update(self, dt):
        """
        Update the agent's position smoothly towards the target position.
        """
        # # Compute the direction towards the target
        # dx = self.target_x - self.screen_x
        # dy = self.target_y - self.screen_y

        # # Normalize the direction and scale by the speed
        # distance = max(1, (dx**2 + dy**2) ** 0.5)
        # dx /= distance
        # dy /= distance
        # dx *= self.speed * dt
        # dy *= self.speed * dt

        # # Move towards the target, but don't overshoot it
        # if abs(dx) > abs(self.target_x - self.screen_x):
        #     self.screen_x = self.target_x
        # else:
        #     self.screen_x += dx
        # if abs(dy) > abs(self.target_y - self.screen_y):
        #     self.screen_y = self.target_y
        # else:
        #     self.screen_y += dy

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