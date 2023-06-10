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
from agent.agent_state import IdleState
from agent.memory_stream import MemoryStream
from agent.planning import Planning
from agent.reflection import Reflection
from environment.grid import Grid


class Agent:
    def __init__(self, x, y, name):
        """
        Initialize agent with given position, name, occupation, and relationships.
        - x, y: initial position of the agent in the environment.
        - name: name of the agent.
        """
        self.x = Grid.screen_to_board(x)
        self.y = Grid.screen_to_board(y)

        self.screen_x = x
        self.screen_y = y

        self.target_x = x
        self.target_y = y

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

    def move(self, dx, dy, environment):
        """
        Move agent in the environment.
        """
        if not self.can_move or (dx != 0 and dy != 0):
            return

        self.target_x = self.x + dx
        self.target_y = self.y + dy

        # Set direction based on movement
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
        elif dy > 0:
            self.direction = "down"
        elif dy < 0:
            self.direction = "up"

    def calculate_path(self, target_x, target_y):
        """
        Utilizes A* pathfinding algorithm to calculate the path to the given target coordinates.
        """
        assert target_x >= 0 and target_x < Grid.grid_width
        assert target_y >= 0 and target_y < Grid.grid_height

        open_nodes = [(0, (self.x, self.y))]
        came_from = {(self.x, self.y): None}
        cost_so_far = {(self.x, self.y): 0}

        while open_nodes:
            _, current = heappop(open_nodes)

            if current == (target_x, target_y):
                break

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_node = (current[0] + dx, current[1] + dy)

                if 0 <= next_node[0] < Grid.grid_width and 0 <= next_node[1] < Grid.grid_height:  # ensure within bounds
                    # Only add the next node to the path if it's walkable
                    if Grid.get(next_node[0], next_node[1]).walkable:
                        new_cost = cost_so_far[current] + 1  # assuming each step has a cost of 1
                        if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                            cost_so_far[next_node] = new_cost
                            priority = new_cost + abs(target_x - next_node[0]) + abs(target_y - next_node[1])  # heuristic
                            heappush(open_nodes, (priority, next_node))
                            came_from[next_node] = current

        # reconstruct path
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()

        # store path
        self.path = path

    def follow_path(self):
        """
        Makes the agent follow its calculated path step by step.
        """
        if self.path:
            # get the next position in the path
            next_x, next_y = self.path.pop(0)

            # calculate the direction to the next position
            dx = next_x - self.x
            dy = next_y - self.y

            # move towards the next position
            self.move(dx, dy)

    def update(self, dt):
        """
        Update the agent's position smoothly towards the target position.
        """
        # Compute the direction towards the target
        dx = self.target_x - self.screen_x
        dy = self.target_y - self.screen_y

        # Normalize the direction and scale by the speed
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        dx /= distance
        dy /= distance
        dx *= self.speed * dt
        dy *= self.speed * dt

        # Move towards the target, but don't overshoot it
        if abs(dx) > abs(self.target_x - self.screen_x):
            self.screen_x = self.target_x
        else:
            self.screen_x += dx
        if abs(dy) > abs(self.target_y - self.screen_y):
            self.screen_y = self.target_y
        else:
            self.screen_y += dy

    def draw(self, window):
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