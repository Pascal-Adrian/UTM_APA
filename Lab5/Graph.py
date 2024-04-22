import sys


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []  # For Kruskal's algorithm (stores edges)
        self.adj_matrix = [[0 for column in range(vertices)] for row in
                           range(vertices)]  # For Prim's algorithm (adjacency matrix)

    # Function to add an edge to the graph
    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])  # Edge list for Kruskal
        self.adj_matrix[u][v] = w  # Adjacency matrix for Prim
        self.adj_matrix[v][u] = w

    # Find function for union-find (Kruskal's algorithm)
    def find(self, parent, i):
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])  # Path compression
        return parent[i]

    # Union function for union-by-rank
    def union(self, parent, rank, x, y):
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1

    # Kruskal's Algorithm
    def kruskal(self):
        self.graph = sorted(self.graph, key=lambda item: item[2])  # Sort edges by weight
        parent = list(range(self.V))
        rank = [0] * self.V
        result = []
        e, i = 0, 0
        minimum_cost = 0

        while e < self.V - 1 and i < len(self.graph):
            u, v, w = self.graph[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            if x != y:
                result.append([u, v, w])
                minimum_cost += w
                e += 1
                self.union(parent, rank, x, y)

        # Return the MST edges and the total cost
        return {"edges": result, "minimum_cost": minimum_cost}

    # Prim's Algorithm
    def prim(self):
        key = [sys.maxsize] * self.V
        parent = [None] * self.V
        mst_set = [False] * self.V
        key[0] = 0
        parent[0] = -1

        for cout in range(self.V):
            min_index = self.min_key(key, mst_set)
            mst_set[min_index] = True

            for v in range(self.V):
                if 0 < self.adj_matrix[min_index][v] < key[v] and not mst_set[v]:
                    key[v] = self.adj_matrix[min_index][v]
                    parent[v] = min_index

        # Construct the result in the same way as Kruskal's
        result = []
        minimum_cost = 0
        for i in range(1, self.V):
            u = parent[i]
            v = i
            w = self.adj_matrix[u][v]
            result.append([u, v, w])
            minimum_cost += w

        # Return the MST edges and the total cost
        return {"edges": result, "minimum_cost": minimum_cost}

    # Utility function to find the minimum key value (for Prim's)
    def min_key(self, key, mst_set):
        min_value = sys.maxsize
        min_index = -1
        for v in range(self.V):
            if key[v] < min_value and not mst_set[v]:
                min_value = key[v]
                min_index = v
        return min_index
