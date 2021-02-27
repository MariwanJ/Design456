# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *																		   *
# *	This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *																		   *
# *	Copyright (C) 2021													   *
# *																		   *
# *																		   *
# *	This library is free software; you can redistribute it and/or		   *
# *	modify it under the terms of the GNU Lesser General Public			   *
# *	License as published by the Free Software Foundation; either		   *
# *	version 2 of the License, or (at your option) any later version.	   *
# *																		   *
# *	This library is distributed in the hope that it will be useful,		   *
# *	but WITHOUT ANY WARRANTY; without even the implied warranty of		   *
# *	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU	   *
# *	Lesser General Public License for more details.						   *
# *																		   *
# *	You should have received a copy of the GNU Lesser General Public	   *
# *	License along with this library; if not, If not, see				   *
# *	<http://www.gnu.org/licenses/>.										   *
# *																		   *
# *	Author : Mariwan Jalal	 mariwan.jalal@gmail.com					   *
# **************************************************************************
import os
import sys
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft as _draft
import Part as _part
import FACE_D as faced

# Toolbar class
"""Design456_Alignment"""

class Design456_Alignment:
    list = ["Design456_AlignToPlane",
            "Design456_TopSideView",
            "Design456_BottomView",
            "Design456_LeftSideView",
            "Design456_RightSideView",
            "Design456_FrontSideView",
            "Design456_BackSideView"
            

            ]

    def Activated(self):
        self.appendToolbar("Design456_Alignment", self.list)

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/Alignments.svg',
            'MenuText': 'Alignments',
            'ToolTip':	'Alignments'
        }


# Object Alignment
class Design456_AlignFlatToPlane:
    def Activated(self):
        try:
            Selectedobjects = Gui.Selection.getSelectionEx()
            #This must be modified
            for eachObj in Selectedobjects:
                eachObj.Object.Placement.Base.z = 0.0
                
        except Exception as err:
            App.Console.PrintError("'Design456_Extract' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/AlignToPlane.svg',
            'MenuText': '2Ddrawing',
            'ToolTip':	'2Ddrawing'
        }
        
Gui.addCommand('Design456_AlignToPlane',Design456_AlignFlatToPlane())

# Plane Alignments

#Top
class Design456_TopSideView:
    def Activated(self):
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, 1.0), 0.0)
        Gui.activeDocument().activeView().viewTop()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/TopSideView.svg',
            'MenuText': 'Top Side View',
            'ToolTip':	'Top Side View'
            }

Gui.addCommand('Design456_TopSideView',Design456_TopSideView())

#Bottom View
class Design456_BottomView:
    def Activated(self):
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, -1.0), 0.0)
        Gui.activeDocument().activeView().viewBottom()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/BottomSideView.svg',
            'MenuText': 'Bottom Side View',
            'ToolTip':	'Bottom Side View'
            }

Gui.addCommand('Design456_BottomView',Design456_BottomView())

#Left
class Design456_LeftSideView:
    def Activated(self):
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(1.0,0.0 , 0.0), 0.0)
        Gui.activeDocument().activeView().viewLeft()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/LeftSideView.svg',
            'MenuText': 'Left Side View',
            'ToolTip':	'Left Side View'
            }

Gui.addCommand('Design456_LeftSideView',Design456_LeftSideView())

#Right
class Design456_RightSideView:
    def Activated(self):
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(-1.0, 0.0, 0.0), 0.0)
        Gui.activeDocument().activeView().viewRight()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/RightSideView.svg',
            'MenuText': 'Right Side View',
            'ToolTip':	'Right Side View'
            }

Gui.addCommand('Design456_RightSideView',Design456_RightSideView())

#Front
class Design456_FrontSideView:
    def Activated(self):
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0,1.0, 0.0), 0.0)
        Gui.activeDocument().activeView().viewFront()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/FrontSideView.svg',
            'MenuText': 'Front Side View',
            'ToolTip':	'Front Side View'
            }

Gui.addCommand('Design456_FrontSideView',Design456_FrontSideView())

#Back
class Design456_BackSideView:
    def Activated(self):
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, -1.0, 0.0), 0.0)
        Gui.activeDocument().activeView().viewRear()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/BacktSideView.svg',
            'MenuText': 'Backside View',
            'ToolTip':	'BackSide View'
            }

Gui.addCommand('Design456_BackSideView',Design456_BackSideView())


class Ui_dlgDesign456_Move(object):
    def __init__(self, dlgDesign456_Move):
            self.window = dlgDesign456_Move

    def setupUi(self, dlgDesign456_Move):
        dlgDesign456_Move.setObjectName("dlgDesign456_Move")
        dlgDesign456_Move.resize(443, 368)
        dlgDesign456_Move.setWindowOpacity(23.0)
        self.buttonBox = QtGui.QDialogButtonBox(dlgDesign456_Move)
        self.buttonBox.setGeometry(QtCore.QRect(270, 340, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.dialX = QtGui.QDial(dlgDesign456_Move)
        self.dialX.setGeometry(QtCore.QRect(10, 20, 161, 151))
        self.dialX.setMaximum(360)
        self.dialX.setPageStep(5)
        self.dialX.setOrientation(QtCore.Qt.Vertical)
        self.dialX.setInvertedAppearance(True)
        self.dialX.setInvertedControls(False)
        self.dialX.setWrapping(True)
        self.dialX.setNotchesVisible(True)
        self.dialX.setObjectName("dialX")
        self.DialY = QtGui.QDial(dlgDesign456_Move)
        self.DialY.setGeometry(QtCore.QRect(240, 20, 161, 151))
        self.DialY.setMaximum(360)
        self.DialY.setPageStep(5)
        self.DialY.setOrientation(QtCore.Qt.Vertical)
        self.DialY.setInvertedAppearance(True)
        self.DialY.setInvertedControls(False)
        self.DialY.setWrapping(True)
        self.DialY.setNotchesVisible(True)
        self.DialY.setObjectName("DialY")
        self.DialZ = QtGui.QDial(dlgDesign456_Move)
        self.DialZ.setGeometry(QtCore.QRect(110, 170, 161, 151))
        self.DialZ.setMaximum(360)
        self.DialZ.setPageStep(5)
        self.DialZ.setOrientation(QtCore.Qt.Vertical)
        self.DialZ.setInvertedAppearance(True)
        self.DialZ.setInvertedControls(False)
        self.DialZ.setWrapping(True)
        self.DialZ.setNotchesVisible(True)
        self.DialZ.setObjectName("DialZ")
        self.lblX = QtGui.QLabel(dlgDesign456_Move)
        self.lblX.setGeometry(QtCore.QRect(60, 0, 54, 17))
        self.lblX.setObjectName("lblX")
        self.lblY = QtGui.QLabel(dlgDesign456_Move)
        self.lblY.setGeometry(QtCore.QRect(290, 0, 54, 17))
        self.lblY.setObjectName("lblY")
        self.lblZ = QtGui.QLabel(dlgDesign456_Move)
        self.lblZ.setGeometry(QtCore.QRect(160, 150, 54, 17))
        self.lblZ.setObjectName("lblZ")
        self.lblValueX = QtGui.QLabel(dlgDesign456_Move)
        self.lblValueX.setGeometry(QtCore.QRect(60, 180, 54, 17))
        self.lblValueX.setAlignment(QtCore.Qt.AlignCenter)
        self.lblValueX.setObjectName("lblValueX")
        self.lblValueY = QtGui.QLabel(dlgDesign456_Move)
        self.lblValueY.setGeometry(QtCore.QRect(290, 180, 54, 17))
        self.lblValueY.setAlignment(QtCore.Qt.AlignCenter)
        self.lblValueY.setObjectName("lblValueY")
        self.lblValueZ = QtGui.QLabel(dlgDesign456_Move)
        self.lblValueZ.setGeometry(QtCore.QRect(160, 320, 54, 17))
        self.lblValueZ.setAlignment(QtCore.Qt.AlignCenter)
        self.lblValueZ.setObjectName("lblValueZ")

        self.retranslateUi(dlgDesign456_Move)
        #self.buttonBox.accepted.connect(dlgDesign456_Move.accept)
        #self.buttonBox.rejected.connect(dlgDesign456_Move.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgDesign456_Move)

    def retranslateUi(self, dlgDesign456_Move):
        _translate = QtCore.QCoreApplication.translate
        dlgDesign456_Move.setWindowTitle(_translate("dlgDesign456_Move", "Design456 Move"))
        self.lblX.setText(_translate("dlgDesign456_Move", "X: Angle"))
        self.lblY.setText(_translate("dlgDesign456_Move", "Y: Angle"))
        self.lblZ.setText(_translate("dlgDesign456_Move", "Z: Angle"))
        self.lblValueX.setText(_translate("dlgDesign456_Move", "0"))
        self.lblValueY.setText(_translate("dlgDesign456_Move", "0"))
        self.lblValueZ.setText(_translate("dlgDesign456_Move", "0"))





#Design456 Move implementation 
class Design456_MoveObject:
    
    def __init__(self):
        self.d = QtGui.QWidget()
        self.ui = Ui_dlgDesign456_Move(self)
        self.ui.setupUi(self.d)
    def accept(self):
        return
    
    def reject(self):
        return
    
    def runClass(self):
        try:
            sel = Gui.Selection.getSelection()
            self.ui.setupUi()
            return
    

     
        except Exception as err:
            App.Console.PrintError("'Design456_loftOnDirection' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno) 
                              
    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':	 Design456Init.ICON_PATH + '/Design456_Move.svg',
            'MenuText': 'Design456 Move',
            'ToolTip':	'Design456 Move'
            }
Gui.addCommand('Design456_MoveObject', Design456_MoveObject())