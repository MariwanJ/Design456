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

import os,sys
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
from  ThreeDWidgets import fr_label_draw

def fillet_callback_move(test):
    print("callback")


class Design456_SmartFillet:
    """
        Apply fillet to an edge using mouse movement.
        Moving an arrow that will represent radius of the fillet.
    """
    _vector=App.Vector(0.0,0.0,0.0)
    selectedObject=None
    mw = None
    dialog = None
    tab = None
    smartInd =None
    _mywin = None
    b1 = None
    scaleLBL = None
    run_Once = False

    def getArrowPosition(self,objType:str=''):
        """"
        Args:
            objType (str, optional): [description]. Defaults to ''.
        
        Find out the vector and rotation of the arrow to be drawn.
        """
        try:
            vectors=self.selectedObject.SubObjects[0].Vertexes
            if objType=='Face':
                self._vector.z=vectors[0].Z
                for i in vectors:
                    self._vector.x+=i.X
                    self._vector.y+=i.Y
                    if self._vector.z<i.Z:
                        self._vector.z=i.Z
                self._vector.x=self._vector.x/4
                self._vector.y=self._vector.y/4

                rotation= [self.selectedObject.SubObjects[0].Faces[0].Surface.Rotation.Axis.x,
                                       self.selectedObject.SubObjects[0].Faces[0].Surface.Rotation.Axis.y,
                                       self.selectedObject.SubObjects[0].Faces[0].Surface.Rotation.Axis.z,self.selectedObject.SubObjects[0].Faces[0].Surface.Rotation.Angle]
                print(rotation)

            elif objType=='Edge':
                #An edge is selected
                self._vector.z=vectors[0].Z
                for i in vectors:
                    self._vector.x+=i.X
                    self._vector.y+=i.Y
                    self._vector.z+=i.Z
                self._vector.x=self._vector.x/2
                self._vector.y=self._vector.y/2
                self._vector.z=self._vector.z/2+0.5*self._vector.z
                
                rotation= [self.selectedObject.SubObjects[0].Placement.Rotation.Axis.x,
                                         self.selectedObject.SubObjects[0].Placement.Rotation.Axis.y,
                                         self.selectedObject.SubObjects[0].Placement.Rotation.Axis.z,math.radians(120)]

            elif objType=='Shape':
                #The whole object is selected
                print("shape")
                
                rotation = [-1.0, 0.0,0.0, math.radians(120) ]
            return rotation     
        except Exception as err:
            App.Console.PrintError("'Design456_SmartFillet' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

    def Activated(self):
        self.selectedObject=Gui.Selection.getSelectionEx()
        if len(self.selectedObject) != 1:
            # Only one object must be self.selectedObj
            errMessage = "Select one object, one face or one edge to fillet"
            faced.getInfo().errorDialog(errMessage)
            return
        
        self.selectedObject=self.selectedObject[0]
        if self.selectedObject.HasSubObjects!=True:
            #we have the whole object. Find all edges that should be fillet.
            rotation = self.getArrowPosition('Shape')
        subObj=self.selectedObject.SubObjects[0]
        if subObj.ShapeType=='Face':
            #We have a face
            rotation = self.getArrowPosition('Face')
        elif subObj.ShapeType=='Edge':
            #Only one edge
            rotation=self.getArrowPosition('Edge')
        else:
            errMessage = "Select and object, a face or an edge to fillet"
            faced.getInfo().errorDialog(errMessage)
            return
        
        self.smartInd=Fr_Arrow_Widget(self._vector,"Fillet", 1, FR_COLOR.FR_OLIVEDRAB, rotation)

        if self._mywin == None:
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
        except Exception as err:
            App.Console.PrintError("'Design456_SmartFillet' Failed. "
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
            if self.mw == None:
                raise Exception("No main window found")
            dw = self.mw.findChildren(QtGui.QDockWidget)
            for i in dw:
                if str(i.objectName()) == "Combo View":
                    self.tab = i.findChild(QtGui.QTabWidget)
                elif str(i.objectName()) == "Python Console":
                    self.tab = i.findChild(QtGui.QTabWidget)
            if self.tab == None:
                raise Exception("No tab widget found")

            self.dialog = QtGui.QDialog()
            oldsize = self.tab.count()
            self.tab.addTab(self.dialog, "Smart Fillet")
            self.tab.setCurrentWidget(self.dialog)
            self.dialog.resize(200, 450)
            self.dialog.setWindowTitle("Smart Fillet")
            la = QtGui.QVBoxLayout(self.dialog)
            e1 = QtGui.QLabel("(Smart Fillet)\nFor quicker\nApplying Fillet")
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
            App.Console.PrintError("'Design456_Fillet' Failed. "
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
        self.tab.removeTab(newsize-1)  # it is 0,1,2,3 ..etc
        self.__del__()  # Remove all smart scale 3dCOIN widgets

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'PartDesign_Fillet.svg',
            'MenuText': 'Direct Scale',
                        'ToolTip':  'Direct Scale'
        }


Gui.addCommand('Design456_SmartFillet', Design456_SmartFillet())
