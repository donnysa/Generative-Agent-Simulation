"""
Utility class for parsing JSON files.

Author: Donny Sanders
"""
import json
import os
import environment.grid as env
import core.agent 

class JsonParser:

    """
    Loads game settings from a JSON file.
    """
    @staticmethod
    def loadSettings():
        """
        Loads game settings from a JSON file.
        """
        with open(os.path.join("resources", "json", "settings.json"), 'r') as f:
            settings = json.load(f)

        # TODO
        return settings

    """
    Loads a Grid object from a JSON file.
    """
    @staticmethod
    def loadGrid(grid_size, width, height):
        """
        Loads a grid from a JSON file.
        The JSON file should contain a 2D array representing the tile types.
        """
        with open(os.path.join("resources", "json", "grid.json"), 'r') as f:
            raw_grid = json.load(f)

        # Determine grid size based on window size
        num_rows = len(raw_grid)
        num_cols = len(raw_grid[0]) if num_rows > 0 else 0

        if num_rows == 0 or num_cols == 0:
            raise ValueError("Grid size cannot be 0.")

        grid_size_x = width // num_cols
        grid_size_y = height // num_rows

        grid = env.Grid(min(grid_size_x, grid_size_y), width, height)
        grid.grid = [[env.Tile(y, x, cell) for y, cell in enumerate(row)] for x, row in enumerate(raw_grid)]

        return grid
    
    @staticmethod
    def loadAgents(grid):
        """
        Loads a list of agents from a JSON file.
        """
        with open(os.path.join("resources", "json", "agents.json"), 'r') as f:
            agent_json = json.load(f)

        agents = []
            
        for agent in agent_json:
            curr = core.agent.Agent(agent["position"][0], 
                                    agent["position"][1],
                                    agent["name"],
                                    grid)
            agents.append(curr)
        
        return agents

    @staticmethod
    def loadObjects(grid):
        """
        Loads a list of objects from a JSON file.
        """
        pass