# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *																		    *
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
import Design456Init
import FACE_D as faced

"""Design456 Part Utils"""


class Design456_Part_Utils:
    list = ["Design456_CommonFace",
            "Design456_CombineFaces",
            "Design456_SubtractFaces",
            "Design456_Part_Surface"


            ]

    def GetResources(self):
        return{
            'Pixmap':	Design456Init.ICON_PATH + '/Part_Utils.svg',
            'MenuText': 'Box',
            'ToolTip': 'Box'
        }

    def IsActive(self):
        if App.ActiveDocument == None:
            return False
        else:
            return True

    def Activated(self):
        self.appendToolbar("Design456_Part_Utils", Design456_Part_Utils())


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
            tempResult = App.ActiveDocument.addObject("Part::Fuse", "tempWire")
            self.localShapeName = "Combine2DShapes"
        return tempResult

    def makeIt(self, commandType):
        self.commandType = commandType
        selection = Gui.Selection.getSelectionEx()
        # Two object must be selected
        if(len(selection) < 2 or len(selection) > 2):
            errMessage = "Select two objects to use Common 2D Tool"
            faced.getInfo(selection).errorDialog(errMessage)
        else:
            nObjects = []
            nObjects.clear()
            GlobalPlacement = App.activeDocument().getObject(
                selection[0].Object.Name).Placement
            for a2dobj in selection:
                m = App.activeDocument().getObject(a2dobj.Object.Name)
                f = App.activeDocument().addObject('Part::Extrusion', 'ExtrudeOriginal')
                f.Base = App.activeDocument().getObject(m.Name)
                f.DirMode = "Normal"
                f.DirLink = a2dobj.Object
                f.LengthFwd = 1.00
                f.LengthRev = 0.0
                f.Solid = True
                f.Reversed = False
                f.Symmetric = False
                f.TaperAngle = 0.0
                f.TaperAngleRev = 0.0
                App.ActiveDocument.recompute()

                # Make a simple copy of the object
                newShape = Part.getShape(
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

            tempResult = self.DoCommand(self.commandType)
            if(commandType == 1):
                tempResult.Shapes = nObjects
            elif(commandType == 2 or commandType == 3):
                tempResult.Tool = nObjects[1]
                tempResult.Base = nObjects[0]
            App.ActiveDocument.recompute()
            newShape = Part.getShape(
                tempResult, '', needSubElement=False, refine=True)
            Result = App.ActiveDocument.addObject('Part::Feature', 'Shape')
            Result.Shape = newShape
            for name in nObjects:
                App.ActiveDocument.removeObject(name.Name)
            App.ActiveDocument.removeObject(tempResult.Name)
            Gui.Selection.clearSelection()
            App.ActiveDocument.recompute()
            Gui.Selection.addSelection(App.ActiveDocument.Name, Result.Name)
            s = Gui.Selection.getSelectionEx()[0]
            obFace = faced.getInfo(s)
            faceName = obFace.SelectTopFace()
            # Extract the face
            sh = Result.Shape.copy()
            sh.Placement = GlobalPlacement  # Result.Placement
            sh.Placement.Base.z = -1
            newobj = Result.Document.addObject(
                "Part::Feature", self.localShapeName)
            newobj.Shape = sh.getElement(faceName)
            App.ActiveDocument.removeObject(Result.Name)
            del nObjects[:]


class Design456_CommonFace:

    def Activated(self):
        cmp = GenCommandForPartUtils()
        cmp.makeIt(1)
        App.ActiveDocument.recompute()
        # extract code here

    def GetResources(self):
        return{
            'Pixmap':	Design456Init.ICON_PATH + '/CommonFace.svg',
            'MenuText': 'CommonFace',
            'ToolTip':	'CommonFace between 2-2D Faces'
        }


Gui.addCommand('Design456_CommonFace', Design456_CommonFace())


# Subtract faces


class Design456_SubtractFaces:
    def Activated(self):
        cmp = GenCommandForPartUtils()
        cmp.makeIt(2)
        App.ActiveDocument.recompute()

    def GetResources(self):
        return{
            'Pixmap':	Design456Init.ICON_PATH + '/SubtractFace.svg',
            'MenuText': 'Subtract Faces',
            'ToolTip':	'Subtract 2-2D Faces'
        }


Gui.addCommand('Design456_SubtractFaces', Design456_SubtractFaces())

# Combine two faces


class Design456_CombineFaces:
    def Activated(self):
        cmp = GenCommandForPartUtils()
        cmp.makeIt(3)
        App.ActiveDocument.recompute()

    def GetResources(self):
        return{
            'Pixmap':	Design456Init.ICON_PATH + '/CombineFaces.svg',
            'MenuText': 'Combine Face',
            'ToolTip':	'Combine 2-2D Faces'
        }


Gui.addCommand('Design456_CombineFaces', Design456_CombineFaces())
# Surface between two line


class Design456_Part_Surface:

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 2 or len(s) > 2):
                # Two object must be selected
                errMessage = "Select two edges or two wire to make a face or "
                faced.getInfo(s).errorDialog(errMessage)
                return
            from textwrap import wrap
            for ss in s:
                word = ss.FullName
                if(word.find('Vertex') != -1):
                    # Two lines or curves or wires must be selected
                    errMessage = "Select two edges or two wires not Vertex"
                    faced.getInfo(s).errorDialog(errMessage)
                    return

            newObj = App.ActiveDocument.addObject(
                'Part::RuledSurface', 'tempSurface')
            for sub in s:
                newObj.Curve1 = (s[0].Object, s[0].SubElementNames)
                newObj.Curve2 = (s[1].Object, s[1].SubElementNames)
            App.ActiveDocument.recompute()
            # Make a simple copy of the object
            newShape = Part.getShape(
                newObj, '', needSubElement=False, refine=True)
            tempNewObj = App.ActiveDocument.addObject(
                'Part::Feature', 'Surface')
            tempNewObj.Shape = newShape
            App.ActiveDocument.ActiveObject.Label = 'Surface'
            App.ActiveDocument.recompute()
            if tempNewObj.isValid() == False:
                App.ActiveDocument.removeObject(tempNewObj.Name)
                # Shape is not OK
                errMessage = "Failed to fillet the objects"
                faced.getInfo(s).errorDialog(errMessage)
            else:
                App.ActiveDocument.removeObject(newObj.Name)
                #Removing these could cause problem if the line is a part of an object
                #You cannot hide them eithe. TODO: I have to find a solution later 
                #App.ActiveDocument.removeObject(s[0].Object.Name)
                #App.ActiveDocument.removeObject(s[1].Object.Name)
                s[0].Object.ViewObject.Visibility=False
                s[1].Object.ViewObject.Visibility=False
                
                App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'Part Surface' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Surface.svg',
            'MenuText': 'Part_Surface',
            'ToolTip':	'Part Surface'
        }


Gui.addCommand('Design456_Part_Surface', Design456_Part_Surface())
