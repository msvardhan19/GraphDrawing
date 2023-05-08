import csv
from math import sin, cos, pi
from queue import Queue


def createNode(nodeID, xCoord, yCoord):
    f.write('''
        <node id="{}">
        <data key="d5"/>
        <data key="d6">
        <y:ShapeNode>
        <y:Geometry height="20.0" width="20.0" x="{}" y="{}"/>
        <y:Fill color="#FFCC00" transparent="false"/>
        <y:BorderStyle color="#000000" raised="false" type="line" width="1.0"/>
        <y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="12" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="17.96875" horizontalTextPosition="center" iconTextGap="4" modelName="custom" textColor="#000000" verticalTextPosition="bottom" visible="true" width="11.634765625" x="9.1826171875" xml:space="preserve" y="6.015625">{}<y:LabelModel><y:SmartNodeLabelModel distance="4.0"/></y:LabelModel><y:ModelParameter><y:SmartNodeLabelModelParameter labelRatioX="0.0" labelRatioY="0.0" nodeRatioX="0.0" nodeRatioY="0.0" offsetX="0.0" offsetY="0.0" upX="0.0" upY="-1.0"/></y:ModelParameter></y:NodeLabel>
        <y:Shape type="circle"/>
        </y:ShapeNode>
        </data>
        </node>
        '''.format(nodeID, xCoord - 10, yCoord - 10, nodeID)
    )


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


class AdjNode:
    def __init__(self, value):
        self.vertex = value
        self.next = None


class Graph:
    def __init__(self, num):
        self.V = num
        self.graph = [None] * self.V
        self.parent = [None] * self.V
        self.childCount = [0] * self.V
        self.factor = [1] * self.V
        self.visited = [False] * self.V
        self.theta = [None] * self.V
        self.xCoord = [None] * self.V
        self.yCoord = [None] * self.V

    def add_edge(self, s, d):
        node = AdjNode(d)
        node.next = self.graph[s]
        self.graph[s] = node

        node = AdjNode(s)
        node.next = self.graph[d]
        self.graph[d] = node

    def PLANET(self, s):
        self.xCoord[s] = 0
        self.yCoord[s] = 0
        self.theta[s] = 0
        self.factor[s] = 1
        self.visited[s] = True
        d = 0
        epsilon = 100

        q = Queue()
        childItr = self.graph[s]
        while childItr:
            self.childCount[s] = self.childCount[s] + 1
            self.parent[childItr.vertex] = (s, self.childCount[s])
            self.visited[childItr.vertex] = True
            q.put(childItr.vertex)
            childItr = childItr.next

        while not q.empty():
            d = d + 1
            temp = Queue()
            while not q.empty():
                v = q.get()
                p = self.parent[v][0]
                n = self.childCount[p]
                self.factor[v] = self.factor[p] * n
                if d == 1:
                    self.theta[v] = (2 * (self.parent[v][1] - 1) * pi)/n
                else:
                    if n == 1:
                        self.theta[v] = self.theta[p]
                    elif d > 2 and self.theta[p] < self.theta[self.parent[p][0]]:
                        self.theta[v] = self.theta[p] + ((2 * self.parent[v][1] - 1) * pi)/(n * self.factor[p])
                    elif d > 2 and self.theta[p] > self.theta[self.parent[p][0]]:
                        self.theta[v] = self.theta[p] - ((2 * self.parent[v][1] - 1) * pi)/(n * self.factor[p])
                    else:
                        self.theta[v] = self.theta[p] - (pi * (n - 1))/(n * self.factor[p]) + \
                                        (2 * (self.parent[v][1] - 1) * pi)/(n * self.factor[p])

                if self.xCoord[p] > 0:
                    self.xCoord[v] = self.xCoord[p] + epsilon * cos(self.theta[v] - self.theta[p])
                else:
                    self.xCoord[v] = self.xCoord[p] - epsilon * cos(self.theta[v] - self.theta[p])
                if self.yCoord[p] > 0:
                    self.yCoord[v] = self.yCoord[p] + epsilon * sin(self.theta[v] - self.theta[p])
                else:
                    self.yCoord[v] = self.yCoord[p] - epsilon * sin(self.theta[v] - self.theta[p])

                childItr = self.graph[v]
                while childItr:
                    if not self.visited[childItr.vertex]:
                        self.childCount[v] = self.childCount[v] + 1
                        self.parent[childItr.vertex] = (v, self.childCount[v])
                        self.visited[childItr.vertex] = True
                        temp.put(childItr.vertex)
                    childItr = childItr.next
            q = temp


inputFile = input("Enter the graph input file name in csv format: ")
outputFile = inputFile[:-3] + "graphml"

with open(inputFile, mode='r') as file:
    csvFile = list(csv.reader(file))
    vertices = int(csvFile[0][0])
    tree = Graph(vertices + 1)
    s = int(csvFile[0][1])
    for i in range(1, vertices):
        tree.add_edge(int(csvFile[i][0]), int(csvFile[i][1]))

    tree.PLANET(s)
    print("Final Coordinates")
    for i in range(1, vertices + 1):
        print(f"{i}: ({tree.xCoord[i]}, {tree.yCoord[i]})")

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
            childItr = tree.graph[v]
            while childItr:
                if childItr.vertex < v:
                    createEdge(edgeID, childItr.vertex, v, [])
                    edgeID = edgeID + 1
                childItr = childItr.next

        f.write('''
            </graph>
            </graphml>
            '''
        )