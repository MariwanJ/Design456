# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *                                                                         *
# *                                                                         *
# *  This library is free software; you can redistribute it and/or          *
# *  modify it under the terms of the GNU Lesser General Public             *
# *  License as published by the Free Software Foundation; either           *
# *  version 2 of the License, or (at your option) any later version.       *
# *                                                                         *
# *  This library is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *  MERCHANTABILITY or FITNESS FOR A PartICULAR PURPOSE.  See the GNU      *
# *  Lesser General Public License for more details.                        *
# *                                                                         *
# *  You should have received a copy of the GNU Lesser General Public       *
# *  License along with this library; if not, If not, see                   *
# *  <http://www.gnu.org/licenses/>.                                        *
# *                                                                         *
# *  Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# ***************************************************************************
# *This command is inpired and suggested by Mario52, modified by Mariwan Jalal
# *https://forum.freecadweb.org/viewtopic.php?f=22&t=46690&sid=18c0765424496ef734ce5b78914f7197
# *https://forum.freecadweb.org/viewtopic.php?f=13&t=48276&p=413611#p413611
# *https://forum.freecadweb.org/viewtopic.php?f=13&t=48276&p=414467#p414467
# *https://forum.freecadweb.org/viewtopic.php?f=22&t=48425
# *mario52
# *25/05/2020 03/07/2020 07/07/2020 15/07/2020
# *
# *converted the code  to a class and added to Design456 by Mariwan Jalal
# * as requested by the Macro author (mario52)
# *Please notice that the usage of this command should be studied.
# *We need to figure out what is the best way to use it.
# *https://forum.freecadweb.org/viewtopic.php?f=22&t=48425
# *https://forum.freecadweb.org/viewtopic.php?f=8&t=54893&start=10

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft as _draft
import Part as _part
import BOPTools.SplitFeatures as SPLIT
import FACE_D as faced

class Design456_loftOnDirection_ui(object):
    def __init__(self, loftOnDirection):
        self.window = loftOnDirection

    def setupUi(self, loftOnDirection):
        self.window = loftOnDirection
        loftOnDirection.setObjectName("Loft On Direction")
        loftOnDirection.resize(300, 250)
        self.chkLoft = QtGui.QCheckBox(loftOnDirection)
        self.chkLoft.setGeometry(QtCore.QRect(160, 70, 82, 23))
        self.chkLoft.setObjectName("chkLoft")
        self.chkAxis = QtGui.QCheckBox(loftOnDirection)
        self.chkAxis.setGeometry(QtCore.QRect(160, 90, 82, 23))
        self.chkAxis.setObjectName("chkAxis")
        self.btnOK = QtGui.QPushButton(loftOnDirection)
        self.btnOK.setGeometry(QtCore.QRect(160, 130, 80, 25))
        self.btnOK.setDefault(True)
        self.btnOK.setObjectName("btnOK")
        self.btnCancel = QtGui.QPushButton(loftOnDirection)
        self.btnCancel.setGeometry(QtCore.QRect(160, 160, 80, 25))
        self.btnCancel.setObjectName("btnCancel")
        self.layoutWidget = QtGui.QWidget(loftOnDirection)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 136, 151))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblLength = QtGui.QLabel(self.layoutWidget)
        self.lblLength.setObjectName("lblLength")
        self.verticalLayout.addWidget(self.lblLength)
        self.lblScaleX = QtGui.QLabel(self.layoutWidget)
        self.lblScaleX.setObjectName("lblScaleX")
        self.verticalLayout.addWidget(self.lblScaleX)
        self.lblScaleY = QtGui.QLabel(self.layoutWidget)
        self.lblScaleY.setObjectName("lblScaleY")
        self.verticalLayout.addWidget(self.lblScaleY)
        self.lblScaleZ = QtGui.QLabel(self.layoutWidget)
        self.lblScaleZ.setObjectName("lblScaleZ")
        self.verticalLayout.addWidget(self.lblScaleZ)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.inLength = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.inLength.setRange(-100000.0, 100000.0)
        self.inLength.setObjectName("inLength")
        self.verticalLayout_2.addWidget(self.inLength)
        self.inScaleX = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.inScaleX.setRange(-100000.0, 100000.0)
        self.inScaleX.setObjectName("inScaleX")
        self.verticalLayout_2.addWidget(self.inScaleX)
        self.inScaleY = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.inScaleY.setRange(-100000.0, 100000.0)
        self.inScaleY.setObjectName("inScaleY")
        self.verticalLayout_2.addWidget(self.inScaleY)
        self.inScaleZ = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.inScaleZ.setRange(-100000.0, 100000.0)
        self.inScaleZ.setObjectName("inScaleZ")

        # Default Values
        self.chkAxis.setChecked(0)
        self.chkLoft.setChecked(1)

        self.verticalLayout_2.addWidget(self.inScaleZ)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.retranslateUi(loftOnDirection)
        QtCore.QMetaObject.connectSlotsByName(loftOnDirection)

    def GetOut(self):

        self.window.hide()

    def retranslateUi(self, loftOnDirection):
        _translate = QtCore.QCoreApplication.translate
        loftOnDirection.setWindowTitle(_translate(
            "loftOnDirection", "loftOnDirection"))
        self.btnCancel.setText(_translate("loftOnDirection", "Cancel"))
        self.label_5.setText(_translate(
            "loftOnDirection", "Select Change variables"))
        loftOnDirection.setWindowTitle(_translate(
            "loftOnDirection", "Loft On Direction"))
        self.btnOK.setText(_translate("loftOnDirection", "OK"))
        self.btnCancel.setText(_translate("loftOnDirection", "Cancel"))

        self.lblLength.setText(_translate("loftOnDirection", "Length"))
        self.lblScaleX.setText(_translate("loftOnDirection", "ScaleX"))
        self.lblScaleY.setText(_translate("loftOnDirection", "ScaleY"))
        self.lblScaleZ.setText(_translate("loftOnDirection", "ScaleZ"))
        self.chkLoft.setText(_translate("loftOnDirection", "Loft"))
        self.chkAxis.setText(_translate("loftOnDirection", "Axis"))

        QtCore.QObject.connect(
            self.btnOK, QtCore.SIGNAL("accepted()"), self.runClass)
        QtCore.QObject.connect(
            self.btnOK, QtCore.SIGNAL("pressed()"), self.runClass)
        QtCore.QObject.connect(
            self.btnCancel, QtCore.SIGNAL("accepted()"), self.GetOut)
        QtCore.QMetaObject.connectSlotsByName(loftOnDirection)

    def msgBOXShow(self):
        # Create a simple loftOnDirection QMessageBox
        msg = "Wrong object"
        diag = QtGui.QMessageBox(
            QtGui.QMessageBox.Warning, '2D Shape selected', msg)
        diag.setWindowModality(QtCore.Qt.ApplicationModal)
        self.GetOut()
        diag.exec_()

        """msg = 'Example of warning message'
        errorloftOnDirection(msg)
        raise(Exception(msg))
        """

    def checkIfShapeIsValid(self):
        geTobject = Gui.Selection.getSelectionEx()[0]
        selectedEdge = geTobject.SubObjects[0]      # select one element
        """This must be fixed. I don't know how to distinguish between 2s and 3d objects.
        I will return for now always 0 but this MUST BE FIXED.2021-02-03 Mariwan
        if(selectedEdge.Volume ==0):
                #We have a 2D shape .. 
                self.msgBOXShow()
                return 1
            else:
                return 0
            """

    def runClass(self):
        try:
            sel = Gui.Selection.getSelectionEx()
            if(len(sel) <1 or len(sel)>1 or 
               len(Gui.Selection.getSelectionEx()[0].SubElementNames)==0):
                # Two object must be selected
                errMessage = "Select a face to use LoftOnDirection Tool"
                faced.getInfo(sel[0]).errorDialog(errMessage)
                return
    
            selectedEdge = Gui.Selection.getSelectionEx(
            )[0].SubObjects[0]    # select one element
            SubElementName = Gui.Selection.getSelectionEx()[
                0].SubElementNames[0]
            

            #### configuration ####
            ValueLength = -(float)(self.inLength.value())
            ValueScaleX = (float)(self.inScaleX.value())
            ValueScaleY = (float)(self.inScaleY.value())
            ValueScaleZ = (float)(self.inScaleZ.value())

            ####
            createAxis = self.chkAxis.isChecked()          # 0 = not Axis, other = Axis
            createLoft = self.chkLoft.isChecked()          # 0 = not loft, other = loft
            #### configuration ####

            if hasattr(selectedEdge, 'Surface'):
                plr = plDirection = App.Placement()

                # section direction
                yL = selectedEdge.CenterOfMass
                uv = selectedEdge.Surface.parameter(yL)
                nv = selectedEdge.normalAt(uv[0], uv[1])
                direction = yL.sub(nv + yL)
                r = App.Rotation(App.Vector(0, 0, 0), direction)
                plDirection.Rotation.Q = r.Q
                #print(r.Q)
                plDirection.Base = yL
                plr = plDirection
                #print("surface : ", sel[0].Name, " ",SubElementName, "  ", direction)
                # section direction

                # section axis
                if createAxis != 0:
                    # section axis
                    points = [App.Vector(0.0, 0.0, 0.0), App.Vector(
                        0.0, 0.0, ValueLength)]
                    centerX = _draft.makeWire(
                        points, closed=False, face=False, support=None)
                    centerX.Placement = plr
                    centerX.Label = "Axis_" + SubElementName
                    # section axis

                #### section scale ####
                if createLoft != 0:
                    #### section scale ####
                    _part.show(selectedEdge.copy())
                    firstFace = App.ActiveDocument.ActiveObject
                    objClone = _draft.scale(firstFace, App.Vector(
                        ValueScaleX, ValueScaleY, ValueScaleZ), center=App.Vector(plDirection.Base), copy=True)  # False

                    # section placement face in length and direction
                    newLocation = (App.Vector(direction).scale(
                        ValueLength, ValueLength, ValueLength))
                    if (direction.x != 0 and abs(direction.x)==direction.x):
                        newLocation.x = newLocation.x+selectedEdge.Placement.Base.x*direction.x
                    elif (direction.x != 0 and abs(direction.x)!=direction.x):
                        newLocation.x = newLocation.x-selectedEdge.Placement.Base.x*direction.x
                    else:
                        newLocation.x = selectedEdge.Placement.Base.x
                    if (direction.y != 0 and abs(direction.y)==direction.y): #positive >0
                        newLocation.y = newLocation.y+selectedEdge.Placement.Base.y*direction.y
                    elif (direction.y != 0 and abs(direction.x)!=direction.y): #negative <0
                        newLocation.y = newLocation.y-selectedEdge.Placement.Base.y*direction.y
                    else:
                        newLocation.y = selectedEdge.Placement.Base.y
                    if (direction.z != 0 and abs(direction.z)==direction.z):
                        newLocation.z = newLocation.z+selectedEdge.Placement.Base.z*direction.z
                    elif (direction.z != 0 and abs(direction.z)!=direction.z): #negative <0:
                        newLocation.z = newLocation.z-selectedEdge.Placement.Base.z*direction.z
                    else:
                        newLocation.z = selectedEdge.Placement.Base.z
                    objClone.Placement.Base = newLocation
                    
                    
                    # section loft
                    newObj = App.ActiveDocument.addObject('Part::Loft', 'Loft')
                    App.ActiveDocument.ActiveObject.Sections = [App.ActiveDocument.getObject(
                        firstFace.Name), App.ActiveDocument.getObject(objClone.Name), ]
                    App.ActiveDocument.ActiveObject.Solid = True
                    newObj = App.ActiveDocument.ActiveObject
                    App.ActiveDocument.recompute()

                    # copy
                    App.ActiveDocument.addObject('Part::Feature', newObj.Name+'N').Shape = _part.getShape(
                        newObj, '', needSubElement=False, refine=True)
                    App.ActiveDocument.recompute()

                    # Remove Old objects. I don't like to keep so many objects without any necessity.
                    
                    for obj in newObj.Sections:
                        App.ActiveDocument.removeObject(obj.Name)
                    App.ActiveDocument.removeObject(newObj.Name)
                    App.ActiveDocument.recompute()
                    
                    # section hidden faces work
            self.window.hide()
        except Exception as err:
            App.Console.PrintError("'Design456_loftOnDirection' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class Design456_loftOnDirection():
    def __init__(self):
        self.d = QtGui.QWidget()
        self.ui = Design456_loftOnDirection_ui(self)
        self.ui.setupUi(self.d)

    def Activated(self):
        self.d.setWindowModality(QtCore.Qt.ApplicationModal)
        if(self.ui.checkIfShapeIsValid() == 1):
            return
        self.d.show()

    def GetResources(self):
        return{
            'Pixmap':   Design456Init.ICON_PATH +'loftOnDirection.svg',
            'MenuText': 'loftOnDirection',
            'ToolTip':  'Loft On Direction'
        }


Gui.addCommand('Design456_loftOnDirection', Design456_loftOnDirection())
