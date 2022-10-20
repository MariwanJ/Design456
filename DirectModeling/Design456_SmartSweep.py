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


__updated__ = '2022-10-19 22:24:03'

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
        print("dragging!!")
        try:
            if userData is None:
                return  # Nothing to do here - shouldn't be None
            #self.redraw()
            #App.ActiveDocument.recompute()
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
    """
    __slots__ = ['myWindow','Apply','Section','PathVertices','PathPointList','PathType','Type','StepSize']
    Placement=None
    WidgetObj=[]
    def __init__(self, obj, 
                 _section=None,
                 _pathType="BSplineCurve" ):
        
        obj.addProperty("App::PropertyLink","Section","Sweep",
                        QT_TRANSLATE_NOOP("App::Property","Face to sweep")).Section=_section
        obj.addProperty("App::PropertyVectorList","PathVertices", "Sweep",
                        QT_TRANSLATE_NOOP("App::Property","PathVertices" )).PathVertices=[]        
        obj.addProperty("App::PropertyLinkList", "PathPointList", "Sweep", 
                        QT_TRANSLATE_NOOP("App::Property", "Link to Point objects")).PathPointList=[]
        obj.addProperty("App::PropertyBool", "Apply", "Execute",
                        QT_TRANSLATE_NOOP("App::Property","Execute the command" )).Apply=False
        obj.addProperty("App::PropertyEnumeration", "PathType", "PathType",
                        "FlowerVase middle type").PathType = ["BSplineCurve","Curve", "Line"]
        obj.PathType = _pathType
        self.Type = "SmartSweep"
        self.StepSize=0.1
        BaseSmartSweep.Placement = obj.Placement
        obj.Proxy = self
        self.myWindow=None
                    
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
                tnObj.setTransitionMode(0)  # Round edges
                f = tnObj.shape().Faces
                f.append(base)
                final = Part.makeShell(f)
                finalObj=Part.makeSolid(final)
            else:
                finalObj = sweepPath
            return finalObj

        except Exception as err:
            App.Console.PrintError("'createObject SmartSweep' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def delOldCoin3dObjects(self):
        try:
            if self.myWindow is None:
                self.myWindow=win.Fr_CoinWindow()
            for i in range(0,len(BaseSmartSweep.WidgetObj)):
                BaseSmartSweep.WidgetObj[i].__del__()
                del BaseSmartSweep.WidgetObj[i]
            BaseSmartSweep.WidgetObj.clear()
            
        except Exception as err:
            App.Console.PrintError("'delOldCoin3dObjects SmartSweep' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def recreateCOIN3DObjects(self):
        try:
            self.delOldCoin3dObjects()
            for i in range(0,len(self.PathPointList)):
                BaseSmartSweep.WidgetObj.append(threeArrowBall([
                    App.Vector(self.PathPointList[i].X,
                               self.PathPointList[i].Y,
                               self.PathPointList[i].Z)
                               ,App.Vector(0,0,0)]))
                BaseSmartSweep.WidgetObj[i].setFreeCADObj(self.PathPointList[i])

                BaseSmartSweep.WidgetObj[i].Activated()
                BaseSmartSweep.WidgetObj[i].w_userData.callerObject = self
                #BaseSmartSweep.WidgetObj[i].w_parent=self.myWindow
                self.myWindow.addWidget(BaseSmartSweep.WidgetObj[i])

            self.myWindow.show()
            
        except Exception as err:
            App.Console.PrintError("'recreateCOIN3DObjects SmartSweep' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def reCreateSweep(self):
        try:
            points=[]
            for i in range(0,len(self.PathPointList)):
                points.append(App.Vector(self.PathPointList[i].X,
                               self.PathPointList[i].Y,
                               self.PathPointList[i].Z))
            if self.PathType == "BSplineCurve":
                curve=Part.BSplineCurve()
                curve.interpolate(points)
                return Part.Wire(curve.toShape())
            elif self.PathType == "Curve":
                pass
            elif self.PathType == "Line":
                pass
            
        except Exception as err:
            App.Console.PrintError("'reCreateSweep SmartSweep' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)       

    def execute(self, obj):
        try:
            
            self.Section= obj.Section
            self.PathVertices=obj.PathVertices      #List link to Draft.Point objects.
            self.Apply=obj.Apply                    #Create the sweep 
            self.PathPointList=obj.PathPointList    #Either you put directly your vertices or you create point objects not both.
            self.PathType=obj.PathType              #BSplineCurve, Curve, or Line
            self.myWindow=None 
            self.StepSize=Design456pref_var.MouseStepSize
            self.recreateCOIN3DObjects()
            objResult = self.createObject()
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
        plc = App.Placement()
        plc.Base = App.Vector(0, 0, 0)
        plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        newObj.Placement = plc
        BaseSmartSweep(newObj)
        ViewProviderSmartSweep(newObj.ViewObject, "SmartSweep")
        # v = Gui.ActiveDocument.ActiveView
        # App.ActiveDocument.recompute()

        # mw = self.getMainWindow()
        #BaseSmartSweep.mywin.show()
        #v = Gui.ActiveDocument.ActiveView
        #App.ActiveDocument.recompute()
        #faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_SmartSweep', Design456_SmartSweep())
#-----------------------------------------------------------------------------

