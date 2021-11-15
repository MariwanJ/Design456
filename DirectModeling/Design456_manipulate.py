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
import math
from PySide.QtCore import QT_TRANSLATE_NOOP
from PySide import QtGui, QtCore
from ThreeDWidgets.constant import FR_BRUSHES
from OCC.Core import ChFi2d
from OCC import Core
import FACE_D as faced

# >>> import Part
# >>> __s__=App.ActiveDocument.Compound.Shape.Faces
# >>> __s__=Part.Solid(Part.Shell(__s__))
# >>> __o__=App.ActiveDocument.addObject("Part::Feature","Compound_solid")
# >>> __o__.Label="Compound (Solid)"
# >>> __o__.Shape=__s__
# >>> del __s__, __o__

class ExtendEdge:
    """[Extend the edge's position to a new position. 
    This will affect the faces share the edge.
    
    ]
    """
    selectedObj = None
    selectedEdge=None
    AffectedFaced = [] #facess needed to be recreated - resized
    
    def findEdgeInFace(self,face,specialEdg):
        """[Find Edg in a face]

        Args:
            face ([Face Obj]): [Face has the specialEdg]
            specialEdg ([Edge Obj]): [An Edge to search for]

        Returns:
            [Boolean]: [True if the face found or False if not found ]
        """
        for edg in face.Edges:
            if specialEdg==edg:
                return True
        return False
    
    def findFacesWithSharedEdge(self,edg):
        """[Find out the faces have the same edge which will be dragged by the mouse]

        Args:
            edg ([Edge]): [Edge object shared between diffrent faces]
        """
        
        for face in self.selectedObj.Shape.Faces:
            if self.findEdgeInFace(edg):
                self.AffectedFaced.append(face)
        if len(self.AffectedFaced)==0:
            errMessage = "Please select an edge which is part of other objects"
            faced.errorDialog(errMessage)
            return
        
    def Activated(self):
        try:
            selectedObj = Gui.Selection.getSelectionEx()
            if len(selectedObj)>2: 
                errMessage = "Please select only one edge and try again"
                faced.errorDialog(errMessage)
                return

            self.selectedObj=selectedObj[0].Object
            self.selectedEdge=selectedObj[0].SubObjects[0]
            if not hasattr(self.selectedEdge,'Edge'):
                raise Exception("Please select only one edge and try again")            

            
        
        except Exception as err:
            App.Console.PrintError("'Design456_SmartFillet' del-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'PartDesign_Fillet.svg',
            'MenuText': ' Smart Fillet',
                        'ToolTip':  ' Smart ExtendEdge'
        }

Gui.addCommand('Design456_ExtendEdge', Design456_ExtendEdge())






class CornerModifier:

    mw = None
    dialog = None  # Dialog for the tool
    tab = None  # Tabs
    smartInd = None  # ?
    _mywin = None                           #
    b1 = None                               #
    CornerModifierLBL = None  # Label
    selectedObj=None

    def Activated(self):
        pass

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
            self.tab.addTab(self.dialog, "CornerModifier")
            self.tab.setCurrentWidget(self.dialog)
            self.dialog.resize(200, 450)
            self.dialog.setWindowTitle("CornerModifier")
            self.formLayoutWidget = QtGui.QWidget(self.dialog)
            self.formLayoutWidget.setGeometry(QtCore.QRect(10, 80, 281, 67))
            self.formLayoutWidget.setObjectName("formLayoutWidget")

            la = QtGui.QVBoxLayout(self.dialog)
            e1 = QtGui.QLabel("CornerModifier")
            commentFont = QtGui.QFont("Times", 12, True)
            e1.setFont(commentFont)

            self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
            self.formLayout.setContentsMargins(0, 0, 0, 0)
            self.formLayout.setObjectName("formLayout")
            self.lblCornerModifier = QtGui.QLabel(self.formLayoutWidget)
            self.dialog.setObjectName("CornerModifier")
            self.formLayout.setWidget(
                0, QtGui.QFormLayout.LabelRole, self.lblCornerModifier)
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
            self.CornerModifierLBL = QtGui.QLabel(
                "Use X,Y,Z to limit the movements\nAnd A for free movement\nCornerModifier Radius or side=7")

            la.addWidget(self.formLayoutWidget)
            la.addWidget(e1)
            la.addWidget(self.CornerModifierLBL)
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
            self.dialog.setWindowTitle(_translate(
                "CornerModifier", "CornerModifier"))
            self.lblCornerModifier.setText(_translate("Dialog", "Brush Type"))
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
            App.Console.PrintError("'Design456_CornerModifier' getMainWindow-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def __del__(self):
        """[Python destructor for the object. Otherwise next drawing might get wrong parameters]
        """
        self.remove_callbacks()
        self.mw = None
        self.dialog = None
        self.tab = None
        self.smartInd = None
        self._mywin = None
        self.b1 = None
        self.PaintLBL = None
        self.pl = None
        self.AllObjects = []
        self.currentObj = None
        self.view = None
        self.Observer = None
        self.continuePainting = True
        self.brushSize = 1
        self.brushType = 0
        self.resultObj = None
        self.runOnce = False

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
            self.__del__()  # Remove all CornerModifier 3dCOIN widgets

        except Exception as err:
            App.Console.PrintError("'recreate CornerModifier Obj' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Design456_CornerModifier.svg',
                'MenuText': "CornerModifier",
                'ToolTip': "Draw or CornerModifier"}


Gui.addCommand('Design456_CornerModifier', Design456_CornerModifier())
