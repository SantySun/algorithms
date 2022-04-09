import unittest

class DoublyLinkedNode:
  def __init__(self, value) -> None:
    self.value = value
    self.prev = None
    self.next = None
  def __str__(self):
    return self.value['value']

class DoublyLinkedList:
  def __init__(self) -> None:
    self.head = DoublyLinkedNode(None)
    self.tail = DoublyLinkedNode(None)
    self.length = 0
    self.head.next = self.tail
    self.tail.prev = self.head
  
  def __len__(self):
    return self.length
  
  def append_head(self, node):
    if self.length == 0:
      self.head.next = node
      self.tail.prev = node
      node.prev = self.head
      node.next = self.tail
    else:
      self.head.next.prev = node
      node.next = self.head.next
      node.prev = self.head
      self.head.next = node
    self.length += 1

  def append_tail(self, node):
    if self.length == 0:
      self.head.next = node
      self.tail.prev = node
      node.prev = self.head
      node.next = self.tail
    else:
      self.tail.prev.next = node
      node.prev = self.tail.prev
      node.next = self.tail
      self.tail.prev = node
    self.length += 1
  
  def pop_last(self):
    if self.length == 0:
      raise Exception
    last_node = self.tail.prev
    last_node.prev.next = last_node.next
    last_node.next.prev = last_node.prev
    self.length -= 1
    return last_node
  
  def __str__(self):
    if self.length != 0:
      current = self.head.next
      l = []
      while current is not self.tail:
        l.append(str(current))
        current = current.next
      return ' <--> '.join(l)
    return ''

class LRUCacheDict:
  def __init__(self) -> None:
    self.cache_dict = {}
    self.cache_values = DoublyLinkedList()
  
  def insert(self, key, value):
    if key in self.cache_dict:
      self.update(key, value)
    else:
      node = DoublyLinkedNode({ 'key': key, 'value': value })
      self.cache_dict[key] = node
      self.cache_values.append_head(node)

  def lookup(self, key):
    if key in self.cache_dict:
      value = self.cache_dict[key].value['value']
      node = self.cache_dict[key]
      self._move_node_to_first(node)
      return value
    else:
      return None

  def update(self, key, value):
    if key in self.cache_dict:
      self.cache_dict[key].value['value'] = value
      node = self.cache_dict[key]
      self._move_node_to_first(node)
      return value
    else:
      raise Exception

  def delete(self):
    if len(self.cache_values) == 0:
      raise Exception
    last_node = self.cache_values.pop_last()
    del self.cache_dict[last_node.value['key']]
  
  def _move_node_to_first(self, node):
    prev_node = node.prev
    next_node = node.next
    node.prev = None
    node.next = None
    prev_node.next = next_node
    next_node.prev = prev_node
    self.cache_values.length -= 1
    self.cache_values.append_head(node)


class LRUTest(unittest.TestCase):
  def setUp(self) -> None:
    self.cache = LRUCacheDict()
    self.cache.insert('key1', 'value1')
    self.cache.insert('key2', 'value2')
    self.cache.insert('key3', 'value3')
    self.cache.insert('key4', 'value4')
    return super().setUp()
  
  def test_insert(self):
    self.assertEqual(len(self.cache.cache_values), 4)
    self.assertEqual(str(self.cache.cache_values), 'value4 <--> value3 <--> value2 <--> value1')
    self.cache.insert('key2', 'value222')
    self.assertEqual(str(self.cache.cache_values), 'value222 <--> value4 <--> value3 <--> value1')
    self.cache.insert('key1', 'value111')
    self.assertEqual(str(self.cache.cache_values), 'value111 <--> value222 <--> value4 <--> value3')
  
  def test_update(self):
    self.cache.update('key2', 'value222')
    self.assertEqual(str(self.cache.cache_values), 'value222 <--> value4 <--> value3 <--> value1')
    self.cache.update('key1', 'value111')
    self.assertEqual(str(self.cache.cache_values), 'value111 <--> value222 <--> value4 <--> value3')
    with self.assertRaises(Exception):
      self.cache.update('key9', 'value9')

  def test_lookup(self):
    self.assertEqual(self.cache.lookup('key1'), 'value1')
    self.assertEqual(str(self.cache.cache_values), 'value1 <--> value4 <--> value3 <--> value2')
    self.assertEqual(self.cache.lookup('key2'), 'value2')
    self.assertEqual(str(self.cache.cache_values), 'value2 <--> value1 <--> value4 <--> value3')
    self.cache.insert('key2', 'value222')
    self.assertEqual(self.cache.lookup('key2'), 'value222')
    self.assertEqual(str(self.cache.cache_values), 'value222 <--> value1 <--> value4 <--> value3')
    self.cache.insert('key1', 'value111')
    self.assertEqual(self.cache.lookup('key1'), 'value111')
    self.assertEqual(str(self.cache.cache_values), 'value111 <--> value222 <--> value4 <--> value3')

  def test_delete(self):
    self.cache.delete()
    self.assertEqual(str(self.cache.cache_values), 'value4 <--> value3 <--> value2')
    self.assertEqual(len(self.cache.cache_values), 3)
    self.cache.delete()
    self.cache.delete()
    self.assertEqual(str(self.cache.cache_values), 'value4')
    self.assertEqual(len(self.cache.cache_values), 1)
    self.cache.delete()
    with self.assertRaises(Exception):
      self.cache.delete()



if __name__ == '__main__':
  unittest.main()