import os 
import time
import pygame
from heapq import heappop, heappush
from agent_state import IdleState
from planning import Planning
from reflection import Reflection
from environment.grid import Grid


from sklearn.preprocessing import MinMaxScaler
import re
from typing import NamedTuple
from datetime import datetime
from memory_stream import MemoryStream
from memory import MemoryObject
from util import embedding, calculate_cosine_similarity

class Score(NamedTuple):
    score: float
    memory: MemoryObject

class Agent:

    RECENCY_ALPHA = 1
    IMPORTANCE_ALPHA = 1
    RELEVANCE_ALPHA = 1

    def __init__(self, x, y, name, description: str):
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

        # Iterate over memory descriptions in the provided 'description' string
        for mem_description in description.split('.'):
            # Create a new MemoryObject instance based on the memory description
            self.memory_stream.memories.append(MemoryObject(mem_description))
    
    def add_observation(self, observation: str):
        self.memory_stream.memories.append(MemoryObject(observation))


    def add_memory(self, memory: MemoryObject):
        """
        Adds a new memory to the memory stream.

        Parameters:
        - memory (MemoryObject): The memory to add.

        The `memory` parameter should be an instance of the MemoryObject class, 
        representing an event that the agent has perceived and wishes to remember.
        """
        
        self.memory_stream.memories.append(memory)

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
        hours_since_last_access = (current_time - memory.most_recent_access_timestamp) / 3600
        decay_factor = 0.99
        recency = decay_factor ** hours_since_last_access
        return recency

    def calculate_relevance(self, memory_embedding, query_embedding):
        return calculate_cosine_similarity(memory_embedding, query_embedding)

    def retrieve_memories(self, current_situation: str, top_k: int = 5):
        """
        Retrieves the most relevant memories based on the current situation.
        The relevance of a memory is calculated as a combination of the memory's recency, importance, and relevance to the current situation.

        Parameters:
            query: str, the current situation described in natural language.
            current_time: float, the current time in Unix timestamp.
            top_k: int, the number of top relevant memories to return.


        Returns:
        - retrieved_memories (List[MemoryObject]): The most relevant memories.
        """
        if not self.memory_stream:
            return []

        current_situation_embedding = embedding(current_situation)
        if current_situation_embedding is None:
            return []

        scored_memories: list[Score] = []

        for memory in self.memory_stream.memories:
            current_time = datetime.now()
            recency = MinMaxScaler(self.calculate_recency(memory, current_time), 0, 1)
            importance = MinMaxScaler(memory.importance, 0, 10)
            relevance = MinMaxScaler(self.calculate_relevance(memory.embedding, current_situation_embedding), -1, 1)

            score = self.RECENCY_ALPHA * recency + self.IMPORTANCE_ALPHA * importance + self.RELEVANCE_ALPHA * relevance
            scored_memories.append(Score(score, memory))
            
        # Sort the memories by their scores and select the top k memories
        scored_memories.sort(key=lambda f: f.score, reverse=True)
        retrieved_memories = [memory[0] for memory in scored_memories[:top_k]]

        # Update the last access time of the retrieved memories
        for memory in retrieved_memories:
            memory.access(current_time)

        return retrieved_memories

            

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
