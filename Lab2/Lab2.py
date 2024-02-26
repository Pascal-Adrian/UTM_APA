from timeit import timeit
import random
import pandas as pd
import matplotlib.pyplot as plt

class Sort:
    def __init__(self):
        self.counter = 0
        self.plots = []
        pass

    def quick_sort(self, array):
        def partition(arr, low, high):
            i = low - 1
            pivot = arr[high]
            for j in range(low, high):
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i+1], arr[high] = arr[high], arr[i+1]
            return i+1

        def quick_sort_helper(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort_helper(arr, low, pi-1)
                quick_sort_helper(arr, pi+1, high)

        quick_sort_helper(array, 0, len(array)-1)
        return array

    def merge_sort(self, array):
        def merge(arr, l, m, r):
            n1 = m - l + 1
            n2 = r - m
            L = [0] * n1
            R = [0] * n2
            for i in range(n1):
                L[i] = arr[l + i]
            for i in range(n2):
                R[i] = arr[m + 1 + i]
            i = j = 0
            k = l
            while i < n1 and j < n2:
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1
            while i < n1:
                arr[k] = L[i]
                i += 1
                k += 1
            while j < n2:
                arr[k] = R[j]
                j += 1
                k += 1

        def merge_sort_helper(arr, l, r):
            if l < r:
                m = l + (r - l) // 2
                merge_sort_helper(arr, l, m)
                merge_sort_helper(arr, m+1, r)
                merge(arr, l, m, r)

        merge_sort_helper(array, 0, len(array)-1)
        return array

    def heap_sort(self, array):
        def heapify(arr, n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2
            if l < n and arr[i] < arr[l]:
                largest = l
            if r < n and arr[largest] < arr[r]:
                largest = r
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)

        n = len(array)
        for i in range(n//2-1, -1, -1):
            heapify(array, n, i)
        for i in range(n-1, 0, -1):
            array[i], array[0] = array[0], array[i]
            heapify(array, i, 0)
        return array

    def tim_sort(self, array):
        MIN_MERGE = 32

        def calcMinRun(n):
            r = 0
            while n >= MIN_MERGE:
                r |= n & 1
                n >>= 1
            return n + r

        def insertionSort(arr, left, right):
            for i in range(left + 1, right + 1):
                j = i
                while j > left and arr[j] < arr[j - 1]:
                    arr[j], arr[j - 1] = arr[j - 1], arr[j]
                    j -= 1

        def merge(arr, l, m, r):
            len1, len2 = m - l + 1, r - m
            left, right = [], []
            for i in range(0, len1):
                left.append(arr[l + i])
            for i in range(0, len2):
                right.append(arr[m + 1 + i])

            i, j, k = 0, 0, l

            while i < len1 and j < len2:
                if left[i] <= right[j]:
                    arr[k] = left[i]
                    i += 1

                else:
                    arr[k] = right[j]
                    j += 1

                k += 1

            while i < len1:
                arr[k] = left[i]
                k += 1
                i += 1

            while j < len2:
                arr[k] = right[j]
                k += 1
                j += 1

        n = len(array)
        minRun = calcMinRun(n)

        for start in range(0, n, minRun):
            end = min(start + minRun - 1, n - 1)
            insertionSort(array, start, end)

        size = minRun
        while size < n:
            for left in range(0, n, 2 * size):
                mid = min(n - 1, left + size - 1)
                right = min((left + 2 * size - 1), (n - 1))

                if mid < right:
                    merge(array, left, mid, right)

            size = 2 * size

        return array

    def test(self, array, tests=1, quick_sort=True, merge_sort=True, heap_sort=True, tim_sort=True):
        run = {}
        if quick_sort:
            run["quick_sort"] = timeit(lambda: self.quick_sort(array.copy()), number=tests)
        if merge_sort:
            run["merge_sort"] = timeit(lambda: self.merge_sort(array.copy()), number=tests)
        if heap_sort:
            run["heap_sort"] = timeit(lambda: self.heap_sort(array.copy()), number=tests)
        if tim_sort:
            run["tim_sort"] = timeit(lambda: self.tim_sort(array.copy()), number=tests)
        return run

    def test_all(self, tests=1):
        results = []
        for i in range(2, 9):
            size = 10**i
            print("====================================")
            print(f"Testing for size {size}...")
            array = [random.randint(0, 10*size) for _ in range(size)]
            run = self.test(array, tests=tests)
            results.append((size, run))
            print("Testing done!")
            print("====================================\n")

        print("\n\n\n")
        print("Saving to df...\n")
        self.save_to_df(results)
        print("Results saved successfully!")

    def save_to_df(self, results):
        df = pd.DataFrame()
        df["n"] = [results[i][0] for i in range(len(results))]
        for key in results[0][1].keys():
            df[key] = [results[i][1][key] for i in range(len(results))]
        self.counter += 1
        df.to_csv(f"apa_lab_2_results_{self.counter}.csv", index=False)

    def individual_plot_from_csv(self, filename):
        df = pd.read_csv(filename)
        for method in df.columns[1:]:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df["n"], df[method], label=method)
            ax.set_xlabel('n')
            ax.set_ylabel('Execution Time (s)')
            ax.set_title(f'Execution Time of Sort Method: {method}')
            ax.legend()
            ax.grid(True)
            self.plots.append(fig)

    def plot_from_csv(self, filename):
        df = pd.read_csv(filename)
        fig, ax = plt.subplots(figsize=(10, 6))
        for method in df.columns[1:]:
            ax.plot(df["n"], df[method], label=method)
        ax.set_xlabel('n')
        ax.set_ylabel('Execution Time (s)')
        ax.set_title('Execution Time of Sort Methods')
        ax.legend()
        ax.grid(True)
        self.plots.append(fig)

    def show_plots(self):
        for plot in self.plots:
            plt.show()

    def get_from_fils_and_print(self, filename):
        df = pd.read_csv(filename)
        for method in df.columns[1:]:
            print(f"Method: {method}")
            print(df[["n", method]])
            print("\n\n\n")


if __name__ == "__main__":
    sort = Sort()
    # sort.test_all()
    # sort.test_all()
    # sort.test_all()
    sort.get_from_fils_and_print("apa_lab_2_results_1.csv")
    sort.plot_from_csv("apa_lab_2_results_1.csv")
    sort.individual_plot_from_csv("apa_lab_2_results_1.csv")
    sort.show_plots()

