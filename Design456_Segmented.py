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
__updated__ = '2022-02-17 22:11:17'

import Design456Init
# from Part import CommandShapes     #Tube   not working

#Sephere

class ViewProviderBox:

    obj_name = "SegmentedSephere"

    def __init__(self, obj, obj_name):
        self.obj_name = obj_name
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



class SegmentedSephere:
    def __init__(self, obj, 
                       radius=10,
                       z_angle=180,
                       xy_angle=360,
                       segments=10,
                       rings=10
                       ):
        obj.addProperty("App::PropertyLength", "Radius", "SegmentedSephere",
                        "Radius of the SegmentedSephere").Radius = radius
        
        obj.addProperty("App::PropertyLength", "Z_Angle","SegmentedSephere",
                        "Z axis angle of the SegmentedSephere").Z_Angle =z_angle

        obj.addProperty("App::PropertyLength", "XY_Angle","SegmentedSephere", 
                        "XY axis angle of the SegmentedSephere").XY_Angle=xy_angle

        obj.addProperty("App::PropertyLength", "Segments","SegmentedSephere", 
                        "segments of the SegmentedSephere").Segments =segments

        obj.addProperty("App::PropertyLength", "Rings","SegmentedSephere", 
                        "Rings of the SegmentedSephere").Rings=rings
        
        obj.Proxy = self

    def MakeFace(self, vert):
        """[summary]

        Args:
            vert ([type]): [description]

        Returns:
            [Face Object]: [Face created using the vertices]
        """
        try:
            L1 = Part.makePolygon(vert,True)
            S1=Part.Shape(L1)
            App.ActiveDocument.recompute()
            face = Part.Face(S1)
            return face

        except Exception as err:
            App.Console.PrintError("'SegmentedSephere MakeFace' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def execute(self, obj):
        self.Radius = float(obj.Radius)
        self.Z_Angle=float(obj.Z_Angle)
        self.XY_Angle=float(obj.XY_Angle)
        self.Segments=int(obj.Segments)
        self.Rings=int(obj.Rings)
        self.vertexes = [[]]
        self.faces = []
        self.phi = 0

        try:
            self.faces.clear()
            self.vertexes.clear()
            for ring in range(0,self.Rings+1):
                self.vertexes.append([])
                phi = ring * math.radians(self.Z_Angle) / self.Rings
                for segment in range(0,self.Segments+1):
                    theta = segment * math.radians(self.XY_Angle) / self.Segments
                    x = round(self.Radius * math.cos(theta) * math.sin(phi),0)
                    y = round(self.Radius * math.sin(theta) * math.sin(phi),0)
                    z = round(self.Radius * math.cos(phi),0)
                    self.vertexes[ring].append(App.Vector(x, y, z))
            for j in range(0,self.Rings):
                for i in range(0, self.Segments):
                    allSelected=[self.vertexes[j][i], self.vertexes[j][i+1],
                                 self.vertexes[j+1][i+1], self.vertexes[j+1][i]]
                    f=self.MakeFace(allSelected)
                    allSelected.clear()
                    self.faces.append(f)
  
            shel=Part.Shell(self.faces)
            solidObjShape = Part.Solid(shel)
            App.ActiveDocument.recompute()   

        except Exception as err:
            App.Console.PrintError("'SegmentedSephere' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


class Design456_Seg_Sephere:
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'SegmentedSphere.svg',
                'MenuText': "SegmentedSephere",
                'ToolTip': "Generate a SegmentedSephere"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "SegmentedSephere")
        SegmentedSephere(newObj)

        ViewProviderBox(newObj.ViewObject, "SegmentedSephere")

        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_Seg_Sephere', Design456_Seg_Sephere())



####################################################
#Group tools

class Design456_Segmented:
    import polyhedrons
    list = ["Design456_Seg_Sephere",
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
