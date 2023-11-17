# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2022                                                    *
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
import Design456Init
import FACE_D as faced
from PySide.QtCore import QT_TRANSLATE_NOOP
from PySide import QtGui, QtCore
from ThreeDWidgets.constant import FR_BRUSHES, FR_COLOR

__updated__ = '2022-02-27 20:13:43'

class Design456_Hole:
    """[Select the part that will be used to make a hole in the surrounding objects]
    """
    def __init__(self):
        self.mw = None
        self.dialog = None  # Dialog for the tool
        self.tab = None  # Tabs
        self.smartInd = None  # ?
        self._mywin = None                           #
        self.b1 = None                               #
        self.HoleLBL = None  # Label
        # current created shape (circle, square, triangles,..etc)
        self.currentObj = None
        self.FoundObjects = None
        self.selectedObj = None
        self.finishedObj = None
        # This should take care of applying the hole command to the objects
        # two things must be done:
        # 1-Fusion for the tool (cutting objects)
        # 2-Fusion for the base objects.

    def applyHole(self):
        """[Create cut object and create fusion if there are several objects for tool and base]
        """
        try:
            fuBase = None
            fuTool = None
            if len(self.FoundObjects) == 0:
                return  # Nothing to do

            for obj in self.selectedObj:
                obj.Object.ViewObject.Transparency = 100
                obj.Object.ViewObject.Transparency = 0
                obj.Object.ViewObject.ShapeColor = FR_COLOR.FR_GRAY

            if(len(self.selectedObj) > 1):
                fuTool = App.ActiveDocument.addObject(
                    "Part::MultiFuse", "tool")
                allOBJ = []
                for obj in self.selectedObj:
                    allOBJ.append(obj.Object)
                fuTool.Shapes = allOBJ
                fuTool.Refine = True
            else:
                fuTool = self.selectedObj[0]
            if len(self.FoundObjects) > 1:
                fuBase = App.ActiveDocument.addObject(
                    "Part::MultiFuse", "base")
                allOBJ = []
                for obj in self.FoundObjects:
                    allOBJ.append(App.ActiveDocument.getObject(obj.Name))
                fuBase.Shapes = allOBJ
                fuBase.Refine = True
            else:
                if len(self.FoundObjects) >= 1:
                    fuBase = self.FoundObjects[0]
                else:
                    if type(self.FoundObjects) == list:
                        fuBase = None
                    else:
                        fuBase = self.FoundObjects
            if (fuTool is None or fuBase is None):
                print("something went wrong, please try again")
                return
            App.ActiveDocument.recompute()
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(fuBase)
            self.finishedObj = App.ActiveDocument.addObject("Part::Cut", "Cut")
            self.finishedObj.Base = fuBase
            self.finishedObj.Tool = fuTool.Object

            App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'apply' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Activated(self):
        """[Design456_Hole tool activation function.]
        """
        try:
            overlappen = False
            self.FoundObjects = faced.findMainListedObjects()
            self.selectedObj = Gui.Selection.getSelectionEx()

            for obj in self.selectedObj:
                obj.Object.ViewObject.ShapeColor = FR_COLOR.FR_LIGHTPINK
                obj.Object.ViewObject.Transparency = 70

                for nObj in self.FoundObjects:
                    if obj.Object == nObj:
                        self.FoundObjects.remove(nObj)

            for nObj in self.FoundObjects:
                overlappen = False
                for obj in self.selectedObj:
                    if(faced.Overlapping(nObj, obj.Object)):
                        overlappen = True
                        break
                # remove not intersecting objects
                if not overlappen:
                    if(len(self.FoundObjects) >= 1):
                        if(nObj in self.FoundObjects):
                            self.FoundObjects.remove(nObj)

                # TODO :FIXME: See if this works ?
                if (not( hasattr(nObj, "Shape") and nObj.Shape.Solids)):
                    if(len(self.FoundObjects) >= 1):
                        if(nObj in self.FoundObjects):
                            self.FoundObjects.remove(nObj)

            self.getMainWindow()
            self.view = Gui.ActiveDocument.activeView()

        except Exception as err:
            App.Console.PrintError("'Holes Command' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def getMainWindow(self):
        """[Create the tab for the tool]

        Returns:
            [QTtab]: [The tab created which should be added to the FreeCAD]
        """
        try:
            toplevel = QtGui.QApplication.topLevelWidgets()
            self.mw = None
            for i in toplevel:
                if i.metaObject().className() == "Gui::MainWindow":
                    self.mw = i
            if self.mw is None:
                raise Exception("No main window found")
            dw = self.mw.findChildren(QtGui.QDockWidget)
            for i in dw:
                if str(i.objectName()) == "Model":
                    self.tab = i.findChild(QtGui.QTabWidget)
                elif str(i.objectName()) == "Python Console":
                    self.tab = i.findChild(QtGui.QTabWidget)
            if self.tab is None:
                raise Exception("No tab widget found")

            self.dialog = QtGui.QDialog()
            oldsize = self.tab.count()
            self.tab.addTab(self.dialog, "Holes")
            self.tab.setCurrentWidget(self.dialog)
            self.dialog.resize(200, 450)
            self.dialog.setWindowTitle("Holes")
            self.formLayoutWidget = QtGui.QWidget(self.dialog)
            self.formLayoutWidget.setGeometry(QtCore.QRect(10, 80, 281, 67))
            self.formLayoutWidget.setObjectName("formLayoutWidget")

            la = QtGui.QVBoxLayout(self.dialog)
            e1 = QtGui.QLabel("Holes")
            commentFont = QtGui.QFont("Times", 12, True)
            e1.setFont(commentFont)

            self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
            self.formLayout.setContentsMargins(0, 0, 0, 0)
            self.formLayout.setObjectName("formLayout")
            self.lblHole = QtGui.QLabel(self.formLayoutWidget)
            self.dialog.setObjectName("Holes")
            self.HoleLBL = QtGui.QLabel(
                "Press OK to apply the hole")

            la.addWidget(self.formLayoutWidget)
            la.addWidget(e1)
            la.addWidget(self.HoleLBL)
            self.okbox = QtGui.QDialogButtonBox(self.dialog)
            self.okbox.setOrientation(QtCore.Qt.Horizontal)
            self.okbox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
            la.addWidget(self.okbox)
            _translate = QtCore.QCoreApplication.translate
            self.dialog.setWindowTitle(_translate("Hole", "Hole"))
            QtCore.QMetaObject.connectSlotsByName(self.dialog)
            QtCore.QObject.connect(
                self.okbox, QtCore.SIGNAL("accepted()"), self.hide)
            return self.dialog

        except Exception as err:
            App.Console.PrintError("'Design456_Hole' getMainWindow-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def __del__(self):
        """[Python destructor for the object. Otherwise next drawing might get wrong parameters]
        """
        self.mw = None
        self.dialog = None
        self.tab = None
        self.smartInd = None
        self._mywin = None
        self.b1 = None
        self.HoleLBL = None

        return self.finishedObj

    def hide(self):
        """
        Hide the widgets. Remove also the tab.
        """
        try:
            self.applyHole()

            self.dialog.hide()
            dw = self.mw.findChildren(QtGui.QDockWidget)
            newsize = self.tab.count()  # Todo : Should we do that?
            self.tab.removeTab(newsize-1)  # it ==0,1,2,3 ..etc
            del self.dialog
            App.ActiveDocument.recompute()
            faced.showFirstTab()
            self.__del__()  # Remove allOBJ Holes 3dCOIN widgets

        except Exception as err:
            App.Console.PrintError("'Holes' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Design456_Hole.svg',
                'MenuText': "Hole",
                'ToolTip': "Hole"}


Gui.addCommand('Design456_Hole', Design456_Hole())
