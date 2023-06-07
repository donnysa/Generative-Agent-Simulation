"""
Utility class for parsing JSON files.

Author: Donny Sanders
"""
import json
import os
import environment.grid as env

class JsonParser:
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

        grid = env.Grid(grid_size, width, height)
        grid.grid = [[env.Tile(y, x, cell) for y, cell in enumerate(row)] for x, row in enumerate(raw_grid)]

        return grid
    
    @staticmethod
    def loadAgents(grid, num_agents):
        """
        Loads a list of agents from a JSON file.
        """
        pass

    @staticmethod
    def loadObjects(grid):
        """
        Loads a list of objects from a JSON file.
        """
        pass