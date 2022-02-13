from random import shuffle
import unittest
from time import time
from matplotlib import pyplot as plt
import sys

sys.path.append('.')

from heap import MinHeap

class Sort:
    @classmethod
    def bubble_sort(self, list):
        for i in range(len(list), 0, -1):
            for j in range(1, i):
                if list[j - 1] > list[j]:
                    list[j - 1], list[j] = list[j], list[j - 1]

    @classmethod
    def selection_sort(self, list):
        def _get_max_index(list, start, end):
            assert end > start
            max_index = start
            for i in range(start + 1, end):
                if list[i] > list[max_index]:
                    max_index = i
            return max_index

        for i in range(len(list), 1, -1):
            max_index = _get_max_index(list, 0, i)
            list[max_index], list[i - 1] = list[i - 1], list[max_index]

    @classmethod
    def insertion_sort(self, list):
        for i in range(1, len(list)):
            position = i
            insert_value = list[i]
            while insert_value < list[position - 1] and position > 0:
                list[position] = list[position - 1]
                position = position - 1
            list[position] = insert_value

    @classmethod
    def quick_sort(self, list):
        def _quick_sort_helper(list, start, end):
            if start < end:
                left_mark = start + 1
                right_mark = end
                pivot_element = list[start]
                while True:
                    while left_mark <= right_mark and list[left_mark] <= pivot_element:
                        left_mark = left_mark + 1
                    while left_mark <= right_mark and list[right_mark] >= pivot_element:
                        right_mark = right_mark - 1

                    if left_mark > right_mark:
                        break
                    else:
                        list[left_mark], list[right_mark] = list[right_mark], list[left_mark]
                list[right_mark], list[start] = list[start], list[right_mark]
                _quick_sort_helper(list, start, right_mark - 1)
                _quick_sort_helper(list, right_mark + 1, end)
        _quick_sort_helper(list, 0, len(list) - 1)

    @classmethod
    def shell_sort(self, list):
        def _gap_insertion_sort(list, start, gap):
            for i in range(start + gap, len(list), gap):
                position = i
                insert_value = list[i]
                while insert_value < list[position - gap] and position >= gap:
                    list[position] = list[position - gap]
                    position = position - gap
                list[position] = insert_value
        gap = len(list) // 2
        while gap > 0:
            for start_position in range(gap):
                _gap_insertion_sort(list, start_position, gap)
            gap = gap // 2

    @classmethod
    def merge_sort(self, list):
        if len(list) > 1:
            left_half = list[len(list)//2:]
            right_half = list[:len(list)//2]
            self.merge_sort(left_half)
            self.merge_sort(right_half)

            left_half_index = 0
            right_half_index = 0
            list_position = 0

            while left_half_index < len(left_half) and right_half_index < len(right_half):
                if left_half[left_half_index] < right_half[right_half_index]:
                    list[list_position] = left_half[left_half_index]
                    left_half_index = left_half_index + 1
                else:
                    list[list_position] = right_half[right_half_index]
                    right_half_index = right_half_index + 1
                list_position = list_position + 1

            while left_half_index < len(left_half):
                list[list_position] = left_half[left_half_index]
                list_position = list_position + 1
                left_half_index = left_half_index + 1

            while right_half_index < len(right_half):
                list[list_position] = right_half[right_half_index]
                list_position = list_position + 1
                right_half_index = right_half_index + 1

    @classmethod
    def heap_sort(self, list):
        heap = MinHeap()
        heap.build_heap(list)
        i = 0
        while heap.current_size > 0:
            list[i] = heap.pop()
            i += 1


class SortTest(unittest.TestCase):
    nums = [i for i in range(1, 101)]
    sorted_nums = [i for i in range(1, 101)]

    def setUp(self) -> None:
        shuffle(self.nums)
        self.assertFalse(
            all([self.nums[i] == self.sorted_nums[i] for i in range(0, 100)]))

    def test_bubble_sort(self):
        Sort.bubble_sort(self.nums)
        self.assertListEqual(self.nums, self.sorted_nums)

    def test_selection_sort(self):

        Sort.selection_sort(self.nums)
        self.assertListEqual(self.nums, self.sorted_nums)

    def test_insertion_sort(self):
        Sort.insertion_sort(self.nums)
        self.assertListEqual(self.nums, self.sorted_nums)

    def test_merge_sort(self):
        Sort.merge_sort(self.nums)
        self.assertListEqual(self.nums, self.sorted_nums)

    def test_shell_sort(self):
        Sort.shell_sort(self.nums)
        self.assertListEqual(self.nums, self.sorted_nums)

    def test_quick_sort(self):
        Sort.quick_sort(self.nums)
        self.assertListEqual(self.nums, self.sorted_nums)
    
    def test_heap_sort(self):
        Sort.heap_sort(self.nums)
        self.assertListEqual(self.nums, self.sorted_nums)


class Plot:
    def __init__(self) -> None:
        self.numbers = [i for i in range(1000)]
        self.plots = []
        shuffle(self.numbers)

    def add_plot_line(self, func):
        print("Executing...", func.__name__)
        x = []
        y = []
        for i in range(10, 1000, 10):
            start = time()
            func(self.numbers[:i])
            time_cost = time() - start

            x.append(i)
            y.append(time_cost * 1000)
        self.plots.append((x, y, func.__name__))

    def plot(self):
        fig, ax = plt.subplots()
        for x, y, function_name in self.plots:
            ax.plot(x, y, dashes=[2,2,2], label=function_name)
        ax.legend()
        plt.show()





if __name__ == '__main__':
    plot = Plot()
    for func in [Sort.quick_sort, Sort.shell_sort, Sort.merge_sort, Sort.selection_sort, Sort.insertion_sort, Sort.bubble_sort, Sort.heap_sort]:
        plot.add_plot_line(func)
    plot.plot()
    unittest.main()

