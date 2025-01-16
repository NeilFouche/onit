"""
Library of algorithms
"""
import heapq


def dijkstra(graph, start, target):
    """
    Implementation of Dijkstra's algorithm to find the shortest path between two nodes.

    Args:
        graph (Graph): The graph containing the two nodes.
        start (str): The starting node identifier.
        target (str): The target node identifier.

    Returns:
        dict: A dictionary representing the shortest path from start to the target,
        including the path data.
    """

    # Initialize the distances and predecessors
    start_node = graph.get_node(start)
    target_node = graph.get_node(target)
    start_node.cost = 0
    visited = set()

    # Initialize the priority queue and add the start node
    priority_queue = []
    heapq.heappush(priority_queue, start_node)

    # Traverse the graph
    while priority_queue:
        current_node = heapq.heappop(priority_queue)

        if current_node == target_node:
            current_node.finalise()
            break

        current_cost = current_node.cost
        visited.add(current_node.name)
        unvisited_neighbours = set(current_node.neighbours) - visited

        for neighbour_name in unvisited_neighbours:
            neighbour_node = graph.get_node(neighbour_name)
            path_cost = current_cost + \
                current_node.distance_to(neighbour_name)

            # Update the nodes if a shorter path is found
            if path_cost < neighbour_node.cost:
                neighbour_node.cost = path_cost
                neighbour_node.predecessor = current_node
                heapq.heappush(priority_queue, neighbour_node)

    # Reconstruct the path
    path = {}
    current_node = target_node
    while current_node:
        path = current_node.get_path_data(path)
        current_node = current_node.predecessor

    return path


def a_star(graph, start, target):
    """
    Implementation of A* algorithm to find the shortest path between two nodes:
    Cost, f(n) = g(n) + h(n)

    Path Cost, g(n):
        The cost of the path from the start node to the current node.

    Heuristic, h(n):
        The heuristic used is the absolute difference in height between
        the current node and the target node.

    Args:
        graph (Graph): The graph containing the two nodes.
        start (str): The starting node identifier.
        target (str): The target node identifier.

    Returns:
        dict: A dictionary representing the shortest path from start to the target,
        including the path data.
    """

    def heuristic(node, target_node):
        return abs(target_node.height - node.height)

    # Initialize the distances and predecessors
    start_node = graph.get_node(start)
    target_node = graph.get_node(target)
    start_node.cost = 0
    visited = set()

    # Initialize the priority queue and add the start node
    priority_queue = []
    heapq.heappush(priority_queue, start_node)

    # Traverse the graph
    while priority_queue:
        current_node = heapq.heappop(priority_queue)

        if current_node == target_node:
            current_node.finalise()
            break

        current_cost = current_node.cost
        visited.add(current_node.name)
        unvisited_neighbours = set(current_node.neighbours) - visited

        for neighbour_name in unvisited_neighbours:
            neighbour_node = graph.get_node(neighbour_name)
            path_cost = current_cost + \
                current_node.distance_to(neighbour_name)

            # Update the nodes if a shorter path is found
            if path_cost < neighbour_node.cost:
                neighbour_node.cost = path_cost + \
                    heuristic(neighbour_node, target_node)
                neighbour_node.predecessor = current_node
                heapq.heappush(priority_queue, neighbour_node)

    # Reconstruct the path
    path = []
    current_node = target_node
    while current_node:
        path.append(current_node.get_path_data(path))
        current_node = current_node.predecessor

    return path
