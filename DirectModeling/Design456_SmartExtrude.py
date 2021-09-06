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
# The ration of delta mouse to mm  #TODO :FIXME : Which value we should choose?
MouseScaleFactor = 1

'''
    We have to recreate the object each time we change the radius. 
    This means that the redrawing must be optimized 
'''


def callback_move(userData: fr_arrow_widget.userDataObject = None):
    """[summary]
    Callback for the arrow movement. This will be used to calculate the radius of the Extrude operation.
    Args:
        userData (fr_arrow_widget.userDataObject, optional): [description]. Defaults to None.

    Returns:
        [type]: [description] None.
    """
    try:
        if userData is None:
            return  # Nothing to do here - shouldn't be None

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
            if linktocaller.run_Once == False:
                print("click move")
                return 0  # nothing to do

        if linktocaller.run_Once == False:
            linktocaller.run_Once = True
            # only once
            linktocaller.startVector = linktocaller.endVector

        linktocaller.extrudeLength = (
            linktocaller.endVector-linktocaller.startVector).dot(linktocaller.normalVector)

        linktocaller.resizeArrowWidgets(linktocaller.endVector)
        linktocaller.ExtrudeLBL.setText(
            "Length= " + str(round(linktocaller.extrudeLength, 4)))
        linktocaller.reCreateExtrudeObject()

    except Exception as err:
        App.Console.PrintError("'View Inside objects' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def callback_release(userData: fr_arrow_widget.userDataObject = None):
    """
       Callback after releasing the left mouse button. 
       This callback will finalize the Extrude operation. 
       Deleting the original object will be done when the user press 'OK' button
    """
    try:
        if (userData is None):
            print("userData is None")
            raise TypeError

        ArrowObject = userData.ArrowObj
        events = userData.events
        linktocaller = userData.callerObject
        # Avoid activating this part several times,
        if (linktocaller.startVector is None):
            return
        print("mouse release")
        ArrowObject.remove_focus()
        linktocaller.run_Once = False
        linktocaller.endVector = App.Vector(ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_x,
                                            ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_y,
                                            ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_z)
        # Undo
        App.ActiveDocument.openTransaction(translate("Design456", "SmartExtrude"))
        linktocaller.startVector = None
        App.ActiveDocument.commitTransaction()  # undo reg.
        newObjcut=[]
        #Do final operation. Either leave it as it is, merge or subtract
        print("linktocaller.OperationOption",linktocaller.OperationOption)
        if linktocaller.OperationOption == 2:
            #2 - Subtraction : Subtract other objects with the extruded part.
            
            #First merge the old object with the extruded face
            old = App.ActiveDocument.addObject("Part::MultiFuse", "MergedTemp")
            old.Shapes=[linktocaller.selectedObj.Object,linktocaller.newObject]
            #Subtraction is complex. I have to cut from each object the same extruded part.
            if (linktocaller.objChangedTransparency  !=[]):
                for i in range(0,len(linktocaller.objChangedTransparency)):
                    newObjcut.append(App.ActiveDocument.addObject("Part::Cut", "CUT"+str(i)) ) 
                    newObjcut[i].Base = App.ActiveDocument.getObject(linktocaller.objChangedTransparency[i].Name)  # Target
                    newObjcut[i].Tool = old               # Subtracted shape/object
                    newObjcut[i].Refine = True
                    TE= Gui.ActiveDocument.getObject(newObjcut[i].Name)
                    TE.Transparency =0
                    App.ActiveDocument.recompute()
                    
        elif linktocaller.OperationOption == 1:
            #1 - Merge : Merge other objects with the extruded part and with the old object
            newObj = App.ActiveDocument.addObject("Part::MultiFuse", "MergedTemp")
            #TODO FIX ME .. IT SHOULD BE SHAPE NOT OBJ. 
            linktocaller.objChangedTransparency.append(linktocaller.selectedObj.Object.Shape)
            linktocaller.objChangedTransparency.append(linktocaller.newObject.Shape)
            newObj.Shapes = linktocaller.objChangedTransparency
            newObj.Refine = True
        elif linktocaller.OperationOption ==0:
            #is here just to make the code more readable. 
            pass # nothing to do . 


        App.ActiveDocument.recompute()
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        faced.EnableAllToolbar(True)
        App.Console.PrintError("'Design456_Extrude' Release Filed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


class Design456_SmartExtrude:
    """
        Apply Extrude to any 3D object by selecting the object, a Face or one or multiple edges 
        Radius of the Extrude is counted by dragging the arrow towards the negative Z axis.
    """
    _vector = App.Vector(0.0, 0.0, 0.0)
    mw = None
    dialog = None
    tab = None
    smartInd = None
    _mywin = None
    b1 = None
    ExtrudeLBL = None
    run_Once = False
    endVector = None
    startVector = None
    extrudeLength = 0.001  # This will be the Delta-mouse position
    # We will make two object, one for visual effect and the other is the original
    selectedObj = None
    direction = None
    # We use this to simplify the code - for both, 2D and 3D object, the face variable is this
    targetFace = None
    newObject = None
    DirExtrusion = App.Vector(0, 0, 0)  # No direction if all are zero
    was2DObject = False
    OperationOption = 0  # default is zero
    objChangedTransparency = []

    def reCreateExtrudeObject(self):
        """
        [
         Recreate the object after changing the length of the extrusion
         This will also change the Transparency of object if subtraction is 
         chosen.
        ]
        """
        try:
            result=None
            self.newObject.LengthFwd = self.extrudeLength
            if self.OperationOption ==2 or self.OperationOption ==1 :  # Must be subtract to activate this
                if (len(self.objChangedTransparency) != 0):
                    for obj in self.objChangedTransparency:
                        if (hasattr(obj,"Name")):
                            o = Gui.ActiveDocument.getObject(obj.Name)
                            o.Transparency = 0
                        elif (hasattr(obj,"Obj.Name")):
                            o = Gui.ActiveDocument.getObject(obj.Object.Name)                      
                            o.Transparency = 0

                result = faced.checkCollision(self.newObject)
                if len(result) != 0:
                    for obj in result:
                        if (hasattr(obj,"Name")):
                            o = Gui.ActiveDocument.getObject(obj.Name)
                        elif (hasattr(obj,"Obj.Name")):
                            o = Gui.ActiveDocument.getObject(obj.Object.Name)                        
                        o.Transparency = 80
            self.objChangedTransparency=result
            App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'reCreateExtrudeObject' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def resizeArrowWidgets(self, endVec):
        """[Resize the arrow widget. The widget will be moved to the new position]
        Args:
            endVec ([App.Vector]): [New position]

        """
        currentLength = self.extrudeLength
        # to let the arrow be outside the object
        self.extrudeLength = self.extrudeLength+15
        self.smartInd.w_vector = self.calculateNewVector()
        self.extrudeLength = currentLength  # return back the value.
        self.smartInd.redraw()

    def getArrowPosition(self):
        """"
         Find out the vector and rotation of the arrow to be drawn.
        """
        #      For now the arrow will be at the top
        rotation = [0.0, 0.0, 0.0, 0.0]

        face1 = None
        if(self.isFaceOf3DObj()):
            # The whole object is selected
            sub1 = self.selectedObj
            face1 = sub1.SubObjects[0]
        else:
            face1 = self.selectedObj.Object.Shape.Faces[0]
        self.extrudeLength = 5
        self._vector = self.calculateNewVector()
        self.extrudeLength = 0.0

        #FIXME - WRONG
        print(face1)
        print(face1.Surface)
        print(face1.Surface.Rotation)
        print(face1.Surface.Rotation.Axis)
        print(face1.Surface.Rotation.Angle)

        rotation = (face1.Surface.Rotation.Axis.x,
                    face1.Surface.Rotation.Axis.y,
                    face1.Surface.Rotation.Axis.z,
                    math.degrees(face1.Surface.Rotation.Angle))

        print("rotation", rotation)
        return rotation

    def isFaceOf3DObj(self):
        """[Check if the selected object is a face or is a 2D object. 
        A face cannot be extruded directly. We have to extract a Face and them Extrude]
            Face of 3D Object = True 
            2D Object= False
        Returns:
            [Boolean]: [Return True if the selected object is a face from 3D object, otherwise False]
        """
        if len(self.selectedObj.Object.Shape.Faces) > 1:
            return True
        else:
            return False

    def extractFace(self):
        """[Extract a face from a 3D object as it cannot be extruded otherwise]

        Returns:
            [Face]: [Face created from the selected face of the 3D object]
        """
        newobj = "eFace"
        sh = self.selectedObj.Object.Shape.copy()
        if hasattr(self.selectedObj.Object, "getGlobalPlacement"):
            gpl = self.selectedObj.Object.getGlobalPlacement()
            sh.Placement = gpl
        else:
            pass  # TODO: WHAT SHOULD WE DO HERE ?

        name = self.selectedObj.SubElementNames[0]
        newobj = App.ActiveDocument.addObject("Part::Feature", newobj)
        newobj.Shape = sh.getElement(name)
        App.ActiveDocument.recompute()
        return newobj

    def calculateNewVector(self):
        """[Calculate the new position that will be used for the arrow drawing]

        Returns:
            [App.Vector]: [Position where the arrow will be moved to]
        """
        if(self.isFaceOf3DObj()):
            ss = self.selectedObj.SubObjects[0]
        else:
            ss = self.selectedObj.Object.Shape
        yL = ss.CenterOfMass
        uv = ss.Surface.parameter(yL)
        nv = ss.normalAt(uv[0], uv[1])
        self.normalVector = nv

        if (self.extrudeLength ==0):
            d = self.extrudeLength = 1
        else:
            d = self.extrudeLength
        point = yL + d * nv
        return (point)

    def Activated(self):
        """[
            Main activation function executes when the tool is used

            ]
        """
        try:
            print("Smart Extrusion Activated")
            sel = Gui.Selection.getSelectionEx()
            if len(sel) == 0:
                # An object must be selected
                errMessage = "Select an object, one face to Extrude"
                faced.errorDialog(errMessage)
                return
            self.selectedObj = sel[0]
            faced.EnableAllToolbar(False)

            App.ActiveDocument.openTransaction(
                translate("Design456", "SmartExtrude"))
            if self.isFaceOf3DObj():  # We must know if the selection is a 2D face or a face from a 3D object
                # We have a 3D Object. Extract a face and start to Extrude
                self.targetFace = self.extractFace()
                self.was2DObject = False
            else:
                # We have a 2D Face - Extract it directly
                self.targetFace = self.selectedObj.Object
                self.was2DObject = True

            rotation = self.getArrowPosition()
            self.smartInd = Fr_Arrow_Widget(
                self._vector, "Extrude", 1, FR_COLOR.FR_RED, rotation, 3)
            self.smartInd.w_callback_ = callback_release
            self.smartInd.w_move_callback_ = callback_move
            self.smartInd.w_userData.callerObject = self
            if self._mywin is None:
                self._mywin = win.Fr_CoinWindow()

            self._mywin.addWidget(self.smartInd)
            mw = self.getMainWindow()
            self._mywin.show()

            self.newObject = App.ActiveDocument.addObject(
                'Part::Extrusion', 'Extrude')
            self.newObject.Base = self.targetFace
            self.newObject.DirMode = "Normal"  # Don't use Custom as it leads to PROBLEM!
            # Above statement != always correct. Some faces require 'custom'
            self.newObject.DirLink = None
            self.newObject.LengthFwd = self.extrudeLength  # Must be negative
            self.newObject.LengthRev = 0.0
            self.newObject.Solid = True
            self.newObject.Reversed = False
            self.newObject.Symmetric = False
            self.newObject.TaperAngle = 0.0
            self.newObject.TaperAngleRev = 0.0

            App.ActiveDocument.recompute()
        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Design456_Extrude' getMainWindwo-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def __del__(self):
        """ 
            class destructor
            Remove all objects from memory even fr_coinwindow
        """
        faced.EnableAllToolbar(True)
        try:
            self.smartInd.hide()
            self.smartInd.__del__()  # call destructor
            if self._mywin != None:
                self._mywin.hide()
                del self._mywin
                self._mywin = None
            App.ActiveDocument.commitTransaction()  # undo reg.
            self.extrudeLength = 0

        except Exception as err:
            App.Console.PrintError("'Design456_Extrude' getMainWindwo-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def getMainWindow(self):
        """[Create the tab for the tool]

        Raises:
            Exception: [If no tabs were found]
            Exception: [If something unusual happen]

        Returns:
            [dialog]: [the new dialog which will be added as a tab to the tab section of FreeCAD]
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
            self.tab.addTab(self.dialog, "Smart Extrude")
            self.tab.setCurrentWidget(self.dialog)
            self.dialog.resize(200, 450)
            self.dialog.setWindowTitle("Smart Extrude")
            self.la = QtGui.QVBoxLayout(self.dialog)
            self.e1 = QtGui.QLabel("(Smart Extrude)\nFor quicker\nApplying Extrude")
            self.groupBox = QtGui.QGroupBox(self.dialog)
            self.groupBox.setGeometry(QtCore.QRect(60, 130, 120, 80))
            self.groupBox.setObjectName("Extrusion Type")

            self.radAsIs = QtGui.QRadioButton(self.groupBox)
            self.radAsIs.setObjectName("radAsIs")
            self.radAsIs.setText("As Is")            

            self.radMerge = QtGui.QRadioButton(self.groupBox)
            self.radMerge.setObjectName("radMerge")
            self.radMerge.setText("Merge")            

            self.radSubtract = QtGui.QRadioButton(self.groupBox)
            self.radSubtract.setObjectName("radSubtract")
            self.radSubtract.setText("Subtract")            
            
            commentFont = QtGui.QFont("Times", 12, True)
            self.ExtrudeLBL = QtGui.QLabel("Extrude Radius=")
            self.e1.setFont(commentFont)
            self.la.addWidget(self.e1)
            self.la.addWidget(self.ExtrudeLBL)

            okbox = QtGui.QDialogButtonBox(self.dialog)
            okbox.setOrientation(QtCore.Qt.Horizontal)
            okbox.setStandardButtons(QtGui.QDialogButtonBox.Ok)

            self.la.addWidget(okbox)

            # Adding checkbox for Merge, Subtract Or just leave it "As is"
            self.la.addWidget(self.radAsIs)
            self.la.addWidget(self.radMerge)
            self.la.addWidget(self.radSubtract)
            self.radAsIs.setChecked(True)
            self.radAsIs.toggled.connect(lambda:self.btnState(self.radAsIs))
            self.radMerge.toggled.connect(lambda:self.btnState(self.radMerge))
            self.radSubtract.toggled.connect(lambda:self.btnState(self.radSubtract))
            
            QtCore.QObject.connect(
                okbox, QtCore.SIGNAL("accepted()"), self.hide)
            QtCore.QMetaObject.connectSlotsByName(self.dialog)

            return self.dialog

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Design456_Extrude' getMainWindwo-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def btnState(self, button):
        print("btnstate activated=",button.text())
        if button.text()=="As Is":
             if button.isChecked() == True:
                self.OperationOption = 0  # 0 as Is default, 1 Merged, 2 Subtracted
        elif button.text()=="Merge":
             if button.isChecked() == True:
                self.OperationOption = 1
        elif button.text()=="Subtract":
             if button.isChecked() == True:
                self.OperationOption = 2

    def hide(self):
        """
        Hide the widgets. Remove also the tab.
        For this tool, I decide to choose the hide to merge, subtract or leave it as is here. 
        I can do that during the extrusion (moving the arrow), but that will be an action
        without undo. Here the user will be finished with the extrusion and want to leave the tool
        TODO: If there will be a discussion about this, we might change this behavior!!

        """

        if (self.OperationOption == 0):
            pass  # Here just to make the code clear that we do nothing otherwise it != necessary
        elif(self.OperationOption == 1):
            # Merge the new object with the old object
            # There are several cases here
            # 1- Old object was only 2D object --
            #    nothing will be done but we must see if the new object != intersecting other objects
            # 2- Old object is intersecting with new object..
            # In case 1 and 2 when there is intersecting we should merge both
            if (self.was2DObject == True):
                # No 3D but collision might happen.
                pass
        self.dialog.hide()
        del self.dialog
        dw = self.mw.findChildren(QtGui.QDockWidget)
        newsize = self.tab.count()  # Todo : Should we do that?
        self.tab.removeTab(newsize-1)  # it ==0,1,2,3 ..etc
        # TODO remove the face or extracted face if there is a merge and make a simple copy
        # App.ActiveDocument.removeObject(self.selectedObj.Name)
        App.ActiveDocument.recompute()
        self.__del__()  # Remove all smart Extrude 3dCOIN widgets

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_SmartExtrude.svg',
            'MenuText': ' Smart Extrude',
                        'ToolTip':  ' Smart Extrude'
        }


Gui.addCommand('Design456_SmartExtrude', Design456_SmartExtrude())
