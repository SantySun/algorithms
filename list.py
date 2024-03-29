import unittest

class Stack:
  def __init__(self) -> None:
    self.length = 0
    self.elements = []
  
  def __len__(self):
    return self.length

  def put(self, obj):
    self.elements.append(obj)
    self.length = self.length + 1
  
  def read(self):
    if self.length == 0:
      return None
    return self.elements[0]
  
  def pop(self):
    if self.length == 0:
      raise Exception(message="Stack is empty, pop not allowed.")
    self.length = self.length - 1
    return self.elements.pop()

class StackTest(unittest.TestCase):
  def setUp(self) -> None:
      self.stack = Stack()
      self.nums = [i for i in range(50)]
      for i in range(30):
        self.stack.put(self.nums[i])
  
  def test_stack_put(self):
    self.assertListEqual(self.stack.elements, self.nums[:30])
  
  def test_stack_length(self):
    self.assertEqual(len(self.stack), 30)
  
  def test_pop(self):
    self.assertEqual(self.stack.pop(), 29)
    self.assertEqual(self.stack.pop(), 28)
    self.assertEqual(self.stack.pop(), 27)
    self.assertEqual(self.stack.pop(), 26)

class Node:
  def __init__(self, val) -> None:
    self.val = val
    self.next = None

  def __str__(self) -> str:
    if self.next:
      return f'{self.val} -> {self.next.val}'
  
class LinkedList:
  def __init__(self, n: any) -> None:
    node = Node(n)
    self.head = node
    self.length = 1

  def append(self, n: any) -> None:
    node = Node(n)
    current = self.head
    while current.next:
      current = current.next
    current.next = node
    self.length = self.length + 1

  def __add__(self, linked_list):
    result = LinkedList(self.head.val)
    current = self.head
    current_result_node = result.head
    while current.next:
      result.append(current.next.val)
      current = current.next
      current_result_node = current_result_node.next
    current_result_node.next = linked_list.head
    return result

  def pop(self, position=None):
    assert position == None or type(position) == int
    result = None
    if position is None:
      current = self.head
      while current.next and current.next.next:
        current = current.next
      result = current.next.val
      current.next = None
    elif position >= self.length:
      raise IndexError
    else:
      if position == 0:
        result = self.head.val
        self.head = self.head.next
      else:
        current = self.head
        for _ in range(position - 1):
          current = current.next
        result = current.next.val
        current.next = current.next.next
    return result
  
  def __str__(self) -> str:
    current = self.head
    values = []
    while current:
      values.append(str(current.val))
      current = current.next
    return '->'.join(values)

class LinkedListTest(unittest.TestCase):
  def setUp(self) -> None:
    self.list_1 = LinkedList(0)   
  
  def test_append(self):
    self.list_1.append('a')
    self.list_1.append('b')
    self.list_1.append(99)
    self.assertEqual(str(self.list_1), '0->a->b->99')
  
  def test_add(self):
    l2 = LinkedList('a')
    l2.append('b')
    l2.append("c")
    self.list_1.append(1)
    self.list_1.append(2)
    self.assertEqual(str(self.list_1 + l2), '0->1->2->a->b->c')
  
  def test_pop(self):
    for i in range(1, 5):
      self.list_1.append(i)
    self.assertEqual(self.list_1.pop(), 4)
    self.assertEqual(str(self.list_1), '0->1->2->3')
    self.assertEqual(self.list_1.pop(0), 0)
    self.assertEqual(str(self.list_1), '1->2->3')
    
    with self.assertRaises(IndexError):
      self.list_1.pop(5)
    
    self.list_1.append(4)
    self.list_1.append(5)
    self.list_1.pop(2)
    self.assertEqual(str(self.list_1), '1->2->4->5')
    self.list_1.pop(3)
    self.assertEqual(str(self.list_1), '1->2->4')

class Element:
  def __init__(self, val) -> None:
    self.val = val
    self.next = None
    self.prev = None

class FIFOQueue:
  def __init__(self, n: any) -> None:
    node = Element(n)
    self.head = node
    self.tail = node
    self.length = 1

  def append(self, n: any):
    if self.length ==  0:
      self.__init__(n)
    else:
      node = Element(n)
      self.tail.next = node
      node.prev = self.tail
      self.tail = node
      self.length = self.length + 1
  
  def pop(self):
    if self.length == 0:
      raise IndexError
    popped = self.head.val
    if self.head.next:
      self.head = self.head.next
      self.head.prev = None
    else:
      self.head = None
      self.tail = None
    self.length -= 1
    return popped
  
  def __len__(self):
    return self.length
  
  def __str__(self):
    current = self.head
    values = []
    while current:
      values.append(str(current.val))
      current = current.next
    return '->'.join(values)

class FIFOQueueTest(unittest.TestCase):
  def setUp(self) -> None:
    self.queue = FIFOQueue(0)
  
  def test_append(self):
    self.queue.append('a')
    self.queue.append('b')
    self.queue.append(99)
    self.assertEqual(self.queue.tail.val, 99)
    self.assertEqual(str(self.queue), '0->a->b->99')

  def test_pop(self):
    for i in range(1, 5):
      self.queue.append(i)
    self.assertEqual(self.queue.pop(), 0)
    self.assertEqual(self.queue.tail.val, 4)
    self.assertEqual(self.queue.pop(), 1)
    self.assertEqual(self.queue.pop(), 2)
    self.assertEqual(self.queue.pop(), 3)

  def test_pop_empty(self):
    self.queue.pop()
    self.assertEqual(self.queue.head, None)
    self.assertEqual(self.queue.tail, None)
    with self.assertRaises(IndexError):
      self.queue.pop()


  def test_length(self):
    for i in range(1, 5):
      self.queue.append(i)
    self.assertEqual(len(self.queue), 5)
    self.queue.pop()
    self.assertEqual(len(self.queue), 4)
    self.queue.pop()
    self.queue.pop()
    self.assertEqual(len(self.queue), 2)
    self.queue.append("a")
    self.assertEqual(len(self.queue), 3)

class Dequeue(FIFOQueue):
  def __init__(self, n: any) -> None:
    super().__init__(n)
  
  def append_front(self, n: any):
    node = Element(n)
    old_head = self.head
    old_head.prev = node
    node.next = old_head
    self.head = node
    self.length += 1

  def pop_tail(self):
    if self.length == 0:
      raise IndexError
    popped = self.tail.val
    if self.tail.prev:
      self.tail = self.tail.prev
      self.tail.next = None
    else:
      self.head = None
      self.tail = None
    self.length -= 1
    return popped

class DequeueTest(FIFOQueueTest):
  def setUp(self):
    self.queue = Dequeue(0)

  def test_append_front(self):
    self.queue.append_front(-1)
    self.assertEqual(self.queue.head.val, -1)
    self.queue.append_front(-2)
    self.assertEqual(self.queue.head.val, -2)
    self.assertEqual(self.queue.head.next.val, -1)
  
  def test_pop_tail(self):
    for i in range(1, 5):
      self.queue.append(i)
    self.assertEqual(self.queue.pop_tail(), 4)
    self.assertEqual(self.queue.tail.val, 3)
    self.assertEqual(self.queue.pop_tail(), 3)
    self.assertEqual(self.queue.pop_tail(), 2)
    self.assertEqual(self.queue.pop_tail(), 1)

  def test_pop_tail_empty(self):
    self.queue.pop_tail()
    self.assertEqual(self.queue.head, None)
    self.assertEqual(self.queue.tail, None)
    with self.assertRaises(IndexError):
      self.queue.pop_tail()

  
  def test_length(self):
    super().test_length()
    self.queue.append_front(-1)
    self.assertEqual(len(self.queue), 4)
    self.queue.pop_tail()
    self.assertEqual(len(self.queue), 3)


if __name__ == "__main__":
  unittest.main()