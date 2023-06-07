"""
Module containing the base class for all objects.
Author: Donny Sanders
"""
import os
import pygame

class Object:
    """
    Base class for all objects in the simulation.
    """

    def __init__(self, x, y, texture=None):
        """
        Initializes the game object.
        x, y: position of the object.
        texture: path to image file to use as texture.
        """
        assert isinstance(x, int) and isinstance(y, int), "Object coordinates must be integers."
        if texture is not None:
            assert isinstance(texture, str), "Texture path must be a string."
            assert os.path.isfile(texture), "Texture file does not exist."

        self.x = x
        self.y = y
        self.texture = pygame.image.load(texture) if texture is not None else None

    def draw(self, surface, size):
        """
        Draws the game object to the given surface.
        size: size of the object.
        """
        if self.texture is not None:
            # Scale the texture to the object's size and draw it
            texture = pygame.transform.scale(self.texture, (size, size))
            surface.blit(texture, (self.x * size, self.y * size))
        else:
            # If no texture, draw a rectangle with a default color (red)
            rect = pygame.Rect(self.x * size, self.y * size, size, size)
            pygame.draw.rect(surface, (255, 0, 0), rect)