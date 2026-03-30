"""
BFS Shortest Path Algorithm for Directed Graphs with Edge Filtering

This module implements Breadth-First Search (BFS) to find the shortest path
between two nodes in a directed graph. It includes automatic filtering of edges
connected to the 'Owen' node before path finding.
"""

from collections import deque
from typing import Optional, Set, Tuple, List


def filter_edges_by_node(edges: Set[Tuple[str, str]], node: str) -> Set[Tuple[str, str]]:
    """
    Filter out edges connected to a specified node.
    
    Removes all edges where the node appears as either the source or destination.
    
    Args:
        edges: A set of directed edge tuples (source, target)
        node: The node name to filter out (including all its connected edges)
    
    Returns:
        A new set of edges with all edges connected to the specified node removed.
    
    Example:
        >>> edges = {('A', 'B'), ('Owen', 'C'), ('D', 'Owen'), ('E', 'F')}
        >>> filtered = filter_edges_by_node(edges, 'Owen')
        >>> filtered
        {('A', 'B'), ('E', 'F')}
    """
    return {(source, target) for source, target in edges 
            if source != node and target != node}


def bfs_shortest_path(
    graph: Tuple[Set[str], Set[Tuple[str, str]]],
    start: str,
    end: str
) -> Optional[List[str]]:
    """
    Find the shortest path between two nodes in a directed graph using BFS.
    
    This function performs automatic edge filtering before path finding:
    - All edges connected to the 'Owen' node are removed from the graph
    - This includes both incoming and outgoing edges from 'Owen'
    - The BFS algorithm then operates on the filtered edge set
    
    BFS guarantees the shortest path in an unweighted graph by exploring nodes
    level by level, where each level represents nodes at distance d from the start.
    
    Args:
        graph: A tuple (V, E) where:
            - V is a set of string node identifiers
            - E is a set of directed edge tuples (source, target)
        start: The starting node (must be in V)
        end: The ending node (must be in V)
    
    Returns:
        A list of nodes representing the shortest path from start to end using
        the filtered graph (with Owen and its edges removed), or None if no path exists.
    
    Raises:
        ValueError: If start or end node is not in the graph.
    
    Time Complexity: O(V + E) where V is the number of vertices and E is the number of edges
    Space Complexity: O(V) for the queue and visited set
    
    Note:
        If either the start or end node is 'Owen', the path will be None since
        Owen has no edges in the filtered graph (no incoming or outgoing edges).
    
    Example:
        >>> V = {'A', 'B', 'C', 'D', 'E'}
        >>> E = {('A', 'B'), ('B', 'C'), ('A', 'D'), ('D', 'E'), ('C', 'E')}
        >>> graph = (V, E)
        >>> bfs_shortest_path(graph, 'A', 'E')
        ['A', 'D', 'E']
    """
    vertices, edges = graph
    
    # Validate that start and end nodes exist in the graph
    if start not in vertices:
        raise ValueError(f"Start node '{start}' not found in graph vertices")
    if end not in vertices:
        raise ValueError(f"End node '{end}' not found in graph vertices")
    
    # If start and end are the same, the path is just the single node
    if start == end:
        return [start]
    
    # Filter edges: remove all edges connected to 'Owen' node
    filtered_edges = filter_edges_by_node(edges, 'Owen')
    
    # Build adjacency list from filtered edges for efficient neighbor lookup
    adjacency_list = {node: [] for node in vertices}
    for source, target in filtered_edges:
        adjacency_list[source].append(target)
    
    # Initialize BFS
    queue = deque([(start, [start])])  # (current_node, path_to_current_node)
    visited = {start}
    
    # BFS traversal
    while queue:
        current_node, path = queue.popleft()
        
        # Explore neighbors
        for neighbor in adjacency_list[current_node]:
            if neighbor == end:
                # Found the target, return the complete path
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    # No path found
    return None


if __name__ == "__main__":
    # Example 1: Simple graph with multiple paths
    print("Example 1: Simple directed graph")
    V1 = {'A', 'B', 'C', 'D', 'E'}
    E1 = {('A', 'B'), ('B', 'C'), ('A', 'D'), ('D', 'E'), ('C', 'E')}
    graph1 = (V1, E1)
    
    result1 = bfs_shortest_path(graph1, 'A', 'E')
    print(f"Graph edges: {E1}")
    print(f"Shortest path from A to E: {result1}")
    print()
    
    # Example 2: Graph where no path exists
    print("Example 2: Graph with no path between two nodes")
    V2 = {'X', 'Y', 'Z', 'W'}
    E2 = {('X', 'Y'), ('Z', 'W')}
    graph2 = (V2, E2)
    
    result2 = bfs_shortest_path(graph2, 'X', 'W')
    print(f"Graph edges: {E2}")
    print(f"Shortest path from X to W: {result2}")
    print()
    
    # Example 3: Single node path
    print("Example 3: Start and end are the same")
    V3 = {'P', 'Q', 'R'}
    E3 = {('P', 'Q'), ('Q', 'R')}
    graph3 = (V3, E3)
    
    result3 = bfs_shortest_path(graph3, 'P', 'P')
    print(f"Shortest path from P to P: {result3}")
    print()
    
    # Example 4: Linear graph
    print("Example 4: Linear directed graph")
    V4 = {'1', '2', '3', '4', '5'}
    E4 = {('1', '2'), ('2', '3'), ('3', '4'), ('4', '5')}
    graph4 = (V4, E4)
    
    result4 = bfs_shortest_path(graph4, '1', '5')
    print(f"Graph edges: {E4}")
    print(f"Shortest path from 1 to 5: {result4}")
    print()
    
    # Example 5: Graph with multiple shortest paths (BFS finds one)
    print("Example 5: Graph with multiple paths of same length")
    V5 = {'S', 'A', 'B', 'C', 'T'}
    E5 = {('S', 'A'), ('S', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'T')}
    graph5 = (V5, E5)
    
    result5 = bfs_shortest_path(graph5, 'S', 'T')
    print(f"Graph edges: {E5}")
    print(f"Shortest path from S to T: {result5}")
    print()
    
    # Example 6: Edge filtering demonstration - Owen as intermediate node
    print("Example 6: Owen node filtering - Owen as intermediate node")
    V6 = {'A', 'B', 'Owen', 'D', 'E'}
    E6 = {('A', 'B'), ('B', 'Owen'), ('Owen', 'D'), ('A', 'E'), ('E', 'D')}
    graph6 = (V6, E6)
    
    print(f"Original edges: {E6}")
    filtered_E6 = filter_edges_by_node(E6, 'Owen')
    print(f"Filtered edges (Owen removed): {filtered_E6}")
    result6 = bfs_shortest_path(graph6, 'A', 'D')
    print(f"Shortest path from A to D (after Owen filtering): {result6}")
    print(f"Note: Path via Owen (A->B->Owen->D) is blocked, using alternative route")
    print()
    
    # Example 7: Edge filtering demonstration - Owen blocking path
    print("Example 7: Owen node filtering - Owen blocking the only path")
    V7 = {'Start', 'Owen', 'End'}
    E7 = {('Start', 'Owen'), ('Owen', 'End')}
    graph7 = (V7, E7)
    
    print(f"Original edges: {E7}")
    filtered_E7 = filter_edges_by_node(E7, 'Owen')
    print(f"Filtered edges (Owen removed): {filtered_E7}")
    result7 = bfs_shortest_path(graph7, 'Start', 'End')
    print(f"Shortest path from Start to End (after Owen filtering): {result7}")
    print(f"Note: No path exists after filtering Owen's edges")
    print()
    
    # Example 8: Edge filtering demonstration - Owen as source node
    print("Example 8: Owen node filtering - Owen as source node")
    V8 = {'Owen', 'X', 'Y', 'Z'}
    E8 = {('Owen', 'X'), ('Owen', 'Y'), ('X', 'Z'), ('Y', 'Z')}
    graph8 = (V8, E8)
    
    print(f"Original edges: {E8}")
    filtered_E8 = filter_edges_by_node(E8, 'Owen')
    print(f"Filtered edges (Owen removed): {filtered_E8}")
    print(f"Note: All outgoing edges from Owen are removed")
    print()
    
    # Example 9: Error handling
    print("Example 9: Error handling for invalid nodes")
    try:
        bfs_shortest_path(graph1, 'A', 'INVALID')
    except ValueError as e:
        print(f"Caught error: {e}")
