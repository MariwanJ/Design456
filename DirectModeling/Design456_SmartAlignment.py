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
import Draft
import Part
from pivy import coin
import FACE_D as faced
from PySide.QtCore import QT_TRANSLATE_NOOP
import ThreeDWidgets.fr_coinwindow as win
from ThreeDWidgets import fr_coin3d
from typing import List
import Design456Init
from PySide import QtGui, QtCore
from ThreeDWidgets.fr_arrow_widget import Fr_Arrow_Widget
from ThreeDWidgets import fr_arrow_widget
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from draftutils.translate import translate  # for translate
import math
from ThreeDWidgets import fr_label_draw
MouseScaleFactor = 1.5      # The ration of delta mouse to mm  #TODO :FIXME : Which value we should choose? 


#TODO: FIXME : NOT IMPLEMENTED

def callback_move(userData: fr_arrow_widget.userDataObject = None):
    """[summary]
    Callback for the arrow movement. This will be used to calculate the radius of the Alignment operation.
    Args:
        userData (fr_arrow_widget.userDataObject, optional): [description]. Defaults to None.

    Returns:
        [type]: [description] None.
    """
    try:
        if userData is None:
            return  # Nothing to do here - shouldn't be None
        mouseToArrowDiff = 0.0

        ArrowObject = userData.ArrowObj
        events = userData.events
        linktocaller = userData.callerObject
        if type(events) != int:
            return

        clickwdgdNode = fr_coin3d.objectMouseClick_Coin3d(ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                                                          ArrowObject.w_pick_radius, ArrowObject.w_widgetSoNodes)
        clickwdglblNode = fr_coin3d.objectMouseClick_Coin3d(ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                                                            ArrowObject.w_pick_radius, ArrowObject.w_widgetlblSoNodes)
        linktocaller.endVector = App.Vector(ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_x,
                                            ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_y,
                                            ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_z)

        if clickwdgdNode is None and clickwdglblNode is None:
            if linktocaller.run_Once is False:
                print("click move")
                return 0  # nothing to do
            

    except Exception as err:
        App.Console.PrintError("'View Inside objects' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def callback_release(userData: fr_arrow_widget.userDataObject = None):
    """
       Callback after releasing the left mouse button. 
       This callback will finalize the Alignment operation. 
       Deleting the original object will be done when the user press 'OK' button
    """
    if (userData is None):
        print("userData is None")
        raise TypeError 
        

class Design456_SmartAlignment:
    """
        Apply Alignment to any 3D object by selecting the object, a Face or one or multiple edges 
        Radius of the Alignment is counted by dragging the arrow towards the negative Z axis.
    """
    _vector = App.Vector(0.0, 0.0, 0.0)
    mw = None
    dialog = None
    tab = None
    smartInd = None
    _mywin = None
    b1 = None
    AlignmentLBL = None
    run_Once = False
    endVector = None
    startVector = None
    # We will make two object, one for visual effect and the other is the original
    selectedObj = []
    # 0 is the original    1 is the fake one (just for interactive effect)
    mouseToArrowDiff = 0.0
    offset=0.0
    AwayFrom3DObject = 10  # Use this to take away the arrow from the object
    AlignmentRadius = 0.00001   #We cannot have zero. TODO: What value we should use? FIXME:
    objectType = None  # Either shape, Face or Edge.
    Originalname = ''
    direction=None

 
    def Activated(self):
        self.selectedObj.clear()
        sel=Gui.Selection.getSelectionEx()
        if len(sel) ==0:
            # An object must be selected
            errMessage = "Select an object, one face or one edge to Alignment"
            faced.errorDialog(errMessage)
            return

        self.selectedObj.append(sel[0])
        self.Originalname = self.selectedObj[0].Object.Name

 
 
        self.smartInd.w_callback_ = callback_release
        self.smartInd.w_move_callback_ = callback_move
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
            if self._mywin != None:
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
            'Pixmap': Design456Init.ICON_PATH + 'Design456_Alignment.svg',
            'MenuText': ' Smart Alignment',
                        'ToolTip':  ' Smart Alignment'
        }

Gui.addCommand('Design456_SmartAlignment', Design456_SmartAlignment())
