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
  def __init__(self, node: Node) -> None:
    self.head = node
    self.length = 1

  def append(self, node: Node) -> None:
    current = self.head
    while current.next:
      current = current.next
    current.next = node
    self.length = self.length + 1

  def __add__(self, linked_list):
    current = self.head
    while current.next:
      current = current.next
    current.next = linked_list.head
    self.length = self.length + linked_list.length
    return self

  def pop(self, position=None):
    assert position == None or type(position) == int
    if position is None:
      current = self.head
      while current.next and current.next.next:
        current = current.next
      current.next = None
    elif position >= self.length:
      raise IndexError
    else:
      if position == 0:
        self.head = self.head.next
      else:
        current = self.head
        for _ in range(position - 1):
          current = current.next
        current.next = current.next.next
  
  def __str__(self) -> str:
    current = self.head
    values = []
    while current:
      values.append(str(current.val))
      current = current.next
    return '->'.join(values)

class LinkedListTest(unittest.TestCase):
  def setUp(self) -> None:
    self.list_1 = LinkedList(Node(0))   
  
  def test_append(self):
    self.list_1.append(Node('a'))
    self.list_1.append(Node('b'))
    self.list_1.append(Node(99))
    self.assertEqual(str(self.list_1), '0->a->b->99')
  
  def test_add(self):
    l2 = LinkedList(Node('a'))
    l2.append(Node('b'))
    l2.append(Node("c"))
    self.list_1.append(Node(1))
    self.list_1.append(Node(2))
    self.assertEqual(str(self.list_1 + l2), '0->1->2->a->b->c')
  
  def test_pop(self):
    for i in range(1, 5):
      self.list_1.append(Node(i))
    self.list_1.pop()
    self.assertEqual(str(self.list_1), '0->1->2->3')
    self.list_1.pop(0)
    self.assertEqual(str(self.list_1), '1->2->3')
    
    with self.assertRaises(IndexError):
      self.list_1.pop(5)
    
    self.list_1.append(Node(4))
    self.list_1.append(Node(5))
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
  def __init__(self, node: Element) -> None:
    self.head = node
    self.tail = node
    self.length = 1

  def append(self, node: Element):
    if self.length ==  0:
      self.__init__(node)
    else:
      self.tail.next = node
      node.prev = self.tail
      self.tail = node
      self.length = self.length + 1
  
  def pop(self):
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
    self.queue = FIFOQueue(Element(0))
  
  def test_append(self):
    self.queue.append(Element('a'))
    self.queue.append(Element('b'))
    self.queue.append(Element(99))
    self.assertEqual(self.queue.tail.val, 99)
    self.assertEqual(str(self.queue), '0->a->b->99')

  def test_pop(self):
    for i in range(1, 5):
      self.queue.append(Element(i))
    self.assertEqual(self.queue.pop(), 4)
    self.assertEqual(self.queue.tail.val, 3)
    self.assertEqual(self.queue.pop(), 3)
    self.assertEqual(self.queue.pop(), 2)
    self.assertEqual(self.queue.pop(), 1)

  def test_pop_empty(self):
    self.queue.pop()
    self.assertEqual(self.queue.head, None)
    self.assertEqual(self.queue.tail, None)
    with self.assertRaises(IndexError):
      self.queue.pop()


  def test_length(self):
    for i in range(1, 5):
      self.queue.append(Element(i))
    self.assertEqual(len(self.queue), 5)
    self.queue.pop()
    self.assertEqual(len(self.queue), 4)
    self.queue.pop()
    self.queue.pop()
    self.assertEqual(len(self.queue), 2)
    self.queue.append(Element("a"))
    self.assertEqual(len(self.queue), 3)

class Dequeue(FIFOQueue):
  def __init__(self, node: Element) -> None:
    super().__init__(node)
  
  def append_front(self, node: Element):
    old_head = self.head
    old_head.prev = node
    node.next = old_head
    self.head = node
    self.length += 1

  def pop_front(self):
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

class DequeueTest(FIFOQueueTest):
  def setUp(self):
    self.queue = Dequeue(Element(0))

  def test_append_front(self):
    self.queue.append_front(Element(-1))
    self.assertEqual(self.queue.head.val, -1)
    self.queue.append_front(Element(-2))
    self.assertEqual(self.queue.head.val, -2)
    self.assertEqual(self.queue.head.next.val, -1)
  
  def test_pop_front(self):
    for i in range(1, 5):
      self.queue.append(Element(i))
    self.assertEqual(self.queue.pop_front(), 0)
    self.assertEqual(self.queue.tail.val, 4)
    self.assertEqual(self.queue.pop_front(), 1)
    self.assertEqual(self.queue.pop_front(), 2)
    self.assertEqual(self.queue.pop_front(), 3)

  def test_pop_front_empty(self):
    self.queue.pop_front()
    self.assertEqual(self.queue.head, None)
    self.assertEqual(self.queue.tail, None)
    with self.assertRaises(IndexError):
      self.queue.pop_front()

  
  def test_length(self):
    super().test_length()
    self.queue.append_front(Element(-1))
    self.assertEqual(len(self.queue), 4)
    self.queue.pop_front()
    self.assertEqual(len(self.queue), 3)


if __name__ == "__main__":
  unittest.main()