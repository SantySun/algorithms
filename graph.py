from typing import Any, List
from unittest import TestCase, main
import sys

sys.path.append('.')
from list import FIFOQueue

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
  
  def DFS(self, start_vertex):
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
          paths.append((final_path, final_cost))
        adj_vertices = [e.opposite(current) for e in graph.incident_edges(current)]
        for v in adj_vertices:
          __DFS_helper(graph, v, new_visited, new_path, total_cost + self.get_edge(current, v).cost)
    __DFS_helper(self, start_vertex)
    paths.sort(key=lambda x: x[1])
    optimum_path = paths[0]
    print(f'best route is {optimum_path[0]}, and total distance is {optimum_path[1]}')
    return paths


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


if __name__ == '__main__':
  tsp = TSP([(0, 0), (1, 1), (1, 0), (0, 1), (2,2), (3,4), (5,6), (7,8)])
  tsp.DFS(tsp.vertices[0])