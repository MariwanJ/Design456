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

# This will be used to avoid user select wrong object, Body, Face, Edges or Vertices
import os
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore

__updated__ = '2021-12-31 08:56:37'

# Toolbar class

class Design456_SelectionGate:
    list = ["Design456_VertexSelectionMode",
            "Design456_EdgesSelectionMode",
            "Design456_FaceSelectionMode",
            "Design456_BodySelectionMode",
            "Design456_TopSideView",
            "Design456_BottomView",
            "Design456_LeftSideView",
            "Design456_RightSideView",
            "Design456_FrontSideView",
            "Design456_BackSideView"

            ]
    """Design456_SelectionGate"""

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + '2D_Drawing.svg',
            'MenuText': '2Ddrawing',
            'ToolTip':  '2Ddrawing'
        }

    def Activated(self):
        self.appendToolbar("Design456_SelectionGate", self.list)


# Allow Everything
class GateSelect0:
    def Activated(self):
        import FACE_D as faced
        try:
            Gui.Selection.removeSelectionGate()
        except Exception as err:
            App.Console.PrintError("'BodySelection Mode' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'SelectionModeBody.svg',
            'MenuText': 'Body Selection Mode',
            'ToolTip':  'Body Selection Mode'
        }


# Only Faces are allowed
class GateSelect1:
    def Activated(self):
        import FACE_D as faced
        try:
            filter = Gui.Selection.Filter(
                'SELECT Part::Feature SUBELEMENT Face')
            Gui.Selection.addSelectionGate(filter)
        except Exception as err:
            App.Console.PrintError("'FaceSelection Mode' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'SelectionModeFace.svg',
            'MenuText': 'FaceSelection Mode',
            'ToolTip':  'FaceSelection Mode'
        }


# Only Edges are allowed
class GateSelect2:
    def Activated(self):
        import FACE_D as faced
        try:
            filter = Gui.Selection.Filter(
                'SELECT Part::Feature SUBELEMENT Edge')
            Gui.Selection.addSelectionGate(filter)
        except Exception as err:
            App.Console.PrintError("'EdgeSelection Mode' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'SelectionModeEdges.svg',
            'MenuText': 'EdgeSelection Mode',
            'ToolTip':  'EdgeSelection Mode'
        }

# Only Vertices are allowed


class GateSelect3:
    def Activated(self):
        import FACE_D as faced
        try:

            filter = Gui.Selection.Filter(
                'SELECT Part::Feature SUBELEMENT Vertex')
            Gui.Selection.addSelectionGate(filter)
        except Exception as err:
            App.Console.PrintError("'VertexSelection Mode' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type,  exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'SelectionModeVertex.svg',
            'MenuText': 'VertexSelection Mode',
            'ToolTip':  'VertexSelection Mode'
        }


Gui.addCommand('Design456_BodySelectionMode',   GateSelect0())
Gui.addCommand('Design456_FaceSelectionMode',   GateSelect1())
Gui.addCommand('Design456_EdgesSelectionMode',  GateSelect2())
Gui.addCommand('Design456_VertexSelectionMode', GateSelect3())


""" Help on how to use this class 
'SELECT Part::Feature SUBELEMENT Edge',
        'SELECT Robot::RobotObject'
        
        You can also set an instance of SelectionFilter:
        filter = Gui.Selection.Filter('SELECT Part::Feature SUBELEMENT Edge')
        Gui.Selection.addSelectionGate(filter)
        
        And the most flexible approach is to write your own selection gate class
        that implements the method 'allow'
        class Gate:
          def allow(self,doc,obj,sub):
            return (sub[0:4] == 'Face')
        Gui.Selection.addSelectionGate(Gate())
"""
