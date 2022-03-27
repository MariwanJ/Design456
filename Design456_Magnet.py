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
from draftutils.translate import translate   #for translate

__updated__ = '2022-02-09 20:53:54'

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
                faced.errorDialog(errMessage)
                return
            App.ActiveDocument.openTransaction(translate("Design456", "Magnet"))
            sub1 = s[0]
            sub2 = s[1]
            face1 = faced.getObjectFromFaceName(sub1, sub1.SubElementNames[0])
            face2 = faced.getObjectFromFaceName(sub2, sub2.SubElementNames[0])
            #App.DraftWorkingPlane.alignToFace(face1)

            sub2.Object.Placement.Base = face1.Placement.Base #face1.CenterOfMass
            sub2.Object.Placement.Base.z= face1.CenterOfMass.z
            # This will fail if the surface doesn't have Rotation 
            if(hasattr(face1.Faces[0].Surface, "Rotation")):
                sub2.Object.Placement.Rotation = face1.Faces[0].Surface.Rotation
            else:
                # Don't know what todo . Don't let it be empty. 
                # TODO: Find a solution for this.
                sub2.Object.Placement.Rotation.Aixs = App.Vector(0, 0, 1)
                sub2.Object.Placement.Rotation.Angle = 0
            App.ActiveDocument.commitTransaction() # undo
            App.ActiveDocument.recompute()
            
        except Exception as err:
            App.Console.PrintError("'Magnet' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type,  exc_tb = sys.exc_info()
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