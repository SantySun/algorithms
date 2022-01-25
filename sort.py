from random import shuffle

class Sort:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def bubble_sort(self, list):
        for i in range(len(list), 0, -1):
            # from the last element to the first element
            for j in range(1, i):
                if list[j - 1] > list[j]:
                    list[j - 1], list[j] = list[j], list[j - 1]
    
    @classmethod
    def selection_sort(self, list):
        pass

    @classmethod
    def quick_sort(self, list):
        pass

    @classmethod
    def shell_sort(self, list):
        pass

    @classmethod
    def merge_sort(self, list):
        pass


def test(func):
    nums = [i for i in range(1, 101)]
    shuffle(nums)

    func(nums)

    for i in range(1, 101):
        assert i == nums[i - 1]
    print("Test Successful:", func.__name__)


test(Sort.bubble_sort)