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
# *	Author :Mariwan Jalal	 mariwan.jalal@gmail.com			           *
# ***************************************************************************
import os
import sys
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import Design456Init
import Design456_Tweak
import Design456_Magnet
import FACE_D as faced
import Design456_Extract
import Design456_Extrude
import Design456_loftOnDirection
import Design456_SplitObject

from PySide import QtCore, QtGui
import Design456_MakeFaceArray

class Design456_Part_Tools:
    list = ["Design456_Extrude",
            "Design456_Extract",
            "Design456_ExtrudeFace",
            "Design456_SplitObject",
            "Design456_loftOnDirection",
            "Design456_Part_Merge",
            "Design456_Part_Subtract",
            "Design456_Part_Intersect",
            "Design456_Part_Group",
            "Design456_Magnet",
            "Design456_Tweak",
            "Design456_Part_Shell",
            "Design456_Part_Fillet",
            "Design456_Part_Chamfer",
            "Design456_MakeFaceArray"
            

            ]

    """Design456 Part Tools Toolbar"""

    def GetResources(self):
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/Part_Tools.svg',
            'MenuText': 'Tools',
            'ToolTip':	'Tools'
        }

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
            return False
        else:
            return True

    def Activated(self):
        self.appendToolbar("Design456_Part_Tools", self.list)


# Merge
class Design456_Part_Merge:

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            temp = None
            if (len(s) < 2):
                # Two object must be selected
                errMessage = "Select two or more objects to Merge"
                faced.getInfo(s).errorDialog(errMessage)
                return
            allObjects = []
            for o in s:
                allObjects.append(App.ActiveDocument.getObject(o.ObjectName))

            newObj = App.activeDocument().addObject("Part::MultiFuse", "MergedTemp")
            newObj.Shapes = allObjects
            App.ActiveDocument.recompute()
            newObj.Refine = True
            App.ActiveDocument.recompute()
            # Make a simple copy
            newShape = Part.getShape(
                newObj, '', needSubElement=False, refine=False)
            NewJ = App.ActiveDocument.addObject(
                'Part::Feature', 'Merged').Shape = newShape
            App.ActiveDocument.recompute()

            # Remove Old objects
            for obj in allObjects:
                App.ActiveDocument.removeObject(obj.Name)
            App.ActiveDocument.removeObject(newObj.Name)
            App.ActiveDocument.recompute()
        except ImportError as err:
            App.Console.PrintError("'Part::Merge' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Merge.svg',
            'MenuText': 'Part_Merge',
            'ToolTip':	'Part Merge'
        }


Gui.addCommand('Design456_Part_Merge', Design456_Part_Merge())


# Subtract
class Design456_Part_Subtract:

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            temp = None
            if (len(s) < 2):
                # Two object must be selected
                errMessage = "Select two or more objects to Subtract"
                faced.getInfo(s).errorDialog(errMessage)
                return
            newObj = App.activeDocument().addObject("Part::Cut", "Subtract")
            newObj.Base = App.ActiveDocument.getObject(
                s[0].ObjectName)  # Target
            newObj.Tool = App.ActiveDocument.getObject(
                s[1].ObjectName)  # Subtracted shape/object
            App.ActiveDocument.recompute()
            newObj.Refine = True
            App.ActiveDocument.recompute()
            # Make a simple copy
            newShape = Part.getShape(
                newObj, '', needSubElement=False, refine=False)
            NewJ = App.ActiveDocument.addObject(
                'Part::Feature', 'Subtract').Shape = newShape
            App.ActiveDocument.recompute()
            # Remove Old objects
            allObjects = []
            for o in s:
                allObjects.append(App.ActiveDocument.getObject(o.ObjectName))
            for obj in allObjects:
                App.ActiveDocument.removeObject(obj.Name)
            App.ActiveDocument.removeObject(newObj.Name)
            App.ActiveDocument.recompute()
        except ImportError as err:
            App.Console.PrintError("'Part::Subtract' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Subtract.svg',
            'MenuText': 'Part_Subtract',
            'ToolTip':	'Part Subtract'
        }


Gui.addCommand('Design456_Part_Subtract', Design456_Part_Subtract())


# Intersect
class Design456_Part_Intersect:

    """Message box (error) """

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            temp = None
            if (len(s) < 2):
                # Two object must be selected
                errMessage = "Select two or more objects to Intersect"
                faced.getInfo(s).errorDialog(errMessage)
                return
            newObj = App.activeDocument().addObject("Part::MultiCommon", "tempIntersect")
            newObj.Shapes = [App.ActiveDocument.getObject(
                s[0].ObjectName), App.ActiveDocument.getObject(s[1].ObjectName)]
            App.ActiveDocument.recompute()
            # Make a simple copy
            newShape = Part.getShape(
                newObj, '', needSubElement=False, refine=False)
            NewJ = App.ActiveDocument.addObject(
                'Part::Feature', 'Intersect').Shape = newShape
            App.ActiveDocument.recompute()
            # Remove Old objects
            allObjects = []
            for o in s:
                allObjects.append(App.ActiveDocument.getObject(o.ObjectName))
            for obj in allObjects:
                App.ActiveDocument.removeObject(obj.Name)
            App.ActiveDocument.removeObject(newObj.Name)
            App.ActiveDocument.recompute()
        except ImportError as err:
            App.Console.PrintError("'Part::Intersect' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Intersect.svg',
            'MenuText': 'Part_Intersect',
            'ToolTip':	'Part Intersect'
        }


Gui.addCommand('Design456_Part_Intersect', Design456_Part_Intersect())
# Group


class Design456_Part_Group:

    """Message box (error) """

    def errorDialog(self, msg):
        # Create a simple dialog QMessageBox
        # The first argument indicates the icon used: one of QtGui.QMessageBox.{NoIcon, Information, Warning, Critical, Question}
        diag = QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Tools ', msg)
        diag.setWindowModality(QtCore.Qt.ApplicationModal)
        diag.exec_()

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            temp = None
            if (len(s) < 2):
                # Two object must be selected
                errMessage = "Select two or more objects to create a group"
                faced.getInfo(s).errorDialog(errMessage)
                return

            newObj = App.activeDocument().Tip = App.activeDocument().addObject('App::Part', 'Group')
            newObj.Label = 'Group'
            for obj_ in s:
                obj = App.ActiveDocument.getObject(obj_.ObjectName)
                newObj.addObject(obj)

            App.ActiveDocument.recompute()
        except ImportError as err:
            App.Console.PrintError("'Part::Part' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Group.svg',
            'MenuText': 'Part_Group',
            'ToolTip':	'Part Group'
        }


Gui.addCommand('Design456_Part_Group', Design456_Part_Group())


# Compund
class Design456_Part_Compound:

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            temp = None
            if (len(s) < 2):
                # Two object must be selected
                errMessage = "Select two or more objects to Merge"
                faced.getInfo(s).errorDialog(errMessage)
                return
            allObjects = []
            for o in s:
                allObjects.append(App.ActiveDocument.getObject(o.ObjectName))

            newObj = App.activeDocument().addObject("Part::Compound", "TempCompound")
            App.ActiveDocument.Compund.Links = allObjects
            # Make a simple copy
            newShape = Part.getShape(
                newObj, '', needSubElement=False, refine=False)
            NewJ = App.ActiveDocument.addObject(
                'Part::Feature', 'Compound').Shape = newShape

            # Remove Old objects
            for obj in allObjects:
                App.ActiveDocument.removeObject(obj.Name)
            App.ActiveDocument.removeObject(newObj.Name)

            App.ActiveDocument.recompute()
        except ImportError as err:
            App.Console.PrintError("'Part::Compund' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Compund.svg',
            'MenuText': 'Part_Compund',
            'ToolTip':	'Part Compound'
        }


Gui.addCommand('Design456_Part_Compound', Design456_Part_Compound())

# Shell


class Design456_Part_Shell:
    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            temp = None
            if (len(s) < 1):
                # Two object must be selected
                errMessage = "Select two or more objects to use Shell Tool"
                faced.getInfo(s).errorDialog(errMessage)
                return
            allObjects = []
            for o in s:
                allObjects.append(App.ActiveDocument.getObject(o.ObjectName))
            currentObj = App.ActiveDocument.getObject(s[0].ObjectName)
            currentObjLink = currentObj.getLinkedObject(True)
            thickObj = App.ActiveDocument.addObject(
                "Part::Thickness", "Thickness")
            thickObj.Value = QtGui.QInputDialog.getDouble(
                None, "Thickness", "Value:")[0]
            thickObj.Join = 0
            thickObj.Mode = 0
            thickObj.Intersection = False
            thickObj.SelfIntersection = False
            getfacename = faced.getInfo(s[0]).getFaceName()
            thickObj.Faces = (currentObj, getfacename,)
            App.ActiveDocument.recompute()
            NewJ = App.ActiveDocument.addObject(
                'Part::Feature', 'Shell').Shape = thickObj.Shape
            App.ActiveDocument.recompute()
            # Remove Old objects
            for obj in allObjects:
                App.ActiveDocument.removeObject(obj.Name)
            App.ActiveDocument.removeObject(thickObj.Name)

            App.ActiveDocument.recompute()
        except ImportError as err:
            App.Console.PrintError("'Part::Shell' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/PartDesign_Shell.svg',
            'MenuText': 'Part_Shell',
            'ToolTip':	'Part Shell'
        }


Gui.addCommand('Design456_Part_Shell', Design456_Part_Shell())


# fillet
class Design456_Part_Fillet:

    def Activated(self):
        s = Gui.Selection.getSelectionEx()
        if (len(s) < 1):
            # One object must be selected at least
            errMessage = "Select a face or an edge use Fillet"
            faced.getInfo(s).errorDialog(errMessage)
            return
        sub1 = Gui.Selection.getSelectionEx()[0]
        tempNewObj = App.ActiveDocument.addObject("Part::Fillet", "tempFillet")
        tempNewObj.Base = sub1.Object
        Radius = QtGui.QInputDialog.getDouble(None, "Radius", "Radius:")[0]
        names = sub1.SubElementNames
        EdgesToBeChanged=[]
        if (len(names) != 0):
            counter = 1
            for name in names:
                EdgesToBeChanged.append((int(name[len(name)-1]), Radius, Radius))
            tempNewObj.Edges = EdgesToBeChanged
            del EdgesToBeChanged
        else:
            errMessage = "Fillet failed. No subelements found"
            faced.getInfo(s).errorDialog(errMessage)
            return
        # Make a simple copy of the object
        App.ActiveDocument.recompute()

        newShape = Part.getShape(
            tempNewObj, '', needSubElement=False, refine=False)
        newObj = App.ActiveDocument.addObject(
            'Part::Feature', 'Fillet').Shape = newShape
        App.ActiveDocument.recompute()
        App.ActiveDocument.ActiveObject.Label = 'Fillet'

        App.ActiveDocument.removeObject(sub1.Object.Name)
        App.ActiveDocument.removeObject(tempNewObj.Name)
        App.ActiveDocument.recompute()

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Fillet.svg',
            'MenuText': 'Part_Fillet',
            'ToolTip':	'Part Fillet'
        }


Gui.addCommand('Design456_Part_Fillet', Design456_Part_Fillet())


# chamfer
class Design456_Part_Chamfer:

    def Activated(self):
        s = Gui.Selection.getSelectionEx()
        if (len(s) < 1):
            # One object must be selected at least
            errMessage = "Select a face or an edge use Chamfer"
            faced.getInfo(s).errorDialog(errMessage)
            return
        sub1 = Gui.Selection.getSelectionEx()[0]
        tempNewObj = App.ActiveDocument.addObject(
            "Part::Chamfer", "tempChamfer")
        tempNewObj.Base = sub1.Object
        Radius = QtGui.QInputDialog.getDouble(None, "Radius", "Radius:")[0]
        names = sub1.SubElementNames
        EdgesToBeChanged=[]
        if (len(names) != 0):
            counter = 1
            for name in names:
                EdgesToBeChanged.append((int(name[len(name)-1]), Radius, Radius))
            tempNewObj.Edges = EdgesToBeChanged
            del EdgesToBeChanged
        else:
            errMessage = "Chamfer failed. No subelements found"
            faced.getInfo(s).errorDialog(errMessage)
            return
        # Make a simple copy of the object
        App.ActiveDocument.recompute()
        newShape = Part.getShape(
            tempNewObj, '', needSubElement=False, refine=False)
        newObj = App.ActiveDocument.addObject(
            'Part::Feature', 'Chamfer').Shape = newShape
        App.ActiveDocument.recompute()
        App.ActiveDocument.ActiveObject.Label = 'Chamfer'

        App.ActiveDocument.removeObject(sub1.Object.Name)
        App.ActiveDocument.removeObject(tempNewObj.Name)
        App.ActiveDocument.recompute()

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Chamfer.svg',
            'MenuText': 'Part_Chamfer',
            'ToolTip':	'Part Chamfer'
        }


Gui.addCommand('Design456_Part_Chamfer', Design456_Part_Chamfer())

