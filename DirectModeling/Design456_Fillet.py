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

MouseScaleFactor = 1.0


def callback_move(userData: fr_arrow_widget.userDataObject = None):
    try:
        #TODO: FIXME
        '''
            We have to recreate the object each time we change the radius. 
            This means that the redrawing must be optimized : TODO: FIXME

        '''
        if userData == None:
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

        if clickwdgdNode == None and clickwdglblNode == None:
            if linktocaller.run_Once == False:
                print("click move")
                return 0  # nothing to do
            
        if linktocaller.run_Once == False:
            linktocaller.run_Once = True
            mouseToArrowDiff = ArrowObject.w_vector.z-linktocaller.endVector.z
            linktocaller.offset=mouseToArrowDiff

         # Keep the old value only first time when drag start
            linktocaller.startVector = linktocaller.endVector

            if not ArrowObject.has_focus():
                ArrowObject.take_focus()
                
        linktocaller.FilletRadius = abs((linktocaller.endVector.y+linktocaller.mouseToArrowDiff)/MouseScaleFactor)            
        linktocaller.resizeArrowWidgets(linktocaller.endVector)
        linktocaller.FilletLBL.setText("scale= "+str(linktocaller.FilletRadius))

        linktocaller.reCreatefilletObject()

    except Exception as err:
        App.Console.PrintError("'View Inside objects' Failed. "
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
        #TODO: FIXME
        ArrowObject = userData.ArrowObj
        events = userData.events
        linktocaller = userData.callerObject

        # Avoid activating this part several times,
        if (linktocaller.startVector == None):
            return

        print("mouse release")
        ArrowObject.remove_focus()
        linktocaller.run_Once = False
        linktocaller.endVector = App.Vector(ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_x,
                                            ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_y,
                                            ArrowObject.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_z)
        # Undo
        App.ActiveDocument.openTransaction(translate("Design456", "Fillet"))

        linktocaller.startVector = None
        userData = None
        linktocaller.mouseToArrowDiff = 0.0
        #linktocaller.FilletLBL.setText("Radius= ")
        App.ActiveDocument.commitTransaction()  # undo reg.
        linktocaller.reCreatefilletObject()
        # Make a simple copy

        #__shape = Part.getShape(linktocaller.selectedObj[1], '', needSubElement=False, refine=False)
        #newObj = App.ActiveDocument.addObject('Part::Feature', "Result")  # Our scaled shape
        #newObj.Shape = __shape
        App.ActiveDocument.recompute()
        #App.ActiveDocument.removeObject(linktocaller.selectedObj[1].ObjectName)
        App.ActiveDocument.removeObject(linktocaller.selectedObj[0].ObjectName)
        #linktocaller.selectedObj.clear()
        linktocaller.selectedObj[0]=linktocaller.selectedObj[1]
        #linktocaller.selectedObj.append(newObj)
        linktocaller.selectedObj[0].ObjectName = linktocaller.Originalname
        linktocaller.selectedObj[0].Label=linktocaller.Originalname
        linktocaller.selectedObj.remove(1)
        App.ActiveDocument.recompute()

        # Redraw the arrows
        #linktocaller.resizeArrowWidgets()
        return 1  # we eat the event no more widgets should get it

    except Exception as err:
        App.Console.PrintError("'View Inside objects' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

class Design456_SmartFillet:
    """
        Apply fillet to an edge using mouse movement.
        Moving an arrow that will represent radius of the fillet.
    """
    _vector = App.Vector(0.0, 0.0, 0.0)
    mw = None
    dialog = None
    tab = None
    smartInd = None
    _mywin = None
    b1 = None
    FilletLBL = None
    run_Once = False
    endVector = None
    startVector = None
    # We will make two object, one for visual effect and the other is the original
    selectedObj = []
    # 0 is the original    1 is the fake one (just for interactive effect)
    mouseToArrowDiff = 0.0
    offset=0.0
    mmAwayFrom3DObject = 10  # Use this to take away the arrow from the object
    FilletRadius = 0.05   #We cannot have zero. TODO: What value we should use? FIXME:
    objectType = None  # Either shape, Face or Edge.
    Originalname = ''

    def registerShapeType(self):
        '''
            Find out shape-type and save the name in objectType
        '''
        if len(self.selectedObj[0].SubElementNames)==0:
            self.objectType = 'Shape'
        elif 'Face' in self.selectedObj[0].SubElementNames[0]:
            self.objectType = 'Face'
        elif 'Edge' in self.selectedObj[0].SubElementNames[0]:
            self.objectType = 'Edge'
        else:
            print("Error")
    
    def resizeArrowWidgets(self,endVec):
        """
        Reposition the arrows by recalculating the boundary box
        and updating the vectors inside each fr_arrow_widget
        """
        self.smartInd.w_vector.z = endVec.z  #Only Z should affect the arrow
        self.smartInd.redraw()
        return
            
    def getArrowPosition(self):
        """"
         Find out the vector and rotation of the arrow to be drawn.
        """
        # TODO: Don't know at the moment how to make this works better i.e. arrow direction and position
        #      For now the arrow will be at the top
        try:
            rotation = None
            if self.objectType == 'Shape':
              # 'Shape'
                # The whole object is selected
                print("shape")
                rotation = [-1.0, 0.0, 0.0, math.radians(57)]
                return rotation

            vectors = self.selectedObj[0].SubObjects[0].Vertexes
            if self.objectType == 'Face':
                self._vector.z = vectors[0].Z
                for i in vectors:
                    self._vector.x += i.X
                    self._vector.y += i.Y
                    if self._vector.z < i.Z:
                        self._vector.z = i.Z+10
                        self._vector.x = self._vector.x/4
                self._vector.y = self._vector.y/4

                rotation = [-1,
                            0,
                            0,
                            math.radians(57)]

            elif self.objectType == 'Edge':
                # An edge is selected
                self._vector.z = vectors[0].Z
                for i in vectors:
                    self._vector.x += i.X/2
                    self._vector.y += i.Y/2
                    self._vector.z = i.Z+10

                rotation = [-1,
                             0,
                             0,
                            math.radians(+57)]

            return rotation
        except Exception as err:
            App.Console.PrintError("'Design456_SmartFillet' getArrowPos-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

    def getEdgesNumbersList(self, names=None):
        """ we need to take out the remaining of the string
            i.e. 'Edge15' --> take out 'Edge'-->4 bytes, We need only the number
            len('Edge')] -->4
        """
        result = []
        if names == None:
            return None
        if type(names == list):
            # multiple edges
            for name in names:
                for subname in name:
                    edgeNumbor = int(subname[4:len(subname)])
                result.append(edgeNumbor, self.FilletRadius, self.FilletRadius)
        else:
            # only one Edge
            edgeNumbor = int(names[4:len(names)])
            result.append((edgeNumbor, self.FilletRadius,self.FilletRadius))
        return result

    def getAllSelectedEdges(self):
        # The format must be (Edges Number, Start-radius, End-radius)
        EdgesToBeChanged = []
        if self.objectType == 'Face':
            EdgesToBeChanged =self.selectedObj[0].SubObjects[0].Edges
        elif  self.objectType=='Edge':
            EdgesToBeChanged =self.selectedObj[0].SubObjects
        elif self.objectType == 'Shape':
            EdgesToBeChanged= self.selectedObj[0].Object.Shape.Edges
        else : 
                print ("Error couldn't find the shape type",self.objectType)
        return EdgesToBeChanged

    def reCreatefilletObject(self):

        # reCreate the fillet. We cannot avoid recreating the object from scratch
        # That is how opencascade library works.
        try:
            if len (self.selectedObj)==2:
                if hasattr(self.selectedObj[1],'ObjectName'):
                    App.ActiveDocument.removeObject(self.selectedObj[1].ObjectName)
                elif hasattr(self.selectedObj[1],'Name'):
                    App.ActiveDocument.removeObject(self.selectedObj[1].Name)
            self.selectedObj.append(self.selectedObj[0].Object.Shape.makeFillet(self.FilletRadius,self.getAllSelectedEdges()))
            Part.show(self.selectedObj[1])
            App.ActiveDocument.recompute()
            
        except Exception as err:
            App.Console.PrintError("'Design456_SmartFillet' recreatefilletObject-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]


    def Activated(self):
        self.selectedObj.clear()
        sel=Gui.Selection.getSelectionEx()
        if len(sel) == 0:
            # An object must be selected
            errMessage = "Select an object, one face or one edge to fillet"
            faced.getInfo().errorDialog(errMessage)
            return

        self.selectedObj.append(sel[0])
        self.Originalname = self.selectedObj[0].Object.Name

        # Find Out shapes type.
        self.registerShapeType()
        o=Gui.ActiveDocument.getObject(self.selectedObj[0].Object.Name)
        o.Transparency=75
        self.reCreatefilletObject()

        # get rotation
        rotation = self.getArrowPosition()

        self.smartInd = Fr_Arrow_Widget(self._vector, "Fillet", 1, FR_COLOR.FR_OLIVEDRAB, rotation)
        self.smartInd.w_callback_ = callback_release
        self.smartInd.w_move_callback_ = callback_move
        self.smartInd.w_userData.callerObject = self

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
            App.Console.PrintError("'Design456_SmartFillet' del-Failed. "
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
            self.FilletLBL = QtGui.QLabel("Fillet Radius=")
            e1.setFont(commentFont)
            la.addWidget(e1)
            la.addWidget(self.FilletLBL)
            okbox = QtGui.QDialogButtonBox(self.dialog)
            okbox.setOrientation(QtCore.Qt.Horizontal)
            okbox.setStandardButtons(
                QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
            la.addWidget(okbox)
            QtCore.QObject.connect(okbox, QtCore.SIGNAL("accepted()"), self.hide)

            QtCore.QMetaObject.connectSlotsByName(self.dialog)
            return self.dialog

        except Exception as err:
            App.Console.PrintError("'Design456_Fillet' getMainWindwo-Failed. "
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
        self.__del__()  # Remove all smart fillet 3dCOIN widgets

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'PartDesign_Fillet.svg',
            'MenuText': ' Smart Fillet',
                        'ToolTip':  ' Smart Fillet'
        }


Gui.addCommand('Design456_SmartFillet', Design456_SmartFillet())
