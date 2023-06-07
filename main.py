"""
Run this file to start the simulation.

This file is the main file, responsible for initializing pygame and the screen, and calling the update method
in Environment to run the simulation.
"""
import pygame
import sys
from environment.simulation import Simulation
from util.json_parser import JsonParser

def main():
    pygame.init()

    width, height, fullscreen = load_settings()
    
    if fullscreen:
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((width, height))

    # Start the simulation
    env = Simulation(width, height, screen)
    env.run()

    # Quit Pygame when the game loop in the environment is done
    pygame.quit()
    sys.exit()

def load_settings():
    settings = JsonParser.loadSettings()
    width = settings['window_width']
    height = settings['window_height']
    fullscreen = settings['fullscreen']

    return width, height, fullscreen
    

if __name__ == "__main__":
    main()