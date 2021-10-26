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
import Draft as _draft
from ThreeDWidgets.constant import FR_BRUSHES
#TODO . FIXME


class Design456_Paint:
    brushType: FR_BRUSHES = FR_BRUSHES.FR_CIRCLE_BRUSH
    brushSize = 1

    mw = None
    dialog = None
    tab = None
    smartInd = None
    _mywin = None
    b1 = None
    PaintLBL = None
    pl = App.Placement()
    pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
    pl.Base = App.Vector(0.0, 0.0, 0.0)
    AllObjects = []
    cmbBrushSize = None
    cmbBrushType = None
    currentObj = None
    view = None
    Observer = None
    continuePainting = True
    brushSize = 1
    brushType = 0
    resultObj=None

    def setSize(self):
        text = self.cmbBrushSize.currentText()
        if text != "":
            self.brushSize = int(text)

    def setTye(self):
        text = self.cmbBrushSize.currentText()
        if text != "":
            self.brushType = int(text)

    def draw_circle(self):
        #make_circle(radius, placement=None, face=None, startangle=None, endangle=None, support=None)
        size = int(self.cmbBrushSize.currentText())
        s = _draft.make_circle(
            radius = size, placement = self.pl, face = True, startangle=None, endangle=None, support=None)
        #Convert/ or get Gui object not App object
        self.currentObj=Gui.ActiveDocument.getObject(s.Name)

    def draw_Half_circle(self):
        size = int(self.cmbBrushSize.currentText())

        pass
    
    def appendToList(self):
        Dir = self.currentObj.Object.Shape.normalAt(0,0)
        tempExtrude=self.currentObj.Object.Shape.extrude(Dir)
        self.AllObjects.append(tempExtrude)
        
    def draw_Square(self):
        size = int(self.cmbBrushSize.currentText())
        s = _draft.make_rectangle(
            length = size, height = size, placement = self.pl, face = True, support = None)
        #Convert/ or get Gui object not App object
        self.currentObj=Gui.ActiveDocument.getObject(s.Name)
        

    def draw_HalfCircle(self):
        pass

    def draw_MultiSided(self, sides):
        self.currentObj = _draft.makePolygon(sides, self.brushSize, True,self.pl, True,  None )
        _draft.autogroup(self.currentObj)

    def draw_Moon(self):
        pass
    
    def mergeAll(self):
        for obj in self.AllObjects:
            pass
    def MoveObj_cb(self,info):
        print("callback!!")
        pos = info["Position"]
        position = self.view.getPoint(pos)
        self.currentObj.Placement.Base = position
        App.ActiveDocument.recompute()

    def placeObject_cb(self, info):
        print("callback!!")
        down = (info["State"] == "DOWN")
        pos = info["Position"]
        if (down):
            self.AllObjects.append(self.currentObj)
            self.MergeAll()
            App.ActiveDocument.recompute()
            self.recreateObject()
        
    def recreateObject(self):
        print("Recreate")
        if(self.currentObj is not None):
            self.currentObj = None

        if self.brushType == 0:
            self.currentObj = self.draw_circle()
        elif self.brushType == 1:
            self.currentObj = self.draw_Half_circle()
        elif self.brushType == 2:
            self.currentObj = self.draw_polygon(self.brushType) #Triangle
        elif self.brushType == 3:
            self.currentObj = self.draw_Square()
        elif (self.brushType == 4 or self.brushType == 5 or
              self.brushType == 6 or self.brushType == 7):
            self.currentObj = self.draw_polygon(self.brushType)
        elif self.brushType == 8:
            self.currentObj = self.draw_Moon()
        if (self.resultObj is None):
            if (len(self.AllObjects)>0):
                self.resultObj.Shapes = self.AllObjects
                self.resultObj = App.ActiveDocument.addObject("Part::MultiFuse","Paint")
                self.resultObj.Refine = True

    def Activated(self):
        self.c1 = None
        self.c2 = None
        try:
            self.getMainWindow()
            self.view = Gui.ActiveDocument.activeView()
            self.recreateObject() # Initial
            App.ActiveDocument.recompute()
            self.c1 = self.view.addEventCallback(
                "SoMouseButtonEvent", self.placeObject_cb)
            self.c2 = self.view.addEventCallback("SoLocation2Event", self.MoveObj_cb )

        except Exception as err:
            App.Console.PrintError("'PaintCommand' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def __del__(self):
        self.removeEventCallback("SoMouseButtonEvent",self.c1)
        self.removeEventCallback("SoLocation2Event",self.c2)
        try:
            App.ActiveDocument.commitTransaction()  # undo reg.

        except Exception as err:
            App.Console.PrintError("'Design456_SmartPaint' del-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

    def BrushChanged_cb(self):
        App.ActiveDocument.removeObject(self.currentObj)
        self.currentObj = None
        self.recreateObject()

    def getMainWindow(self):

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
            self.tab.addTab(self.dialog, "Paint")
            self.tab.setCurrentWidget(self.dialog)
            self.dialog.resize(200, 450)
            self.dialog.setWindowTitle("Paint")
            self.formLayoutWidget = QtGui.QWidget(self.dialog)
            self.formLayoutWidget.setGeometry(QtCore.QRect(10, 80, 281, 67))
            self.formLayoutWidget.setObjectName("formLayoutWidget")

            la = QtGui.QVBoxLayout(self.dialog)
            e1 = QtGui.QLabel("Paint")
            commentFont = QtGui.QFont("Times", 12, True)
            self.PaintLBL = QtGui.QLabel("Paint Radius=")
            e1.setFont(commentFont)

            self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
            self.formLayout.setContentsMargins(0, 0, 0, 0)
            self.formLayout.setObjectName("formLayout")
            self.lblPaint = QtGui.QLabel(self.formLayoutWidget)
            self.dialog.setObjectName("Pint")
            self.formLayout.setWidget(
                0, QtGui.QFormLayout.LabelRole, self.lblPaint)
            self.cmbBrushType = QtGui.QComboBox(self.formLayoutWidget)
            self.cmbBrushType.setCurrentText("")
            self.cmbBrushType.setObjectName("cmbBrushType")
            self.formLayout.setWidget(
                0, QtGui.QFormLayout.FieldRole, self.cmbBrushType)
            self.cmbBrushSize = QtGui.QComboBox(self.formLayoutWidget)
            self.cmbBrushSize.setCurrentText("")
            self.cmbBrushSize.setObjectName("cmbBrushSize")
            self.formLayout.setWidget(
                1, QtGui.QFormLayout.FieldRole, self.cmbBrushSize)
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

            la.addWidget(self.formLayoutWidget)
            la.addWidget(e1)
            la.addWidget(self.PaintLBL)
            okbox = QtGui.QDialogButtonBox(self.dialog)
            okbox.setOrientation(QtCore.Qt.Horizontal)
            okbox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
            la.addWidget(okbox)

            self.cmbBrushType.addItem("Circle")
            self.cmbBrushType.addItem("Half Circle")
            self.cmbBrushType.addItem("Triangle")
            self.cmbBrushType.addItem("Square")
            self.cmbBrushType.addItem("Four Sided")
            self.cmbBrushType.addItem("Five Sided")
            self.cmbBrushType.addItem("Six sided")
            self.cmbBrushType.addItem("Moon")
            for i in range(1, 400):
                self.cmbBrushSize.addItem(str(i))
            self.cmbBrushSize.setCurrentIndex(FR_BRUSHES.FR_SQUARE_BRUSH)
            self.cmbBrushSize.setCurrentIndex(1)
            self.cmbBrushSize.currentTextChanged.connect(self.BrushChanged_cb)
            self.cmbBrushSize.currentIndexChanged.connect(self.BrushChanged_cb)
            self.cmbBrushType.currentTextChanged.connect(self.BrushChanged_cb)
            self.cmbBrushType.currentIndexChanged.connect(self.BrushChanged_cb)
            
            
            QtCore.QObject.connect(
                okbox, QtCore.SIGNAL("accepted()"), self.hide)

            _translate = QtCore.QCoreApplication.translate
            self.dialog.setWindowTitle(_translate("Pain", "Pint"))
            self.lblPaint.setText(_translate("Dialog", "Brush Type"))
            self.cmbBrushType.setToolTip(_translate("Dialog", "Brush Type"))
            self.cmbBrushSize.setToolTip(_translate("Dialog", "Brush Type"))
            self.lblBrushSize.setText(_translate("Dialog", "Brush Size"))
            self.radioAsIs.setText(_translate("Dialog", "As is"))
            self.radioMerge.setText(_translate("Dialog", "Merge"))
            QtCore.QMetaObject.connectSlotsByName(self.dialog)

            return self.dialog

        except Exception as err:
            App.Console.PrintError("'Design456_Paint' getMainWindwo-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def hide(self):
        """
        Hide the widgets. Remove also the tab.
        """
        self.dialog.hide()
        del self.dialog
        dw = self.mw.findChildren(QtGui.QDockWidget)
        newsize = self.tab.count()  # Todo : Should we do that?
        self.tab.removeTab(newsize-1)  # it ==0,1,2,3 ..etc

        App.ActiveDocument.recompute()
        self.__del__()  # Remove all Paint 3dCOIN widgets

    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Design456_Paint.svg',
                'MenuText': "Paint",
                'ToolTip': "Draw or Paint"}


Gui.addCommand('Design456_Paint', Design456_Paint())
