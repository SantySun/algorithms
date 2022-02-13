from typing import Any, List
from unittest import TestCase
import sys

sys.path.append('.')
from list import FIFOQueue
from heap import MinHeap

class Vertex:
  def __init__(self, data) -> None:
    self.data = data

  def __hash__(self) -> int:
    return hash(id(self))


class Edge:
  def __init__(self, origin, destination, cost=None) -> None:
    self.origin = origin
    self.destination = destination
    self.cost = cost
  
  def endpoints(self):
    return (self.origin, self.destination)
  
  def opposite(self, vertex):
    return self.origin if vertex is self.destination else self.destination

  def __str__(self) -> str:
    return f'{[self.origin.data]} --{self.cost if self.cost else ""}--> {[self.destination.data]}'

  def __hash__(self) -> int:
    return hash((self.origin, self.destination))


class Graph:
  def __init__(self, directed=False) -> None:
    '''
    self._outgoing: { 
      vertex_1: { vertex_2: edge_1_2, vertex_3: edge_1_3 },
      vertex_2: { vertex_1: edge_2_1, vertex_4: edge_2_4 },
      ...
    }
    '''
    self.vertices = []
    self._outgoing = {}
    self._incoming = self._outgoing if not directed else {}
  
  def is_directed(self) -> bool:
    return self._incoming is not self._outgoing
  
  def vertices_count(self) -> int:
    return len(self.vertices)
  
  def get_vertices(self):
    return self.vertices
  
  def edge_count(self):
    total = sum(len(self._outgoing[v] for v in self._outgoing))
    return total if self.is_directed() else total // 2

  def edges(self):
    result = set()
    for secondary_map in self._outgoing.values():
      result.update(secondary_map.values())
    return result
  
  def get_edge(self, origin, destination):
    return self._outgoing[origin].get(destination)
  
  def degree(self, vertex, outgoing=True):
    return len(self._outgoing[vertex]) if outgoing else len(self._incoming[vertex])
  
  def incident_edges(self, vertex, outgoing=True):
    adj = self._outgoing.get(vertex) if outgoing else self._incoming.get(vertex)
    return adj.values()
  
  def insert_vertex(self, v):
    vertex = Vertex(v)
    self.vertices.append(vertex)
    self._outgoing[vertex] = {}
    if self.is_directed():
      self._incoming[vertex] = {}
    return vertex
  
  def insert_edge(self, origin, destination, cost=None):
    edge = Edge(origin=origin, destination=destination, cost=cost)
    self._outgoing[origin][destination] = edge
    self._incoming[destination][origin] = edge

class GraphTraversal:
  @classmethod
  def DFS(self, graph: Graph, start_vertex: Vertex, sequence: List, visited_vertices=None):
    if not visited_vertices:
      visited_vertices = {}
      for v in graph.vertices():
        visited_vertices[v] = False
    if not visited_vertices[start_vertex]:
      visited_vertices[start_vertex] = True
      sequence.append(start_vertex.data)
      # get adjacent vertices
      adj_vertices = [e.opposite(start_vertex) for e in graph.incident_edges(start_vertex)]
      for v in adj_vertices:
        self.DFS(graph, v, sequence, visited_vertices)
  
  @classmethod
  def BFS(self, graph: Graph, start_vertex: Vertex):
    visited_vertices = {}
    for v in graph.vertices():
      visited_vertices[v] = False
    result = []
    queue = FIFOQueue(start_vertex)
    while len(queue) > 0:
      vertex = queue.pop()
      result.append(vertex.data)
      visited_vertices[vertex] = True
      adj_vertices = [e.opposite(vertex) for e in graph.incident_edges(vertex)]
      for v in adj_vertices:
        if not visited_vertices[v]:
          queue.append(v)
    return result


class TSP(Graph):
  def __init__(self, cords: List[Any]) -> None:
    super().__init__()
    for c in cords:
      self.insert_vertex(c)
    length = len(cords)
    for i in range(length):
      for j in range(i+1, length):
        u = self.vertices[i]
        v = self.vertices[j]
        cost = self.__calc_distance(u, v)
        self.insert_edge(u, v, cost)
        self.insert_edge(v, u, cost)

  def __calc_distance(self, u: Vertex, v: Vertex):
    return ((u.data[0] - v.data[0])**2 + (u.data[1] - v.data[1])**2)**0.5
  
  def DFS(self, start_vertex=None):
    if not start_vertex:
      start_vertex = self.vertices[0]
    paths = []
    def __DFS_helper(graph, current, visited_vertices={}, path=None, total_cost=0):
      if not visited_vertices:
        visited_vertices = {}
        for v in self.vertices:
          visited_vertices[v] = False
      if not visited_vertices[current]:
        new_visited = dict(visited_vertices)
        new_visited[current] = True
        new_path = path + " -> " + str(current.data) if path else str(current.data)
        if len([v for v in new_visited.values() if v]) == self.vertices_count():
          final_path = new_path + " -> " + str(start_vertex.data)
          final_cost = total_cost + self.get_edge(current, start_vertex).cost
          if not paths:
            paths.append((final_path, final_cost))
          elif paths[0][1] > final_cost:
            paths[0] = (final_path, final_cost)
        else:
          adj_vertices = [e.opposite(current) for e in graph.incident_edges(current)]
          for v in adj_vertices:
            __DFS_helper(graph, v, new_visited, new_path, total_cost + self.get_edge(current, v).cost)
    __DFS_helper(self, start_vertex)
    optimum_path = paths[0]
    print(f'best route is {optimum_path[0]}, and total distance is {optimum_path[1]}')
    return optimum_path


class GraphTraversalTest(TestCase):
  def setUp(self) -> None:
    self.graph = Graph()
    self.vertices = [None] + [self.graph.insert_vertex(i) for i in range(1, 16)]
    for i in range(2, 16):
      self.graph.insert_edge(self.vertices[i//2], self.vertices[i])
    return super().setUp()
  
  def test_bfs(self):
    bfs_result = GraphTraversal.BFS(self.graph, self.vertices[1])
    self.assertListEqual(bfs_result, [i for i in range(1, 16)])
  
  def test_dfs(self):
    result = []
    GraphTraversal.DFS(self.graph, self.vertices[1], result)
    self.assertListEqual(result, [1,2,4,8,9,5,10,11,3,6,12,13,7,14,15])


class PathNode:
  def __init__(self, vertex, value, path) -> None:
    self.vertex = vertex
    self.cost = value
    self.path = path
  
  def has_same_vertex(self, __o) -> bool:
    return self.vertex is __o.vertex
  
  def __gt__(self, __o) -> bool:
    return self.cost > __o.cost

  def __lt__(self, __o) -> bool:
    return self.cost < __o.cost

  def __eq__(self, __o) -> bool:
    # return self.cost == __o.cost
    return  self.vertex is __o.vertex
  
  def __le__(self, __o) -> bool:
    return self.__lt__(__o) or self.__eq__( __o)
  
  def __str__(self) -> str:
    return f'Total Cost to {self.vertex.data}: {self.cost}, path: {self.path}'
  

class Dijkstra:
  def __init__(self, graph: Graph, start: Vertex) -> None:
    self.path = ""
    self.graph = graph
    assert start in graph.get_vertices()
    self.start = start
  
  def solution(self):
    nodes = []
    path_node_map = {}
    for v in self.graph.get_vertices():
      if v is not self.start:
        n = PathNode(v, sys.maxsize, "")
      else:
        n = PathNode(v, 0, f"{v.data}")
      nodes.append(n)
      path_node_map[v] = n
    pq = MinHeap()
    pq.build_heap(nodes)

    while not pq.is_empty() > 0:
      path_node = pq.pop()
      adj_vertices = [
        e.opposite(path_node.vertex) for e in self.graph.incident_edges(path_node.vertex)
      ]
      for v in adj_vertices:
        new_cost = path_node.cost + self.graph.get_edge(path_node.vertex, v).cost
        if path_node_map[v].cost > new_cost:
          new_node = PathNode(v, new_cost, path_node.path + f" -> {v.data}")
          pq.update(path_node_map[v], new_node)
          path_node_map[v] = new_node
    
    return path_node_map

class PrimNode:
  def __init__(self, vertex: Vertex, precost, edge: Edge) -> None:
    self.vertex = vertex
    self.precost = precost
    self.edge = edge
    self.destination = edge.opposite(vertex)
  
  def __lt__(self, __o) -> bool:
    return self.precost + self.edge.cost < __o.precost + __o.edge.cost
  
  def __eq__(self, __o) -> bool:
    return self.precost + self.edge.cost == __o.precost + __o.edge.cost
  
  def __gt__(self, __o) -> bool:
    return self.precost + self.edge.cost > __o.precost + __o.edge.cost
  
  def __le__(self, __o) -> bool:
    return self.__lt__(__o) or self.__eq__(__o)
class PrimJarnik:
  def __init__(self, graph: Graph) -> None:
    self.graph = graph
  
  def solution(self, starting_index=0):
    visited_vertices = {}
    solution_edges = []
    for i, v in enumerate(self.graph.get_vertices()):
      visited_vertices[v] = False if i != starting_index else True
    pq = MinHeap()
    starting_vertex = self.graph.get_vertices()[starting_index]
    pq.build_heap([PrimNode(starting_vertex, 0, e) for e in self.graph.incident_edges(starting_vertex)])

    while not pq.is_empty():
      pn = pq.pop()
      if not visited_vertices[pn.destination]:
        visited_vertices[pn.destination] = True
        solution_edges.append(pn.edge)
        for e in self.graph.incident_edges(pn.destination):
          if not visited_vertices[e.opposite(pn.destination)]:
            pq.insert(PrimNode(pn.destination, pn.precost + pn.edge.cost, e))
        
    
    return solution_edges



def build_graph(directed):
  graph = Graph(directed=directed)
  for i in range(1, 10):
    graph.insert_vertex(i)
  
  vertices = [None, *graph.get_vertices()]
  graph.insert_edge(vertices[1], vertices[2], 2)
  graph.insert_edge(vertices[1], vertices[3], 9)
  graph.insert_edge(vertices[2], vertices[4], 5)
  graph.insert_edge(vertices[3], vertices[4], 1)
  graph.insert_edge(vertices[4], vertices[5], 4)
  graph.insert_edge(vertices[2], vertices[7], 1)
  graph.insert_edge(vertices[7], vertices[8], 7)
  graph.insert_edge(vertices[8], vertices[9], 2)
  graph.insert_edge(vertices[7], vertices[6], 3)
  graph.insert_edge(vertices[3], vertices[9], 13)
  graph.insert_edge(vertices[6], vertices[5], 4)
  graph.insert_edge(vertices[6], vertices[8], 3)

  return graph
  

if __name__ == '__main__':
  # Test TSP problem
  tsp = TSP([(0, 0), (1, 1), (1, 0), (0, 1), (2,2), (3,4), (5,6), (7,8)])
  tsp.DFS()


  # Test Dijkstra Algorithm
  G = build_graph(True)
  problem = Dijkstra(G, G.get_vertices()[0])
  solution = problem.solution()
  for v in solution.values():
    print(str(v))
  

  # Test Prim Algorithm
  G = build_graph(False)
  problem = PrimJarnik(G)
  solution = problem.solution()
  for v in solution:
    print(str(v))
