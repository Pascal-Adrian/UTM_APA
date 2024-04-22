from Lab5.Graph import Graph
import time
import matplotlib.pyplot as plt
import random

def generate_random_graph(n_nodes, max_weight):
    graph = Graph(n_nodes)
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i != j:
                graph.add_edge(i, j, random.randint(1, max_weight))
    return graph

def test(lb=2, ub=10, max_weight=100):
    n_nodes = [2**i for i in range(lb, ub)]
    prim_results = []
    kruskal_results = []

    for n in n_nodes:
        graph = generate_random_graph(n, max_weight)

        start = time.time()
        graph.prim()
        end = time.time()

        prim_results.append(end - start)

        start = time.time()
        graph.kruskal()
        end = time.time()

        kruskal_results.append(end - start)

    return n_nodes, prim_results, kruskal_results

def plot(x, y, title="Time complexity"):
    plt.plot(x, y)
    plt.xlabel("Number of nodes")
    plt.ylabel("Time")
    plt.title(title)
    plt.show()


def print_results(n_nodes, results):
    for i in range(len(n_nodes)):
        print(f"{n_nodes[i]}: {results[i]}")


def main():
    n_nodes, prim_results, kruskal_results = test()
    plot(n_nodes, prim_results, "Prim")
    plot(n_nodes, kruskal_results, "Kruskal")
    print("\nPrim results:")
    print_results(n_nodes, prim_results)
    print("\nKruskal results:")
    print_results(n_nodes, kruskal_results)


if __name__ == "__main__":
    main()