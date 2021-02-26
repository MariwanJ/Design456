# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *																		   *
# *	This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *																		   *
# *	Copyright (C) 2021													   *
# *																		   *
# *																		   *
# *	This library is free software; you can redistribute it and/or		   *
# *	modify it under the terms of the GNU Lesser General Public			   *
# *	License as published by the Free Software Foundation; either		   *
# *	version 2 of the License, or (at your option) any later version.	   *
# *																		   *
# *	This library is distributed in the hope that it will be useful,		   *
# *	but WITHOUT ANY WARRANTY; without even the implied warranty of		   *
# *	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU	   *
# *	Lesser General Public License for more details.						   *
# *																		   *
# *	You should have received a copy of the GNU Lesser General Public	   *
# *	License along with this library; if not, If not, see				   *
# *	<http://www.gnu.org/licenses/>.										   *
# *																		   *
# *	Author : Mariwan Jalal	 mariwan.jalal@gmail.com					   *
# **************************************************************************
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Draft
import Part
import Design456Init
import FACE_D as faced

# Toolbar class
"""Design456_Alignment"""

class Design456_Alignment:
    list = ["Design456_AlignToPlane",
            "Design456_TopSideView",
            "Design456_BottomView",
            "Design456_LeftSideView",
            "Design456_RightSideView",
            "Design456_FrontSideView",
            "Design456_BackSideView"
            

            ]

    def Activated(self):
        self.appendToolbar("Design456_Alignment", self.list)

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/Alignments.svg',
            'MenuText': 'Alignments',
            'ToolTip':	'Alignments'
        }


# Object Alignment
class Design456_AlignFlatToPlane:
    def Activated(self):
        try:
            Selectedobjects = Gui.Selection.getSelectionEx()
            #This must be modified
            for eachObj in Selectedobjects:
                eachObj.Object.Placement.Base.z = 0.0
                
        except Exception as err:
            App.Console.PrintError("'Design456_Extract' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/AlignToPlane.svg',
            'MenuText': '2Ddrawing',
            'ToolTip':	'2Ddrawing'
        }
        
Gui.addCommand('Design456_AlignToPlane',Design456_AlignFlatToPlane())

# Plane Alignments

#Top
class Design456_TopSideView:
    def Activated(self):
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, 1.0), 0.0)
        Gui.activeDocument().activeView().viewTop()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/TopSideView.svg',
            'MenuText': 'Top Side View',
            'ToolTip':	'Top Side View'
            }

Gui.addCommand('Design456_TopSideView',Design456_TopSideView())

#Bottom View
class Design456_BottomView:
    def Activated(self):
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, -1.0), 0.0)
        Gui.activeDocument().activeView().viewBottom()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/BottomSideView.svg',
            'MenuText': 'Bottom Side View',
            'ToolTip':	'Bottom Side View'
            }

Gui.addCommand('Design456_BottomView',Design456_BottomView())

#Left
class Design456_LeftSideView:
    def Activated(self):
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(1.0,0.0 , 0.0), 0.0)
        Gui.activeDocument().activeView().viewLeft()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/LeftSideView.svg',
            'MenuText': 'Left Side View',
            'ToolTip':	'Left Side View'
            }

Gui.addCommand('Design456_LeftSideView',Design456_LeftSideView())

#Right
class Design456_RightSideView:
    def Activated(self):
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(-1.0, 0.0, 0.0), 0.0)
        Gui.activeDocument().activeView().viewRight()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/RightSideView.svg',
            'MenuText': 'Right Side View',
            'ToolTip':	'Right Side View'
            }

Gui.addCommand('Design456_RightSideView',Design456_RightSideView())

#Front
class Design456_FrontSideView:
    def Activated(self):
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0,1.0, 0.0), 0.0)
        Gui.activeDocument().activeView().viewFront()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/FrontSideView.svg',
            'MenuText': 'Front Side View',
            'ToolTip':	'Front Side View'
            }

Gui.addCommand('Design456_FrontSideView',Design456_FrontSideView())

#Back
class Design456_BackSideView:
    def Activated(self):
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, -1.0, 0.0), 0.0)
        Gui.activeDocument().activeView().viewRear()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/BacktSideView.svg',
            'MenuText': 'Backside View',
            'ToolTip':	'BackSide View'
            }

Gui.addCommand('Design456_BackSideView',Design456_BackSideView())
