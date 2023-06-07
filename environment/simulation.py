"""
Module containing the simulation in which the agents operate.

Author: Donny Sanders
"""
import pygame
from agents.agent import Agent

from util.json_parser import JsonParser

class Simulation:
    """
    Main class representng the simulation.
    Contains grid and handles main simulation loop.
    """
    def __init__(self, width, height, screen):
        """
        Initializes the simulation.
        width, height: dimensions of the simulation.
        screen: pygame surface for drawing the simulation.
        """
        assert width > 0 and height > 0, "Simulation dimensions must be greater than 0."

        # List of objects to draw. Could be used to store agents, obstacles, etc.
        self.drawables = []
        self.agents = []
        
        self.grid = JsonParser.loadGrid(100, width, height)
        self.screen = screen

        RobertoFilipe = Agent(3, 5, "Roberto Filipe")
        self.agents.append(RobertoFilipe)
        self.drawables.append(RobertoFilipe)
        
        self.running = True

    def handle_events(self):
        """
        Handles events related to the main loop.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """
        Updates the simulation state.
        """
        pass

    def draw(self):
        """
        Draws the simulation.
        """
        self.grid.draw(self.screen)
        for drawable in self.drawables:
            drawable.draw(self.screen, self.grid.grid_size)

    def run(self):
        """
        Runs the main loop of the simulation.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()

    def resolve_agents(self):
        """
        Resolves all agent based interactions.
        """
        for agent in self.agents:
            agent.state.execute(agent)