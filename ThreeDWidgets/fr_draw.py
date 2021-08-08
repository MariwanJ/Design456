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

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import Design456Init
from typing import List
from ThreeDWidgets.constant import FR_COLOR
# draw a line in 3D world
import math
from dataclasses import dataclass


@dataclass
class userDataObject:
    def __init__(self):
        """
            Data object used to simplify sending data to different drawing objects.
        """
        self.Vectors: List[App.Vector] = []                     # the vertices 
        self.Scale: int = 1.0                                   # scale 
        self.Radius: float = 0.0                                # radius 
        self.Height: float = 0.0                                # height
        self.Color: List[float, float, float] = []              # color
        self.LineWidth: float = 1.0                             # drawing line width
        self.Transparency: float = 50.0                         # transparency
        self.Rotation: List[(float, float, float), float] = []  # rotation axis and angle 

"""
Example using draw_Point(p1,color):


        
"""
def draw_Point(p1,size=0.1, color=FR_COLOR.FR_GOLD, type=0):
    """[Draw a point. The point could be any of cubic, or sphere shapes. Default is Cubic]

    Args:
        p1 ([type]): [Position of the point]
        color ([type], optional): [Color of the point]. Defaults to FR_COLOR.FR_GOLD.
        type (int, optional): [Point's shape. Either Cubic=0 or Sphere =1 ]. Defaults to 0.

    Returns:
        [type]: [description]
        
    EXAMPLE: 
        from pivy import coin
        import fr_draw as d 

        sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
        for i in range( 3, 100):
            root=d.draw_Point(App.Vector(i,i,i) ,0.09 ,(0.5,0.5,1),1 )
            sg.addChild(root)
    """
    try:
        so_separator = coin.SoSeparator()
        coords = coin.SoTranslation()
        coords.translation.setValue(p1)
        if type==0:
            point = coin.SoCube()
            point.width=size
            point.height=size
            point.depth=size
        elif type==1:
            point = coin.SoSphere()
            point.radius=size
        
        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = color
        so_separator.addChild(col1)
        so_separator.addChild(coords)
        so_separator.addChild(point)
        return so_separator

    except Exception as err:
        App.Console.PrintError("'draw_point' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def draw_square_frame(vectors: List[App.Vector] = [], color=(0, 0, 0), lineWidth=1):
    try:
        if len(vectors) != 4:
            ValueError("4 Vertices must be given to the function")
        v = []
        v.append(coin.SoVertexProperty())
        v[0].vertex.set1Value(0, vectors[0])
        v[0].vertex.set1Value(1, vectors[1])

        v.append(coin.SoVertexProperty())
        v[1].vertex.set1Value(0, vectors[1])
        v[1].vertex.set1Value(1, vectors[2])

        v.append(coin.SoVertexProperty())
        v[2].vertex.set1Value(0, vectors[2])
        v[2].vertex.set1Value(1, vectors[3])

        v.append(coin.SoVertexProperty())
        v[3].vertex.set1Value(0, vectors[3])
        v[3].vertex.set1Value(1, vectors[0])

        coords = coin.SoTransform()
        Totallines = []
        for i in range(0, 4):
            newSo = coin.SoSeparator()
            line = coin.SoLineSet()
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
        # Drawing style could be FILLED,LINE, POINTS
        style.drawstyle = coin.SoDrawStyle.FILLED
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


# draw arrow
def draw_arrow(_Points=[], _color=FR_COLOR.FR_BLACK, _ArrSize=1.0, _rotation=[1.0, 1.0, 1.0, 0.0]):
    '''
    Draw a 3D arrow at the position given by the _Points and the color given by _color. 
    Scale it by the _ArrSize, and rotate it by the _rotation which consist of App.Vector(x,y,z) --the axis and 
    An angle in radians. 
    '''
    try:
        so_separatorRoot = coin.SoSeparator()
        so_separatorHead = coin.SoSeparator()
        so_separatorTail = coin.SoSeparator()
        # decide at which position the object will be placed
        transHead = coin.SoTranslation()
        # decide at which position the object will be placed
        transTail = coin.SoTranslation()
        # decide at which position the whole objects will be placed
        transRoot = coin.SoTranslation()
        coordsRoot = coin.SoTransform()
        tempR = coin.SbVec3f()
        print(_rotation)
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        cone = coin.SoCone()
        cone.bottomRadius = 3
        cone.height = 3

        cylinder = coin.SoCylinder()
        cylinder.height = 10
        cylinder.radius = 0.5
        p1 = App.Vector(0.0, 0.0, 0.0)  # (_Points[0])
        p2 = App.Vector(p1.x, p1.y-5, p1.z)
        styleHead = coin.SoDrawStyle()
        styleTail = coin.SoDrawStyle()

        styleHead.style = coin.SoDrawStyle.LINES  # draw only frame not filled
        styleHead.lineWidth = 3
        styleTail.style = coin.SoDrawStyle.LINES  # draw only frame not filled
        styleTail.lineWidth = 2

        coordsRoot.scaleFactor.setValue([_ArrSize, _ArrSize, _ArrSize])
        coordsRoot.translation.setValue(App.Vector(0, 0, 0))

        # SbRotation (const SbVec3f &axis, const float radians)
        coordsRoot.rotation.setValue(*tempR, _rotation[3])
        transHead.translation.setValue(p1)
        transTail.translation.setValue(p2)
        transRoot.translation.setValue(_Points)

        color = coin.SoBaseColor()
        color.rgb = _color

        so_separatorHead.addChild(color)
        so_separatorTail.addChild(color)

        so_separatorHead.addChild(transHead)
        so_separatorTail.addChild(transTail)
        # so_separatorHead.addChild(styleHead)
        so_separatorHead.addChild(cone)

        # so_separatorTail.addChild(styleTail)
        so_separatorTail.addChild(cylinder)

        group = coin.SoSeparator()
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


def draw_box(p1=App.Vector(0,0,0),size=App.Vector(1,1,1), color=FR_COLOR.FR_GOLD, Texture="",style=0, LineWidth=1, LinePattern=0xffff):
    """[Use this function to draw a box. The box-style could be configured.]

    Args:
        p1 ([App.Vector]): [Defines the position of the vector ] . Defaults to App.Vector(0,0,0)
        size ([App.Vector], optional): [Defines the size of the box]. Defaults to App.Vector(1,1,1).
        color ([tuple], optional): [Box color as defined in FR_COLOR]. Defaults to FR_COLOR.FR_GOLD.
        texture (None, optional): [File name of the texture image]. Defaults to Null string.
        style (int, optional): [Box style: Filed=0, Lines ,Points,Invisible]. Defaults to 0.
        LineWidth (int, optional): [Line width: applicable only when you have line style]. Defaults to 1.
        LinePattern (hexadecimal, optional): [Defines if you have dashed lines or continuse line]. Defaults to 0xffff.

    Returns:
        [type]: [description]
    
    Example : 
    from pivy import coin
    import math
    import fr_draw as d 
    import time
    from PySide import QtCore,QtGui

    sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()

    a=range(0,35)
    arev=reversed(a)
    while(True):
        for i in a:
            root=d.draw_box(App.Vector(0,0,0) ,App.Vector(i,i,i), (0,0.5,1), "",1,0, 0xffff)
            sg.addChild(root)
            QtGui.QApplication.processEvents()
            FreeCADGui.updateGui()
            time.sleep(0.1)
            sg.removeChild(root)
            QtGui.QApplication.processEvents()

        for i in arev:
            root=d.draw_box(App.Vector(0,0,0) ,App.Vector(i,i,i), (0,0.5,1), "",1,0, 0xffff)
            sg.addChild(root)
            QtGui.QApplication.processEvents()
            FreeCADGui.updateGui()
            time.sleep(0.1)
            sg.removeChild(root)
            QtGui.QApplication.processEvents()

    """
    try:
        root = coin.SoSeparator()
        coords = coin.SoTranslation()
        coords.translation.setValue(p1)
       
        texture=coin.SoTexture2()
        texture.filename=Texture
        
        boxstyle=coin.SoDrawStyle()
        boxstyle.style=style
        boxstyle.lineWidth=LineWidth
        boxstyle.linePattern=LinePattern
        
        box = coin.SoCube()
        box.width=size.x
        box.height=size.y
        box.depth=size.z
        

        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = color
        root.addChild(col1)
        root.addChild(coords)
        root.addChild(boxstyle)
        
        #root.addChild(texture)
        root.addChild(box)
        return root
    
    except Exception as err:
        App.Console.PrintError("'draw_point' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)



# draw a Four sided shape
class draw_fourSidedShape:
    '''
        Create a four sided shape using four vertices.
    '''

    def __init__(self, Points=[], color=FR_COLOR.FR_BLUE, texture="",use_texture=False, LineWidth=1):
        """ 
            Draw any four sided shape,
            This will be the base of all multi-points drawing.

        Args:
            Points (list, optional): [Vertices to be used to draw the shape]. Defaults to [].
            color (tuple, optional): [color value as per FR_COLOR]. Defaults to FR_COLOR.FR_BLUE.
            use_texture (bool, optional): [drawing should have a texture]. Defaults to False.
            texture (string, optional): [File name of the texture]. Defaults to False.
            LineWidth (int, optional): [width of the line]. Defaults to 1.

        Raises:
            ValueError: [4 vertices must be applied to the class]

        Returns:
            [coin.SoSeparator]: [created drawing]
        """
        self.faces = []  # Keep the 6 faces
        self.Points = Points
        self.color = color
        self.use_texture = use_texture
        self.texture=texture
        self.lineWidth = LineWidth

    def Activated(self):
        if len(self.Points) != 4:
            raise ValueError('Vertices must be 4')
        so_separator = coin.SoSeparator()
        v = coin.SoVertexProperty()
        coords = coin.SoTransform()

        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = self.color

        FourSidedShape = coin.SoSeparator()
        coords = coin.SoCoordinate3()
        for i in range(0, len(self.Points)):
            coords.point.set1Value(i, self.Points[i])
        if self.use_texture ==True :
            textureCoords = coin.SoTextureCoordinate2()
            textureCoords.point.set1Value(0, 0, 0)
            textureCoords.point.set1Value(1, 1, 0)
            textureCoords.point.set1Value(2, 1, 1)
            textureCoords.point.set1Value(3, 0, 1)
            texture=coin.SoTexture2()
            if self.texture is not "":
                texture.filename=self.texture
            else:
                texture=self.genTextureImage()
        _face = coin.SoFaceSet()
        _face.numVertices.set1Value(0, 4)
        FourSidedShape.addChild(coords)      
        if self.use_texture == True:
            FourSidedShape.addChild(textureCoords)
            FourSidedShape.addChild(texture)
        FourSidedShape.addChild(_face)
        return FourSidedShape

    def genTextureImage(self):
        imgsize = coin.SbVec2s(5, 5)
        width = imgsize[0]
        height = imgsize[1]
        imgData = ''

        for i in range(height):
            for j in range(width):
                #imgData=imgData+((chr(134)).encode('latin-1'))
                imgData=imgData+chr(180)
        coinSoImage = coin.SoSFImage()
        coinSoImage.setValue(imgsize, 1, imgData)
        return coinSoImage


# Draw a NurbsFace face in the 3D Coin
class draw_NurbsFace:

    def __init__(self, Points=[], color=FR_COLOR.FR_RED, use_texture=False, LineWidth=1):
        """ 
            Draw any four sided shape,
            This will be the base of all multi-points drawing.
        Args:
            Points (list, optional): [description]. Defaults to [].
            color (tuple, optional): [description]. Defaults to (0.0,0.0,0.0).
            use_texture (bool, optional): [description]. Defaults to False.
            LineWidth (int, optional): [description]. Defaults to 1.

        Raises:
            ValueError: [4 vertices must be applied to the class]

        Returns:
            [coin.SoSeparator]: [created drawing]
        """
        self.faces = []  # Keep the 6 faces
        self.Points = Points
        self.color = color
        self.use_texture = use_texture
        self.lineWidth = LineWidth

    def Activated(self):
        if len(self.Points) < 4:
            raise ValueError('Use the function with 4 vertices')
        material = coin.SoMaterial()
        material.transparency.setValue(0.0)
        material.diffuseColor.setValue(coin.SbColor(self.color))
        material.specularColor.setValue(coin.SbColor(1, 1, 1))
        material.shininess.setValue(1.0)

        sizeOfPointsArray = len(self.Points)
        sqrtSize = int(math.sqrt(sizeOfPointsArray))
        controlPts = coin.SoCoordinate3()
        controlPts.point.setValues(0, sizeOfPointsArray, self.Points)

        Uknots = [0.0]*sqrtSize + [1.0]*sqrtSize
        Vknots = [0.0]*sqrtSize + [1.0]*sqrtSize

        surface = coin.SoNurbsSurface()
        surface.numUControlPoints = sqrtSize
        surface.numVControlPoints = sqrtSize
        surface.uKnotVector.setValues(0, len(Uknots), Uknots)
        surface.vKnotVector.setValues(0, len(Vknots), Vknots)

        # prop = coin.SoNurbsProperty() #word censored! Not available in coin3d

        surfaceNode = coin.SoSeparator()
        surfaceNode.addChild(controlPts)
        surfaceNode.addChild(material)
        surfaceNode.addChild(surface)
        return surfaceNode

    def genTextureImage(self):
        imgsize = coin.SbVec2s(5, 5)
        width = imgsize[0]
        height = imgsize[1]
        imgData = ''

        for i in range(height):
            for j in range(width):
                #imgData=imgData+((chr(134)).encode('latin-1'))
                imgData=imgData+chr(134)
        coinSoImage = coin.SoSFImage()
        coinSoImage.setValue(imgsize, 1, imgData)
        return coinSoImage


# this function is just an example showing how you can affect the drawing
def createFrameShape():
    sg = Gui.ActiveDocument.ActiveView.getSceneGraph()
    root = coin.SoSeparator()
    drawStyle = coin.SoDrawStyle()
    drawStyle.style = coin.SoDrawStyle.LINES
    root.addChild(drawStyle)
    shapeHints = coin.SoShapeHints()
    shapeHints.vertexOrdering = coin.SoShapeHints.COUNTERCLOCKWISE
    shapeHints.shapeType = coin.SoShapeHints.SOLID
    root.addChild(shapeHints)
    lightModel = coin.SoLightModel()
    lightModel.model = coin.SoLightModel.BASE_COLOR
    root.addChild(lightModel)

    cube = coin.SoCube()
    root.addChild(cube)
    sg.addChild(root)

# Load a SVG image to the coin3D


def loadImageTo3D(filename, Bsize, location):
    svg = coin.SoTexture2()
    svg.filename = filename
    box = coin.SoVRMLBox()
    box.size = Bsize  # (2,2,0)
    imagePos = coin.SoTransform()
    imagePos.translation.setValue(location)  # ([10,0,0])
    imagePos.rotation = coin.SbRotation(0, 0, 0, 0)
    image = coin.SoSeparator()
    image.addChild(imagePos)
    image.addChild(svg)
    image.addChild(box)
    return image        # Add this to the senegraph to show the picture.
# todo fixme


def draw_Curve(knots=None, data=None):
    curveSep = coin.SoSeparator()
    complexity = coin.SoComplexity()
    # controll coordinate with normalization (last bit)
    controlPts = coin.SoCoordinate4()
    curve = coin.SoNurbsCurve()
    controlPts.point.setValues(data)
    #curve.numControlPoints = array.shape[1]
    curve.knotVector.setValues(knots)
    curveSep.addChild(complexity)
    curveSep.addChild(controlPts)
    curveSep.addChild(curve)
    return curveSep


class draw_cylinder:
    """
    Create a Cylinder shape with wide configuration possibilities
    """

    def __init__(self, CylinderData: userDataObject = None):
        """[Draw a cylinder. Parameters determine how the cylinder is drawn]

        Args:
            CylinderData (userDataObject, optional): [description]. Defaults to None.
            userDataObject is an object that you will setup and send to this class. 
            It will contains all information needed to draw the cylinder. 
            
            class userDataObject:
                def __init__(self):
                self.Vectors: List[App.Vector] = []                     # the vertices 
                self.Scale: int = 1.0                                   # scale 
                self.Radius: float = 0.0                                # radius 
                self.Height: float = 0.0                                # height
                self.Color: List[float, float, float] = []              # color
                self.LineWidth: float = 1.0                             # drawing line width
                self.Transparency: float = 50.0                         # transparency
                self.Rotation: List[(float, float, float), float] = []  # rotation axis and angle 
            
            
        """
        self.CylinderSO = None
        self.TransCylinder = None
        self.CylinderTransform = None
        self.TempR = None
        self.Cylinder = None
        self.CylinderStyle = None
        self.Material = None
        self.Height = CylinderData.Height
        self.Radius = CylinderData.Radius
        self.Linewidth = CylinderData.LineWidth
        self.Transparency = CylinderData.Transparency
        self.Scale = CylinderData.Scale
        self.Rotation = CylinderData.Rotation
        self.color = CylinderData.Color

    def Activated(self):

        cylinderSO = coin.SoSeparator()
        transCylinder = coin.SoTranslation()
        cylinderTransform = coin.SoTransform()
        tempR = coin.SbVec3f()
        tempR.setValue(self.rotation[0], self.rotation[1], self.rotation[2])

        cylinder = coin.SoCylinder()
        p1 = App.Vector(0.0, 0.0, 0.0)  # (_Points[0])
        cylinderStyle = coin.SoDrawStyle()

        cylinderStyle.style = coin.SoDrawStyle.LINES  # draw only frame not filled
        cylinderStyle.lineWidth = 3

        cylinderTransform.scaleFactor.setValue([self.Scale, self.Scale, self.Scale])
        cylinderTransform.translation.setValue(App.Vector(0, 0, 0))
        # SbRotation (const SbVec3f &axis, const float radians)
        cylinderTransform.rotation.setValue(*tempR, self.rotation[3])
        transCylinder.translation.setValue(p1)

        material = coin.SoMaterial()
        material.transparency.setValue(80)
        material.diffuseColor.setValue(coin.SbColor(self.Color))
        # material.specularColor.setValue(coin.SbColor(1,1,1))
        material.shininess.setValue(1.0)
        cylinderSO.addChild(material)
        cylinderSO.addChild(cylinderTransform)
        cylinderSO.addChild(transCylinder)
        cylinderSO.addChild(cylinder)
        return cylinderSO
    

def draw_FaceSet(vertices=None, numvertices=(3,), _color=FR_COLOR.FR_GOLD):
    """[summary]

    Args:
        vertices (App.Vector, optional): Vertices will be used to draw the face. 3 will result in a triangle, four and above could draw different shapes. 
          Defaults to None.
        numvertices (List of integers, optional): [This will specify how these verticies should be used when the function draw them]. Defaults (3,).
        _color ([FL_COLOR], optional): [Provides the color for the drawing]. Defaults to FR_COLOR.FR_GOLD.

    Returns:
        [type]: [description]
        
    Example how to use draw_FceSet:
    from pivy import coin
    import math
    import fr_draw as d 
    
    def regular_polygon_vertexes(sidescount, radius, z, startangle=0):
        try:
            vertexes = []
            if radius != 0:
                for i in range(0, sidescount+1):
                    angle = 2 * math.pi * i / sidescount + math.pi + startangle
                    vertex = (radius * math.cos(angle),
                              radius * math.sin(angle), z)
                    vertexes.append(vertex)
            else:
                vertex = (0, 0, z)
                vertexes.append(vertex)
            return vertexes
        except Exception as err:
            App.Console.PrintError("'regular_polygon_vertexes' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return
    
    Verticies=regular_polygon_vertexes(4,30,0,90)
    n=len(Verticies)
    numvertices = (n, )
    root=d.draw_FaceSet(Verticies,numvertices,(0,1,1))
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(root)
    """
    try:
        rootSo = coin.SoSeparator()
        # This is the preferred code for Inventor 2.1

        # Using the new SoVertexProperty node is more efficient
        myVertexProperty = coin.SoVertexProperty()
        myVertexProperty.normalBinding = coin.SoNormalBinding.PER_FACE

        # Define material
        myVertexProperty.orderedRGBA = coin.SbColor(_color).getPackedValue()

        # Define coordinates for vertices - how these vertices will be divided per face
        myVertexProperty.vertex.setValues(0, len(vertices), vertices)

        # Define the FaceSet
        myFaceSet = coin.SoFaceSet()
        myFaceSet.numVertices.setValues(0, len(numvertices), numvertices)

        myFaceSet.vertexProperty = myVertexProperty
        rootSo.addChild(myFaceSet)
        return rootSo

    except Exception as err:
        App.Console.PrintError("'Draw Face' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

class draw_polygonBase:
    
    def __init__(self,sides=3,radius=5, startangel=0,pos=App.Vector(0,0,0), _color=FR_COLOR.FR_GOLD):
        """[summary]

        Args:
            sides (int, optional): [description]. Defaults to 3.
            angel (int, optional): [description]. Defaults to 0.
            pos ([type], optional): [description]. Defaults to App.Vector(0,0,0).
            _color ([type], optional): [description]. Defaults to FR_COLOR.FR_GOLD.
            
        Example:
        from pivy import coin
        import math
        import fr_draw as d 
        import time
        from PySide import QtCore,QtGui
        sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
        for i in range( 3, 25):
            f=d.draw_polygonBase(i,10,0,App.Vector(0,0,0), (0,1,1))
            root=f.draw()
            sg.addChild(root)
            QtGui.QApplication.processEvents()
            FreeCADGui.updateGui()
            time.sleep(0.5)
            sg.removeChild(root)
            QtGui.QApplication.processEvents()

        arange=range(3,25)
        revrange=reversed(arange)
        for i in revrange:
            f=d.draw_polygonBase(i,10,0,App.Vector(0,0,0), (0,1,1))
            root=f.draw()
            sg.addChild(root)
            QtGui.QApplication.processEvents()
            FreeCADGui.updateGui()
            time.sleep(0.5)
            sg.removeChild(root)
            QtGui.QApplication.processEvents()    
        
        """
        self.vertices=None
        self.noVertices=0
        self.color=_color
        self.position=pos
        self.sides=sides
        self.startAngel=startangel
        self.radius=radius
        
    def regular_polygon_vertexes(self,sidescount, radius, position=App.Vector(0,0,0),startangle=0):
        try:
            z=position.z
            vertexes = []
            if radius != 0:
                for i in range(0, sidescount+1):
                    angle = 2 * math.pi * i / sidescount + math.pi + startangle
                    vertex = (position.x +radius * math.cos(angle),
                              position.y+radius * math.sin(angle), z)
                    vertexes.append(vertex)
            else:
                vertex = (0, 0, z)
                vertexes.append(vertex)
            return vertexes
    
        except Exception as err:
            App.Console.PrintError("'regular_polygon_vertexes' Failed. "
                               "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return
    
    def draw(self):
        self.vertices=self.regular_polygon_vertexes(self.sides,self.radius,self.position,self.startAngel)
        numberOfvert=len(self.vertices)
        soRoot= draw_FaceSet(self.vertices,(numberOfvert,),self.color)
        return soRoot  # SoSeparator created during the drawing. You need to add this to the senegraph

#TODO : FIXME:
def draw_faceIndexed():
    IV_STRICT = 1

    # Routine to create a scene graph representing a dodecahedron
    So_END_FACE_INDEX = -1
    vertexPositions = (
        (0.0000,  1.2142,  0.7453),  # top

        (0.0000,  1.2142, -0.7453),  # points surrounding top
        (-1.2142,  0.7453,  0.0000),
        (-0.7453,  0.0000,  1.2142),
        (0.7453,  0.0000,  1.2142),
        (1.2142,  0.7453,  0.0000),

        (0.0000, -1.2142,  0.7453),  # points surrounding bottom
        (-1.2142, -0.7453,  0.0000),
        (-0.7453,  0.0000, -1.2142),
        (0.7453,  0.0000, -1.2142),
        (1.2142, -0.7453,  0.0000),

        (0.0000, -1.2142, -0.7453),  # bottom
    )

    #
    # Connectivity, information 12 faces with 5 vertices each ),
    # (plus the end-of-face indicator for each face):
    #

    Indicies = (
        1,  2,  3,  4, 5, So_END_FACE_INDEX,  # top face

        0,  1,  8,  7, 3, So_END_FACE_INDEX,  # 5 faces about top
        0,  2,  7,  6, 4, So_END_FACE_INDEX,
        0,  3,  6, 10, 5, So_END_FACE_INDEX,
        0,  4, 10,  9, 1, So_END_FACE_INDEX,
        0,  5,  9,  8, 2, So_END_FACE_INDEX,

        9,  5, 4, 6, 11, So_END_FACE_INDEX,  # 5 faces about bottom
        10,  4, 3, 7, 11, So_END_FACE_INDEX,
        6,  3, 2, 8, 11, So_END_FACE_INDEX,
        7,  2, 1, 9, 11, So_END_FACE_INDEX,
        8,  1, 5, 10, 11, So_END_FACE_INDEX,

        6,  7, 8, 9, 10, So_END_FACE_INDEX,  # bottom face
    )

    # Colors for the 12 faces
    colors = (
        (1.0, .0, 0), (.0,  .0, 1.0), (0, .7,  .7), (.0, 1.0,  0),
        (1.0, .0, 0), (.0,  .0, 1.0), (0, .7,  .7), (.0, 1.0,  0),
        (1.0, .0, 0), (.0,  .0, 1.0), (0, .7,  .7), (.0, 1.0,  0),
    )

    result = coin.SoSeparator()

    if IV_STRICT:
        # This is the preferred code for Inventor 2.1
        # Using the new coin.SoVertexProperty node is more efficient
        myVertexProperty = coin.SoVertexProperty()
        # Define colors for the faces
        for i in range(12):
            myVertexProperty.orderedRGBA.set1Value(
                i, coin.SbColor(colors[i]).getPackedValue())
            myVertexProperty.materialBinding = coin.SoMaterialBinding.PER_FACE
        # Define coordinates for vertices
        myVertexProperty.vertex.setValues(0, 12, vertexPositions)
        # Define the IndexedFaceSet, with Indicies into
        # the vertices:
        myFaceSet = coin.SoIndexedFaceSet()
        myFaceSet.coordIndex.setValues(0, 72, Indicies)
        myFaceSet.vertexProperty = myVertexProperty
        result.addChild(myFaceSet)

    else:
        # Define colors for the faces
        myMaterials = coin.SoMaterial()
        myMaterials.diffuseColor.setValues(0, 12, colors)
        result.addChild(myMaterials)
        myMaterialBinding = coin.SoMaterialBinding()
        myMaterialBinding.value = coin.SoMaterialBinding.PER_FACE
        result.addChild(myMaterialBinding)
        # Define coordinates for vertices
        myCoords = coin.SoCoordinate3()
        myCoords.point.setValues(0, 12, vertexPositions)
        result.addChild(myCoords)
        # Define the IndexedFaceSet, with Indicies into
        # the vertices:
        myFaceSet = coin.SoIndexedFaceSet()
        myFaceSet.coordIndex.setValues(0, 72, Indicies)
        result.addChild(myFaceSet)
    view = Gui.ActiveDocument.ActiveView
    sg = view.getSceneGraph()
    sg.addChild(result)
