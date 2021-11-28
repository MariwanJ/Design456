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
from pivy import coin

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

from pivy import coin
import fr_draw as d 
from PySide import QtCore,QtGui
sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
root=d.draw_Point()
sg.addChild(root)
        
"""
def draw_Point(p1=App.Vector(0,0,0),size=0.1, color=FR_COLOR.FR_GOLD, type=0):
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
        if type ==0 :
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

"""
#Example using square_frame
from pivy import coin
import fr_draw as d 
from PySide import QtCore,QtGui
sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()

ve=[]
ve.append(App.Vector(0,0,0))
ve.append(App.Vector(10,0,0))
ve.append(App.Vector(10,10,0))
ve.append(App.Vector(0,10,0))
color= (1, 0.5, 1)
rot=[0,1,0,-90]
root=d.draw_square_frame(ve,color, rot, 5)
for i in root:
    sg.addChild(i)

"""
def draw_square_frame(vectors: List[App.Vector] = [], color=(0, 0, 0), _rotation=[0,0,1,0], lineWidth=1):
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

        transform = coin.SoTransform()
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        transform.rotation.setValue(tempR, math.radians(_rotation[3]))
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
            newSo.addChild(transform)
            newSo.addChild(line)
            Totallines.append(newSo)
        return Totallines

    except Exception as err:
        App.Console.PrintError("'draw_square' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

"""
#Example using draw_line
from pivy import coin
import fr_draw as d 
from PySide import QtCore,QtGui
sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()

ve=[]
ve.append(App.Vector(0,0,0))
ve.append(App.Vector(10,10,10))
#ve.append(App.Vector(10,10,0))
#ve.append(App.Vector(0,10,0))
color= (1, 0.5, 1)
rot=[0,1,0,-90]
root=d.draw_line(ve,color, rot, 5)
sg.addChild(root)
=======s



"""
def draw_line(vec=[], color=(1,1,1), _rotation=[0,0,1,0], LineWidth=1):
    try:
        so_separator = coin.SoSeparator()
        v = coin.SoVertexProperty()
        v.vertex.set1Value(0, vec[0])
        v.vertex.set1Value(1, vec[1])
        transform = coin.SoTransform()
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        transform.rotation.setValue(tempR, math.radians(_rotation[3]))
        
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
        so_separator.addChild(transform)
        so_separator.addChild(line)
        return so_separator

    except Exception as err:
        App.Console.PrintError("'draw_line' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


# draw arrow (Angel is in degree)
def draw_arrow(_Points=[], _color=FR_COLOR.FR_BLACK, _ArrSize=1.0, _rotation=[0.0, 0.0, 1.0, 0.0]):
    '''
    Draw a 3D arrow at the position given by the _Points and the color given by _color. 
    Scale it by the _ArrSize, and rotate it by the _rotation which consist of App.Vector(x,y,z) --the axis and 
    An angle in degree. 
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

        TailsTransform=coin.SoTransform()
        HeadTransform=coin.SoTransform()
        
        tailHeadTrs = coin.SbVec3f()
        tailHeadTrs.setValue(1,0,0)
        
        TailsTransform.rotation.setValue(tailHeadTrs,math.radians(90))
        HeadTransform.rotation.setValue(tailHeadTrs,math.radians(90))

        coordsRoot = coin.SoTransform()
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        cone = coin.SoCone()
        cone.bottomRadius = 3
        cone.height = 3

        cylinder = coin.SoCylinder()
        cylinder.height = 10
        cylinder.radius = 0.5
        p1 = App.Vector(0.0, 10.0, 0.0)  # (_Points[0])
        p2 = App.Vector(p1.x, p1.y-5, p1.z)
        styleHead = coin.SoDrawStyle()
        styleTail = coin.SoDrawStyle()

        styleHead.style = coin.SoDrawStyle.LINES  # draw only frame not filled
        styleHead.lineWidth = 3
        styleTail.style = coin.SoDrawStyle.LINES  # draw only frame not filled
        styleTail.lineWidth = 2

        coordsRoot.scaleFactor.setValue([_ArrSize, _ArrSize, _ArrSize])
        coordsRoot.translation.setValue(App.Vector(0, 0, 0))

        coordsRoot.rotation.setValue(tempR, math.radians(_rotation[3]))    # SbRotation (const SbVec3f &axis, const float radians)
        transHead.translation.setValue(p1)
        transTail.translation.setValue(p2)
        transRoot.translation.setValue(_Points)

        color = coin.SoBaseColor()
        color.rgb = _color

        so_separatorHead.addChild(color)
        so_separatorTail.addChild(color)

        #Rotate the arrow to be on Z axis
        so_separatorHead.addChild(TailsTransform)
        so_separatorTail.addChild(HeadTransform)

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

"""
Example using the function: 

from pivy import coin
import math
import fr_draw as d 
import time
from PySide import QtCore,QtGui
sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
root=d.draw_DoubleSidedArrow(App.Vector(0,0,0),(0,1,1),1,[1.0, 0.0, 0.0, 180])
sg.addChild(root)

"""

# draw a 3D arrow (Angel is in degree)
def draw_DoubleSidedArrow(_Points=App.Vector(0,0,0), _color=FR_COLOR.FR_BLACK, _ArrSize=1.0, _rotation=[0.0, 0.0, 1.0, 0.0]):
    """['''
        Draw a 3D arrow at the position given by the _Points and the color given by _color. 
        Scale it by the _ArrSize, and rotate it by the _rotation which consist of App.Vector(x,y,z) --the axis and 
        An angle in degree. 
    ''']

    Args:
        _Points (App.Vector, optional): [Position of the arrow 2 App.Vector]. Defaults to [].
        _color ([type], optional): [Arrow Color]. Defaults to FR_COLOR.FR_BLACK.
        _ArrSize (float, optional): [Size of the arrow]. Defaults to 1.0.
        _rotation (list, optional): [Axis and angle of rotation]. Defaults to [0.0, 0.0, 1.0, 0.0].

    Returns:
        [type]: [description]
    """
    try:
        so_separatorRoot = coin.SoSeparator()
        so_separatorHead = coin.SoSeparator()
        so_separatorTail = coin.SoSeparator()
        
        so_First  = coin.SoSeparator()   #First arrow 
        so_Second = coin.SoSeparator()   #Second arrow - reverse direction
        
        firstT=coin.SoTransform()
        secondT=coin.SoTransform()
        
        
        # decide at which position the object will be placed
        transHead = coin.SoTranslation()
        # decide at which position the object will be placed
        transTail = coin.SoTranslation()
        # decide at which position the whole objects will be placed
        transRoot = coin.SoTranslation()

        TailsTransform=coin.SoTransform()
        HeadTransform=coin.SoTransform()
        
        tailHeadTrs = coin.SbVec3f()
        tailHeadTrs.setValue(1,0,0)
        
        TailsTransform.rotation.setValue(tailHeadTrs,math.radians(90))
        HeadTransform.rotation.setValue(tailHeadTrs,math.radians(90))

        coordsRoot = coin.SoTransform()
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        cone = coin.SoCone()
        cone.bottomRadius = 3
        cone.height = 3

        cylinder = coin.SoCylinder()
        cylinder.height = 10
        cylinder.radius = 0.5
        p1 = App.Vector(0.0, 10.0, 0.0)  # (_Points[0])
        p2 = App.Vector(p1.x, p1.y-5, p1.z)
        styleHead = coin.SoDrawStyle()
        styleTail = coin.SoDrawStyle()

        styleHead.style = coin.SoDrawStyle.LINES  # draw only frame not filled
        styleHead.lineWidth = 3
        styleTail.style = coin.SoDrawStyle.LINES  # draw only frame not filled
        styleTail.lineWidth = 2

        coordsRoot.scaleFactor.setValue([_ArrSize, _ArrSize, _ArrSize])
        coordsRoot.translation.setValue(App.Vector(0, 0, 0))

        basicRot=coin.SbVec3f()
        basicRot.setValue(0.0,1.0,.0)
        firstT.rotation.setValue(basicRot,0)
        firstT.translation.setValue(App.Vector(0, 0, 0))
        secondT.rotation.setValue(basicRot,math.radians(-180.0))
        secondT.translation.setValue(App.Vector(0, 0, 0))
        
        coordsRoot.rotation.setValue(tempR, math.radians(_rotation[3]))    # SbRotation (const SbVec3f &axis, const float radians)
        coordsRoot.rotation.setValue(tempR, math.radians(_rotation[3]))
        
        transHead.translation.setValue(p1)
        transTail.translation.setValue(p2)
        transRoot.translation.setValue(_Points)

        color = coin.SoBaseColor()
        color.rgb = _color

        so_separatorHead.addChild(color)
        so_separatorTail.addChild(color)

        #Rotate the arrow to be on Z axis
        so_separatorHead.addChild(TailsTransform)
        so_separatorTail.addChild(HeadTransform)

        so_separatorHead.addChild(transHead)
        so_separatorTail.addChild(transTail)
        # so_separatorHead.addChild(styleHead)
        so_separatorHead.addChild(cone)

        # so_separatorTail.addChild(styleTail)
        so_separatorTail.addChild(cylinder)

        
        so_First.addChild(firstT)
        so_First.addChild(so_separatorHead)
        so_First.addChild(so_separatorTail)

        so_Second.addChild(secondT)
        so_Second.addChild(so_separatorHead)
        so_Second.addChild(so_separatorTail)
        
        group = coin.SoSeparator()
        group.addChild(transRoot)
        group.addChild(coordsRoot)
        group.addChild(so_First)
        group.addChild(so_Second)
        
        return group
    
    except Exception as err:
        App.Console.PrintError("'draw_arrow' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


#TODO: FIXME: ADD ROTATION
"""
    Example : 
    from pivy import coin
    import math
    import fr_draw as d 
    import time

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
def draw_box(p1=App.Vector(0,0,0),size=App.Vector(1,1,1), color=FR_COLOR.FR_GOLD, Texture="",style=0, LineWidth=1, LinePattern=0xffff):
    """[Use this function to draw a box. The box-style could be configured.]

    Args:
        p1 ([App.Vector]): [Defines the position of the vector ] . Defaults to App.Vector(0,0,0)
        size ([App.Vector], optional): [Defines the size of the box]. Defaults to App.Vector(1,1,1).
        color ([tuple], optional): [Box color as defined in FR_COLOR]. Defaults to FR_COLOR.FR_GOLD.
        texture (None, optional): [File name of the texture image]. Defaults to Null string.
        style (int, optional): [Box style: Filed=0, Lines ,Points,Invisible]. Defaults to 0.
        LineWidth (int, optional): [Line width: applicable only when you have line style]. Defaults to 1.
        LinePattern (hexadecimal, optional): [Defines if you have dashed lines or continuous line]. Defaults to 0xffff.

    Returns:
        [type]: [description]

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
#TODO FIXME:ADD ROTATION
"""
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
            if self.texture !="":
                texture.filename=self.texture
            else:
                texture=self.genTextureImage()
        _face = coin.SoFaceSet()
        _face.numVertices.set1Value(0, 4)
        FourSidedShape.addChild(coords)      
        if self.use_texture is True:
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
#TODO: ADD ROTATION
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
#TODO: FIXME: ADD ROTATION
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
def loadImageTo3D(filename, BoxSize=(2,2,0.01), location=App.Vector(0,0,0), rotation=(0.0,0.0,0.0,0.0)):
    """[Load svg file to the coin3d world. 
       Place it at the location given by 'location' and you can rotate it by the angle given by rotation]

    Args:
        filename (str, optional): [File name must be given]. Defaults to "".
        BoxSize (tuple, optional): [Size of the image]. Defaults to (2,2,0.01).
        location ([type], optional): [Placing location of the image]. Defaults to App.Vector(0,0,0).
        rotation (tuple, optional): [Rotation axis and angle ]. Defaults to (0.0,0.0,0.0,0.0).

    Returns:
        [type]: [SoSeparator of the drawing ]
    """
    svg = coin.SoTexture2()
    svg.filename = filename
    box = coin.SoVRMLBox()
    box.size = BoxSize
    imagePos = coin.SoTransform()
    imagePos.translation.setValue(location)  
    tempR = coin.SbVec3f()
    tempR.setValue(rotation[0], rotation[1], rotation[2])
    imagePos.rotation.setValue(tempR, math.radians(rotation[3]))
    image = coin.SoSeparator()
    image.addChild(imagePos)
    image.addChild(svg)
    image.addChild(box)
    return image                # Add this to the scenegraph to show the picture.



# todo fixme
def draw_Curve(knots=None, data=None):
    curveSep = coin.SoSeparator()
    complexity = coin.SoComplexity()
    # control coordinate with normalization (last bit)
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
    
    [Draw a cylinder. Parameters determine how the cylinder is drawn]

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
                self.Rotation: List[(float, float, float), float] = []  # rotation axis and angle in degree 
            
            
        """

    def __init__(self, CylinderData: userDataObject = None):
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
        cylinderTransform.rotation.setValue(tempR, math.radians(self.rotation[3]))
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
    


#TODO: FIXME : ADD ROTATION
def draw_FaceSet(vertices = None, numvertices = (3,), _color = FR_COLOR.FR_GOLD):
    """[summary]

    Args:
        vertices (App.Vector, optional): Vertices will be used to draw the face. 3 will result in a triangle, four and above could draw different shapes. 
          Defaults to None.
        numvertices (List of integers, optional): [This will specify how these vertices should be used when the function draw them]. Defaults (3,).
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
    
    vertices=regular_polygon_vertexes(4,30,0,90)
    n=len(vertices)
    numvertices = (n, )
    root=d.draw_FaceSet(vertices,numvertices,(0,1,1))
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

#TODO: FIXME : ADD ROTATION
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
        return soRoot  # SoSeparator created during the drawing. You need to add this to the scenegraph

def draw_faceIndexed(p1=App.Vector(0,0,0),vertexPositions: List[float] = [],indices=[],color=FR_COLOR.FR_GOLD,scale=(1,1,1),opacity=0, _rotation=[1.0, 0.0, 0.0, 0.0]):
    """[Draw any faceIndexed object by providing the vertexpositions and indices.]

    Args:
        p1 ([App.Vector], optional): [Position of the drawing]. Defaults to App.Vector(0,0,0).
        vertexPositions (List[App.Vector], optional): [Vertices of the drawing-must be given]. Defaults to [].
        indices (list, optional): [Indexed faceset's coordIndex must be given]. Defaults to [].
        color ([float,float,float], optional): [Color of the drawing]. Defaults to FR_COLOR.FR_GOLD.
        scale ((float,float,float), optional): [Scale factor for each axis]. Defaults to (1,1,1).
        opacity (int, optional): [Opacity percentage of the object. From 0 to 100]. Defaults to 0.
        _rotation ((float,float,float,float), optional): [Rotation axis and the angle in degree]. Defaults to [1.0, 0.0, 0.0, 0.0].
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
    transform.rotation.setValue(tempR, math.radians(_rotation[3]))
    material = coin.SoMaterial()
    material.transparency.setValue(opacity)
    material.diffuseColor.setValue(coin.SbColor(color))
    
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
# New drawings based on conversion of drawing in
# Inkscape > FreeCAD > Export VRML
# and later convert the VRML file manually to coin
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

def draw_2Darrow(p1=App.Vector(0,0,0),color=FR_COLOR.FR_GOLD,scale=[0.5,0.5,0.5],type=0,opacity=0, _rotation=[0.0, 0.0, 1.0, 0.0]):
    """[2D Arrow]

    Args:
        p1 ([App.Vector], optional): [Position of the arrow]. Defaults to App.Vector(0,0,0).
        color ((float,float,float)), optional): [RGB Value between 0 to 1]. Defaults to FR_COLOR.FR_GOLD.
        scale ((float,float,float)), optional): [Scale factor for each axis]. Defaults to (1,1,1).
        type (int, optional): [Arrow type. At the moment there are 2 types]. Defaults to 1.
        opacity (int, optional): [Opacity of the drawn arrow]. Defaults to 0.
        _rotation (list, optional): [Rotation of the arrow provided by three float and an angle (float) in degree]. Defaults to [1.0, 0.0, 0.0, 0.0].

    Returns:
        [SoSeparator]: [SoSeparator which hold the drawing. Add it to the scenegraph to show the arrow]
    """    
    try:
        root=coin.SoSeparator() #root group holder
        transform=coin.SoTransform()
        trans=coin.SoTranslation()
        trans.translation.setValue(p1)
        transform.scaleFactor.setValue([scale[0], scale[1], scale[2]])

        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        transform.rotation.setValue(tempR, math.radians(_rotation[3]))
        material = coin.SoMaterial()
        material.transparency.setValue(opacity)
        material.diffuseColor.setValue(coin.SbColor(color))
        if type ==0 :
            soSepArrow=coin.SoSeparator()   # drawing holder
            soIndexFace= coin.SoIndexedFaceSet()
            cordinate= coin.SoCoordinate3()
            Shapehint= coin.SoShapeHints()
            Shapehint.shapeType=coin.SoShapeHints.UNKNOWN_FACE_TYPE
            Shapehint.vertexOrdering= coin.SoShapeHints.CLOCKWISE
            Shapehint.faceType=coin.SoShapeHints.UNKNOWN_FACE_TYPE
            vertexPositions=[(0.00,	16.29	,0.17 ),
                            (0.00,	-0.03	,0.17 ),
                            (0.00,	-16.33	,0.17 ),
                            (0.00,	-16.34	,0.18 ),
                            (0.00,	-16.21	,0.25 ),
                            (0.00,	-15.96	,0.45 ),
                            (0.00,	-15.59	,0.80 ),
                            (0.00,	-15.09	,1.35 ),
                            (0.00,	-14.47	,2.11 ),
                            (0.00,	-13.85	,2.93 ),
                            (0.00,	-13.20	,3.86 ),
                            (0.00,	-12.54	,4.86 ),
                            (0.00,	-11.91	,5.90 ),
                            (0.00,	-11.30	,6.97 ),
                            (0.00,	-10.73	,8.04 ),
                            (0.00,	-10.21	,9.11 ),
                            (0.00,	-9.73	,10.18),
                            (0.00,	-9.30	,11.23),
                            (0.00,	-8.92	,12.26),
                            (0.00,	-8.58	,13.27),
                            (0.00,	-8.30	,14.26),
                            (0.00,	-8.06	,15.22),
                            (0.00,	-7.86	,16.16),
                            (0.00,	-7.70	,17.07),
                            (0.00,	-7.59	,17.96),
                            (0.00,	-7.52	,18.82),
                            (0.00,	-7.49	,19.66),
                            (0.00,	-7.49	,20.28),
                            (0.00,	-7.51	,20.89),
                            (0.00,	-12.99	,21.42),
                            (0.00,	-0.03	,35.19),
                            (0.00,	12.94	,21.42),
                            (0.00,	7.46	,20.89),
                            (0.00,	7.43	,20.02),
                            (0.00,	7.45	,19.15),
                            (0.00,	7.51	,18.22),
                            (0.00,	7.62	,17.27),
                            (0.00,	7.78	,16.30),
                            (0.00,	7.98	,15.30),
                            (0.00,	8.24	,14.27),
                            (0.00,	8.55	,13.21),
                            (0.00,	8.91	,12.13),
                            (0.00,	9.32	,11.03),
                            (0.00,	9.79	,9.91 ),
                            (0.00,	10.31	,8.78 ),
                            (0.00,	10.88	,7.64 ),
                            (0.00,	11.50	,6.51 ),
                            (0.00,	12.16	,5.39 ),
                            (0.00,	12.85	,4.30 ),
                            (0.00,	13.55	,3.28 ),
                            (0.00,	14.23	,2.34 ),
                            (0.00,	14.88	,1.54 ),
                            (0.00,	15.39	,0.96 ),
                            (0.00,	15.79	,0.55 ),
                            (0.00,	16.09	,0.30 ),
                            (0.00,	16.20	,0.22 ),
                            (0.00,	16.29	,0.17 ),
                            (0.00,	16.29	,0.17 ),
                            (0.00,	-0.03	,0.17 ),
                            (0.00,	-16.33	,0.17 ),
                            (0.00,	-16.34	,0.18 ),
                            (0.00,	-7.51	,20.89),
                            (0.00,	-12.99	,21.42),
                            (0.00,	-0.03	,35.19),
                            (0.00,	12.94	,21.42),
                            (0.00,	7.46	,20.89),
                            (0.00,	16.29	,0.17 )
                            ]

            cordinate.point.setValues(0, 61, vertexPositions)
            indices= [  4, 2, 3, -1, 1, 4, 5, -1,
              1, 5, 6, -1, 1, 6, 7, -1,
              1, 7, 8, -1, 1, 8, 9, -1,
              1, 9, 10, -1, 1, 10, 11, -1,
              1, 11, 12, -1, 1, 12, 13, -1,
              1, 13, 14, -1, 1, 14, 15, -1,
              1, 2, 4, -1, 16, 1, 15, -1,
              17, 1, 16, -1, 18, 1, 17, -1,
              52, 53, 1, -1, 54, 1, 53, -1,
              51, 52, 1, -1, 55, 1, 54, -1,
              0, 1, 55, -1, 56, 0, 55, -1,
              50, 51, 1, -1, 49, 50, 1, -1,
              48, 49, 1, -1, 47, 48, 1, -1,
              46, 47, 1, -1, 45, 46, 1, -1,
              44, 45, 1, -1, 43, 44, 1, -1,
              42, 43, 1, -1, 41, 42, 1, -1,
              41, 1, 18, -1, 40, 41, 18, -1,
              40, 18, 19, -1, 39, 19, 20, -1,
              39, 20, 21, -1, 39, 40, 19, -1,
              38, 39, 21, -1, 38, 21, 22, -1,
              37, 22, 23, -1, 37, 38, 22, -1,
              36, 23, 24, -1, 36, 37, 23, -1,
              35, 36, 24, -1, 35, 24, 25, -1,
              34, 25, 26, -1, 34, 35, 25, -1,
              33, 26, 27, -1, 33, 34, 26, -1,
              32, 27, 28, -1, 32, 33, 27, -1,
              30, 28, 29, -1, 30, 31, 32, -1,
              30, 32, 28, -1 ]
            soIndexFace.coordIndex.setValues(0, len(indices), indices)
            soSepArrow.addChild(Shapehint)
            soSepArrow.addChild(cordinate) 
            soSepArrow.addChild(soIndexFace)

            root.addChild(transform)             
            root.addChild(trans)
            root.addChild(material)
            root.addChild(soSepArrow)

        elif type==1:
            soIndexfacesHead =coin.SoIndexedFaceSet()
            soIndexfacesTail1=coin.SoIndexedFaceSet()
            soIndexfacesTail2=coin.SoIndexedFaceSet()
            vertexHead=[(0,11.11 ,        32.71  ),
                        (0,3.65  ,        32.71  ),
                        (0,3.65  ,        6.944 ),
                        (0,-3.65 ,        6.944 ),
                        (0,-3.65 ,        32.71  ),
                        (0,-11.11,        32.71  ),
                        (0,0     ,        44.45   ),
                        (0,11.11 ,        32.71  ),
                        (0,3.65  ,        32.71  ),
                        (0,3.65  ,        6.944 ),
                        (0,-3.65 ,        6.944 ),
                        (0,-3.65 ,        32.71  ),
                        (0,-11.11,        32.71  ),
                        (0,0     ,        44.45   )
                        ]

            vertexTail1=   [(0,    3.65 ,  0  ),
                            (0,    -3.65,  0  ),
                            (0,    -3.65,  1.39  ),
                            (0,    3.65 ,  1.39  ),
                            (0,    3.65 ,  0  ),
                            (0,    -3.65,  0  ),
                            (0,    -3.65,  1.39  ),
                            (0,    3.65 ,  1.39  )]

            vertexTail2=   [(0,    3.65 ,  2.78  ),
                            (0,    -3.65,  2.78  ),
                            (0,    -3.65,  5.55  ),
                            (0,    3.65 ,  5.55  ),
                            (0,    3.65 ,  2.78  ),
                            (0,    -3.65,  2.78  ),
                            (0,    -3.65,  5.55  ),
                            (0,    3.65 ,  5.55  )
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
        
        elif type==2:
            soSepArrow=coin.SoSeparator()   # drawing holder
            soIndexFace= coin.SoIndexedFaceSet()
            cordinate= coin.SoCoordinate3()
            vertexPositions=[(0,	-8.7955   ,7.769	 ),
                             (0,	-8.7485   ,7.571	 ),
                             (0,	-8.6795   ,7.376	 ),
                             (0,	-8.5845   ,7.175	 ),
                             (0,	-8.4685   ,6.982	 ),
                             (0,	-8.3475   ,6.819	 ),
                             (0,	-8.2145   ,6.673	 ),
                             (0,	-8.1205   ,6.584	 ),
                             (0,	-8.0215   ,6.504	 ),
                             (0,	-7.8375   ,6.379	 ),
                             (0,	-7.6455   ,6.276	 ),
                             (0,	-7.4435   ,6.193	 ),
                             (0,	-7.2335   ,6.132	 ),
                             (0,	-7.0195   ,6.093	 ),
                             (0,	-6.8025   ,6.078	 ),
                             (0,	-6.6065   ,6.084	 ),
                             (0,	-6.4125   ,6.108	 ),
                             (0,	-6.2195   ,6.151	 ),
                             (0,	-6.0315   ,6.213	 ),
                             (0,	-5.8495   ,6.292	 ),
                             (0,	-5.7385   ,6.351	 ),
                             (0,	-5.6295   ,6.418	 ),
                             (0,	-5.4995   ,6.526	 ),
                             (0,	-5.1355   ,6.867	 ),
                             (0,	-4.5425   ,7.444	 ),
                             (0,	-3.7505   ,8.228	 ),
                             (0,	-2.0495   ,9.923	 ),
                             (0,	-2.0485   ,5.858	 ),
                             (0,	-2.0445   ,2.908	 ),
                             (0,	-2.0325   ,2.131	 ),
                             (0,	-2.0125   ,1.743	 ),
                             (0,	-1.9855   ,1.516	 ),
                             (0,	-1.9515   ,1.377	 ),
                             (0,	-1.8965   ,1.244	 ),
                             (0,	-1.8245   ,1.101	 ),
                             (0,	-1.7215   ,0.919	 ),
                             (0,	-1.6005   ,0.749	 ),
                             (0,	-1.4585   ,0.59	 ),
                             (0,	-1.2985   ,0.446	 ),
                             (0,	-1.1215   ,0.317	 ),
                             (0,	-0.9295   ,0.207	 ),
                             (0,	-0.7785   ,0.137	 ),
                             (0,	-0.6205   ,0.078	 ),
                             (0,	-0.4425   ,0.027	 ),
                             (0,	-0.2855   ,0.006	 ),
                             (0,	-0.1625   ,0.001	 ),
                             (0,	-0.0015   ,0	     ),
                             (0,	0.2615   ,0.005	 ),
                             (0,	0.42349   ,0.024	 ),
                             (0,	0.5145   ,0.046	 ),
                             (0,	0.6175   ,0.078	 ),
                             (0,	0.81449   ,0.153	 ),
                             (0,	0.9985   ,0.243	 ),
                             (0,	1.1645   ,0.345	 ),
                             (0,	1.3155   ,0.46	 ),
                             (0,	1.4695   ,0.605	 ),
                             (0,	1.6095   ,0.769	 ),
                             (0,	1.7325   ,0.948	 ),
                             (0,	1.8415   ,1.144	 ),
                             (0,	1.9355   ,1.341	 ),
                             (0,	1.9695   ,1.448	 ),
                             (0,	1.9995   ,1.628	 ),
                             (0,	2.0215   ,1.926	 ),
                             (0,	2.0375   ,2.494	 ),
                             (0,	2.0455   ,3.782	 ),
                             (0,	2.0455   ,5.858	 ),
                             (0,	2.0465   ,9.923	 ),
                             (0,	3.7475   ,8.228	 ),
                             (0,	4.9225   ,7.07	 ),
                             (0,	5.4185   ,6.597	 ),
                             (0,	5.5475   ,6.48	 ),
                             (0,	5.6195   ,6.422	 ),
                             (0,	5.8055   ,6.313	 ),
                             (0,	5.9935   ,6.225	 ),
                             (0,	6.1735   ,6.162	 ),
                             (0,	6.3785   ,6.113	 ),
                             (0,	6.5695   ,6.088	 ),
                             (0,	6.7695   ,6.08	 ),
                             (0,	6.9895   ,6.092	 ),
                             (0,	7.2025   ,6.126	 ),
                             (0,	7.4115   ,6.183	 ),
                             (0,	7.6125   ,6.261	 ),
                             (0,	7.8045   ,6.36	 ),
                             (0,	7.9845   ,6.479	 ),
                             (0,	8.1355   ,6.602	 ),
                             (0,	8.2735   ,6.74	 ),
                             (0,	8.3995   ,6.891	 ),
                             (0,	8.5115   ,7.054	 ),
                             (0,	8.6075   ,7.229	 ),
                             (0,	8.6665   ,7.361	 ),
                             (0,	8.7175   ,7.498	 ),
                             (0,	8.7725   ,7.697	 ),
                             (0,	8.8045   ,7.901	 ),
                             (0,	8.8165   ,8.116	 ),
                             (0,	8.8055   ,8.334	 ),
                             (0,	8.7705   ,8.552	 ),
                             (0,	8.7205   ,8.745	 ),
                             (0,	8.6525   ,8.932	 ),
                             (0,	8.5755   ,9.094	 ),
                             (0,	8.4845   ,9.249	 ),
                             (0,	8.3645   ,9.383	 ),
                             (0,	8.0575   ,9.703	 ),
                             (0,	6.9215   ,10.863	 ),
                             (0,	4.4655   ,13.34	 ),
                             (0,	2.3105   ,15.492	 ),
                             (0,	1.6055   ,16.186	 ),
                             (0,	1.3855   ,16.398	 ),
                             (0,	1.2805   ,16.493	 ),
                             (0,	1.0865   ,16.632	 ),
                             (0,	0.91949   ,16.728	 ),
                             (0,	0.7775   ,16.792	 ),
                             (0,	0.6175   ,16.853	 ),
                             (0,	0.43949   ,16.906	 ),
                             (0,	0.30149   ,16.926	 ),
                             (0,	0.17249   ,16.932	 ),
                             (0,	-0.0015   ,16.933	 ),
                             (0,	-0.2635   ,16.928	 ),
                             (0,	-0.4245   ,16.909	 ),
                             (0,	-0.5145   ,16.888	 ),
                             (0,	-0.6135   ,16.857	 ),
                             (0,	-0.7885   ,16.798	 ),
                             (0,	-0.8975   ,16.75	 ),
                             (0,	-1.0265   ,16.67	 ),
                             (0,	-1.2135   ,16.524	 ),
                             (0,	-1.5135   ,16.255	 ),
                             (0,	-2.0575   ,15.733	 ),
                             (0,	-3.1545   ,14.646	 ),
                             (0,	-4.8375   ,12.963	 ),
                             (0,	-7.3585   ,10.437	 ),
                             (0,	-8.0195   ,9.756	 ),
                             (0,	-8.3365   ,9.41	 ),
                             (0,	-8.5115   ,9.196	 ),
                             (0,	-8.6015   ,9.059	 ),
                             (0,	-8.6385   ,8.987	 ),
                             (0,	-8.6695   ,8.91	 ),
                             (0,	-8.7235   ,8.75	 ),
                             (0,	-8.7655   ,8.588	 ),
                             (0,	-8.7965   ,8.399	 ),
                             (0,	-8.8165   ,8.147	 ),
                             (0,	-8.8145   ,7.945	 ),
                             (0,	-8.7955   ,7.769	 ),
                             (0,	-8.7955   ,7.769	 ),
                             (0,	-8.0215   ,6.504	 ),
                             (0,	-5.6295   ,6.418	 ),
                             (0,	-3.7505   ,8.228	 ),
                             (0,	-2.0495   ,9.923	 ),
                             (0,	-2.0485   ,5.858	 ),
                             (0,	-1.8245   ,1.101	 ),
                             (0,	-0.6205   ,0.078	 ),
                             (0,	-0.0015   ,0	     ),
                             (0,	0.6175   ,0.078	 ),
                             (0,	1.8415   ,1.144	 ),
                             (0,	2.0455   ,5.858	 ),
                             (0,	2.0465   ,9.923	 ),
                             (0,	3.7475   ,8.228	 ),
                             (0,	5.6195   ,6.422	 ),
                             (0,	6.7695   ,6.08	 ),
                             (0,	8.7175   ,7.498	 ),
                             (0,	8.4845   ,9.249	 ),
                             (0,	1.2805   ,16.493	 ),
                             (0,	0.6175   ,16.853	 ),
                             (0,	-0.0015   ,16.933	 ),
                             (0,	-0.6135   ,16.857	 ),
                             (0,	-4.8375   ,12.963	 ),
                             (0,	-8.7235   ,8.75	 ),
                             (0,	-8.7955   ,7.769	 )
                             ]

            cordinate.point.setValues(0, 166, vertexPositions)
            indices= [ 121, 120, 122, -1, 131, 134, 132, -1,
                        132, 134, 133, -1, 130, 135, 131, -1,
                        131, 135, 134, -1, 122, 119, 123, -1,
                        120, 119, 122, -1, 130, 136, 135, -1,
                        130, 137, 136, -1, 117, 116, 118, -1,
                        118, 116, 119, -1, 119, 116, 123, -1,
                        130, 138, 137, -1, 116, 115, 123, -1,
                        138, 1, 139, -1, 139, 1, 140, -1,
                        140, 1, 0, -1, 112, 111, 113, -1,
                        113, 111, 114, -1, 138, 2, 1, -1,
                        114, 110, 115, -1, 111, 110, 114, -1,
                        138, 3, 2, -1, 109, 108, 110, -1,
                        110, 108, 115, -1, 138, 4, 3, -1,
                        130, 4, 138, -1, 107, 106, 108, -1,
                        108, 106, 115, -1, 123, 106, 124, -1,
                        115, 106, 123, -1, 124, 105, 125, -1,
                        106, 105, 124, -1, 5, 8, 6, -1,
                        6, 8, 7, -1, 4, 9, 5, -1,
                        5, 9, 8, -1, 130, 9, 4, -1,
                        130, 10, 9, -1, 130, 11, 10, -1,
                        105, 104, 125, -1, 11, 22, 12, -1,
                        12, 22, 13, -1, 13, 22, 14, -1,
                        14, 22, 15, -1, 15, 22, 16, -1,
                        16, 22, 17, -1, 17, 22, 18, -1,
                        18, 22, 19, -1, 19, 22, 20, -1,
                        20, 22, 21, -1, 130, 22, 11, -1,
                        129, 23, 130, -1, 130, 23, 22, -1,
                        128, 24, 129, -1, 129, 24, 23, -1,
                        127, 25, 128, -1, 128, 25, 24, -1,
                        125, 26, 126, -1, 126, 26, 127, -1,
                        104, 26, 125, -1, 127, 26, 25, -1,
                        103, 66, 104, -1, 104, 66, 26, -1,
                        66, 102, 67, -1, 103, 102, 66, -1,
                        26, 65, 27, -1, 66, 65, 26, -1,
                        30, 33, 31, -1, 31, 33, 32, -1,
                        30, 34, 33, -1, 34, 36, 35, -1,
                        30, 36, 34, -1, 102, 68, 67, -1,
                        30, 37, 36, -1, 30, 38, 37, -1,
                        27, 64, 28, -1, 65, 64, 27, -1,
                        102, 101, 68, -1, 30, 39, 38, -1,
                        101, 69, 68, -1, 101, 100, 69, -1,
                        99, 98, 100, -1, 69, 72, 70, -1,
                        70, 72, 71, -1, 64, 63, 28, -1,
                        28, 63, 29, -1, 42, 44, 43, -1,
                        98, 97, 100, -1, 69, 73, 72, -1,
                        42, 45, 44, -1, 40, 45, 41, -1,
                        41, 45, 42, -1, 97, 96, 100, -1,
                        39, 46, 40, -1, 40, 46, 45, -1,
                        30, 46, 39, -1, 69, 74, 73, -1,
                        63, 62, 29, -1, 29, 62, 30, -1,
                        30, 62, 46, -1, 96, 95, 100, -1,
                        69, 75, 74, -1, 47, 49, 48, -1,
                        95, 94, 100, -1, 69, 76, 75, -1,
                        46, 50, 47, -1, 47, 50, 49, -1,
                        60, 59, 61, -1, 46, 51, 50, -1,
                        69, 77, 76, -1, 61, 58, 62, -1,
                        59, 58, 61, -1, 94, 93, 100, -1,
                        46, 52, 51, -1, 58, 57, 62, -1,
                        62, 56, 46, -1, 46, 56, 52, -1,
                        57, 56, 62, -1, 52, 55, 53, -1,
                        53, 55, 54, -1, 56, 55, 52, -1,
                        100, 78, 69, -1, 69, 78, 77, -1,
                        91, 90, 92, -1, 90, 89, 92, -1,
                        93, 89, 100, -1, 92, 89, 93, -1,
                        89, 88, 100, -1, 88, 87, 100, -1,
                        80, 83, 81, -1, 81, 83, 82, -1,
                        87, 86, 100, -1, 78, 86, 79, -1,
                        100, 86, 78, -1, 80, 84, 83, -1,
                        79, 84, 80, -1, 86, 85, 79, -1,
                        79, 85, 84, -1 ]
            soIndexFace.coordIndex.setValues(0, len(indices), indices)
            soSepArrow.addChild(cordinate) 
            soSepArrow.addChild(soIndexFace)

            root.addChild(material)
            root.addChild(transform)             
            root.addChild(trans)
            root.addChild(soSepArrow)
    
        #Finalize the drawing by adding color, pos, scale , opacity
        return root
    except Exception as err:
        App.Console.PrintError("'draw 2d Arrow failed' draw 2D-Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]


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
    transform.rotation.setValue(tempR, math.radians(_rotation[3]))
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


def draw_washer(p1=App.Vector(0,0,0),color=FR_COLOR.FR_GOLD,scale=(1,1,1),type=1,opacity=0, _rotation=[1.0, 0.0, 0.0, 0.0]):
    root=coin.SoSeparator() 
    transform=coin.SoTransform()
    trans=coin.SoTranslation()
    trans.translation.setValue(p1)
    transform.rotation.setValue(_rotation)
    transform.translation.setValue(p1)
    transform.scaleFactor.setValue([scale[0], scale[1], scale[2]])
    tempR = coin.SbVec3f()
    tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
    transform.rotation.setValue(tempR, math.radians(_rotation[3]))
    material = coin.SoMaterial()
    material.transparency.setValue(opacity)
    material.diffuseColor.setValue(coin.SbColor(color))
    
    soSepArrow=coin.SoSeparator()   # drawing holder
    soIndexFace= coin.SoIndexedFaceSet()
    cordinate= coin.SoCoordinate3()
    vertexPositions=[ (7.11  ,  0.00   , 0.0),
                        (7.10  ,  0.37   , 0.0),
                        (7.07  ,  0.73   , 0.0),
                        (7.03  ,  1.09   , 0.0),
                        (6.96  ,  1.45   , 0.0),
                        (6.88  ,  1.81   , 0.0),
                        (6.77  ,  2.16   , 0.0),
                        (6.65  ,  2.51   , 0.0),
                        (6.52  ,  2.85   , 0.0),
                        (6.36  ,  3.18   , 0.0),
                        (6.19  ,  3.50   , 0.0),
                        (6.00  ,  3.82   , 0.0),
                        (5.80  ,  4.12   , 0.0),
                        (5.58  ,  4.41   , 0.0),
                        (5.34  ,  4.69   , 0.0),
                        (5.09  ,  4.96   , 0.0),
                        (4.83  ,  5.22   , 0.0),
                        (4.55  ,  5.46   , 0.0),
                        (4.27  ,  5.69   , 0.0),
                        (3.97  ,  5.90   , 0.0),
                        (3.66  ,  6.10   , 0.0),
                        (3.34  ,  6.28   , 0.0),
                        (3.01  ,  6.44   , 0.0),
                        (2.68  ,  6.59   , 0.0),
                        (2.34  ,  6.72   , 0.0),
                        (1.99  ,  6.83   , 0.0),
                        (1.63  ,  6.92   , 0.0),
                        (1.27  ,  7.00   , 0.0),
                        (0.91  ,  7.05   , 0.0),
                        (0.55  ,  7.09   , 0.0),
                        (0.18  ,  7.11   , 0.0),
                        (-0.18 ,  7.11   , 0.0),
                        (-0.55 ,  7.09   , 0.0),
                        (-0.91 ,  7.05   , 0.0),
                        (-1.27 ,  7.00   , 0.0),
                        (-1.63 ,  6.92   , 0.0),
                        (-1.99 ,  6.83   , 0.0),
                        (-2.34 ,  6.72   , 0.0),
                        (-2.68 ,  6.59   , 0.0),
                        (-3.01 ,  6.44   , 0.0),
                        (-3.34 ,  6.28   , 0.0),
                        (-3.66 ,  6.10   , 0.0),
                        (-3.97 ,  5.90   , 0.0),
                        (-4.27 ,  5.69   , 0.0),
                        (-4.55 ,  5.46   , 0.0),
                        (-4.83 ,  5.22   , 0.0),
                        (-5.09 ,  4.96   , 0.0),
                        (-5.34 ,  4.69   , 0.0),
                        (-5.58 ,  4.41   , 0.0),
                        (-5.80 ,  4.12   , 0.0),
                        (-6.00 ,  3.82   , 0.0),
                        (-6.19 ,  3.50   , 0.0),
                        (-6.36 ,  3.18   , 0.0),
                        (-6.52 ,  2.85   , 0.0),
                        (-6.65 ,  2.51   , 0.0),
                        (-6.77 ,  2.16   , 0.0),
                        (-6.88 ,  1.81   , 0.0),
                        (-6.96 ,  1.45   , 0.0),
                        (-7.03 ,  1.09   , 0.0),
                        (-7.07 ,  0.73   , 0.0),
                        (-7.10 ,  0.37   , 0.0),
                        (-7.11 ,  -1.81  , 0.0),
                        (-7.10 ,  -0.37  , 0.0),
                        (-7.07 ,  -0.73  , 0.0),
                        (-7.03 ,  -1.09  , 0.0),
                        (-6.96 ,  -1.45  , 0.0),
                        (-6.88 ,  -1.81  , 0.0),
                        (-6.77 ,  -2.16  , 0.0),
                        (-6.65 ,  -2.51  , 0.0),
                        (-6.52 ,  -2.85  , 0.0),
                        (-6.36 ,  -3.18  , 0.0),
                        (-6.19 ,  -3.50  , 0.0),
                        (-6.00 ,  -3.82  , 0.0),
                        (-5.80 ,  -4.12  , 0.0),
                        (-5.58 ,  -4.41  , 0.0),
                        (-5.34 ,  -4.69  , 0.0),
                        (-5.09 ,  -4.96  , 0.0),
                        (-4.83 ,  -5.22  , 0.0),
                        (-4.55 ,  -5.46  , 0.0),
                        (-4.27 ,  -5.69  , 0.0),
                        (-3.97 ,  -5.90  , 0.0),
                        (-3.66 ,  -6.10  , 0.0),
                        (-3.34 ,  -6.28  , 0.0),
                        (-3.01 ,  -6.44  , 0.0),
                        (-2.68 ,  -6.59  , 0.0),
                        (-2.34 ,  -6.72  , 0.0),
                        (-1.99 ,  -6.83  , 0.0),
                        (-1.63 ,  -6.92  , 0.0),
                        (-1.27 ,  -7.00  , 0.0),
                        (-0.91 ,  -7.05  , 0.0),
                        (-0.55 ,  -7.09  , 0.0),
                        (-0.18 ,  -7.11  , 0.0),
                        (0.18  ,  -7.11  , 0.0),
                        (0.55  ,  -7.09  , 0.0),
                        (0.91  ,  -7.05  , 0.0),
                        (1.27  ,  -7.00  , 0.0),
                        (1.63  ,  -6.92  , 0.0),
                        (1.99  ,  -6.83  , 0.0),
                        (2.34  ,  -6.72  , 0.0),
                        (2.68  ,  -6.59  , 0.0),
                        (3.01  ,  -6.44  , 0.0),
                        (3.34  ,  -6.28  , 0.0),
                        (3.66  ,  -6.10  , 0.0),
                        (3.97  ,  -5.90  , 0.0),
                        (4.27  ,  -5.69  , 0.0),
                        (4.55  ,  -5.46  , 0.0),
                        (4.83  ,  -5.22  , 0.0),
                        (5.09  ,  -4.96  , 0.0),
                        (5.34  ,  -4.69  , 0.0),
                        (5.58  ,  -4.41  , 0.0),
                        (5.80  ,  -4.12  , 0.0),
                        (6.00  ,  -3.82  , 0.0),
                        (6.19  ,  -3.50  , 0.0),
                        (6.36  ,  -3.18  , 0.0),
                        (6.52  ,  -2.85  , 0.0),
                        (6.65  ,  -2.51  , 0.0),
                        (6.77  ,  -2.16  , 0.0),
                        (6.88  ,  -1.81  , 0.0),
                        (6.96  ,  -1.45  , 0.0),
                        (7.03  ,  -1.09  , 0.0),
                        (7.07  ,  -0.73  , 0.0),
                        (7.10  ,  -0.37  , 0.0),
                        (3.98  ,  0.00   , 0.0),
                        (3.97  ,  0.27   , 0.0),
                        (3.95  ,  0.54   , 0.0),
                        (3.90  ,  0.81   , 0.0),
                        (3.83  ,  1.07   , 0.0),
                        (3.75  ,  1.33   , 0.0),
                        (3.65  ,  1.59   , 0.0),
                        (3.54  ,  1.83   , 0.0),
                        (3.40  ,  2.07   , 0.0),
                        (3.25  ,  2.30   , 0.0),
                        (3.09  ,  2.51   , 0.0),
                        (2.91  ,  2.72   , 0.0),
                        (2.72  ,  2.91   , 0.0),
                        (2.51  ,  3.09   , 0.0),
                        (2.30  ,  3.25   , 0.0),
                        (2.07  ,  3.40   , 0.0),
                        (1.83  ,  3.54   , 0.0),
                        (1.59  ,  3.65   , 0.0),
                        (1.33  ,  3.75   , 0.0),
                        (1.07  ,  3.83   , 0.0),
                        (0.81  ,  3.90   , 0.0),
                        (0.54  ,  3.95   , 0.0),
                        (0.27  ,  3.97   , 0.0),
                        (0.00  ,  3.98   , 0.0),
                        (-0.27 ,  3.97   , 0.0),
                        (-0.54 ,  3.95   , 0.0),
                        (-0.81 ,  3.90   , 0.0),
                        (-1.07 ,  3.83   , 0.0),
                        (-1.33 ,  3.75   , 0.0),
                        (-1.59 ,  3.65   , 0.0),
                        (-1.83 ,  3.54   , 0.0),
                        (-2.07 ,  3.40   , 0.0),
                        (-2.30 ,  3.25   , 0.0),
                        (-2.51 ,  3.09   , 0.0),
                        (-2.72 ,  2.91   , 0.0),
                        (-2.91 ,  2.72   , 0.0),
                        (-3.09 ,  2.51   , 0.0),
                        (-3.25 ,  2.30   , 0.0),
                        (-3.40 ,  2.07   , 0.0),
                        (-3.54 ,  1.83   , 0.0),
                        (-3.65 ,  1.59   , 0.0),
                        (-3.75 ,  1.33   , 0.0),
                        (-3.83 ,  1.07   , 0.0),
                        (-3.90 ,  0.81   , 0.0),
                        (-3.95 ,  0.54   , 0.0),
                        (-3.97 ,  0.27   , 0.0),
                        (-3.98 ,  -1.01  , 0.0),
                        (-3.97 ,  -0.27  , 0.0),
                        (-3.95 ,  -0.54  , 0.0),
                        (-3.90 ,  -0.81  , 0.0),
                        (-3.83 ,  -1.07  , 0.0),
                        (-3.75 ,  -1.33  , 0.0),
                        (-3.65 ,  -1.59  , 0.0),
                        (-3.54 ,  -1.83  , 0.0),
                        (-3.40 ,  -2.07  , 0.0),
                        (-3.25 ,  -2.30  , 0.0),
                        (-3.09 ,  -2.51  , 0.0),
                        (-2.91 ,  -2.72  , 0.0),
                        (-2.72 ,  -2.91  , 0.0),
                        (-2.51 ,  -3.09  , 0.0),
                        (-2.30 ,  -3.25  , 0.0),
                        (-2.07 ,  -3.40  , 0.0),
                        (-1.83 ,  -3.54  , 0.0),
                        (-1.59 ,  -3.65  , 0.0),
                        (-1.33 ,  -3.75  , 0.0),
                        (-1.07 ,  -3.83  , 0.0),
                        (-0.81 ,  -3.90  , 0.0),
                        (-0.54 ,  -3.95  , 0.0),
                        (-0.27 ,  -3.97  , 0.0),
                        (0.00  ,  -3.98  , 0.0),
                        (0.27  ,  -3.97  , 0.0),
                        (0.54  ,  -3.95  , 0.0),
                        (0.81  ,  -3.90  , 0.0),
                        (1.07  ,  -3.83  , 0.0),
                        (1.33  ,  -3.75  , 0.0),
                        (1.59  ,  -3.65  , 0.0),
                        (1.83  ,  -3.54  , 0.0),
                        (2.07  ,  -3.40  , 0.0),
                        (2.30  ,  -3.25  , 0.0),
                        (2.51  ,  -3.09  , 0.0),
                        (2.72  ,  -2.91  , 0.0),
                        (2.91  ,  -2.72  , 0.0),
                        (3.09  ,  -2.51  , 0.0),
                        (3.25  ,  -2.30  , 0.0),
                        (3.40  ,  -2.07  , 0.0),
                        (3.54  ,  -1.83  , 0.0),
                        (3.65  ,  -1.59  , 0.0),
                        (3.75  ,  -1.33  , 0.0),
                        (3.83  ,  -1.07  , 0.0),
                        (3.90  ,  -0.81  , 0.0),
                        (3.95  ,  -0.54  , 0.0),
                        (3.97  ,  -0.27  , 0.0),
                        (7.11  ,  0.00   , 0.0),
                        (3.98  ,  0.00   , 0.0),
                        ]
                                        
    
    cordinate.point.setValues(0, 432, vertexPositions)
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




def draw_tube(p1=App.Vector(0,0,0),color=FR_COLOR.FR_GOLD,scale=(1,1,1),type=1,opacity=0, _rotation=[1.0, 0.0, 0.0, 0.0]):
    root=coin.SoSeparator() 
    transform=coin.SoTransform()
    trans=coin.SoTranslation()
    trans.translation.setValue(p1)
    transform.rotation.setValue(_rotation)
    transform.translation.setValue(p1)
    transform.scaleFactor.setValue([scale[0], scale[1], scale[2]])
    tempR = coin.SbVec3f()
    tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
    transform.rotation.setValue(tempR, math.radians(_rotation[3]))
    material = coin.SoMaterial()
    material.transparency.setValue(opacity)
    material.diffuseColor.setValue(coin.SbColor(color))
    
    soSepArrow=coin.SoSeparator()   # drawing holder
    soIndexFace= coin.SoIndexedFaceSet()
    cordinate= coin.SoCoordinate3()
    vertexPositions=[(5.00000	  ,	 0.00000  ,		10	 ),
                    (4.99013	  ,	 0.31395	,	 10	 ), 
                    (4.96057	  ,	 0.62667	,	 10	 ), 
                    (4.91144	  ,	 0.93691	,	 10	 ), 
                    (4.84292	  ,	 1.24345	,	 10	 ), 
                    (4.75528	  ,	 1.54509	,	 10	 ), 
                    (4.64888	  ,	 1.84062	,	 10	 ), 
                    (4.52414	  ,	 2.12890	,	 10	 ), 
                    (4.38153	  ,	 2.40877	,	 10	 ), 
                    (4.22164	  ,	 2.67913	,	 10	 ), 
                    (4.04509	  ,	 2.93893	,	 10	 ), 
                    (3.85257	  ,	 3.18712	,	 10	 ), 
                    (3.64484	  ,	 3.42274	,	 10	 ), 
                    (3.42274	  ,	 3.64484	,	 10	 ), 
                    (3.18712	  ,	 3.85257	,	 10	 ), 
                    (2.93893	  ,	 4.04509	,	 10	 ), 
                    (2.67913	  ,	 4.22164	,	 10	 ), 
                    (2.40877	  ,	 4.38153	,	 10	 ), 
                    (2.12890	  ,	 4.52414	,	 10	 ), 
                    (1.84062	  ,	 4.64888	,	 10	 ), 
                    (1.54509	  ,	 4.75528	,	 10	 ), 
                    (1.24345	  ,	 4.84292	,	 10	 ), 
                    (0.93691	  ,	 4.91144	,	 10	 ), 
                    (0.62667	  ,	 4.96057	,	 10	 ), 
                    (0.31395	  ,	 4.99013	,	 10	 ), 
                    (0.00000	  ,	 5.00000	,	 10	 ), 
                    (-0.31395	,4.99013	  ,	 10	),
                    (-0.62667	,4.96057	  ,	 10	),
                    (-0.93691	,4.91144	  ,	 10	),
                    (-1.24345	,4.84292	  ,	 10	),
                    (-1.54509	,4.75528	  ,	 10	),
                    (-1.84062	,4.64888	  ,	 10	),
                    (-2.12890	,4.52414	  ,	 10	),
                    (-2.40877	,4.38153	  ,	 10	),
                    (-2.67913	,4.22164	  ,	 10	),
                    (-2.93893	,4.04509	  ,	 10	),
                    (-3.18712	,3.85257	  ,	 10	),
                    (-3.42274	,3.64484	  ,	 10	),
                    (-3.64484	,3.42274	  ,	 10	),
                    (-3.85257	,3.18712	  ,	 10	),
                    (-4.04509	,2.93893	  ,	 10	),
                    (-4.22164	,2.67913	  ,	 10	),
                    (-4.38153	,2.40877	  ,	 10	),
                    (-4.52414	,2.12890	  ,	 10	),
                    (-4.64888	,1.84062	  ,	 10	),
                    (-4.75528	,1.54509	  ,	 10	),
                    (-4.84292	,1.24345	  ,	 10	),
                    (-4.91144	,0.93691	  ,	 10	),
                    (-4.96057	,0.62667	  ,	 10	),
                    (-4.99013	,0.31395	  ,	 10	),
                    (-5.00000	,0.00000	  ,	 10	),
                    (-4.99013	,-0.31395	  ,	 10	),
                    (-4.96057	,-0.62667	  ,	 10	),
                    (-4.91144	,-0.93691	  ,	 10	),
                    (-4.84292	,-1.24345	  ,	 10	),
                    (-4.75528	,-1.54509	  ,	 10	),
                    (-4.64888	,-1.84062	  ,	 10	),
                    (-4.52414	,-2.12890	  ,	 10	),
                    (-4.38153	,-2.40877	  ,	 10	),
                    (-4.22164	,-2.67913	  ,	 10	),
                    (-4.04509	,-2.93893	  ,	 10	),
                    (-3.85257	,-3.18712	  ,	 10	),
                    (-3.64484	,-3.42274	  ,	 10	),
                    (-3.42274	,-3.64484	  ,	 10	),
                    (-3.18712	,-3.85257	  ,	 10	),
                    (-2.93893	,-4.04509	  ,	 10	),
                    (-2.67913	,-4.22164	  ,	 10	),
                    (-2.40877	,-4.38153	  ,	 10	),
                    (-2.12890	,-4.52414	  ,	 10	),
                    (-1.84062	,-4.64888	  ,	 10	),
                    (-1.54509	,-4.75528	  ,	 10	),
                    (-1.24345	,-4.84292	  ,	 10	),
                    (-0.93691	,-4.91144	  ,	 10	),
                    (-0.62667	,-4.96057	  ,	 10	),
                    (-0.31395	,-4.99013	  ,	 10	),
                    (0.00000	  ,	 -5.00000,	10	),
                    (0.31395	  ,	 -4.99013,	10	),
                    (0.62667	  ,	 -4.96057,	10	),
                    (0.93691	  ,	 -4.91144,	10	),
                    (1.24345	  ,	 -4.84292,	10	),
                    (1.54509	  ,	 -4.75528,	10	),
                    (1.84062	  ,	 -4.64888,	10	),
                    (2.12890	  ,	 -4.52414,	10	),
                    (2.40877	  ,	 -4.38153,	10	),
                    (2.67913	  ,	 -4.22164,	10	),
                    (2.93893	  ,	 -4.04509,	10	),
                    (3.18712	  ,	 -3.85257,	10	),
                    (3.42274	  ,	 -3.64484,	10	),
                    (3.64484	  ,	 -3.42274,	10	),
                    (3.85257	  ,	 -3.18712,	10	),
                    (4.04509	  ,	 -2.93893,	10	),
                    (4.22164	  ,	 -2.67913,	10	),
                    (4.38153	  ,	 -2.40877,	10	),
                    (4.52414	  ,	 -2.12890,	10	),
                    (4.64888	  ,	 -1.84062,	10	),
                    (4.75528	  ,	 -1.54509,	10	),
                    (4.84292	  ,	 -1.24345,	10	),
                    (4.91144	  ,	 -0.93691,	10	),
                    (4.96057	  ,	 -0.62667,	10	),
                    (4.99013	  ,	 -0.31395,	10	),
                    (5.00000	  ,	 0.00000	,10	),
                    (5.00000	  ,	 0.00000	,0	),
                    (4.99013	  ,	 0.31395	,0	),
                    (4.96057	  ,	 0.62667	,0	),
                    (4.91144	  ,	 0.93691	,0	),
                    (4.84292	  ,	 1.24345	,0	),
                    (4.75528	  ,	 1.54509	,0	),
                    (4.64888	  ,	 1.84062	,0	),
                    (4.52414	  ,	 2.12890	,0	),
                    (4.38153	  ,	 2.40877	,0	),
                    (4.22164	  ,	 2.67913	,0	),
                    (4.04509	  ,	 2.93893	,0	),
                    (3.85257	  ,	 3.18712	,0	),
                    (3.64484	  ,	 3.42274	,0	),
                    (3.42274	  ,	 3.64484	,0	),
                    (3.18712	  ,	 3.85257	,0	),
                    (2.93893	  ,	 4.04509	,0	),
                    (2.67913	  ,	 4.22164	,0	),
                    (2.40877	  ,	 4.38153	,0	),
                    (2.12890	  ,	 4.52414	,0	),
                    (1.84062	  ,	 4.64888	,0	),
                    (1.54509	  ,	 4.75528	,0	),
                    (1.24345	  ,	 4.84292	,0	),
                    (0.93691	  ,	 4.91144	,0	),
                    (0.62667	  ,	 4.96057	,0	),
                    (0.31395	  ,	 4.99013	,0	),
                    (0.00000	  ,	 5.00000	,0	),
                    (-0.31395	,4.99013	  ,	 0	),
                    (-0.62667	,4.96057	  ,	 0	),
                    (-0.93691	,4.91144	  ,	 0	),
                    (-1.24345	,4.84292	  ,	 0	),
                    (-1.54509	,4.75528	  ,	 0	),
                    (-1.84062	,4.64888	  ,	 0	),
                    (-2.12890	,4.52414	  ,	 0	),
                    (-2.40877	,4.38153	  ,	 0	),
                    (-2.67913	,4.22164	  ,	 0	),
                    (-2.93893	,4.04509	  ,	 0	),
                    (-3.18712	,3.85257	  ,	 0	),
                    (-3.42274	,3.64484	  ,	 0	),
                    (-3.64484	,3.42274	  ,	 0	),
                    (-3.85257	,3.18712	  ,	 0	),
                    (-4.04509	,2.93893	  ,	 0	),
                    (-4.22164	,2.67913	  ,	 0	),
                    (-4.38153	,2.40877	  ,	 0	),
                    (-4.52414	,2.12890	  ,	 0	),
                    (-4.64888	,1.84062	  ,	 0	),
                    (-4.75528	,1.54509	  ,	 0	),
                    (-4.84292	,1.24345	  ,	 0	),
                    (-4.91144	,0.93691	  ,	 0	),
                    (-4.96057	,0.62667	  ,	 0	),
                    (-4.99013	,0.31395	  ,	 0	),
                    (-5.00000	,0.00000	  ,	 0	),
                    (-4.99013	,-0.31395	  ,	 0	),
                    (-4.96057	,-0.62667	  ,	 0	),
                    (-4.91144	,-0.93691	  ,	 0	),
                    (-4.84292	,-1.24345	  ,	 0	),
                    (-4.75528	,-1.54509	  ,	 0	),
                    (-4.64888	,-1.84062	  ,	 0	),
                    (-4.52414	,-2.12890	  ,	 0	),
                    (-4.38153	,-2.40877	  ,	 0	),
                    (-4.22164	,-2.67913	  ,	 0	),
                    (-4.04509	,-2.93893	  ,	 0	),
                    (-3.85257	,-3.18712	  ,	 0	),
                    (-3.64484	,-3.42274	  ,	 0	),
                    (-3.42274	,-3.64484	  ,	 0	),
                    (-3.18712	,-3.85257	  ,	 0	),
                    (-2.93893	,-4.04509	  ,	 0	),
                    (-2.67913	,-4.22164	  ,	 0	),
                    (-2.40877	,-4.38153	  ,	 0	),
                    (-2.12890	,-4.52414	  ,	 0	),
                    (-1.84062	,-4.64888	  ,	 0	),
                    (-1.54509	,-4.75528	  ,	 0	),
                    (-1.24345	,-4.84292	  ,	 0	),
                    (-0.93691	,-4.91144	  ,	 0	),
                    (-0.62667	,-4.96057	  ,	 0	),
                    (-0.31395	,-4.99013	  ,	 0	),
                    (0.00000	  ,	 -5.00000,	0	),
                    (0.31395	  ,	 -4.99013,	0	),
                    (0.62667	  ,	 -4.96057,	0	),
                    (0.93691	  ,	 -4.91144,	0	),
                    (1.24345	  ,	 -4.84292,	0	),
                    (1.54509	  ,	 -4.75528,	0	),
                    (1.84062	  ,	 -4.64888,	0	),
                    (2.12890	  ,	 -4.52414,	0	),
                    (2.40877	  ,	 -4.38153,	0	),
                    (2.67913	  ,	 -4.22164,	0	),
                    (2.93893	  ,	 -4.04509,	0	),
                    (3.18712	  ,	 -3.85257,	0	),
                    (3.42274	  ,	 -3.64484,	0	),
                    (3.64484	  ,	 -3.42274,	0	),
                    (3.85257	  ,	 -3.18712,	0	),
                    (4.04509	  ,	 -2.93893,	0	),
                    (4.22164	  ,	 -2.67913,	0	),
                    (4.38153	  ,	 -2.40877,	0	),
                    (4.52414	  ,	 -2.12890,	0	),
                    (4.64888	  ,	 -1.84062,	0	),
                    (4.75528	  ,	 -1.54509,	0	),
                    (4.84292	  ,	 -1.24345,	0	),
                    (4.91144	  ,	 -0.93691,	0	),
                    (4.96057	  ,	 -0.62667,	0	),
                    (4.99013	  ,	 -0.31395,	0	),
                    (5.00000	  ,	 0.00000	,0	),
                    (5.00000	  ,	 0.00000	,10	),
                    (4.99013	  ,	 0.31395	,10	),
                    (4.96057	  ,	 0.62667	,10	),
                    (4.91144	  ,	 0.93691	,10	),
                    (4.84292	  ,	 1.24345	,10	),
                    (4.75528	  ,	 1.54509	,10	),
                    (4.64888	  ,	 1.84062	,10	),
                    (4.52414	  ,	 2.12890	,10	),
                    (4.38153	  ,	 2.40877	,10	),
                    (4.22164	  ,	 2.67913	,10	),
                    (4.04509	  ,	 2.93893	,10	),
                    (3.85257	  ,	 3.18712	,10	),
                    (3.64484	  ,	 3.42274	,10	),
                    (3.42274	  ,	 3.64484	,10	),
                    (3.18712	  ,	 3.85257	,10	),
                    (2.93893	  ,	 4.04509	,10	),
                    (2.67913	  ,	 4.22164	,10	),
                    (2.40877	  ,	 4.38153	,10	),
                    (2.12890	  ,	 4.52414	,10	),
                    (1.84062	  ,	 4.64888	,10	),
                    (1.54509	  ,	 4.75528	,10	),
                    (1.24345	  ,	 4.84292	,10	),
                    (0.93691	  ,	 4.91144	,10	),
                    (0.62667	  ,	 4.96057	,10	),
                    (0.31395	  ,	 4.99013	,10	),
                    (0.00000	  ,	 5.00000	,10	),
                    (-0.31395	,4.99013	  ,	 10	),
                    (-0.62667	,4.96057	  ,	 10	),
                    (-0.93691	,4.91144	  ,	 10	),
                    (-1.24345	,4.84292	  ,	 10	),
                    (-1.54509	,4.75528	  ,	 10	),
                    (-1.84062	,4.64888	  ,	 10	),
                    (-2.12890	,4.52414	  ,	 10	),
                    (-2.40877	,4.38153	  ,	 10	),
                    (-2.67913	,4.22164	  ,	 10	),
                    (-2.93893	,4.04509	  ,	 10	),
                    (-3.18712	,3.85257	  ,	 10	),
                    (-3.42274	,3.64484	  ,	 10	),
                    (-3.64484	,3.42274	  ,	 10	),
                    (-3.85257	,3.18712	  ,	 10	),
                    (-4.04509	,2.93893	  ,	 10	),
                    (-4.22164	,2.67913	  ,	 10	),
                    (-4.38153	,2.40877	  ,	 10	),
                    (-4.52414	,2.12890	  ,	 10	),
                    (-4.64888	,1.84062	  ,	 10	),
                    (-4.75528	,1.54509	  ,	 10	),
                    (-4.84292	,1.24345	  ,	 10	),
                    (-4.91144	,0.93691	  ,	 10	),
                    (-4.96057	,0.62667	  ,	 10	),
                    (-4.99013	,0.31395	  ,	 10	),
                    (-5.00000	,0.00000	  ,	 10	),
                    (-4.99013	,-0.31395	  ,	 10	),
                    (-4.96057	,-0.62667	  ,	 10	),
                    (-4.91144	,-0.93691	  ,	 10	),
                    (-4.84292	,-1.24345	  ,	 10	),
                    (-4.75528	,-1.54509	  ,	 10	),
                    (-4.64888	,-1.84062	  ,	 10	),
                    (-4.52414	,-2.12890	  ,	 10	),
                    (-4.38153	,-2.40877	  ,	 10	),
                    (-4.22164	,-2.67913	  ,	 10	),
                    (-4.04509	,-2.93893	  ,	 10	),
                    (-3.85257	,-3.18712	  ,	 10	),
                    (-3.64484	,-3.42274	  ,	 10	),
                    (-3.42274	,-3.64484	  ,	 10	),
                    (-3.18712	,-3.85257	  ,	 10	),
                    (-2.93893	,-4.04509	  ,	 10	),
                    (-2.67913	,-4.22164	  ,	 10	),
                    (-2.40877	,-4.38153	  ,	 10	),
                    (-2.12890	,-4.52414	  ,	 10	),
                    (-1.84062	,-4.64888	  ,	 10	),
                    (-1.54509	,-4.75528	  ,	 10	),
                    (-1.24345	,-4.84292	  ,	 10	),
                    (-0.93691	,-4.91144	  ,	 10	),
                    (-0.62667	,-4.96057	  ,	 10	),
                    (-0.31395	,-4.99013	  ,	 10	),
                    (0.00000	  ,	 -5.00000,	10	),
                    (0.31395	  ,	 -4.99013,	10	),
                    (0.62667	  ,	 -4.96057,	10	),
                    (0.93691	  ,	 -4.91144,	10	),
                    (1.24345	  ,	 -4.84292,	10	),
                    (1.54509	  ,	 -4.75528,	10	),
                    (1.84062	  ,	 -4.64888,	10	),
                    (2.12890	  ,	 -4.52414,	10	),
                    (2.40877	  ,	 -4.38153,	10	),
                    (2.67913	  ,	 -4.22164,	10	),
                    (2.93893	  ,	 -4.04509,	10	),
                    (3.18712	  ,	 -3.85257,	10	),
                    (3.42274	  ,	 -3.64484,	10	),
                    (3.64484	  ,	 -3.42274,	10	),
                    (3.85257	  ,	 -3.18712,	10	),
                    (4.04509	  ,	 -2.93893,	10	),
                    (4.22164	  ,	 -2.67913,	10	),
                    (4.38153	  ,	 -2.40877,	10	),
                    (4.52414	  ,	 -2.12890,	10	),
                    (4.64888	  ,	 -1.84062,	10	),
                    (4.75528	  ,	 -1.54509,	10	),
                    (4.84292	  ,	 -1.24345,	10	),
                    (4.91144	  ,	 -0.93691,	10	),
                    (4.96057	  ,	 -0.62667,	10	),
                    (4.99013	  ,	 -0.31395,	10	),
                    (2.00000	  ,	 0.00000	,10	),
                    (1.99006	  ,	 0.19914	,10	),
                    (1.96035	  ,	 0.39629	,10	),
                    (1.91115	  ,	 0.58951	,10	),
                    (1.84295	  ,	 0.77687	,10	),
                    (1.75644	  ,	 0.95651	,10	),
                    (1.65248	  ,	 1.12664	,10	),
                    (1.53209	  ,	 1.28558	,10	),
                    (1.39647	  ,	 1.43173	,10	),
                    (1.24698	  ,	 1.56366	,10	),
                    (1.08509	  ,	 1.68005	,10	),
                    (0.91242	  ,	 1.77974	,10	),
                    (0.73068	  ,	 1.86175	,10	),
                    (0.54168	  ,	 1.92525	,10	),
                    (0.34730	  ,	 1.96962	,10	),
                    (0.14946	  ,	 1.99441	,10	),
                    (-0.04986	,1.99938	  ,	 10	),
                    (-0.24869	,1.98448	  ,	 10	),
                    (-0.44504	,1.94986	  ,	 10	),
                    (-0.63697	,1.89585	  ,	 10	),
                    (-0.82257	,1.82301	  ,	 10	),
                    (-1.00000	,1.73205	  ,	 10	),
                    (-1.16749	,1.62388	  ,	 10	),
                    (-1.32337	,1.49956	  ,	 10	),
                    (-1.46610	,1.36035	  ,	 10	),
                    (-1.59427	,1.20761	  ,	 10	),
                    (-1.70658	,1.04287	  ,	 10	),
                    (-1.80194	,0.86777	  ,	 10	),
                    (-1.87939	,0.68404	  ,	 10	),
                    (-1.93815	,0.49351	  ,	 10	),
                    (-1.97766	,0.29808	  ,	 10	),
                    (-1.99751	,0.09969	  ,	 10	),
                    (-1.99751	,-0.09969	  ,	 10	),
                    (-1.97766	,-0.29808	  ,	 10	),
                    (-1.93815	,-0.49351	  ,	 10	),
                    (-1.87939	,-0.68404	  ,	 10	),
                    (-1.80194	,-0.86777	  ,	 10	),
                    (-1.70658	,-1.04287	  ,	 10	),
                    (-1.59427	,-1.20761	  ,	 10	),
                    (-1.46610	,-1.36035	  ,	 10	),
                    (-1.32337	,-1.49956	  ,	 10	),
                    (-1.16749	,-1.62388	  ,	 10	),
                    (-1.00000	,-1.73205	  ,	 10	),
                    (-0.82257	,-1.82301	  ,	 10	),
                    (-0.63697	,-1.89585	  ,	 10	),
                    (-0.44504	,-1.94986	  ,	 10	),
                    (-0.24869	,-1.98448	  ,	 10	),
                    (-0.04986	,-1.99938	  ,	 10	),
                    (0.14946	  ,	 -1.99441,	10	),
                    (0.34730	  ,	 -1.96962,	10	),
                    (0.54168	  ,	 -1.92525,	10	),
                    (0.73068	  ,	 -1.86175,	10	),
                    (0.91242	  ,	 -1.77974,	10	),
                    (1.08509	  ,	 -1.68005,	10	),
                    (1.24698	  ,	 -1.56366,	10	),
                    (1.39647	  ,	 -1.43173,	10	),
                    (1.53209	  ,	 -1.28558,	10	),
                    (1.65248	  ,	 -1.12664,	10	),
                    (1.75644	  ,	 -0.95651,	10	),
                    (1.84295	  ,	 -0.77687,	10	),
                    (1.91115	  ,	 -0.58951,	10	),
                    (1.96035	  ,	 -0.39629,	10	),
                    (1.99006	  ,	 -0.19914,	10	),
                    (5.00000	  ,	 0.00000	,0	),
                    (4.99013	  ,	 0.31395	,0	),
                    (4.96057	  ,	 0.62667	,0	),
                    (4.91144	  ,	 0.93691	,0	),
                    (4.84292	  ,	 1.24345	,0	),
                    (4.75528	  ,	 1.54509	,0	),
                    (4.64888	  ,	 1.84062	,0	),
                    (4.52414	  ,	 2.12890	,0	),
                    (4.38153	  ,	 2.40877	,0	),
                    (4.22164	  ,	 2.67913	,0	),
                    (4.04509	  ,	 2.93893	,0	),
                    (3.85257	  ,	 3.18712	,0	),
                    (3.64484	  ,	 3.42274	,0	),
                    (3.42274	  ,	 3.64484	,0	),
                    (3.18712	  ,	 3.85257	,0	),
                    (2.93893	  ,	 4.04509	,0	),
                    (2.67913	  ,	 4.22164	,0	),
                    (2.40877	  ,	 4.38153	,0	),
                    (2.12890	  ,	 4.52414	,0	),
                    (1.84062	  ,	 4.64888	,0	),
                    (1.54509	  ,	 4.75528	,0	),
                    (1.24345	  ,	 4.84292	,0	),
                    (0.93691	  ,	 4.91144	,0	),
                    (0.62667	  ,	 4.96057	,0	),
                    (0.31395	  ,	 4.99013	,0	),
                    (0.00000	  ,	 5.00000	,0	),
                    (-0.31395	,4.99013	  ,	 0	),
                    (-0.62667	,4.96057	  ,	 0	),
                    (-0.93691	,4.91144	  ,	 0	),
                    (-1.24345	,4.84292	  ,	 0	),
                    (-1.54509	,4.75528	  ,	 0	),
                    (-1.84062	,4.64888	  ,	 0	),
                    (-2.12890	,4.52414	  ,	 0	),
                    (-2.40877	,4.38153	  ,	 0	),
                    (-2.67913	,4.22164	  ,	 0	),
                    (-2.93893	,4.04509	  ,	 0	),
                    (-3.18712	,3.85257	  ,	 0	),
                    (-3.42274	,3.64484	  ,	 0	),
                    (-3.64484	,3.42274	  ,	 0	),
                    (-3.85257	,3.18712	  ,	 0	),
                    (-4.04509	,2.93893	  ,	 0	),
                    (-4.22164	,2.67913	  ,	 0	),
                    (-4.38153	,2.40877	  ,	 0	),
                    (-4.52414	,2.12890	  ,	 0	),
                    (-4.64888	,1.84062	  ,	 0	),
                    (-4.75528	,1.54509	  ,	 0	),
                    (-4.84292	,1.24345	  ,	 0	),
                    (-4.91144	,0.93691	  ,	 0	),
                    (-4.96057	,0.62667	  ,	 0	),
                    (-4.99013	,0.31395	  ,	 0	),
                    (-5.00000	,0.00000	  ,	 0	),
                    (-4.99013	,-0.31395	  ,	 0	),
                    (-4.96057	,-0.62667	  ,	 0	),
                    (-4.91144	,-0.93691	  ,	 0	),
                    (-4.84292	,-1.24345	  ,	 0	),
                    (-4.75528	,-1.54509	  ,	 0	),
                    (-4.64888	,-1.84062	  ,	 0	),
                    (-4.52414	,-2.12890	  ,	 0	),
                    (-4.38153	,-2.40877	  ,	 0	),
                    (-4.22164	,-2.67913	  ,	 0	),
                    (-4.04509	,-2.93893	  ,	 0	),
                    (-3.85257	,-3.18712	  ,	 0	),
                    (-3.64484	,-3.42274	  ,	 0	),
                    (-3.42274	,-3.64484	  ,	 0	),
                    (-3.18712	,-3.85257	  ,	 0	),
                    (-2.93893	,-4.04509	  ,	 0	),
                    (-2.67913	,-4.22164	  ,	 0	),
                    (-2.40877	,-4.38153	  ,	 0	),
                    (-2.12890	,-4.52414	  ,	 0	),
                    (-1.84062	,-4.64888	  ,	 0	),
                    (-1.54509	,-4.75528	  ,	 0	),
                    (-1.24345	,-4.84292	  ,	 0	),
                    (-0.93691	,-4.91144	  ,	 0	),
                    (-0.62667	,-4.96057	  ,	 0	),
                    (-0.31395	,-4.99013	  ,	 0	),
                    (0.00000	  ,	 -5.00000,	0	),
                    (0.31395	  ,	 -4.99013,	0	),
                    (0.62667	  ,	 -4.96057,	0	),
                    (0.93691	  ,	 -4.91144,	0	),
                    (1.24345	  ,	 -4.84292,	0	),
                    (1.54509	  ,	 -4.75528,	0	),
                    (1.84062	  ,	 -4.64888,	0	),
                    (2.12890	  ,	 -4.52414,	0	),
                    (2.40877	  ,	 -4.38153,	0	),
                    (2.67913	  ,	 -4.22164,	0	),
                    (2.93893	  ,	 -4.04509,	0	),
                    (3.18712	  ,	 -3.85257,	0	),
                    (3.42274	  ,	 -3.64484,	0	),
                    (3.64484	  ,	 -3.42274,	0	),
                    (3.85257	  ,	 -3.18712,	0	),
                    (4.04509	  ,	 -2.93893,	0	),
                    (4.22164	  ,	 -2.67913,	0	),
                    (4.38153	  ,	 -2.40877,	0	),
                    (4.52414	  ,	 -2.12890,	0	),
                    (4.64888	  ,	 -1.84062,	0	),
                    (4.75528	  ,	 -1.54509,	0	),
                    (4.84292	  ,	 -1.24345,	0	),
                    (4.91144	  ,	 -0.93691,	0	),
                    (4.96057	  ,	 -0.62667,	0	),
                    (4.99013	  ,	 -0.31395,	0	),
                    (2.00000	  ,	 0.00000	,0	),
                    (1.99006	  ,	 0.19914	,0	),
                    (1.96035	  ,	 0.39629	,0	),
                    (1.91115	  ,	 0.58951	,0	),
                    (1.84295	  ,	 0.77687	,0	),
                    (1.75644	  ,	 0.95651	,0	),
                    (1.65248	  ,	 1.12664	,0	),
                    (1.53209	  ,	 1.28558	,0	),
                    (1.39647	  ,	 1.43173	,0	),
                    (1.24698	  ,	 1.56366	,0	),
                    (1.08509	  ,	 1.68005	,0	),
                    (0.91242	  ,	 1.77974	,0	),
                    (0.73068	  ,	 1.86175	,0	),
                    (0.54168	  ,	 1.92525	,0	),
                    (0.34730	  ,	 1.96962	,0	),
                    (0.14946	  ,	 1.99441	,0	),
                    (-0.04986	,1.99938	  ,	 0	),
                    (-0.24869	,1.98448	  ,	 0	),
                    (-0.44504	,1.94986	  ,	 0	),
                    (-0.63697	,1.89585	  ,	 0	),
                    (-0.82257	,1.82301	  ,	 0	),
                    (-1.00000	,1.73205	  ,	 0	),
                    (-1.16749	,1.62388	  ,	 0	),
                    (-1.32337	,1.49956	  ,	 0	),
                    (-1.46610	,1.36035	  ,	 0	),
                    (-1.59427	,1.20761	  ,	 0	),
                    (-1.70658	,1.04287	  ,	 0	),
                    (-1.80194	,0.86777	  ,	 0	),
                    (-1.87939	,0.68404	  ,	 0	),
                    (-1.93815	,0.49351	  ,	 0	),
                    (-1.97766	,0.29808	  ,	 0	),
                    (-1.99751	,0.09969	  ,	 0	),
                    (-1.99751	,-0.09969	  ,	 0	),
                    (-1.97766	,-0.29808	  ,	 0	),
                    (-1.93815	,-0.49351	  ,	 0	),
                    (-1.87939	,-0.68404	  ,	 0	),
                    (-1.80194	,-0.86777	  ,	 0	),
                    (-1.70658	,-1.04287	  ,	 0	),
                    (-1.59427	,-1.20761	  ,	 0	),
                    (-1.46610	,-1.36035	  ,	 0	),
                    (-1.32337	,-1.49956	  ,	 0	),
                    (-1.16749	,-1.62388	  ,	 0	),
                    (-1.00000	,-1.73205	  ,	 0	),
                    (-0.82257	,-1.82301	  ,	 0	),
                    (-0.63697	,-1.89585	  ,	 0	),
                    (-0.44504	,-1.94986	  ,	 0	),
                    (-0.24869	,-1.98448	  ,	 0	),
                    (-0.04986	,-1.99938	  ,	 0	),
                    (0.14946	,-1.99441,	0	 ),
                    (0.34730	,-1.96962,	0	 ),
                    (0.54168	,-1.92525,	0	 ),
                    (0.73068	,-1.86175,	0	 ),
                    (0.91242	,-1.77974,	0	 ),
                    (1.08509	,-1.68005,	0	 ),
                    (1.24698	,-1.56366,	0	 ),
                    (1.39647	,-1.43173,	0	 ),
                    (1.53209	,-1.28558,	0	 ),
                    (1.65248	,-1.12664,	0	 ),
                    (1.75644	,-0.95651,	0	 ),
                    (1.84295	,-0.77687,	0	 ),
                    (1.91115	,-0.58951,	0	 ),
                    (1.96035	,-0.39629,	0	 ),
                    (1.99006	,-0.19914,	0	 ),
                    (2.00000	,0.00000	,10	 ),
                    (1.99006	,0.19914	,10	 ),
                    (1.96035	,0.39629	,10	 ),
                    (1.91115	,0.58951	,10	 ),
                    (1.84295	,0.77687	,10	 ),
                    (1.75644	,0.95651	,10	 ),
                    (1.65248	,1.12664	,10	 ),
                    (1.53209	,1.28558	,10	 ),
                    (1.39647	,1.43173	,10	 ),
                    (1.24698	,1.56366	,10	 ),
                    (1.08509	,1.68005	,10	 ),
                    (0.91242	,1.77974	,10	 ),
                    (0.73068	,1.86175	,10	 ),
                    (0.54168	,1.92525	,10	 ),
                    (0.34730	,1.96962	,10	 ),
                    (0.14946	,1.99441	,10	 ),
                    (-0.04986	,1.99938	  ,	 10	),
                    (-0.24869	,1.98448	  ,	 10	),
                    (-0.44504	,1.94986	  ,	 10	),
                    (-0.63697	,1.89585	  ,	 10	),
                    (-0.82257	,1.82301	  ,	 10	),
                    (-1.00000	,1.73205	  ,	 10	),
                    (-1.16749	,1.62388	  ,	 10	),
                    (-1.32337	,1.49956	  ,	 10	),
                    (-1.46610	,1.36035	  ,	 10	),
                    (-1.59427	,1.20761	  ,	 10	),
                    (-1.70658	,1.04287	  ,	 10	),
                    (-1.80194	,0.86777	  ,	 10	),
                    (-1.87939	,0.68404	  ,	 10	),
                    (-1.93815	,0.49351	  ,	 10	),
                    (-1.97766	,0.29808	  ,	 10	),
                    (-1.99751	,0.09969	  ,	 10	),
                    (-1.99751	,-0.09969	  ,	 10	),
                    (-1.97766	,-0.29808	  ,	 10	),
                    (-1.93815	,-0.49351	  ,	 10	),
                    (-1.87939	,-0.68404	  ,	 10	),
                    (-1.80194	,-0.86777	  ,	 10	),
                    (-1.70658	,-1.04287	  ,	 10	),
                    (-1.59427	,-1.20761	  ,	 10	),
                    (-1.46610	,-1.36035	  ,	 10	),
                    (-1.32337	,-1.49956	  ,	 10	),
                    (-1.16749	,-1.62388	  ,	 10	),
                    (-1.00000	,-1.73205	  ,	 10	),
                    (-0.82257	,-1.82301	  ,	 10	),
                    (-0.63697	,-1.89585	  ,	 10	),
                    (-0.44504	,-1.94986	  ,	 10	),
                    (-0.24869	,-1.98448	  ,	 10	),
                    (-0.04986	,-1.99938	  ,	 10	),
                    (0.14946	,-1.99441	  ,	 10	),
                    (0.34730	,-1.96962	  ,	 10	),
                    (0.54168	,-1.92525	  ,	 10	),
                    (0.73068	,-1.86175	  ,	 10	),
                    (0.91242	,-1.77974	  ,	 10	),
                    (1.08509	,-1.68005	  ,	 10	),
                    (1.24698	,-1.56366	  ,	 10	),
                    (1.39647	,-1.43173	  ,	 10	),
                    (1.53209	,-1.28558	  ,	 10	),
                    (1.65248	,-1.12664	  ,	 10	),
                    (1.75644	,-0.95651	  ,	 10	),
                    (1.84295	,-0.77687	  ,	 10	),
                    (1.91115	,-0.58951	  ,	 10	),
                    (1.96035	,-0.39629	  ,	 10	),
                    (1.99006	,-0.19914	  ,	 10	),
                    (2.00000	,0.00000	  ,	 10	),
                    (2.00000	,0.00000	  ,	 0	),
                    (1.99006	,0.19914	  ,	 0	),
                    (1.96035	,0.39629	  ,	 0	),
                    (1.91115	,0.58951	  ,	 0	),
                    (1.84295	,0.77687	  ,	 0	),
                    (1.75644	,0.95651	  ,	 0	),
                    (1.65248	,1.12664	  ,	 0	),
                    (1.53209	,1.28558	  ,	 0	),
                    (1.39647	,1.43173	  ,	 0	),
                    (1.24698	,1.56366	  ,	 0	),
                    (1.08509	,1.68005	  ,	 0	),
                    (0.91242	,1.77974	  ,	 0	),
                    (0.73068	,1.86175	  ,	 0	),
                    (0.54168	,1.92525	  ,	 0	),
                    (0.34730	,1.96962	  ,	 0	),
                    (0.14946	,1.99441	  ,	 0	),
                    (-0.04986	,1.99938	  ,	 0	),
                    (-0.24869	,1.98448	  ,	 0	),
                    (-0.44504	,1.94986	  ,	 0	),
                    (-0.63697	,1.89585	  ,	 0	),
                    (-0.82257	,1.82301	  ,	 0	),
                    (-1.00000	,1.73205	  ,	 0	),
                    (-1.16749	,1.62388	  ,	 0	),
                    (-1.32337	,1.49956	  ,	 0	),
                    (-1.46610	,1.36035	  ,	 0	),
                    (-1.59427	,1.20761	  ,	 0	),
                    (-1.70658	,1.04287	  ,	 0	),
                    (-1.80194	,0.86777	  ,	 0	),
                    (-1.87939	,0.68404	  ,	 0	),
                    (-1.93815	,0.49351	  ,	 0	),
                    (-1.97766	,0.29808	  ,	 0	),
                    (-1.99751	,0.09969	  ,	 0	),
                    (-1.99751	,-0.09969	  ,	 0	),
                    (-1.97766	,-0.29808	  ,	 0	),
                    (-1.93815	,-0.49351	  ,	 0	),
                    (-1.87939	,-0.68404	  ,	 0	),
                    (-1.80194	,-0.86777	  ,	 0	),
                    (-1.70658	,-1.04287	  ,	 0	),
                    (-1.59427	,-1.20761	  ,	 0	),
                    (-1.46610	,-1.36035	  ,	 0	),
                    (-1.32337	,-1.49956	  ,	 0	),
                    (-1.16749	,-1.62388	  ,	 0	),
                    (-1.00000	,-1.73205	  ,	 0	),
                    (-0.82257	,-1.82301	  ,	 0	),
                    (-0.63697	,-1.89585	  ,	 0	),
                    (-0.44504	,-1.94986	  ,	 0	),
                    (-0.24869	,-1.98448	  ,	 0	),
                    (-0.04986	,-1.99938	  ,	 0	),
                    (0.14946   ,-1.99441	  ,	 0	),
                    (0.34730   ,-1.96962	  ,	 0	),
                    (0.54168   ,-1.92525	  ,	 0	),
                    (0.73068   ,-1.86175	  ,	 0	),
                    (0.91242   ,-1.77974	  ,	 0	),
                    (1.08509   ,-1.68005	  ,	 0	),
                    (1.24698   ,-1.56366	  ,	 0	),
                    (1.39647   ,-1.43173	  ,	 0	),
                    (1.53209   ,-1.28558	  ,	 0	),
                    (1.65248   ,-1.12664	  ,	 0	),
                    (1.75644   ,-0.95651	  ,	 0	),
                    (1.84295   ,-0.77687	  ,	 0	),
                    (1.91115   ,-0.58951	  ,	 0	),
                    (1.96035   ,-0.39629	  ,	 0	),
                    (1.99006   ,-0.19914	  ,	 0	),
                    (2.00000   ,0.00000	      ,	 0	),
                    (5.00000   ,0.00000	      ,	 10	),
                    (5.00000   ,0.00000	      ,	 0	),
                    (2.00000   ,0.00000	      ,	 10	),
                    (2.00000   ,0.00000	      ,	 0	),
		  
                         ]
                                        
    
    cordinate.point.setValues(0, 660, vertexPositions)
    indices= [1, 0, 101, -1, 1, 101, 102, -1,
                2, 102, 103, -1, 2, 1, 102, -1,
                3, 103, 104, -1, 3, 2, 103, -1,
                4, 104, 105, -1, 4, 3, 104, -1,
                5, 105, 106, -1, 5, 106, 107, -1,
                5, 4, 105, -1, 6, 5, 107, -1,
                7, 107, 108, -1, 7, 6, 107, -1,
                8, 108, 109, -1, 8, 7, 108, -1,
                9, 109, 110, -1, 9, 110, 111, -1,
                9, 8, 109, -1, 10, 111, 112, -1,
                10, 9, 111, -1, 11, 10, 112, -1,
                12, 112, 113, -1, 12, 113, 114, -1,
                12, 11, 112, -1, 13, 12, 114, -1,
                14, 114, 115, -1, 14, 13, 114, -1,
                15, 115, 116, -1, 15, 14, 115, -1,
                16, 116, 117, -1, 16, 15, 116, -1,
                17, 117, 118, -1, 17, 16, 117, -1,
                18, 118, 119, -1, 18, 17, 118, -1,
                19, 119, 120, -1, 19, 18, 119, -1,
                20, 120, 121, -1, 20, 121, 122, -1,
                20, 19, 120, -1, 21, 20, 122, -1,
                22, 122, 123, -1, 22, 21, 122, -1,
                23, 123, 124, -1, 23, 22, 123, -1,
                24, 124, 125, -1, 24, 125, 126, -1,
                24, 23, 124, -1, 25, 24, 126, -1,
                26, 25, 126, -1, 26, 126, 127, -1,
                26, 127, 128, -1, 27, 26, 128, -1,
                28, 27, 128, -1, 28, 128, 129, -1,
                29, 28, 129, -1, 29, 129, 130, -1,
                30, 29, 130, -1, 30, 130, 131, -1,
                31, 30, 131, -1, 31, 131, 132, -1,
                32, 132, 133, -1, 32, 31, 132, -1,
                33, 133, 134, -1, 33, 32, 133, -1,
                34, 134, 135, -1, 34, 33, 134, -1,
                35, 135, 136, -1, 35, 34, 135, -1,
                36, 136, 137, -1, 36, 35, 136, -1,
                37, 137, 138, -1, 37, 36, 137, -1,
                38, 138, 139, -1, 38, 37, 138, -1,
                39, 139, 140, -1, 39, 38, 139, -1,
                40, 140, 141, -1, 40, 141, 142, -1,
                40, 39, 140, -1, 41, 40, 142, -1,
                42, 142, 143, -1, 42, 143, 144, -1,
                42, 41, 142, -1, 43, 42, 144, -1,
                44, 144, 145, -1, 44, 145, 146, -1,
                44, 43, 144, -1, 45, 44, 146, -1,
                46, 146, 147, -1, 46, 45, 146, -1,
                47, 147, 148, -1, 47, 148, 149, -1,
                47, 46, 147, -1, 48, 47, 149, -1,
                49, 149, 150, -1, 49, 48, 149, -1,
                50, 49, 150, -1, 50, 150, 151, -1,
                51, 50, 151, -1, 51, 151, 152, -1,
                51, 152, 153, -1, 52, 51, 153, -1,
                53, 52, 153, -1, 53, 153, 154, -1,
                54, 53, 154, -1, 54, 154, 155, -1,
                55, 54, 155, -1, 55, 155, 156, -1,
                56, 55, 156, -1, 56, 156, 157, -1,
                56, 157, 158, -1, 57, 56, 158, -1,
                58, 57, 158, -1, 58, 158, 159, -1,
                59, 58, 159, -1, 59, 159, 160, -1,
                59, 160, 161, -1, 60, 59, 161, -1,
                61, 60, 161, -1, 61, 161, 162, -1,
                62, 61, 162, -1, 62, 162, 163, -1,
                63, 62, 163, -1, 63, 163, 164, -1,
                63, 164, 165, -1, 64, 63, 165, -1,
                64, 165, 166, -1, 65, 64, 166, -1,
                66, 166, 167, -1, 66, 65, 166, -1,
                67, 167, 168, -1, 67, 66, 167, -1,
                68, 168, 169, -1, 68, 67, 168, -1,
                69, 169, 170, -1, 69, 68, 169, -1,
                70, 170, 171, -1, 70, 69, 170, -1,
                71, 171, 172, -1, 71, 70, 171, -1,
                72, 172, 173, -1, 72, 173, 174, -1,
                72, 71, 172, -1, 73, 174, 175, -1,
                73, 72, 174, -1, 74, 73, 175, -1,
                75, 74, 175, -1, 75, 175, 176, -1,
                76, 75, 176, -1, 76, 176, 177, -1,
                77, 76, 177, -1, 77, 177, 178, -1,
                78, 77, 178, -1, 78, 178, 179, -1,
                79, 78, 179, -1, 79, 179, 180, -1,
                80, 79, 180, -1, 80, 180, 181, -1,
                81, 80, 181, -1, 81, 181, 182, -1,
                82, 81, 182, -1, 82, 182, 183, -1,
                83, 82, 183, -1, 83, 183, 184, -1,
                84, 83, 184, -1, 84, 184, 185, -1,
                85, 84, 185, -1, 85, 185, 186, -1,
                86, 85, 186, -1, 86, 186, 187, -1,
                87, 86, 187, -1, 87, 187, 188, -1,
                88, 87, 188, -1, 88, 188, 189, -1,
                89, 88, 189, -1, 89, 189, 190, -1,
                90, 89, 190, -1, 90, 190, 191, -1,
                90, 191, 192, -1, 91, 90, 192, -1,
                92, 91, 192, -1, 92, 192, 193, -1,
                93, 92, 193, -1, 93, 193, 194, -1,
                93, 194, 195, -1, 94, 93, 195, -1,
                95, 94, 195, -1, 95, 195, 196, -1,
                96, 95, 196, -1, 96, 196, 197, -1,
                97, 96, 197, -1, 97, 197, 198, -1,
                98, 97, 198, -1, 98, 198, 199, -1,
                99, 199, 200, -1, 99, 98, 199, -1,
                100, 99, 200, -1, 100, 200, 201, -1,
                341, 263, 264, -1, 341, 264, 265, -1,
                342, 341, 265, -1, 342, 265, 266, -1,
                340, 262, 263, -1, 340, 263, 341, -1,
                343, 342, 266, -1, 343, 266, 267, -1,
                343, 267, 268, -1, 339, 262, 340, -1,
                339, 260, 261, -1, 339, 261, 262, -1,
                344, 268, 269, -1, 344, 343, 268, -1,
                338, 260, 339, -1, 338, 258, 259, -1,
                338, 259, 260, -1, 345, 269, 270, -1,
                345, 270, 271, -1, 345, 344, 269, -1,
                337, 258, 338, -1, 337, 257, 258, -1,
                346, 271, 272, -1, 346, 272, 273, -1,
                346, 345, 271, -1, 336, 255, 256, -1,
                336, 256, 257, -1, 336, 257, 337, -1,
                347, 346, 273, -1, 347, 273, 274, -1,
                335, 255, 336, -1, 335, 254, 255, -1,
                348, 347, 274, -1, 348, 274, 275, -1,
                348, 275, 276, -1, 334, 254, 335, -1,
                334, 252, 253, -1, 334, 253, 254, -1,
                349, 276, 277, -1, 349, 348, 276, -1,
                333, 252, 334, -1, 333, 250, 251, -1,
                333, 251, 252, -1, 350, 277, 278, -1,
                350, 278, 279, -1, 350, 349, 277, -1,
                332, 250, 333, -1, 332, 249, 250, -1,
                351, 279, 280, -1, 351, 350, 279, -1,
                351, 280, 281, -1, 331, 249, 332, -1,
                331, 247, 248, -1, 331, 248, 249, -1,
                352, 281, 282, -1, 352, 351, 281, -1,
                330, 247, 331, -1, 330, 246, 247, -1,
                353, 282, 283, -1, 353, 283, 284, -1,
                353, 352, 282, -1, 329, 244, 245, -1,
                329, 245, 246, -1, 329, 246, 330, -1,
                354, 284, 285, -1, 354, 353, 284, -1,
                328, 242, 243, -1, 328, 243, 244, -1,
                328, 244, 329, -1, 355, 354, 285, -1,
                355, 285, 286, -1, 355, 286, 287, -1,
                327, 241, 242, -1, 327, 242, 328, -1,
                356, 355, 287, -1, 356, 287, 288, -1,
                289, 356, 288, -1, 326, 241, 327, -1,
                326, 240, 241, -1, 357, 356, 289, -1,
                290, 357, 289, -1, 239, 326, 325, -1,
                239, 240, 326, -1, 358, 357, 290, -1,
                291, 358, 290, -1, 238, 325, 324, -1,
                238, 239, 325, -1, 292, 358, 291, -1,
                292, 359, 358, -1, 237, 238, 324, -1,
                293, 359, 292, -1, 293, 360, 359, -1,
                236, 324, 323, -1, 236, 237, 324, -1,
                294, 360, 293, -1, 235, 323, 322, -1,
                235, 236, 323, -1, 295, 361, 360, -1,
                295, 360, 294, -1, 234, 235, 322, -1,
                296, 362, 361, -1, 296, 361, 295, -1,
                233, 322, 321, -1, 233, 234, 322, -1,
                297, 362, 296, -1, 232, 233, 321, -1,
                298, 362, 297, -1, 298, 363, 362, -1,
                231, 321, 320, -1, 231, 232, 321, -1,
                299, 363, 298, -1, 230, 320, 319, -1,
                230, 231, 320, -1, 300, 363, 299, -1,
                300, 364, 363, -1, 229, 230, 319, -1,
                301, 364, 300, -1, 301, 302, 364, -1,
                228, 229, 319, -1, 228, 319, 318, -1,
                227, 318, 317, -1, 227, 228, 318, -1,
                202, 302, 301, -1, 203, 303, 302, -1,
                203, 302, 202, -1, 226, 227, 317, -1,
                225, 317, 316, -1, 225, 226, 317, -1,
                204, 304, 303, -1, 204, 303, 203, -1,
                224, 225, 316, -1, 205, 304, 204, -1,
                223, 316, 315, -1, 223, 224, 316, -1,
                206, 305, 304, -1, 206, 304, 205, -1,
                222, 315, 314, -1, 222, 223, 315, -1,
                207, 305, 206, -1, 221, 222, 314, -1,
                208, 306, 305, -1, 208, 305, 207, -1,
                209, 307, 306, -1, 209, 306, 208, -1,
                220, 314, 313, -1, 220, 221, 314, -1,
                210, 307, 209, -1, 219, 220, 313, -1,
                219, 313, 312, -1, 218, 219, 312, -1,
                211, 308, 307, -1, 211, 307, 210, -1,
                212, 309, 308, -1, 212, 308, 211, -1,
                217, 312, 311, -1, 217, 218, 312, -1,
                213, 309, 212, -1, 216, 217, 311, -1,
                214, 310, 309, -1, 214, 309, 213, -1,
                215, 311, 310, -1, 215, 216, 311, -1,
                215, 310, 214, -1, 426, 504, 427, -1,
                427, 504, 428, -1, 504, 505, 428, -1,
                428, 505, 429, -1, 425, 503, 426, -1,
                426, 503, 504, -1, 505, 506, 429, -1,
                429, 506, 430, -1, 430, 506, 431, -1,
                425, 502, 503, -1, 423, 502, 424, -1,
                424, 502, 425, -1, 431, 507, 432, -1,
                506, 507, 431, -1, 423, 501, 502, -1,
                421, 501, 422, -1, 422, 501, 423, -1,
                432, 508, 433, -1, 433, 508, 434, -1,
                507, 508, 432, -1, 421, 500, 501, -1,
                420, 500, 421, -1, 434, 509, 435, -1,
                435, 509, 436, -1, 508, 509, 434, -1,
                418, 499, 419, -1, 419, 499, 420, -1,
                420, 499, 500, -1, 509, 510, 436, -1,
                436, 510, 437, -1, 418, 498, 499, -1,
                417, 498, 418, -1, 510, 511, 437, -1,
                437, 511, 438, -1, 438, 511, 439, -1,
                417, 497, 498, -1, 415, 497, 416, -1,
                416, 497, 417, -1, 439, 512, 440, -1,
                511, 512, 439, -1, 415, 496, 497, -1,
                413, 496, 414, -1, 414, 496, 415, -1,
                440, 513, 441, -1, 441, 513, 442, -1,
                512, 513, 440, -1, 413, 495, 496, -1,
                412, 495, 413, -1, 442, 514, 443, -1,
                513, 514, 442, -1, 443, 514, 444, -1,
                412, 494, 495, -1, 410, 494, 411, -1,
                411, 494, 412, -1, 444, 515, 445, -1,
                514, 515, 444, -1, 410, 493, 494, -1,
                409, 493, 410, -1, 445, 516, 446, -1,
                446, 516, 447, -1, 515, 516, 445, -1,
                407, 492, 408, -1, 408, 492, 409, -1,
                409, 492, 493, -1, 447, 517, 448, -1,
                516, 517, 447, -1, 405, 491, 406, -1,
                406, 491, 407, -1, 407, 491, 492, -1,
                517, 518, 448, -1, 448, 518, 449, -1,
                449, 518, 450, -1, 404, 490, 405, -1,
                405, 490, 491, -1, 518, 519, 450, -1,
                450, 519, 451, -1, 519, 452, 451, -1,
                404, 489, 490, -1, 403, 489, 404, -1,
                519, 520, 452, -1, 520, 453, 452, -1,
                489, 402, 488, -1, 403, 402, 489, -1,
                520, 521, 453, -1, 521, 454, 453, -1,
                488, 401, 487, -1, 402, 401, 488, -1,
                521, 455, 454, -1, 522, 455, 521, -1,
                401, 400, 487, -1, 522, 456, 455, -1,
                523, 456, 522, -1, 487, 399, 486, -1,
                400, 399, 487, -1, 523, 457, 456, -1,
                486, 398, 485, -1, 399, 398, 486, -1,
                524, 458, 523, -1, 523, 458, 457, -1,
                398, 397, 485, -1, 525, 459, 524, -1,
                524, 459, 458, -1, 485, 396, 484, -1,
                397, 396, 485, -1, 525, 460, 459, -1,
                396, 395, 484, -1, 525, 461, 460, -1,
                526, 461, 525, -1, 484, 394, 483, -1,
                395, 394, 484, -1, 526, 462, 461, -1,
                483, 393, 482, -1, 394, 393, 483, -1,
                526, 463, 462, -1, 527, 463, 526, -1,
                393, 392, 482, -1, 527, 464, 463, -1,
                465, 464, 527, -1, 392, 391, 482, -1,
                482, 391, 481, -1, 481, 390, 480, -1,
                391, 390, 481, -1, 465, 365, 464, -1,
                466, 366, 465, -1, 465, 366, 365, -1,
                390, 389, 480, -1, 480, 388, 479, -1,
                389, 388, 480, -1, 467, 367, 466, -1,
                466, 367, 366, -1, 388, 387, 479, -1,
                467, 368, 367, -1, 479, 386, 478, -1,
                387, 386, 479, -1, 468, 369, 467, -1,
                467, 369, 368, -1, 478, 385, 477, -1,
                386, 385, 478, -1, 468, 370, 369, -1,
                385, 384, 477, -1, 469, 371, 468, -1,
                468, 371, 370, -1, 470, 372, 469, -1,
                469, 372, 371, -1, 477, 383, 476, -1,
                384, 383, 477, -1, 470, 373, 372, -1,
                383, 382, 476, -1, 476, 382, 475, -1,
                382, 381, 475, -1, 471, 374, 470, -1,
                470, 374, 373, -1, 472, 375, 471, -1,
                471, 375, 374, -1, 475, 380, 474, -1,
                381, 380, 475, -1, 472, 376, 375, -1,
                380, 379, 474, -1, 473, 377, 472, -1,
                472, 377, 376, -1, 474, 378, 473, -1,
                379, 378, 474, -1, 473, 378, 377, -1,
                528, 529, 592, -1, 592, 529, 593, -1,
                529, 530, 593, -1, 593, 530, 594, -1,
                530, 531, 594, -1, 594, 531, 595, -1,
                531, 532, 595, -1, 595, 532, 596, -1,
                532, 533, 596, -1, 596, 533, 597, -1,
                597, 533, 598, -1, 533, 534, 598, -1,
                598, 534, 599, -1, 534, 535, 599, -1,
                535, 536, 599, -1, 599, 536, 600, -1,
                600, 536, 601, -1, 536, 537, 601, -1,
                537, 538, 601, -1, 601, 538, 602, -1,
                602, 539, 603, -1, 538, 539, 602, -1,
                603, 539, 604, -1, 539, 540, 604, -1,
                604, 541, 605, -1, 540, 541, 604, -1,
                605, 542, 606, -1, 541, 542, 605, -1,
                606, 543, 607, -1, 607, 543, 608, -1,
                542, 543, 606, -1, 543, 544, 608, -1,
                608, 545, 609, -1, 544, 545, 608, -1,
                545, 546, 609, -1, 609, 546, 610, -1,
                610, 546, 611, -1, 546, 547, 611, -1,
                547, 548, 611, -1, 611, 548, 612, -1,
                548, 549, 612, -1, 612, 549, 613, -1,
                549, 550, 613, -1, 613, 550, 614, -1,
                550, 551, 614, -1, 614, 551, 615, -1,
                551, 552, 615, -1, 615, 552, 616, -1,
                552, 553, 616, -1, 616, 553, 617, -1,
                553, 554, 617, -1, 617, 554, 618, -1,
                618, 554, 619, -1, 554, 555, 619, -1,
                555, 556, 619, -1, 619, 556, 620, -1,
                556, 557, 620, -1, 620, 557, 621, -1,
                557, 558, 621, -1, 621, 558, 622, -1,
                558, 559, 622, -1, 622, 559, 623, -1,
                559, 560, 623, -1, 623, 560, 624, -1,
                560, 561, 624, -1, 624, 561, 625, -1,
                561, 562, 625, -1, 625, 562, 626, -1,
                562, 563, 626, -1, 626, 563, 627, -1,
                627, 563, 628, -1, 563, 564, 628, -1,
                628, 565, 629, -1, 564, 565, 628, -1,
                629, 566, 630, -1, 565, 566, 629, -1,
                630, 567, 631, -1, 631, 567, 632, -1,
                566, 567, 630, -1, 632, 568, 633, -1,
                567, 568, 632, -1, 568, 569, 633, -1,
                633, 570, 634, -1, 634, 570, 635, -1,
                569, 570, 633, -1, 570, 571, 635, -1,
                635, 572, 636, -1, 571, 572, 635, -1,
                636, 572, 637, -1, 572, 573, 637, -1,
                637, 574, 638, -1, 573, 574, 637, -1,
                638, 575, 639, -1, 574, 575, 638, -1,
                639, 576, 640, -1, 640, 576, 641, -1,
                575, 576, 639, -1, 641, 577, 642, -1,
                576, 577, 641, -1, 642, 578, 643, -1,
                577, 578, 642, -1, 578, 579, 643, -1,
                643, 580, 644, -1, 644, 580, 645, -1,
                579, 580, 643, -1, 580, 581, 645, -1,
                645, 582, 646, -1, 646, 582, 647, -1,
                581, 582, 645, -1, 582, 583, 647, -1,
                647, 584, 648, -1, 583, 584, 647, -1,
                648, 585, 649, -1, 584, 585, 648, -1,
                649, 586, 650, -1, 650, 586, 651, -1,
                585, 586, 649, -1, 586, 587, 651, -1,
                651, 588, 652, -1, 652, 588, 653, -1,
                587, 588, 651, -1, 588, 589, 653, -1,
                653, 590, 654, -1, 654, 590, 655, -1,
                589, 590, 653, -1, 590, 591, 655, -1 
                ]
    soIndexFace.coordIndex.setValues(0, len(indices), indices)
    soSepArrow.addChild(cordinate) 
    soSepArrow.addChild(soIndexFace)

    root.addChild(trans)
    root.addChild(material)
    root.addChild(transform)
    root.addChild(soSepArrow)
    #Finalize the drawing by adding color, pos, scale , opacity
    return root







#**************************************************************************************************
#
#           The below part, is proof of concept. Not mented to be used in widget system.
#           You see in this example that you can create drawing using coindesigner and bring 
#           The whole script and put it in a variable and later use that variable to draw
#           the object. In the example the variable is 'arrow1_str'
#           It is better to convert the code you have in coindesigner to a real python code
#           as I did for the above widgets (circle, 2d arrow, ..etc)
#
#**************************************************************************************************

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
    """[2D Arrow - This version is more like an example how you can use Inventor 2.x code for drawing. Not attempted to be used in widgets]

    Args:
        p1 ([App.Vector], optional): [Position of the arrow]. Defaults to App.Vector(0,0,0).
        color ((float,float,float)), optional): [RGB Value between 0 to 1]. Defaults to FR_COLOR.FR_GOLD.
        scale ((float,float,float)), optional): [Scale factor for each axis]. Defaults to (1,1,1).
        type (int, optional): [Arrow type. At the moment there are 2 types]. Defaults to 1.
        opacity (int, optional): [Opacity of the drawn arrow]. Defaults to 0.
        _rotation (list, optional): [Rotation of the arrow provided by three float and an angle (float) in degree]. Defaults to [1.0, 0.0, 0.0, 0.0].

    Returns:
        [SoSeparator]: [SoSeparator which hold the drawing. Add it to the scenegraph to show the arrow]
    """
    if type == 0:

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
    transform.rotation.setValue(tempR, math.radians(_rotation[3]))

    input = coin.SoInput()
    input.setBuffer(arrow1_str)
    result = coin.SoDB.readAll(input)
    trans.translation.setValue(p1)
    if result is None:
        print("ERROR ")
        return None
    # Set up the duck transformations
    root.addChild(material)
    root.addChild(transform )
    root.addChild(trans)
    arrow.addChild(result)
    root.addChild(arrow)
    return root

#Save scenegraph to IV format 2.x

def saveSceneGraphtoIVfile(filename):
    """[Save current scenegraph to IV format]

    Args:
        filename ([str]): [pathname and file name ]
    """
    sg = Gui.ActiveDocument.ActiveView.getSceneGraph()
    sowriteAct=coin.SoWriteAction()
    sowriteAct.getOutput().openFile(filename)
    sowriteAct.getOutput().setBinary(False)
    sowriteAct.apply(sg)
    sowriteAct.getOutput().closeFile()
