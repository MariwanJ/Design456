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
from ThreeDWidgets.constant import BRUSHES
#TODO . FIXME

class ViewProviderBox:

    obj_name = "Paint"

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
        return (Design456Init.ICON_PATH + 'Design456_Paint.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

# ===========================================================================

#Create 2D Paints
class Paint:
    """
    Create a 2D Paints
    """
    def __init__(self, obj, color=FR_COLOR.FR_BLACK, _Size=10, _brushes:BRUSHES.BrushType=0, _sides=4):
        _join=True
        
        _tip = QT_TRANSLATE_NOOP("App::Property", "Types")
        obj.addProperty("App::PropertyBrushes", "Brushes",
                        "Paint", _tip).Brushes = _brushes
        
        _tip = QT_TRANSLATE_NOOP("App::Property", "Size")
        obj.addProperty("App::PropertyLength", "Size",
                        "Paint", _tip).Size = _Size
        
        _tip = QT_TRANSLATE_NOOP("App::Property", "Paint Join")
        obj.addProperty("App::PropertyLength", "Join",
                        "Paint", _tip).Join = _join
        
        _tip = QT_TRANSLATE_NOOP("App::Property", "Sides of the Brush")
        obj.addProperty("App::PropertyInteger", "Sides",
                        "Paint", _tip).Sides = _sides
        
        _tip = QT_TRANSLATE_NOOP("App::Property", "Make Face")
        obj.addProperty("App::PropertyBool", "MakeFace",
                        "Paint", _tip).MakeFace = True
        
        _tip = QT_TRANSLATE_NOOP("App::Property", "The area of this object")
        obj.addProperty("App::PropertyArea", "Area", "Paint", _tip).Area
        obj.Proxy = self

    def execute(self, obj):
        try:
            # Write how you draw this
            pass


        except Exception as err:
            App.Console.PrintError("'Paint' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return



class Design456_Paint:
    def Activated(self):
        try:
            pass
            App.ActiveDocument.recompute()
                
        except Exception as err:
            App.Console.PrintError("'PaintCommand' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return
            
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH+ 'Design456_Paint.svg',
                'MenuText': "Paint",
                'ToolTip': "Draw a Paint"}

Gui.addCommand('Design456_Paint', Design456_Paint())
