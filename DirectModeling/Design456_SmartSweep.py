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
from tkinter import N

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


__updated__ = '2022-10-09 21:34:18'

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
        super().__init__(vectors, label)
        
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

            ArrowObject = userData.ballArrows
            events = userData.events
            linktocaller = userData.callerObject
            linktocaller.stepSizeDelta=Design456pref_var.MouseStepSize
            if type(events) != int:
                return
            linktocaller.endVector = App.Vector(ArrowObject.w_parent.w_lastEventXYZ.Coin_x,
                                                ArrowObject.w_parent.w_lastEventXYZ.Coin_y,
                                                ArrowObject.w_parent.w_lastEventXYZ.Coin_z)
            if(userData.ActiveAxis=="X"):
                clickwdgdNode = ArrowObject.w_parent.objectMouseClick_Coin3d(ArrowObject.w_parent.w_lastEventXYZ.pos,
                                                                        ArrowObject.w_pick_radius, ArrowObject.w_XarrowSeparator)
                linktocaller.w_vector[0].x=linktocaller.endVector.x
                
            elif (userData.ActiveAxis=="Y"):
                clickwdgdNode = ArrowObject.w_parent.objectMouseClick_Coin3d(ArrowObject.w_parent.w_lastEventXYZ.pos,
                                                                        ArrowObject.w_pick_radius, ArrowObject.w_YarrowSeparator)
                linktocaller.w_vector[0].y=linktocaller.endVector.y
            elif (userData.ActiveAxis=="Z"):
                clickwdgdNode = ArrowObject.w_parent.objectMouseClick_Coin3d(ArrowObject.w_parent.w_lastEventXYZ.pos,
                                                                        ArrowObject.w_pick_radius, ArrowObject.w_ZarrowSeparator)
                linktocaller.w_vector[0].z=linktocaller.endVector.z
            elif (userData.ActiveAxis=="A"):
                clickwdgdNode = ArrowObject.w_parent.objectMouseClick_Coin3d(ArrowObject.w_parent.w_lastEventXYZ.pos,
                                                                        ArrowObject.w_pick_radius, ArrowObject.w_ZarrowSeparator)
                linktocaller.w_vector[0]=linktocaller.endVector

            clickwdglblNode = ArrowObject.w_parent.objectMouseClick_Coin3d(ArrowObject.w_parent.w_lastEventXYZ.pos,
                                                                        ArrowObject.w_pick_radius, ArrowObject.w_widgetlblSoNodes)
            if clickwdgdNode is None and clickwdglblNode is None:
                return   # Nothing to do
            linktocaller.recreatePoint()
            linktocaller.lblExtrudeSize.setText("xLength Steps = " + str(linktocaller.stepSizeDelta))
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

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


class BaseSmartSweep:
    """ SmartSweep shape with a flexible capabilities 
    """
    Placement=None
    def __init__(self, obj,
                 _vertices=None, 
                 _section=None):
        obj.addProperty("App::PropertyLinkSub","Section","Sweep",
                        QT_TRANSLATE_NOOP("App::Property","Face to sweep")).Section=None
        obj.addProperty("App::PropertyVectorList","Points","Sweep",
                        QT_TRANSLATE_NOOP("App::Property","PathVertices")).PathVertices=[]        
        obj.addProperty("App::PropertyBoolean", "Apply", "Sweep").Apply=False

        self.Type = "SmartSweep"
        BaseSmartSweep.Placement = obj.Placement
        obj.Proxy = self

            
    def createObject(self):
        try:
            finalObj = None
 
            return finalObj

        except Exception as err:
            App.Console.PrintError("'createObject SmartSweep' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def execute(self, obj):
        try:
            self.Section=obj.Section
            self.Vertices=obj.Vertices
            self.Apply=obj.Apply
            
            objResult = self.createObject()            
            obj.Shape = objResult

        except Exception as err:
            App.Console.PrintError("'execute SmartSweep' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class Design456_SmartSweep:
    def __init__(self):
        self.WidgetObj=[]
        self.CoinThreeDWindow=None
        
        
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
        v = Gui.ActiveDocument.ActiveView
        App.ActiveDocument.recompute()
        faced.PartMover(v, newObj, deleteOnEscape=True)

        if self.CoinThreeDWindow is None:
            self.CoinThreeDWindow = win.Fr_CoinWindow()
        self.CoinThreeDWindow.addWidget(self.smartInd)
        mw = self.getMainWindow()
        self.CoinThreeDWindow.show()

        for i in range(0,len(newObj.Vertices)):
            self.WidgetObj.append(threeArrowBall(newObj.Vertices[i]))
            self.CoinThreeDWindow.addWidget(self.WidgetObj[0])
                
        #v = Gui.ActiveDocument.ActiveView
        #App.ActiveDocument.recompute()
        #faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_SmartSweep', Design456_SmartSweep())
#-----------------------------------------------------------------------------

