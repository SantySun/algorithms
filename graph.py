from unittest import TestCase, main
import sys

from numpy import unicode_
sys.path.append('.')
from list import FIFOQueue

class Vertex:
  def __init__(self, data) -> None:
    self.data = data
  
  def data(self) -> any:
    return self.data

  def __hash__(self) -> int:
    return hash(id(self))


class Edge:
  def __init__(self, origin, destination, cost=None) -> None:
    self.origin = origin
    self.destination = destination
    self.cost = cost
  
  def endpoints(self):
    return (self.origin, self.destination)
  
  def cost(self):
    return self.cost
  
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
    self._outgoing = {}
    self._incoming = self._outgoing if not directed else {}
  
  def is_directed(self) -> bool:
    return self._incoming is not self._outgoing
  
  def vertices_count(self) -> int:
    return len(self._outgoing)
  
  def vertices(self):
    return self._outgoing.keys()
  
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
    self._outgoing[vertex] = {}
    if self.is_directed():
      self._incoming[vertex] = {}
    return vertex
  
  def insert_edge(self, origin, destination, cost):
    edge = Edge(origin=origin, destination=destination, cost=cost)
    self._outgoing[origin][destination] = edge
    self._incoming[destination][origin] = edge

class GraphTraversal:
  @classmethod
  def DFS(self, graph: Graph, start_vertex: Vertex, visited_vertices=None):
    if not visited_vertices:
      visited_vertices = {}
      for v in graph.vertices():
        visited_vertices[v] = False
    if not visited_vertices[start_vertex]:
      print("Visiting...", start_vertex.data)
      visited_vertices[start_vertex] = True
      # get adjacent vertices
      adj_vertices = [e.opposite(start_vertex) for e in graph.incident_edges(start_vertex)]
      for v in adj_vertices:
        self.DFS(graph, v, visited_vertices)
  
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


class GraphTest(TestCase):
  def setUp(self) -> None:
    self.graph = Graph()
    self.vertices = [None] + [self.graph.insert_vertex(i) for i in range(1, 16)]
    for i in range(2, 16):
      self.graph.insert_edge(self.vertices[i//2], self.vertices[i], None)
    return super().setUp()
  
  def test_bfs(self):
    print("BFS======================>")
    bfs_result = GraphTraversal.BFS(self.graph, self.vertices[1])
    self.assertListEqual(bfs_result, [i for i in range(1, 16)])
  
  def test_dfs(self):
    print("DFS+++++++++++++++++++++++>")
    GraphTraversal.DFS(self.graph, self.vertices[1])


if __name__ == '__main__':
  main()