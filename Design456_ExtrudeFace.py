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
# ***************************************************************************
import os,sys
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import FACE_D as faced
import Design456_Extract as face_extract
import Design456_Part_Tools as tools

class Design456_ExtrudeFace:
    def __init__(self):
        return

    def Activated(self):
        try:

            s = Gui.Selection.getSelectionEx()
            if (len(s) < 1):
                # An object must be selected
                errMessage = "Select an object to use Extrude Face"
                faced.getInfo(s).errorDialog(errMessage)
                return
            lengthForward = QtGui.QInputDialog.getDouble(
                None, "Get value", "Input:", 0, -10000.0, 10000.0, 2)[0]
            if(lengthForward == 0):
                return  # nothing to do here

            objName = s[0].ObjectName
            sh = s[0].Object.Shape.copy()
            if hasattr(s[0].Object, "getGlobalPlacement"):
                gpl = s[0].Object.getGlobalPlacement()
                sh.Placement = gpl
            name = s[0].SubElementNames[0]
            fullname = objName+"_"+name  # Name of the face extracted
            newobj = s[0].Document.addObject("Part::Feature", fullname)
            newobj.Shape = sh.getElement(name)
            selection = newobj  # The face extraced
            activeSel = Gui.Selection.getSelection(App.ActiveDocument.Name)
            Gui.Selection.removeSelection(activeSel[0])
            # Select the face extracted before
            Gui.Selection.addSelection(selection)
            App.ActiveDocument.recompute()
            m = App.activeDocument().getObject(fullname)
            f = App.activeDocument().addObject(
                'Part::Extrusion', 'ExtrudeFace')	  # Add extrusion
            f.Base = newobj				# App.activeDocument().getObject(fullname)
            f.DirMode = "Normal"
            f.DirLink = None
            f.LengthFwd = lengthForward
            f.LengthRev = 0.0
            f.Solid = True
            f.Reversed = False
            f.Symmetric = False
            f.TaperAngle = 0.0
            f.TaperAngleRev = 0.0
            App.ActiveDocument.recompute()
            newPart_ = App.ActiveDocument.addObject(
                'Part::Feature', f.Name+'N')
            newPart_.Shape = Part.getShape(
                f, '', needSubElement=False, refine=False)
            if newPart_.isValid() == False:
                App.ActiveDocument.removeObject(newPart_.Name)
                App.ActiveDocument.removeObject(f.Name)
                # Shape is not OK
                errMessage = "Failed to extrude the Face"
                faced.getInfo(m).errorDialog(errMessage)
            else:
                # remove old objects
                App.ActiveDocument.removeObject(f.Name)
                App.ActiveDocument.removeObject(m.Name)
                # This will not work for split objects as they are not two separate objects.2021-02-22
                # Make the two objects merged
                obj1 = App.ActiveDocument.getObject(s[0].ObjectName)
                obj2 = newPart_
                selections = Gui.Selection.getSelectionEx()
                for i in selections:
                    Gui.Selection.removeSelection(selections)
                    Gui.Selection.addSelection(obj1)
                    Gui.Selection.addSelection(obj2)
                    Gui.runCommand('Design456_Part_Merge', 0)
            App.ActiveDocument.recompute()

            return
        except Exception as err:
            App.Console.PrintError("'ExtrudeFace' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/ExtrudeFace.svg',
            'MenuText': 'ExtrudeFace',
                        'ToolTip':	'ExtrudeFace'
        }


Gui.addCommand('Design456_ExtrudeFace', Design456_ExtrudeFace())
