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
import os,sys
import FreeCAD as App
import FreeCADGui as Gui
import Draft as _draft
import Part as _part
import Design456Init
from pivy import coin
import FACE_D as faced
import math as _math
from PySide.QtCore import QT_TRANSLATE_NOOP

#TODO . FIXME

class ViewProviderBox:

    obj_name = "Hole"

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
        return (Design456Init.ICON_PATH + 'Design456_Hole.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

# ===========================================================================

#Create 3D Holes
class Hole:
    """
    Create a 3D Holes
    """
    def __init__(self, obj, _InnerRadius=10, _OuterRadius=20, _Angle=2*_math.pi, _Corners=40):
        _tip = QT_TRANSLATE_NOOP("App::Property", "Hole Angel")
        obj.addProperty("App::PropertyAngle", "Angle",
                        "Hole", _tip).Angle = _Angle
        _tip = QT_TRANSLATE_NOOP("App::Property", "Inner Radius of the Hole")
        obj.addProperty("App::PropertyLength", "InnerRadius",
                        "Hole", _tip).InnerRadius = _InnerRadius
        _tip = QT_TRANSLATE_NOOP("App::Property", "Outer Radius of the Hole")
        obj.addProperty("App::PropertyLength", "OuterRadius",
                        "Hole", _tip).OuterRadius = _OuterRadius
        _tip = QT_TRANSLATE_NOOP("App::Property", "Corners of the Hole")
        obj.addProperty("App::PropertyInteger", "Corners",
                        "Hole", _tip).Corners = _Corners
        _tip = QT_TRANSLATE_NOOP("App::Property", "Make Face")
        obj.addProperty("App::PropertyBool", "MakeFace",
                        "Hole", _tip).MakeFace = True
        _tip = QT_TRANSLATE_NOOP("App::Property", "The area of this object")
        obj.addProperty("App::PropertyArea", "Area", "Hole", _tip).Area
        obj.Proxy = self

    def execute(self, obj):
        try:
            pass
            

        except Exception as err:
            App.Console.PrintError("'Hole' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return



class Design456_Hole:
    def Activated(self):
        try:
            pass
            App.ActiveDocument.recompute()
                
        except Exception as err:
            App.Console.PrintError("'HoleCommand' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return
            
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH+ 'Design456_Hole.svg',
                'MenuText': "Hole",
                'ToolTip': "Draw a Hole"}

Gui.addCommand('Design456_Hole', Design456_Hole())
