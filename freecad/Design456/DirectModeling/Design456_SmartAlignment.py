# -*- coding:  -*-
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

from ThreeDWidgets.fr_align_widget import Fr_Align_Widget
from ThreeDWidgets.fr_align_widget import userDataObject
from draftutils.translate import translate  # for translation
from ThreeDWidgets.constant import FR_COLOR

__updated__ = '2022-06-30 09:25:44'
#####################################################

#We need to capture undo redo for the buttons. To redraw the buttons. 
class SmartAlignObserver(object):
    '''
        This object will provide the mechanism to
        undo actions while the tool is active.
    '''
    def __init__(self,_linkToCaller):
        '''
            Initialize the class with the link to the caller object
        '''
        self.linkToCaller = _linkToCaller
        
    def slotRedoDocument(self,doc):
        '''
            Capture Redo event from the document
        '''
        self.linkToCaller.recreateAll()  #Redo event. Redraw everything
    
    def slotUndoDocument(self,doc):
        '''
            Capture Undo event from the document
        '''
        self.linkToCaller.recreateAll() #Undo event. Redraw everything
#####################################################

#                        CALLBACKS              #
def callback_release(userData: userDataObject = None):
    print("release callback")

# All buttons callbacks

#min   center  max  
#BTN0, BTN1,  BTN2 is for X-AXIS

def callback_btn0(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback.
            It has the alignment BoundBox.XMin 
    """
    if userDataObject is None:
        return
    linktocaller = userData.callerObject
    objs = linktocaller.selectedObj
    App.ActiveDocument.openTransaction(translate("Design456", "SmartAlign_btn0")) #Register Undo
    for i in range(0, len(objs)):
        if objs[i].Object.Shape.BoundBox.XMin != linktocaller.NewBoundary.XMin: 
            objs[i].Object.Placement.Base.x = linktocaller.NewBoundary.XMin+(objs[i].Object.Placement.Base.x-objs[i].Object.Shape.BoundBox.XMin)
    linktocaller.recreateAll()
    App.ActiveDocument.commitTransaction()  # undo reg.

def callback_btn1(userData: userDataObject = None):
    """
            This function run when Align is clicked 
            - event callback. 
            It has the alignment BoundBox.XCenter
    """
    if userData is None:
        return

    linktocaller = userData.callerObject
    objs = linktocaller.selectedObj
    App.ActiveDocument.openTransaction(translate("Design456", "SmartAlign_btn1")) #Register Undo
    for i in range(0, len(objs)):
        if objs[i].Object.Shape.BoundBox.Center.x != linktocaller.NewBoundary.Center.x:
            # assume that all objects must have BoundBox.Center == placement.base   
            objs[i].Object.Placement.Base.x = linktocaller.NewBoundary.Center.x+(objs[i].Object.Placement.Base.x-objs[i].Object.Shape.BoundBox.Center.x) #objs[i].Object.Shape.BoundBox.XMin+(linktocaller.NewBoundary.Center.x-objs[i].Object.Shape.BoundBox.Center.x)
    linktocaller.recreateAll()
    App.ActiveDocument.commitTransaction()  # undo reg.

def callback_btn2(userData: userDataObject = None):
    """
            This function run when Align is clicked 
            - event callback. 
            It has the alignment BoundBox.XMax
    """
    if userData is None:
        return

    linktocaller = userData.callerObject
    objs = linktocaller.selectedObj
    App.ActiveDocument.openTransaction(translate("Design456", "SmartAlign_btn2"))  #Register Undo
    for i in range(0, len(objs)):
        if objs[i].Object.Shape.BoundBox.XMax != linktocaller.NewBoundary.XMax: 
            objs[i].Object.Placement.Base.x = linktocaller.NewBoundary.XMax  +(objs[i].Object.Placement.Base.x-objs[i].Object.Shape.BoundBox.XMax)
    linktocaller.recreateAll()
    App.ActiveDocument.commitTransaction()  # undo reg.

 
#min   center  max     
#BTN3, BTN4, BTN5 is for Y-AXIS
def callback_btn3(userData: userDataObject = None):
    """
            This function run when Align is clicked 
            - event callback. 
            It has the alignment BoundBox.YMin 
 
    """
    if userData is None:
        return

    linktocaller = userData.callerObject
    objs = linktocaller.selectedObj
    App.ActiveDocument.openTransaction(translate("Design456", "SmartAlign_btn3")) #Register Undo
    for i in range(0, len(objs)): 
        if objs[i].Object.Shape.BoundBox.YMin != linktocaller.NewBoundary.YMin: 
            objs[i].Object.Placement.Base.y = linktocaller.NewBoundary.YMin+(objs[i].Object.Placement.Base.y-objs[i].Object.Shape.BoundBox.YMin)

    linktocaller.recreateAll()
    App.ActiveDocument.commitTransaction()  # undo reg.
    
def callback_btn4(userData: userDataObject = None):
    """
            This function run when Align is clicked 
            - event callback. 
            It has the alignment BoundBox.YCenter 

    """
    if userData is None:
        return

    linktocaller = userData.callerObject
    objs = linktocaller.selectedObj
    App.ActiveDocument.openTransaction(translate("Design456", "SmartAlign_btn4")) #Register Undo
    for i in range(0, len(objs)):
        if objs[i].Object.Shape.BoundBox.Center.y != linktocaller.NewBoundary.Center.y: 
            objs[i].Object.Placement.Base.y = linktocaller.NewBoundary.Center.y+(objs[i].Object.Placement.Base.y-objs[i].Object.Shape.BoundBox.Center.y)
    linktocaller.recreateAll()
    App.ActiveDocument.commitTransaction()  # undo reg.


def callback_btn5(userData: userDataObject = None):
    """
            This function run when Align is clicked 
            - event callback. 
            It has the alignment BoundBox.YMax
    """
    if userData is None:
        return

    linktocaller = userData.callerObject
    objs = linktocaller.selectedObj
    App.ActiveDocument.openTransaction(translate("Design456", "SmartAlign_btn5")) #Register Undo
    for i in range(0, len(objs)):
        if objs[i].Object.Shape.BoundBox.YMax != linktocaller.NewBoundary.YMax:
            objs[i].Object.Placement.Base.y = linktocaller.NewBoundary.YMax +(objs[i].Object.Placement.Base.y-objs[i].Object.Shape.BoundBox.YMax)
    linktocaller.recreateAll()
    App.ActiveDocument.commitTransaction()  # undo reg.

#min   center  max  
# BTN6, BTN7, BTN8 is for Z-Axis
def callback_btn6(userData: userDataObject = None):
    """
            This function run when Align is clicked 
            - event callback. 
            It has the alignment BoundBox.ZMin
    """
    if userData is None:
        return

    linktocaller = userData.callerObject
    objs = linktocaller.selectedObj
    App.ActiveDocument.openTransaction(translate("Design456", "SmartAlign_btn6")) #Register Undo
    for i in range(0, len(objs)):
        if objs[i].Object.Shape.BoundBox.ZMin != linktocaller.NewBoundary.ZMin: 
            objs[i].Object.Placement.Base.z = linktocaller.NewBoundary.ZMin+(objs[i].Object.Placement.Base.z-objs[i].Object.Shape.BoundBox.ZMin)
    linktocaller.recreateAll()
    App.ActiveDocument.commitTransaction()  # undo reg.



def callback_btn7(userData: userDataObject = None):
    """
            This function run when Align is clicked 
            - event callback. 
            It has the alignment BoundBox.ZCenter
    """
    if userData is None:
        return

    linktocaller = userData.callerObject
    objs = linktocaller.selectedObj
    App.ActiveDocument.openTransaction(translate("Design456", "SmartAlign_btn7")) #Register Undo
    for i in range(0, len(objs)):
        if objs[i].Object.Shape.BoundBox.Center.z != linktocaller.NewBoundary.Center.z: 
             objs[i].Object.Placement.Base.z = linktocaller.NewBoundary.Center.z+(objs[i].Object.Placement.Base.z-objs[i].Object.Shape.BoundBox.Center.z)
    linktocaller.recreateAll()
    App.ActiveDocument.commitTransaction()  # undo reg.


def callback_btn8(userData: userDataObject = None):
    """
            This function run when Align is clicked 
            - event callback. 
            It has the alignment BoundBox.ZMax
    """
    if userData is None:
        return

    linktocaller = userData.callerObject
    objs = linktocaller.selectedObj
    App.ActiveDocument.openTransaction(translate("Design456", "SmartAlign_btn8")) #Register Undo
    for i in range(0, len(objs)):
        if objs[i].Object.Shape.BoundBox.ZMax != linktocaller.NewBoundary.ZMax: 
            objs[i].Object.Placement.Base.z = linktocaller.NewBoundary.ZMax +(objs[i].Object.Placement.Base.z-objs[i].Object.Shape.BoundBox.ZMax)
    linktocaller.recreateAll()
    App.ActiveDocument.commitTransaction()  # undo reg.


#                          END OF CALLBACKS                              #


class Design456_SmartAlignment:
    """
        Apply Alignment to any 3D object by selecting the objects 
        Press any button to alignment the objects
    """

    def __init__(self):
        self._vector = App.Vector(0.0, 0.0, 0.0)  # not used dummy value
        self.mw = None
        self.dialog = None
        self.tab = None
        self.smartInd = None
        self._mywin = None
        self.b1 = None
        self.endVector = None
        self.startVector = None
        # We will make two object, one for visual effect and the other is the original
        self.selectedObj = []
        # 0 is the original    1 is the fake one (just for interactive effect)
        self.objectType = None  # Either shape, Face or Edge.
        self.NewBoundary = None
        self.savedColors = []
        self.DocObserver = None


    def CalculateBoundary(self):
        Results = []
        _min = self.selectedObj[0].Object.Shape.BoundBox.XMin
        for i in range(1, len(self.selectedObj)):
            if self.selectedObj[i].Object.Shape.BoundBox.XMin < _min :
                _min = self.selectedObj[i].Object.Shape.BoundBox.XMin
        Results.append(_min)

        _min = self.selectedObj[0].Object.Shape.BoundBox.YMin
        for i in range(1, len(self.selectedObj)):
            if self.selectedObj[i].Object.Shape.BoundBox.YMin < _min :
                _min = self.selectedObj[i].Object.Shape.BoundBox.YMin
        Results.append(_min)
        _min = self.selectedObj[0].Object.Shape.BoundBox.ZMin
        for i in range(1, len(self.selectedObj)):
            if self.selectedObj[i].Object.Shape.BoundBox.ZMin < _min :
                _min = self.selectedObj[i].Object.Shape.BoundBox.ZMin
        Results.append(_min)
        _max = self.selectedObj[0].Object.Shape.BoundBox.XMax
        for i in range(1, len(self.selectedObj)):
            if self.selectedObj[i].Object.Shape.BoundBox.XMax > _max :
                _max = self.selectedObj[i].Object.Shape.BoundBox.XMax
        Results.append(_max)
        _max = self.selectedObj[0].Object.Shape.BoundBox.YMax
        for i in range(1, len(self.selectedObj)):
            if self.selectedObj[i].Object.Shape.BoundBox.YMax > _max :
                _max = self.selectedObj[i].Object.Shape.BoundBox.YMax
        Results.append(_max)        
        _max = self.selectedObj[0].Object.Shape.BoundBox.ZMax
        for i in range(1, len(self.selectedObj)):
            if self.selectedObj[i].Object.Shape.BoundBox.ZMax > _max :
                _max = self.selectedObj[i].Object.Shape.BoundBox.ZMax
        Results.append(_max)
        XMin = Results[0]
        YMin = Results[1]
        ZMin = Results[2]
        XMax = Results[3]
        YMax = Results[4]
        ZMax = Results[5]
        # App.BoundBox([Xmin,Ymin,Zmin,Xmax,Ymax,Zmax])
        if self.NewBoundary is not None:
            try:
                del self.NewBoundary
            except:
                pass
        self.NewBoundary = App.BoundBox(XMin, YMin, ZMin, XMax, YMax, ZMax)

    def recreateAll(self):
        self.CalculateBoundary()
        self.savedColors = [self.selectedObj[0].Object.ViewObject.DiffuseColor,
                            self.selectedObj[1].Object.ViewObject.DiffuseColor]
        if self.smartInd is not None:
            self.smartInd.setBoundary(self.NewBoundary)
            self.smartInd.redraw()

    def Activated(self):
        import ThreeDWidgets.fr_coinwindow as win
        self.selectedObj.clear()
        sel = Gui.Selection.getSelectionEx()
        if len(sel) < 2:
            # An object must be selected
            errMessage = "Select at least two objects to Align them"
            faced.errorDialog(errMessage)
            return
        #Observer to capture events
        self.DocObserver= SmartAlignObserver(self)
        App.addDocumentObserver(self.DocObserver)
        
        self.selectedObj = sel
        self.recreateAll()
        self.smartInd = Fr_Align_Widget(self.NewBoundary, ["Align Tool", ])

        self.smartInd.w_callback_ = callback_release
        self.smartInd.w_btnCallbacks_ = [callback_btn0,
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
            e1 = QtGui.QLabel(
                "(Smart Alignment)\nAlign objects to the same\nposition by pressing the round buttons")
            commentFont = QtGui.QFont("Times", 12, True)
            e1.setFont(commentFont)
            la.addWidget(e1)
            okbox = QtGui.QDialogButtonBox(self.dialog)
            okbox.setOrientation(QtCore.Qt.Horizontal)
            okbox.setStandardButtons(
                QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
            la.addWidget(okbox)
            QtCore.QObject.connect(
                okbox, QtCore.SIGNAL("accepted()"), self.hide)

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
        try:
            App.removeDocumentObserver(self.DocObserver)
            self.dialog.hide()
            del self.dialog
            dw = self.mw.findChildren(QtGui.QDockWidget)
            newsize = self.tab.count()  # Todo : Should we do that?
            self.tab.removeTab(newsize-1)  # it ==0,1,2,3 ..etc

            App.ActiveDocument.recompute()
            faced.showFirstTab()
            self.__del__()  # Remove all smart Alignment 3dCOIN widgets
            
        except Exception as err:
            App.Console.PrintError("'Design456_Alignment' getMainWindow-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_SmartAlignment.svg',
            'MenuText': ' Smart Alignment',
                        'ToolTip':  ' Smart Alignment'
        }


Gui.addCommand('Design456_SmartAlignment', Design456_SmartAlignment())
