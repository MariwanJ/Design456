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
# *	Author : __title__   = "Macro_Make_Arc_3_points"                       *
# *__author__  = "Mario52"                                                 *
# *__url__     = "http://www.freecadweb.org/index-fr.html"                 *
# *__version__ = "00.01"                                                   *
# *__date__    = "14/07/2016"                                              *
#                                                                          *
# * Modfied by: Mariwan Jalal	 mariwan.jalal@gmail.com	               *
# **************************************************************************
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Draft
import Part
import Design456Init
import FACE_D as faced

# Move an object to the location of the mouse click on another surface

class Design456_2Ddrawing:
    list = ["Design456_Arc3Points",
            "Design456_MultiPointToWireOpen",
            "Design456_MultiPointToWireClose",

            ]
    """Design456 Design456_2Ddrawing Toolbar"""

    def GetResources(self):
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/2D_Drawing.svg',
            'MenuText': '2Ddrawing',
            'ToolTip':	'2Ddrawing'
        }

    def IsActive(self):
        if App.ActiveDocument == None:
            return False
        else:
            return True

    def Activated(self):
        self.appendToolbar("Design456_2Ddrawing", self.list)


class Design456_Arc3Points:
    def Activated(self):
        try:
            selected = Gui.Selection.getSelectionEx()
            if (len(selected) < 3 or len(selected) > 3):
                # Two object must be selected
                errMessage = "Select two or more objects to useArc3Points Tool"
                faced.getInfo(selected).errorDialog(errMessage)
                return
            allSelected=[]
            for t in selected:
                allSelected.append(t.Object.Shape.Vertexes[0].Placement.Base)
            C1 = Part.Arc(App.Vector(allSelected[0]), App.Vector(allSelected[1]), App.Vector(allSelected[2]))
            S1 = Part.Shape([C1])
            W = Part.Wire(S1.Edges)
            Part.show(W)
            App.ActiveDocument.recompute()
            App.ActiveDocument.ActiveObject.Label = "Arc_3_Points"
            for n in selected:
                App.ActiveDocument.removeObject(n.ObjectName)
            del allSelected[:]
            App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'Arc3Points' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Arc3Points.svg',
            'MenuText': 'Arc3Points',
                        'ToolTip':	'Arc 3Points'
        }

Gui.addCommand('Design456_Arc3Points', Design456_Arc3Points())


class Design456_MultiPointToWireOpen:
    def Activated(self):
        try:
            selected = Gui.Selection.getSelectionEx()
            if (len(selected) < 2 ):
                # Two object must be selected
                errMessage = "Select two or more objects to use MultiPointsToLineOpen Tool"
                faced.getInfo(selected).errorDialog(errMessage)
                return
            allSelected=[]
            for t in selected:
                allSelected.append(t.Object.Shape.Vertexes[0].Placement.Base)
            Wire1 = Draft.makeWire(allSelected, closed=False)
            for n in selected:
                App.ActiveDocument.removeObject(n.Object.Name)
                
            del allSelected[:]
            App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'MultiPointToWire' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/MultiPointsToWireOpen.svg',
            'MenuText': 'Multi-Points To Line Open',
                        'ToolTip':	'Multi-Points To Line Open'
        }


Gui.addCommand('Design456_MultiPointToWireOpen', Design456_MultiPointToWireOpen())



class Design456_MultiPointToWireClose:
    def Activated(self):
        try:
            selected = Gui.Selection.getSelectionEx()
            if (len(selected) < 2):
                # Two object must be selected
                errMessage = "Select two or more objects to use MultiPointsToLineClose Tool"
                faced.getInfo(selected).errorDialog(errMessage)
                return
            allSelected=[]
            for t in selected:
                allSelected.append(t.Object.Shape.Vertexes[0].Placement.Base)

            Wire1 = Draft.makeWire(allSelected, closed=True)

            for n in selected:
                App.ActiveDocument.removeObject(n.Object.Name)
            #del allSelected[:]
            
            App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'MultiPointsToLineClosed' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/MultiPointsToWireClosed.svg',
            'MenuText': 'Multi-Points To Line Close',
                        'ToolTip':	'Multi-Points To Line Close'
        }


Gui.addCommand('Design456_MultiPointToWireClose', Design456_MultiPointToWireClose())
