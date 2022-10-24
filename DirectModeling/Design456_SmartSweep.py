# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# **************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2022                                                    *
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
from re import T
import sys
#from tkinter import N

from pivy import coin
import FreeCAD as App
import FreeCADGui as Gui
import FACE_D as faced
from PySide.QtCore import QT_TRANSLATE_NOOP
from typing import List
import Design456Init
from PySide import QtGui, QtCore
from ThreeDWidgets.fr_ball_three_arrows import Fr_BallThreeArrows_Widget
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from ThreeDWidgets import fr_ball_three_arrows 
from Design456Pref import Design456pref_var  #Variable shared between preferences and other tools

from ThreeDWidgets.constant import FR_COLOR
from draftutils.translate import translate  # for translation
import math
from ThreeDWidgets import fr_label_draw
import ThreeDWidgets.fr_coinwindow as win
import Part
import Draft
from symbol import try_stmt
import BOPTools.SplitFeatures


__updated__ = '2022-10-24 20:51:28'

'''
Part.BSplineCurve([poles],              #[vector]
                  [multiplicities],     #[int]
                  [knots],              #[float]
                  periodic,             #bool
                  degree,               #int
                  [weights],            #[float]
                  checkRational)        #bool



import Part

absolutePoints=[]
absolutePoints.append(FreeCAD.Vector(1065.5057, 1215.3951, 0.0))
absolutePoints.append(FreeCAD.Vector(1125.6292, 1247.0432, 0.0)) 
absolutePoints.append(FreeCAD.Vector(1292.6256, 1273.3331, 0.0))

curve=Part.BSplineCurve()
curve.interpolate(absolutePoints)
Part.show(curve.toShape())
Gui.ActiveDocument.ActiveView.fitAll()

'''
#*********************************************************************************


"""
The idea is to have a list of points that you move using the 3Dcoin widget. 
Each 3Dcoin should have it's own callback for each arrow. 
That is why this is a complicated tool. 
I need to figure out how to do that efficiently and optimized. 
not easy :(

TODO:
 -Think about having a distance to the vector point for the 3D coin object
 -Think about how to remove the coin window
 -Think about how to avoid executing sweep with the smallest movement
 -Think about how to finalize the shape (make simple copy)
 -
"""


'''
Instance of the class for this tool. Callbacks will be inside the class.
'''
class threeArrowBall(Fr_BallThreeArrows_Widget):
    
    def __init__(self, vectors: List[App.Vector] = [], label: str = [[]]):
        self.linkToPoint=None
        super().__init__(vectors, label)
        self.oldPosition = None

            
    def setLinkToDraftPoint(self,draftPointObj):
        self.linkToPoint= draftPointObj# 
    
    def callback(self,userData):
        App.ActiveDocument.recompute()
        pass #Do nothing
    
    def Activated(self):
        self.w_ball_cb_=self.DraggingCallback
        self.w_xAxis_cb_=self.DraggingCallback
        self.w_yAxis_cb_=self.DraggingCallback
        self.w_zAxis_cb_=self.DraggingCallback
        self.w_callback_=self.callback
            
    def DraggingCallback(self,userData: fr_ball_three_arrows.userDataObject = None):
        """[ Callback for the arrow movement. 
        This will be used to calculate the length of the Extrude operation.]
        Args:
            userData (fr_ball_three_arrows.userDataObject, optional): 
            [Userdata contain link to several variable and the ball-arrows widget]. Defaults to None.

        Returns:
            [type]: [Nothing is returned].
        """
        try:
            if userData is None:
                return  # Nothing to do here - shouldn't be None
            return

        except Exception as err:
            App.Console.PrintError("'DraggingCallback' Failed. "
                                "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
 
######################################################################

# Smart Sweep 

class ViewProviderSmartSweep:

    obj_name = "SmartSweep"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderSmartSweep.obj_name
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
        return (Design456Init.ICON_PATH + 'SmartSweep.svg')

    # def __getstate__(self):
    #     return None

    #def __setstate__(self, state):
    #    return None
    #
    
    def __getstate__(self):
      return self.Type 

    def __setstate__(self, state):
       if state:
           self.Type = state 
           
class BaseSmartSweep:
    """ SmartSweep shape with a flexible capabilities 
['Apply', 'CoinVisible', 'PathPointList', 'PathType', 'Placement', 'Section', 'StepSize', 'Type',
    """
    __slots__ = ['Apply','CoinVisible','PathPointList','PathType','Section','StepSize','Type','WidgetObj']
    #Placement=None
    coinWin=None
    def __init__(self, obj, 
                 _section=None,
                 _pathType="BSplineCurve" ):
        obj.addProperty("App::PropertyLink","Section","Sweep",
                        QT_TRANSLATE_NOOP("App::Property","Face to sweep")).Section=_section   
        obj.addProperty("App::PropertyLinkList", "PathPointList", "Sweep", 
                        QT_TRANSLATE_NOOP("App::Property", "Link to Point objects")).PathPointList=[]
        obj.addProperty("App::PropertyBool", "Apply", "Execute",
                        QT_TRANSLATE_NOOP("App::Property","Execute the command" )).Apply=False
        obj.addProperty("App::PropertyEnumeration", "PathType", "PathType",
                        "FlowerVase middle type").PathType = ["BSplineCurve","ArcOfThree", "Line"]

        obj.addProperty("App::PropertyBool", "CoinVisible", "Execute",
                        QT_TRANSLATE_NOOP("App::Property","Hide or show coin widget" )).CoinVisible=True
            
        obj.PathType = _pathType
        #BaseSmartSweep.Placement = obj.Placement
        global stepSize
        global Type
        global WidgetObj
        
        self.StepSize=0.1
        BaseSmartSweep.coinWin=win.Fr_CoinWindow()
        self.Type = ""
        self.WidgetObj=[]
        obj.Proxy = self
           
    def createObject(self):
        try:
            finalObj = None 
            sweepPath=self.reCreateSweep()
            if self.Section is None:
                return sweepPath
            
            base=self.Section.Shape
            if base is None:
                return sweepPath
            
            if self.Apply==True:
                tnObj = Part.BRepOffsetAPI.MakePipeShell(sweepPath)
                tnObj.add(Part.Wire(base.Edges), WithContact=False, WithCorrection=False) #Todo check WithContact and WithCorrection
                tnObj.setTransitionMode(1)  # Round edges
                tnObj.setFrenetMode(True)
                tnObj.build()  #This will create the shape. Without his the SmartSweep fail since the shape is still not made
                tnObj.makeSolid()
                finalObj=tnObj.shape()
            else:
                finalObj = sweepPath
            self.Section.Placement.Base=App.Vector(self.PathPointList[0].X,self.PathPointList[0].Y,self.PathPointList[0].Z)
            return finalObj

        except Exception as err:
            App.Console.PrintError("'createObject SmartSweep' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def delOldCoin3dObjects(self):
        try:
            if BaseSmartSweep.coinWin is None:
               return
            for i in range(0,len(self.WidgetObj)):
                self.WidgetObj[i].__del__()
            while(len(self.WidgetObj)>0):
                del self.WidgetObj[len(self.WidgetObj)-1]    
            self.WidgetObj.clear()
            
        except Exception as err:
            App.Console.PrintError("'delOldCoin3dObjects SmartSweep' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def recreateCOIN3DObjects(self):
        try:
            if self.CoinVisible is False:
                if BaseSmartSweep.coinWin is None:
                    BaseSmartSweep.coinWin=win.Fr_CoinWindow()
                BaseSmartSweep.coinWin.hide()
                return
            self.delOldCoin3dObjects()
            nrOfPoints=len(self.PathPointList)
            if nrOfPoints<1:
                return #Nothing to do 
            for i in range(0,nrOfPoints):
                self.WidgetObj.append(threeArrowBall([
                    App.Vector(self.PathPointList[i].X,
                               self.PathPointList[i].Y,
                               self.PathPointList[i].Z)
                               ,App.Vector(0,0,0)]))
                self.PathPointList[i].Visibility=False
                self.WidgetObj[i].setFreeCADObj(self.PathPointList[i])

                self.WidgetObj[i].Activated()
                self.WidgetObj[i].w_userData.callerObject = self
                BaseSmartSweep.coinWin.addWidget(self.WidgetObj[i])
            self.Section.Visibility = False
            BaseSmartSweep.coinWin.show()
            
        except Exception as err:
            App.Console.PrintError("'recreateCOIN3DObjects SmartSweep' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def reCreateSweep(self):
        try:
            edges=[]
            points=[]
            nrOfPoints=len(self.PathPointList)
            for i in range(0,nrOfPoints):
                points.append(App.Vector(self.PathPointList[i].X,
                               self.PathPointList[i].Y,
                               self.PathPointList[i].Z))
            if self.PathType == "BSplineCurve":
                curve=Part.BSplineCurve()
                curve.interpolate(points)
                return Part.Wire(curve.toShape())
            
            if self.PathType == "ArcOfThree":
                nrOfEdges=0
                nrOfEdges=int(nrOfPoints/3)
                ge=int(nrOfEdges*3)
                if (ge!=nrOfPoints):
                    #We have less than 3*n points. You need to give multiples of 3 points.
                    App.Console.PrintError("You need to have multiple of 3 points when you use ArcOfThree")
                    App.Console.PrintError("Last points are ignored")
                if nrOfEdges>1:
                    C1 = Part.Arc(points[0], points[1], points[2])
                    edges.append(C1.toShape())
                    for i in range(0,nrOfEdges):
                        C1 = Part.Arc(points[2+2*i], points[3+2*i], points[4+2*i])
                        edges.append(C1.toShape())
                else:
                    C1 = Part.Arc(points[0], points[1], points[2])
                    edges.append(C1.toShape())
                W=Part.Wire(edges)
                return W
            elif self.PathType == "Line":
                W=Part.Wire(Part.makePolygon(points))            
                return W
            
        except Exception as err:
            App.Console.PrintError("'reCreateSweep SmartSweep' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)       

    def execute(self, obj):
        try:
            self.Section= obj.Section
            self.Apply=obj.Apply
            #Create the sweep 
            self.Type = "SmartSweep"
            self.PathPointList=obj.PathPointList   #We must have the first point always.    
            self.PathType=obj.PathType              #BSplineCurve, Curve, or Line

            self.StepSize=Design456pref_var.MouseStepSize
            self.CoinVisible=obj.CoinVisible
            self.recreateCOIN3DObjects()
            objResult = self.createObject()
            if objResult is None:
                objResult = Part.Point(App.Vector(0,0,0)).toShape() #dummy shape just to avoid problem in freecad
            obj.Shape = objResult

        except Exception as err:
            App.Console.PrintError("'execute SmartSweep' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class Design456_SmartSweep:
        
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'SmartSweep.svg',
                'MenuText': "SmartSweep",
                'ToolTip': "Generate a SmartSweep"}

    def Activated(self):
        
        newObj = App.ActiveDocument.addObject("Part::FeaturePython", "SmartSweep")
        # plc = App.Placement()
        # plc.Base = App.Vector(0, 0, 0)
        # plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        #newObj.Placement = plc
        self.baseObj=BaseSmartSweep(newObj)
        ViewProviderSmartSweep(newObj.ViewObject, "SmartSweep")
        App.ActiveDocument.recompute()

Gui.addCommand('Design456_SmartSweep', Design456_SmartSweep())
#-----------------------------------------------------------------------------

