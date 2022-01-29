import random
import unittest
import sys

sys.path.append('.')

from list import Stack, FIFOQueue
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
  
  def random_populate(self, val):
    action = random.choice(['left', 'right'])
    if action == 'left':
      if self.left:
        self.left.random_populate(val)
      else:
        self.insert_left(val)
    else:
      if self.right:
        self.right.random_populate(val)
      else:
        self.insert_right(val)


class TreeSearch:
  def __init__(self, t) -> None:
    self.target = t
    self.path = 'root'

  def DFS_recursive(self, tree: BinaryTree) -> str:
    def _recursive_helper(tree, path=self.path):
      if tree.val == self.target:
        return path
      if tree.left:
        left_result = _recursive_helper(tree.left, path + f' -LEFT-> [{tree.left.val}]')
        if left_result: 
          return left_result
      if tree.right:
        return _recursive_helper(tree.right, path + f' -RIGHT-> [{tree.right.val}]')
    return _recursive_helper(tree)
      

  def DFS_iterative(self, tree: BinaryTree):
    def _iterative_helper(tree: BinaryTree, path=self.path):
      nodes = Stack()
      nodes.put((tree, path))
      while len(nodes) > 0:
        node = nodes.pop()
        if node[0].val == self.target:
          return node[1]
        if node[0].right:
          nodes.put((node[0].right, node[1] + f' -RIGHT-> [{node[0].right.val}]'))
        if node[0].left:
          nodes.put((node[0].left, node[1] + f' -LEFT-> [{node[0].left.val}]'))
    return _iterative_helper(tree)


  def BFS_recursive(self, tree):
    pass

  def BFS_iterative(self, tree):
    def _iterative_helper(tree, path=self.path):
      queue = FIFOQueue((tree, path))
      while len(queue) > 0:
        node = queue.pop()
        if node[0].val == self.target:
          return node[1]
        if node[0].left:
          queue.append((node[0].left, node[1] + f' -LEFT-> [{node[0].left.val}]' ))
        if node[0].right:
          queue.append((node[0].right, node[1] + f' -RIGHT-> [{node[0].right.val}]'))
    return _iterative_helper(tree)


class DFSTest(unittest.TestCase):
  def setUp(self) -> None:
    self.tree = BinaryTree(0)
    node_values = [i for i in range(1, 1000)]
    random.shuffle(node_values)
    for v in node_values:
      self.tree.random_populate(v)
    return super().setUp()

  def test_DFS_search(self):
    task = TreeSearch(50)
    dfs_i = task.DFS_iterative(self.tree)
    dfs_r = task.DFS_recursive(self.tree)
    bfs_i = task.BFS_iterative(self.tree)
    self.assertEqual(dfs_i, dfs_r)
    self.assertEqual(bfs_i, dfs_r)
    

if __name__ == "__main__":
  unittest.main()