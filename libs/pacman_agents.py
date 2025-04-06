import random
from copy import copy

from libs import PacmanAgent
from libs.layouts import manhattan_distance


class RightTurnAgent(PacmanAgent):
    """
    A Pacman agent that turns right at every opportunity.
    """

    def get_action(self, state):
        actions = self.get_legal_actions(state)
        return actions[0]


class MonCherryAgent(PacmanAgent):
    """
    A Pacman agent that rushes the cherries. Falls back to nearest food if no cherries are left.
    """

    def get_action(self, state):
        actions = self.get_legal_actions(state)

        # If there are cherries, go for the closest one
        if state.layout.cherries:
            cherries_distance = [manhattan_distance(self.position.coordinates, cherry)
                                 for cherry in state.layout.cherries]
            cherry_position = state.layout.cherries[cherries_distance.index(min(cherries_distance))]
            target = cherry_position
        else:
            # No cherries — go for closest food
            if not state.layout.food:
                return random.choice(actions)
            food_distances = [manhattan_distance(self.position.coordinates, food)
                              for food in state.layout.food]
            food_position = state.layout.food[food_distances.index(min(food_distances))]
            target = food_position

        # Find shortest path to target (cherry or food)
        maze = copy(state.layout.maze)
        from libs.greedy_shortest_path import AStar

        shortest_path = AStar(maze).search(
            (self.position.coordinates[1], self.position.coordinates[0]),
            (target[1], target[0])
        )

        try:
            next_position = (shortest_path[1][1], shortest_path[1][0])
        except (TypeError, IndexError):
            return random.choice(actions)

        vector = (next_position[0] - self.position.coordinates[0],
                  next_position[1] - self.position.coordinates[1])

        if vector in actions:
            return vector
        else:
            return random.choice(actions)


class ReflexAgent(PacmanAgent):
    """
    Here: implement a reflex agent that chooses an action by evaluating each action available in the current state.
    """

    def get_action(self, state):
        actions = self.get_legal_actions(state)
        return random.choice(actions)
