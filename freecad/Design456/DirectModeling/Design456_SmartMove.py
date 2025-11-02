# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# **************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2025                                                    *
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
from pivy import coin
import FACE_D as faced
from PySide.QtCore import QT_TRANSLATE_NOOP
from typing import List
import Design456Init
from PySide import QtGui, QtCore
from ThreeDWidgets.fr_arrow_widget import Fr_Arrow_Widget
from ThreeDWidgets import fr_arrow_widget
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from draftutils.translate import translate  # for translation
import math
from ThreeDWidgets.fr_three_arrows_widget import Fr_ThreeArrows_Widget

MouseScaleFactor = 1.5

__updated__ = '2022-03-27 10:22:58'

def callback_move(userData: fr_arrow_widget.userDataObject = None):
    pass

def callback_release(userData: fr_arrow_widget.userDataObject = None):
    pass
#TODO: FIXME:
# This tool should easily move, rotate and place any object. 
# Rotation Axis must be changable. Default will be centerofmass
# but it can also choose other by moving the Axis bar which will be
# a COIN3D bar or line. 
# This must make placement of object much much easier and simpler. 

class Design456_SmartMove:
    """
        Apply Move to any 3D object by selecting the object.
    """
    def __init__(self):
        self.selectedObjects = None
        self.ArrowObject = None
        self.AxisBarObject = None
        self.AxisBarLocation= App.Vector(0,0,0)
        self.w_vector=App.Vector(0,0,0)

        self.dialog = None
        self.tab = None
        self.smartInd = None
        self._mywin = None
        self.b1 = None
        self.AlignmentLBL = None
        self.run_Once = False
        self.endVector = None
        self.startVector = None
        self.w_rotation = None
        self.setupRotation = None
        self.w_scale = None


    def Activated(self):
        s=Gui.Selection.getSelectionEx()
        if len(s)<1: 
            # An object must be selected
            errMessage = "Select an object before using the tool"
            faced.errorDialog(errMessage)
            return
        try:
            self.selectedObjects=s
            self.w_vector= s[0].Object.Placement.Base
            self.discObj = Fr_ThreeArrows_Widget([self.w_vector, App.Vector(0, 0, 0)],  #
                                                 # label
                                                 [(str(round(self.w_rotation[0], 2)) + "°" +
                                                   str(round(self.w_rotation[1], 2)) + "°" +
                                                   str(round(self.w_rotation[2], 2)) + "°"), ],
                                                 FR_COLOR.FR_WHITE,  # lblcolor
                                                 [FR_COLOR.FR_RED, FR_COLOR.FR_GREEN,
                                                 FR_COLOR.FR_BLUE],  # arrows color
                                                 # rotation of the disc main
                                                 [0, 0, 0, 0],
                                                 self.setupRotation,  # setup rotation
                                                 [30.0, 30.0, 30.0],  # scale
                                                 1,  # type
                                                 0,  # opacity
                                                 10)  # distance between them
            self.discObj.enableDiscs()

            # Different callbacks for each action.
            self.discObj.w_xAxis_cb_ = self.MouseDragging_cb
            self.discObj.w_yAxis_cb_ = self.MouseDragging_cb
            self.discObj.w_zAxis_cb_ = self.MouseDragging_cb

            
            self.discObj.w_discXAxis_cb_ = self.RotatingObject_cb
            self.discObj.w_discYAxis_cb_ = self.RotatingObject_cb
            self.discObj.w_discZAxis_cb_ = self.RotatingObject_cb


            self.discObj.w_callback_ = self.callback_release
            self.discObj.w_userData.callerObject = self

            self.COIN_recreateObject()

            if self._mywin is None:
                self._mywin = win.Fr_CoinWindow()

            self._mywin.addWidget(self.discObj)
            mw = self.getMainWindow()
            self._mywin.show()
            
        except Exception as err:
            App.Console.PrintError("'Activated SmartMove' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


    def MouseDragging_cb(self):
        pass
    
    def RotatingObject_cb(self):
        pass

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
                if str(i.objectName()) == "Model":
                    self.tab = i.findChild(QtGui.QTabWidget)
                elif str(i.objectName()) == "Python Console":
                    self.tab = i.findChild(QtGui.QTabWidget)
            if self.tab is None:
                raise Exception("No tab widget found")

            self.dialog = QtGui.QDialog()
            oldsize = self.tab.count()
            self.tab.addTab(self.dialog, "Smart Alignment")
            self.tab.setCurrentWidget(self.dialog)
            self.dialog.resize(200, 450)
            self.dialog.setWindowTitle("Smart Alignment")
            la = QtGui.QVBoxLayout(self.dialog)
            e1 = QtGui.QLabel("(Smart Alignment)\nFor quicker\nApplying Alignment")
            commentFont = QtGui.QFont("Times", 12, True)
            self.AlignmentLBL = QtGui.QLabel("Radius=")
            e1.setFont(commentFont)
            la.addWidget(e1)
            la.addWidget(self.AlignmentLBL)
            okbox = QtGui.QDialogButtonBox(self.dialog)
            okbox.setOrientation(QtCore.Qt.Horizontal)
            okbox.setStandardButtons(
                QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
            la.addWidget(okbox)
            QtCore.QObject.connect(okbox, QtCore.SIGNAL("accepted()"), self.hide)

            QtCore.QMetaObject.connectSlotsByName(self.dialog)
            return self.dialog

        except Exception as err:
            App.Console.PrintError("'Design456_Alignment' getMainWindow-Failed. "
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
        temp=self.selectedObj[0]
        App.ActiveDocument.recompute()
        faced.showFirstTab()
        self.__del__()  # Remove all smart Alignment 3dCOIN widgets
    
    def __del__(self):
        """ 
            class destructor
            Remove all objects from memory even fr_coinwindow
        """
        try:
            self.Arrow.hide()
            self.ArrowObject.__del__()
            if self._mywin is not None:
                self._mywin.hide()
                del self._mywin
                self._mywin = None
            App.ActiveDocument.commitTransaction()  # undo reg.

        except Exception as err:
            App.Console.PrintError("'Design456_SmartAlignment' del-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

    
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_SmartMove.svg',
            'MenuText': ' Smart Move',
                        'ToolTip':  ' Smart Move'
        }


Gui.addCommand('Design456_SmartMove', Design456_SmartMove())
