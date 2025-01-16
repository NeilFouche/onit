"""
Graph class
"""

from abc import ABC, abstractmethod
import copy


class Graph(ABC):
    """
    Abstract class for a graph
    """

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
            self.predecessor = None

            for key, value in kwargs.items():
                setattr(self, key, value)

        @abstractmethod
        def distance_to(self, neighbour):
            """Returns the distance to a neighbour"""

        @abstractmethod
        def get_path_data(self, path):
            """Returns the path data"""

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

    # END OF INNER CLASS

    def __init__(self):
        self.nodes = {}

    @abstractmethod
    def add_node(self, name, schema):
        """Adds a node to the graph"""

    def get_node(self, name):
        """Returns a node from the graph"""
        return self.nodes[name]

    def get_nodes(self):
        """Returns all node names from the graph"""
        return list(self.nodes)


class SchemaGraph(Graph):
    """
    A class to represent the schema of a database as a graph
    """

    class SchemaNode(Graph.Node):
        """
        A class to represent a node in the graph
        """

        def __init__(self, name, *args, **kwargs):
            self.name = name
            self.neighbours = []
            self._neighbour_distances = {}
            self.distance = float("infinity")
            self.predecessor = None

            schema = kwargs.get("schema")
            self._foreign_keys = schema["foreign_keys"]
            self._height = schema["height"]
            self.foreign_key = None

            self._set_neighbours(data=schema["neighbours"])
            self._set_neighbour_distances(data=schema["neighbours"])

            super().__init__(
                self.name,
                self.neighbours,
                self._neighbour_distances,
                *args,
                **kwargs
            )

        def set_foreign_key(self, neighbour):
            """Sets the foreign key for the node"""
            if not self._foreign_keys:
                return

            self.foreign_key = self._foreign_keys[neighbour]

        def distance_to(self, neighbour):
            """Returns the distance to a neighbour"""
            if neighbour not in self._neighbour_distances:
                return float("infinity")

            return self._neighbour_distances[neighbour]

        def finalise(self):
            """Method to finalise the node"""
            self.set_foreign_key(self.predecessor.name)

        def get_path_data(self, path):
            """Returns the path data"""
            return {
                "table_name": self.name,
                "foreign_key": self.foreign_key,
                "height": self._height
            }

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
                self._neighbour_distances[item["name"]] = item["distance"]

        @property
        def predecessor(self):
            """Returns the predecessor of the node"""
            return self._predecessor

        @predecessor.setter
        def predecessor(self, predecessor):
            """Sets the predecessor of the node and handles predecessor references"""
            if predecessor:
                predecessor_copy = copy.deepcopy(predecessor)
                self.set_foreign_key(predecessor.name)
                self._predecessor = predecessor_copy
            else:
                self._predecessor = None

        @property
        def height(self):
            """Returns the height of the node"""
            return self._height

        @height.setter
        def height(self, height):
            """Sets the height of the node"""
            self._height = height

    # END OF INNER CLASS

    def __init__(self):
        self.nodes = {}
        super().__init__()

    def add_node(self, name, schema):
        """Adds a node to the graph"""
        self.nodes[name] = self.SchemaNode(name, schema=schema)
