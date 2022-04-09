from collections import deque
import heapq
import time
import string
import unittest
import random
from typing import List


class MaxN:
  def __init__(self, l: List[int]):
    self.numbers = l
  
  def max_n(self, n: int):
    assert n <= len(self.numbers)
    heap_list = self.numbers[:n]
    heapq.heapify(heap_list)

    for i in range(n, len(self.numbers)):
      if self.numbers[i] > heap_list[0]:
        heapq.heappushpop(heap_list, self.numbers[i])
    
    result = []
    while heap_list:
      result.append(heapq.heappop(heap_list))
    
    return result


class MaxNTest(unittest.TestCase):
  numbers = [n for n in range(100)]

  def setUp(self) -> None:
    random.shuffle(self.numbers)
  
  
  def test_max_10(self):
    max_n = MaxN(self.numbers)
    self.assertListEqual([n for n in range(90, 100)], max_n.max_n(10))
    self.assertListEqual(heapq.nlargest(10, self.numbers, key = lambda x: x)[::-1], max_n.max_n(10))

class FileCollectionSort:
  def __init__(self, M, N):
    self.files = [
      {
        "file_name": self.__generate_file(5),
        "collection_id": i % (N - 1),
        "size": round(random.random() * i * 100) 
      } for i in range(M)
    ]
    random.shuffle(self.files)
    for f in random.choices(self.files, k=len(self.files) // 5):
      f["collection_id"] = None
    # print(self.files)
  
  def __generate_file(self, N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
  
  def solution(self, K):
    collections = {
      "uncategorized": 0
    }
    for f in self.files:
      if f["collection_id"] is not None:
        if str(f["collection_id"]) not in collections:
          collections[str(f["collection_id"])] = 0
        collections[str(f["collection_id"])] += f["size"]
      else:
        collections["uncategorized"] += f["size"]
    
    # time: O(M), space: O(N)
    
    hq = []
    for k in collections:
      if len(hq) < K:
        heapq.heappush(hq, (collections[k], k)) # => sum(x from 1 to K, log(x)) => Klog(K) 
      else:
        if collections[k] > hq[0][0]:
          heapq.heappushpop(hq, (collections[k], k)) # time: (N-K) * logK
    # space: O(K), time: O(NlogK)

    result = []
    while len(hq) > 0:
      result.append(heapq.heappop(hq))
    
    # time: O(KlogK)
    print(result)
    return result

    # total:
    # time: O(M + NlogK + KlogK) => O(M + 2 * NlogN)
    # space: O(N + K) => O(N)


# if __name__ == '__main__':
#   fcs = FileCollectionSort(M = 300, N = 14)
#   fcs.solution(5)
  # unittest.main()

class GetPI:
  def __init__(self) -> None:
    self.total = 0
    self.inside = 0
  
  def __is_in_circle(self, cord) -> bool:
    return (cord[0] - 0.5)**2 + (cord[1] - 0.5)**2 <= 0.25
  
  def add_cord(self) -> None:
    cord = (random.random(), random.random())
    self.total += 1
    if self.__is_in_circle(cord):
      self.inside += 1
  
  def get_PI(self) -> float:
    for _ in range(100000000):
      self.add_cord()
    
    return self.inside * 4 / self.total


if __name__ == '__main__':
  pi = GetPI()
  print(pi.get_PI())