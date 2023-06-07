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
        self.grid_width = width // grid_size
        self.grid_height = height // grid_size

        # Initialize the grid with Tile objects
        self.grid = [[Tile(x, y) for y in range(self.grid_height)] for x in range(self.grid_width)]

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

class Tile:
    """
    Model class representing a drawable tile in the grid, with a texture and walkable property.
    """
    def __init__(self, x, y, walkable=True, texture=None):
        """
        Initializes the tile.
        x, y: grid position of the tile.
        walkable: boolean indicating whether this tile can be walked on.
        texture: path to image file to use as texture.
        """
        assert isinstance(x, int) and isinstance(y, int), "Tile coordinates must be integers."
        assert isinstance(walkable, bool), "Walkable must be a boolean."
        if texture is not None:
            assert isinstance(texture, str), "Texture path must be a string."
            assert os.path.isfile(texture), "Texture file does not exist."
            
        self.x = x
        self.y = y
        self.walkable = walkable
        self.texture = pygame.image.load(texture) if texture is not None else None  # load texture from file

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