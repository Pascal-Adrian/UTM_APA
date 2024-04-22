import heapq
import sys


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for _ in range(vertices)] for _ in range(vertices)]

    def add_edge(self, u, v, weight):
        self.graph[u][v] = weight
        self.graph[v][u] = weight  # If the graph is undirected

    def dijkstra(self, source):
        distances = [sys.maxsize] * self.V
        distances[source] = 0
        priority_queue = [(0, source)]

        while priority_queue:
            (dist, current_vertex) = heapq.heappop(priority_queue)

            for neighbor in range(self.V):
                if self.graph[current_vertex][neighbor] > 0:
                    distance = self.graph[current_vertex][neighbor]
                    if dist + distance < distances[neighbor]:
                        distances[neighbor] = dist + distance
                        heapq.heappush(priority_queue, (distances[neighbor], neighbor))

        return distances

    def floyd_warshall(self):
        # Initialize the distance matrix with graph weights or infinity
        distances = [[sys.maxsize if i != j else 0 for j in range(self.V)] for i in range(self.V)]

        # Set initial distances from the graph
        for i in range(self.V):
            for j in range(self.V):
                if self.graph[i][j] > 0:
                    distances[i][j] = self.graph[i][j]

        # Apply Floyd-Warshall dynamic programming approach
        for k in range(self.V):
            for i in range(self.V):
                for j in range(self.V):
                    if distances[i][k] + distances[k][j] < distances[i][j]:
                        distances[i][j] = distances[i][k] + distances[k][j]

        return distances
