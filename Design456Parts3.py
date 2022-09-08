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

__updated__ = '2022-09-08 21:10:43'


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
    
    def __getstate__(self):
        return None
    
    def __setstate__(self):
        return None
    
    def getIcon(self):
        return (Design456Init.ICON_PATH + 'Fence.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

class BaseFence:
    """ Fence shape based on several parameters
    """
    placement=App.Placement()
    def __init__(self, obj,
                 _width=30.00,
                 _height=10.00,
                 _sections=10,
                 _connectionWidth=1.00,
                 _sectionWidth=2.00,
                 _bottomDistance=1.00,
                 _topDistance=6.00,
                 _sharpLength=1.00,
                 _type=0,
                 ):

        obj.addProperty("App::PropertyLength", "Width", "Fence",
                        "Width of the Fence").Width = _width
        
        obj.addProperty("App::PropertyLength", "Height", "Fence",
                        "Height of the Fence").Height = _height
        
        obj.addProperty("App::PropertyLength", "ConnectionWidth", "Fence",
                        "Connections Width between sections").ConnectionWidth = _connectionWidth

        obj.addProperty("App::PropertyLength", "SectionWidth", "Fence",
                        "Section Width of the Fence").SectionWidth = _sectionWidth

        obj.addProperty("App::PropertyLength", "BottomDistance", "Fence",
                        "Connection Bottom distance").BottomDistance = _bottomDistance

        obj.addProperty("App::PropertyLength", "TopDistance", "Fence",
                        "Top connection distance").TopDistance = _topDistance

        obj.addProperty("App::PropertyLength", "SharpLength", "Fence",
                        "Sharp part length").SharpLength= _sharpLength
        
        obj.addProperty("App::PropertyInteger", "Sections", "Fence",
                        "Fence type").Sections = _sections
        
        obj.addProperty("App::PropertyInteger", "Type", "Fence",
                        "Fence base type").Type = _type
        obj.Proxy = self
        BaseFence.placement=obj.Placement

        
    def oneElementNormalFence(self,Xoffsett,smallWidth):
        CoreStart=(smallWidth-self.SectionWidth)/2
        zOffset=-self.Height/2
        #Left side         
        p10=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset)

        p11=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.BottomDistance)

        p12=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.BottomDistance)

        p13=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)

        p14=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)

        p15=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.TopDistance)
        
        p16=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.TopDistance)
        
        p17=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)
        
        p18=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)
        
        p19=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+self.Height/2-self.SharpLength)
        
        p20=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+CoreStart+(self.SectionWidth)/2,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+self.Height/2)
        
        #Right side 

        
        p39=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+self.Height/2-self.SharpLength)
        
        p38=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)

        
        p37=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)
        
        p36=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.TopDistance)
                                
        p35=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.TopDistance)                                
                                
        p34=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)
        
 
        p33=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)


        p32=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.BottomDistance)
        
        p31=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset+self.BottomDistance)
        
        p30=App.Vector(BaseFence.placement.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.placement.Placement.Base.y,
                       BaseFence.placement.Placement.Base.z+zOffset)
                
        newobj=Part.Face(Part.Wire(Part.makePolygon([p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p39,p38,p37,p36,p35,p34,p33,p32,p31,p30,p10])))
        objExtr=newobj.extrude(App.Vector(0,2,0))
        return objExtr
    
    def normalFence(self):
        obj1=None
        try:
            smallWidth=self.Width/self.Sections
            objs=[]
            offset=0
            obj1=self.oneElementNormalFence(offset,smallWidth)
            for i in range(1, self.Sections):
                offset=i*smallWidth
                objs.append(self.oneElementNormalFence(offset,smallWidth))
            if(len(objs)>1):
                return (obj1.fuse(objs)).removeSplitter()
            else:
                return obj1.removeSplitter()
            
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


        self.Width = float(obj.Width)        
        self.Height = int(obj.Height)
        self.SectionWidth = float(obj.SectionWidth)
        self.Type = int(obj.Type)
        self.BottomDistance = float(obj.BottomDistance)
        self.TopDistance = float(obj.TopDistance)
        self.SharpLength = float(obj.SharpLength)
        self.ConnectionWidth = float(obj.ConnectionWidth)
        self.Sections = int(obj.Sections)
        #Both distances cannot crosse each other 
        if self.BottomDistance == self.TopDistance or self.BottomDistance > self.TopDistance:
            self.BottomDistance = self.TopDistance -(1.0)
            obj.BottomDistance=self.BottomDistance

        elif self.TopDistance < self.BottomDistance:
            self.TopDistance = self.BottomDistance + (1.0)
            obj.TopDistance=self.TopDistance
            
        obj.Shape = self.createObject()

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