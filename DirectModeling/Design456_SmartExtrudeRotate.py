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
import ThreeDWidgets.fr_coinwindow as win
from ThreeDWidgets import fr_coin3d
from typing import List
import Design456Init
from PySide import QtGui, QtCore
from ThreeDWidgets.fr_degreewheel_widget import Fr_DegreeWheel_Widget
from ThreeDWidgets import fr_degreewheel_widget
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from draftutils.translate import translate  # for translate
import math

# The ration of delta mouse to mm  #TODO :FIXME : Which value we should choose?
MouseScaleFactor = 1
# TODO: FIXME:
"""
    
    THIS IS A START OF A NEW TOOL WHICH SHOULD BE NEW IN FREECAD
    I HAVE SEEN THAT IN OTHER CAD PROGRAM AND I WANT TO MAKE IT
    EXTRUDE A FACE BY ROTATING A FACE. THERE WILL BE OPTIONS 
    WHICH I SHOULD DECIDE. KEEP TUNED!! :)
    THIS WILL BE THE FIRST TOOL THAT USES THE DEGREE WHEEL WIDGET
    

    How it works: 
    We have to recreate the object each time we change the radius. 
    This means that the redrawing must be optimized
    
    1-If we have a 2D face, we just extrude it by rotating the face to desired degree 
    2-If we have a face from a 3D object, we extract that face and extrude it and as point 1
    3-Created object either it will remain as a new object or would be merged. 
      But if it is used as a tool to cut another 3D object, the object will disappear. 
    Known issue: 
        ???TODO: FIXME:§

"""
# TODO: As I wish to simplify the tree and make a simple
# copy of all objects, I leave it now and I should
# come back to do it. I must have it as an option in menu. (don't know how to do it now.)

"""
import DraftVecUtils
rotatedVector = DraftVecUtils.rotate(myVector,angle_in_radians,normalVector)    

We need to calculate the normal vector for each direction

x
y
45Degree
135Degree


"""


# TODO FIXME:
# Double click - Rotation only
def smartlbl_callback(smartLine, obj, parentlink):
    print("lbl callback")
    pass


# Rotation only
def callback_Rotate(userData: fr_degreewheel_widget.userDataObject=None):
    print("Rotate callback")
    pass


# Extrude in the X direction
def callback_moveX(userData: fr_degreewheel_widget.userDataObject=None):
    print("MOVEX")
    if userData is None:
        print("userData is nothing")
        return  # Nothing to do here - shouldn't be None
    events = userData.events    
    linktocaller = userData.callerObject
    if type(events) != int:
        print("event was not int")
        return
    wheelObj = userData.wheelObj

    linktocaller.direction = "X"

    clickwdgdNode = fr_coin3d.objectMouseClick_Coin3d(wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                                                        wheelObj.w_pick_radius, wheelObj.w_XsoSeparator)
    
    linktocaller.endVector = App.Vector(wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_x,
                                        wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_y,
                                        wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_z)

    if linktocaller.run_Once == False:
        linktocaller.run_Once = True
        # only once
        linktocaller.startVector = linktocaller.endVector
        linktocaller.mouseOffset = App.Vector(0, 0, 0)  # linktocaller.wheelObj.w_vector[0].sub(linktocaller.startVector)

    linktocaller.extrudeLength = (
        linktocaller.endVector - linktocaller.startVector).dot(linktocaller.normalVector)

   
    linktocaller.ExtrudeLBL.setText(
        "Length= " + str(round(linktocaller.extrudeLength, 4)))
    linktocaller.calculateNewVector()
    linktocaller.wheelObj.redraw()
    #linktocaller.reCreateExtrudeObject()
    App.ActiveDocument.recompute()


# Extrude in the Y direction
def callback_moveY(userData: fr_degreewheel_widget.userDataObject=None):
    print("MOVEY")

    if userData is None:
        print("userData is nothing")
        return  # Nothing to do here - shouldn't be None
    events = userData.events    
    linktocaller = userData.callerObject
    if type(events) != int:
        print("event was not int")
        return
    wheelObj = userData.wheelObj

    linktocaller.direction = "Y"

    clickwdgdNode = fr_coin3d.objectMouseClick_Coin3d(wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                                                        wheelObj.w_pick_radius, wheelObj.w_YsoSeparator)
    
    linktocaller.endVector = App.Vector(wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_x,
                                        wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_y,
                                        wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_z)

    if linktocaller.run_Once == False:
        linktocaller.run_Once = True
        # only once
        linktocaller.startVector = linktocaller.endVector
        linktocaller.mouseOffset = App.Vector(0, 0, 0)  # linktocaller.wheelObj.w_vector[0].sub(linktocaller.startVector)
    print("///////////////")
    print( linktocaller.endVector)
    print(linktocaller.startVector)

    print(linktocaller.normalVector)
    linktocaller.extrudeLength = (
        linktocaller.endVector-linktocaller.startVector).dot(linktocaller.normalVector)

    linktocaller.wheelObj.redraw()
    linktocaller.ExtrudeLBL.setText(
        "Length= " + str(round(linktocaller.extrudeLength, 4)))
    linktocaller.calculateNewVector()
    #linktocaller.wheelObj.w_vector[0] = linktocaller._Vector
    #linktocaller.reCreateExtrudeObject()
    App.ActiveDocument.recompute()


# Extrude in the 45 degree rotated direction
def callback_move45(userData: fr_degreewheel_widget.userDataObject=None):
    print("MOVE45")

    if userData is None:
        print("userData is nothing")
        return  # Nothing to do here - shouldn't be None
    events = userData.events    
    linktocaller = userData.callerObject
    if type(events) != int:
        print("event was not int")
        return
    wheelObj = userData.wheelObj
    linktocaller.direction = "45"

    clickwdgdNode = fr_coin3d.objectMouseClick_Coin3d(wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                                                      wheelObj.w_pick_radius, wheelObj.w_45soSeparator)

    linktocaller.endVector = App.Vector(wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_x,
                                        wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_y,
                                        wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_z)
    if linktocaller.run_Once == False:
        linktocaller.run_Once = True
        # only once
        linktocaller.startVector = linktocaller.endVector
        linktocaller.mouseOffset = App.Vector(0, 0, 0)  # linktocaller.wheelObj.w_vector[0].sub(linktocaller.startVector)
        
    print(linktocaller.normalVector)
    linktocaller.extrudeLength = (linktocaller.endVector-linktocaller.startVector).dot(linktocaller.normalVector)


    linktocaller.ExtrudeLBL.setText("Length= " + str(round(linktocaller.extrudeLength, 4)))
    linktocaller.calculateNewVector()
    linktocaller.wheelObj.redraw()
    #linktocaller.wheelObj.w_vector[0] = linktocaller._Vector
    #linktocaller.reCreateExtrudeObject()
    App.ActiveDocument.recompute()


# Extrude in the 135 degree rotated direction
def callback_move135(userData: fr_degreewheel_widget.userDataObject=None):
    print("MOVE135")

    if userData is None:
        print("userData is nothing")
        return  # Nothing to do here - shouldn't be None
    events = userData.events    
    linktocaller = userData.callerObject
    if type(events) != int:
        print("event was not int")
        return
    wheelObj = userData.wheelObj
    linktocaller.direction = "135"

    clickwdgdNode = fr_coin3d.objectMouseClick_Coin3d(wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                                                      wheelObj.w_pick_radius, wheelObj.w_135soSeparator)

    linktocaller.endVector = App.Vector(wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_x,
                                        wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_y,
                                        wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_z)
    
    if linktocaller.run_Once == False:
        linktocaller.run_Once = True
        # only once
        linktocaller.startVector = linktocaller.endVector
        linktocaller.mouseOffset = App.Vector(0, 0, 0)  # linktocaller.wheelObj.w_vector[0].sub(linktocaller.startVector)
    print("///////////////")
    print( linktocaller.endVector)
    print(linktocaller.startVector)
    print(linktocaller.normalVector)
    linktocaller.extrudeLength = (
        linktocaller.endVector-linktocaller.startVector).dot(linktocaller.normalVector)

    
    linktocaller.ExtrudeLBL.setText("Length= " + str(round(linktocaller.extrudeLength, 4)))
    linktocaller.calculateNewVector()
    linktocaller.wheelObj.redraw()
    #linktocaller.wheelObj.w_vector[0] = linktocaller._Vector
    #linktocaller.reCreateExtrudeObject()
    App.ActiveDocument.recompute()


# TODO FIXME:
def callback_release(userData: fr_degreewheel_widget.userDataObject=None):
    """
       Callback after releasing the left mouse button. 
       This callback will finalize the Extrude operation. 
       Deleting the original object will be done when the user press 'OK' button
    """
    try:
        print("release callback")
        if (userData is None):
            print("userData is None")
            raise TypeError
        events = userData.events
        linktocaller = userData.callerObject
        # Avoid activating this part several times,
        if (linktocaller.startVector is None):
            return
        print("mouse release")
        linktocaller.direction = "135"
        userData.wheelObj.remove_focus()
        linktocaller.run_Once = False
        App.ActiveDocument.recompute()
        linktocaller.startVector = None
        App.ActiveDocument.commitTransaction()  # undo reg.

    except Exception as err:
        faced.EnableAllToolbar(True)
        App.Console.PrintError("'Design456_ExtrudeRotate' ExtractFace Filed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


class Design456_SmartExtrudeRotate:
    """
        Apply Extrude to any 3D/2D object by selecting the object's face, and rotate it 
        Length of the Extrude is counted by rotation degree and the axis.
    """
    _Vector = App.Vector(0.0, 0.0, 0.0)  # WHEEL POSITION
    mw = None
    dialog = None
    tab = None
    wheelObj = None
    _mywin = None
    b1 = None
    ExtrudeLBL = None
    run_Once = False
    endVector = None
    startVector = None
    extrudeLength = 0.001  # This will be the Delta-mouse position
    # We will make two object, one for visual effect and the other is the original
    selectedObj = None
    selected=None
    direction = None
    setupRotation = [0, 0, 0, 0]
    Rotation = [0, 0, 0, 0]  # Used only with the center (cylinder)
    # We use this to simplify the code - for both, 2D and 3D object, the face variable is this
    newObject = None
    mouseOffset = App.Vector(0, 0, 0)
    OperationOption = 0  # default is zero
    objChangedTransparency = []
    ExtractedFaces = []
    FirstLocation=None

    def calculateRotatedNormal(self,Wheelaxis):
        """[calculate placement, angle of rotation, axis of rotation based on the]

        Args:
            Wheelaxis ([str]): [Direction of the wheel coin widget - Axis type ]

        Returns:
            [Base.placement]: [Placement, rotation angle and axis of rotation for face2]
        """
        
        faceRotation=0
        #TODO: Lets take only X axis first , then Y ..etc and so on. 
        face1Obj=self.ExtractedFaces[0]
        pl=self.ExtractedFaces[0].Placement
        faceDir= faced.getDirectionAxis(self.selected) #face direction

        #THIS PART WILL BE COMPLICATED AND MUST BE WELL WRITTEN. 
        #TAKE CARE OF ALL POSSIBILITIES 
        
        if  faceDir=="+x" and Wheelaxis=="X":              #faceDir ==x --> towards +Z direction
            pl.Rotation.Axis=App.Vector(0,-1,0)
            pl.Rotation.Angle=math.radians(90)
            pl.Base.x=self.selectedObj.Object.Shape.BoundBox.XMax+ self.selectedObj.Object.Shape.BoundBox.XLength  # Only X will be changed. 
            pl.Base.y=face1Obj.Placement.Base.y
            pl.Base.z=face1Obj.Placement.Base.z
            
        elif faceDir=="-x" and Wheelaxis=="X":
            pl.Rotation.Axis=App.Vector(0,-1,0)
            pl.Rotation.Angle=math.radians(90)
            pl.Base.z=self.selectedObj.Object.Shape.BoundBox.ZMax  # Only z will be changed. 
            pl.Base.y=face1Obj.Placement.Base.y
            pl.Base.x=face1Obj.Placement.Base.x

        elif (faceDir=="+x" and Wheelaxis=="Y") or (faceDir=="-x" and Wheelaxis=="Y") :
            #We do nothing .. it is ok to not change 
            pl.Rotation.Axis=App.Vector(-1,0,0)
            pl.Rotation.Angle=math.radians(0)
            pl.Base.y=face1Obj.Placement.Base.y # Only X will be changed. 
            pl.Base.x=face1Obj.Placement.Base.x
            pl.Base.z=face1Obj.Placement.Base.z
        
        elif faceDir=="+y" and Wheelaxis=="X":              #faceDir ==x --> towards +Z direction
            pl.Rotation.Axis=App.Vector(1,0,0)
            pl.Rotation.Angle=math.radians(90)
            pl.Base.y=self.selectedObj.Object.Shape.BoundBox.YMax+self.selectedObj.Object.Shape.BoundBox.YLength  # Only y will be changed. 
            pl.Base.x=face1Obj.Placement.Base.x
            pl.Base.z=face1Obj.Placement.Base.z

        elif faceDir=="-y" and Wheelaxis=="X":                        #ok Don't change
            pl.Rotation.Axis=App.Vector(1,0,0)
            pl.Rotation.Angle=math.radians(90)
            pl.Base.z=self.selectedObj.Object.Shape.BoundBox.ZMax  # Only z will be changed. 
            pl.Base.x=face1Obj.Placement.Base.x
            pl.Base.y=face1Obj.Placement.Base.y
            
        elif (faceDir=="+y" and Wheelaxis=="Y") or (faceDir=="-y" and Wheelaxis=="Y") :
            #We do nothing .. it is ok to not change 
            pl.Base = face1Obj.Placement.Base
            pl.Rotation.Axis = face1Obj.Placement.Rotation.Axis 
            pl.Rotation.Angle= face1Obj.Placement.Rotation.Angle
            
        elif  faceDir=="-z" and Wheelaxis=="X" or (faceDir=="+z" and Wheelaxis=="X"):              #faceDir ==x --> towards +Z direction
            #We do nothing .. it is ok to not change 
            pl.Base = face1Obj.Placement.Base
            pl.Rotation.Axis = face1Obj.Placement.Rotation.Axis 
            pl.Rotation.Angle= face1Obj.Placement.Rotation.Angle  
            
        elif faceDir=="+z" and Wheelaxis=="Y" :            #faceDir ==y --> towards +Y direction
            pl.Rotation.Axis=App.Vector(-1,0,0)
            pl.Rotation.Angle=math.radians(90)
            pl.Base.z=2*face1Obj.Shape.BoundBox.ZLength  # Only X will be changed. 
            pl.Base.x=face1Obj.Placement.Base.x
            pl.Base.y=face1Obj.Placement.Base.y
            
        elif faceDir=="-z" and Wheelaxis=="Y":                                                 #enough to rotate
            pl.Rotation.Axis=App.Vector(1,0,0)
            pl.Rotation.Angle=math.radians(90)
            pl.Base.x=2* face1Obj.Shape.BoundBox.XLength  # Only X will be changed. 
            pl.Base.y=face1Obj.Placement.Base.y
            pl.Base.z=face1Obj.Placement.Base.z

        # Now we have 45 and 135 Degrees : 
        
        
        
        
        
        
        
        print("pl=",pl)
        return pl
        
            
    def calculateNewVector(self):
        """[Calculate the new position that will be used for the Wheel drawing]
        Returns:
            [App.Vector]: [Position where the Wheel will be moved to]
        """
        # For now the Wheel will be at the top
        rotAxis=App.Vector(0,0,0) #Axis of the rotation for face2
        faceAngle=0             #New angle due to the rotation of face2
        base=App.Vector(0,0,0)  #New location for Face2 due to the rotation of the face
        try:
            #TODO:FIXME
            pl=self.calculateRotatedNormal(self.direction)
            self.ExtractedFaces[1].Placement=pl
            face2 = None
            if(self.isFaceOf3DObj()):
                # The whole object is selected
                sub1 = self.ExtractedFaces[1]
                face2 = sub1.Shape
            else:
                face2 = self.ExtractedFaces[1].Shape

            yL = face2.CenterOfMass
            uv = face2.Surface.parameter(yL)
            nv = face2.normalAt(uv[0], uv[1])
            self.normalVector = nv
            #Center disk rotation
            if (face2.Surface.Rotation is None):
                calAn = math.degrees(nv.getAngle(App.Vector(1, 1, 0)))
                rotation = [0, 1, 0, calAn]
            else:
                rotation = (face2.Surface.Rotation.Axis.x,
                            face2.Surface.Rotation.Axis.y,
                            face2.Surface.Rotation.Axis.z,
                            math.degrees(face2.Surface.Rotation.Angle))
            
            if (self.extrudeLength == 0):
                d = self.extrudeLength = 1
            else:
                d = self.extrudeLength
            self.ExtractedFaces[1].Placement.Base = face2.Placement.Base + d * nv  # The face itself
            if (self.wheelObj is not None):                
                self.wheelObj.w_vector[0] = yL+  d * nv  # the wheel 

            self.FirstLocation=yL+  d * nv  # the wheel 
            App.ActiveDocument.recompute()
            return rotation

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'ExtractFace getWheelPosition-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def isFaceOf3DObj(self):
        """[Check if the selected object is a face from a 3D object or is a 2D object. 
            A face from a 3D object, cannot be extruded directly. 
            We have to extract a Face and them Extrude]
            Face of 3D Object = True 
            2D Object= False
        Returns:
            [Boolean]: [Return True if the selected object is a face from 3D object, otherwise False]
        """
        if len(self.selectedObj.Object.Shape.Faces) > 1:
            return True
        else:
            return False

    def extractFaces(self):
        """[Extract a face from a 3D object as it cannot be extruded otherwise]

        Returns:
            [Face]: [Face created from the selected face of the 3D object]
        """
        try:
            name = self.selectedObj.SubElementNames[0]
            print(name)
            # TODO: THIS PART MIGHT FAIL TAKE ALL KIND OF 3D OBJECT TOO SEE IF HASATTR Subobject and then fix that
            sh = self.selectedObj.Object.Shape.copy()

            o = App.ActiveDocument.addObject("Part::Feature", "face2")
            o.Shape = sh.getElement(name)
            self.ExtractedFaces.append(Gui.ActiveDocument.getObject(o.Label).Object)
            o = App.ActiveDocument.addObject("Part::Feature", "face2")
            o.Shape = sh.getElement(name)
            self.ExtractedFaces.append(Gui.ActiveDocument.getObject(o.Label).Object)
            if hasattr(self.selectedObj.Object, "getGlobalPlacement"):
                gpl = self.selectedObj.Object.getGlobalPlacement()
                self.ExtractedFaces[0].Placement = gpl
                self.ExtractedFaces[1].Placement = gpl
            else:
                pass  # TODO: WHAT SHOULD WE DO HERE ?
                print("error")
            App.ActiveDocument.recompute()

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Design456_ExtrudeRotate' ExtractFace-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # (exc_type, fname, exc_tb.tb_lineno)

    def Activated(self):
        """[ Executes when the tool is used   ]
        """
        try:
            print("Smart ExtrudeRotate")
            self.selected = Gui.Selection.getSelectionEx()
            if len(self.selected) == 0:
                # An object must be selected
                errMessage = "Select an object, one face to Extrude"
                faced.errorDialog(errMessage)
                return
            self.selectedObj = self.selected[0]
            faced.EnableAllToolbar(False)
            # Undo
            App.ActiveDocument.openTransaction(translate("Design456", "SmartExtrudeRotate"))
            self.ExtractedFaces.clear()
            if self.isFaceOf3DObj():  # We must know if the selection is a 2D face or a face from a 3D object
                # We have a 3D Object. Extract a face and start to Extrude
                self.extractFaces()
            else:
                # We have a 2D Face - Extract it directly
                print("2d object copy the face itself")
                sh = self.selectedObj.Object.Shape.copy()
                o = App.ActiveDocument.addObject("Part::Feature", "face2")
                o.Shape = sh
                self.ExtractedFaces.append(self.selectedObj.Object)
                self.ExtractedFaces.append(App.ActiveDocument.getObject(o.Name))
            self.setupRotation = self.calculateNewVector()  # Deside how the Degree Wheel be drawn
            print("self.setupRotation",self.setupRotation)
            self.wheelObj = Fr_DegreeWheel_Widget([self.FirstLocation, App.Vector(0, 0, 0)], str(
                round(self.Rotation[3], 2)) + "°", 1, FR_COLOR.FR_RED, [0, 0, 0, 0], self.setupRotation, 1)

            # Define the callbacks. We have many callbacks here.
            # TODO: FIXME:

            # Different callbacks for each action.
            self.wheelObj.w_wheel_cb_ = callback_Rotate
            self.wheelObj.w_xAxis_cb_ = callback_moveX
            self.wheelObj.w_yAxis_cb_ = callback_moveY
            self.wheelObj.w_45Axis_cb_ = callback_move45
            self.wheelObj.w_135Axis_cb_ = callback_move135

            self.wheelObj.w_callback_ = callback_release
            self.wheelObj.w_userData.callerObject = self
            self.newObject = App.ActiveDocument.addObject('Part::Loft', 'ExtendFace')
            self.newObject.Sections = self.ExtractedFaces
            self.newObject.Solid = True
            self.newObject.Ruled = False  # TODO: SHOULD THIS BE RULED?
            self.newObject.Closed = False  # TODO: SHOULD THIS BE CLOSED?
            self.ExtractedFaces[0].Visibility = False
            self.ExtractedFaces[1].Visibility = False
            if self._mywin is None:
                self._mywin = win.Fr_CoinWindow()

            self._mywin.addWidget(self.wheelObj)
            mw = self.getMainWindow()
            self._mywin.show()

            # TODO: FIXME:
            # loft will be used . make some experementations.
            # But when should we use sweep???? don't know now

            App.ActiveDocument.recompute()

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Design456_ExtrudeRotate' ExtractFace-Failed. "
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
            self.wheelObj.hide()
            self.wheelObj.__del__()  # call destructor
            if self._mywin is not None:
                self._mywin.hide()
                del self._mywin
                self._mywin = None
            App.ActiveDocument.commitTransaction()  # undo reg.
            self.mw = None
            self.dialog = None
            self.tab = None
            self.wheelObj = None
            self._mywin = None
            self.b1 = None
            self.ExtrudeLBL = None
            self.run_Once = False
            self.endVector = None
            self.startVector = None
            self.extrudeLength = 0.001  # This will be the Delta-mouse position
            # We will make two object, one for visual effect and the other is the original
            self.selectedObj = None
            self.selected=None
            self.direction = None
            self.setupRotation = [0, 0, 0, 0]
            self.Rotation = [0, 0, 0, 0]  # Used only with the center (cylinder)
            # We use this to simplify the code - for both, 2D and 3D object, the face variable is this
            self.newObject = None
            self.mouseOffset = App.Vector(0, 0, 0)
            self.OperationOption = 0  # default is zero
            self.objChangedTransparency = []
            self.ExtractedFaces = []
            self.FirstLocation=None
            del self

        except Exception as err:
            App.Console.PrintError("'Design456_ExtrudeRotate' ExtractFace-Failed. "
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
            self.tab.addTab(self.dialog, "Smart Extrude Rotate")
            self.tab.setCurrentWidget(self.dialog)
            self.dialog.resize(200, 450)
            self.dialog.setWindowTitle("Smart Extrude Rotate")
            self.la = QtGui.QVBoxLayout(self.dialog)
            self.e1 = QtGui.QLabel(
                "(Smart Extrude Rotate)\nFor quicker\nApplying Extrude")
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
            self.ExtrudeLBL = QtGui.QLabel("Extrude Length=")
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
            self.radAsIs.toggled.connect(lambda: self.btnState(self.radAsIs))
            self.radMerge.toggled.connect(lambda: self.btnState(self.radMerge))
            self.radSubtract.toggled.connect(
                lambda: self.btnState(self.radSubtract))

            QtCore.QObject.connect(
                okbox, QtCore.SIGNAL("accepted()"), self.hide)
            QtCore.QMetaObject.connectSlotsByName(self.dialog)

            return self.dialog

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Design456_ExtrudeRotate' ExtractFace-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def btnState(self, button):
        if button.text() == "As Is":
            if button.isChecked() == True:
                self.OperationOption = 0  # 0 as Is default, 1 Merged, 2 Subtracted
        elif button.text() == "Merge":
            if button.isChecked() == True:
                self.OperationOption = 1
        elif button.text() == "Subtract":
            if button.isChecked() == True:
                self.OperationOption = 2

    def hide(self):
        """
        Hide the widgets. Remove also the tab.
        TODO:
        For this tool, I decide to choose the hide to merge, subtract or leave it as is here. 
        I can do that during the extrusion (moving the Wheel), but that will be an action
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
            if (self.isFaceOf3DObj() == True):
                # No 3D but collision might happen.
                pass

        self.dialog.hide()
        del self.dialog
        dw = self.mw.findChildren(QtGui.QDockWidget)
        newsize = self.tab.count()  # Todo : Should we do that?
        self.tab.removeTab(newsize - 1)  # it ==0,1,2,3 ..etc
        App.ActiveDocument.commitTransaction()  # undo reg.
        App.ActiveDocument.recompute()
        self.__del__()  # Remove all smart Extrude Rotate 3dCOIN widgets

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_SmartExtrudeRotate.svg',
            'MenuText': ' Smart Extrude Rotate',
                        'ToolTip':  ' Smart Extrude Rotate'
        }


Gui.addCommand('Design456_SmartExtrudeRotate', Design456_SmartExtrudeRotate())
