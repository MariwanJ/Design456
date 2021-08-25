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
            linktocaller.startVector=linktocaller.endVector

         # Keep the old value only first time when drag start
            linktocaller.startVector = linktocaller.endVector
    
        
        print("ExtrudeRadius",linktocaller.ExtrudeRadius)         
        linktocaller.resizeArrowWidgets(linktocaller.endVector)
        linktocaller.ExtrudeLBL.setText("scale= "+ str(round(linktocaller.ExtrudeRadius,4)))
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
    if (userData==None ):
        print("userData is None")
        raise TypeError 
        
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
    App.ActiveDocument.openTransaction(translate("Design456", "SmartExtrude"))
    linktocaller.startVector = None
    linktocaller.mouseToArrowDiff = 0.0
    App.ActiveDocument.commitTransaction()  # undo reg.
    linktocaller.selectedObj[0].Object.Visibility=False
    if hasattr(linktocaller.selectedObj[0],'Object'):
        linktocaller.selectedObj[0].Object.Label=linktocaller.Originalname
    App.ActiveDocument.recompute()
    App.ActiveDocument.commitTransaction()  # undo reg.

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
    # We will make two object, one for visual effect and the other is the original
    selectedObj =None
    AwayFrom3DObject = 10  # Use this to take away the arrow from the object
    objectType = None  # Either shape, Face or Edge.
    direction=None
    targetFace=None # We use this to simplify the code - for both, 2D and 3D object, the face variable is this

    def resizeArrowWidgets(self,endVec):
        """
        Reposition the arrows by recalculating the boundary box
        and updating the vectors inside each fr_arrow_widget
        """
        if(self.direction=="+x" or self.direction=="-x" ):
            self.smartInd.w_vector.x = endVec.x  #Only X should affect the arrow
        elif(self.direction=="+y" or self.direction=="-y" ):
            self.smartInd.w_vector.y = endVec.y  #Only Y should affect the arrow
        elif(self.direction=="+z" or self.direction=="-z" ):
            self.smartInd.w_vector.z = endVec.z  #Only Z should affect the arrow
        self.smartInd.redraw()
        return
    
    def getArrowPosition(self):
        """"
         Find out the vector and rotation of the arrow to be drawn.
        """
        #      For now the arrow will be at the top
        rotation = [0.0,0.0,0.0,0.0]
        self.direction= faced.getDirectionAxis() #Must be getSelectionEx
        addFactor=(0,0,0)
        maxBoundary= (self.selectedObj.SubObjects[0].Surface.Axis)
        if (self.direction =="+x"):
            rotation = [0.0, 0.0, -1.0, 90.0]
            addFactor=(maxBoundary.x,0,0)
        elif (self.direction =="-x"):
            rotation = [0.0, 0.0, 1.0,90.0]
            addFactor=(-maxBoundary.x,0,0)
        elif (self.direction =="+y"):                
            rotation = [0.0, 0.0, 1.0, 0.0]
            addFactor=(0,maxBoundary.y,0)
        elif (self.direction =="-y"):
            rotation = [0.0, 0.0, 1.0, 180.0]
            addFactor=(0,-maxBoundary.y,0)
        elif (self.direction =="+z"):
            rotation = [1.0, 0.0, 0.0, 90.0]
            addFactor=(0,0,maxBoundary.z)
        elif (self.direction =="-z"):
            rotation = [-1.0, 0.0, 0.0, 90.0]
            addFactor=(0,0,-maxBoundary.z)
        face1=None
        if(self.isFaceOf3DObj()):
            # The whole object is selected
            sub1 = self.selectedObj
            face1=sub1.SubObjects[0]
        else:
            face1=self.selectedObj.Object.Shape.Faces[0]
        self._vector = face1.CenterOfMass
        #FIXME - WRONG 
        rotation=[face1.Surface.Rotation.Axis.x,face1.Surface.Rotation.Axis.y,face1.Surface.Rotation.Axis.z,math.degrees(face1.Surface.Rotation.Angle)]
        
        print("rotation", rotation)
        rotation=[face1.normalAt(0,0),math.degrees(face1.Placement.Rotation.Angle)]
        
        self._vector.z=self.selectedObj.Object.Shape.BoundBox.ZLength/2
        #self._vector.x= self._vector.x+addFactor[0]
        #self._vector.y= self._vector.y+addFactor[1]
        #self._vector.z= self._vector.z+addFactor[2]
        
        print(rotation)
        print(self._vector)
        return rotation

    def isFaceOf3DObj(self):
        """[Check if the selected object is a face or is a 2D object. 
        A face cannot be extruded directly. We have to extract a Face and them Extrude]
            Face of 3D Object = True 
            2D Object= False
        Returns:
            [Boolean]: [Return True if the selected object is a face from 3D object, otherwise False]
        """
        if len(self.selectedObj.Object.Shape.Faces)>1:
            return True
        else :
             return False 

    def extractFace(self):
        """[Extract a face from a 3D object as it cannot be extruded otherwise]

        Returns:
            [Face]: [Face created from the selected face of the 3D object]
        """
        newobj="eFace"
        sh = self.selectedObj.Object.Shape.copy()
        if hasattr(self.selectedObj.Object, "getGlobalPlacement"):
            gpl = self.selectedObj.Object.getGlobalPlacement()
            sh.Placement = gpl
        else : 
            pass #TODO: WHAT SHOULD WE DO HERE ? 

        name =self.selectedObj.SubElementNames[0]
        newobj = App.ActiveDocument.addObject("Part::Feature", newobj)
        newobj.Shape = sh.getElement(name)
        App.ActiveDocument.recompute()
        return newobj
        

    def Activated(self):
        sel=Gui.Selection.getSelectionEx()
        if len(sel) == 0:
            # An object must be selected
            errMessage = "Select an object, one face to Extrude"
            faced.errorDialog(errMessage)
            return
        self.selectedObj=sel[0]
        if self.isFaceOf3DObj():  #We must know if the selection is a 2D face or a face from a 3D object
            #We have a 3D Object. Extract a face and start to Extrude
            self.targetFace= self.extractFace()
        else: 
            #We have a 2D Face - Extract it directly
            self.targetFace=self.selectedObj
        
        #We have the face here. Now extrusion should  start here. 
        #We will make this very smart. 
        # 1- you can resize the face extraced
        # 2- Extrusion is either with the same size or to different size (smaller or bigger)
        # 3- User can choose if the new object is merged to the older object or not. 
        # 4-
        rotation=self.getArrowPosition()
        
        self.smartInd = Fr_Arrow_Widget(self._vector, "Extrude", 2, FR_COLOR.FR_RED, rotation,1)
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
            App.ActiveDocument.commitTransaction()  # undo reg.

        except Exception as err:
            App.Console.PrintError("'Design456_SmartExtrude' del-Failed. "
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
            self.tab.addTab(self.dialog, "Smart Extrude")
            self.tab.setCurrentWidget(self.dialog)
            self.dialog.resize(200, 450)
            self.dialog.setWindowTitle("Smart Extrude")
            la = QtGui.QVBoxLayout(self.dialog)
            e1 = QtGui.QLabel("(Smart Extrude)\nFor quicker\nApplying Extrude")
            commentFont = QtGui.QFont("Times", 12, True)
            self.ExtrudeLBL = QtGui.QLabel("Extrude Radius=")
            e1.setFont(commentFont)
            la.addWidget(e1)
            la.addWidget(self.ExtrudeLBL)
            okbox = QtGui.QDialogButtonBox(self.dialog)
            okbox.setOrientation(QtCore.Qt.Horizontal)
            okbox.setStandardButtons(
                QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
            la.addWidget(okbox)
            QtCore.QObject.connect(okbox, QtCore.SIGNAL("accepted()"), self.hide)

            QtCore.QMetaObject.connectSlotsByName(self.dialog)
            return self.dialog

        except Exception as err:
            App.Console.PrintError("'Design456_Extrude' getMainWindwo-Failed. "
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
        temp=self.selectedObj
        
        App.ActiveDocument.recompute()
        self.__del__()  # Remove all smart Extrude 3dCOIN widgets

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_Extrude.svg',
            'MenuText': ' Smart Extrude',
                        'ToolTip':  ' Smart Extrude'
        }


Gui.addCommand('Design456_SmartExtrude', Design456_SmartExtrude())
