import random
import unittest

class MinHeap:
  def __init__(self) -> None:
      self.heap_list = [0]
      self.current_size = 0
  
  def build_heap(self, heap_list) -> None:
      self.current_size = len(heap_list)
      self.heap_list = [0] + heap_list[:]
      i = self.current_size // 2
      while i > 0:
        self.__perc_down(i)
        i -= 1

  def insert(self, val):
      self.heap_list.append(val)
      self.current_size += 1
      self.__perc_up(self.current_size)

  def __perc_up(self, i):
    while i // 2 > 0:
      if self.heap_list[i] < self.heap_list[ i // 2]:
        self.heap_list[i], self.heap_list[i // 2] = self.heap_list[i // 2], self.heap_list[i]
        i = i // 2
      else:
        break

  def pop(self):
    if self.current_size == 0:
      raise IndexError
    min_val = self.heap_list[1]
    self.heap_list[1] = self.heap_list[self.current_size]
    self.heap_list.pop()
    self.current_size -= 1
    self.__perc_down(1)
    return min_val
  
  def update(self, node, new_node) -> None:
    i = 0
    for index in range(1, self.current_size + 1):
      if self.heap_list[index] == node:
        i = index
    if i == 0:
      raise Exception(message="Cannot find node")
    self.heap_list[i] = new_node
    self.__perc_up(i)
  
  def is_empty(self) -> bool:
    return self.current_size == 0

  def __perc_down(self, i):
    while i * 2 <= self.current_size:
      min_child = self.__min_child(i)
      if self.heap_list[i] > self.heap_list[min_child]:
        self.heap_list[i], self.heap_list[min_child] = self.heap_list[min_child], self.heap_list[i]
        i = min_child
      else:
        break
  
  def __min_child(self, i):
    if i * 2 + 1 > self.current_size:
      return i * 2
    return i * 2 if self.heap_list[i * 2] <= self.heap_list[i * 2 + 1] else i * 2 + 1
  
class MinHeapTest(unittest.TestCase):
  heap_list = [i for i in range(1000)]

  def setUp(self) -> None:
    random.shuffle(self.heap_list)
    self.heap = MinHeap()
    self.heap.build_heap(self.heap_list)
    return super().setUp()
  
  def test_heap_pop(self):
    self.new_heap = MinHeap()
    with self.assertRaises(IndexError):
      self.new_heap.pop()


if __name__ == '__main__':
  unittest.main()