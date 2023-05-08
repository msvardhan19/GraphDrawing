# importing necessary libraries
import csv

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

f = open("task1,2.graphml", "w")

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

with open('task1nodeInput.csv', mode='r') as file:
    csvFile = csv.reader(file)
    # all lines in input csv file follow this format: node id, x coordinate, y coordinate
    for line in csvFile:
        createNode(line[0], line[1], line[2])

with open('task1edgeInput.csv', mode='r') as file:
    csvFile = list(csv.reader(file))
    # first line of input file consists number of edges
    edges = int(csvFile[0][0])
    # rest of the lines have both the source and target separated by comma
    for i in range(1, edges + 1):
        createEdge(i, csvFile[i][0], csvFile[i][1])

f.write('''
    </graph>
    </graphml>
  '''
        )

f.close()