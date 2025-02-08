# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2025                                                     *
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
from draftutils.translate import translate  # for translate
import Design456Init
import FACE_D as faced
import DraftGeomUtils
import math
import BOPTools.SplitFeatures

__updated__ = '2023-04-08 13:11:13'


# Roof

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
        return (Design456Init.ICON_PATH + 'Roof.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# Roof
class Design456_Roof:
    """ Roof shape based on several parameters
    """

    def __init__(self, obj,
                 width=20,
                 length=20,
                 height=10,
                 thickness=1):

        obj.addProperty("App::PropertyLength", "Width", "Roof",
                        "Width of the Roof").Width = width

        obj.addProperty("App::PropertyLength", "Length", "Roof",
                        "Length of the Roof").Length = length

        obj.addProperty("App::PropertyLength", "Height", "Roof",
                        "Height of the Roof").Height = height

        obj.addProperty("App::PropertyLength", "Thickness", "Roof",
                        "Thickness of the Roof").Thickness = thickness
        obj.Proxy = self

    def execute(self, obj):
        self.Width = float(obj.Width)
        self.Height = float(obj.Height)
        self.Length = float(obj.Length)
        self.Thickness = float(obj.Thickness)
        vert1 = [App.Vector(0, 0, 0), App.Vector(self.Width, 0, 0),
                 App.Vector(self.Width/2, 0.0, self.Height),
                 App.Vector(0, 0, 0)]
        newWidth = self.Width-2*self.Thickness
        newLength = self.Length-2*self.Thickness
        newHeight = self.Height-self.Thickness
        vert2 = [App.Vector(self.Thickness, self.Thickness, 0), App.Vector(self.Thickness+newWidth, self.Thickness, 0),
                 App.Vector(self.Width/2, self.Thickness, newHeight),
                 App.Vector(self.Thickness, self.Thickness, 0)]
        FaceTriangle1 = Part.Face(Part.makePolygon(vert1))
        obj1 = FaceTriangle1.extrude(App.Vector(0.0, self.Length, 0.0))

        FaceTriangle2 = Part.Face(Part.makePolygon(vert2))
        obj2 = FaceTriangle2.extrude(App.Vector(
            0.0, self.Length-2*self.Thickness, 0.0))
        Result = obj1.cut(obj2)
        obj.Shape = Result


class Design456_Seg_Roof:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Roof.svg',
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


# ***************************


# Housing

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
        return (Design456Init.ICON_PATH + 'Housing.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# Housing
class Design456_HousingBase:
    """ Housing shape based on several parameters
    """

    def __init__(self, obj,
                 width=20,
                 length=20,
                 height=10,
                 thickness=1):

        obj.addProperty("App::PropertyLength", "Width", "Housing",
                        "Width of the Housing").Width = width

        obj.addProperty("App::PropertyLength", "Length", "Housing",
                        "Length of the Housing").Length = length

        obj.addProperty("App::PropertyLength", "Height", "Housing",
                        "Height of the Housing").Height = height

        obj.addProperty("App::PropertyLength", "Thickness", "Housing",
                        "Thickness of the Housing").Thickness = thickness
        obj.Proxy = self

    def execute(self, obj):
        self.Width = float(obj.Width)
        self.Height = float(obj.Height)
        self.Length = float(obj.Length)
        self.Thickness = float(obj.Thickness)
        Result = None
        V1_FSQ = [App.Vector(0, 0, 0),
                  App.Vector(self.Width, 0, 0),
                  App.Vector(self.Width, self.Length, 0),
                  App.Vector(0.0, self.Length, 0),
                  App.Vector(0, 0, 0)]

        V2_FSQ = [App.Vector(self.Thickness, self.Thickness, 0),
                  App.Vector(self.Width-self.Thickness, self.Thickness, 0),
                  App.Vector(self.Width-self.Thickness,
                             self.Length-self.Thickness, 0),
                  App.Vector(self.Thickness, self.Length-self.Thickness, 0),
                  App.Vector(self.Thickness, self.Thickness, 0)]
        # one used with secondFace to cut
        firstFace1 = Part.Face(Part.makePolygon(V1_FSQ))
        # Other used to make the bottom
        firstFace2 = Part.Face(Part.makePolygon(V1_FSQ))
        secondFace = Part.Face(Part.makePolygon(V2_FSQ))
        resultButtom = firstFace1.cut(secondFace)
        extrude1 = resultButtom.extrude(App.Vector(0, 0, self.Height))
        extrude2 = firstFace2.extrude(App.Vector(0, 0, self.Thickness))
        fused = extrude1.fuse(extrude2)
        Result = fused.removeSplitter()
        obj.Shape = Result


class Design456_Housing:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Housing.svg',
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


# RoundedHousing

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
        return (Design456Init.ICON_PATH + 'RoundedHousing.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

################################


# RoundedHousing
class Design456_RoundedHousingBase:
    """ RoundedHousing shape based on several parameters
    """

    def __init__(self, obj,
                 width=20,
                 length=20,
                 height=10,
                 radius=1,
                 thickness=1, chamfer=False):

        obj.addProperty("App::PropertyLength", "Width", "RoundedHousing",
                        "Width of the RoundedHousing").Width = width

        obj.addProperty("App::PropertyLength", "Length", "RoundedHousing",
                        "Length of the RoundedHousing").Length = length

        obj.addProperty("App::PropertyLength", "Height", "RoundedHousing",
                        "Height of the RoundedHousing").Height = height

        obj.addProperty("App::PropertyLength", "Radius", "RoundedHousing",
                        "Radius of the RoundedHousing").Radius = radius

        obj.addProperty("App::PropertyLength", "Thickness", "RoundedHousing",
                        "Thickness of the RoundedHousing").Thickness = thickness

        obj.addProperty("App::PropertyBool", "Chamfer", "RoundedHousing",
                        "Chamfer corner").Chamfer = chamfer
        obj.Proxy = self

    def execute(self, obj):
        self.Width = float(obj.Width)
        self.Height = float(obj.Height)
        self.Length = float(obj.Length)
        self.Radius = float(obj.Radius)
        self.Thickness = float(obj.Thickness)
        self.Chamfer = obj.Chamfer
        Result = None
        # base rectangle vertices and walls after a cut
        V1_FSQ = [App.Vector(0, 0, 0),
                  App.Vector(self.Width, 0, 0),
                  App.Vector(self.Width, self.Length, 0),
                  App.Vector(0.0, self.Length, 0),
                  App.Vector(0, 0, 0)]

        # cut middle part to make walls
        V2_FSQ = [App.Vector(self.Thickness, self.Thickness, 0),
                  App.Vector(self.Width-self.Thickness, self.Thickness, 0),
                  App.Vector(self.Width-self.Thickness,
                             self.Length-self.Thickness, 0),
                  App.Vector(self.Thickness, self.Length-self.Thickness, 0),
                  App.Vector(self.Thickness, self.Thickness, 0)]

        W1 = Part.makePolygon(V1_FSQ)
        W11 = DraftGeomUtils.filletWire(W1, self.Radius, chamfer=self.Chamfer)

        firstFace1 = Part.Face(W11)  # one used with secondFace to cut
        firstFace2 = firstFace1.copy()  # Other used to make the bottom

        W2 = Part.makePolygon(V2_FSQ)
        W22 = DraftGeomUtils.filletWire(W2, self.Radius, chamfer=self.Chamfer)

        secondFace = Part.Face(W22)

        resultButtom = firstFace1.cut(secondFace)
        extrude1 = resultButtom.extrude(App.Vector(0, 0, self.Height))
        extrude2 = firstFace2.extrude(App.Vector(0, 0, self.Thickness))
        fused = extrude1.fuse(extrude2)
        Result = fused.removeSplitter()
        obj.Shape = Result


class Design456_RoundedHousing:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'RoundedHousing.svg',
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


# 33


# EllipseBox

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
        return (Design456Init.ICON_PATH + 'EllipseBoxBase.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

# EllipseBoxBase


class Design456_EllipseBoxBase:
    """ EllipseHousingshape based on several parameters
    """

    def __init__(self, obj,
                 height=10,
                 major_radius=10,
                 minor_radius=8,
                 thickness=1):

        obj.addProperty("App::PropertyLength", "Height", "EllipseBox",
                        "Height of the EllipseBox").Height = height

        obj.addProperty("App::PropertyLength", "MajorRadius", "EllipseBox",
                        "Major Radius of the EllipseBox").MajorRadius = major_radius

        obj.addProperty("App::PropertyLength", "MinorRadius", "EllipseBox",
                        "Minor Radius of the EllipseBox").MinorRadius = minor_radius

        obj.addProperty("App::PropertyLength", "Thickness", "EllipseBox",
                        "Thickness of the EllipseBox").Thickness = thickness

        obj.Proxy = self

    def execute(self, obj):
        self.Height = float(obj.Height)
        self.MajorRadius = float(obj.MajorRadius)
        self.MinorRadius = float(obj.MinorRadius)
        self.Thickness = float(obj.Thickness)
        Result = None
        # base Ellipse vertices and walls after a cut

        if (self.MajorRadius < self.MinorRadius):
            self.MajorRadius = self.MinorRadius
            print("Major Radius must be grater or equal to Minor Radius")
        Center = App.Vector(App.Vector(0, 0, 0))
        W1 = Part.Ellipse(Center, self.MajorRadius, self.MinorRadius)
        # one used with secondFace to cut
        firstFace1 = Part.Face(Part.Wire(W1.toShape()))
        firstFace2 = firstFace1.copy()  # Other used to make the bottom

        W2 = Part.Ellipse(Center, self.MajorRadius -
                          self.Thickness, self.MinorRadius-self.Thickness)
        secondFace = Part.Face(Part.Wire(W2.toShape()))
        resultButtom = firstFace1.cut(secondFace)
        extrude1 = resultButtom.extrude(App.Vector(0, 0, self.Height))
        extrude2 = firstFace2.extrude(App.Vector(0, 0, self.Thickness))
        fused = extrude1.fuse(extrude2)
        Result = fused.removeSplitter()
        obj.Shape = Result


class Design456_EllipseBox:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'EllipseBox.svg',
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

# NonuniformedBox

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
        return (Design456Init.ICON_PATH + 'NonuniformedBox.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

# NonuniformedBox


class Design456_NonuniformedBoxBase:
    """ NonuniformedBoxshape based on several parameters
    """

    def __init__(self, obj,
                 height=10,
                 radius=1,
                 thickness=1,
                 base_radius=1,
                 vertices=[], chamfer=False):

        obj.addProperty("App::PropertyLength", "Height", "NonuniformedBox",
                        "Height of the NonuniformedBox").Height = height
        
        obj.addProperty("App::PropertyLength", "Thickness", "NonuniformedBox",
                        "Thickness of the NonuniformedBox").Thickness = thickness

        obj.addProperty("App::PropertyBool", "Chamfer", "RoundedHousing",
                        "Chamfer corner").Chamfer = chamfer

        obj.addProperty("App::PropertyLength", "Radius", "RoundedHousing",
                        "Radius of the NonuniformedBox").Radius = radius

        obj.addProperty("App::PropertyLength", "SideOneRadius", "RoundedHousing",
                        "Side Radius of the NonuniformedBox").SideOneRadius = base_radius

        obj.Proxy = self
        s = Gui.Selection.getSelectionEx()
        self.Vertices = []
        if len(s) > 2:
            self.Vertices.clear()
            for subObj in s:
                self.Vertices.append(subObj.Object.Shape.Vertexes[0].Point)
            self.Vertices.append(s[0].Object.Shape.Vertexes[0].Point)

    def execute(self, obj):
        self.Height = float(obj.Height)
        self.Radius = float(obj.Radius)
        self.SideOneRadius = float(obj.SideOneRadius)
        self.Thickness = float(obj.Thickness)
        self.Chamfer = obj.Chamfer

        Result = None
        # base None-uniformed vertices and walls after a cut

        V1_FSQ = []
        V1_FSQ = self.Vertices
        W1 = Part.makePolygon(V1_FSQ)

        if self.Radius > 0:
            W11 = DraftGeomUtils.filletWire(
                W1, self.Radius, chamfer=self.Chamfer)
        else:
            W11 = W1

        firstFace1 = Part.Face(W11)  # One used with secondFace to cut

        if self.SideOneRadius > 0:
            W12 = DraftGeomUtils.filletWire(
                W1, self.SideOneRadius, chamfer=self.Chamfer)
        else:
            W12 = W1  # Other used to make the bottom

        firstFace2 = Part.Face(W12)
        secondFace = firstFace2.makeOffset2D(-self.Thickness)
        resultButtom = firstFace1.cut(secondFace)
        extrude1 = resultButtom.extrude(App.Vector(0, 0, self.Height))
        extrude2 = firstFace2.extrude(App.Vector(0, 0, self.Thickness))
        fused = extrude1.fuse(extrude2)
        Result = fused.removeSplitter()
        obj.Shape = Result


class Design456_NonuniformedBox:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'NonuniformedBox.svg',
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

# Paraboloid

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
        return (Design456Init.ICON_PATH + 'Paraboloid.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

###########################################################################
# Paraboloid


class Design456_ParaboloidBase:
    """ Paraboloidshape based on several parameters
    """

    def __init__(self, obj,
                 height=10,
                 base_radius=10,
                 middle_radius=8,
                 ):

        obj.addProperty("App::PropertyLength", "Height", "Paraboloid",
                        "Height of the Paraboloid").Height = height

        obj.addProperty("App::PropertyLength", "BaseRadius", "Paraboloid",
                        "Base Radius of the Paraboloid").BaseRadius = base_radius

        obj.addProperty("App::PropertyLength", "MiddleRadius", "Paraboloid",
                        "Middle Radius of the Paraboloid").MiddleRadius = middle_radius

        self.points = []
        obj.Proxy = self

    def execute(self, obj):
        self.Height = float(obj.Height)
        self.BaseRadius = float(obj.BaseRadius)
        self.MiddleRadius = float(obj.MiddleRadius)
        point1 = App.Vector(self.BaseRadius, 0, 0)
        point2 = App.Vector(self.MiddleRadius, 0, self.Height/2)
        point3 = App.Vector(0, 0, self.Height)
        Result = None
        bsp = Part.BSplineCurve()
        bsp.buildFromPoles([point1, point2, point3])
        shp = bsp.toShape()
        circle = Part.makeCircle(
            self.BaseRadius, App.Vector(0, 0, 0), App.Vector(0, 0, 1))
        sweep = Part.makeSweepSurface(circle, shp)
        base = Part.Face(Part.Wire(circle))
        shell1 = Part.Shell([base, sweep])

        nResult = Part.makeSolid(shell1)
        Result = nResult.removeSplitter()
        obj.Shape = Result


class Design456_Paraboloid:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Paraboloid.svg',
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

# Capsule

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
        return (Design456Init.ICON_PATH + 'Capsule.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

###########################################################################

# Capsule


class Design456_CapsuleBase:
    """ Capsule shape based on several parameters
    """

    def __init__(self, obj,
                 length=20,
                 side_R_radius=5,
                 side_L_radius=5,
                 height_radius=5,
                 ):

        obj.addProperty("App::PropertyLength", "Length", "Capsule",
                        "Length of the Capsule").Length = length

        obj.addProperty("App::PropertyFloat", "SideRightRadius", "Capsule",
                        "R-Base Radius of the Capsule").SideRightRadius = side_R_radius
        
        obj.addProperty("App::PropertyFloat", "SideLeftRadius", "Capsule",
                        "L-Base Radius of the Capsule").SideLeftRadius = side_L_radius

        obj.addProperty("App::PropertyFloat", "HeightRadius", "Capsule",
                        "Height-Radius of the Capsule").HeightRadius = height_radius
        obj.Proxy = self

    def execute(self, obj):
        self.Length = float(obj.Length)
        self.SideRightRadius = float(obj.SideRightRadius)
        self.SideLeftRadius = float(obj.SideLeftRadius)
        self.HeightRadius = float(obj.HeightRadius)
        middle = Part.makeCylinder(self.HeightRadius, self.Length,
                                   App.Vector(-self.Length/2, 0, 0), App.Vector(1, 0, 0), 360)
        left = Part.makeSphere(
            self.SideLeftRadius, App.Vector(-self.Length/2, 0, 0), App.Vector(1, 0, 0))
        right = Part.makeSphere(self.SideRightRadius, App.Vector(
            self.Length/2, 0, 0), App.Vector(1, 0, 0))
        shpt = middle.fuse([right, left])
        Result = shpt.removeSplitter()
        obj.Shape = Result


class Design456_Capsule:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'capsule.svg',
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


# Parallelepiped

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
        return (Design456Init.ICON_PATH + 'Parallelepiped.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

# TODO: FIXME:
# Parallelepiped


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

        obj.addProperty("App::PropertyLength", "Height", "Parallelepiped",
                        "Height of the Parallelepiped").Height = height

        obj.addProperty("App::PropertyLength", "Length", "Parallelepiped",
                        "Length of the Parallelepiped").Length = length

        obj.addProperty("App::PropertyLength", "Width", "Parallelepiped",
                        "Width of the Parallelepiped").Width = width

        obj.addProperty("App::PropertyAngle", "AngleX", "Parallelepiped",
                        "AngleY of the Parallelepiped").AngleX = anglex

        obj.addProperty("App::PropertyAngle", "AngleY", "Parallelepiped",
                        "AngleX of the Parallelepiped").AngleY = angley

        obj.Proxy = self

    def execute(self, obj):
        self.Height = float(obj.Height)
        self.Length = float(obj.Length)
        self.Width = float(obj.Width)
        self.AngleX = float(obj.AngleX)
        self.AngleY = float(obj.AngleY)

        p1 = App.Vector(-self.Width/2, self.Length/2, 0)    # - +
        p2 = App.Vector(self.Width/2, self.Length/2, 0)     # + +
        p3 = App.Vector(self.Width/2, -self.Length/2, 0)    # - +
        p4 = App.Vector(-self.Width/2, -self.Length/2, 0)   # - -

        shiftSizeX = self.Height * math.cos(math.radians(90-self.AngleX))
        shiftSizeY = self.Height * math.cos(math.radians(90-self.AngleY))

        p11 = App.Vector(shiftSizeX-self.Width/2,
                         shiftSizeY+self.Length/2, self.Height)
        p22 = App.Vector(shiftSizeX+self.Width/2,
                         shiftSizeY+self.Length/2, self.Height)
        p33 = App.Vector(shiftSizeX+self.Width/2,
                         shiftSizeY-self.Length/2, self.Height)
        p44 = App.Vector(shiftSizeX-self.Width/2,
                         shiftSizeY-self.Length/2, self.Height)

        bottom = Part.makePolygon([p1, p2, p3, p4, p1])
        top = Part.makePolygon([p11, p22, p33, p44, p11])
        left = Part.makePolygon([p4, p44, p11, p1, p4])
        right = Part.makePolygon([p33, p22, p2, p3, p33])
        front = Part.makePolygon([p4, p44, p33, p3, p4])
        back = Part.makePolygon([p1, p11, p22, p2, p1])

        W1 = Part.Wire(bottom)
        W2 = Part.Wire(top)
        W3 = Part.Wire(left)
        W4 = Part.Wire(right)
        W5 = Part.Wire(front)
        W6 = Part.Wire(back)
        f1 = Part.Face(W1)
        f2 = Part.Face(W2)
        f3 = Part.Face(W3)
        f4 = Part.Face(W4)
        f5 = Part.Face(W5)
        f6 = Part.Face(W6)
        shell = Part.makeShell([f1, f2, f3, f4, f5, f6])
        Result = Part.Solid(shell)
        obj.Shape = Result


class Design456_Parallelepiped:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Parallelepiped.svg',
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
# RoundRoof

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
        return (Design456Init.ICON_PATH + 'RoundRoof.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# RoundRoof
class Design456_BaseRoundRoof:
    """ RoundRoof shape based on several parameters
    """

    def __init__(self, obj,
                 width=20,
                 length=20,
                 height=10,
                 thickness=1):

        obj.addProperty("App::PropertyLength", "Width", "RoundRoof",
                        "Width of the RoundRoof").Width = width

        obj.addProperty("App::PropertyLength", "Length", "RoundRoof",
                        "Length of the RoundRoof").Length = length

        obj.addProperty("App::PropertyLength", "Height", "RoundRoof",
                        "Height of the RoundRoof").Height = height

        obj.addProperty("App::PropertyLength", "Thickness", "RoundRoof",
                        "Thickness of the RoundRoof").Thickness = thickness

        obj.Proxy = self

    def execute(self, obj):
        self.Width = float(obj.Width)
        self.Height = float(obj.Height)
        self.Length = float(obj.Length)
        self.Thickness = float(obj.Thickness)
        Result = None

        p1 = App.Vector(0, 0, 0)
        p2 = App.Vector(0, self.Length/2, self.Height)
        p3 = App.Vector(0, self.Length, 0)

        p11 = App.Vector(p1.x+self.Thickness, p1.y+self.Thickness, p1.z)
        p22 = App.Vector(p2.x+self.Thickness, p2.y, p2.z-self.Thickness)
        p33 = App.Vector(p3.x+self.Thickness, p3.y-self.Thickness, p3.z)

        c1 = Part.ArcOfCircle(p1, p2, p3)
        c11 = c1.copy()
        l1 = Part.LineSegment(p1, p3)

        c2 = Part.ArcOfCircle(p11, p22, p33)
        l2 = Part.LineSegment(p11, p33)

        W1 = Part.Wire([c1.toShape(), l1.toShape()])
        W2 = Part.Wire([c2.toShape(), l2.toShape()])
        f1 = Part.Face(W1)
        f2 = Part.Face(W2)
        obj1 = f1.extrude(App.Vector(self.Width, 0, 0))
        obj2 = f2.extrude(App.Vector(self.Width-2*self.Thickness, 0, 0))
        Result = obj1.cut(obj2)
        obj.Shape = Result


class Design456_RoundRoof:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'RoundRoof.svg',
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

# FlowerVase

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
        return (Design456Init.ICON_PATH + 'FlowerVase.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

# FlowerVase


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
        return (Design456Init.ICON_PATH + 'FlowerVase.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


# FlowerVase
class Design456_BaseFlowerVase:
    """ FlowerVase shape based on several parameters
    """
    Placement=None
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

        obj.addProperty("App::PropertyEnumeration", "baseType", "1)Sections",
                        "FlowerVase base type").baseType = ["Circle", "Polygon"]
        obj.baseType = _baseType

        obj.addProperty("App::PropertyEnumeration", "middleType", "1)Sections",
                        "FlowerVase middle type").middleType = ["Circle", "Polygon"]
        obj.middleType = _middleType

        obj.addProperty("App::PropertyEnumeration", "topType", "1)Sections",
                        "FlowerVase top type").topType = ["Circle", "Polygon"]
        obj.topType = _topType

        obj.addProperty("App::PropertyLength", "baseRadius", "2)Radius",
                        "baseRadius of the FlowerVase").baseRadius = _baseRadius

        obj.addProperty("App::PropertyLength", "middleRadius", "2)Radius",
                        "middleRadius of the FlowerVase").middleRadius = _middleRadius

        obj.addProperty("App::PropertyLength", "topRadius", "2)Radius",
                        "topRadius of the FlowerVase").topRadius = _topRadius

        obj.addProperty("App::PropertyLength", "Height", "3)Others",
                        "Height of the FlowerVase").Height = _height

        obj.addProperty("App::PropertyLength", "neckHeight", "3)Others",
                        "neckHeight of the FlowerVase").neckHeight = _neckHeight

        obj.addProperty("App::PropertyInteger", "baseSides", "3)Others",
                        "base sides of the FlowerVase").baseSides = _baseSides
        
        obj.addProperty("App::PropertyInteger", "middleSides", "3)Others",
                        "middle sides of the FlowerVase").middleSides = _middleSides
        
        obj.addProperty("App::PropertyInteger", "topSides", "3)Others",
                        "top sides of the FlowerVase").topSides = _topSides

        obj.addProperty("App::PropertyBool", "Solid", "3)Others",
                        "Solid").Solid = _solid
        
        obj.addProperty("App::PropertyBool", "WithContact", "3)Others",
                        "With Contact").WithContact = _withContact
        
        obj.addProperty("App::PropertyBool", "WithCorrection", "3)Others",
                        "With Correction").WithCorrection = _withCorrection

        Design456_BaseFlowerVase.Placement = obj.Placement
        obj.Proxy = self
        self.Type = "FlowerVase"

    def calculatePolygonVertices(self, radius, sides, Zaxis=0.0):
        try:
            vertices = []
            slice = 360/sides
            _angle = math.radians(slice)
            for i in range(0, sides+1):
                x =  Design456_BaseFlowerVase.Placement.Base.x+(radius * math.cos(_angle*i))
                y =  Design456_BaseFlowerVase.Placement.Base.y+(radius * math.sin(_angle*i))
                z = Zaxis+ Design456_BaseFlowerVase.Placement.Base.z
                point = App.Vector(x, y, z)
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

            self.baseType = str(obj.baseType)
            self.middleType = str(obj.middleType)
            self.topType = str(obj.topType)

            self.baseRadius = float(obj.baseRadius)
            self.middleRadius = float(obj.middleRadius)
            self.topRadius = float(obj.topRadius)

            self.Height = float(obj.Height)
            self.neckHeight = float(obj.neckHeight)
            self.Result = None

            self.baseObj = None
            self.middleObj = None
            self.topObj = None
            self.baseObj = None
            self.sweepPath = None
            self.Solid = obj.Solid
            self.baseSides = obj.baseSides
            self.middleSides = obj.middleSides
            self.topSides = obj.topSides
            self.WithContact = obj.WithContact
            self.WithCorrection = obj.WithCorrection

            if self.baseType == "Circle":  # (self,radius,sides,plc,Zaxis=0.0):
                self.baseObj = Part.Wire(Part.makeCircle(
                    self.baseRadius, App.Vector(0, 0, 0), App.Vector(0, 0, 1), 0, 360))
            elif self.baseType == "Polygon":
                self.baseObj = Part.makePolygon(
                    self.calculatePolygonVertices(self.baseRadius, self.baseSides))

            if self.middleType == "Circle":
                self.middleObj = Part.Wire(Part.makeCircle(self.middleRadius, App.Vector(
                    0, 0, (self.Height-self.neckHeight)/2), App.Vector(0, 0, 1), 0, 360))
            elif self.middleType == "Polygon":
                self.middleObj = Part.makePolygon(self.calculatePolygonVertices(
                    self.middleRadius, self.middleSides, (self.Height-self.neckHeight)/2))

            if self.topType == "Circle":
                self.topObj = Part.Wire(Part.makeCircle(self.topRadius, App.Vector(
                    0, 0, (self.Height-self.neckHeight)), App.Vector(0, 0, 1), 0, 360))
            elif self.middleType == "Polygon":
                self.topObj = Part.makePolygon(self.calculatePolygonVertices(
                    self.topRadius, self.topSides, (self.Height-self.neckHeight)))

            try:
                self.sweepPath = Part.makePolygon([App.Vector(0, 0, 0), App.Vector(
                    0, 0, self.Height)])  # must be the total height
                tnObj = Part.BRepOffsetAPI.MakePipeShell(self.sweepPath)
                tnObj.add(self.baseObj, self.WithContact, self.WithCorrection)
                tnObj.add(self.middleObj, self.WithContact,
                          self.WithCorrection)
                tnObj.add(self.topObj, self.WithContact, self.WithCorrection)
                tnObj.setTransitionMode(0)  # Round edges
                f = tnObj.shape().Faces
                f.append(Part.Face(self.baseObj))
                nObj = Part.makeShell(f)
                FinalObj = None
                if self.Solid is True:
                    tnObj.makeSolid()
                    FinalObj = tnObj.shape()
                else:
                    FinalObj = nObj
            except:
                # In case OCC fails
                FinalObj = self.baseObj
                print("OCC Failed please change your values")

            if FinalObj is None:
                print("OCC Failed please change your values")
                obj.Shape = self.baseObj  # Avoid not showing anything
            elif FinalObj.isValid():
                obj.Shape = FinalObj
            else:
                print("OCC Failed please change your values")
                obj.Shape = self.baseObj  # Avoid not showing anything

        except Exception as err:
            App.Console.PrintError("'execute FlowerVase' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class Design456_FlowerVase:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'FlowerVase.svg',
                'MenuText': "FlowerVase",
                'ToolTip': "Generate a FlowerVase"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "FlowerVase")
        plc = App.Placement()
        plc.Base = App.Vector(0, 0, 0)
        plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        newObj.Placement = plc
        Design456_BaseFlowerVase(newObj)

        ViewProviderFlowerVase(newObj.ViewObject, "FlowerVase")
        v = Gui.ActiveDocument.ActiveView
        App.ActiveDocument.recompute()
        faced.PartMover(v, newObj, deleteOnEscape=True)


Gui.addCommand('Design456_FlowerVase', Design456_FlowerVase())

######################


# Corrugated Steel
class ViewProviderCorrugatedSteel:

    obj_name = "CorrugatedSteel"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderCorrugatedSteel.obj_name
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
        return (Design456Init.ICON_PATH + 'CorrugatedSteel.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

# CorrugatedSteel


class Design456_BaseCorrugatedSteel:
    """ CorrugatedSteel shape based on several parameters
    """
    Placement=None
    def __init__(self, obj,
                 _height=0.5,
                 _width=10.0,
                 _length=10.0,
                 _wavePeriod=1.0,
                 _solid=True,
                 _withContact=False,
                 _withCorrection=False):

        obj.addProperty("App::PropertyLength", "Height", "Sheet",
                        "Height of the CorrugatedSteel").Height = _height
        
        obj.addProperty("App::PropertyLength", "Width", "Sheet",
                        "Width of the CorrugatedSteel").Width = _width
        
        obj.addProperty("App::PropertyLength", "Length", "Sheet",
                        "Length of the CorrugatedSteel").Length = _length

        obj.addProperty("App::PropertyLength", "wavePeriod", "Sheet",
                        "wave Amplitude of the CorrugatedSteel").wavePeriod = _wavePeriod

        obj.addProperty("App::PropertyBool", "Solid", "Sheet",
                        "Solid").Solid = _solid
        
        obj.addProperty("App::PropertyBool", "WithContact", "Sheet",
                        "CorrugatedSteel Width contact").WithContact = _withContact
        
        obj.addProperty("App::PropertyBool", "WithCorrection", "Sheet",
                        "CorrugatedSteel With Correction").WithCorrection = _withCorrection

        Design456_BaseCorrugatedSteel.Placement = obj.Placement
        obj.Proxy = self
        self.Type = "CorrugatedSteel"

    def calculateWavedEdge(self):
        vertices = []
        angelParts = math.radians(360/6)
        count1 = 0.0
        count2 = 0
        seg1 = (self.wavePeriod/6)  # basic single segments per each angle
        x = 0.0
        y = 0.0
        z = 0.0
        while (count1 < self.Length):
            for count2 in range(0, 6):
                z = self.Height*(self.wavePeriod/3*math.sin(count2*angelParts))
                vertices.append(App.Vector(x+Design456_BaseCorrugatedSteel.Placement.Base.x,
                                           y+Design456_BaseCorrugatedSteel.Placement.Base.y,
                                           z+Design456_BaseCorrugatedSteel.Placement.Base.z))
                x = x+seg1
            count1 = count1+self.wavePeriod
        return (vertices)

    def execute(self, obj):
        try:

            self.Height = float(obj.Height)
            self.Length = float(obj.Length)
            self.Width = float(obj.Width)
            self.wavePeriod = float(obj.wavePeriod)

            self.baseObj = None
            self.sweepPath = None
            self.Solid = obj.Solid
            self.WithContact = obj.WithContact
            self.WithCorrection = obj.WithCorrection
            vert = self.calculateWavedEdge()
            bs = Part.BSplineCurve()
            bs.interpolate(vert)
            bObj = bs.toShape()
            self.sweepPath = Part.makePolygon([App.Vector(
                self.Length/2, 0, self.wavePeriod/3), App.Vector(self.Length/2, self.Width, self.wavePeriod/3)])
            tnObj = Part.BRepOffsetAPI.MakePipeShell(self.sweepPath)
            tnObj.add(Part.Wire(bObj), self.WithContact, self.WithCorrection)
            tnObj.setTransitionMode(0)  # Round edges
            #nObj = Part.makeShell()
            obj.Shape = tnObj.shape()

        except Exception as err:
            App.Console.PrintError("'execute CorrugatedSteel' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class Design456_CorrugatedSteel:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'CorrugatedSteel.svg',
                'MenuText': "CorrugatedSteel",
                'ToolTip': "Generate a CorrugatedSteel"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "CorrugatedSteel")
        plc = App.Placement()
        plc.Base = App.Vector(0, 0, 0)
        plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        newObj.Placement = plc
        Design456_BaseCorrugatedSteel(newObj)

        ViewProviderCorrugatedSteel(newObj.ViewObject, "CorrugatedSteel")
        v = Gui.ActiveDocument.ActiveView
        App.ActiveDocument.recompute()
        faced.PartMover(v, newObj, deleteOnEscape=True)


Gui.addCommand('Design456_CorrugatedSteel', Design456_CorrugatedSteel())

############################


class ViewProviderAcousticFoam:

    obj_name = "AcousticFoam"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderAcousticFoam.obj_name
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
        return (Design456Init.ICON_PATH + 'AcousticFoam.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

# AcousticFoam


class Design456_BaseAcousticFoam:
    """ AcousticFoam shape based on several parameters
    """

    def __init__(self, obj,
                 _height=1.0,
                 _width=10.0,
                 _length=10.0,
                 _wavePeriod=1,
                 _solid=True,
                 _waveType="Sine",
                 _distanceBetweenWaves=1,
                 _waveAmplitude=0.3,
                 _cutOffset=2):

        obj.addProperty("App::PropertyLength", "Height", "Foam",
                        "Height of the AcousticFoam").Height = _height
        
        obj.addProperty("App::PropertyLength", "Width", "Foam",
                        "Width of the AcousticFoam").Width = _width
        
        obj.addProperty("App::PropertyLength", "Length", "Foam",
                        "Length of the AcousticFoam").Length = _length

        obj.addProperty("App::PropertyLength", "distanceBetweenWaves", "Foam",
                        "distance between waves of the AcousticFoam").distanceBetweenWaves = _distanceBetweenWaves

        obj.addProperty("App::PropertyLength", "waveAmplitude", "Foam",
                        "wave Amplitude of the AcousticFoam").waveAmplitude = _waveAmplitude

        obj.addProperty("App::PropertyLength", "wavePeriod", "Foam",
                        "wave period of the AcousticFoam").wavePeriod = _wavePeriod

        obj.addProperty("App::PropertyInteger", "cutOffset", "Foam",
                        "cut Offset of the AcousticFoam").cutOffset = _cutOffset

        obj.addProperty("App::PropertyEnumeration", "waveType", "Foam",
                        "AcousticFoam wave type").waveType = ["Sine", "Cos", "Tan"]

        obj.addProperty("App::PropertyBool", "Solid", "Foam",
                        "AcousticFoam top type").Solid = _solid
        obj.waveType = _waveType
        obj.Proxy = self
        if obj.Solid is True:
            self.cutOffset = _cutOffset
        else:
            self.cutOffset = 0
        self.Type = "AcousticFoam"

    def calculateWavedEdge(self, vector, angle=0):
        vertices = []
        angelParts = math.radians(360/6)
        count1 = 0.0
        count2 = 0
        seg1 = (self.wavePeriod/6)  # basic single segments per each angle
        x = 0.0
        y = 0.0
        z = 0.0
        while (count1 < (self.Length+self.cutOffset)):
            for count2 in range(0, 6):
                if self.waveType == "Sine":
                    z = self.waveAmplitude * \
                        (self.wavePeriod/3 *
                         math.sin(math.radians(angle)+count2*angelParts))
                elif self.waveType == "Cos":
                    z = self.waveAmplitude * \
                        (self.wavePeriod/3 *
                         math.cos(math.radians(angle)+count2*angelParts))
                elif self.waveType == "Tan":
                    z = self.waveAmplitude*self.Height * \
                        (self.wavePeriod/3 *
                         math.tan(math.radians(angle)+count2*angelParts))

                vertices.append(App.Vector(x+vector.x,
                                           y+vector.y,
                                           z+vector.z))
                x = x+seg1
            count1 = count1+self.wavePeriod
        return (vertices)

    def execute(self, obj):
        try:
            self.Height = float(obj.Height)  # Extrusion Axis (Z)
            self.Length = float(obj.Length)  # X AXIS
            self.Width = float(obj.Width)  # Y AXIS
            # Wave amplitude (Z) for one surface
            self.waveAmplitude = float(obj.waveAmplitude)
            self.wavePeriod = float(obj.wavePeriod)
            self.waveType = str(obj.waveType)
            self.distanceBetweenWaves = float(obj.distanceBetweenWaves)
            self.baseObj = None
            self.sweepPath = None
            self.Solid = obj.Solid
            waves = []
            nrOfWaves = int((self.Width+self.cutOffset) /
                            self.distanceBetweenWaves)
            v = App.Vector(0, 0, 0)
            originalY = v.y
            for i in range(0, nrOfWaves):
                v.y = originalY+self.distanceBetweenWaves*i
                if int(i/2) == (i/2):
                    vert = self.calculateWavedEdge(v, 0)
                    v.y = originalY+self.distanceBetweenWaves*i
                else:
                    vert = self.calculateWavedEdge(v, -180)
                    v.y = originalY+self.distanceBetweenWaves*i
                newY = originalY+self.distanceBetweenWaves/2+self.distanceBetweenWaves*i
                p1 = App.Vector(vert[0].x, newY, 0)
                p2 = App.Vector(vert[0].x+self.Length+self.cutOffset, newY, 0)
                objLINE = Part.Wire(Part.makePolygon([p1, p2]))
                bs = Part.BSplineCurve()
                bs.interpolate(vert)
                bObj = bs.toShape()
                waves.append(Part.Wire(bObj))
                waves.append(objLINE)
            tnObj = Part.makeLoft(waves, False, False)

            if self.Solid is True:
                tnObj = tnObj.extrude(App.Vector(0, 0, self.Height))
                # remove PI size from the box
                box = Part.makeBox(self.Length, self.Width, self.Height*4)
                box.Placement.Base.z = -self.Height
                tnObj = tnObj.common(box)
            obj.Shape = tnObj

        except Exception as err:
            App.Console.PrintError("'execute AcousticFoam' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class Design456_AcousticFoam:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'AcousticFoam.svg',
                'MenuText': "AcousticFoam",
                'ToolTip': "Generate a AcousticFoam"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "AcousticFoam")
        plc = App.Placement()
        plc.Base = App.Vector(0, 0, 0)
        plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        newObj.Placement = plc
        Design456_BaseAcousticFoam(newObj)

        ViewProviderAcousticFoam(newObj.ViewObject, "AcousticFoam")
        v = Gui.ActiveDocument.ActiveView
        App.ActiveDocument.recompute()
        faced.PartMover(v, newObj, deleteOnEscape=True)


Gui.addCommand('Design456_AcousticFoam', Design456_AcousticFoam())


######################################################################


class ViewProviderGrass:

    obj_name = "Grass"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderGrass.obj_name
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
        return (Design456Init.ICON_PATH + 'Grass.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

# Grass


class Design456_BaseGrass:
    """ Grass shape based on several parameters
    """

    def __init__(self, obj,
                 _height=1.0,
                 _width=10.0,
                 _length=10.0,
                 _wavePeriod=1,
                 _solid=True,
                 _waveType="Sine",
                 _distanceBetweenWaves=1,
                 _waveAmplitude=0.3,
                 _waveMaxAngel=75.0,
                 _cutOffset=2):

        obj.addProperty("App::PropertyLength", "Height", "Grass",
                        "Height of the Grass").Height = _height
        
        obj.addProperty("App::PropertyLength", "Width", "Grass",
                        "Width of the Grass").Width = _width
        
        obj.addProperty("App::PropertyLength", "Length", "Grass",
                        "Length of the Grass").Length = _length

        obj.addProperty("App::PropertyLength", "waveMaxAngle", "Grass",
                        "wave Max angle of the Grass").waveMaxAngle = _waveMaxAngel

        obj.addProperty("App::PropertyLength", "distanceBetweenWaves", "Grass",
                        "distance between waves of the Grass").distanceBetweenWaves = _distanceBetweenWaves

        obj.addProperty("App::PropertyInteger", "cutOffset", "Grass",
                        "cut Offset of the Grass").cutOffset = _cutOffset

        obj.addProperty("App::PropertyLength", "waveAmplitude", "Grass",
                        "wave Amplitude of the Grass").waveAmplitude = _waveAmplitude

        obj.addProperty("App::PropertyLength", "wavePeriod", "Grass",
                        "wave period of the Grass").wavePeriod = _wavePeriod

        obj.addProperty("App::PropertyEnumeration", "waveType", "Grass",
                        "Grass wave type").waveType = ["Sine", "Cos", "Tan"]

        obj.addProperty("App::PropertyBool", "Solid", "Grass",
                        "Grass type").Solid = _solid
        obj.waveType = _waveType
        obj.Proxy = self
        if obj.Solid is True:
            self.cutOffset = _cutOffset
        else:
            self.cutOffset = 0
        self.Type = "Grass"

    def calculateWavedEdge(self, vector, angle=0):
        vertices = []
        angelParts = math.radians(self.waveMaxAngle/6)
        count1 = 0.0
        count2 = 0
        seg1 = (self.wavePeriod/6)  # basic single segments per each angle
        x = 0.0
        y = 0.0
        z = 0.0
        while (count1 < (self.Length+self.cutOffset)):
            for count2 in range(0, 6):
                if self.waveType == "Sine":
                    z = self.waveAmplitude * \
                        (self.wavePeriod/3 *
                         math.sin(math.radians(angle)+count2*angelParts))
                elif self.waveType == "Cos":
                    z = self.waveAmplitude * \
                        (self.wavePeriod/3 *
                         math.cos(math.radians(angle)+count2*angelParts))
                elif self.waveType == "Tan":
                    z = self.waveAmplitude * \
                        (self.wavePeriod/3 *
                         math.tan(math.radians(angle)+count2*angelParts))
                vertices.append(App.Vector(x+vector.x,
                                           y+vector.y,
                                           z+vector.z))
                x = x+seg1
            count1 = count1+self.wavePeriod
        return (vertices)

    def execute(self, obj):
        try:
            self.Height = float(obj.Height)  # Extrusion Axis (Z)
            self.Length = float(obj.Length)  # X AXIS
            self.Width = float(obj.Width)  # Y AXIS
            # Wave amplitude (Z) for one surface
            self.waveAmplitude = float(obj.waveAmplitude)
            self.wavePeriod = float(obj.wavePeriod)
            self.waveType = str(obj.waveType)
            self.distanceBetweenWaves = float(obj.distanceBetweenWaves)
            self.baseObj = None
            self.sweepPath = None
            self.Solid = obj.Solid
            self.waveMaxAngle = float(obj.waveMaxAngle)
            waves = []
            nrOfWaves = int((self.Width+self.cutOffset) /
                            self.distanceBetweenWaves)
            v = App.Vector(0, 0, 0)
            originalY = v.y
            for i in range(0, nrOfWaves):
                v.y = originalY+self.distanceBetweenWaves*i
                if int(i/2) == (i/2):
                    vert = self.calculateWavedEdge(v, 0)
                    v.y = originalY+self.distanceBetweenWaves*i
                else:
                    vert = self.calculateWavedEdge(v, -180)
                    v.y = originalY+self.distanceBetweenWaves*i
                newY = originalY+self.distanceBetweenWaves/2+self.distanceBetweenWaves*i
                p1 = App.Vector(vert[0].x, newY, 0)
                p2 = App.Vector(vert[0].x+self.Length+self.cutOffset, newY, 0)
                bs = Part.BSplineCurve()
                bs.interpolate(vert)
                bObj = bs.toShape()
                waves.append(Part.Wire(bObj))
            tnObj = Part.makeLoft(waves, False, False)

            if self.Solid is True:
                tnObj = tnObj.extrude(App.Vector(0, 0, self.Height))
                # remove PI size from the box
                box = Part.makeBox(self.Length, self.Width, self.Height*4)
                box.Placement.Base.z = -self.Height
                tnObj = tnObj.common(box)
            obj.Shape = tnObj

        except Exception as err:
            App.Console.PrintError("'execute Grass' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class Design456_Grass:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Grass.svg',
                'MenuText': "Grass",
                'ToolTip': "Generate a Grass"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Grass")
        plc = App.Placement()
        plc.Base = App.Vector(0, 0, 0)
        plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        newObj.Placement = plc
        Design456_BaseGrass(newObj)

        ViewProviderGrass(newObj.ViewObject, "Grass")
        v = Gui.ActiveDocument.ActiveView
        App.ActiveDocument.recompute()
        faced.PartMover(v, newObj, deleteOnEscape=True)


Gui.addCommand('Design456_Grass', Design456_Grass())


######################################################################

# Honeycomb Cylinder

# Honeycomb Cylinder

class ViewProviderHoneycombCylinder:

    obj_name = "HoneycombCylinder"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderHoneycombCylinder.obj_name
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
        return (Design456Init.ICON_PATH + 'HoneycombCylinder.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


class BaseHoneycombCylinder:
    """ HoneycombCylinder shape based on several parameters
    """
    Placement=None
    def __init__(self, obj,
                 _height=20.0,  # Shape hight
                 _Radius=10.0,
                 _holeType="Hexagon 06Sides",  # Hole type : Triangle, Square, Oval, Pentagon, Heptagon, Octagon, Hexagon ..etc
                 ):

        obj.addProperty("App::PropertyLength", "Height", "HoneycombCylinder",
                        "Height of the HoneycombCylinder").Height = _height

        obj.addProperty("App::PropertyLength", "Radius", "HoneycombCylinder",
                        "Radius of the HoneycombCylinder").Radius = _Radius

        obj.addProperty("App::PropertyEnumeration", "HoleType", "HoneycombCylinder",
                        "Hole type").HoleType = ["Circle",
                                                 "Triangle 03Sides",
                                                 "Square 04Sides",
                                                 "Pentagon 05Sides",
                                                 "Hexagon 06Sides",
                                                 "Heptagon 07Sides",
                                                 "Octagon 08Sides",
                                                 "Nonagon 09Sides",
                                                 "Decagon 10Sides"]

        self.Type = "HoneycombCylinder"
        BaseHoneycombCylinder.Placement = obj.Placement
        obj.Proxy = self
        obj.HoleType =_holeType

    def createPolygonOne3D(self, sides=3):
        try:
            points = []
            flatObj = None
            newObj = None
            angles = 360/sides
            # Extra 5 points to make the object longer for cutting
            y1 = BaseHoneycombCylinder.Placement.Base.y - (2*self.Radius+5)
            y2 = -y1+ (2*self.Radius+5)
            
            for i in range(0, sides):
                # The polygon will be
                x = BaseHoneycombCylinder.Placement.Base.x+self.HoleRadius * math.cos(math.radians(i*angles))
                z = BaseHoneycombCylinder.Placement.Base.z+self.HoleRadius * math.sin(math.radians(i*angles))
                points.append(App.Vector(x, y1, z))
            
            points.append(points[0])  # close the loop
            flatObj = Part.Face(Part.makePolygon(points))
            newObj = flatObj.extrude(App.Vector(0, y2, 0))
            return newObj

        except Exception as err:
            App.Console.PrintError("'createObject HoneycombCylinder' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def createOneRing(self, _sides):
        try:
            angles = 180/self.Holes
            plc = BaseHoneycombCylinder.Placement.copy()
            ringHoles = []
            plc.Rotation.Axis = App.Vector(0.0, 0.0, 1.0)
            plc.Base = BaseHoneycombCylinder.Placement.Base
            plc.Base.z = plc.Base.z
            for i in range(0, self.Holes):
                if self.HoleType=="Circle":
                    ringHoles.append(self.createOneCylinder())
                else:
                    ringHoles.append(self.createPolygonOne3D(_sides))
                plc.Rotation.Angle = math.radians(angles*i)
                ringHoles[i].Placement = plc
            return (Part.makeCompound(ringHoles))

        except Exception as err:
            App.Console.PrintError("'createObject HoneycombCylinder' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    
    def createOneCylinder(self):        
        try:
            flatObj = None
            newObj = None
            x = BaseHoneycombCylinder.Placement.Base.x
            z = BaseHoneycombCylinder.Placement.Base.z
            y1 = BaseHoneycombCylinder.Placement.Base.y - (2*self.Radius+5)
            y2 = -y1+ (2*self.Radius+5)
            circle=Part.Wire(Part.makeCircle(self.HoleRadius,App.Vector(x,y1,z),App.Vector(0,1,0)))
            flatObj = Part.Face(circle)
            newObj = flatObj.extrude(App.Vector(0, y2, 0))
            return newObj

        except Exception as err:
            App.Console.PrintError("'createObject HoneycombCylinder' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def createObject(self):
        finalObj = None
        baseObj = None
        coreObj = None
        try:
            # From this tool, I will create shapes having  origin center in the centerofmass TODO: Good or bad? let me know!
            baseObj = Part.makeCylinder(self.Radius, self.Height,
                                        App.Vector(BaseHoneycombCylinder.Placement.Base.x,
                                                   BaseHoneycombCylinder.Placement.Base.y,
                                                   BaseHoneycombCylinder.Placement.Base.z-self.Height/2))
            # We should have a higher shape to cut the top also
            coreObj = Part.makeCylinder(self.innerRadius, self.Height,
                                        App.Vector(BaseHoneycombCylinder.Placement.Base.x,
                                                   BaseHoneycombCylinder.Placement.Base.y,
                                                   BaseHoneycombCylinder.Placement.Base.z-self.Height/2))
            finalObj = baseObj.cut(coreObj)

            z = -self.Height/2
            allRings = []
            cutRot = 20
            _sides = 1
            nrOfRings = int(self.Height/self.HoleRadius/2)
            compoundOBJ=None
            if self.HoleType == "":
                # No holes
                pass  # do nothing

            elif self.HoleType == "Circle":
                pass
            elif (self.HoleType == "Triangle 03Sides" or 
                  self.HoleType == "Square 04Sides" or
                  self.HoleType == "Pentagon 05Sides" or
                  self.HoleType == "Hexagon 06Sides" or
                  self.HoleType == "Heptagon 07Sides" or
                  self.HoleType == "Octagon 08Sides" or
                  self.HoleType == "Nonagon 09Sides" or
                  self.HoleType == "Decagon 10Sides"):
                pos=self.HoleType.find(" ")+1
                _sides=int(self.HoleType[pos:pos+2])
                if _sides==0 and self.HoleType != "Circle":
                    _sides=3 #avoid divide by zero
                    print("warning the side was zero")

            for i in range(0, nrOfRings+1):
                z = -self.Height/2.4+self.Distance*i
                allRings.append(self.createOneRing(_sides))
                allRings[i].Placement.Base.z = z
                if cutRot == 0:
                    cutRot = 20
                else:
                    cutRot = 0
                allRings[i].Placement.Rotation.Angle = math.degrees(cutRot)
                allRings[i].Placement.Rotation.Axis = App.Vector(0, 0, 1)
                compoundOBJ = Part.Compound(allRings)

            compoundOBJ = Part.Compound(allRings)
            ResultObj = finalObj.cut(compoundOBJ)
            return ResultObj

        except Exception as err:
            App.Console.PrintError("'createObject HoneycombCylinder' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def execute(self, obj):
        try:
            self.Height = float(obj.Height)
            self.Radius = float(obj.Radius)
            self.innerRadius = self.Radius-1
            self.Holes = int(6)
            self.HoleType = obj.HoleType
            self.HoleRadius = self.Radius* 0.218 #2.35
            self.Distance = float(self.HoleRadius*2)
            obj.Shape = Part.makeCompound(self.createObject())

        except Exception as err:
            App.Console.PrintError("'execute HoneycombCylinder' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class Design456_HoneycombCylinder:

    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'HoneycombCylinder.svg',
                'MenuText': "HoneycombCylinder",
                'ToolTip': "Generate a HoneycombCylinder"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "HoneycombCylinder")
        plc = App.Placement()
        plc.Base = App.Vector(0, 0, 0)
        plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        newObj.Placement = plc

        BaseHoneycombCylinder(newObj)
        ViewProviderHoneycombCylinder(newObj.ViewObject, "HoneycombCylinder")
        v = Gui.ActiveDocument.ActiveView
        App.ActiveDocument.recompute()
        faced.PartMover(v, newObj, deleteOnEscape=True)


Gui.addCommand('Design456_HoneycombCylinder', Design456_HoneycombCylinder())
#-----------------------------------------------------------------------------


# Honeycomb Fence

class ViewProviderHoneycombFence:

    obj_name = "HoneycombFence"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderHoneycombFence.obj_name
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
        return (Design456Init.ICON_PATH + 'HoneycombFence.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None



class BaseHoneycombFence:
    """ HoneycombFence shape based on several parameters
    """
    Placement=None
    def __init__(self, obj,
                 _height=30.0,  # Shape hight
                 _width=30.0,
                 _thickness=2,
                 _holeType="Hexagon 06Sides",  # Hole type : Triangle, Square, Oval, Pentagon, Heptagon, Octagon, Hexagon ..etc
                 ):

        obj.addProperty("App::PropertyLength", "Height", "HoneycombFence",
                        "Height of the HoneycombFence").Height = _height

        obj.addProperty("App::PropertyLength", "Thickness", "HoneycombFence",
                        "Thickness of the HoneycombFence").Thickness = _thickness
        
        obj.addProperty("App::PropertyLength", "Width", "HoneycombFence",
                        "Width of the HoneycombFence").Width = _width

        obj.addProperty("App::PropertyEnumeration", "HoleType", "HoneycombFence",
                        "Hole type").HoleType = ["Circle",
                                                 "Triangle 03Sides",
                                                 "Square 04Sides",
                                                 "Pentagon 05Sides",
                                                 "Hexagon 06Sides",
                                                 "Heptagon 07Sides",
                                                 "Octagon 08Sides",
                                                 "Nonagon 09Sides",
                                                 "Decagon 10Sides"]

        self.Type = "HoneycombFence"
        BaseHoneycombFence.Placement = obj.Placement
        obj.Proxy = self
        obj.HoleType =_holeType

    def createPolygonOne3D(self, sides=3):
        try:
            points = []
            flatObj = None
            newObj = None
            angles = 360/sides
            # Extra 5 points to make the object longer for cutting
            y1 = BaseHoneycombFence.Placement.Base.y - (2*self.Thickness+5)
            y2 = -y1+ (2*self.Thickness+5)
            
            for i in range(0, sides):
                # The polygon will be
                x = BaseHoneycombFence.Placement.Base.x-self.Width/2 +self.HoleRadius * math.cos(math.radians(i*angles))
                z = BaseHoneycombFence.Placement.Base.z+self.HoleRadius * math.sin(math.radians(i*angles))
                points.append(App.Vector(x, y1, z))
            
            points.append(points[0])  # close the loop
            flatObj = Part.Face(Part.makePolygon(points))
            newObj = flatObj.extrude(App.Vector(0, y2, 0))
            return newObj

        except Exception as err:
            App.Console.PrintError("'createObject HoneycombFence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def createOneLine(self, _sides):
        try:
            pos = self.Distance+self.HoleRadius*2
            plc = BaseHoneycombFence.Placement.copy()
            ringHoles = []
            plc.Rotation.Axis = App.Vector(0.0, 0.0, 1.0)
            plc.Base = BaseHoneycombFence.Placement.Base
            startX=plc.Base.x
            for i in range(0, self.Holes+2):
                if self.HoleType=="Circle":
                    ringHoles.append(self.createOneCylinder())
                else:
                    ringHoles.append(self.createPolygonOne3D(_sides))
                plc.Base.x= startX+(pos*i)
                ringHoles[i].Placement = plc
            return (Part.makeCompound(ringHoles))

        except Exception as err:
            App.Console.PrintError("'createObject HoneycombFence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    
    def createOneCylinder(self):        
        try:
            flatObj = None
            newObj = None
            x = BaseHoneycombFence.Placement.Base.x-self.Width/2
            z = BaseHoneycombFence.Placement.Base.z
            y1 = BaseHoneycombFence.Placement.Base.y - (2*self.Thickness+5)
            y2 = -y1+ (2*self.Thickness+5)
            circle=Part.Wire(Part.makeCircle(self.HoleRadius,App.Vector(x,y1,z),App.Vector(0,1,0)))
            flatObj = Part.Face(circle)
            newObj = flatObj.extrude(App.Vector(0, y2, 0))
            return newObj

        except Exception as err:
            App.Console.PrintError("'createObject HoneycombFence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def createObject(self):
        baseObj = None
        try:
            # origin center is in the centerofmass #  TODO: Good or bad? let me know!
            baseObj = Part.makeBox(self.Width, self.Thickness,self.Height,
                                        App.Vector(BaseHoneycombFence.Placement.Base.x-self.Width/2,
                                                   BaseHoneycombFence.Placement.Base.y,
                                                   BaseHoneycombFence.Placement.Base.z-self.Height/2))
            z = -self.Height/2
            allRings = []
            cutRot = 20
            _sides = 1
            nrOfRings = int(self.Height/(self.Distance))
            compoundOBJ=None
            if self.HoleType == "":
                # No holes
                pass  # do nothing

            elif self.HoleType == "Circle":
                pass
            elif (self.HoleType == "Triangle 03Sides" or 
                  self.HoleType == "Square 04Sides" or
                  self.HoleType == "Pentagon 05Sides" or
                  self.HoleType == "Hexagon 06Sides" or
                  self.HoleType == "Heptagon 07Sides" or
                  self.HoleType == "Octagon 08Sides" or
                  self.HoleType == "Nonagon 09Sides" or
                  self.HoleType == "Decagon 10Sides"):
                pos=self.HoleType.find(" ")+1
                _sides=int(self.HoleType[pos:pos+2])
                if _sides==0 and self.HoleType != "Circle":
                    _sides=3 #avoid divide by zero
                    print("warning the side was zero")

            for i in range(0, nrOfRings*2+3):
                z = -self.Height/2+(self.Distance/2)*i
                allRings.append(self.createOneLine(_sides))
                allRings[i].Placement.Base.z = z
                if cutRot == 0:
                    cutRot = self.HoleRadius*2
                else:
                    cutRot = 0
                allRings[i].Placement.Base.x=allRings[i].Placement.Base.x+cutRot
                compoundOBJ = Part.Compound(allRings)
            compoundOBJ = Part.Compound(allRings)
            ResultObj = baseObj.cut(compoundOBJ)
            return ResultObj

        except Exception as err:
            App.Console.PrintError("'createObject HoneycombFence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def execute(self, obj):
        try:
            self.Height = float(obj.Height)
            self.Width = float(obj.Width)
            self.Thickness=float(obj.Thickness)
            self.HoleType = obj.HoleType
            if self.Width>self.Height:
                self.HoleRadius = (self.Height/6)*0.5
            else:    
                self.HoleRadius = (self.Width/6)*0.5
            self.Distance =self.HoleRadius*2.2
            self.Holes = int(self.Width/(self.HoleRadius+self.Distance))
            obj.Shape = Part.makeCompound(self.createObject())

        except Exception as err:
            App.Console.PrintError("'execute HoneycombFence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class Design456_HoneycombFence:

    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'HoneycombFence.svg',
                'MenuText': "HoneycombFence",
                'ToolTip': "Generate a HoneycombFence"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "HoneycombFence")
        plc = App.Placement()
        plc.Base = App.Vector(0, 0, 0)
        plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        newObj.Placement = plc

        BaseHoneycombFence(newObj)
        ViewProviderHoneycombFence(newObj.ViewObject, "HoneycombFence")
        v = Gui.ActiveDocument.ActiveView
        App.ActiveDocument.recompute()
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_HoneycombFence', Design456_HoneycombFence())
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#TODO:FIXME:

# Pen holder

class ViewProviderPenHolder:

    obj_name = "PenHolder"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderPenHolder.obj_name
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
        return (Design456Init.ICON_PATH + 'PenHolder.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

class BasePenHolder:
    """ PenHolder shape based on several parameters
    """
    Placement=None
    def __init__(self, obj,
                 _height=12.0,  # Shape hight
                 _radius=12.0,
                 _thickness=2,
                 _sectionWidth=4,
                 _sharpLength=2,
                 _coverIssue=0.4,
                 _makeShell=True

                 ):

        obj.addProperty("App::PropertyLength", "Height", "PenHolder",
                        "Height of the PenHolder").Height = _height

        obj.addProperty("App::PropertyLength", "Thickness", "PenHolder",
                        "Thickness of the PenHolder").Thickness = _thickness
        
        obj.addProperty("App::PropertyLength", "SectionWidth", "PenHolder",
                        "Section Width of the PenHolder").SectionWidth = _sectionWidth

        obj.addProperty("App::PropertyLength", "Radius", "PenHolder",
                        "Radius of the PenHolder").Radius = _radius

        obj.addProperty("App::PropertyLength", "SharpLength", "PenHolder",
                        "Sharp Length of the PenHolder").SharpLength = _sharpLength
        
        obj.addProperty("App::PropertyBool", "makeShell", "PenHolder",
                        "Make shell for the PenHolder").makeShell = _makeShell

        obj.addProperty("App::PropertyLength", "CoverIssue", "PenHolder",
                        "Cover issue of the PenHolder").CoverIssue = _coverIssue
                
        self.Type = "PenHolder"
        BasePenHolder.Placement = obj.Placement
        obj.Proxy = self
        
    def createObjectOneElement(self):
        """ Create one element that will be used later to create the object
            by copying it and rotating. Later merging all of them. 
        """
        ResultObj=None
        plc=BasePenHolder.Placement.Base
        """   One element consist of 3 parts box, and two pyramid
                                box
                        ......................  
                     .                           .
                        ......................  
        """
        try:
            rows=int(self.Height/self.SectionWidth)
            objs=[]
            originalZ=plc.z
            starty=plc.y-self.Radius
            for i in range(0,rows):
                plc.z=originalZ+self.SectionWidth*i
                p1 =App.Vector(plc.x,starty,plc.z)
                p2 =App.Vector(plc.x+self.SectionWidth,starty,plc.z)
                p3 =App.Vector(plc.x+self.SectionWidth,starty,plc.z+self.SectionWidth)
                p4 =App.Vector(plc.x,starty,plc.z+self.SectionWidth)
                p11=App.Vector(plc.x,starty+self.Radius*2,plc.z)
                p12=App.Vector(plc.x+self.SectionWidth,starty+self.Radius*2,plc.z)
                p13=App.Vector(plc.x+self.SectionWidth,starty+self.Radius*2,plc.z+self.SectionWidth)
                p14=App.Vector(plc.x,starty+self.Radius*2,plc.z+self.SectionWidth)

                p15= App.Vector(plc.x+self.SectionWidth/2,starty-self.SharpLength,plc.z+self.SectionWidth/2)
                p16=App.Vector(plc.x+self.SectionWidth/2,starty+self.Radius*2+self.SharpLength,plc.z+self.SectionWidth/2)

                #Square shape on the sides
                left=Part.Face(Part.Wire(Part.makePolygon([p1,p2,p3,p4,p1])))
                right=Part.Face(Part.Wire(Part.makePolygon([p11,p12,p13,p14,p11])))

                #Pyramid on the sides:
                side1=Part.Face(Part.Wire(Part.makePolygon([p1,p2,p15,p1])))
                side2=Part.Face(Part.Wire(Part.makePolygon([p2,p3,p15,p2])))
                side3=Part.Face(Part.Wire(Part.makePolygon([p3,p4,p15,p3])))
                side4=Part.Face(Part.Wire(Part.makePolygon([p4,p1,p15,p4])))

                side11=Part.Face(Part.Wire(Part.makePolygon([p11,p12,p16,p11])))
                side12=Part.Face(Part.Wire(Part.makePolygon([p12,p13,p16,p12])))
                side13=Part.Face(Part.Wire(Part.makePolygon([p13,p14,p16,p13])))
                side14=Part.Face(Part.Wire(Part.makePolygon([p14,p11,p16,p14])))
                leftG =Part.Solid(Part.Shell([left,side1,side2,side3,side4]))
                rightG=Part.Solid(Part.Shell([right,side11,side12,side13,side14]))
                box=left.extrude(App.Vector(0,self.Radius*2,0))
                ResultObj1=box.fuse(leftG)
                ResultObj=ResultObj1.fuse(rightG)
                objs.append(ResultObj)
            finalObj=objs[0]
            for i in range(1,len(objs)):
                finalObj=finalObj.fuse(objs[i])
            return finalObj.removeSplitter()

        except Exception as err:
            App.Console.PrintError("'createObject PenHolder' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def createObject(self):
        try:
            Columns=int(math.pi*self.Radius/self.SectionWidth)
            angles=180/Columns
            allObj=[]
            OneColumn=self.createObjectOneElement()
            for i in range(1,Columns):
                nobj=OneColumn.copy()
                nobj.Placement.Rotation.Axis=App.Vector(0,0,1)
                nobj.Placement.Rotation.Angle=math.radians(angles*i)
                allObj.append(nobj)
            cyl1=Part.makeCylinder(self.Radius+self.CoverIssue,self.Height,BasePenHolder.Placement.Base) #TODO: This must be a segmented cylinder
            outsideObj=OneColumn.fuse([*allObj,cyl1])
            newObj1=outsideObj.removeSplitter()
            if self.makeShell is True:
                plc=BasePenHolder.Placement.copy()
                plc.Base.z=plc.Base.z+self.Thickness
                cyl2=Part.makeCylinder(self.Radius-self.Thickness,self.Height,plc.Base) 
                FinalObject=newObj1.cut(cyl2)
            else:
                FinalObject=newObj1
            FinalObject.Placement=BasePenHolder.Placement
            return FinalObject
        except Exception as err:
            App.Console.PrintError("'execute PenHolder' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def execute(self, obj):
        self.Height = float(obj.Height)
        self.Radius = float(obj.Radius)
        self.Thickness=float(obj.Thickness)
        self.SectionWidth=float(obj.SectionWidth)
        self.SharpLength=float(obj.SharpLength)
        self.makeShell = bool(obj.makeShell)
        self.CoverIssue=float(obj.CoverIssue)
        obj.Shape =self.createObject()


class Design456_PenHolder:

    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'PenHolder.svg',
                'MenuText': "PenHolder",
                'ToolTip': "Generate a PenHolder"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "PenHolder")
        plc = App.Placement()
        plc.Base = App.Vector(0, 0, 0)
        plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        newObj.Placement = plc

        BasePenHolder(newObj)
        ViewProviderPenHolder(newObj.ViewObject, "PenHolder")
        v = Gui.ActiveDocument.ActiveView
        App.ActiveDocument.recompute()
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_PenHolder', Design456_PenHolder())



######################################################################################
#TODO : FIXME: Shell is not implemented yet
# Pumpkin

class ViewProviderPumpkin:

    obj_name = "Pumpkin"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderPumpkin.obj_name
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
        return (Design456Init.ICON_PATH + 'Pumpkin.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

class BasePumpkin:
    """ Pumpkin shape based on several parameters
    """
    Placement=None
    def __init__(self, obj,
                 _radius=10.0,
                 _scale=0.75,
                 _sectionWidth=10.0,
                 _sections=8,
                 _makeShell=True ):

        obj.addProperty("App::PropertyLength", "SectionWidth", "Pumpkin",
                        "Section Width of the Pumpkin").SectionWidth = _sectionWidth
        
        obj.addProperty("App::PropertyLength", "Scale", "Pumpkin",
                        "Radius of the Pumpkin").Scale = _scale

        obj.addProperty("App::PropertyInteger", "Sections", "Pumpkin",
                        "Radius of the Pumpkin").Sections = _sections
        
        obj.addProperty("App::PropertyLength", "Radius", "Pumpkin",
                        "Radius of the Pumpkin").Radius = _radius
        
        #TODO :FIXME : Not implemented yet
        obj.addProperty("App::PropertyBool", "makeShell", "Pumpkin",
                        "Make shell for the Pumpkin").makeShell = _makeShell
        self.Type = "Pumpkin"
        BasePumpkin.Placement = obj.Placement
        obj.Proxy = self
        
    def createObjectOneElement(self):
        """ Create one element that will be used later to create the object
            by copying it and rotating. Later merging all of them. 
        """
        obj1=None
        try:
            mtr1= App.Matrix(  
                             1, 0,          0, 0,
                             0, self.Scale, 0, 0,
                             0, 0,          1, 0,
                             0, 0,          0, 1)
                                    
            obj1=Part.makeSphere(self.Radius,
                                      App.Vector(self.SectionWidth/2,0,0),
                                      App.Vector(0,0,1)
                                      )
            obj2=Part.makeSphere(self.Radius,
                                      App.Vector(-self.SectionWidth/2,0,0),
                                      App.Vector(0,0,1)
                                      )
            obj1=obj1.transformGeometry(mtr1)
            obj2=obj2.transformGeometry(mtr1)
            obj3=obj1.fuse(obj2)
            obj3.Placement=BasePumpkin.Placement.copy()
            return obj3

        except Exception as err:
            App.Console.PrintError("'createObject Pumpkin' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def createObject(self):
        try:
            angle=math.radians(180/self.Sections)
            Elements=[]
            first=self.createObjectOneElement()
            for i in range(0,self.Sections-1):
                Elements.append(first.copy())
                Elements[i].Placement.Rotation.Angle=angle+angle*(i)
                Elements[i].Placement.Rotation.Axis=App.Vector(0,0,1)

            finalObj=first.fuse(Elements)
            return finalObj
        except Exception as err:
            App.Console.PrintError("'execute Pumpkin' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def execute(self, obj):
        self.Radius = float(obj.Radius)
        self.SectionWidth=float(obj.SectionWidth)
        self.makeShell = bool(obj.makeShell)
        self.Scale=float(obj.Scale)
        self.Sections=int(obj.Sections)
        obj.Shape =self.createObject()

class Design456_Pumpkin:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Pumpkin.svg',
                'MenuText': "Pumpkin",
                'ToolTip': "Generate a Pumpkin"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Pumpkin")
        plc = App.Placement()
        plc.Base = App.Vector(0, 0, 0)
        plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        newObj.Placement = plc

        BasePumpkin(newObj)
        ViewProviderPumpkin(newObj.ViewObject, "Pumpkin")
        v = Gui.ActiveDocument.ActiveView
        App.ActiveDocument.recompute()
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_Pumpkin', Design456_Pumpkin())