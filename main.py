"""
Run this file to start the simulation.

This file is the main file, responsible for initializing pygame and the screen, and calling the update method
in Environment to run the simulation.
"""
import pygame
import sys
from environment.simulation import Simulation

def main():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))

    # Start the simulation
    env = Simulation(width, height, screen)
    env.run()

    # Quit Pygame when the game loop in the environment is done
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()