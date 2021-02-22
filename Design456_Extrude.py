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
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore
import Draft
import Part
import FACE_D as faced
from time import time as _time, sleep as _sleep


class Design456_Extrude:
    def __init__(self):
        return

    def Activated(self):
        try:
            selection = Gui.Selection.getSelectionEx()
            if (len(selection) < 1):
                # An object must be selected
                errMessage = "Select a face to use Extrude"
                faced.getInfo(selection).errorDialog(errMessage)
                return
            m = selection[0].Object
            f = App.activeDocument().addObject('Part::Extrusion', 'ExtrudeOriginal')
            faceSelected= faced.getInfo(selection[0]).getFaceName()
            f.Base=m
            #f.Base = App.activeDocument().getObject(m.Name)
            f.DirMode = "Custom"
            f.DirLink =None
            # TODO: This "if" might not work always ?
        #	if(m.Placement.Rotation.Axis.x==1):
        #		f.Base.MapMode='ObjectYZ'
        #	elif (m.Placement.Rotation.Axis.y==1):
        #		f.Base.MapMode='ObjectXZ'
        #	elif (m.Placement.Rotation.Axis.z==1):
        #		f.Base.MapMode='ObjectXY'

            f.LengthFwd = QtGui.QInputDialog.getDouble( None, "Get length", "Length:",0,-10000.0,10000.0,2)[0]
            while(f.LengthFwd == 0):
                _sleep(.1)
                Gui.updateGui()
            f.LengthRev = 0.0
            f.Solid = True
            f.Reversed = False
            f.Symmetric = False
            f.TaperAngle = 0.0
            f.TaperAngleRev = 0.0

            # Make a simple copy of the object
            App.ActiveDocument.recompute()
            newShape = Part.getShape(f, '', needSubElement=False, refine=False)
            newObj = App.ActiveDocument.addObject(
                'Part::Feature', 'Extrude').Shape = newShape
            App.ActiveDocument.ActiveObject.Label = f.Label
            #if something went wrong .. delete all new objecst.
            if  newObj.isValid()==False:
                App.ActiveDocument.removeObject(newObj.Name)
                App.ActiveDocument.removeObject(f.Name)
                # Shape is not OK
                errMessage = "Failed to extrude the shape"
                faced.getInfo(m).errorDialog(errMessage)
            else:
                #Remove old objects 
                App.ActiveDocument.clearUndos()
                App.ActiveDocument.recompute()
                App.ActiveDocument.removeObject(f.Name)
                App.ActiveDocument.removeObject(m.Name)
                return
            App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'Design456_Extrude' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GuiViewFit(self):
        try:
            Gui.SendMsgToActiveView("ViewFit")
            self.timer.stop()
        except Exception as err:
            App.Console.PrintError("'Design456_Extrude_ViewFit' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Extrude.svg',
            'MenuText': 'Extrude',
                        'ToolTip':	'Extrude'
        }


Gui.addCommand('Design456_Extrude', Design456_Extrude())
