"""
Graph class
"""

from abc import ABC, abstractmethod


class Node(ABC):
    """
    Abstract class for a node in the graph
    """

    @abstractmethod
    def __init__(self, name, neighbours, neighbour_distances, *args, **kwargs):
        self.name = name
        self.neighbours = neighbours
        self._neigbour_distances = neighbour_distances
        self.cost = float("infinity")
        self.height = 0
        self.predecessor: Node

        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def distance_to(self, neighbour):
        """Returns the distance to a neighbour"""

    @abstractmethod
    def _set_neighbours(self, *args, **kwargs):
        """For setting the neighbours of the node"""

    @abstractmethod
    def _set_neighbour_distances(self, *args, **kwargs):
        """For setting the neighbour distances of the node"""

    def finalise(self):
        """For logic that needs to be executed before the procedure ends"""
        return

    @property
    def height(self):
        """Returns the height of the node"""
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of the node"""
        self._height = height

    def __str__(self):
        return f"({self.name} | {self.cost} | {self.predecessor.name if self.predecessor else '-'})"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.cost < other.distance

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.cost > other.distance


class Graph(ABC):
    """
    Abstract class for a graph
    """

    def __init__(self):
        self.nodes = {}

    @abstractmethod
    def add_node(self, name, schema):
        """Adds a node to the graph"""

    @abstractmethod
    def add_nodes(self, data):
        """Adds multiple nodes to the graph"""

    @abstractmethod
    def get_node(self, name) -> Node:
        """Returns a node from the graph"""
        return self.nodes[name]

    @abstractmethod
    def get_nodes(self) -> list[Node]:
        """Returns all node names from the graph"""
        return list(self.nodes)

