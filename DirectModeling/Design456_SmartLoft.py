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

# from tkinter import N

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
from Design456Pref import (
    Design456pref_var,
)  # Variable shared between preferences and other tools

from ThreeDWidgets.constant import FR_COLOR
from draftutils.translate import translate  # for translation
from ThreeDWidgets import fr_label_draw
import ThreeDWidgets.fr_coinwindow as win
import Part


__updated__ = "2022-11-01 22:15:39"

"""
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

"""
# *********************************************************************************


"""
Instance of the class for this tool. Callbacks will be inside the class.
"""


class threeArrowBall(Fr_BallThreeArrows_Widget):
    def __init__(self, vectors: List[App.Vector] = [], label: str = [[]]):
        super().__init__(vectors, label)
        self.linkToPoint = None
        self.oldPosition = None

    def setLinkToDraftPoint(self, draftPointObj):
        self.linkToPoint = draftPointObj  #

    def callback(self, userData):
        App.ActiveDocument.recompute()
        pass  # Do nothing

    def Activated(self):
        self.w_ball_cb_ = self.DraggingCallback
        self.w_xAxis_cb_ = self.DraggingCallback
        self.w_yAxis_cb_ = self.DraggingCallback
        self.w_zAxis_cb_ = self.DraggingCallback
        self.w_callback_ = self.callback

    def DraggingCallback(self, userData: fr_ball_three_arrows.userDataObject = None):
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
            obj=userData.ballArrows

        except Exception as err:
            App.Console.PrintError("'execute SmartLoft' Failed. " "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


######################################################################

# Smart Loft


class ViewProviderSmartLoft:

    obj_name = "SmartLoft"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderSmartLoft.obj_name
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
        return Design456Init.ICON_PATH + "SmartLoft.svg"

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
    

class Design456_SmartLoft:
    def __init__(self):
        self.coinWin=None

    class BaseSmartLoft:
        """SmartLoft shape with a flexible capabilities"""
        # __slots__ = [
        #     "Apply",
        #     "stepSize",
        #     "CoinVisible",
        #     "PathPointList",
        #     "PathType",
        #     "Section",
        #     "StepSize",
        #     "WidgetObj",
        #     "outer"
        # ]
        # Placement=None

        def __init__(self,OuterObject, obj):

            obj.addProperty("App::PropertyLink","Section","Loft",
                    QT_TRANSLATE_NOOP("App::Property", "Face to Loft"),).Section = None
            obj.addProperty("App::PropertyLinkList", "PathPointList", "Loft",
                QT_TRANSLATE_NOOP("App::Property", "Link to Point objects"),).PathPointList = []
            obj.addProperty("App::PropertyBool", "Apply","Execute",
                QT_TRANSLATE_NOOP("App::Property", "Execute the command"),).Apply = False
            obj.addProperty("App::PropertyBool", "SimpleCopy","Finalize",
                QT_TRANSLATE_NOOP("App::Property", "Create Simple Copy"),).SimpleCopy = False

            obj.addProperty("App::PropertyInteger", "CoinScale","Coin",
                QT_TRANSLATE_NOOP("App::Property", "Coin3D scale"),).CoinScale = 6

         
            obj.addProperty("App::PropertyEnumeration", "PathType", "PathType", 
                            "Path Type").PathType = ["BSplineCurve", "ArcOfThree", "Line"]
            obj.addProperty("App::PropertyBool", "CoinVisible", "Execute",
                QT_TRANSLATE_NOOP("App::Property", "Hide or show coin widget"),).CoinVisible = True
            obj.PathType = "BSplineCurve"
            self.outer=OuterObject
            self.WidgetObj=[]
            self.Type="SmartLoft"
            self.done=False
            obj.Proxy = self

        def createObject(self):
            try:
                finalObj = None
                LoftPath = self.reCreateLoft()
                if self.Section is None:
                    return LoftPath

                base = self.Section.Shape
                if base is None:
                    return LoftPath

                if self.Apply == True:
                    tnObj = Part.BRepOffsetAPI.MakePipeShell(LoftPath)
                    tnObj.add(
                        Part.Wire(base.Edges), WithContact=False, WithCorrection=False
                    )  # Todo check WithContact and WithCorrection
                    tnObj.setTransitionMode(1)  # Round edges
                    tnObj.setFrenetMode(False)
                    tnObj.build()  # This will create the shape. Without his the SmartLoft fail since the shape is still not made
                    tnObj.makeSolid()
                    finalObj = tnObj.shape()
                else:
                    finalObj = LoftPath
                self.Section.Placement.Base = App.Vector(
                    self.PathPointList[0].X,
                    self.PathPointList[0].Y,
                    self.PathPointList[0].Z,
                )
                return finalObj

            except Exception as err:
                App.Console.PrintError(
                    "'createObject SmartLoft' Failed. " "{err}\n".format(err=str(err))
                )
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

        def delOldCoin3dObjects(self):
            try:
                totalWID = len(self.WidgetObj)
                for jj in range(0, totalWID):
                    self.WidgetObj[jj].hide()
                    self.WidgetObj[jj].__del__()
                while(len(self.WidgetObj)>0):
                    del self.WidgetObj[len(self.WidgetObj)-1]
                self.WidgetObj.clear()

            except Exception as err:
                App.Console.PrintError(
                    "'delOldCoin3dObjects SmartLoft' Failed. "
                    "{err}\n".format(err=str(err)))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

        def recreateCOIN3DObjects(self):
            try:
                if self.CoinVisible is False:
                    self.outer.coinWin.hide()
                    return
                self.delOldCoin3dObjects()
                if self.outer.coinWin is None:
                    return
                
                nrOfPoints = len(self.PathPointList)
                if nrOfPoints < 1:
                    return  # Nothing to do
                for i in range(0, nrOfPoints):
                    self.WidgetObj.append(
                        threeArrowBall(
                            [
                                App.Vector(
                                    self.PathPointList[i].X,
                                    self.PathPointList[i].Y,
                                    self.PathPointList[i].Z,
                                ),
                                App.Vector(0, 0, 0),
                            ]
                        )
                    )
                    
                    self.PathPointList[i].Visibility = False
                    self.WidgetObj[i].setFreeCADObj(self.PathPointList[i])
                    self.WidgetObj[i].w_Scale=[self.CoinScale,self.CoinScale,self.CoinScale]
                    self.WidgetObj[i].ballScale=[self.WidgetObj[i].w_Scale[0]/6.0,
                                                 self.WidgetObj[i].w_Scale[1]/6.0,
                                                 self.WidgetObj[i].w_Scale[2]/6.0] #there is a diff in scaling ball and arrows
                    
                    self.WidgetObj[i].Activated()
                    self.WidgetObj[i].w_userData.callerObject = self
                    self.outer.coinWin.addWidget(self.WidgetObj[i])
                if self.Section is not None:
                    self.Section.Visibility = False
                self.outer.coinWin.show()

            except Exception as err:
                App.Console.PrintError(
                    "'recreateCOIN3DObjects SmartLoft' Failed. "
                    "{err}\n".format(err=str(err))
                )
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

        def reCreateLoft(self):
            try:
                edges = []
                points = []
                nrOfPoints = len(self.PathPointList)
                if nrOfPoints ==0:
                    return None #Nothing to create
                for i in range(0, nrOfPoints):
                    points.append(
                        App.Vector(
                            self.PathPointList[i].X,
                            self.PathPointList[i].Y,
                            self.PathPointList[i].Z,
                        )
                    )
                if self.PathType == "BSplineCurve":
                    curve = Part.BSplineCurve()
                    curve.interpolate(points)
                    return Part.Wire(curve.toShape())

                if self.PathType == "ArcOfThree":
                    nrOfEdges = 0
                    nrOfEdges = int(nrOfPoints / 3)
                    ge = int(nrOfEdges * 3)
                    if ge != nrOfPoints:
                        # We have less than 3*n points. You need to give multiples of 3 points.
                        App.Console.PrintError(
                            "You need to have multiple of 3 points when you use ArcOfThree"
                        )
                        App.Console.PrintError("Last points are ignored")
                    if nrOfEdges > 1:
                        C1 = Part.Arc(points[0], points[1], points[2])
                        edges.append(C1.toShape())
                        for i in range(0, nrOfEdges):
                            C1 = Part.Arc(
                                points[2 + 2 * i], points[3 + 2 * i], points[4 + 2 * i]
                            )
                            edges.append(C1.toShape())
                    else:
                        C1 = Part.Arc(points[0], points[1], points[2])
                        edges.append(C1.toShape())
                    W = Part.Wire(edges)
                    return W
                elif self.PathType == "Line":
                    W = Part.Wire(Part.makePolygon(points))
                    return W

            except Exception as err:
                App.Console.PrintError(
                    "'reCreateLoft SmartLoft' Failed. " "{err}\n".format(err=str(err))
                )
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

        def execute(self, obj):
            try:
                self.Section = obj.Section
                self.Apply = obj.Apply
                self.CoinScale= obj.CoinScale
                self.SimpleCopy = obj.SimpleCopy  #used to finalize the object
                # Create the Loft

                self.PathPointList = ( obj.PathPointList )  # We must have the first point always.
                self.PathType = obj.PathType  # BSplineCurve, Curve, or Line
                self.StepSize = Design456pref_var.MouseStepSize
                self.CoinVisible = obj.CoinVisible
                self.recreateCOIN3DObjects()
                objResult = self.createObject()
                if objResult is None:
                    objResult = Part.Point(App.Vector(0, 0, 0)).toShape()  # dummy shape just to avoid problem in freecad
                obj.Shape = objResult
                newObj=None
                if self.SimpleCopy is True:
                    import DefeaturingWB.oDefeaturingTools
                    if self.done is True: #Freecad run execute twice always. a bug in FreeCAD I have to eliminate that
                        return #Todo:FIXME:Remove these two lines if freecad fix the bug
                    
                    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
                    
                    #TODO FIXME: NOT CORREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEECT
                    
                    self.done=True
                    Gui.Selection.clearSelection()
                    Gui.Selection.addSelection( App.ActiveDocument.getObject(obj.Name))
                    DefeaturingWB.oDefeaturingTools.osimplecopy_RH()
                    for i in self.WidgetObj:
                        i.hide()
                        i.__del__()
                    self.outer.coinWin.hide()
                    self.outer.coinWin.redraw()
                    for i in self.PathPointList:
                        App.ActiveDocument.removeObject(i.Name)
                    del self.outer.coinWin
                    self.outer.coinWin=None
                    App.ActiveDocument.removeObject(obj.Name)
                    App.ActiveDocument.removeObject(self.Section.Name)
                    App.ActiveDocument.recompute()
                    return 

            except Exception as err:
                App.Console.PrintError(
                    "'execute SmartLoft' Failed. " "{err}\n".format(err=str(err))
                )
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            "Pixmap": Design456Init.ICON_PATH + "SmartLoft.svg",
            "MenuText": "SmartLoft",
            "ToolTip": "Generate a SmartLoft",
        }

    def Activated(self):
        newObj = App.ActiveDocument.addObject("Part::FeaturePython", "SmartLoft")
        self.coinWin = win.Fr_CoinWindow()
        self.InnerObject=self.BaseSmartLoft(self,newObj)
        ViewProviderSmartLoft(newObj.ViewObject, "SmartLoft")
        App.ActiveDocument.recompute()

Gui.addCommand("Design456_SmartLoft", Design456_SmartLoft())
# -----------------------------------------------------------------------------

#dummy class 

class BaseSmartLoft:
    def ___init__(self):
        return Design456_SmartLoft.BaseSmartLoft

