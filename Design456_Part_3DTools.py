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
# * Author :Mariwan Jalal    mariwan.jalal@gmail.com                       *
# ***************************************************************************
import sys
import os
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import Design456Init
import FACE_D as faced
import Design456_loftOnDirection
import Design456_Extrude
import Design456_ExtrudeFace
import Design456_SplitObject
import Design456_Magnet
import Design456_Tweak
import Design456_unifySplitFuse
from PySide import QtCore, QtGui


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

            newObj = App.ActiveDocument.addObject("Part::MultiFuse", "MergedTemp")
            newObj.Shapes = allObjects
            newObj.Refine = True
            App.ActiveDocument.recompute()
            if newObj.isValid() == False:
                App.ActiveDocument.removeObject(newObj.Name)
                # Shape is not OK
                errMessage = "Failed Merge"
                faced.getInfo(s).errorDialog(errMessage)
            else:

                # Make a simple copy
                newShape = Part.getShape(
                    newObj, '', needSubElement=False, refine=True)
                NewJ = App.ActiveDocument.addObject(
                    'Part::Feature', 'Merged').Shape = newShape
                App.ActiveDocument.recompute()
                # Remove Old objects
                for obj in allObjects:
                   App.ActiveDocument.removeObject(obj.Name)
                App.ActiveDocument.removeObject(newObj.Name)
            App.ActiveDocument.recompute()
            del allObjects[:]
        except Exception as err:
            App.Console.PrintError("'Part::Merge' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Merge.svg',
            'MenuText': 'Part_Merge',
            'ToolTip':  'Part Merge'
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
            newObj = App.ActiveDocument.addObject("Part::Cut", "tempSubtract")
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
            if newObj.isValid() == False:
                App.ActiveDocument.removeObject(NewJ.Name)
                # Shape is not OK
                errMessage = "Failed to subtract objects"
                faced.getInfo(s).errorDialog(errMessage)
            else:
                # Remove Old objects
                allObjects = []
                for o in s:
                    allObjects.append(
                        App.ActiveDocument.getObject(o.ObjectName))
                for obj in allObjects:
                    App.ActiveDocument.removeObject(obj.Name)
                App.ActiveDocument.removeObject(newObj.Name)
            App.ActiveDocument.recompute()
            del allObjects[:]
        except Exception as err:
            App.Console.PrintError("'Part::Subtract' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Subtract.svg',
            'MenuText': 'Part_Subtract',
            'ToolTip':  'Part Subtract'
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
            newObj = App.ActiveDocument.addObject("Part::MultiCommon", "tempIntersect")
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
            del allObjects[:]
        except Exception as err:
            App.Console.PrintError("'Part::Intersect' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Intersect.svg',
            'MenuText': 'Part_Intersect',
            'ToolTip':  'Part Intersect'
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

            newObj = App.ActiveDocument.Tip = App.ActiveDocument.addObject('App::Part', 'Group')
            newObj.Label = 'Group'
            for obj_ in s:
                obj = App.ActiveDocument.getObject(obj_.ObjectName)
                newObj.addObject(obj)

            App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'Part::Part' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Group.svg',
            'MenuText': 'Part_Group',
            'ToolTip':  'Part Group'
        }


Gui.addCommand('Design456_Part_Group', Design456_Part_Group())


# Compound
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

            newObj = App.ActiveDocument.addObject("Part::Compound", "TempCompound")
            newObj.Links = allObjects
            # Make a simple copy
            App.ActiveDocument.recompute()
            newShape = Part.getShape(
                newObj, '', needSubElement=False, refine=True)
            NewJ = App.ActiveDocument.addObject(
                'Part::Feature', 'Compound').Shape = newShape

            # Remove Old objects
            for obj in allObjects:
                App.ActiveDocument.removeObject(obj.Name)
            App.ActiveDocument.removeObject(newObj.Name)

            App.ActiveDocument.recompute()
            del allObjects[:]
        except Exception as err:
            App.Console.PrintError("'Part::Compound' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_Part_Compound.svg',
            'MenuText': 'Part Compound',
            'ToolTip':  'Part Compound'
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
            thickness = QtGui.QInputDialog.getDouble(
                None, "Thickness", "Value:", 0, -1000.0, 1000.0, 2)[0]
            if(thickness == 0):
                return  # Nothing to do
            allObjects = []
            for o in s:
                allObjects.append(App.ActiveDocument.getObject(o.ObjectName))
            currentObj = App.ActiveDocument.getObject(s[0].ObjectName)
            currentObjLink = currentObj.getLinkedObject(True)
            thickObj = App.ActiveDocument.addObject(
                "Part::Thickness", "Thickness")
            thickObj.Value = thickness
            thickObj.Join = 0
            thickObj.Mode = 0
            thickObj.Intersection = False
            thickObj.SelfIntersection = False
            getfacename = faced.getInfo(s[0]).getFaceName()
            thickObj.Faces = (currentObj, getfacename,)
            if thickObj.isValid() == False:
                App.ActiveDocument.removeObject(thickObj.Name)
                # Shape is not OK
                errMessage = "Failed create shell"
                faced.getInfo(s).errorDialog(errMessage)
            else:
                App.ActiveDocument.recompute()
                NewJ = App.ActiveDocument.addObject(
                    'Part::Feature', 'Shell').Shape = thickObj.Shape
                App.ActiveDocument.recompute()
                # Remove Old objects
                for obj in allObjects:
                    App.ActiveDocument.removeObject(obj.Name)
                App.ActiveDocument.removeObject(thickObj.Name)

            App.ActiveDocument.recompute()
            del allObjects[:]
        except Exception as err:
            App.Console.PrintError("'Part::Shell' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'PartDesign_Shell.svg',
            'MenuText': 'Part_Shell',
            'ToolTip':  'Part Shell'
        }


Gui.addCommand('Design456_Part_Shell', Design456_Part_Shell())


# fillet
class Design456_Part_Fillet:

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 1):
                # One object must be selected at least
                errMessage = "Select a face or an edge use Fillet"
                faced.getInfo(s).errorDialog(errMessage)
                return
            Radius = QtGui.QInputDialog.getDouble(
                None, "Fillet Radius", "Radius:", 0, 1.0, 20.0, 2)[0]
            if (Radius == 0):
                return
            tempNewObj = App.ActiveDocument.addObject(
                "Part::Fillet", "tempFillet")
            sub1 = s[0]
            tempNewObj.Base = sub1.Object
            names = sub1.SubElementNames
            print(names)
            EdgesToBeChanged = []
            if (len(names) != 0):
                counter = 1
                """ we need to take the rest of the string
                            i.e. 'Edge15' --> take out 'Edge'-->4 bytes
                            len('Edge')] -->4
                """
                for name in names:
                    edgeNumbor = int(name[4:len(name)])
                    EdgesToBeChanged.append((edgeNumbor, Radius, Radius))
                print(EdgesToBeChanged)
                tempNewObj.Edges = EdgesToBeChanged
            else:
                errMessage = "Fillet failed. No subelements found"
                faced.getInfo(s).errorDialog(errMessage)
                return

            if tempNewObj.isValid() == False:
                App.ActiveDocument.removeObject(tempNewObj.Name)
                # Shape is not OK
                errMessage = "Failed to fillet the objects"
                faced.getInfo(s).errorDialog(errMessage)
            else:
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
            del EdgesToBeChanged[:]

        except Exception as err:
            App.Console.PrintError("'Fillet' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Fillet.svg',
            'MenuText': 'Part_Fillet',
            'ToolTip':  'Part Fillet'
        }


Gui.addCommand('Design456_Part_Fillet', Design456_Part_Fillet())


# chamfer
class Design456_Part_Chamfer:

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 1):
                # One object must be selected at least
                errMessage = "Select a face or an edge use Chamfer"
                faced.getInfo(s).errorDialog(errMessage)
                return
            Radius = QtGui.QInputDialog.getDouble(
                None, "Radius", "Radius:", 0, -10000.0, 10000.0, 2)[0]
            if (Radius == 0):
                return  # Nothing to do here
            sub1 = s[0]
            tempNewObj = App.ActiveDocument.addObject(
                "Part::Chamfer", "tempChamfer")
            tempNewObj.Base = sub1.Object
            names = sub1.SubElementNames
            EdgesToBeChanged = []
            if (len(names) != 0):
                counter = 1
                for name in names:
                    edgeNumbor = int(name[4:len(name)])
                    EdgesToBeChanged.append((edgeNumbor, Radius, Radius))
                tempNewObj.Edges = EdgesToBeChanged
            else:
                errMessage = "Chamfer failed. No subelements found"
                faced.getInfo(s).errorDialog(errMessage)
                return
            # Make a simple copy of the object
            App.ActiveDocument.recompute()
            if tempNewObj.isValid() == False:
                App.ActiveDocument.removeObject(tempNewObj.Name)
                # Shape is not OK
                errMessage = "Failed to fillet the objects"
                faced.getInfo(s).errorDialog(errMessage)
            else:
                newShape = Part.getShape(
                    tempNewObj, '', needSubElement=False, refine=False)
                newObj = App.ActiveDocument.addObject(
                    'Part::Feature', 'Chamfer').Shape = newShape
                App.ActiveDocument.recompute()
                App.ActiveDocument.ActiveObject.Label = 'Chamfer'

                App.ActiveDocument.removeObject(sub1.Object.Name)
                App.ActiveDocument.removeObject(tempNewObj.Name)
            App.ActiveDocument.recompute()
            del EdgesToBeChanged[:]
        except Exception as err:
            App.Console.PrintError("'Chamfer' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Chamfer.svg',
            'MenuText': 'Part_Chamfer',
            'ToolTip':  'Part Chamfer'
        }


Gui.addCommand('Design456_Part_Chamfer', Design456_Part_Chamfer())


class Design456_Part_3DToolsGroup:
        
    """Design456 Part 3D Tools"""

    def GetCommands(self):
        """3D Modifying Tools."""
        return ("Design456_Extrude",
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
                "Design456_Part_Compound",
                "Design456_unifySplitFuse1",
                "Design456_unifySplitFuse2",
                "Design_ColorizeObject",

                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools for modifying 3D Shapes")
        return {'Pixmap':  Design456Init.ICON_PATH+ 'Design456_3DTools.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "3Dtools"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_Part_3DToolsGroup", Design456_Part_3DToolsGroup())
