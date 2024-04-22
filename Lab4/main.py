from Lab4.Graph import Graph
import time
import matplotlib.pyplot as plt
import random

def generate_random_graph(n_nodes, density, max_weight):
    graph = Graph(n_nodes)
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i != j and random.random() < density:
                graph.add_edge(i, j, random.randint(1, max_weight))
    return graph

def test(lb=2, ub=10, density=0.5, max_weight=10):
    n_nodes = [2**i for i in range(lb, ub)]
    dijsktra_results = []
    floyd_warshall_results = []

    for n in n_nodes:
        graph = generate_random_graph(n, density, max_weight)

        start = time.time()
        graph.dijkstra(0)
        end = time.time()

        dijsktra_results.append(end - start)

        start = time.time()
        graph.floyd_warshall()
        end = time.time()

        floyd_warshall_results.append(end - start)

    return n_nodes, dijsktra_results, floyd_warshall_results

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
    n_nodes, dijsktra_results, floyd_warshall_results = test()
    plot(n_nodes, dijsktra_results, "Dijkstra")
    plot(n_nodes, floyd_warshall_results, "Floyd-Warshall")
    print("\nDijkstra results:")
    print_results(n_nodes, dijsktra_results)
    print("\nFloyd-Warshall results:")
    print_results(n_nodes, floyd_warshall_results)


if __name__ == "__main__":
    main()
