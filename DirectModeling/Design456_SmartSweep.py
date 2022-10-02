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
import FreeCAD as App
import FreeCADGui as Gui
from pivy import coin
import FACE_D as faced
from PySide.QtCore import QT_TRANSLATE_NOOP
from typing import List
import Design456Init
from PySide import QtGui, QtCore
from ThreeDWidgets.fr_arrow_widget import Fr_Arrow_Widget
from ThreeDWidgets import fr_arrow_widget
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from draftutils.translate import translate  # for translation
import math
from ThreeDWidgets import fr_label_draw



__updated__ = '2022-10-02 21:51:49'

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

    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'SmartSweep.svg',
                'MenuText': "SmartSweep",
                'ToolTip': "Generate a SmartSweep"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "SmartSweep")
        plc = App.Placement()
        plc.Base = App.Vector(0, 0, 0)
        plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        newObj.Placement = plc

        BaseSmartSweep(newObj)
        ViewProviderSmartSweep(newObj.ViewObject, "SmartSweep")
        v = Gui.ActiveDocument.ActiveView
        App.ActiveDocument.recompute()
        faced.PartMover(v, newObj, deleteOnEscape=True)


Gui.addCommand('Design456_SmartSweep', Design456_SmartSweep())
#-----------------------------------------------------------------------------

