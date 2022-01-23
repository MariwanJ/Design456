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
# ***************************************************************************
import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore
import Draft
import Part
import FACE_D as faced
from time import time as _time, sleep as _sleep
from draftutils.translate import translate  # for translation
import math

__updated__ = '2022-01-23 12:56:35'

class Design456_Extrude:
    
    def ExtractThenExtrude(self):
        try:

            s = Gui.Selection.getSelectionEx()
            if (len(s) < 1):
                # An object must be selected
                errMessage = "Select an object to use Extrude Face"
                faced.errorDialog(errMessage)
                return
            lengthForward =- QtGui.QInputDialog.getDouble(
                None, "Length of Extrusion", "Input:", 0, -10000.0, 10000.0, 2)[0]
            if(lengthForward ==0):
                return  # nothing to do here

            objName = s[0].ObjectName
            App.ActiveDocument.openTransaction(translate("Design456","Extrude a face"))
            sh = s[0].Object.Shape.copy()
            if hasattr(s[0].Object, "getGlobalPlacement"):
                gpl = s[0].Object.getGlobalPlacement()
                sh.Placement = gpl
            name = s[0].SubElementNames[0]
            fullname = objName+"_"+name  # Name of the face extracted
            newobj = s[0].Document.addObject("Part::Feature", fullname)
            newobj.Shape = sh.getElement(name)
            selection = newobj  # The face extracted
            activeSel = Gui.Selection.getSelection(App.ActiveDocument.Name)
            Gui.Selection.removeSelection(activeSel[0])
            # Select the face extracted before
            Gui.Selection.addSelection(selection)
            App.ActiveDocument.recompute()
            m = App.ActiveDocument.getObject(fullname)
            f = App.ActiveDocument.addObject(
                'Part::Extrusion', 'ExtrudeFace')     # Add extrusion
            f.Base = newobj             # App.ActiveDocument.getObject(fullname)
            f.DirMode = "Normal"
            f.DirLink = None
            f.LengthFwd = lengthForward
            f.LengthRev = 0.0
            f.Solid = True
            f.Reversed = False
            f.Symmetric = False
            f.TaperAngle = 0.0
            f.TaperAngleRev = 0.0
            yL = newobj.Shape.Faces[0].CenterOfMass
            uv = newobj.Shape.Faces[0].Surface.parameter(yL)
            nv = newobj.Shape.Faces[0].normalAt(uv[0], uv[1])
            direction = yL.sub(nv + yL)
            direction= App.Vector(round(direction.x,2),round(direction.y,2),round(direction.z,2) )
            print(direction,"direction" )
            r = App.Rotation(App.Vector(0, 0, 0), direction)
            if (abs(f.Dir.x) != 1 or abs(f.Dir.y) != 1 or abs(f.Dir.z) != 1):
                f.DirMode = "Custom"
            f.Dir=direction
            App.ActiveDocument.recompute()
            newPart_ = App.ActiveDocument.addObject(
                'Part::Feature', f.Name+'N')
            newPart_.Shape = Part.getShape(
                f, '', needSubElement=False, refine=False)
            if newPart_.isValid() is False:
                App.ActiveDocument.removeObject(newPart_.Name)
                App.ActiveDocument.removeObject(f.Name)
                # Shape != OK
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
            App.ActiveDocument.commitTransaction() #undo reg.
            App.ActiveDocument.recompute()

            return
        except Exception as err:
            App.Console.PrintError("'ExtrudeFace' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Activated(self):
        try:
            selection = Gui.Selection.getSelectionEx()
            if (len(selection) < 1):
                # An object must be selected
                errMessage = "Select a face to use Extrude"
                faced.errorDialog(errMessage)
                return
            if not isinstance(selection[0].Object.Shape, Part.Face):
                self.ExtractThenExtrude()
            else:
                App.ActiveDocument.openTransaction(
                    translate("Design456", "Extrude"))
                m = selection[0].Object
                f = App.ActiveDocument.addObject(
                    'Part::Extrusion', 'ExtrudeOriginal')
                f.Base = m
                # F.DirMode causes too many failure. Some faces needs custom, other needs Normal.
                # Difficult to know when you use each of them.
                f.DirMode = "Normal"  # Don't use Custom as it leads to PROBLEM!
                f.DirLink = None  # Above statement != always correct. Some faces require 'custom'

                
                # Extrude must get a negative number ???
                f.LengthFwd =- (QtGui.QInputDialog.getDouble(
                    None, "Length of Extrusion", "Length:", 0, -10000.0, 10000.0, 2)[0])
                while(f.LengthFwd == 0):
                    _sleep(.1)
                    Gui.updateGui()
                f.LengthRev = 0.0
                f.Solid = True
                f.Reversed = False
                f.Symmetric = False
                f.TaperAngle = 0.0
                f.TaperAngleRev = 0.0
                # section direction
                yL = m.Shape.Faces[0].CenterOfMass
                uv = m.Shape.Faces[0].Surface.parameter(yL)
                nv = m.Shape.Faces[0].normalAt(uv[0], uv[1])
                direction = yL.sub(nv + yL)
                direction= App.Vector(round(direction.x,2),round(direction.y,2),round(direction.z,2) )
                f.Dir=direction
                print(direction,"direction" )
                r = App.Rotation(App.Vector(0, 0, 0), direction)

                f.Dir = direction #selection[0].Object.Shape.normalAt(0, 0)  # Normal line
                if (f.Dir.x != 1 or f.Dir.y != 1 or f.Dir.z != 1):
                    f.DirMode = "Custom"
                # Make a simple copy of the object
                App.ActiveDocument.recompute()
                newShape = Part.getShape(f, '', needSubElement=False, refine=False)
                newObj = App.ActiveDocument.addObject(
                    'Part::Feature', 'Extrude').Shape = newShape
                App.ActiveDocument.recompute()
                # if something went wrong .. delete all new objects.
                if newObj.isValid() is False:
                    App.ActiveDocument.removeObject(newObj.Name)
                    App.ActiveDocument.removeObject(f.Name)
                    # Shape != OK
                    errMessage = "Failed to extrude the shape"
                    faced.getInfo(m).errorDialog(errMessage)
                else:
                    # Remove old objects
                    # App.ActiveDocument.clearUndos()
                    App.ActiveDocument.recompute()
                    App.ActiveDocument.removeObject(f.Name)
                    App.ActiveDocument.removeObject(m.Name)
                    return
                App.ActiveDocument.commitTransaction()  # undo reg.
                App.ActiveDocument.recompute()
                
        except Exception as err:
            App.Console.PrintError("'Design456_Extrude' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
        except Exception as err:
            App.Console.PrintError("'Design456_Extrude_ViewFit' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Extrude.svg',
            'MenuText': 'Extrude',
                        'ToolTip':  'Extrude'
        }


Gui.addCommand('Design456_Extrude', Design456_Extrude())
