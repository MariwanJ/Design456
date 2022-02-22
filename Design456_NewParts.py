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

__updated__ = '2022-02-22 21:43:40'


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
        vert2=[App.Vector(self.Thickness,self.Thickness,0),App.Vector(self.Width-self.Thickness,self.Thickness,0),
               App.Vector((self.Width-2*self.Thickness)/2,self.Thickness,self.Height-2*self.Thickness),
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
