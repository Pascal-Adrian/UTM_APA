from collections import defaultdict, deque
class Graph:

    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def __dfs_helper(self, v, visited):
        visited.add(v)

        for neighbour in self.graph[v]:
            if neighbour not in visited:
                self.__dfs_helper(neighbour, visited)

    def DFS(self, v):
        visited = set()
        self.__dfs_helper(v, visited)
        return visited

    def BFS(self, v):
        order = []
        # Create a queue for BFS
        queue = deque()
        visited = [False] * (max(self.graph.keys()) + 1)

        # Mark the current node as visited and enqueue it
        visited[v] = True
        queue.append(v)

        # Iterate over the queue
        while queue:
            # Dequeue a vertex from queue and print it
            currentNode = queue.popleft()
            order.append(currentNode)

            # Get all adjacent vertices of the dequeued vertex currentNode
            # If an adjacent has not been visited, then mark it visited and enqueue it
            for neighbor in self.graph[currentNode]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)

        return order

    def clear(self):
        self.graph = defaultdict(list)