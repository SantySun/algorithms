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


class Traversal:
  def __init__(self, tree) -> None:
    self.tree = tree
  
  def inorder_recursive(self):
    result = []
    def _inorder_helper(tree):
      if tree.left:
        _inorder_helper(tree.left)
      result.append(tree.get_root_val())
      if tree.right:
        _inorder_helper(tree.right)
    _inorder_helper(self.tree)
    return result

  def inorder_iterative(self):
    result = []
    stack = []
    cur = self.tree
    while len(stack) or cur:
      if cur:
        stack.append(cur)
        cur = cur.left
      else:
        cur = stack.pop()
        result.append(cur.val)
        cur = cur.right
    return result
  
  def preorder_recursive(self):
    result = []
    def _preorder_helper(tree):
      result.append(tree.get_root_val())
      if tree.left:
        _preorder_helper(tree.left)
      if tree.right:
        _preorder_helper(tree.right)
    _preorder_helper(self.tree)
    return result

  def preorder_iterative(self):
    result = []
    stack = [self.tree]
    while len(stack):
      cur = stack.pop()
      result.append(cur.val)
      if cur.right:
        stack.append(cur.right)
      if cur.left:
        stack.append(cur.left)
    return result

  def postorder_recursive(self):
    result = []
    def _postorder_helper(tree):
      if tree.left:
        _postorder_helper(tree.left)
      if tree.right:
        _postorder_helper(tree.right)
      result.append(tree.get_root_val())
    _postorder_helper(self.tree)
    return result
  
  def postorder_iterative(self):
    stack = [self.tree]
    result = []
    while len(stack):
      cur = stack.pop()
      result.append(cur.val)
      if cur.left:
        stack.append(cur.left)
      if cur.right:
        stack.append(cur.right)
    return result[::-1]

class DFSTest(unittest.TestCase):
  def setUp(self) -> None:
    self.tree = BinaryTree(0)
    node_values = [i for i in range(1, 1000)]
    random.shuffle(node_values)
    for v in node_values:
      self.random_populate(self.tree, v)
    return super().setUp()
  
  def random_populate(self, tree, val):
    action = random.choice(['left', 'right'])
    if action == 'left':
      if tree.left:
        self.random_populate(tree.left, val)
      else:
        tree.insert_left(val)
    else:
      if tree.right:
        self.random_populate(tree.right, val)
      else:
        tree.insert_right(val)

  def test_DFS_search(self):
    task = TreeSearch(50)
    dfs_i = task.DFS_iterative(self.tree)
    dfs_r = task.DFS_recursive(self.tree)
    bfs_i = task.BFS_iterative(self.tree)
    print("DFS_Iterative:", dfs_i)
    print("DFS_Recursive:", dfs_r)
    print("BFS_Iterative:", bfs_i)
    self.assertEqual(dfs_i, dfs_r)
    self.assertEqual(bfs_i, dfs_r)

  def test_traveral(self):
    traversal = Traversal(self.tree)
    self.assertListEqual(traversal.inorder_iterative(), traversal.inorder_recursive())
    self.assertListEqual(traversal.preorder_iterative(), traversal.preorder_recursive())
    self.assertListEqual(traversal.postorder_iterative(), traversal.postorder_recursive())
    

if __name__ == "__main__":
  unittest.main()