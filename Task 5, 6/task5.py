# importing necessary libraries
import csv

class AdjNode:
    def __init__(self, value):
        self.vertex = value
        self.next = None

# class to store the given tree
class Graph:
    def __init__(self, num):
        self.V = num
        self.graph = [None] * self.V
        self.visited = set()
        self.pre = [None] * self.V
        self.low = [1] * self.V
        self.sign = [0] * self.V
        self.parent = [None] * self.V
        self.st = list()
        self.curr = 1

    # function that adds a node with id "d" at end of the adjacency list of vertex s and vice versa
    def add_edge(self, s, d):
        node = AdjNode(d)
        node.next = self.graph[s]
        self.graph[s] = node

        node = AdjNode(s)
        node.next = self.graph[d]
        self.graph[d] = node

    # depth first search traversal. parameter p indicates the pass
    def dfs(self, v, p):
        if p == 1:
            self.pre[v] = self.curr
            self.low[v] = self.curr
            self.curr += 1

        self.visited.add(v)

        childItr = tree.graph[v]
        if p == 1:
            while childItr:
                if childItr.vertex in self.visited:
                    self.low[v] = min(self.pre[childItr.vertex], self.low[v])
                childItr = childItr.next
        elif v != s and v != t:
            self.st.insert(self.st.index(self.parent[v]) + self.sign[self.low[v]], v)
            self.sign[self.parent[v]] = 1 - self.sign[self.low[v]]

        childItr = tree.graph[v]
        while childItr:
            if childItr.vertex not in self.visited:
                if p == 1:
                    self.parent[childItr.vertex] = v
                self.low[v] = min(self.low[v], self.dfs(childItr.vertex, p))
            childItr = childItr.next

        return self.low[v]

    def generateSTNumbering(self, s, t):
        # initial list = [s,t]
        self.st.append(s)
        self.st.append(t)
        # sign of s is -
        self.sign[s] = 0
        # clearing data stored in first pass
        self.visited.clear()
        # 2 as argument indicates second pass
        self.dfs(s, 2)

    def validate(self):
        print("preorder numbering ", end="- ")
        for i in range(1, self.V):
            print(self.pre[i], end=" ")

        print("\nlow values ", end="- ")
        for i in range(1, self.V):
            print(self.low[i], end=" ")

        print("\nst-Numbering ", end="- ")
        for i in self.st:
            print(i, end=" ")


with open('graphInput.csv', mode='r') as file:
    csvFile = list(csv.reader(file))
    # first line of input gives the number of vertices and edges
    vertices = int(csvFile[0][0])
    edges = int(csvFile[0][1])
    tree = Graph(vertices + 1)

    # then subsequent lines gives end-vertices of each edge
    # assumed that first line has both s and t
    s = int(csvFile[1][0])
    t = int(csvFile[1][1])

    for i in range(1, edges):
        tree.add_edge(int(csvFile[i + 1][0]), int(csvFile[i + 1][1]))
    tree.add_edge(s, t)

    # 1 as argument indicates first pass, where low values and pre-ordering is computed
    tree.dfs(s, 1)
    # function that calls dfs function in second pass
    tree.generateSTNumbering(s, t)
    # printing computed low-values, numbering of the vertices
    tree.validate()
