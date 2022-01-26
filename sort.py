from random import shuffle

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
        pass

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
        pass


def test(func):
    nums = [i for i in range(1, 101)]
    shuffle(nums)

    func(nums)

    for i in range(1, 101):
        try:
            assert i == nums[i - 1]
        except:
            print("expect:", i, "actual:", nums[i - 1])
            return
    print("Test Successful:", func.__name__)


test(Sort.bubble_sort)
test(Sort.selection_sort)
test(Sort.insertion_sort)
test(Sort.shell_sort)