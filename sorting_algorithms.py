"""OOP implementation of sorting algorithms."""

import random
import time
from typing import List


class SortingAlgorithm:
    """Base class for sorting algorithms."""

    def __init__(self) -> None:
        from visualiser import WINDOW_HEIGHT
        self.array = random.sample(range(WINDOW_HEIGHT), WINDOW_HEIGHT)
        self.start_time = None
        self.time_taken = None
        self.sleep_time = 0.0

    def set_sleep_time(self, sleep_time: float) -> None:
        """Set sleeping time."""
        self.sleep_time = sleep_time

    def algorithm(self) -> None:
        """Sorting algorithm implementation."""
        pass

    def update_window(self, swap1: int = 0, swap2: int = 0) -> None:
        """Update game window."""
        from visualiser import update_window, WINDOW
        update_window(self, WINDOW, swap1, swap2)
        time.sleep(self.sleep_time)

    def get_time_taken(self) -> float:
        """Return time taken for sorting."""
        return self.time_taken

    def run(self) -> List[int]:
        """Run the sorting algorithm and return sorted array."""
        self.start_time = time.time()
        self.algorithm()
        self.time_taken = time.time() - self.start_time

        return self.array


class SelectionSort(SortingAlgorithm):
    """Selection sort implementation."""

    def __init__(self) -> None:
        super().__init__()

    def algorithm(self):
        for i in range(len(self.array) - 1):

            # Find the next item
            min_index = i
            for j in range(i + 1, len(self.array)):
                if self.array[j] < self.array[min_index]:
                    min_index = j

            # Swap the current item with the correct one
            self.array[i], self.array[min_index] = self.array[min_index], self.array[i]
            self.update_window(i, min_index)  # Update the window to reflect the changes


class BubbleSort(SortingAlgorithm):
    """Bubble sort implementation."""

    def __init__(self) -> None:
        super().__init__()

    def algorithm(self) -> None:
        for i in range(len(self.array)):
            swap_occurred = False
            for j in range(len(self.array) - i - 1):
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    swap_occurred = True
            self.update_window(len(self.array) - i - 2, len(self.array) - i - 1)
            if not swap_occurred:  # Nothing got swapped, array is sorted
                break


class CombSort(SortingAlgorithm):
    """Comb sort implementation."""

    def __init__(self) -> None:
        super().__init__()

    def algorithm(self) -> None:
        gap = self.get_next_gap(len(self.array))
        swap_occurred = True  # Initialize to True so loop runs at least once
        while gap != 1 or swap_occurred:
            swap_occurred = False
            for i in range(len(self.array) - gap):
                if self.array[i] > self.array[i + gap]:
                    self.array[i], self.array[i + gap] = self.array[i + gap], self.array[i]
                    self.update_window(i, i + gap)
                    swap_occurred = True
            gap = self.get_next_gap(gap)

    @staticmethod
    def get_next_gap(gap) -> int:
        """Shrink given gap by a shrink factor of 1.3 and return the result."""

        gap = int(gap // 1.3)
        if gap < 1:
            return 1
        return gap


class QuickSort(SortingAlgorithm):
    """Quick sort implementation."""

    def __init__(self):
        super().__init__()

    def algorithm(self) -> None:
        self.quick_sort(self.array)

    def quick_sort(self, array: List[int], start: int = None, end: int = None):
        """Sort given array[start:end] using quick sort algorithm. Arguments 'start' and 'end' are
        interpreted as in slice notation. Also change self.array and update the game window."""

        if start is None:
            start = 0
        if end is None:
            end = len(array)
        if start < end:
            pivot = self.partition(array, start, end)
            self.quick_sort(array, start, pivot)  # Recursively sort left array
            self.quick_sort(array, pivot + 1, end)  # Recursively sort right array

    def partition(self, array: List[int], start: int, end: int) -> int:
        """Naive partitioning of the array, with pivot value being the first item."""

        pivot_value = array[start]
        lower = start
        upper = end - 1

        done = False
        while not done:
            while lower <= upper and array[lower] <= pivot_value:
                lower += 1
            while upper >= lower and array[upper] >= pivot_value:
                upper -= 1

            if upper < lower:  # Pointers crossing index is pivot index
                done = True
            else:  # Pointers haven't crossed, so swap them
                array[lower], array[upper] = array[upper], array[lower]
                self.update_window(lower, upper)

        # Swap item at 'start' with item at 'upper' (now pivot index)
        array[start], array[upper] = array[upper], array[start]
        self.update_window(start, upper)
        return upper


class StoogeSort(SortingAlgorithm):
    """Stooge sort implementation."""

    def __init__(self) -> None:
        super().__init__()

    def algorithm(self) -> None:
        self.stooge_sort(self.array)

    def stooge_sort(self, array: List[int], low: int = None, high: int = None) -> None:
        if low is None:
            low = 0
        if high is None:
            high = len(array) - 1

        if low >= high:
            return

        if array[low] > array[high]:
            array[low], array[high] = array[high], array[low]
            self.update_window(low, high)

        if high - low + 1 > 2:  # More than 2 elements in array
            index = int((high - low + 1) / 3)

            # Recursively sort first 2 / 3 elements
            self.stooge_sort(self.array, low, (high - index))

            # Recursively sort last 2 / 3 elements
            self.stooge_sort(self.array, low + index, high)

            # Recursively sort first 2 / 3 elements again, to confirm they're sorted
            self.stooge_sort(self.array, low, (high - index))

