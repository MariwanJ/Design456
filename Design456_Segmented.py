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
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft 
import Part 
import FACE_D as faced
from draftutils.translate import translate   #for translate
import math 
import DraftGeomUtils
import Design456Init
import Design456_NewParts

__updated__ = '2022-05-21 18:21:32'

#SegmentedSphere

class ViewProviderSphere:

    obj_name = "SegmentedSphere"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderSphere.obj_name
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
        return ( Design456Init.ICON_PATH + 'SegmentedSphere.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None



class SegmentedSphere:
    def __init__(self, obj, 
                       radius=10,
                       segments=15,
                       rings=10
                       ):
        obj.addProperty("App::PropertyLength", "Radius", "SegmentedSphere",
                        "Radius of the SegmentedSphere").Radius = radius
        # This causes the shape to be invalid
        # obj.addProperty("App::PropertyLength", "Z_Angle","SegmentedSphere",
        #                 "Z axis angle of the SegmentedSphere").Z_Angle =z_angle

        # obj.addProperty("App::PropertyLength", "XY_Angle","SegmentedSphere", 
        #                 "XY axis angle of the SegmentedSphere").XY_Angle=xy_angle

        obj.addProperty("App::PropertyLength", "Segments","SegmentedSphere", 
                        "segments of the SegmentedSphere").Segments =segments

        obj.addProperty("App::PropertyLength", "Rings","SegmentedSphere", 
                        "Rings of the SegmentedSphere").Rings=rings
        
        obj.Proxy = self
    
    def make_face(self,vert):
        face=None

        try:       
            wire = Part.makePolygon(vert)
            face=Part.Face(wire)
            self.faces.append(face)
        except:
            wire1 = Part.makePolygon([vert[0],vert[1],vert[2],vert[0]])
            wire2 = Part.makePolygon([vert[0],vert[2],vert[3],vert[0]])
            face1=Part.Face(wire1)
            face2=Part.Face(wire2)
            self.faces.append(face1)
            self.faces.append(face2)

    def execute(self, obj):
        self.Radius = float(obj.Radius)
        self.Z_Angle=180.0
        self.XY_Angle=360.0
        self.Segments=int(obj.Segments)
        self.Rings=int(obj.Rings)
        self.vertexes = [[]]
        self.faces = []
        self.phi = 0
        self.faces.clear()
        self.vertexes.clear()
        self.Untouchedfaces = []
        try:
            for ring in range(0,self.Rings+1):
                self.vertexes.append([])
                phi = ring * math.radians(self.Z_Angle) / self.Rings
                for segment in range(0,self.Segments+1):
                    theta = segment * math.radians(self.XY_Angle) / self.Segments
                    x = round(self.Radius * math.cos(theta) * math.sin(phi),0)
                    y = round(self.Radius * math.sin(theta) * math.sin(phi),0)
                    # To let the object be above (0,0,0) we have to add the radius
                    z =  round(self.Radius * math.cos(phi),0) + self.Radius 
                    self.vertexes[ring].append(App.Vector(x, y, z))
    
            for j in range(0,self.Rings):
                for i in range(0, self.Segments):
                    self.make_face([self.vertexes[j+1][i],self.vertexes[j][i], self.vertexes[j][i+1],self.vertexes[j+1][i+1],self.vertexes[j+1][i]])
            _shell=Part.Shell(self.faces)
            obj.Shape = Part.Solid(_shell)
        
        except Exception as err:
            App.Console.PrintError("'SegmentedSphere' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

class Design456_Seg_Sphere:
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'SegmentedSphere.svg',
                'MenuText': "SegmentedSphere",
                'ToolTip': "Generate a SegmentedSphere"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "SegmentedSphere")
        SegmentedSphere(newObj)
        ViewProviderSphere(newObj.ViewObject, "SegmentedSphere")
        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_Seg_Sphere', Design456_Seg_Sphere())

#************************

#SegmentedCylinder

class ViewProviderCylinder:

    obj_name = "SegmentedCylinder"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderCylinder.obj_name
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
        return ( Design456Init.ICON_PATH + 'SegmentedCylinder.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None



class SegmentedCylinder:
    def __init__(self, obj, 
                       radius=10,
                       xy_angle=360,
                       segments=8,
                       height=10
                       ):
        obj.addProperty("App::PropertyLength", "Radius", "SegmentedCylinder",
                        "Radius of the SegmentedCylinder").Radius = radius

        obj.addProperty("App::PropertyAngle", "XY_Angle","SegmentedCylinder", 
                        "XY axis angle of the SegmentedCylinder").XY_Angle=xy_angle

        obj.addProperty("App::PropertyLength", "Segments","SegmentedCylinder", 
                        "segments of the SegmentedCylinder").Segments =segments

        obj.addProperty("App::PropertyLength", "Height","SegmentedCylinder", 
                        "Rings of the SegmentedCylinder").Height=height
        obj.Proxy = self
    
    def execute(self, obj):
        self.Radius = float(obj.Radius)
        self.XY_Angle=float(obj.XY_Angle)
        self.Segments=int(obj.Segments)
        self.Height=float(obj.Height)
        pl = App.Placement()
        pl.Rotation.Q = (0.0, 0.0, 0, 1.0)
        pl.Base = App.Vector(0, 0, 0.0)
        vertices =[]
        FIRST=None
        for segment in range(0,self.Segments):
            theta = segment * math.radians(self.XY_Angle) / self.Segments
            x= self.Radius*math.cos(theta)
            y=math.sin(theta)*self.Radius
            vertices.append(App.Vector(x,y,0.0))
        vertices.append(vertices[0])
        polygon=Part.Face(Part.makePolygon(vertices))
        solid=polygon.extrude(App.Vector(0.0, 0.0,self.Height ))
        obj.Shape= solid


class Design456_Seg_Cylinder:
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'SegmentedCylinder.svg',
                'MenuText': "SegmentedCylinder",
                'ToolTip': "Generate a SegmentedCylinder"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "SegmentedCylinder")
        SegmentedCylinder(newObj)

        ViewProviderCylinder(newObj.ViewObject, "SegmentedCylinder")

        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_Seg_Cylinder', Design456_Seg_Cylinder())



####################################################
#Group tools

class Design456_Segmented:
    #import polyhedrons
    list = ["Design456_Seg_Sphere",
            "Design456_Seg_Cylinder",
            "Design456_Seg_Roof",
            "Design456_RoundRoof",
            "Design456_Paraboloid",
            "Design456_Capsule",
            "Design456_Parallelepiped",

            "Design456_Housing",
            "Design456_RoundedHousing",
            "Design456_EllipseBox",
            "Design456_NonuniformedBox",
            ]




    """Design456 Part Toolbar"""

    def GetResources(self):
        return{
            'Pixmap':   Design456Init.ICON_PATH + 'Part_Seg_Parts.svg',
            'MenuText': 'Seg Parts',
                        'ToolTip': 'Segmented Parts'
        }

    def IsActive(self):
        if App.ActiveDocument is None:
            return False
        else:
            return True
