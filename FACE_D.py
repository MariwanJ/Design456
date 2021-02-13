# ***************************************************************************
# *                                                                         *
# *  This file is part of the Open Source Design456 Workbench - FreeCAD.    *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *																		   *
# *                                                                         *
# *  This library is free software; you can redistribute it and/or          *
# *  modify it under the terms of the GNU Lesser General Public             *
# *  License as published by the Free Software Foundation; either           *
# *  version 2 of the License, or (at your option) any later version.       *
# *                                                                         *
# *  This library is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# *  Lesser General Public License for more details.                        *
# *                                                                         *
# *  You should have received a copy of the GNU Lesser General Public       *
# *  License along with this library; if not, If not, see                   *
# *  <http://www.gnu.org/licenses/>.                                        *
# *                                                                         *
# *  Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# ***************************************************************************
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
# TODO: Do we need this? I must check it later


class FACE_D:
    def __init__(self, view):
        self.view = view
        v = Gui.activeDocument().activeView()

    def getDirectionAxis(self):
        try:
            s = Gui.Selection.getSelectionEx()
            obj = s[0]
            faceSel = obj.SubObjects[0]
            dir = faceSel.normalAt(0, 0)
            if dir.z == 1:
                return "z"
            elif dir.y == 1:
                return "y"
            else:
                return "x"
        except ImportError as err:
            App.Console.PrintError("'FACE_D.getDirectionAxis' Failed. "
                                   "{err}\n".format(err=str(err)))

    def MousePosition(self, info):
        try:
            down = (info["State"] == "DOWN")
            pos = info["Position"]
            # if (down):
            FreeCAD.Console.PrintMessage(
                "Clicked on position: ("+str(pos[0])+", "+str(pos[1])+")\n")
            pnt = self.view.getPoint(pos)
            FreeCAD.Console.PrintMessage(
                "World coordinates: " + str(pnt) + "\n")
            info = self.view.getObjectInfo(pos)
            FreeCAD.Console.PrintMessage("Object info: " + str(info) + "\n")
            o = ViewObserver(v)
            c = v.addEventCallback("SoMouseButtonEvent", o.logPosition)
            return pnt
        except ImportError as err:
            App.Console.PrintError("'FACE_D.getDirectionAxis' Failed. "
                                   "{err}\n".format(err=str(err)))

    def ExtractFace(self):
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
            return self.newobj
            #o.Object.ViewObject.Visibility = False
        except ImportError as err:
            App.Console.PrintError("'FACE_D.ExtractFace' Failed. "
                                   "{err}\n".format(err=str(err)))


#This class is from A2P WB modified by Mariwan
class PartMover:
    def __init__(self, view, obj):
        self.obj = obj
        self.initialPosition = self.obj.Placement.Base
        self.view = view
        self.callbackMove = self.view.addEventCallback("SoLocation2Event",self.moveMouse)
        self.callbackClick = self.view.addEventCallback("SoMouseButtonEvent",self.clickMouse)
        self.callbackKey = self.view.addEventCallback("SoKeyboardEvent",self.KeyboardEvent)
        self.objectToDelete = None # object reference when pressing the escape key
        
    def moveMouse(self, info):
        newPos = self.view.getPoint( *info['Position'] )
        self.obj.Placement.Base = newPos
        
    def removeCallbacks(self):
        self.view.removeEventCallback("SoLocation2Event",self.callbackMove)
        self.view.removeEventCallback("SoMouseButtonEvent",self.callbackClick)
        self.view.removeEventCallback("SoKeyboardEvent",self.callbackKey)
        
    def clickMouse(self, info):
        if info['Button'] == 'BUTTON1' and info['State'] == 'DOWN':
            #if not info['ShiftDown'] and not info['CtrlDown']: #struggles within Inventor Navigation
            if not info['ShiftDown']:
                self.removeCallbacks()
                App.ActiveDocument.recompute()
            elif info['ShiftDown']:
                self.obj = duplicateImportedPart(self.obj)
                self.deleteOnEscape = True
                
    def KeyboardEvent(self, info):
        if info['State'] == 'UP' and info['Key'] == 'ESCAPE':
            self.removeCallbacks()
            if not self.deleteOnEscape:
                self.obj.Placement.Base = self.initialPosition
            else:
                self.objectToDelete = self.obj #This can be asked by a timer in a calling func...
                #This causes a crash in FC0.19/Qt5/Py3             
                #FreeCAD.activeDocument().removeObject(self.obj.Name)
#===============================================================================
toolTip = \
'''
Move the selected part.

Select a part and hit this
button. The part can be moved
around by mouse.

If the part is constrained, it
will jump back by next solving
of the assembly.
'''