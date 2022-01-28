import random
import unittest
import sys

sys.path.append('.')

from sort import Sort
class BinaryTree:
  def __init__(self, val) -> None:
      self.val = val
      self.left = None
      self.right = None
  
  def get_left_child(self):
    return self.left
  
  def get_right_child(self):
    return self.right
  
  def set_root_val(self, val):
    self.val = val

  def get_root_val(self):
    return self.val
  
  def insert_left(self,val):
    if not self.left:
      self.left = BinaryTree(val)
    else:
      t = BinaryTree(val)
      t.left = self.get_left_child()
      self.left = t

  def insert_right(self, val):
    if not self.right:
      self.right = BinaryTree(val)
    else:
      t = BinaryTree(val)
      t.right = self.get_right_child()
      self.right = t


# class BTreeTest(unittest.TestCase):
#   node_values = [i for i in range(1, 17)]
  
#   def setUp(self) -> None:
#     random.shuffle(self.node_values)
#     return super().setUp()

class MinHeap:
  def __init__(self) -> None:
      self.heap_list = [0]
      self.currrent_size = 0
  
  def build_heap(self, heap_list) -> None:
      self.currrent_size = len(heap_list)
      self.heap_list = [0] + heap_list[:]
      i = self.currrent_size // 2
      while i > 0:
        self.perc_down(i)
        i -= 1

  def insert(self, val):
      self.heap_list.append(val)
      self.currrent_size += 1
      self.perc_up(self.currrent_size)

  def perc_up(self, i):
    while i // 2 > 0:
      if self.heap_list[i] < self.heap_list[ i // 2]:
        self.heap_list[i], self.heap_list[i // 2] = self.heap_list[i // 2], self.heap_list[i]
        i = i // 2
      else:
        break

  def pop(self):
    if self.currrent_size == 0:
      raise IndexError
    min_val = self.heap_list[1]
    self.heap_list[1] = self.heap_list[self.currrent_size]
    self.heap_list.pop()
    self.currrent_size -= 1
    self.perc_down(1)
    return min_val
  
  def perc_down(self, i):
    while i * 2 <= self.currrent_size:
      min_child = self.min_child(i);
      if self.heap_list[i] > self.heap_list[min_child]:
        self.heap_list[i], self.heap_list[min_child] = self.heap_list[min_child], self.heap_list[i]
        i = min_child
      else:
        break
  
  def min_child(self, i):
    if i * 2 + 1 > self.currrent_size:
      return i * 2
    return i * 2 if self.heap_list[i * 2] <= self.heap_list[i * 2 + 1] else i * 2 + 1
  
class MinHeapTest(unittest.TestCase):
  heap_list = [i for i in range(1000)]

  def setUp(self) -> None:
    random.shuffle(self.heap_list)
    self.heap = MinHeap()
    self.heap.build_heap(self.heap_list)
    return super().setUp()
  
  def test_heap_sort(self):
    sorted_list = []
    while self.heap.currrent_size > 0:
      sorted_list.append(self.heap.pop())
    Sort.merge_sort(self.heap_list)
    self.assertListEqual(sorted_list, self.heap_list)
  
  def test_heap_pop(self):
    self.new_heap = MinHeap()
    with self.assertRaises(IndexError):
      self.new_heap.pop()


if __name__ == "__main__":
  unittest.main()