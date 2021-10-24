# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *                                                                         *
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
import sys
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft as _draft
import Part as _part
import Design456Init
import FACE_D as faced
from draftutils.translate import translate  # for translate


class GenCommandForPartUtils:
    localShapeName = ""

    typeOfCommand = 0

    def DoCommand(self, typeOfCommand):
        self.typeOfCommand = typeOfCommand
        self.localShapeName = ""
        if(self.typeOfCommand == 1):  # Common
            tempResult = App.ActiveDocument.addObject(
                "Part::MultiCommon", "tempWire")
            self.localShapeName = "Common2DShapes"
        elif(self.typeOfCommand == 2):  # Cut  - Subtract
            tempResult = App.ActiveDocument.addObject("Part::Cut", "tempWire")
            self.localShapeName = "Subtract2DShapes"
        elif(self.typeOfCommand == 3):  # merge or fusion
            tempResult = App.ActiveDocument.addObject(
                "Part::MultiFuse", "tempWire")
            self.localShapeName = "Combine2DShapes"
        return tempResult

    def makeIt(self, commandType):
        try:
            nObjects = []
            newShape = None
            simpl_cpy = None
            self.commandType = commandType
            selection = Gui.Selection.getSelectionEx()
            # Two object must be selected
            if(len(selection) < 2 or len(selection) > 2):
                errMessage = "Select two objects to use Common 2D Tool"
                faced.errorDialog(errMessage)
                return None
            else:
                nObjects.clear()
                GlobalPlacement = App.ActiveDocument.getObject(
                    selection[0].Object.Name).Placement
                for a2dobj in selection:
                    m = App.ActiveDocument.getObject(a2dobj.Object.Name)
                    f = App.ActiveDocument.addObject(
                        'Part::Extrusion', 'ExtrudeOriginal')
                    f.Base = App.ActiveDocument.getObject(m.Name)
                    f.DirMode = "Normal"
                    f.DirLink = a2dobj.Object

                    if faced.getDirectionAxis() == "+x":
                        f.Dir = (1, 0, 0)
                    elif faced.getDirectionAxis() == "-x":
                        f.Dir = (-1, 0, 0)
                    elif faced.getDirectionAxis() == "+y":
                        f.Dir = (0, 1, 0)
                    elif faced.getDirectionAxis() == "-y":
                        f.Dir = (0, -1, 0)
                    elif faced.getDirectionAxis() == "+z":
                        f.Dir = (0, 0, 1)
                    elif faced.getDirectionAxis() == "-z":
                        f.Dir = (0, 0, -1)

                    f.LengthFwd = 1.00
                    f.LengthRev = 0.0
                    f.Solid = True
                    f.Reversed = False
                    f.Symmetric = False
                    f.TaperAngle = 0.0
                    f.TaperAngleRev = 0.0
                    App.ActiveDocument.recompute()

                    # Make a simple copy of the object
                    newShape = _part.getShape(
                        f, '', needSubElement=False, refine=True)
                    newObj = App.ActiveDocument.addObject(
                        'Part::Feature', 'Extrude')
                    newObj.Shape = newShape
                    App.ActiveDocument.recompute()
                    App.ActiveDocument.ActiveObject.Label = f.Label
                    App.ActiveDocument.recompute()
                    App.ActiveDocument.removeObject(f.Name)
                    App.ActiveDocument.removeObject(m.Name)
                    App.ActiveDocument.recompute()
                    nObjects.append(newObj)

                # Create the common 3D shape
                tempResult = self.DoCommand(self.commandType)
                if(self.commandType == 1 or self.commandType == 3):
                    tempResult.Shapes = nObjects
                    tempResult.Refine = True
                elif(self.commandType == 2):
                    tempResult.Tool = nObjects[1]
                    tempResult.Base = nObjects[0]
                App.ActiveDocument.recompute()
                # Make a simple version
                newShape = _part.getShape(
                    tempResult, '', needSubElement=False, refine=False)
                simpl_cpy = App.ActiveDocument.addObject(
                    'Part::Feature', 'Shape')
                simpl_cpy.Shape = newShape  # simple version of the 3D common
                App.ActiveDocument.recompute()
                for name in nObjects:
                    App.ActiveDocument.removeObject(name.Name)
                App.ActiveDocument.removeObject(tempResult.Name)
                App.ActiveDocument.recompute()
            # Extract the face
            sh = simpl_cpy.Shape.copy()
            # sh.Placement = GlobalPlacement  # Result.Placement
            sh.Placement.Base.z = -1

            Gui.Selection.clearSelection()
            App.ActiveDocument.recompute()
            Gui.Selection.addSelection(App.ActiveDocument.Name, simpl_cpy.Name)
            s = Gui.Selection.getSelectionEx()[0]
            faceName = faced.SelectTopFace(simpl_cpy).Activated()

            newobj = App.ActiveDocument.addObject(
                "Part::Feature", self.localShapeName)
            newobj.Shape = sh.getElement(faceName)
            App.ActiveDocument.removeObject(simpl_cpy.Name)
            del nObjects[:]
        except Exception as err:
            App.Console.PrintError("'makeIt' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class Design456_CommonFace:

    def Activated(self):
        App.ActiveDocument.openTransaction(
            translate("Design456", "CommonFace"))
        cmp = GenCommandForPartUtils()
        cmp.makeIt(1)
        App.ActiveDocument.commitTransaction()  # undo reg.de here
        App.ActiveDocument.recompute()

    def GetResources(self):
        return{
            'Pixmap':   Design456Init.ICON_PATH + 'CommonFace.svg',
            'MenuText': 'CommonFace',
            'ToolTip':  'CommonFace between 2-2D Faces'
        }


Gui.addCommand('Design456_CommonFace', Design456_CommonFace())


# Subtract faces


class Design456_SubtractFaces:
    def Activated(self):
        App.ActiveDocument.openTransaction(
            translate("Design456", "CommonFace"))
        cmp = GenCommandForPartUtils()
        cmp.makeIt(2)
        App.ActiveDocument.commitTransaction()  # undo reg.de here
        App.ActiveDocument.recompute()

    def GetResources(self):
        return{
            'Pixmap':   Design456Init.ICON_PATH + 'SubtractFace.svg',
            'MenuText': 'Subtract Faces',
            'ToolTip':  'Subtract 2-2D Faces'
        }


Gui.addCommand('Design456_SubtractFaces', Design456_SubtractFaces())

# Combine two faces


class Design456_CombineFaces:
    def Activated(self):
        App.ActiveDocument.openTransaction(
            translate("Design456", "Combine Faces"))
        cmp = GenCommandForPartUtils()
        cmp.makeIt(3)
        App.ActiveDocument.commitTransaction()  # undo reg.de here
        App.ActiveDocument.recompute()

    def GetResources(self):
        return{
            'Pixmap':   Design456Init.ICON_PATH + 'CombineFaces.svg',
            'MenuText': 'Combine Face',
            'ToolTip':  'Combine 2-2D Faces'
        }


Gui.addCommand('Design456_CombineFaces', Design456_CombineFaces())
# Surface between two line


class Design456_Part_Surface:

    def Activated(self):
        try:
            App.ActiveDocument.openTransaction(
                translate("Design456", "Surface"))
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 2 or len(s) > 2):
                # Two object must be selected
                errMessage = "Select two edges or two wire to make a face or "
                faced.errorDialog(errMessage)
                return
            from textwrap import wrap
            for ss in s:
                word = ss.FullName
                if(word.find('Vertex') != -1):
                    # Two lines or curves or wires must be selected
                    errMessage = "Select two edges or two wires not Vertex"
                    faced.errorDialog(errMessage)
                    return

            newObj = App.ActiveDocument.addObject(
                'Part::RuledSurface', 'tempSurface')
            for sub in s:
                newObj.Curve1 = (s[0].Object, s[0].SubElementNames)
                newObj.Curve2 = (s[1].Object, s[1].SubElementNames)
            App.ActiveDocument.recompute()
            # Make a simple copy of the object
            newShape = _part.getShape(
                newObj, '', needSubElement=False, refine=True)
            tempNewObj = App.ActiveDocument.addObject(
                'Part::Feature', 'Surface')
            tempNewObj.Shape = newShape
            App.ActiveDocument.ActiveObject.Label = 'Surface'
            App.ActiveDocument.recompute()
            if tempNewObj.isValid() is False:
                App.ActiveDocument.removeObject(tempNewObj.Name)
                # Shape != OK
                errMessage = "Failed to fillet the objects"
                faced.errorDialog(errMessage)
            else:
                App.ActiveDocument.removeObject(newObj.Name)
                # Removing these could cause problem if the line is a part of an object
                # You cannot hide them either. TODO: I have to find a solution later
                # App.ActiveDocument.removeObject(s[0].Object.Name)
                # App.ActiveDocument.removeObject(s[1].Object.Name)
                s[0].Object.ViewObject.Visibility = False
                s[1].Object.ViewObject.Visibility = False
                App.ActiveDocument.commitTransaction()  # undo reg.de here
                App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'Part Surface' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Surface.svg',
            'MenuText': 'Part_Surface',
            'ToolTip':  'Part Surface'
        }


Gui.addCommand('Design456_Part_Surface', Design456_Part_Surface())


"""Design456 Part 2D Tools"""


class Design456_Part_2DToolsGroup:
    def __init__(self):
        return

    """Gui command for the group of 2D tools."""

    def GetCommands(self):
        """2D Face commands."""
        return ("Design456_CommonFace",
                "Design456_CombineFaces",
                "Design456_SubtractFaces",
                "Design456_Part_Surface",

                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools for modifying 2D Shapes")
        return {'Pixmap':  Design456Init.ICON_PATH + 'Design456_2DTools.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "2Dtools"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Part_2DToolsGroup", Design456_Part_2DToolsGroup())
