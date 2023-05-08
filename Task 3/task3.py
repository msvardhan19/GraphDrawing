# importing necessary libraries
import csv
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
        <y:Shape type="rectangle"/>
        </y:ShapeNode>
      </data>
      </node>
    '''.format(nodeID, xCoord, yCoord, nodeID)
            )

# function to create an edge between source and target nodes
def createEdge(edgeID, source, target):
    f.write('''
      <edge id="{}" source="{}" target="{}">
      <data key="d9"/>
      <data key="d10">
        <y:PolyLineEdge>
        <y:Path sx="0.0" sy="0.0" tx="0.0" ty="0.0"/>
        <y:LineStyle color="#000000" type="line" width="1.0"/>
        <y:Arrows source="none" target="none"/>
        <y:BendStyle smoothed="false"/>
        </y:PolyLineEdge>
      </data>
      </edge>
      '''.format(edgeID, source, target)
    )


class AdjNode:
    def __init__(self, value):
        self.vertex = value
        self.next = None


# class to store the given tree
class Graph:
    def __init__(self, num):
        self.V = num
        self.adjList = [None] * self.V

    # function that adds a node with id "d" at end of the adjacency list of vertex s and vice versa
    def add_edge(self, s, d):
        node = AdjNode(d)
        node.next = self.adjList[s]
        self.adjList[s] = node

        node = AdjNode(s)
        node.next = self.adjList[d]
        self.adjList[d] = node

    # at end of this dfs traversal, all vertices are assigned coordinates in the cartesian plane
    def dfs(self, v, parent, childCount, x, y):
        if childCount == 1:
            y += 2 * multiplier
        elif childCount == 2:
            x += multiplier

        createNode(v, x, y)
        childCount = 0
        childItr = tree.adjList[v]
        while childItr:
            if childItr.vertex != parent:
                childCount += 1
                x = self.dfs(childItr.vertex, v, childCount, x, y)
            childItr = childItr.next
        return x


inputFile = input("Enter the graph input file name in csv format: ")
outputFile = inputFile[:-3] + "graphml"

with open(inputFile, mode='r') as file:
    with open(outputFile, mode='w') as f:
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
        ''')

        csvFile = list(csv.reader(file))
        # first line of input file gives the number of edges
        vertices = int(csvFile[0][0])

        # creating a tree with one extra vertex to avoid zero indexing
        tree = Graph(vertices + 1)

        # edge relations are stored in an adjacency list
        # assumed that all edges are undirected
        for i in range(1, vertices):
            tree.add_edge(int(csvFile[i][0]), int(csvFile[i][1]))

        # start the dfs traversal with the vertex in the first given edge as root
        # also assign (0,0) to the root
        # -1 indicates that the root doesn't have any parent
        tree.dfs(int(csvFile[1][0]), -1, 0, 0, 0)

        for i in range(1, vertices):
            createEdge(i, int(csvFile[i][0]), int(csvFile[i][1]))

        f.write('''
            </graph>
            </graphml>
          ''')