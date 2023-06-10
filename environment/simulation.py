"""
Module containing the simulation in which the agents operate.

Author: Donny Sanders
"""
import time
import pygame
from agents.agent import Agent
from time import *

from util.json_parser import JsonParser

class Simulation:
    """
    Main class representng the simulation.
    Contains grid and handles main simulation loop.
    """
    debugval = False
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

        roberto_filipe = Agent(3, 5, "Roberto Filipe")
        self.agents.append(roberto_filipe)
        self.drawables.append(roberto_filipe)
        
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
        dt = time.time() - self.last_update
        self.last_update = time.time()
        # for agent in self.agents:
            # agent.update(dt)

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
        self.last_update = time.time()
        while self.running:
            self.handle_events()
            self.invertBool()
            self.update()
            self.draw()
            pygame.display.flip()

    def resolve_agents(self):
        """
        Resolves all agent based interactions.
        """
        for agent in self.agents:
            agent.state.execute(agent)
    def invertBool(self):
        """
        Inverts debug boolean
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DELETE]:
            self.debug()
        
    def debug(self):
        """
        Turns on a debug mode that allows the agent to be moved by the user.
        """
        keys = pygame.key.get_pressed()
        assert self.agents.count != 0
        debugAgent = self.agents[0]
        if keys[pygame.K_LEFT]:
            print("moving left")
            debugAgent.move(-0.1,0)
        if keys[pygame.K_RIGHT]:
            debugAgent.move(0.1,0)
        if keys[pygame.K_UP]:
            debugAgent.move(0,-0.1)
        if keys[pygame.K_DOWN]:
            debugAgent.move(0,0.1)
            
            
        