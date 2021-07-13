# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2021                                                     *
# *                                                                        *
# *                                                                        *
# * This library is free software; you can redistribute it and/or          *
# * modify it under the terms of the GNU Lesser General Public             *
# * License as published by the Free Software Foundation; either           *
# * version 2 of the License, or (at your option) any later version.       *
# *                                                                        *
# * This library is distributed in the hope that it will be useful,        *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# * Lesser General Public License for more details.                        *
# *                                                                        *
# * You should have received a copy of the GNU Lesser General Public       *
# * License along with this library; if not, If not, see                   *
# * <http://www.gnu.org/licenses/>.                                        *
# *                                                                        *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

import os,sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import Design456Init
from typing import List
from ThreeDWidgets.constant import FR_COLOR
# draw a line in 3D world
import math


def draw_Point(p1, color):
    try:
        so_separator = coin.SoSeparator()
        v = coin.SoVertexProperty()
        v.vertex.set1Value(0, p1)

        coords = coin.SoTransform()
        line = coin.SoLineSet()
        line.vertexProperty = v
        style = coin.SoDrawStyle()
        so_separator.addChild(style)
        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = color
        so_separator.addChild(col1)
        so_separator.addChild(line)
        so_separator.addChild(coords)
        return so_separator

    except Exception as err:
        App.Console.PrintError("'draw_point' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

def draw_square_frame(vectors: List[App.Vector] = [],color=(0,0,0),lineWidth=1):
    try:
        if len(vectors) !=4:
            ValueError ("4 Vertices must be given to the function")
        v=[]
        v.append( coin.SoVertexProperty())
        v[0].vertex.set1Value(0, vectors[0])
        v[0].vertex.set1Value(1, vectors[1])

        v.append( coin.SoVertexProperty())
        v[1].vertex.set1Value(0, vectors[1])
        v[1].vertex.set1Value(1, vectors[2])

        v.append( coin.SoVertexProperty())        
        v[2].vertex.set1Value(0, vectors[2])
        v[2].vertex.set1Value(1, vectors[3])
        
        v.append( coin.SoVertexProperty())        
        v[3].vertex.set1Value(0, vectors[3])
        v[3].vertex.set1Value(1, vectors[0])
        
        coords = coin.SoTransform()
        Totallines=[]
        for i in range(0,4):
            newSo = coin.SoSeparator()
            line  = coin.SoLineSet()
            line.vertexProperty = v[i]
            style = coin.SoDrawStyle()
            style.lineWidth = lineWidth
            newSo.addChild(style)
            col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
            col1.rgb = color
            newSo.addChild(col1)
            newSo.addChild(line)
            newSo.addChild(coords)
            Totallines.append(newSo)
        return Totallines

    except Exception as err:
        App.Console.PrintError("'draw_square' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

def draw_line(p1, p2, color, LineWidth):
    try:
        so_separator = coin.SoSeparator()
        v = coin.SoVertexProperty()
        v.vertex.set1Value(0, p1)
        v.vertex.set1Value(1, p2)
        coords = coin.SoTransform()
        line = coin.SoLineSet()
        line.vertexProperty = v
        style = coin.SoDrawStyle()
        style.lineWidth = LineWidth
        style.drawstyle=coin.SoDrawStyle.FILLED       #Drawing style could be FILLED,LINE, POINTS
        so_separator.addChild(style)
        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = color
        so_separator.addChild(col1)
        so_separator.addChild(line)
        so_separator.addChild(coords)
        return so_separator

    except Exception as err:
        App.Console.PrintError("'draw_line' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


#draw arrow 
def draw_arrow(_Points=[], _color=FR_COLOR.FR_BLACK, _ArrSize=1.0,_rotation=[1.0,1.0,1.0,0.0]):
    '''
    Draw a 3D arrow at the position given by the _Points and the color given by _color. 
    Scale it by the _ArrSize, and rotate it by the _rotation which consist of App.Vector(x,y,z) --the axis and 
    An angle in radians. 
    '''
    try:
        so_separatorRoot=coin.SoSeparator()
        so_separatorHead = coin.SoSeparator()
        so_separatorTail = coin.SoSeparator()
        transHead = coin.SoTranslation()   # decide at which position the object will be placed
        transTail = coin.SoTranslation()   # decide at which position the object will be placed
        transRoot= coin.SoTranslation()    # decide at which position the whole objects will be placed
        coordsRoot = coin.SoTransform()
        tempR= coin.SbVec3f()
        print(_rotation)
        print(len(_rotation))
        tempR.setValue(_rotation[0],_rotation[1],_rotation[2])
        cone=coin.SoCone()
        cone.bottomRadius= 3
        cone.height= 3

        cylinder=coin.SoCylinder()
        cylinder.height = 10
        cylinder.radius = 0.5
        p1=App.Vector(0.0,0.0,0.0)#(_Points[0])
        p2=App.Vector(p1.x,p1.y-5,p1.z)
        styleHead = coin.SoDrawStyle()
        styleTail = coin.SoDrawStyle()

        styleHead.style = coin.SoDrawStyle.LINES     #draw only frame not filled
        styleHead.lineWidth = 3
        styleTail.style = coin.SoDrawStyle.LINES     #draw only frame not filled
        styleTail.lineWidth = 2

        coordsRoot.scaleFactor.setValue([_ArrSize,_ArrSize,_ArrSize])
        coordsRoot.translation.setValue(App.Vector(0,0,0))

        coordsRoot.rotation.setValue(*tempR,_rotation[3]) #  SbRotation (const SbVec3f &axis, const float radians)
        transHead.translation.setValue(p1)
        transTail.translation.setValue(p2)
        transRoot.translation.setValue(_Points)

        color=coin.SoBaseColor(); 
        color.rgb=_color

        so_separatorHead.addChild(color)
        so_separatorTail.addChild(color)

        so_separatorHead.addChild(transHead)
        so_separatorTail.addChild(transTail)
        #so_separatorHead.addChild(styleHead)
        so_separatorHead.addChild(cone)

        #so_separatorTail.addChild(styleTail)
        so_separatorTail.addChild(cylinder)

        group= coin.SoSeparator()        
        group.addChild(transRoot)
        group.addChild(coordsRoot)
        group.addChild(so_separatorHead)
        group.addChild(so_separatorTail)
        return group
    except Exception as err:
        App.Console.PrintError("'draw_arrow' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

#draw a box
def draw_box(Points=[], color=(0.0,0.0,0.0), LineWidth=1):
    """
        Draw any box. This will be the base of all multi-point drawing.
        Curves, and arc is not here.
    """
    if len(Points) != 6:
        raise ValueError('Vertices must be 6')
    so_separator = coin.SoSeparator()
    v = coin.SoVertexProperty()
    coords = coin.SoTransform()
    p1=Points[0]
    p2=Points[1]
    p3=Points[2]
    p4=Points[3]
    p5=Points[4]
    p6=Points[5]
    square = coin.SbBox3f(p1, p2, p3, p4, p5, p6)
    square.vertexProperty = v
    style = coin.SoDrawStyle()
    style.lineWidth = LineWidth
    so_separator.addChild(style)
    so_separator.addChild(color)
    so_separator.addChild(square)
    so_separator.addChild(coords)
    return draw_square

# Draw a polygon face in the 3D Coin
def draw_polygon(vector,color=FR_COLOR.FR_BLUEG, LineWidth=1.0):
    """ Draw a square and return the SoSeparator"""
    node = coin.SoSeparator()
    coords = coin.SoCoordinate3()
    length=len(vector)
    for i in range(0,length+1):
        coords.point.set1Value(i,vector[i])
    
    col=coin.SoBaseColor()
    col.rgb= color
    style = coin.SoDrawStyle()
    style.lineWidth = LineWidth
    faceset = coin.SoFaceSet()
    faceset.numVertices.set1Value(0, 4)
    node.addChild(col)
    node.addChild(style)
    node.addChild(coords)
    node.addChild(faceset)
    return node

#Draw a square face in the 3D Coin
def draw_square(vertices, color=(0.0,0.0,0.0), LineWidth=1.0):
    if len(vertices) != 4:
        raise ValueError('Vertices must be 4')
    return draw_polygon(vertices,color,LineWidth)


#this function is just an example showing how you can affect the drawing
def createFrameShape():
    sg = Gui.ActiveDocument.ActiveView.getSceneGraph()
    root=coin.SoSeparator()
    drawStyle=coin.SoDrawStyle()
    drawStyle.style=coin.SoDrawStyle.LINES
    root.addChild(drawStyle)
    shapeHints=coin.SoShapeHints()
    shapeHints.vertexOrdering=coin.SoShapeHints.COUNTERCLOCKWISE
    shapeHints.shapeType=coin.SoShapeHints.SOLID
    root.addChild(shapeHints)
    lightModel=coin.SoLightModel()
    lightModel.model=coin.SoLightModel.BASE_COLOR
    root.addChild(lightModel)

    cone=coin.SoCube ()
    root.addChild(cone)
    sg.addChild(root)

#Load a SVG image to the coin3D
def loadImageTo3D(filename,Bsize, location):
    svg = coin.SoTexture2()
    svg.filename = filename
    box = coin.SoVRMLBox()
    box.size = Bsize    #(2,2,0)
    imagePos = coin.SoTransform()
    imagePos.translation.setValue(location) #([10,0,0])
    imagePos.rotation = coin.SbRotation(0,0,0,0)
    image = coin.SoSeparator()
    image.addChild(imagePos)
    image.addChild(svg)
    image.addChild(box)
    return image        # Add this to the senegraph to show the picture.
#todo fixme
def drawCurve(knots, data):
    array = {[0. , 0. , 0.01, 0.07, 0.18, 0.36, 0.5 , 0.71, 1. ],
             [0. , 0.02, 0.05, 0.09, 0.1 , 0.08, 0.06, 0.04, 0. ],
             [0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. ],
             [1. , 1. , 1. , 1. , 1. , 1. , 1. , 1. , 1. ]
             }

    """The knot vector    """
    knots = ([0] * 5 + [1] * 2 + [2] *2 + [3] * 5)

    curveSep = coin.SoSeparator()
    complexity = coin.SoComplexity()
    controlPts = coin.SoCoordinate4()
    curve = coin.SoNurbsCurve()
    controlPts.point.setValues(0, array.shape[1], array.T.tolist())
    curve.numControlPoints = array.shape[1]
    curve.knotVector.setValues(0, len(knots), knots)
    curveSep += [complexity, controlPts, curve]