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
import Draft as _draft
import Part as _part
import Design456Init
from pivy import coin
import FACE_D as faced
import math as _math
from PySide.QtCore import QT_TRANSLATE_NOOP
from PySide import QtGui, QtCore
from ThreeDWidgets.constant import FR_BRUSHES
import math
from pivy import coin
import Design456_2Ddrawing

class Design456_Hole:

    mw = None
    dialog = None  # Dialog for the tool
    tab = None  # Tabs
    smartInd = None  # ?
    _mywin = None                           #
    b1 = None                               #
    HoleLBL = None  # Label
    # current created shape (circle, square, triangles,..etc)
    currentObj = None

    firstSize = 0.1


    def Activated(self):
        """[Design456_Hole tool activation function.]
        """
        self.c1 = None
        self.c2 = None
        try:
            self.getMainWindow()
            self.view = Gui.ActiveDocument.activeView()
        except Exception as err:
            App.Console.PrintError("'Hole Command' Failed. "
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
                if str(i.objectName()) == "Combo View":
                    self.tab = i.findChild(QtGui.QTabWidget)
                elif str(i.objectName()) == "Python Console":
                    self.tab = i.findChild(QtGui.QTabWidget)
            if self.tab is None:
                raise Exception("No tab widget found")

            self.dialog = QtGui.QDialog()
            oldsize = self.tab.count()
            self.tab.addTab(self.dialog, "Hole")
            self.tab.setCurrentWidget(self.dialog)
            self.dialog.resize(200, 450)
            self.dialog.setWindowTitle("Hole")
            self.formLayoutWidget = QtGui.QWidget(self.dialog)
            self.formLayoutWidget.setGeometry(QtCore.QRect(10, 80, 281, 67))
            self.formLayoutWidget.setObjectName("formLayoutWidget")

            la = QtGui.QVBoxLayout(self.dialog)
            e1 = QtGui.QLabel("Hole")
            commentFont = QtGui.QFont("Times", 12, True)
            e1.setFont(commentFont)

            self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
            self.formLayout.setContentsMargins(0, 0, 0, 0)
            self.formLayout.setObjectName("formLayout")
            self.lblHole = QtGui.QLabel(self.formLayoutWidget)
            self.dialog.setObjectName("Hole")
            self.formLayout.setWidget(
                0, QtGui.QFormLayout.LabelRole, self.lblHole)
            self.lstBrushType = QtGui.QListWidget(self.dialog)
            self.lstBrushType.setGeometry(10, 10, 50, 40)
            self.lstBrushType.setObjectName("lstBrushType")
            self.formLayout.setWidget(
                0, QtGui.QFormLayout.FieldRole, self.lstBrushType)
            self.lstBrushSize = QtGui.QListWidget(self.dialog)
            self.lstBrushSize.setGeometry(10, 55, 50, 20)

            self.lstBrushSize.setObjectName("lstBrushSize")
            self.formLayout.setWidget(
                1, QtGui.QFormLayout.FieldRole, self.lstBrushSize)
            self.lblBrushSize = QtGui.QLabel(self.formLayoutWidget)
            self.lblBrushSize.setObjectName("lblBrushSize")
            self.formLayout.setWidget(
                1, QtGui.QFormLayout.LabelRole, self.lblBrushSize)
            self.formLayoutWidget_2 = QtGui.QWidget(self.dialog)
            self.formLayoutWidget_2.setGeometry(QtCore.QRect(10, 160, 160, 80))
            self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
            self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget_2)
            self.formLayout_2.setContentsMargins(0, 0, 0, 0)
            self.formLayout_2.setObjectName("formLayout_2")
            self.radioAsIs = QtGui.QRadioButton(self.formLayoutWidget_2)
            self.radioAsIs.setObjectName("radioAsIs")
            self.formLayout_2.setWidget(
                0, QtGui.QFormLayout.FieldRole, self.radioAsIs)
            self.radioMerge = QtGui.QRadioButton(self.formLayoutWidget_2)
            self.radioMerge.setObjectName("radioMerge")
            self.formLayout_2.setWidget(
                1, QtGui.QFormLayout.FieldRole, self.radioMerge)
            self.HoleLBL = QtGui.QLabel(
                "Use X,Y,Z to limit the movements\nAnd A for free movement\nHole Radius or side=7")

            la.addWidget(self.formLayoutWidget)
            la.addWidget(e1)
            la.addWidget(self.HoleLBL)
            self.okbox = QtGui.QDialogButtonBox(self.dialog)
            self.okbox.setOrientation(QtCore.Qt.Horizontal)
            self.okbox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
            la.addWidget(self.okbox)
            # Add All shape names to the combobox
            for nameOfObject in self.listOfDrawings:
                self.lstBrushType.addItem(nameOfObject)

            for i in range(1, 1000):
                self.lstBrushSize.addItem(str(i))
            self.lstBrushSize.setCurrentRow(6)
            self.lstBrushType.setCurrentRow(FR_BRUSHES.FR_CIRCLE_BRUSH)

            self.lstBrushSize.currentItemChanged.connect(
                self.BrushSizeChanged_cb)

            self.lstBrushType.currentItemChanged.connect(
                self.BrushTypeChanged_cb)

            _translate = QtCore.QCoreApplication.translate
            self.dialog.setWindowTitle(_translate("Pain", "Hole"))
            self.lblHole.setText(_translate("Dialog", "Brush Type"))
            self.lstBrushType.setToolTip(_translate("Dialog", "Brush Type"))
            self.lstBrushSize.setToolTip(_translate("Dialog", "Brush Type"))
            self.lblBrushSize.setText(_translate("Dialog", "Brush Size"))
            self.radioAsIs.setText(_translate("Dialog", "As is"))
            self.radioMerge.setText(_translate("Dialog", "Merge"))

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

    def hide(self):
        """
        Hide the widgets. Remove also the tab.
        """
        try:
            if (self.currentObj is not None):
                App.ActiveDocument.removeObject(self.currentObj.Object.Name)
                self.currentObj = None
            self.dialog.hide()
            dw = self.mw.findChildren(QtGui.QDockWidget)
            newsize = self.tab.count()  # Todo : Should we do that?
            self.tab.removeTab(newsize-1)  # it ==0,1,2,3 ..etc
            del self.dialog
            App.ActiveDocument.recompute()
            self.__del__()  # Remove all Hole 3dCOIN widgets

        except Exception as err:
            App.Console.PrintError("'recreate Hole Obj' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Design456_Hole.svg',
                'MenuText': "Hole",
                'ToolTip': "Draw or Hole"}

Gui.addCommand('Design456_Hole', Design456_Hole())

