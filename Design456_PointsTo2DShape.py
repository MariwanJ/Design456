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

# Move an object to the location of the mouse click on another surface


class Design456_3Point:

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 3):
                # Two object must be selected
                errMessage = "Select two or more objects to use Magnet Tool"
                faced.getInfo(s).errorDialog(errMessage)
                return
            sub1 = Gui.Selection.getSelectionEx()[0]
            sub2 = Gui.Selection.getSelectionEx()[1]
            sub3=  Gui.Selection.getSelectionEx()[2]
            


            App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'Magnet' Failed. " 
                                   "{err}\n".format(err=str(err)))


    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Magnet.svg',
            'MenuText': 'Part_Magnet',
                        'ToolTip':	'Part Magnet'
        }


Gui.addCommand('Design456_3Point', Design456_3Point())
