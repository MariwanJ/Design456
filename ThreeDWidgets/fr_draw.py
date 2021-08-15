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
from types import coroutine
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


# draw arrow (Angel is in degree)
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
        coordsRoot.rotation.setValue(*tempR, math.radians(_rotation[3]))
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
            
        Example:
        
        from pivy import coin
        import math
        import fr_draw as d 
        import time
        from PySide import QtCore,QtGui
        file="E:/TEMP/freecad.png"      #TODO: FIXME:
        sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
        vert=[]
        vert.append(App.Vector(0,0,0))
        vert.append(App.Vector(120,0,30))
        vert.append(App.Vector(120,120,30))
        vert.append(App.Vector(0,120,30))

        f=d.draw_fourSidedShape(vert,(0,0,0),file,True,4)
        root=f.Activated()
        sg.addChild(root)
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
            if self.texture !="":
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
#Angle is in degree
def loadImageTo3D(filename="", BoxSize=(2,2,0.01), location=App.Vector(0,0,0), rotation=(0.0,0.0,0.0,0.0)):
    svg = coin.SoTexture2()
    svg.filename = filename
    box = coin.SoVRMLBox()
    box.size = BoxSize
    imagePos = coin.SoTransform()
    imagePos.translation.setValue(location)  
    tempR = coin.SbVec3f()
    tempR.setValue(rotation[0], rotation[1], rotation[2])
    imagePos.rotation.setValue(*tempR, math.radians(rotation[3]))
    image = coin.SoSeparator()
    image.addChild(imagePos)
    image.addChild(svg)
    image.addChild(box)
    return image                # Add this to the senegraph to show the picture.



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

def draw_faceIndexed(p1=App.Vector(0,0,0),vertexPositions: List[(float,float,float)] = [],indices=[],color=FR_COLOR.FR_GOLD,scale=(1,1,1),type=1,opacity=0, _rotation=[1.0, 0.0, 0.0, 0.0]):
    """[summary]

    Args:
        p1 ([App.Vector], optional): [Position of the drawing]. Defaults to App.Vector(0,0,0).
        vertexPositions (List[App.Vector], optional): [Vertices that must be given]. Defaults to [].
        indices (list, optional): [Indexed faceset's coordIndex must be given]. Defaults to [].
        color ([float,float,float], optional): [Color of the drawing]. Defaults to FR_COLOR.FR_GOLD.
        scale (tuple, optional): [description]. Defaults to (1,1,1).
        type (int, optional): [description]. Defaults to 1.
        opacity (int, optional): [description]. Defaults to 0.
        _rotation (list, optional): [description]. Defaults to [1.0, 0.0, 0.0, 0.0].
    """
    root=coin.SoSeparator() #root group holder
    transform=coin.SoTransform()
    trans=coin.SoTranslation()
    trans.translation.setValue(p1)
    transform.rotation.setValue(_rotation)
    transform.translation.setValue(p1)
    transform.scaleFactor.setValue([scale[0], scale[1], scale[2]])
    tempR = coin.SbVec3f()
    tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
    transform.rotation.setValue(*tempR, math.radians(_rotation[3]))
    material = coin.SoMaterial()
    material.transparency.setValue(opacity)
    material.diffuseColor.setValue(coin.SbColor(color))
    
    if type==0:
        soSepArrow=coin.SoSeparator()   # drawing holder
        soIndexFace= coin.SoIndexedFaceSet()
        cordinate= coin.SoCoordinate3()
        Shapehint= coin.SoShapeHints()
        Shapehint.shapeType=coin.SoShapeHints.UNKNOWN_FACE_TYPE
        Shapehint.vertexOrdering= coin.SoShapeHints.CLOCKWISE
        Shapehint.faceType=coin.SoShapeHints.UNKNOWN_FACE_TYPE
        
        cordinate.point.setValues(0, 61, vertexPositions)
        soIndexFace.coordIndex.setValues(0, len(indices), indices)
        soSepArrow.addChild(Shapehint)
        soSepArrow.addChild(cordinate) 
        soSepArrow.addChild(soIndexFace)
        
        root.addChild(trans)
        root.addChild(material)
        root.addChild(transform)
        root.addChild(soSepArrow)






####################################################
#New drawings based on conversion of drawing in Inscape --> FreeCAD --> export vrml 
# and later convert manually the VRML file to coin
    """
    Example using the drawing: 
    from pivy import coin
    import math
    import fr_draw as d 
    import time
    from PySide import QtCore,QtGui
    sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
    for i in range (0,181): 
        root=d.draw_2Darrow(App.Vector(0,0,0),(0,1,1),(1,1,1),1,0, [1.0, 0.0, 0.0, i])
        sg.addChild(root)
    for i in range (0,181): 
        root=d.draw_2Darrow(App.Vector(0,0,0),(0,1,1),(1,1,1),1,0, [-1.0, 0.0, 0.0, i])
        sg.addChild(root)

    """
def draw_2Darrow(p1=App.Vector(0,0,0),color=FR_COLOR.FR_GOLD,scale=(1,1,1),type=1,opacity=0, _rotation=[1.0, 0.0, 0.0, 0.0]):
    root=coin.SoSeparator() #root group holder
    transform=coin.SoTransform()
    trans=coin.SoTranslation()
    trans.translation.setValue(p1)
    transform.rotation.setValue(_rotation)
    transform.translation.setValue(p1)
    transform.scaleFactor.setValue([scale[0], scale[1], scale[2]])
    tempR = coin.SbVec3f()
    tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
    transform.rotation.setValue(*tempR, math.radians(_rotation[3]))
    material = coin.SoMaterial()
    material.transparency.setValue(opacity)
    material.diffuseColor.setValue(coin.SbColor(color))
    
    if type==0:
        soSepArrow=coin.SoSeparator()   # drawing holder
        soIndexFace= coin.SoIndexedFaceSet()
        cordinate= coin.SoCoordinate3()
        Shapehint= coin.SoShapeHints()
        Shapehint.shapeType=coin.SoShapeHints.UNKNOWN_FACE_TYPE
        Shapehint.vertexOrdering= coin.SoShapeHints.CLOCKWISE
        Shapehint.faceType=coin.SoShapeHints.UNKNOWN_FACE_TYPE
        vertexPositions=[(-16.210 ,   	 13.805   , 	0),
                         (-15.370 ,   	 13.165   , 	0),
                         (-14.520 ,   	 12.545   , 	0),
                         (-13.550 ,   	 11.905   , 	0),
                         (-12.780 ,   	 11.415   , 	0),
                         (-12.010 ,   	 10.945   , 	0),
                         (-10.980 ,   	 10.365   , 	0),
                         (-9.940  ,  	 9.815    ,	    0),
                         (-8.930  ,  	 9.315    ,	    0),
                         (-7.940  ,  	 8.855    ,	    0),
                         (-6.960  ,  	 8.445    ,	    0),
                         (-5.990  ,  	 8.075    ,	    0),
                         (-5.030  ,  	 7.735    ,	    0),
                         (-4.090  ,  	 7.445    ,	    0),
                         (-3.160  ,  	 7.195    ,	    0),
                         (-2.240  ,  	 6.975    ,	    0),
                         (-1.330  ,  	 6.795    ,	    0),
                         (-0.440  ,  	 6.645    ,	    0),
                         ( 0.440  ,  	 6.535    ,	    0),
                         ( 1.310  ,  	 6.455    ,	    0),
                         ( 2.170  ,  	 6.415    ,	    0),
                         ( 3.020  ,  	 6.405    ,	    0),
                         ( 3.710  ,  	 6.425    ,	    0),
                         ( 4.410  ,  	 6.465    ,	    0),
                         ( 4.830  ,  	 10.725   , 	0),
                         ( 16.210 ,   	 0.015    ,	    0),
                         ( 4.830  ,  	-10.705   , 	0),
                         ( 4.410  ,  	-6.445    ,	    0),
                         ( 3.450  ,  	-6.395    ,	    0),
                         ( 2.580  ,  	-6.395    ,	    0),
                         ( 1.710  ,  	-6.415    ,	    0),
                         ( 0.840  ,  	-6.475    ,	    0),
                         (-0.020  ,  	-6.555    ,	    0),
                         (-0.880  ,  	-6.685    ,	    0),
                         (-1.620  ,  	-6.815    ,	    0),
                         (-2.360  ,  	-6.965    ,	    0),
                         (-3.460  ,  	-7.255    ,	    0),
                         (-4.560  ,  	-7.575    ,	    0),
                         (-5.660  ,  	-7.935    ,	    0),
                         (-6.750  ,  	-8.345    ,	    0),
                         (-7.840  ,  	-8.795    ,	    0),
                         (-8.920  ,  	-9.275    ,	    0),
                         (-9.990  ,  	-9.805    ,	    0),
                         (-11.050 ,   	-10.365   , 	0),
                         (-12.100 ,   	-10.965   , 	0),
                         (-13.140 ,   	-11.605   , 	0),
                         (-14.150 ,   	-12.285   , 	0),
                         (-15.150 ,   	-12.995   , 	0),
                         (-15.680 ,   	-13.395   , 	0),
                         (-16.210 ,   	-13.805   , 	0),
                         (-16.210 ,   	 0.015    ,	    0),
                         (-16.210 ,   	 13.805   , 	0),
                         (-12.010 ,   	 10.945   , 	0),
                         ( 4.410  ,  	 6.465    ,	    0),
                         ( 4.830  ,  	 10.725   , 	0),
                         ( 16.210 ,   	 0.015    ,	    0),
                         ( 4.830  ,  	-10.705   , 	0),
                         ( 4.410  ,  	-6.445    ,	    0),
                         (-2.360  ,  	-6.965    ,	    0),
                         (-16.210 ,   	-13.805   , 	0),
                         (-16.210 ,   	 0.015    ,	    0),]
        
        cordinate.point.setValues(0, 61, vertexPositions)
        indices= [ 27, 25, 26, -1, 23, 25, 27, -1,
                    22, 27, 28, -1, 22, 23, 27, -1,
                    21, 28, 29, -1, 21, 22, 28, -1,
                    20, 21, 29, -1, 20, 29, 30, -1,
                    19, 30, 31, -1, 19, 20, 30, -1,
                    24, 25, 23, -1, 18, 19, 31, -1,
                    18, 31, 32, -1, 17, 32, 33, -1,
                    17, 18, 32, -1, 16, 33, 34, -1,
                    16, 17, 33, -1, 15, 34, 35, -1,
                    15, 16, 34, -1, 14, 35, 36, -1,
                    14, 15, 35, -1, 13, 14, 36, -1,
                    13, 36, 37, -1, 12, 37, 38, -1,
                    12, 13, 37, -1, 50, 12, 38, -1,
                    50, 10, 11, -1, 50, 11, 12, -1,
                    50, 38, 39, -1, 50, 39, 40, -1,
                    50, 40, 41, -1, 50, 41, 42, -1,
                    50, 42, 43, -1, 50, 43, 44, -1,
                    50, 44, 45, -1, 50, 45, 46, -1,
                    50, 46, 47, -1, 50, 47, 48, -1,
                    50, 48, 49, -1, 9, 10, 50, -1,
                    8, 9, 50, -1, 7, 8, 50, -1,
                    6, 7, 50, -1, 5, 6, 50, -1,
                    4, 5, 50, -1, 3, 4, 50, -1,
                    2, 3, 50, -1, 1, 2, 50, -1,
                    0, 1, 50, -1 ]
        soIndexFace.coordIndex.setValues(0, len(indices), indices)
        soSepArrow.addChild(Shapehint)
        soSepArrow.addChild(cordinate) 
        soSepArrow.addChild(soIndexFace)
        
        root.addChild(trans)
        root.addChild(material)
        root.addChild(transform)
        root.addChild(soSepArrow)
        
    elif type==1:
        soIndexfacesHead =coin.SoIndexedFaceSet()
        soIndexfacesTail1=coin.SoIndexedFaceSet()
        soIndexfacesTail2=coin.SoIndexedFaceSet()
        vertexHead=[(-5.87  ,    11.11 ,  0),
                    (-5.87  ,    3.65  ,  0),
                    (-31.64 ,    3.65  ,  0),
                    (-31.64 ,    -3.65 ,  0),
                    (-5.87  ,    -3.65 ,  0),
                    (-5.87  ,    -11.11,  0),
                    (5.87   ,    0     ,  0),
                    (-5.87  ,    11.11 ,  0),
                    (-5.87  ,    3.65  ,  0),
                    (-31.64 ,    3.65  ,  0),
                    (-31.64 ,    -3.65 ,  0),
                    (-5.87  ,    -3.65 ,  0),
                    (-5.87  ,    -11.11,  0),
                    (5.87   ,    0     ,  0)
                    ]

        vertexTail1=[(-38.58 ,    3.65  ,  0),
                        (-38.58 ,    -3.65 ,  0),
                        (-37.19 ,    -3.65 ,  0),
                        (-37.19 ,    3.65  ,  0),
                        (-38.58 ,    3.65  ,  0),
                        (-38.58 ,    -3.65 ,  0),
                        (-37.19 ,    -3.65 ,  0),
                        (-37.19 ,    3.65  ,  0)]
        
        vertexTail2=[(-35.8  ,    3.65  ,  0),
                        (-35.8  ,    -3.65 ,  0),
                        (-33.03 ,    -3.65 ,  0),
                        (-33.03 ,    3.65  ,  0),
                        (-35.8  ,    3.65  ,  0),
                        (-35.8  ,    -3.65 ,  0),
                        (-33.03 ,    -3.65 ,  0),
                        (-33.03 ,    3.65  ,  0)
                        ]
        
        indicesHead= [ 1, 2, 3, -1, 1, 3, 4, -1,
                       6, 0, 1, -1, 6, 4, 5, -1,
                        6, 1, 4, -1 ]
        indicesTail1=[ 3, 0, 1, -1, 3, 1, 2, -1 ]
        indicesTail2=[ 3, 0, 1, -1, 3, 1, 2, -1 ]

        coordinateHead=coin.SoCoordinate3()
        coordinateTail1=coin.SoCoordinate3()
        coordinateTail2=coin.SoCoordinate3()
        
        coordinateHead.point.setValues(0, 14, vertexHead)
        coordinateTail1.point.setValues(0, 8, vertexTail1)
        coordinateTail2.point.setValues(0, 8, vertexTail2)
        
        soSeparatorMain=coin.SoSeparator()
        Shapehint= coin.SoShapeHints()
        Shapehint.shapeType=coin.SoShapeHints.UNKNOWN_FACE_TYPE
        Shapehint.vertexOrdering= coin.SoShapeHints.COUNTERCLOCKWISE
        Shapehint.faceType=coin.SoShapeHints.UNKNOWN_FACE_TYPE
        
        soIndexfacesHead.coordIndex.setValues(0, len(indicesHead), indicesHead)
        soIndexfacesTail1.coordIndex.setValues(0, len(indicesTail1), indicesTail1)
        soIndexfacesTail2.coordIndex.setValues(0, len(indicesTail2), indicesTail2)
        
        soSeparatorMain.addChild(Shapehint)
        soSeparatorMain.addChild(coordinateHead)
        soSeparatorMain.addChild(soIndexfacesHead)

        soSeparatorMain.addChild(coordinateTail1)
        soSeparatorMain.addChild(soIndexfacesTail1)
        
        soSeparatorMain.addChild(coordinateTail2)
        soSeparatorMain.addChild(soIndexfacesTail2)        
        
        root.addChild(trans)
        root.addChild(material)
        root.addChild(transform)

        root.addChild(soSeparatorMain)
    #Finalize the drawing by adding color, pos, scale , opacity
    return root



"""
    Example using the drawing: 
    from pivy import coin
    import math
    import fr_draw as d 
    import time
    from PySide import QtCore,QtGui
    sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
    for i in range (0,181): 
        root=d.draw_TwoDarrow(App.Vector(0,0,0),(0,1,1),(1,1,1),1,0, [1.0, 0.0, 0.0, i])
        sg.addChild(root)
    for i in range (0,181): 
        root=d.draw_TwoDarrow(App.Vector(0,0,0),(0,1,1),(1,1,1),1,0, [-1.0, 0.0, 0.0, i])
        sg.addChild(root)

"""
def draw_TwoDarrow(p1=App.Vector(0,0,0),color=FR_COLOR.FR_GOLD,scale=(1,1,1),type=1,opacity=0, _rotation=[1.0, 0.0, 0.0, 0.0]):
    if type==0:
        arrow1_str="""#Inventor V2.1 ascii
            DEF root Separator {
              ShapeHints {
                vertexOrdering CLOCKWISE
                shapeType SOLID
                faceType CONVEX
              }
              VertexProperty {
                vertex [ 84.044998 -56.896271 0,
                    84.878975 -57.540318 0,
                    85.734688 -58.155235 0,
                    86.703186 -58.804478 0,
                    87.468605 -59.288124 0,
                    88.243706 -59.755527 0,
                    89.26725 -60.339321 0,
                    90.310753 -60.894997 0,
                    91.315041 -61.392021 0,
                    92.308304 -61.846939 0,
                    93.289848 -62.260395 0,
                    94.259178 -62.633118 0,
                    95.215981 -62.965904 0,
                    96.160065 -63.259579 0,
                    97.091377 -63.514984 0,
                    98.009964 -63.732956 0,
                    98.915955 -63.914307 0,
                    99.809555 -64.059807 0,
                    100.69104 -64.170197 0,
                    101.56074 -64.24614 0,
                    102.41901 -64.288269 0,
                    103.26627 -64.297104 0,
                    103.96442 -64.279381 0,
                    104.66389 -64.238457 0,
                    105.07834 -59.98032 0,
                    116.45697 -70.693359 0,
                    105.07834 -81.406395 0,
                    104.66389 -77.15033 0,
                    103.69802 -77.103256 0,
                    102.82792 -77.095093 0,
                    101.95882 -77.119354 0,
                    101.09246 -77.17598 0,
                    100.23052 -77.264824 0,
                    99.374641 -77.385674 0,
                    98.629578 -77.517899 0,
                    97.889114 -77.674843 0,
                    96.785973 -77.958443 0,
                    95.693489 -78.279922 0,
                    94.594559 -78.644653 0,
                    93.499832 -79.049988 0,
                    92.410858 -79.495689 0,
                    91.329269 -79.981453 0,
                    90.256821 -80.506813 0,
                    89.195351 -81.071213 0,
                    88.146782 -81.673943 0,
                    87.113083 -82.314133 0,
                    86.096298 -82.990799 0,
                    85.098495 -83.702782 0,
                    84.568085 -84.101654 0,
                    84.044998 -84.509567 0,
                    84.044998 -70.693359 0,
                    84.044998 -56.896271 0,
                    88.243706 -59.755527 0,
                    104.66389 -64.238457 0,
                    105.07834 -59.98032 0,
                    116.45697 -70.693359 0,
                    105.07834 -81.406395 0,
                    104.66389 -77.15033 0,
                    97.889114 -77.674843 0,
                    84.044998 -84.509567 0,
                    84.044998 -70.693359 0 ]
                normalBinding PER_FACE_INDEXED
                materialBinding PER_FACE_INDEXED

              }
              IndexedFaceSet {
                coordIndex [ 27, 25, 26, -1, 23, 25, 27, -1,
                    22, 27, 28, -1, 22, 23, 27, -1,
                    21, 28, 29, -1, 21, 22, 28, -1,
                    20, 21, 29, -1, 20, 29, 30, -1,
                    19, 30, 31, -1, 19, 20, 30, -1,
                    24, 25, 23, -1, 18, 19, 31, -1,
                    18, 31, 32, -1, 17, 32, 33, -1,
                    17, 18, 32, -1, 16, 33, 34, -1,
                    16, 17, 33, -1, 15, 34, 35, -1,
                    15, 16, 34, -1, 14, 35, 36, -1,
                    14, 15, 35, -1, 13, 14, 36, -1,
                    13, 36, 37, -1, 12, 37, 38, -1,
                    12, 13, 37, -1, 50, 12, 38, -1,
                    50, 10, 11, -1, 50, 11, 12, -1,
                    50, 38, 39, -1, 50, 39, 40, -1,
                    50, 40, 41, -1, 50, 41, 42, -1,
                    50, 42, 43, -1, 50, 43, 44, -1,
                    50, 44, 45, -1, 50, 45, 46, -1,
                    50, 46, 47, -1, 50, 47, 48, -1,
                    50, 48, 49, -1, 9, 10, 50, -1,
                    8, 9, 50, -1, 7, 8, 50, -1,
                    6, 7, 50, -1, 5, 6, 50, -1,
                    4, 5, 50, -1, 3, 4, 50, -1,
                    2, 3, 50, -1, 1, 2, 50, -1,
                    0, 1, 50, -1 ]
              }
            }
            """
    elif type==1:
        arrow1_str="""
        #Inventor V2.1 ascii
        DEF root Separator {
          renderCaching OFF
          boundingBoxCaching OFF
          renderCulling OFF
          pickCulling OFF
          Separator {
            Coordinate3 {
              point [ 104.70005 -67.598953 0,
                  104.70005 -75.059814 0,
                  78.933617 -75.059814 0,
                  78.933617 -82.361931 0,
                  104.70005 -82.361931 0,
                  104.70005 -89.8228 0,
                  116.43636 -78.710876 0,
                  104.70005 -67.598953 0,
                  104.70005 -75.059814 0,
                  78.933617 -75.059814 0,
                  78.933617 -82.361931 0,
                  104.70005 -82.361931 0,
                  104.70005 -89.8228 0,
                  116.43636 -78.710876 0 ]
            }
            IndexedFaceSet {
              coordIndex [ 1, 2, 3, -1, 1, 3, 4, -1,
                  6, 0, 1, -1, 6, 4, 5, -1,
                  6, 1, 4, -1 ]
            }
          }
          Separator {
            Coordinate3 {
              point [ 71.988663 -75.059814 0,
                  71.988663 -82.361931 0,
                  73.377655 -82.361931 0,
                  73.377655 -75.059814 0,
                  71.988663 -75.059814 0,
                  71.988663 -82.361931 0,
                  73.377655 -82.361931 0,
                  73.377655 -75.059814 0 ]
            }
            IndexedFaceSet {
              coordIndex [ 3, 0, 1, -1, 3, 1, 2, -1 ]
            }
          }
          Separator {
            Coordinate3 {
              point [ 74.766647 -75.059814 0,
                  74.766647 -82.361931 0,
                  77.544624 -82.361931 0,
                  77.544624 -75.059814 0,
                  74.766647 -75.059814 0,
                  74.766647 -82.361931 0,
                  77.544624 -82.361931 0,
                  77.544624 -75.059814 0 ]
            }
            IndexedFaceSet {
              coordIndex [ 3, 0, 1, -1, 3, 1, 2, -1 ]
            }
          }
        }
        """

    root=coin.SoSeparator()
    arrow=coin.SoSeparator()
    transform=coin.SoTransform()
    trans=coin.SoTranslation()
    material = coin.SoMaterial()
    material.transparency.setValue(opacity)
    material.diffuseColor.setValue(coin.SbColor(color))
    transform.scaleFactor.setValue([scale [0], scale[1], scale[2]])

    tempR = coin.SbVec3f()
    tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
    transform.rotation.setValue(*tempR, math.radians(_rotation[3]))

    input = coin.SoInput()
    input.setBuffer(arrow1_str)
    result = coin.SoDB.readAll(input)
    trans.translation.setValue(p1)
    if result == None:
        print("ERROR ")
        return None
    # Set up the duck transformations
    root.addChild(material)
    root.addChild(transform )
    root.addChild(trans)
    arrow.addChild(result)
    root.addChild(arrow)
    return root
    


"""
Example using the circle:

from pivy import coin
import fr_draw as d 
from PySide import QtCore,QtGui
sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
root=d.draw_circle()
sg.addChild(root)    

"""
def draw_circle(p1=App.Vector(0,0,0),color=FR_COLOR.FR_GOLD,scale=(1,1,1),opacity=0, _rotation=[0.0, 0.0, 0.0, 0.0]):
    root=coin.SoSeparator() 
    transform=coin.SoTransform()
    trans=coin.SoTranslation()
    trans.translation.setValue(p1)
    transform.rotation.setValue(_rotation)
    transform.translation.setValue(p1)
    transform.scaleFactor.setValue([scale[0], scale[1], scale[2]])
    tempR = coin.SbVec3f()
    tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
    transform.rotation.setValue(*tempR, math.radians(_rotation[3]))
    material = coin.SoMaterial()
    material.transparency.setValue(opacity)
    material.diffuseColor.setValue(coin.SbColor(color))
    
    soSepArrow=coin.SoSeparator()   # drawing holder
    soIndexFace= coin.SoIndexedFaceSet()
    cordinate= coin.SoCoordinate3()
    vertexPositions=[(7.11 ,   0      ,0),
                    (7.1  ,   0.37   ,0),
                    (7.07 ,   0.73   ,0),
                    (7.03 ,   1.09   ,0),
                    (6.96 ,   1.45   ,0),
                    (6.88 ,   1.81   ,0),
                    (6.77 ,   2.16   ,0),
                    (6.65 ,   2.51   ,0),
                    (6.52 ,   2.85   ,0),
                    (6.36 ,   3.18   ,0),
                    (6.19 ,   3.5    ,0),
                    (6    ,   3.82   ,0),
                    (5.8  ,   4.12   ,0),
                    (5.58 ,   4.41   ,0),
                    (5.34 ,   4.69   ,0),
                    (5.09 ,   4.96   ,0),
                    (4.83 ,   5.22   ,0),
                    (4.55 ,   5.46   ,0),
                    (4.27 ,   5.69   ,0),
                    (3.97 ,   5.9    ,0),
                    (3.66 ,   6.1    ,0),
                    (3.34 ,   6.28   ,0),
                    (3.01 ,   6.44   ,0),
                    (2.68 ,   6.59   ,0),
                    (2.34 ,   6.72   ,0),
                    (1.99 ,   6.83   ,0),
                    (1.63 ,   6.92   ,0),
                    (1.27 ,   7      ,0),
                    (0.91 ,   7.05   ,0),
                    (0.55 ,   7.09   ,0),
                    (0.18 ,   7.11   ,0),
                    (-0.18,   7.11   ,0),
                    (-0.55,   7.09   ,0),
                    (-0.91,   7.05   ,0),
                    (-1.27,   7      ,0),
                    (-1.63,   6.92   ,0),
                    (-1.99,   6.83   ,0),
                    (-2.34,   6.72   ,0),
                    (-2.68,   6.59   ,0),
                    (-3.01,   6.44   ,0),
                    (-3.34,   6.28   ,0),
                    (-3.66,   6.1    ,0),
                    (-3.97,   5.9    ,0),
                    (-4.27,   5.69   ,0),
                    (-4.55,   5.46   ,0),
                    (-4.83,   5.22   ,0),
                    (-5.09,   4.96   ,0),
                    (-5.34,   4.69   ,0),
                    (-5.58,   4.41   ,0),
                    (-5.8 ,   4.12   ,0),
                    (-6   ,   3.82   ,0),
                    (-6.19,   3.5    ,0),
                    (-6.36,   3.18   ,0),
                    (-6.52,   2.85   ,0),
                    (-6.65,   2.51   ,0),
                    (-6.77,   2.16   ,0),
                    (-6.88,   1.81   ,0),
                    (-6.96,   1.45   ,0),
                    (-7.03,   1.09   ,0),
                    (-7.07,   0.73   ,0),
                    (-7.1 ,   0.37   ,0),
                    (-7.11,   -1.81  ,0),
                    (-7.1 ,   -0.37  ,0),
                    (-7.07,   -0.73  ,0),
                    (-7.03,   -1.09  ,0),
                    (-6.96,   -1.45  ,0),
                    (-6.88,   -1.81  ,0),
                    (-6.77,   -2.16  ,0),
                    (-6.65,   -2.51  ,0),
                    (-6.52,   -2.85  ,0),
                    (-6.36,   -3.18  ,0),
                    (-6.19,   -3.5   ,0),
                    (-6   ,   -3.82  ,0),
                    (-5.8 ,   -4.12  ,0),
                    (-5.58,   -4.41  ,0),
                    (-5.34,   -4.69  ,0),
                    (-5.09,   -4.96  ,0),
                    (-4.83,   -5.22  ,0),
                    (-4.55,   -5.46  ,0),
                    (-4.27,   -5.69  ,0),
                    (-3.97,   -5.9   ,0),
                    (-3.66,   -6.1   ,0),
                    (-3.34,   -6.28  ,0),
                    (-3.01,   -6.44  ,0),
                    (-2.68,   -6.59  ,0),
                    (-2.34,   -6.72  ,0),
                    (-1.99,   -6.83  ,0),
                    (-1.63,   -6.92  ,0),
                    (-1.27,   -7     ,0),
                    (-0.91,   -7.05  ,0),
                    (-0.55,   -7.09  ,0),
                    (-0.18,   -7.11  ,0),
                    (0.18 ,   -7.11  ,0),
                    (0.55 ,   -7.09  ,0),
                    (0.91 ,   -7.05  ,0),
                    (1.27 ,   -7     ,0),
                    (1.63 ,   -6.92  ,0),
                    (1.99 ,   -6.83  ,0),
                    (2.34 ,   -6.72  ,0),
                    (2.68 ,   -6.59  ,0),
                    (3.01 ,   -6.44  ,0),
                    (3.34 ,   -6.28  ,0),
                    (3.66 ,   -6.1   ,0),
                    (3.97 ,   -5.9   ,0),
                    (4.27 ,   -5.69  ,0),
                    (4.55 ,   -5.46  ,0),
                    (4.83 ,   -5.22  ,0),
                    (5.09 ,   -4.96  ,0),
                    (5.34 ,   -4.69  ,0),
                    (5.58 ,   -4.41  ,0),
                    (5.8  ,   -4.12  ,0),
                    (6    ,   -3.82  ,0),
                    (6.19 ,   -3.5   ,0),
                    (6.36 ,   -3.18  ,0),
                    (6.52 ,   -2.85  ,0),
                    (6.65 ,   -2.51  ,0),
                    (6.77 ,   -2.16  ,0),
                    (6.88 ,   -1.81  ,0),
                    (6.96 ,   -1.45  ,0),
                    (7.03 ,   -1.09  ,0),
                    (7.07 ,   -0.73  ,0),
                    (7.1  ,  -0.37   ,0),
                    (7.11 ,     0    ,0),]
    
    cordinate.point.setValues(0, 123, vertexPositions)
    indices= [ 74, 75, 76, -1, 79, 76, 77, -1,
                79, 77, 78, -1, 72, 73, 74, -1,
                71, 74, 76, -1, 71, 72, 74, -1,
                82, 76, 79, -1, 82, 71, 76, -1,
                82, 79, 80, -1, 82, 80, 81, -1,
                69, 70, 71, -1, 85, 82, 83, -1,
                85, 83, 84, -1, 87, 82, 85, -1,
                87, 85, 86, -1, 88, 82, 87, -1,
                89, 82, 88, -1, 63, 64, 65, -1,
                63, 65, 66, -1, 63, 66, 67, -1,
                63, 67, 68, -1, 63, 68, 69, -1,
                90, 71, 82, -1, 90, 69, 71, -1,
                90, 82, 89, -1, 61, 62, 63, -1,
                94, 91, 92, -1, 94, 92, 93, -1,
                57, 58, 59, -1, 57, 59, 60, -1,
                57, 60, 61, -1, 57, 61, 63, -1,
                98, 94, 95, -1, 98, 95, 96, -1,
                98, 96, 97, -1, 54, 55, 56, -1,
                54, 56, 57, -1, 54, 63, 69, -1,
                54, 69, 90, -1, 54, 57, 63, -1,
                54, 90, 91, -1, 52, 53, 54, -1,
                102, 100, 101, -1, 102, 94, 98, -1,
                102, 98, 99, -1, 102, 99, 100, -1,
                50, 51, 52, -1, 104, 102, 103, -1,
                47, 48, 49, -1, 47, 49, 50, -1,
                46, 50, 52, -1, 46, 47, 50, -1,
                107, 104, 105, -1, 107, 105, 106, -1,
                107, 94, 102, -1, 107, 102, 104, -1,
                44, 45, 46, -1, 109, 107, 108, -1,
                43, 46, 52, -1, 43, 44, 46, -1,
                110, 107, 109, -1, 112, 110, 111, -1,
                112, 107, 110, -1, 113, 94, 107, -1,
                113, 54, 91, -1, 113, 52, 54, -1,
                113, 107, 112, -1, 113, 91, 94, -1,
                39, 40, 41, -1, 39, 41, 42, -1,
                39, 42, 43, -1, 38, 39, 43, -1,
                115, 113, 114, -1, 36, 37, 38, -1,
                117, 115, 116, -1, 117, 113, 115, -1,
                118, 113, 117, -1, 33, 34, 35, -1,
                31, 32, 33, -1, 31, 33, 35, -1,
                0, 120, 121, -1, 30, 31, 35, -1,
                30, 35, 36, -1, 1, 120, 0, -1,
                1, 118, 119, -1, 1, 119, 120, -1,
                1, 113, 118, -1, 2, 113, 1, -1,
                28, 29, 30, -1, 28, 38, 43, -1,
                28, 36, 38, -1, 28, 30, 36, -1,
                4, 2, 3, -1, 26, 27, 28, -1,
                6, 4, 5, -1, 6, 2, 4, -1,
                24, 25, 26, -1, 7, 2, 6, -1,
                22, 24, 26, -1, 22, 23, 24, -1,
                9, 7, 8, -1, 21, 22, 26, -1,
                20, 21, 26, -1, 11, 9, 10, -1,
                11, 7, 9, -1, 19, 26, 28, -1,
                19, 20, 26, -1, 18, 19, 28, -1,
                17, 18, 28, -1, 14, 11, 12, -1,
                14, 12, 13, -1, 14, 7, 11, -1,
                15, 113, 2, -1, 15, 16, 17, -1,
                15, 2, 7, -1, 15, 7, 14, -1,
                15, 17, 28, -1, 15, 43, 52, -1,
                15, 52, 113, -1, 15, 28, 43, -1 ]
    soIndexFace.coordIndex.setValues(0, len(indices), indices)
    soSepArrow.addChild(cordinate) 
    soSepArrow.addChild(soIndexFace)

    root.addChild(trans)
    root.addChild(material)
    root.addChild(transform)
    root.addChild(soSepArrow)
    #Finalize the drawing by adding color, pos, scale , opacity
    return root

