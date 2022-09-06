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
from draftutils.translate import translate  # for translate
import Design456Init
import FACE_D as faced
import DraftGeomUtils
import math
import BOPTools.SplitFeatures

__updated__ = '2022-09-06 21:16:26'


#TODO : FIXME: 
# Fence

class ViewProviderFence:

    obj_name = "Fence"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderFence.obj_name
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
        return (Design456Init.ICON_PATH + 'Fence.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

class BaseFence:
    """ Fence shape based on several parameters
    """

    def __init__(self, obj,
                 _width=10.0,
                 _height=10,
                 _connectionWidth=1,
                 _sectionWidth=4,
                 _topDistance1=1,
                 _TopDistance2=3,
                 _topDistance3=4,
                 _type=0,
                 ):

        obj.addProperty("App::PropertyLength", "Width", "Fence",
                        "Width of the Fence").Width = _width

        obj.addProperty("App::PropertyLength", "ConnectionWidth", "Fence",
                        "Section Width of the Fence").ConnectionWidth = _connectionWidth

        obj.addProperty("App::PropertyLength", "SectionWidth", "Fence",
                        "Section Width of the Fence").SectionWidth = _sectionWidth

        obj.addProperty("App::PropertyLength", "TopDistance1", "Fence",
                        "Top distance1 for section").TopDistance1 = _topDistance1

        obj.addProperty("App::PropertyLength", "TopDistance2", "Fence",
                        "Top distance2 for section").TopDistance2 = _TopDistance2

        obj.addProperty("App::PropertyLength", "TopDistance3", "Fence",
                        "Top distance2 for section").TopDistance3= _topDistance3

        obj.addProperty("App::PropertyInteger", "Height", "Fence",
                        "Radius of the Fence").Height = _height
        
        obj.addProperty("App::PropertyInteger", "Type", "Type",
                        "FlowerVase base type").Type = _type
        self.Type = _type
        self.Placement = obj.Placement
        obj.Proxy = self
    def oneElementNormalFence(self):
        obj=None
        CoreStart=(self.Width-self.SectionWidth)/2
        zOffset=-self.Height/2
        #Left side 
        
        p10=App.Vector(self.Placement.Base.x+CoreStart,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset)

        p11=App.Vector(self.Placement.Base.x+CoreStart,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance1)

        p12=App.Vector(self.Placement.Base.x,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance1)

        p13=App.Vector(self.Placement.Base.x,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance1+self.ConnectionWidth)

        p14=App.Vector(self.Placement.Base.x+CoreStart,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance1+self.ConnectionWidth)

        p15=App.Vector(self.Placement.Base.x+CoreStart,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance2)
        
        p16=App.Vector(self.Placement.Base.x,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance2)
        
        p17=App.Vector(self.Placement.Base.x,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance2+self.ConnectionWidth)
        
        p18=App.Vector(self.Placement.Base.x+CoreStart,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance2+self.ConnectionWidth)
        
        p19=App.Vector(self.Placement.Base.x+CoreStart,
                       self.Placement.Base.y,
                       self.Placement.Base.z+self.Height/2-self.TopDistance3)
        
        p20=App.Vector(self.Placement.Base.x+CoreStart+(self.SectionWidth)/2,
                       self.Placement.Base.y,
                       self.Placement.Base.z+self.Height)
        
        #Right side 

        
        p39=App.Vector(self.Placement.Base.x+CoreStart+self.SectionWidth,
                       self.Placement.Base.y,
                       self.Placement.Base.z+self.Height/2-self.TopDistance3)
        
        p38=App.Vector(self.Placement.Base.x+CoreStart+self.SectionWidth,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance2+self.ConnectionWidth)

        
        p37=App.Vector(self.Placement.Base.x+self.SectionWidth,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance2+self.ConnectionWidth)
        
        p36=App.Vector(self.Placement.Base.x+self.SectionWidth,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance2)
                                
        p35=App.Vector(self.Placement.Base.x+CoreStart+self.SectionWidth,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance2)                                
                                
        p34=App.Vector(self.Placement.Base.x+CoreStart+self.SectionWidth,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance1+self.ConnectionWidth)
        
 
        p33=App.Vector(self.Placement.Base.x+self.SectionWidth,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance1+self.ConnectionWidth)


        p32=App.Vector(self.Placement.Base.x+self.SectionWidth,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance1)
        p31=App.Vector(self.Placement.Base.x+CoreStart+self.SectionWidth,
                       self.Placement.Base.y,
                       self.Placement.Base.z+zOffset+self.TopDistance1)
        
        obj=Part.Face(Part.Wire(Part.makePolygon([p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p39,p38,p37,p36,p35,p34,p33,p32,p31,p10])))
        objExtr=obj.extrude(App.Vector(0,2,0))
        return objExtr
    
    def normalFence(self):
        obj1=None
        try:
            obj1=self.oneElementNormalFence()
            return obj1

        except Exception as err:
            App.Console.PrintError("'createObject Fence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def TypeOne(self):
        try:
            return self.normalFence()
    
        except Exception as err:
            App.Console.PrintError("'createObject Fence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
 
    def createObject(self):
        try:
            finalObj=None
            if self.Type==0:
                finalObj=self.normalFence()
            elif self.Type==1:
                pass
            elif self.Type==2:
                pass
            elif self.Type==3:
                pass
            elif self.Type==4:
                pass
            
            return finalObj
        except Exception as err:
            App.Console.PrintError("'execute Fence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def execute(self, obj):
        self.Width=float(obj.Width)        
        self.Height=int(obj.Height)
        self.SectionWidth = float(obj.SectionWidth)
        self.Type=int(obj.Type)
        self.TopDistance1=float(obj.TopDistance1)
        self.TopDistance2=float(obj.TopDistance2)
        self.TopDistance3=float(obj.TopDistance3)
        self.ConnectionWidth=float(obj.ConnectionWidth)
        
        obj.Shape =self.createObject()

class Design456_Fence:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Fence.svg',
                'MenuText': "Fence",
                'ToolTip': "Generate a Fence"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Fence")
        plc = App.Placement()
        plc.Base = App.Vector(0, 0, 0)
        plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        newObj.Placement = plc

        BaseFence(newObj)
        ViewProviderFence(newObj.ViewObject, "Fence")
        v = Gui.ActiveDocument.ActiveView
        App.ActiveDocument.recompute()
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_Fence', Design456_Fence())