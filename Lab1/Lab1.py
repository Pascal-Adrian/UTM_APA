import numpy as np
import pandas as pd
from timeit import timeit
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(100000)


class Fibonnaci:

    def __init__(self):
        self.save_counter = 0
        self.plots = []
        pass

    def reccursive(self, n):
        if n <= 1:
            return n
        return self.reccursive(n-1) + self.reccursive(n-2)

    def recursive_dynamic(self, n):
        def recursive_dynamic_helper(n, memo):
            if n <= 1:
                return n
            if memo[n]:
                return memo[n]
            memo[n] = recursive_dynamic_helper(n-1, memo) + recursive_dynamic_helper(n-2, memo)
            return memo[n]
        return recursive_dynamic_helper(n, [None] * (n + 1))

    def itterative(self, n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    def dynamic_array(self, n):
        fib = [0, 1]
        for i in range(2, n+1):
            fib.append(fib[i-1] + fib[i-2])
        return fib[n]

    def matrix(self, n):
        F = np.array([[1, 1], [1, 0]], dtype=object)
        if n == 0:
            return 0
        F = np.linalg.matrix_power(F, n-1)

        return F[0][0]

    def binet_formula(self, n):
        phi = int((1 + 5**0.5) / 2)
        return int((phi**n - (1-phi)**n) / 5**0.5)

    def test(self, array, tests=1, recursive=False, recursive_dynamic=False, itterative=False, dynamic_array=False,
                 matrix=False, binet_formula=False):
        results = []

        for i in array:
            run = {}
            if recursive:
                run["reccursive"] = timeit(lambda: self.reccursive(i), number=tests)
            if recursive_dynamic:
                run["recursive_dynamic"] = timeit(lambda: self.recursive_dynamic(i), number=tests)
            if itterative:
                run["itterative"] = timeit(lambda: self.itterative(i), number=tests)
            if dynamic_array:
                run["dynamic_array"] = timeit(lambda: self.dynamic_array(i), number=tests)
            if matrix:
                run["matrix"] = timeit(lambda: self.matrix(i), number=tests)
            if binet_formula:
                run["binet_formula"] = timeit(lambda: self.binet_formula(i), number=tests)
            results.append((i, run))

        self.plot(results)
        self.save_to_df(results)

    def plot(self, results):
        plots = []
        for method in results[0][1].keys():
            fig, ax = plt.subplots(figsize=(10, 6))
            x = [result[0] for result in results]
            y = [result[1][method] for result in results]
            ax.plot(x, y, label=method)
            ax.set_xlabel('n')
            ax.set_ylabel('Execution Time (s)')
            ax.set_title(f'Execution Time of Fibonacci Method: {method}')
            ax.legend()
            ax.grid(True)
            self.plots.append(fig)

    def show_plots(self):
        for plot in self.plots:
            plt.show()


    def save_to_df(self, results):
        columns = ["n"]
        for method in results[0][1].keys():
            columns.append(method)
        dataframe = pd.DataFrame(columns=columns)
        for result in results:
            data = [result[0]]
            for method in result[1].keys():
                data.append(result[1][method])
            dataframe.loc[len(dataframe)] = data
        self.save_counter += 1
        dataframe.to_csv(f"apa_lab_1_results_{self.save_counter}.csv", index=False)

    def get_from_df_and_plot(self, filename):
        dataframe = pd.read_csv(filename)
        results = []
        for index, row in dataframe.iterrows():
            run = {}
            for method in dataframe.columns[1:]:
                run[method] = row[method]
            results.append((row["n"], run))
        self.plot(results)

    def get_from_df(self, filename, method):
        dataframe = pd.read_csv(filename)
        if method in dataframe.columns:
            return dataframe[["n", method]]
        return None

    def plot_all_results_on_the_same_axes(self, results):
        fig, ax = plt.subplots(figsize=(10, 6))
        for method in results[0][1].keys():
            x = [result[0] for result in results]
            y = [result[1][method] for result in results]
            ax.plot(x, y, label=method)
        ax.set_xlabel('n')
        ax.set_ylabel('Execution Time (s)')
        ax.set_title(f'Execution Time of Fibonacci Methods')
        ax.legend()
        ax.grid(True)
        plt.show()


if __name__ == "__main__":
    fib = Fibonnaci()
    fib.test([5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45], tests=1, recursive=True,
             recursive_dynamic=True, itterative=True, dynamic_array=True, matrix=True, binet_formula=True)
    fib.test([501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849],
             tests=1, recursive=False, recursive_dynamic=True, itterative=True, dynamic_array=True, matrix=True,
             binet_formula=True)
    fib.get_from_df_and_plot("apa_lab_1_results_1.csv")
    fib.get_from_df_and_plot("apa_lab_1_results_2.csv")

    print(fib.get_from_df("apa_lab_1_results_2.csv", "recursive_dynamic"))
    print(fib.get_from_df("apa_lab_1_results_2.csv", "itterative"))
    print(fib.get_from_df("apa_lab_1_results_2.csv", "dynamic_array"))
    print(fib.get_from_df("apa_lab_1_results_2.csv", "matrix"))
    print(fib.get_from_df("apa_lab_1_results_2.csv", "binet_formula"))
    fib.show_plots()

