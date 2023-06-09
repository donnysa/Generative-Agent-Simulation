"""
Module containing the Grid and Tile classes, which represent a grid of drawable tiles.

Author: Donny Sanders
"""
import os
import pygame

class Grid:
    """
    Model class representing a grid of drawable tiles.
    """
    def __init__(self, grid_size, width, height):
        """
        Initializes the grid.
        grid_size: size of each grid cell.
        width, height: dimensions of the grid.
        """
        assert grid_size > 0, "Grid size must be greater than 0."
        assert width > 0 and height > 0, "Grid dimensions must be greater than 0."

        self.grid_size = grid_size
        self.grid_width = width 
        self.grid_height = height

        # # Initialize the grid with Tile objects. Right now they are all grass.
        # self.grid = [[Tile(x, y, "grass") for y in range(self.grid_height)] for x in range(self.grid_width)]

    def get(self, x, y):
        """
        Returns the tile at the given grid position.
        """
        assert 0 <= x < self.grid_width, "X coordinate is out of bounds."
        assert 0 <= y < self.grid_height, "Y coordinate is out of bounds."

        return self.grid[x][y]

    def draw(self, surface):
        """
        Draws all the tiles of the grid to the given surface.
        """
        for row in self.grid:
            for tile in row:
                tile.draw(surface, self.grid_size)

    # Utility methods

    @staticmethod
    def screen_to_board(x, y, grid_size):
        """
        Converts screen coordinates (pixels) to board coordinates (grid cells).
        x, y: screen coordinates.
        grid_size: size of each grid cell.
        Returns a tuple (board_x, board_y) representing the board coordinates.
        """
        board_x = x // grid_size
        board_y = y // grid_size
        return board_x, board_y

    @staticmethod
    def board_to_screen(board_x, board_y, grid_size):
        """
        Converts board coordinates (grid cells) to screen coordinates (pixels).
        board_x, board_y: board coordinates.
        grid_size: size of each grid cell.
        Returns a tuple (x, y) representing the screen coordinates.
        """
        x = board_x * grid_size
        y = board_y * grid_size
        return x, y

class Tile:
    """
    Model class representing a drawable tile in the grid, with a texture and walkable property.
    """

    TEXTURES = {
        0 : os.path.join("resources", "images", "grass.png"),
        1 : os.path.join("resources", "images", "dirt.png"),
    }

    def __init__(self, x, y, type, walkable=True):
        """
        Initializes the tile.
        x, y: grid position of the tile.
        type: type of the tile. Must be one of the keys in the TEXTURES dictionary.
        walkable: boolean indicating whether this tile can be walked on.
        """
        assert isinstance(x, int) and isinstance(y, int), "Tile coordinates must be integers."
        assert isinstance(walkable, bool), "Walkable must be a boolean."
        assert type in self.TEXTURES, f"Invalid tile type '{type}'. Valid types are {list(self.TEXTURES.keys())}."
            
        self.x = x
        self.y = y
        self.walkable = walkable
        try:
            self.texture = pygame.image.load(self.TEXTURES[type])
        except pygame.error:
            raise ValueError(f"Failed to load texture for tile type '{type}'")

    def draw(self, surface, size):
        """
        Draws the tile to the given surface.
        size: size of the tile.
        """
        if self.texture is not None:
            # Scale the texture to the tile's size and draw it
            texture = pygame.transform.scale(self.texture, (size, size))
            surface.blit(texture, (self.x * size, self.y * size))
        else:
            # If no texture, fill the tile with a default color (green)
            rect = pygame.Rect(self.x * size, self.y * size, size, size)
            pygame.draw.rect(surface, (0, 255, 0), rect, 1)

