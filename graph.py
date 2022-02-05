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

  