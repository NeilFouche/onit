
import copy
from typing import Optional

class Node():
    """
    A class to represent a node in the graph
    """

    def __init__(self, name, **kwargs):
        self.name = name
        self.cost = float("infinity")
        self.distance = 0
        self.neighbours = []
        self.__neighbour_distances = {}
        self.__predecessor: Optional[Node] = None

        schema = kwargs.get("schema", {})
        self.__foreign_keys = schema["foreign_keys"]
        self.__height = schema["height"]
        self.foreign_key: str = ""

        self._set_neighbours(data=schema["neighbours"])
        self._set_neighbour_distances(data=schema["neighbours"])

    ###########################################################################
    #                             PUBLIC METHODS                              #
    ###########################################################################

    def set_foreign_key(self, neighbour):
        """Sets the foreign key for the node"""
        if not self.__foreign_keys:
            return

        self.foreign_key = self.__foreign_keys[neighbour]

    def distance_to(self, neighbour):
        """Returns the distance to a neighbour"""
        if neighbour not in self.__neighbour_distances:
            return float("infinity")

        return self.__neighbour_distances[neighbour]

    def finalise(self):
        """Method to finalise the node"""
        if self.predecessor is None:
            return None
        self.set_foreign_key(self.predecessor.name)

    def reset(self):
        self.cost = float("infinity")
        self.distance = 0
        self.__predecessor = None


    ###########################################################################
    #                             PRIVATE METHODS                             #
    ###########################################################################

    def _set_neighbours(self, *args, **kwargs):
        """Extracts the neighbour names from the schema and stores them as a list"""
        neighbours_config = kwargs.get("data")

        if not neighbours_config:
            return

        self.neighbours = [item["name"] for item in neighbours_config]

    def _set_neighbour_distances(self, *args, **kwargs):
        """Extracts the neighbour distances from the schema and stores them as a dictionary"""
        neighbours_config = kwargs.get("data")

        if not neighbours_config:
            return

        for item in neighbours_config:
            self.__neighbour_distances[item["name"]] = item["distance"]

    ###########################################################################
    #                               PROPERTIES                                #
    ###########################################################################

    @property
    def predecessor(self):
        """Returns the predecessor of the node"""
        return self.__predecessor

    @predecessor.setter
    def predecessor(self, predecessor):
        """Sets the predecessor of the node and handles predecessor references"""
        if predecessor:
            predecessor_copy = copy.deepcopy(predecessor)
            self.set_foreign_key(predecessor.name)
            self.__predecessor = predecessor_copy

    @property
    def height(self):
        """Returns the height of the node"""
        return self.__height

    @height.setter
    def height(self, height):
        """Sets the height of the node"""
        self.__height = height

    ###########################################################################
    #                              MAGIC METHODS                              #
    ###########################################################################

    def __str__(self):
        return f"({self.name} | {self.cost} | {self.__predecessor.name if self.__predecessor else '-'})"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.cost < other.distance

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.cost > other.distance

class Graph():
    """
    A class to represent the schema of a database as a graph
    """

    def __init__(self):
        self.nodes: dict[str, Node] = {}
        super().__init__()

    def add_node(self, name, schema):
        """Adds a node to the graph"""
        self.nodes[name] = Node(name, schema=schema)

    def get_node(self, name) -> Node:
        """Returns a node from the graph"""
        return self.nodes[name]

    def get_nodes(self) -> list[Node]:
        """Returns all node names from the graph"""
        return list(self.nodes.values())

    def reset(self):
        for node in self.nodes:
            self.nodes[node].reset()

