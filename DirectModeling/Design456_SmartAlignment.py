# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# **************************************************************************
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
from pivy import coin
import FACE_D as faced
from PySide.QtCore import QT_TRANSLATE_NOOP
from typing import List
import Design456Init
from PySide import QtGui, QtCore

from ThreeDWidgets.Fr_Align_Widget import Fr_Align_Widget
from draftutils.translate import translate  # for translation

__updated__ = '2022-01-13 10:05:42'


#TODO: FIXME : NOT IMPLEMENTED

#                        CALLBACKS              #

# All buttons callbacks
def callback_btn0(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy Align-widget btn0 callback")

def callback_btn1(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy Align-widget btn1 callback")

def callback_btn2(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy Align-widget btn2 callback")

def callback_btn3(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy Align-widget btn3 callback")


def callback_btn4(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy Align-widget btn4 callback")

def callback_btn5(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy Align-widget btn5 callback")

def callback_btn6(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy Align-widget btn6 callback")

def callback_btn7(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy Align-widget btn7 callback")

def callback_btn8(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy Align-widget btn8 callback")


#                          END OF CALLBACKS                              #



class Design456_SmartAlignment:
    """
        Apply Alignment to any 3D object by selecting the object, a Face or one or multiple edges 
        Radius of the Alignment is counted by dragging the arrow towards the negative Z axis.
    """
    def __init__(self):
        self._vector = App.Vector(0.0, 0.0, 0.0) # not used dummy value
        self.mw = None
        self.dialog = None
        self.tab = None
        self.smartInd = None
        self._mywin = None
        self.b1 = None
        self.AlignmentLBL = None
        self.endVector = None
        self.startVector = None
        # We will make two object, one for visual effect and the other is the original
        self.selectedObj = []
        # 0 is the original    1 is the fake one (just for interactive effect)
        self.objectType = None  # Either shape, Face or Edge.
        self.NewBoundary=None
        

    def CalculateBoundary(self):
        a = self.selectedObj[0].Object.Shape.Boundary
        b = self.selectedObj[1].Object.Shape.Boundary
        self.NewBoundary = a # Just initialize it
        self.NewBoundary.XMax = maximum(a.XLength, b.XLength)
        self.NewBoundary.XMin = minimum(a.XLength, b.XLength)
        self.NewBoundary.YMax = maximum(a.YLength, b.YLength)
        self.NewBoundary.YMin = minimum(a.YLength, b.YLength) 
        self.NewBoundary.ZMax = maximum(a.ZLength, b.ZLength)
        self.NewBoundary.ZMin = minimum(a.ZLength, b.ZLength)

        self.NewBoundary.XLength = bTtotal.Xmax - bTtotal.Xmin  
        self.NewBoundary.YLength = bTtotal.Ymax - bTtotal.Ymin
        self.NewBoundary.ZLength = bTtotal.Zmax - bTtotal.Zmin
        self.NewBoundary.Center = App.Vector(bTotal.XLength/2, bTotal.YLength/2, bTotal.ZLength/2)
        self.NewBoundary.DiagonalLength = sqrt(powers(bTotal.XLength,2), 
                                     powers(bTotal.YLength,2),
                                     powers(bTotal.ZLength,2) )

    def Activated(self):
        import ThreeDWidgets.fr_coinwindow as win
        self.selectedObj.clear()
        sel=Gui.Selection.getSelectionEx()
        if len(sel) < 2:
            # An object must be selected
            errMessage = "Select at least two objects to Align them"
            faced.errorDialog(errMessage)
            return
        
        self.selectedObj = sel
        self.CalculateBoundary()
        print(self.self.NewBoundary)
        self.smartInd = Fr_Align_Widget(self.NewBoundary, ["Align Tool",])

        self.smartInd.w_callback_ = callback_release
        self.w_btnCallbacks_ = [callback_btn0, 
                                callback_btn1, 
                                callback_btn2, 
                                callback_btn3,
                                callback_btn4,
                                callback_btn5,
                                callback_btn6,
                                callback_btn7,
                                callback_btn8]

        self.smartInd.w_userData.callerObject = self

        if self._mywin is None:
            self._mywin = win.Fr_CoinWindow()
        self._mywin.addWidget(self.smartInd)
        mw = self.getMainWindow()
        self._mywin.show()
        
    def __del__(self):
        """ 
            class destructor
            Remove all objects from memory even fr_coinwindow
        """
        try:
            self.smartInd.hide()
            self.smartInd.__del__()  # call destructor
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
        if(self.AlignmentRadius<=0.01):
            #Alignment != applied. return the original object as it was
            if(len(self.selectedObj)==2):
                if hasattr(self.selectedObj[1],"Object"):
                    App.ActiveDocument.removeObject(self.selectedObj[1].Object.Name)    
                else:
                    App.ActiveDocument.removeObject(self.selectedObj[1].Name)
            o=Gui.ActiveDocument.getObject(self.selectedObj[0].Object.Name)
            o.Transparency=0
            o.Object.Label=self.Originalname
        else:
            self.selectedObj[0]=self.selectedObj[1]
            self.selectedObj.pop(1)
            no=App.ActiveDocument.getObject(self.selectedObj[0].Name)
            no.Label=self.Originalname
            App.ActiveDocument.removeObject(temp.Object.Name)
            self.AlignmentRadius=0.0001
        
        App.ActiveDocument.recompute()
        self.__del__()  # Remove all smart Alignment 3dCOIN widgets

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_SmartAlignment.svg',
            'MenuText': ' Smart Alignment',
                        'ToolTip':  ' Smart Alignment'
        }

Gui.addCommand('Design456_SmartAlignment', Design456_SmartAlignment())
