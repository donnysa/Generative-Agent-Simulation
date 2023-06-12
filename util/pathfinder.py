"""
Module containing A* pathfinding algorithm.

Author: Donny Sanders
"""
from heapq import heappop, heappush

class Pathfinder:
    """
    Pathfinder using A* search algorithm to navigate in a grid.
    """
    def __init__(self, grid):
        """
        Initialize the Pathfinder with a grid.
        grid: Grid object
        """
        self.grid = grid

    def heuristic(self, a, b):
        """
        Calculate the Manhattan distance between two points a and b.
        """
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def get_neighbors(self, node):
        """
        Returns valid neighbors (walkable, within grid) around the node.
        """
        # Create all possible neighboring positions
        neighbors = [(node[0]-1, node[1]), (node[0]+1, node[1]), (node[0], node[1]-1), (node[0], node[1]+1)]

        # Validate neighboring positions (within grid and walkable)
        neighbors = [(x, y) for x, y in neighbors if 0 <= x < self.grid.grid_width and 0 <= y < self.grid.grid_height]
        neighbors = [(x, y) for x, y in neighbors if self.grid.get(x, y).walkable]

        return neighbors

    def reconstruct_path(self, came_from, current):
        """
        Reconstruct the path from start to end by following the came_from links.
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path = path[::-1]  # Reverse list
        return path

    def find_path(self, start, end):
        """
        Find a path from start to end using A* algorithm.
        start, end: tuples of (x, y) coordinates
        """
        open_set = [(0, start)]
        came_from = {start: None}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}

        # Main A* search loop
        while open_set:
            current = heappop(open_set)[1]
            
            if current == end:
                return self.reconstruct_path(came_from, current)
            
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                
                # If the tentative g score is less than the g score of the neighbor (or if the neighbor doesn't have a g score yet)
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end)
                    
                    # If neighbor is not in the open set, add it
                    if neighbor not in [i[1] for i in open_set]:
                        heappush(open_set, (f_score[neighbor], neighbor))

        return []  # No path was found