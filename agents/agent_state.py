"""
Module containing a finite state machine for agents (for animation, etc.).

Author: Donny Sanders
"""
from abc import ABC, abstractmethod

class AgentState(ABC):
    """
    Abstract base class for all agent states.
    """
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.current_frame = 0

    @abstractmethod
    def enter(self):
        self.current_frame = 0

    @abstractmethod
    def execute(self, agent):
        # Cycle through frames
        self.current_frame = (self.current_frame + 1) % self.num_frames

    @abstractmethod
    def exit(self, agent):
        pass

    @abstractmethod
    def handle_event(self, agent, event):
        pass

class IdleState(AgentState):
    """
    The agent is currently idle.
    """
    def __init__(self):
        super().__init__(num_frames=1)

    def enter(self):
        pass

    def execute(self, agent):
        pass

    def exit(self, agent):
        pass

    def handle_event(self, agent, event):
        pass

class WalkingState(AgentState):
    """
    The agent is currently walking.
    """
    def __init__(self):
        super().__init__(num_frames=8)

    def enter(self):
        super().enter()

    def execute(self, agent):
        super.execute(agent)

    def exit(self, agent):
        pass

    def handle_event(self, agent, event):
        pass

class RunningState(AgentState):
    """
    The agent is currently running.
    """
    def __init__(self):
        super().__init__(num_frames=20)

    def enter(self):
        super().enter()

    def execute(self, agent):
        pass

    def exit(self, agent):
        pass

    def handle_event(self, agent, event):
        pass