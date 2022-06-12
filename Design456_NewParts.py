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
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
from draftutils.translate import translate   #for translate
import Design456Init
import FACE_D as faced
import DraftGeomUtils
import math
__updated__ = '2022-06-12 19:35:11'


#Roof

class ViewProviderRoof:

    obj_name = "Roof"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderRoof.obj_name
        obj.Proxy = self

    def attach(self, obj):
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self, obj):
        return "As Is"

    def getDefaultDisplayMode(self):
        return "As Is"

    def setDisplayMode(self, mode):
        return "As Is"

    def onChanged(self, vobj, prop):
        pass

    def getIcon(self):
        return ( Design456Init.ICON_PATH + 'Roof.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


#Roof 
class Design456_Roof:
    """ Roof shape based on several parameters
    """
    def __init__(self, obj, 
                       width=20,
                       length=20,
                       height=10,
                       thickness=1):


        obj.addProperty("App::PropertyLength", "Width","Roof", 
                        "Width of the Roof").Width = width

        obj.addProperty("App::PropertyLength", "Length","Roof", 
                        "Length of the Roof").Length = length

        obj.addProperty("App::PropertyLength", "Height","Roof", 
                        "Height of the Roof").Height = height

        obj.addProperty("App::PropertyLength", "Thickness","Roof", 
                        "Thickness of the Roof").Thickness = thickness
        obj.Proxy = self
    
    def execute(self, obj):
        self.Width=float(obj.Width)
        self.Height=float(obj.Height)
        self.Length=float(obj.Length)
        self.Thickness=float(obj.Thickness)
        vert1=[App.Vector(0,0,0),App.Vector(self.Width,0,0),
                App.Vector(self.Width/2,0.0,self.Height),
                App.Vector(0,0,0)]
        newWidth=self.Width-2*self.Thickness
        newLength=self.Length-2*self.Thickness
        newHeight=self.Height-self.Thickness
        vert2=[App.Vector(self.Thickness,self.Thickness,0),App.Vector(self.Thickness+newWidth,self.Thickness,0),
               App.Vector(self.Width/2,self.Thickness,newHeight),
               App.Vector(self.Thickness,self.Thickness,0)]
        FaceTriangle1=Part.Face(Part.makePolygon(vert1))
        obj1 =FaceTriangle1.extrude(App.Vector(0.0,self.Length,0.0))
        
        FaceTriangle2=Part.Face(Part.makePolygon(vert2))
        obj2= FaceTriangle2.extrude(App.Vector(0.0,self.Length-2*self.Thickness,0.0))
        Result = obj1.cut(obj2)
        obj.Shape=Result
        
class Design456_Seg_Roof:
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'Roof.svg',
                'MenuText': "Roof",
                'ToolTip': "Generate a Roof"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Roof")
        Design456_Roof(newObj)

        ViewProviderRoof(newObj.ViewObject, "Roof")

        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_Seg_Roof', Design456_Seg_Roof())


#***************************



#Housing

class ViewProviderHousing:

    obj_name = "Housing"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderHousing.obj_name
        obj.Proxy = self

    def attach(self, obj):
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self, obj):
        return "As Is"

    def getDefaultDisplayMode(self):
        return "As Is"

    def setDisplayMode(self, mode):
        return "As Is"

    def onChanged(self, vobj, prop):
        pass

    def getIcon(self):
        return ( Design456Init.ICON_PATH + 'Housing.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


#Housing 
class Design456_HousingBase:
    """ Housing shape based on several parameters
    """
    def __init__(self, obj, 
                       width=20,
                       length=20,
                       height=10,
                       thickness=1):


        obj.addProperty("App::PropertyLength", "Width","Housing", 
                        "Width of the Housing").Width = width

        obj.addProperty("App::PropertyLength", "Length","Housing", 
                        "Length of the Housing").Length = length

        obj.addProperty("App::PropertyLength", "Height","Housing", 
                        "Height of the Housing").Height = height

        obj.addProperty("App::PropertyLength", "Thickness","Housing", 
                        "Thickness of the Housing").Thickness = thickness
        obj.Proxy = self
    
    def execute(self, obj):
        self.Width=float(obj.Width)
        self.Height=float(obj.Height)
        self.Length=float(obj.Length)
        self.Thickness=float(obj.Thickness)
        Result=None
        V1_FSQ=[App.Vector(0,0,0),
                 App.Vector(self.Width,0,0),
                 App.Vector(self.Width,self.Length,0),
                 App.Vector(0.0,self.Length,0),
                 App.Vector(0,0,0)]

        V2_FSQ=[App.Vector(self.Thickness,self.Thickness,0),
                 App.Vector(self.Width-self.Thickness,self.Thickness,0),
                 App.Vector(self.Width-self.Thickness,self.Length-self.Thickness,0),
                 App.Vector(self.Thickness,self.Length-self.Thickness,0),
                 App.Vector(self.Thickness,self.Thickness,0)]
        firstFace1=Part.Face(Part.makePolygon(V1_FSQ))  # one used with secondFace to cut
        firstFace2=Part.Face(Part.makePolygon(V1_FSQ))  # Other used to make the bottom
        secondFace=Part.Face(Part.makePolygon(V2_FSQ))
        resultButtom=firstFace1.cut(secondFace)
        extrude1=resultButtom.extrude(App.Vector(0,0,self.Height))
        extrude2=firstFace2.extrude(App.Vector(0,0,self.Thickness))
        fused=extrude1.fuse(extrude2)
        Result=fused.removeSplitter()
        obj.Shape=Result
        
class Design456_Housing:
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'Housing.svg',
                'MenuText': "Housing",
                'ToolTip': "Generate a Housing"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Housing")
        Design456_HousingBase(newObj)

        ViewProviderHousing(newObj.ViewObject, "Housing")

        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_Housing', Design456_Housing())





#RoundedHousing

class ViewProviderRoundedHousing:

    obj_name = "RoundedHousing"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderRoundedHousing.obj_name
        obj.Proxy = self

    def attach(self, obj):
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self, obj):
        return "As Is"

    def getDefaultDisplayMode(self):
        return "As Is"

    def setDisplayMode(self, mode):
        return "As Is"

    def onChanged(self, vobj, prop):
        pass

    def getIcon(self):
        return ( Design456Init.ICON_PATH + 'RoundedHousing.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

################################


#RoundedHousing 
class Design456_RoundedHousingBase:
    """ RoundedHousing shape based on several parameters
    """
    def __init__(self, obj, 
                       width=20,
                       length=20,
                       height=10,
                       radius=1,
                       thickness=1,chamfer=False):


        obj.addProperty("App::PropertyLength", "Width","RoundedHousing", 
                        "Width of the RoundedHousing").Width = width

        obj.addProperty("App::PropertyLength", "Length","RoundedHousing", 
                        "Length of the RoundedHousing").Length = length

        obj.addProperty("App::PropertyLength", "Height","RoundedHousing", 
                        "Height of the RoundedHousing").Height = height

        obj.addProperty("App::PropertyLength", "Radius","RoundedHousing", 
                        "Height of the RoundedHousing").Radius = radius

        obj.addProperty("App::PropertyLength", "Thickness","RoundedHousing", 
                        "Thickness of the RoundedHousing").Thickness = thickness

        obj.addProperty("App::PropertyBool", "Chamfer","RoundedHousing", 
                        "Chamfer corner").Chamfer = chamfer
        obj.Proxy = self
    
    def execute(self, obj):
        self.Width=float(obj.Width)
        self.Height=float(obj.Height)
        self.Length=float(obj.Length)
        self.Radius=float(obj.Radius)
        self.Thickness=float(obj.Thickness)
        self.Chamfer=obj.Chamfer
        Result=None
        # base rectangle vertices and walls after a cut
        V1_FSQ=[App.Vector(0,0,0),
                App.Vector(self.Width,0,0),
                App.Vector(self.Width,self.Length,0),
                App.Vector(0.0,self.Length,0),
                App.Vector(0,0,0)]

        # cut middle part to make walls
        V2_FSQ=[App.Vector(self.Thickness,self.Thickness,0),
                App.Vector(self.Width-self.Thickness,self.Thickness,0),
                App.Vector(self.Width-self.Thickness,self.Length-self.Thickness,0),
                App.Vector(self.Thickness,self.Length-self.Thickness,0),
                App.Vector(self.Thickness,self.Thickness,0)]
        
        W1=Part.makePolygon(V1_FSQ)
        W11 = DraftGeomUtils.filletWire(W1,self.Radius, chamfer=self.Chamfer)
        
        firstFace1=Part.Face(W11)  # one used with secondFace to cut
        firstFace2=firstFace1.copy()  # Other used to make the bottom

        W2=Part.makePolygon(V2_FSQ)
        W22 = DraftGeomUtils.filletWire(W2,self.Radius, chamfer=self.Chamfer)
        
        secondFace=Part.Face(W22)

        resultButtom=firstFace1.cut(secondFace)
        extrude1=resultButtom.extrude(App.Vector(0,0,self.Height))
        extrude2=firstFace2.extrude(App.Vector(0,0,self.Thickness))
        fused=extrude1.fuse(extrude2)
        Result=fused.removeSplitter()
        obj.Shape=Result
        
class Design456_RoundedHousing:
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'RoundedHousing.svg',
                'MenuText': "RoundedHousing",
                'ToolTip': "Generate a RoundedHousing"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "RoundedHousing")
        Design456_RoundedHousingBase(newObj)

        ViewProviderRoundedHousing(newObj.ViewObject, "RoundedHousing")

        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_RoundedHousing', Design456_RoundedHousing())


###########################33


#EllipseBox

class ViewProviderEllipseBox:

    obj_name = "EllipseBoxBase"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderEllipseBox.obj_name
        obj.Proxy = self

    def attach(self, obj):
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self, obj):
        return "As Is"

    def getDefaultDisplayMode(self):
        return "As Is"

    def setDisplayMode(self, mode):
        return "As Is"

    def onChanged(self, vobj, prop):
        pass

    def getIcon(self):
        return ( Design456Init.ICON_PATH + 'EllipseBoxBase.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

#EllipseBoxBase
class Design456_EllipseBoxBase:
    """ EllipseHousingshape based on several parameters
    """
    def __init__(self, obj, 
                       height=10,
                       major_radius=10,
                       minor_radius=8,
                       thickness=1):

        obj.addProperty("App::PropertyLength", "Height","EllipseBox", 
                        "Height of the EllipseBox").Height = height

        obj.addProperty("App::PropertyLength", "MajorRadius","EllipseBox", 
                        "Height of the EllipseBox").MajorRadius = major_radius
        
        obj.addProperty("App::PropertyLength", "MinorRadius","EllipseBox", 
                        "Height of the EllipseBox").MinorRadius = minor_radius

        obj.addProperty("App::PropertyLength", "Thickness","EllipseBox", 
                        "Thickness of the EllipseBox").Thickness = thickness

        obj.Proxy = self
    
    def execute(self, obj):
        self.Height=float(obj.Height)
        self.MajorRadius=float(obj.MajorRadius)
        self.MinorRadius=float(obj.MinorRadius)
        self.Thickness=float(obj.Thickness)
        Result=None
        # base Ellipse vertices and walls after a cut

        if(self.MajorRadius<self.MinorRadius):
            self.MajorRadius=self.MinorRadius
            print("Major Radius must be grater or equal to Minor Radius")
        Center=App.Vector(App.Vector(0,0,0))
        W1=Part.Ellipse(Center,self.MajorRadius,self.MinorRadius)
        firstFace1=Part.Face(Part.Wire(W1.toShape()))  # one used with secondFace to cut
        firstFace2=firstFace1.copy()  # Other used to make the bottom

        
        W2=Part.Ellipse(Center,self.MajorRadius-self.Thickness,self.MinorRadius-self.Thickness)
        secondFace=Part.Face(Part.Wire(W2.toShape()))
        resultButtom=firstFace1.cut(secondFace)
        extrude1=resultButtom.extrude(App.Vector(0,0,self.Height))
        extrude2=firstFace2.extrude(App.Vector(0,0,self.Thickness))
        fused=extrude1.fuse(extrude2)
        Result=fused.removeSplitter()
        obj.Shape=Result
        
class Design456_EllipseBox:
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'EllipseBox.svg',
                'MenuText': "EllipseBox",
                'ToolTip': "Generate a EllipseBox"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "EllipseBox")
        Design456_EllipseBoxBase(newObj)

        ViewProviderEllipseBox(newObj.ViewObject, "EllipseBox")

        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_EllipseBox', Design456_EllipseBox())


############################

#NonuniformedBox

class ViewProviderNoneUniformBox:

    obj_name = "NonuniformedBoxBase"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderNoneUniformBox.obj_name
        obj.Proxy = self

    def attach(self, obj):
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self, obj):
        return "As Is"

    def getDefaultDisplayMode(self):
        return "As Is"

    def setDisplayMode(self, mode):
        return "As Is"

    def onChanged(self, vobj, prop):
        pass

    def getIcon(self):
        return ( Design456Init.ICON_PATH + 'NonuniformedBox.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

#NonuniformedBox
class Design456_NonuniformedBoxBase:
    """ NonuniformedBoxshape based on several parameters
    """
    def __init__(self, obj, 
                       height=10,
                       radius=1,
                       thickness=1,
                       base_radius=1,
                       vertices=[], chamfer=False):

        obj.addProperty("App::PropertyLength", "Height","NonuniformedBox", 
                        "Height of the NonuniformedBox").Height = height
        obj.addProperty("App::PropertyLength", "Thickness","NonuniformedBox", 
                        "Thickness of the NonuniformedBox").Thickness = thickness
                        
        obj.addProperty("App::PropertyBool", "Chamfer","RoundedHousing", 
                        "Chamfer corner").Chamfer = chamfer
                        
        obj.addProperty("App::PropertyLength", "Radius","RoundedHousing", 
                        "Radius of the NonuniformedBox").Radius = radius

        obj.addProperty("App::PropertyLength", "SideOneRadius","RoundedHousing", 
                        "Base Radius of the NonuniformedBox").SideOneRadius = base_radius
                        

        obj.Proxy = self
        s=Gui.Selection.getSelectionEx()
        self.Vertices=[]
        if len(s)>2:
            self.Vertices.clear()
            for subObj in s:
                self.Vertices.append(subObj.Object.Shape.Vertexes[0].Point)
            self.Vertices.append(s[0].Object.Shape.Vertexes[0].Point)
            
    def execute(self, obj):
        self.Height=float(obj.Height)
        self.Radius=float(obj.Radius)
        self.SideOneRadius=float(obj.SideOneRadius)
        self.Thickness=float(obj.Thickness)
        self.Chamfer=obj.Chamfer
    
        Result=None
        # base None-uniformed vertices and walls after a cut

        V1_FSQ=[]
        V1_FSQ=self.Vertices
        W1=Part.makePolygon(V1_FSQ)

        if self.Radius>0:
            W11 = DraftGeomUtils.filletWire(W1,self.Radius, chamfer=self.Chamfer)
        else:
            W11=W1
        
        firstFace1=Part.Face(W11)  # One used with secondFace to cut
        
        if self.SideOneRadius>0:
            W12 = DraftGeomUtils.filletWire(W1,self.SideOneRadius, chamfer=self.Chamfer)
        else:
            W12=W1  # Other used to make the bottom
        
        firstFace2=Part.Face(W12) 
        secondFace= firstFace2.makeOffset2D(-self.Thickness)
        resultButtom=firstFace1.cut(secondFace)
        extrude1=resultButtom.extrude(App.Vector(0,0,self.Height))
        extrude2=firstFace2.extrude(App.Vector(0,0,self.Thickness))
        fused=extrude1.fuse(extrude2)
        Result=fused.removeSplitter()
        obj.Shape=Result
        
class Design456_NonuniformedBox:
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'NonuniformedBox.svg',
                'MenuText': "NonuniformedBox",
                'ToolTip': "Generate a NonuniformedBox"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "NonuniformedBox")
        Design456_NonuniformedBoxBase(newObj)

        ViewProviderNoneUniformBox(newObj.ViewObject, "NonuniformedBox")

        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_NonuniformedBox', Design456_NonuniformedBox())



############################

#Paraboloid

class ViewProviderParaboloid:

    obj_name = "ParaboloidBase"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderNoneUniformBox.obj_name
        obj.Proxy = self

    def attach(self, obj):
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self, obj):
        return "As Is"

    def getDefaultDisplayMode(self):
        return "As Is"

    def setDisplayMode(self, mode):
        return "As Is"

    def onChanged(self, vobj, prop):
        pass

    def getIcon(self):
        return ( Design456Init.ICON_PATH + 'Paraboloid.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

###########################################################################
#Paraboloid
class Design456_ParaboloidBase:
    """ Paraboloidshape based on several parameters
    """
    def __init__(self, obj, 
                       height=10,
                       base_radius=10,
                       middle_radius=8,
                       ):

        obj.addProperty("App::PropertyLength", "Height","Paraboloid", 
                        "Height of the Paraboloid").Height = height

        obj.addProperty("App::PropertyLength", "BaseRadius","Paraboloid", 
                        "Base Radius of the Paraboloid").BaseRadius = base_radius

        obj.addProperty("App::PropertyLength", "MiddleRadius","Paraboloid", 
                        "Base Radius of the Paraboloid").MiddleRadius = middle_radius

        self.points=[]                       
        obj.Proxy = self

            
    def execute(self, obj):
        self.Height=float(obj.Height)
        self.BaseRadius=float(obj.BaseRadius)
        self.MiddleRadius=float(obj.MiddleRadius)
        point1=App.Vector(self.BaseRadius,0,0)
        point2=App.Vector(self.MiddleRadius,0,self.Height/2)
        point3=App.Vector(0,0,self.Height)
        Result=None
        bsp=Part.BSplineCurve()
        bsp.buildFromPoles([point1,point2,point3])
        shp=bsp.toShape()
        circle=Part.makeCircle(self.BaseRadius, App.Vector(0,0,0),App.Vector(0,0,1))
        sweep=Part.makeSweepSurface(circle,shp)
        base=Part.Face(Part.Wire(circle))
        shell1=Part.Shell([base,sweep])

        nResult=Part.makeSolid(shell1)
        Result=nResult.removeSplitter()
        obj.Shape=Result
        
class Design456_Paraboloid:
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'Paraboloid.svg',
                'MenuText': "Paraboloid",
                'ToolTip': "Generate a Paraboloid"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Paraboloid")
        Design456_ParaboloidBase(newObj)

        ViewProviderParaboloid(newObj.ViewObject, "Paraboloid")

        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_Paraboloid', Design456_Paraboloid())


################################

#Capsule

class ViewProviderCapsule:

    obj_name = "CapsuleBase"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderNoneUniformBox.obj_name
        obj.Proxy = self

    def attach(self, obj):
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self, obj):
        return "As Is"

    def getDefaultDisplayMode(self):
        return "As Is"

    def setDisplayMode(self, mode):
        return "As Is"

    def onChanged(self, vobj, prop):
        pass

    def getIcon(self):
        return ( Design456Init.ICON_PATH + 'Capsule.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

########################################################################### 

#Capsule
class Design456_CapsuleBase:
    """ Capsuleshape based on several parameters
    """
    def __init__(self, obj, 
                       length=20,
                       side_R_radius=5,
                       side_L_radius=5,
                       height_radius=5,
                       ):

        obj.addProperty("App::PropertyLength", "Length","Capsule", 
                        "Length of the Capsule").Length = length

        obj.addProperty("App::PropertyFloat", "SideRightRadius","Capsule", 
                        "Base Radius of the Capsule").SideRightRadius = side_R_radius
        obj.addProperty("App::PropertyFloat", "SideLeftRadius","Capsule", 
                        "Base Radius of the Capsule").SideLeftRadius = side_L_radius
                        
        obj.addProperty("App::PropertyFloat", "HeightRadius","Capsule", 
                        "Base Radius of the Capsule").HeightRadius = height_radius
        obj.Proxy = self

            
    def execute(self, obj):
        self.Length=float(obj.Length)
        self.SideRightRadius=float(obj.SideRightRadius)
        self.SideLeftRadius=float(obj.SideLeftRadius)
        self.HeightRadius=float(obj.HeightRadius)
        middle=Part.makeCylinder(self.HeightRadius,self.Length,App.Vector(-self.Length/2,0,0),App.Vector(1,0,0),360)
        left=Part.makeSphere(self.SideLeftRadius,App.Vector(-self.Length/2,0,0),App.Vector(1,0,0))
        right=Part.makeSphere(self.SideRightRadius,App.Vector(self.Length/2,0,0),App.Vector(1,0,0))
        shpt=middle.fuse([right,left])
        Result=shpt.removeSplitter()
        obj.Shape=Result
        
class Design456_Capsule:
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'capsule.svg',
                'MenuText': "Capsule",
                'ToolTip': "Generate a Capsule"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Capsule")
        Design456_CapsuleBase(newObj)

        ViewProviderCapsule(newObj.ViewObject, "Capsule")

        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_Capsule', Design456_Capsule())

#################################


#Parallelepiped

class ViewProviderParallelepiped:

    obj_name = "ParallelepipedBase"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderNoneUniformBox.obj_name
        obj.Proxy = self

    def attach(self, obj):
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self, obj):
        return "As Is"

    def getDefaultDisplayMode(self):
        return "As Is"

    def setDisplayMode(self, mode):
        return "As Is"

    def onChanged(self, vobj, prop):
        pass

    def getIcon(self):
        return ( Design456Init.ICON_PATH + 'Parallelepiped.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

########################################################################### TODO: FIXME:
#Parallelepiped

class Design456_ParallelepipedBase:
    """ Parallelepipedshape based on several parameters
    """
    def __init__(self, obj, 
                       height=10,
                       length=10,
                       width=30,
                       anglex=30,
                       angley=30,
                       ):

        obj.addProperty("App::PropertyLength", "Height","Parallelepiped", 
                        "Height of the Parallelepiped").Height = height

        obj.addProperty("App::PropertyLength", "Length","Parallelepiped", 
                        "length of the Parallelepiped").Length = length

        obj.addProperty("App::PropertyLength", "Width","Parallelepiped", 
                        "Width of the Parallelepiped").Width = width

        obj.addProperty("App::PropertyAngle", "AngleX","Parallelepiped", 
                        "Angle of the Parallelepiped").AngleX = anglex

        obj.addProperty("App::PropertyAngle", "AngleY","Parallelepiped", 
                        "Angle of the Parallelepiped").AngleY = angley
                                    
        obj.Proxy = self

            
    def execute(self, obj):
        self.Height=float(obj.Height)
        self.Length=float(obj.Length)
        self.Width=float(obj.Width)
        self.AngleX= float(obj.AngleX)
        self.AngleY= float(obj.AngleY)

        p1=App.Vector(-self.Width/2,self.Length/2,0)    # - +  
        p2=App.Vector(self.Width/2,self.Length/2,0)     # + +  
        p3=App.Vector(self.Width/2,-self.Length/2,0)    # - +  
        p4=App.Vector(-self.Width/2,-self.Length/2,0)   # - -

        shiftSizeX=self.Height * math.cos(math.radians(90-self.AngleX))
        shiftSizeY=self.Height * math.cos(math.radians(90-self.AngleY))
        
        p11=App.Vector(shiftSizeX-self.Width/2,shiftSizeY+self.Length/2,self.Height)
        p22=App.Vector(shiftSizeX+self.Width/2,shiftSizeY+self.Length/2,self.Height)
        p33=App.Vector(shiftSizeX+self.Width/2,shiftSizeY-self.Length/2,self.Height)
        p44=App.Vector(shiftSizeX-self.Width/2,shiftSizeY-self.Length/2,self.Height)

        bottom=Part.makePolygon([p1,p2,p3,p4,p1])
        top=Part.makePolygon([p11,p22,p33,p44,p11])
        left=Part.makePolygon([p4,p44,p11,p1,p4])
        right=Part.makePolygon([p33,p22,p2,p3,p33])
        front=Part.makePolygon([p4,p44,p33,p3,p4])
        back=Part.makePolygon([p1,p11,p22,p2,p1])

        W1=Part.Wire(bottom)
        W2=Part.Wire(top)
        W3=Part.Wire(left)
        W4=Part.Wire(right)
        W5=Part.Wire(front)
        W6=Part.Wire(back)
        f1=Part.Face(W1)
        f2=Part.Face(W2)
        f3=Part.Face(W3)
        f4=Part.Face(W4)
        f5=Part.Face(W5)
        f6=Part.Face(W6)
        shell=Part.makeShell([f1,f2,f3,f4,f5,f6])
        Result=Part.Solid(shell)
        obj.Shape=Result
        
class Design456_Parallelepiped:
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'Parallelepiped.svg',
                'MenuText': "Parallelepiped",
                'ToolTip': "Generate a Parallelepiped"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Parallelepiped")
        Design456_ParallelepipedBase(newObj)

        ViewProviderParallelepiped(newObj.ViewObject, "Parallelepiped")

        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_Parallelepiped', Design456_Parallelepiped())


####################
#RoundRoof

class ViewProviderRoundRoof:

    obj_name = "RoundRoof"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderRoundRoof.obj_name
        obj.Proxy = self

    def attach(self, obj):
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self, obj):
        return "As Is"

    def getDefaultDisplayMode(self):
        return "As Is"

    def setDisplayMode(self, mode):
        return "As Is"

    def onChanged(self, vobj, prop):
        pass

    def getIcon(self):
        return ( Design456Init.ICON_PATH + 'RoundRoof.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


#RoundRoof 
class Design456_BaseRoundRoof:
    """ RoundRoof shape based on several parameters
    """
    def __init__(self, obj, 
                       width=20,
                       length=20,
                       height=10,
                       thickness=1):

        obj.addProperty("App::PropertyLength", "Width","RoundRoof", 
                        "Width of the RoundRoof").Width = width

        obj.addProperty("App::PropertyLength", "Length","RoundRoof", 
                        "Length of the RoundRoof").Length = length

        obj.addProperty("App::PropertyLength", "Height","RoundRoof", 
                        "Height of the RoundRoof").Height = height

        obj.addProperty("App::PropertyLength", "Thickness","RoundRoof", 
                        "Thickness of the RoundRoof").Thickness = thickness

        obj.Proxy = self
    
    def execute(self, obj):
        self.Width=float(obj.Width)
        self.Height=float(obj.Height)
        self.Length=float(obj.Length)
        self.Thickness=float(obj.Thickness)
        Result=None

        p1=App.Vector(0,0,0)
        p2=App.Vector(0,self.Length/2,self.Height)
        p3=App.Vector(0,self.Length,0)

        p11=App.Vector(p1.x+self.Thickness,p1.y+self.Thickness,p1.z)
        p22=App.Vector(p2.x+self.Thickness,p2.y,p2.z-self.Thickness)
        p33=App.Vector(p3.x+self.Thickness,p3.y-self.Thickness,p3.z)

        c1= Part.ArcOfCircle(p1,p2,p3)
        c11=c1.copy()
        l1=Part.LineSegment(p1,p3)
        
        c2=Part.ArcOfCircle(p11,p22,p33)
        l2=Part.LineSegment(p11,p33)
                
        W1=Part.Wire([c1.toShape(),l1.toShape()])
        W2=Part.Wire([c2.toShape(),l2.toShape()])
        f1=Part.Face(W1)
        f2=Part.Face(W2)
        obj1=f1.extrude(App.Vector(self.Width,0,0))
        obj2=f2.extrude(App.Vector(self.Width-2*self.Thickness,0,0))
        Result=obj1.cut(obj2)
        obj.Shape=Result

class Design456_RoundRoof:
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'RoundRoof.svg',
                'MenuText': "RoundRoof",
                'ToolTip': "Generate a RoundRoof"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "RoundRoof")
        Design456_BaseRoundRoof(newObj)

        ViewProviderRoundRoof(newObj.ViewObject, "RoundRoof")

        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_RoundRoof', Design456_RoundRoof())


####################################

#FlowerVase

class ViewProviderFlowerVase:

    obj_name = "FlowerVase"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderFlowerVase.obj_name
        obj.Proxy = self

    def attach(self, obj):
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self, obj):
        return "As Is"

    def getDefaultDisplayMode(self):
        return "As Is"

    def setDisplayMode(self, mode):
        return "As Is"

    def onChanged(self, vobj, prop):
        pass

    def getIcon(self):
        return ( Design456Init.ICON_PATH + 'FlowerVase.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


#FlowerVase 
class Design456_BaseFlowerVase:
    """ FlowerVase shape based on several parameters
    """
    def __init__(self, obj, 
                       _baseType="Circle",
                       _middleType="Polygon",
                       _topType="Circle",
                       _baseSides=8,
                       _middleSides=8,
                       _topSides=8,
                       _baseRadius=10,
                       _middleRadius=20,
                       _topRadius=5,
                       _height=20,
                       _neckHeight=2,
                        _solid=True,
                        _withContact=False,
                        _withCorrection=False):

        obj.addProperty("App::PropertyEnumeration", "baseType","1)Sections", 
                        "FlowerVase base type").baseType = ["Circle","Polygon"]
        obj.baseType=_baseType

        obj.addProperty("App::PropertyEnumeration", "middleType","1)Sections", 
                        "FlowerVase middle type").middleType = ["Circle","Polygon"]
        obj.middleType=_middleType

        obj.addProperty("App::PropertyEnumeration", "topType","1)Sections", 
                        "FlowerVase top type").topType = ["Circle","Polygon"]
        obj.topType=_topType

        obj.addProperty("App::PropertyLength", "baseRadius","2)Radius", 
                        "Length of the FlowerVase").baseRadius = _baseRadius

        obj.addProperty("App::PropertyLength", "middleRadius","2)Radius", 
                        "Length of the FlowerVase").middleRadius = _middleRadius

        obj.addProperty("App::PropertyLength", "topRadius","2)Radius", 
                        "Length of the FlowerVase").topRadius = _topRadius


        obj.addProperty("App::PropertyLength", "Height","3)Others", 
                        "Height of the FlowerVase").Height = _height
        
        obj.addProperty("App::PropertyLength", "neckHeight","3)Others", 
                        "Height of the FlowerVase").neckHeight = _neckHeight

        obj.addProperty("App::PropertyInteger", "baseSides","3)Others", 
                        "base sides of the FlowerVase").baseSides = _baseSides
        obj.addProperty("App::PropertyInteger", "middleSides","3)Others", 
                        "middle sides of the FlowerVase").middleSides = _middleSides
        obj.addProperty("App::PropertyInteger", "topSides","3)Others", 
                        "top sides of the FlowerVase").topSides = _topSides
        
        obj.addProperty("App::PropertyBool", "Solid","3)Others", 
                        "FlowerVase top type").Solid=_solid
        obj.addProperty("App::PropertyBool", "WithContact","3)Others", 
                        "FlowerVase top type").WithContact=_withContact
        obj.addProperty("App::PropertyBool", "WithCorrection","3)Others", 
                        "FlowerVase top type").WithCorrection=_withCorrection
        obj.Proxy = self
        self.Type ="FlowerVase"
        
 
            
    def calculatePolygonVertices(self,radius,sides,plc,Zaxis=0.0):
        try:
            vertices=[]
            slice=360/sides
            _angle=math.radians(slice)
            for i in range(0, sides+1):
                x=plc.Base.x+(radius * math.cos(_angle*i))
                y=plc.Base.y+(radius *math.sin(_angle*i))
                z=Zaxis+plc.Base.z
                point = App.Vector(x,y, z)
                vertices.append(point)
            return vertices
        
        except Exception as err:
            App.Console.PrintError("'calculatePolygonVertices' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
                
    def execute(self, obj):
        try:
            self.plc=App.Placement()
            self.plc.Base=App.Vector(0,0,0)
            self.plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
            self.baseType=str(obj.baseType)
            self.middleType=str(obj.middleType)
            self.topType=str(obj.topType)

            self.baseRadius=float(obj.baseRadius)
            self.middleRadius=float(obj.middleRadius)
            self.topRadius=float(obj.topRadius)

            self.Height=float(obj.Height)
            self.neckHeight=float(obj.neckHeight)
            self.Result=None

            self.baseObj=None
            self.middleObj=None
            self.topObj = None
            self.baseObj=None
            self.sweepPath=None
            self.Solid=obj.Solid
            self.baseSides=obj.baseSides
            self.middleSides=obj.middleSides
            self.topSides=obj.topSides
            self.WithContact=obj.WithContact
            self.WithCorrection=obj.WithCorrection
            obj.Placement=self.plc

            if self.baseType=="Circle":                                #(self,radius,sides,plc,Zaxis=0.0):
                self.baseObj=Part.Wire(Part.makeCircle(self.baseRadius,obj.Placement.Base, App.Vector(0,0,1),0,360))
            elif self.baseType=="Polygon":
                self.baseObj=Part.makePolygon(self.calculatePolygonVertices(self.baseRadius,self.baseSides,self.plc))

            if self.middleType=="Circle":
                self.middleObj=Part.Wire(Part.makeCircle(self.middleRadius,App.Vector(0,0,(self.Height-self.neckHeight)/2), App.Vector(0,0,1),0,360))
            elif self.middleType=="Polygon":
                self.middleObj=Part.makePolygon(self.calculatePolygonVertices(self.middleRadius,self.middleSides,self.plc,(self.Height-self.neckHeight)/2))

            if self.topType=="Circle":
                self.topObj=Part.Wire(Part.makeCircle(self.topRadius,App.Vector(0,0,(self.Height-self.neckHeight)), App.Vector(0,0,1),0,360))
            elif self.middleType=="Polygon":
                self.topObj=Part.makePolygon(self.calculatePolygonVertices(self.topRadius,self.topSides,self.plc,(self.Height-self.neckHeight)))
          
            try:
                self.sweepPath = Part.makePolygon([App.Vector(0,0,0),App.Vector(0,0,self.Height)]) #must be the total height
                tnObj=Part.BRepOffsetAPI.MakePipeShell(self.sweepPath)
                tnObj.add(self.baseObj,self.WithContact,self.WithCorrection)
                tnObj.add(self.middleObj,self.WithContact,self.WithCorrection)
                tnObj.add(self.topObj,self.WithContact,self.WithCorrection)
                tnObj.setTransitionMode(0)  #Round edges
                f=tnObj.shape().Faces
                f.append(Part.Face(self.baseObj))
                nObj = Part.makeShell(f)
                FinalObj=None
                if self.Solid is True:
                    tnObj.makeSolid()
                    FinalObj = tnObj.shape()
                else:
                    FinalObj=nObj
            except:
                #In case OCC fails
                FinalObj=self.baseObj
                print("OCC Failed please change your values")
                
            if FinalObj is None:
                print("OCC Failed please change your values")
                obj.Shape=self.baseObj  #Avoid not showing anything      
            elif FinalObj.isValid():
                obj.Shape = FinalObj
            else:
                print("OCC Failed please change your values")
                obj.Shape=self.baseObj  #Avoid not showing anything

        except Exception as err:
            App.Console.PrintError("'execute FlowerVase' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

class Design456_FlowerVase:
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'FlowerVase.svg',
                'MenuText': "FlowerVase",
                'ToolTip': "Generate a FlowerVase"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "FlowerVase")
        Design456_BaseFlowerVase(newObj)

        ViewProviderFlowerVase(newObj.ViewObject, "FlowerVase")
        v = Gui.ActiveDocument.ActiveView
        App.ActiveDocument.recompute()
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_FlowerVase', Design456_FlowerVase())
