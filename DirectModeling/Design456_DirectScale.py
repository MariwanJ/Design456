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
import Draft
import Part
from ThreeDWidgets import fr_arrow_widget
from pivy import coin
import FACE_D as faced
from PySide.QtCore import QT_TRANSLATE_NOOP

from typing import List
import Design456Init
from PySide import QtGui, QtCore
from ThreeDWidgets.fr_arrow_widget import Fr_Arrow_Widget
from ThreeDWidgets.constant import FR_COLOR
from draftutils.translate import translate  # for translation

# This will be used to convert mouse movement to scale factor.
SCALE_FACTOR = 15.0


def calculateScale(ArrowObject, linktocaller, sizeChanged):
    """
        Calculate the scale from the mouse movement. 
    """

    try:
        deltaX = sizeChanged.x
        deltaY = sizeChanged.y
        deltaZ = sizeChanged.z
        (lengthX, lengthY, lengthZ) = linktocaller.getObjectLength()
        uniformValue = 1.0
        oldLength = 0.0

        if (linktocaller.b1.text() == 'Uniform'):

            # We resize them all regardless the change in which axis made
            if ArrowObject.w_color == FR_COLOR.FR_OLIVEDRAB:
                uniformValue = deltaY/SCALE_FACTOR
                uniformValue = (lengthY+uniformValue)/lengthY
            elif ArrowObject.w_color == FR_COLOR.FR_RED:
                uniformValue = deltaX/SCALE_FACTOR
                uniformValue = (lengthX+uniformValue)/lengthX
            elif ArrowObject.w_color == FR_COLOR.FR_BLUE:
                uniformValue = deltaZ/SCALE_FACTOR
                uniformValue = (lengthZ+uniformValue)/lengthZ

            else:
                # This shouldn't happen
                errMessage = "Unknown error occurred, wrong Arrow-Color"
                faced.errorDialog(errMessage)
                return
            scaleX = scaleY = scaleZ = uniformValue
            linktocaller.scaleLBL.setText("scale= "+str(round(scaleX, 4)))
        else:
            scaleX = 1
            scaleY = 1
            scaleZ = 1
            if ArrowObject.w_color == FR_COLOR.FR_OLIVEDRAB:
                # y-direction moved
                scaleY = deltaY/SCALE_FACTOR
                scaleY = (lengthY+scaleY)/lengthY
                linktocaller.scaleLBL.setText("scale= "+str(round(scaleY, 4)))
            elif ArrowObject.w_color == FR_COLOR.FR_RED:
                # x-direction moved
                scaleX = deltaX/SCALE_FACTOR
                scaleX = (lengthX+scaleX)/lengthX
                linktocaller.scaleLBL.setText("scale= "+str(round(scaleX, 4)))
            elif ArrowObject.w_color == FR_COLOR.FR_BLUE:
                # z-direction moved
                scaleZ = deltaZ/SCALE_FACTOR
                scaleZ = (lengthZ+deltaZ)/lengthZ
                linktocaller.scaleLBL.setText("scale= "+str(round(scaleZ, 4)))
        return(scaleX, scaleY, scaleZ)

    except Exception as err:
        App.Console.PrintError("'Resize' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def ResizeObject(ArrowObject, linktocaller, sizeChanged):
    """
        This function will resize the 3D object. It clones the old object
        and make a new simple copy of the 3D object. 
    """
    # if the whichone = 0 ---> The real object will be resized, fake will be deleted.
    #        whichone = 1 ---> the fake object will be resized.
    try:
        (scaleX, scaleY, scaleZ) = calculateScale(
            ArrowObject, linktocaller, sizeChanged)
        # Apply the scale
        # Avoid having the scale too small
        if scaleX < 0.005:
            scaleX = 0.005
            print("too small scaleX")
        elif scaleX > 20:
            scaleX = 1
            print("too high scaleX")

        if scaleY < 0.005:
            scaleY = 0.005
            print("too small scaleY")
        elif scaleY > 20:
            scaleY = 1
            print("too high scaleY")

        if scaleZ < 0.005:
            scaleZ = 0.005
            print("too small scaleZ")
        elif scaleZ > 20:
            scaleZ = 1
            print("too high scaleZ")

        linktocaller.selectedObj[1].Scale = (scaleX, scaleY, scaleZ)
        App.ActiveDocument.recompute()
        linktocaller.reCreateBothOriginalAndCloneObject()

    except Exception as err:
        App.Console.PrintError("'Resize' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def callback_release(userData: fr_arrow_widget.userDataObject = None):
    """
       Callback after releasing the left mouse button. 
       This will do the actual job in resizing the 3D object.
    """
    try:
        ArrowObject = userData.ArrowObj
        events = userData.events
        linktocaller = userData.callerObject

        # Avoid activating this part several times,
        if (linktocaller.startVector is None):
            return

        ArrowObject.remove_focus()
        linktocaller.run_Once = False
        # Undo
        App.ActiveDocument.openTransaction(
            translate("Design456", "DirectScale"))

        linktocaller.startVector = None
        # userData = None   #This cannot be correct
        linktocaller.mouseToArrowDiff = 0.0
        linktocaller.scaleLBL.setText("scale= ")

        linktocaller.reCreateBothOriginalAndCloneObject()
        # original
        App.ActiveDocument.recompute()

        App.ActiveDocument.commitTransaction()  # undo reg.
        # Redraw the arrows

        linktocaller.resizeArrowWidgets()

        return 1  # we eat the event no more widgets should get it

    except Exception as err:
        App.Console.PrintError("'callback release' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def callback_move(userData: fr_arrow_widget.userDataObject = None):
    """
        Mouse DRAG callback. It will update the location of the arrows, 
        and keep track of mouse-position. 
        This will continue until a mouse release occurs
    """

    try:
        if userData is None:
            return  # Nothing to do here - shouldn't be None

        ArrowObject = userData.ArrowObj
        events = userData.events
        linktocaller = userData.callerObject
        if type(events) != int:
            return

        clickwdgdNode = ArrowObject.w_parent.objectMouseClick_Coin3d(ArrowObject.w_parent.w_lastEventXYZ.pos,
                                                          ArrowObject.w_pick_radius, ArrowObject.w_widgetSoNodes)
        clickwdglblNode = ArrowObject.w_parent.objectMouseClick_Coin3d(ArrowObject.w_parent.w_lastEventXYZ.pos,
                                                            ArrowObject.w_pick_radius, ArrowObject.w_widgetlblSoNodes)
        linktocaller.endVector = App.Vector(ArrowObject.w_parent.w_lastEventXYZ.Coin_x,
                                            ArrowObject.w_parent.w_lastEventXYZ.Coin_y,
                                            ArrowObject.w_parent.w_lastEventXYZ.Coin_z)

        if clickwdgdNode is None and clickwdglblNode is None:
            if linktocaller.run_Once is False:
                return 0  # nothing to do

        if linktocaller.run_Once is False:
            linktocaller.run_Once = True
            linktocaller.mouseToArrowDiff = linktocaller.endVector.sub(
                userData.ArrowObj.w_vector[0])
            # Keep the old value only first time when drag start
            linktocaller.startVector = linktocaller.endVector
            if not ArrowObject.has_focus():
                ArrowObject.take_focus()

        scale = 1.0

        MovementsSize = linktocaller.endVector.sub(
            linktocaller.mouseToArrowDiff)
        (scaleX, scaleY, scaleZ) = calculateScale(
            ArrowObject, linktocaller, MovementsSize)

        if ArrowObject.w_color == FR_COLOR.FR_OLIVEDRAB:
            scale = scaleY
#            ArrowObject.w_vector[0].y = MovementsSize.y #+linktocaller.mmAwayFrom3DObject

        elif ArrowObject.w_color == FR_COLOR.FR_RED:
            #            ArrowObject.w_vector[0].x = MovementsSize.x #+linktocaller.mmAwayFrom3DObject
            scale = scaleX

        elif ArrowObject.w_color == FR_COLOR.FR_BLUE:
            #            ArrowObject.w_vector[0].z = MovementsSize.z #+linktocaller.mmAwayFrom3DObject
            scale = scaleZ

        linktocaller.scaleLBL.setText("scale= "+str(scale))

        linktocaller.smartInd[1].changeLabelstr(
            "  Scale= " + str(round(scaleX, 4)))
        linktocaller.smartInd[0].changeLabelstr(
            "  Scale= " + str(round(scaleY, 4)))
        linktocaller.smartInd[2].changeLabelstr(
            "  Scale= " + str(round(scaleZ, 4)))
        linktocaller.resizeArrowWidgets()
        linktocaller.smartInd[0].redraw()
        linktocaller.smartInd[1].redraw()
        linktocaller.smartInd[2].redraw()

        ResizeObject(ArrowObject, linktocaller, MovementsSize)

    except Exception as err:
        App.Console.PrintError("'callback' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


class Design456_DirectScale:
    """
    Direct scaling of any 3D Object by dragging either uniform arrow or
    un-uniform arrows.
    """
    def __init__(self):
        self.mw = None
        self.dialog = None
        self.tab = None
        self.smartInd = []
        self._mywin = None
        self.b1 = None
        self.scaleLBL = None
        self.run_Once = False
        self.endVector = None
        self.startVector = None
        # We will make two object, one for visual effect and the other is the original
        self.selectedObj = []
        # 0 is the original    1 is the fake one (just for interactive effect)
        self.mouseToArrowDiff = None
        self.mmAwayFrom3DObject = 5  # Use this to take away the arrow from the object
    
    def getObjectLength(self, whichOne=1):
        """ 
            get Max length of the 3D object by taking the 
            boundary box length
        """
        return(self.selectedObj[whichOne].Shape.BoundBox.XLength,
               self.selectedObj[whichOne].Shape.BoundBox.YLength,
               self.selectedObj[whichOne].Shape.BoundBox.ZLength)

    def returnVectorsFromBoundaryBox(self, whichone=0):
        """
        Calculate vertices which will be used to draw the arrows. 
        """
        # Max object length in all directions
        (lengthX, lengthY, lengthZ) = self.getObjectLength(1)
        # Make the start 2 mm before the object is placed
        startX = self.selectedObj[whichone].Shape.BoundBox.XMin
        startY = self.selectedObj[whichone].Shape.BoundBox.YMin
        startZ = self.selectedObj[whichone].Shape.BoundBox.ZMin
        EndX = self.selectedObj[whichone].Shape.BoundBox.XMax
        EndY = self.selectedObj[whichone].Shape.BoundBox.YMax
        EndZ = self.selectedObj[whichone].Shape.BoundBox.ZMax
        p1: App.Vector = None
        p2: App.Vector = None
        _vectors: List[App.Vector] = []
        leng = []
        leng.append(lengthX)
        leng.append(lengthY)
        leng.append(lengthZ)
        # Must be two vectors, second is dummy value
        p1 = [App.Vector(startX+lengthX/2, EndY + self.mmAwayFrom3DObject,
                         startZ+lengthZ/2), App.Vector(0, 0, 0)]
        p2 = [App.Vector(EndX+self.mmAwayFrom3DObject, startY +
                         lengthY/2, startZ+lengthZ/2), App.Vector(0, 0, 0)]
        p3 = [App.Vector(startX+lengthX/2, startY+lengthY / 2,
                         EndZ+self.mmAwayFrom3DObject), App.Vector(0, 0, 0)]
        _vectors.append(p1)
        _vectors.append(p2)
        _vectors.append(p3)
        return (_vectors, leng)
        # we have a self.selectedObj object. Try to show the dimensions.

    def createArrows(self):
        """ 
        It creates the arrows and add them to the coin window.
        Called by Activated function of DirectScale
        """
        (_vec, length) = self.returnVectorsFromBoundaryBox(0)

        self.smartInd.clear()

        rotation = [-1.0, 0.0, 0.0, 90]
        self.smartInd.append(Fr_Arrow_Widget(
            _vec[0], "Y-Axis", 1, FR_COLOR.FR_OLIVEDRAB, rotation))
        # External function
        self.smartInd[0].w_callback_ = callback_release
        self.smartInd[0].w_move_callback_ = callback_move
        self.smartInd[0].w_userData.callerObject = self

        rotation = [0.0, 1.0, 0.0, 90.0]
        self.smartInd.append(Fr_Arrow_Widget(
            _vec[1], "X-Axis", 1, FR_COLOR.FR_RED, rotation))
        self.smartInd[1].w_callback_ = callback_release
        self.smartInd[1].w_move_callback_ = callback_move
        self.smartInd[1].w_userData.callerObject = self

        rotation = [1.0, 0.0, 1.0, 0.0]
        self.smartInd.append(Fr_Arrow_Widget(
            _vec[2], "Z-Axis", 1, FR_COLOR.FR_BLUE, rotation))
        self.smartInd[2].w_callback_ = callback_release
        self.smartInd[2].w_move_callback_ = callback_move
        self.smartInd[2].w_userData.callerObject = self

    def Activated(self):
        import ThreeDWidgets.fr_coinwindow as win
        try:
            sel = Gui.Selection.getSelection()
            if len(sel) != 1:
                # Only one object must be self.selectedObj
                errMessage = "Select one object to scale"
                faced.errorDialog(errMessage)
                return

            self.selectedObj.clear()
            self.selectedObj.append(sel[0])  # original
            if not hasattr(self.selectedObj[0], 'Shape'):
                # Only one object must be self.selectedObj
                errMessage = "self.selectedObj object has no Shape,\n please make a simple copy of the object"
                faced.errorDialog(errMessage)
                return

            cloneObj = Draft.clone(self.selectedObj[0], forcedraft=True)

            # Scale the object to 1
            cloneObj.Scale = App.Vector(1, 1, 1)
            self.selectedObj[0].Visibility = False
            self.selectedObj.append(cloneObj)

            App.ActiveDocument.recompute()

            (self.mw, self.dialog, self.tab) = faced.createActionTab(
                "Direct Scale").Activated()
            la = QtGui.QVBoxLayout(self.dialog)
            e1 = QtGui.QLabel(
                "(Direct Scale)\nFor quicker\nresizing any\n3D Objects")
            self.scaleLBL = QtGui.QLabel("Scale=")
            commentFont = QtGui.QFont("Times", 12, True)
            self.b1 = QtGui.QPushButton("Uniform")
            BUTTON_SIZE = QtCore.QSize(100, 100)
            self.b1.setMinimumSize(BUTTON_SIZE)
            self.b1.setStyleSheet("background: orange;")
            self.b1.setCheckable(True)
            self.b1.toggle()
            self.b1.clicked.connect(lambda: self.whichbtn(self.b1))
            self.b1.clicked.connect(self.btnState)
            la.addWidget(self.b1)
            e1.setFont(commentFont)
            self.scaleLBL.setFont(commentFont)
            la.addWidget(e1)
            la.addWidget(self.scaleLBL)
            self.okbox = QtGui.QDialogButtonBox(self.dialog)
            self.okbox.setOrientation(QtCore.Qt.Horizontal)
            self.okbox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
            la.addWidget(self.okbox)
            QtCore.QObject.connect(
                self.okbox, QtCore.SIGNAL("accepted()"), self.hide)

            QtCore.QMetaObject.connectSlotsByName(self.dialog)
            self.createArrows()

            # set self.selectedObj object to each smartArrow
            if self._mywin is None:
                self._mywin = win.Fr_CoinWindow()
            self._mywin.addWidget(self.smartInd)
            self._mywin.show()

        # we have a self.selectedObj object. Try to show the dimensions.
        except Exception as err:
            App.Console.PrintError("'Design456_DirectScale' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def reCreateBothOriginalAndCloneObject(self):

        # Create a simple copy
        nameOriginal = self.selectedObj[0].Name

        App.ActiveDocument.removeObject(self.selectedObj[0].Name)

        __shape = Part.getShape(
            self.selectedObj[1], '', needSubElement=False, refine=False)
        newObj = App.ActiveDocument.addObject(
            'Part::Feature', nameOriginal)  # Our scaled shape
        newObj.Shape = __shape
        App.ActiveDocument.removeObject(self.selectedObj[1].Name)
        # Make scaled object to be the original for us now
        self.selectedObj[0] = newObj
        # Make a scaled from the new original shape
        cloneObj = Draft.clone(self.selectedObj[0], forcedraft=True)
        # Scale the object to 1
        cloneObj.Scale = App.Vector(1, 1, 1)

        # Hide again the new Original self.selectedObj[0].Visibility = False
        self.selectedObj[1] = cloneObj
        App.ActiveDocument.recompute()

    def hide(self):
        """
        Hide the widgets. Remove also the tab.
        """
        self.dialog.hide()
        del self.dialog
        dw = self.mw.findChildren(QtGui.QDockWidget)
        newsize = self.tab.count()  # Todo : Should we do that?
        self.tab.removeTab(newsize-1)  # it ==0,1,2,3 ..etc
        self.__del__()  # Remove all smart scale 3dCOIN widgets

    def btnState(self):
        """ 
        Change button text to represent the direct scale mode (Uniform or None uniform)

        """
        if self.b1.isChecked():
            self.b1.setText("Uniform")

        else:
            self.b1.setText("None Uniform")

    def whichbtn(self, b1):
        if b1.text() == 'Uniform':
            b1.setStyleSheet("background: blue;")
        else:
            b1.setStyleSheet("background: orange;")

    def resizeArrowWidgets(self):
        """
        Reposition the arrows by recalculating the boundary box
        and updating the vectors inside each fr_arrow_widget
        """
        (_vec, length) = self.returnVectorsFromBoundaryBox(1)
        for i in range(0, 3):
            self.smartInd[i].w_vector = _vec[i]

        for wdg in self.smartInd:
            wdg.redraw()
        return

    def __del__(self):
        """
        Remove all widget from Fr_CoinWindow and from the scenegraph
        """
        try:
            if type(self.smartInd) == list:
                for i in self.smartInd:
                    i.hide()
                    i.__del__()
                    del i  # call destructor
            else:
                self.smartInd.hide()
                self.smartInd.__del__()
                del self.smartInd

            if self._mywin is not None:
                self._mywin.hide()
                del self._mywin
                self._mywin = None
            # remove the temp object, and show the original
            # App.ActiveDocument.removeObject(self.selectedObj[1].Name)
            self.selectedObj[1].Visibility = False
            App.ActiveDocument.removeObject(self.selectedObj[1].Name)
            self.selectedObj[0].Visibility = True
            self.selectedObj.clear()

        except Exception as err:
            App.Console.PrintError("'Design456_SmartScale' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'DirectScale.svg',
            'MenuText': 'Direct Scale',
                        'ToolTip':  'Direct Scale'
        }


Gui.addCommand('Design456_DirectScale', Design456_DirectScale())
