import time
from Lab3.Graph import Graph
from networkx.generators.random_graphs import erdos_renyi_graph
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(100000)


def test(lb=2, ub=12, p=0.8, n_tests=10):
    BFS_results = []
    DFS_results = []
    n_nodes = [2**i for i in range(lb, ub)]
    for n in n_nodes:
        temp_dfs = []
        temp_bfs = []
        for i in range(n_tests):
            graph = Graph()
            G = erdos_renyi_graph(n, p)
            for edge in G.edges:
                graph.addEdge(edge[0], edge[1])

            start = time.perf_counter()
            graph.DFS(0)
            finish = time.perf_counter()

            temp_dfs.append(finish - start)

            start = time.perf_counter()
            graph.BFS(0)
            finish = time.perf_counter()

            temp_bfs.append(finish - start)

        DFS_results.append(sum(temp_dfs) / n_tests)
        BFS_results.append(sum(temp_bfs) / n_tests)

    return n_nodes, BFS_results, DFS_results

def plot(x, y, title="Time complexity"):
    plt.plot(x, y)
    plt.xlabel("Number of nodes")
    plt.ylabel("Time")
    plt.title(title)
    plt.show()

def plot_2(x, y1, y2, title="DFS and BFS time complexity"):
    plt.plot(x, y1, label="BFS")
    plt.plot(x, y2, label="DFS")
    plt.xlabel("Number of nodes")
    plt.ylabel("Time")
    plt.title(title)
    plt.legend()
    plt.show()

def print_results(n_nodes, results):
    for i in range(len(n_nodes)):
        print(f"{n_nodes[i]}: {results[i]}")

def extensive_test():
    for i in range(1, 11):
        p = i / 10
        n_nodes, BFS_results, DFS_results = test(2, 12, p, 10)
        plot_2(n_nodes, BFS_results, DFS_results, "DFS and BFS time complexity for p = " + str(i / 10))
        print("===========================================\n")
        print(f"p = {i / 10}\n")
        # print("DFS results:")
        # print_results(n_nodes, DFS_results)
        plot(n_nodes, BFS_results, "BFS time complexity for p = " + str(i / 10))
        # print("\n-------------------------------------------\n")
        print("BFS results:")
        print_results(n_nodes, BFS_results)



if __name__ == "__main__":
    extensive_test()