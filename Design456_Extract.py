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
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore
import Draft
import Part


class Design456_Extract:
    """Extract the selected shapes from objects"""

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            for o in s:
                objName = o.ObjectName
                sh = o.Object.Shape.copy()
                if hasattr(o.Object, "getGlobalPlacement"):
                    gpl = o.Object.getGlobalPlacement()
                    sh.Placement = gpl
                for name in o.SubElementNames:
                    fullname = objName+"_"+name
                    newobj = o.Document.addObject("Part::Feature", fullname)
                    newobj.Shape = sh.getElement(name)
            App.ActiveDocument.recompute()
        except ImportError as err:
            App.Console.PrintError("'Design456_Extract' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return{
            'Pixmap':	Design456Init.ICON_PATH + '/Extract.svg',
            'MenuText': 'Extract',
            'ToolTip': 'Extract selected subshapes from objects'
        }


Gui.addCommand('Design456_Extract', Design456_Extract())
