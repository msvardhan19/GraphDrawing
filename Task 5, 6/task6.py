# importing necessary libraries
import csv
import numpy
from collections import defaultdict
from functools import cmp_to_key
multiplier = 50

# function to create a node (label same as the id) for given x coordinate and y coordinate
def createNode(nodeID, xCoord, yCoord):
    f.write('''
        <node id="{}">
        <data key="d5"/>
        <data key="d6">
        <y:ShapeNode>
        <y:Geometry height="30.0" width="30.0" x="{}" y="{}"/>
        <y:Fill color="#FFCC00" transparent="false"/>
        <y:BorderStyle color="#000000" raised="false" type="line" width="1.0"/>
        <y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="17.96875" horizontalTextPosition="center" iconTextGap="4" modelName="custom" textColor="#000000" verticalTextPosition="bottom" visible="true" width="11.634765625" x="9.1826171875" xml:space="preserve" y="6.015625">{}<y:LabelModel><y:SmartNodeLabelModel distance="4.0"/></y:LabelModel><y:ModelParameter><y:SmartNodeLabelModelParameter labelRatioX="0.0" labelRatioY="0.0" nodeRatioX="0.0" nodeRatioY="0.0" offsetX="0.0" offsetY="0.0" upX="0.0" upY="-1.0"/></y:ModelParameter></y:NodeLabel>
        <y:Shape type="circle"/>
        </y:ShapeNode>
        </data>
        </node>
        '''.format(nodeID, xCoord - 15, yCoord - 15, nodeID)
    )

# function to create an edge between source and target nodes. also creates bends as provided in argument
def createEdge(edgeID, source, target, bends):
    f.write('''
        <edge id="{}" source="{}" target="{}">
        <data key="d9"/>
        <data key="d10">
        <y:PolyLineEdge>
        <y:Path sx="0.0" sy="0.0" tx="0.0" ty="0.0">'''.format(edgeID, source, target)
    )

    for bend in bends:
        f.write('''
            <y:Point x = "{}" y = "{}"/>
            '''.format(bend[0], bend[1])
        )

    f.write('''</y:Path>
        <y:LineStyle color="#000000" type="line" width="1.0"/>
        <y:Arrows source="none" target="none"/>
        <y:BendStyle smoothed="false"/>
        </y:PolyLineEdge>
        </data>
        </edge>
        '''
    )


def coordsComp1(a, b):
    if a[1] < b[1]:
        return 1
    elif a[1] > b[1]:
        return -1
    elif a[0] < b[0]:
        return -1
    else:
        return 1


def coordsComp2(a, b):
    if a[1] < b[1]:
        return 1
    elif a[1] > b[1]:
        return -1
    elif a[0] < b[0]:
        return 1
    else:
        return -1


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
        self.left = [0] * self.V
        self.right = [0] * self.V
        self.xCoord = [None] * self.V
        self.yCoord = [None] * self.V
        self.edgePos = [[] for i in range(self.V)]
        self.stPos = [0] * self.V
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


inputFile = input("Enter the graph input file name in csv format: ")
outputFile = inputFile[:-3] + "graphml"

with open(inputFile, mode='r') as file:
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

    # stPos(v) indicates position of v in the st-numbering
    for i in range(vertices):
        tree.stPos[tree.st[i]] = i

    for i in range(1, vertices + 1):
        childItr = tree.graph[i]
        while childItr:
            # an edge u,v(same order in st) contributes to right[u] and left[v]
            if tree.stPos[i] < tree.stPos[childItr.vertex]:
                tree.right[i] += 1
                tree.left[childItr.vertex] += 1
            childItr = childItr.next

    print("\nLeft-Right Values")
    for i in range(1, vertices + 1):
        print(f"{i}: ({tree.left[i]},{tree.right[i]})")

    tree.xCoord[s] = 0
    bendToAdd = []
    for i in range(vertices):
        v = tree.st[i]
        childItr = tree.graph[v]

        # in/out Vertices is the list of all vertices, the current vertex has incoming/outgoing edge to
        inVertices = []
        outVertices = []

        # inPositions is the list of coordinates of all inVertices
        inPositions = []

        outColumn = [[0, 1, -1, 2], [0, 1, -1], [0, 1], [0]]
        displaceBy = [[0, 0, 0, 0], [0, 1, -1], [0, 1], [0]]

        while childItr:
            if tree.stPos[childItr.vertex] > i:
                outVertices.append(childItr.vertex)
            childItr = childItr.next

        for j in tree.edgePos[v]:
            inPositions.append(j[1][0])
            inVertices.append(j[0])

        inVertices = [x for _, x in sorted(zip(inPositions, inVertices))]
        inPositions.sort()

        tree.yCoord[v] = -multiplier * i
        if len(inPositions) == 1:
            tree.xCoord[v] = inPositions[0]
        elif len(inPositions) > 1:
            tree.xCoord[v] = inPositions[1]

        for j in range(len(outVertices)):
            if displaceBy[tree.left[v]][j] != 0:
                for k in range(1, vertices + 1):
                    if tree.xCoord[k] is not None and numpy.sign(tree.xCoord[k] - tree.xCoord[v]) == numpy.sign(displaceBy[tree.left[v]][j]):
                        tree.xCoord[k] = tree.xCoord[k] + displaceBy[tree.left[v]][j] * multiplier
                    for ele in range(len(tree.edgePos[k])):
                        if numpy.sign(tree.edgePos[k][ele][1][0] - tree.xCoord[v]) == numpy.sign(displaceBy[tree.left[v]][j]):
                            tree.edgePos[k][ele] = (tree.edgePos[k][ele][0], (tree.edgePos[k][ele][1][0] +
                                                     displaceBy[tree.left[v]][j] * multiplier, tree.edgePos[k][ele][1][1]))
            if j < 3:
                tree.edgePos[outVertices[j]].append((v, (tree.xCoord[v] + outColumn[tree.left[v]][j] * multiplier, tree.yCoord[v])))
            else:
                tree.edgePos[outVertices[j]].append((v, (tree.xCoord[v], tree.yCoord[v] + multiplier)))
                tree.edgePos[outVertices[j]].append((v, (tree.xCoord[v] + 2 * multiplier, tree.yCoord[v] + multiplier)))

        for j in range(len(inVertices)):
            firstBend = -1
            for k in tree.edgePos[v]:
                if k[0] == inVertices[j]:
                    firstBend = k[1][0]

            if j < 3:
                tree.edgePos[v].append((inVertices[j], (firstBend, tree.yCoord[v])))
            else:
                tree.edgePos[v].append((inVertices[j], (firstBend, tree.yCoord[v] - multiplier)))
                tree.edgePos[v].append((inVertices[j], (tree.xCoord[v], tree.yCoord[v] - multiplier)))

    print("\nFinal Coordinates")
    for i in range(1, vertices + 1):
        print(f"{i}: ({tree.xCoord[i]},{tree.yCoord[i]})")

    with open(outputFile, "w") as f:
        f.write('''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:java="http://www.yworks.com/xml/yfiles-common/1.0/java" xmlns:sys="http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0" xmlns:x="http://www.yworks.com/xml/yfiles-common/markup/2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:y="http://www.yworks.com/xml/graphml" xmlns:yed="http://www.yworks.com/xml/yed/3" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd">
            <!--Created by yEd 3.22-->
            <key attr.name="Description" attr.type="string" for="graph" id="d0"/>
            <key for="port" id="d1" yfiles.type="portgraphics"/>
            <key for="port" id="d2" yfiles.type="portgeometry"/>
            <key for="port" id="d3" yfiles.type="portuserdata"/>
            <key attr.name="url" attr.type="string" for="node" id="d4"/>
            <key attr.name="description" attr.type="string" for="node" id="d5"/>
            <key for="node" id="d6" yfiles.type="nodegraphics"/>
            <key for="graphml" id="d7" yfiles.type="resources"/>
            <key attr.name="url" attr.type="string" for="edge" id="d8"/>
            <key attr.name="description" attr.type="string" for="edge" id="d9"/>
            <key for="edge" id="d10" yfiles.type="edgegraphics"/>
            <graph edgedefault="directed" id="G">
            <data key="d0"/>
            '''
        )

        for i in range(1, vertices + 1):
            createNode(i, tree.xCoord[i], tree.yCoord[i])

        edgeID = 1
        for v in range(1, vertices + 1):
            d = defaultdict(list)

            for [u, bend] in tree.edgePos[v]:
                if bend[0] == tree.xCoord[u] and bend[1] == tree.yCoord[u]:
                    bend = ()
                elif bend[0] == tree.xCoord[v] and bend[1] == tree.yCoord[v]:
                    bend = ()
                d[u].append(bend)

            for [u, bends] in d.items():
                bends = [x for x in bends if x != ()]
                if tree.xCoord[u] < tree.xCoord[v]:
                    bends.sort(key=cmp_to_key(coordsComp1))
                else:
                    bends.sort(key=cmp_to_key(coordsComp2))
                createEdge(edgeID, u, v, bends)
                edgeID += 1

        f.write('''
            </graph>
            </graphml>
            '''
        )