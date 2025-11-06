"""
A component for modeling paths in a graph.

This component is designed to be used with the Graph class and provides methods
for creating and manipulating paths within a graph.
"""


class GraphPath:

    def __init__(self, nodes, edges):

        self._nodes = nodes
        self._edges = edges
        self._distance = None
        self._junction = None

    ###########################################################################
    #                             PUBLIC METHODS                              #
    ###########################################################################

    def get_nodes(self, properties: dict = None):
        """
        Get nodes from the path based on properties.

        Args:
            properties (dict): A dictionary of properties to filter nodes.

        Returns:
            list: A list of nodes that match the properties.
        """
        if properties is None:
            return self._nodes

        return [
            node
            for node in self._nodes
            if all(
                hasattr(node, key) and node.get(key) == value
                for key, value in properties.items()
            )
        ]

    def sub_paths(self, intermediate_nodes: list) -> list:
        """
        Get sub-paths from the main path based on intermediate nodes.

        Args:
            intermediate_nodes (list): A list of nodes to use as intermediates.

        Returns:
            list: A list of sub-paths.
        """

        paths = []
        start_index = 0
        for node in intermediate_nodes:
            current_index = self._nodes.index(node)
            nodes = self.nodes[start_index:current_index]
            edges = self.edges[start_index:current_index-1]
            path = GraphPath(nodes, edges)
            path.junction = Junction(
                label=node.label,
                node=node,
                predecessor=self._get_predecessor(index=current_index),
                successor=self._get_successor(index=current_index)
            )
            paths.append(path)
            start_index = current_index+1

        return paths

    def get_node_props(self, key: str, reverse: bool = False) -> list:
        """
        Get properties of nodes in the path.

        Args:
            key (str): The property key to retrieve.

        Returns:
            list: A list of node properties.
        """
        if reverse:
            reversed_nodes = self.nodes[::-1]
            return [node.get(key) for node in reversed_nodes]

        return [node.get(key) for node in self.nodes]

    def get_edge_props(self, key: str, reverse: bool = False) -> list:
        """
        Get properties of edges in the path.

        Args:
            key (str): The property key to retrieve.

        Returns:
            list: A list of edge properties.
        """
        if reverse:
            reversed_edges = self.edges[::-1]
            return [edge.get(key) for edge in reversed_edges]

        return [edge.get(key) for edge in self.edges]

    ###############################################################################
    #                             PRIVATE METHODS                             #
    ###############################################################################

    def _get_predecessor(self, node=None, index=None):
        """
        Get the predecessor of a node.

        Args:
            node: The node to find the predecessor for.
            index: The index of the node.

        Returns:
            The predecessor node.
        """
        if not node and not index:
            return None

        index = index or self._nodes.index(node)

        return self._nodes[index - 1] if index > 0 else None

    def _get_successor(self, node=None, index=None):
        """
        Get the successor of a node.

        Args:
            node: The node to find the successor for.
            index: The index of the node.

        Returns:
            The successor node.
        """
        if not node and not index:
            return None

        index = index or self._nodes.index(node)

        return self._nodes[index + 1] if index < len(self._nodes) - 1 else None

    ###########################################################################
    #                            GETTERS & SETTERS                            #
    ###########################################################################

    @property
    def nodes(self):
        """Get the nodes in the graph."""
        return self._nodes

    @property
    def edges(self):
        """Get the edges in the graph."""
        return self._edges

    @property
    def distance(self):
        """Get the distance of the path."""
        if self._distance is None:
            self._distance = sum(edge.distance for edge in self.edges)
        return self._distance

    @property
    def head(self):
        """Get the head of the path."""
        return self.nodes[-1] if self.nodes else None

    @property
    def tail(self):
        """Get the tail of the path."""
        return self.nodes[0] if self.nodes else None

    @property
    def junction(self):
        """Get the junction of the path."""
        return self._junction

    @junction.setter
    def junction(self, junction):
        """Set the junction of the path."""
        self._junction = junction


class Junction():
    """
    A junction in a graph path.

    This class represents a junction in a graph path, which is a point where
    multiple paths converge or diverge.
    """

    def __init__(self, label, node, predecessor=None, successor=None):
        self.label = label
        self.node = node
        self.predecessor = predecessor
        self.successor = successor
