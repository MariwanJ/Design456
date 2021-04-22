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
import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import Draft
import Part
import Design456Init
import FACE_D as faced

# Move an object to the location of the mouse click on another surface
class Design456_Magnet:
    """ Magnet tool. 
        Use this tool to move any object to any face.
        Select face1 (destination) 
        Select face2 (Source - Moved object)
        Click the icon .. Done
    """
    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 2):
                # Two object must be selected
                errMessage = "Select two or more objects to use Magnet Tool"
                faced.getInfo(s).errorDialog(errMessage)
                return
            sub1 = Gui.Selection.getSelectionEx()[0]
            sub2 = Gui.Selection.getSelectionEx()[1]
            face1 = faced.getInfo(sub1).getObjectFromFaceName(
                sub1.SubElementNames[0])
            face2 = faced.getInfo(sub2).getObjectFromFaceName(
                sub2.SubElementNames[0])

            sub2.Object.Placement.Base = face1.CenterOfMass
            sub2.Object.Placement.Rotation = face1.Faces[0].Surface.Rotation
            sub2.Object.Placement.Rotation.Q = face1.Faces[0].Surface.Rotation.Q
            App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'Magnet' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH +'Part_Magnet.svg',
            'MenuText': 'Part_Magnet',
                        'ToolTip':  'Part Magnet'
        }


Gui.addCommand('Design456_Magnet', Design456_Magnet())
Design456_Magnet.__doc__ = """Magnet tool: 
                            Use this tool for moving any object by
                            Selecting face1 of obj1 (destination) 
                            Selecting face2 of obj2 (Source - Moved object)
                            Click the 'Magnet' icon .. Done
                            """