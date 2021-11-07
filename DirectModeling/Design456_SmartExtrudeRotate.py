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
import Part as _part

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
# come back to do it. I must have it as an option in FreeCAD Preferences-menu. (don't know how to do it now.)


# TODO FIXME:
# Double click - Rotation only
def smartlbl_callback(smartLine, obj, parentlink):
    print("lbl callback")
    pass


# Rotation only TODO: FIXME:
def callback_Rotate(userData: fr_degreewheel_widget.userDataObject = None):
    if userData is None:
        print("userData is nothing")
        return  # Nothing to do here - shouldn't be None
    events = userData.events
    linktocaller = userData.callerObject
    linktocaller.isItRotation = True           # Disallow Axis manupulations
    if type(events) != int:
        print("event was not int")
        return
    wheelObj = userData.wheelObj
    linktocaller.direction = "Center"
    clickwdgdNode = fr_coin3d.objectMouseClick_Coin3d(wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                                                      wheelObj.w_pick_radius, wheelObj.w_centersoSeparator)

    linktocaller.endVector = App.Vector(wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_x,
                                        wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_y,
                                        wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_z)
    startX = startY = 0
    if linktocaller.editing is False:
        if linktocaller.run_Once is False:
            linktocaller.run_Once = True
            # only once
            linktocaller.startVector = linktocaller.endVector
            App.ActiveDocument.removeObject(linktocaller.newObject.Name)
            del linktocaller.newObject  # remove any object exist (loft)
            linktocaller.reCreateRevolveObj(0)
            linktocaller.editing = True
            wheelObj.w_vector[0].z=0

    else:
        linktocaller.run_Once = True
        if (linktocaller.startVector is None):
            linktocaller.startVector = linktocaller.endVector
    oldangle = wheelObj.w_Rotation[3]
    mx = wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_x
    my = wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_y
    mz = wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_z
    # calculating the angle in a better way:
    print(linktocaller.normalVector)
    if abs(linktocaller.normalVector.x) == 1:
        angle = math.degrees(math.atan2(mz, mx))
    elif abs(linktocaller.normalVector.y) == 1:
        angle = math.degrees(math.atan2(mz, my))
    elif abs(linktocaller.normalVector.z) == 1:
        angle = math.degrees(math.atan2(my, mx))
    # Here axis has an angel  find a best way to calculate
    else:
        angle = math.atan2(mz/my)  # Not sure if this will be good TODO:FIXME:
    print("AngleBefore", angle)
    angle = round(angle, 1)
    while (angle < (oldangle-180)):
        angle = angle+360
    while (angle > (oldangle+180)):
        angle = angle-360
    print("AngleAfter", angle)
    if (angle < -360):
        angle = -360
    elif (angle > 360):
        angle = 360

    if (linktocaller.RotateLBL is not None):
        linktocaller.RotateLBL.setText("Rotation Axis= " + "(" +
                                       str(linktocaller.w_rotation[0])+","
                                       + str(linktocaller.w_rotation[1]) +
                                       "," +
                                       str(linktocaller.w_rotation[2]) + ")"
                                       + "\nRotation Angle= " + str(angle) + " °")

    wheelObj.w_Rotation[3] = angle
    if linktocaller.newObject is None:
        return
    linktocaller.newObject.Angle = angle
    wheelObj.redraw()
    App.ActiveDocument.recompute()


# Extrude in the X direction
def callback_moveX(userData: fr_degreewheel_widget.userDataObject = None):
    print("MOVEX")
    if userData is None:
        print("userData is nothing")
        return  # Nothing to do here - shouldn't be None
    events = userData.events
    linktocaller = userData.callerObject
    if linktocaller.isItRotation is True:
        callback_Rotate(userData)
        return  # We cannot allow this tool
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

    if linktocaller.run_Once is False:
        linktocaller.run_Once = True
        # only once
        linktocaller.startVector = linktocaller.endVector
        # linktocaller.wheelObj.w_vector[0].sub(linktocaller.startVector)
        linktocaller.mouseOffset = App.Vector(0, 0, 0)

    linktocaller.extrudeLength = (
        linktocaller.endVector - linktocaller.startVector).dot(linktocaller.normalVector)

    linktocaller.ExtrudeLBL.setText(
        "Length= " + str(round(linktocaller.extrudeLength, 4)))
    linktocaller.calculateNewVector()
    linktocaller.wheelObj.redraw()
    # linktocaller.reCreateExtrudeObject()
    App.ActiveDocument.recompute()


# Extrude in the Y direction
def callback_moveY(userData: fr_degreewheel_widget.userDataObject = None):
    print("MOVEY")

    if userData is None:
        print("userData is nothing")
        return  # Nothing to do here - shouldn't be None
    events = userData.events
    linktocaller = userData.callerObject
    if linktocaller.isItRotation is True:
        callback_Rotate(userData)
        return  # We cannot allow this tool

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

    if linktocaller.run_Once is False:
        linktocaller.run_Once = True
        # only once
        linktocaller.startVector = linktocaller.endVector
        # linktocaller.wheelObj.w_vector[0].sub(linktocaller.startVector)
        linktocaller.mouseOffset = App.Vector(0, 0, 0)
    linktocaller.extrudeLength = (
        linktocaller.endVector-linktocaller.startVector).dot(linktocaller.normalVector)

    linktocaller.wheelObj.redraw()
    linktocaller.ExtrudeLBL.setText(
        "Length= " + str(round(linktocaller.extrudeLength, 4)))
    linktocaller.calculateNewVector()
    # linktocaller.wheelObj.w_vector[0] = linktocaller._Vector
    # linktocaller.reCreateExtrudeObject()
    App.ActiveDocument.recompute()


# Extrude in the 45 degree rotated direction
def callback_move45(userData: fr_degreewheel_widget.userDataObject = None):
    print("MOVE45")

    if userData is None:
        print("userData is nothing")
        return  # Nothing to do here - shouldn't be None
    events = userData.events
    linktocaller = userData.callerObject
    if linktocaller.isItRotation is True:
        callback_Rotate(userData)
        return  # We cannot allow this tool

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
    if linktocaller.run_Once is False:
        linktocaller.run_Once = True
        # only once
        linktocaller.startVector = linktocaller.endVector
        # linktocaller.wheelObj.w_vector[0].sub(linktocaller.startVector)
        linktocaller.mouseOffset = App.Vector(0, 0, 0)

    linktocaller.extrudeLength = (
        linktocaller.endVector-linktocaller.startVector).dot(linktocaller.normalVector)

    linktocaller.ExtrudeLBL.setText(
        "Length= " + str(round(linktocaller.extrudeLength, 4)))
    linktocaller.calculateNewVector()
    linktocaller.wheelObj.redraw()
    #linktocaller.wheelObj.w_vector[0] = linktocaller._Vector
    # linktocaller.reCreateExtrudeObject()
    App.ActiveDocument.recompute()


# Extrude in the 135 degree rotated direction
def callback_move135(userData: fr_degreewheel_widget.userDataObject = None):
    print("MOVE135")

    if userData is None:
        print("userData is nothing")
        return  # Nothing to do here - shouldn't be None
    events = userData.events
    linktocaller = userData.callerObject
    if linktocaller.isItRotation is True:
        callback_Rotate(userData)
        return  # We cannot allow this tool

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

    if linktocaller.run_Once is False:
        linktocaller.run_Once = True
        # only once
        linktocaller.startVector = linktocaller.endVector
        # linktocaller.wheelObj.w_vector[0].sub(linktocaller.startVector)
        linktocaller.mouseOffset = App.Vector(0, 0, 0)
    linktocaller.extrudeLength = (
        linktocaller.endVector-linktocaller.startVector).dot(linktocaller.normalVector)

    linktocaller.ExtrudeLBL.setText(
        "Length= " + str(round(linktocaller.extrudeLength, 4)))
    linktocaller.calculateNewVector()
    linktocaller.wheelObj.redraw()
    #linktocaller.wheelObj.w_vector[0] = linktocaller._Vector
    # linktocaller.reCreateExtrudeObject()
    App.ActiveDocument.recompute()


# TODO FIXME:
def callback_release(userData: fr_degreewheel_widget.userDataObject = None):
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
        userData.wheelObj.remove_focus()
        linktocaller.run_Once = False
        App.ActiveDocument.recompute()
        linktocaller.startVector = None
        App.ActiveDocument.commitTransaction()  # undo reg.

    except Exception as err:
        faced.EnableAllToolbar(True)
        App.Console.PrintError("'Design456_ExtrudeRotate' Callback Release Filed. "
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
    editing = False
    w_rotation = [0.0, 0.0, 0.0, 0.0]  # Center/Wheel rotation
    _mywin = None
    b1 = None
    ExtrudeLBL = None
    RotateLBL = None
    run_Once = False
    endVector = None
    startVector = None
    extrudeLength = 0.001  # This will be the Delta-mouse position
    # We will make two object, one for visual effect and the other is the original
    selectedObj = None
    selected = None
    direction = None
    faceDir = None
    setupRotation = [0, 0, 0, 0]
    # We use this to simplify the code
    # for both, 2D and 3D object, the face variable is this
    newObject = None
    mouseOffset = App.Vector(0, 0, 0)
    OperationOption = 0  # default is zero
    OperationType = 0      # default is zero
    objChangedTransparency = []
    ExtractedFaces = []
    FirstLocation = None
    # We cannot combine rotation with direction extrusion.
    # This varialbe is used to disale all other options
    isItRotation = False

    def calculateRotatedNormal(self, Wheelaxis):
        """[calculate placement, angle of rotation, axis of rotation based on the]

        Args:
            Wheelaxis ([str]): [Direction of the wheel coin widget - Axis type ]

        Returns:
            [Base.placement]: [Placement, rotation angle and axis of rotation for face2]
        """
        if self.isItRotation is True:
            return  # We shouldnt be here .

        faceRotation = 0
        # TODO: Lets take only X axis first , then Y ..etc and so on.
        face1Obj = self.ExtractedFaces[0]
        pl = self.ExtractedFaces[0].Placement
        self.faceDir = faced.getDirectionAxis(self.selected)  # face direction

        # THIS PART WILL BE COMPLICATED AND MUST BE WELL WRITTEN.

        # Wheelaxis color: RED is X , GREEN is Y,  FR_BLUEVIOLET is 45 and ORANGE is 135
        s = self.ExtractedFaces[1]
        # Reset the placement of the object if was not correct
        s.Placement = self.ExtractedFaces[0].Placement
        ax = self.selectedObj.Object.Shape.CenterOfMass
        if self.faceDir == "+x" and Wheelaxis == "X":
            faced.RealRotateObjectToAnAxis(s, ax, 0, 90, 0)
            self.ExtractedFaces[1].Placement.Base.x = self.ExtractedFaces[1].Placement.Base.x + \
                self.ExtractedFaces[1].Shape.BoundBox.XLength
            pl = self.ExtractedFaces[1].Placement

        elif self.faceDir == "-x" and Wheelaxis == "X":
            faced.RealRotateObjectToAnAxis(s, ax, 0, 90, 0)
            self.ExtractedFaces[1].Placement.Base.x = self.ExtractedFaces[1].Placement.Base.x - \
                self.ExtractedFaces[1].Shape.BoundBox.XLength
            pl = self.ExtractedFaces[1].Placement

        elif (self.faceDir == "+x" and Wheelaxis == "Y") or (self.faceDir == "-x" and Wheelaxis == "Y"):
            # We do nothing .. it is ok to not change
            pl = self.ExtractedFaces[1].Placement

        elif self.faceDir == "+y" and Wheelaxis == "X":
            faced.RealRotateObjectToAnAxis(s, ax, 0, 0, -90)
            self.ExtractedFaces[1].Placement.Base.y = self.ExtractedFaces[1].Placement.Base.y + \
                self.ExtractedFaces[1].Shape.BoundBox.YLength
            pl = self.ExtractedFaces[1].Placement

        elif self.faceDir == "-y" and Wheelaxis == "X":
            faced.RealRotateObjectToAnAxis(s, ax, 0, 0, 90)
            self.ExtractedFaces[1].Placement.Base.y = self.ExtractedFaces[1].Placement.Base.y - \
                self.ExtractedFaces[1].Shape.BoundBox.YLength
            pl = self.ExtractedFaces[1].Placement

        elif (self.faceDir == "+y" and Wheelaxis == "Y") or (self.faceDir == "-y" and Wheelaxis == "Y"):
            pl = self.ExtractedFaces[1].Placement

        elif self.faceDir == "-z" and Wheelaxis == "X" or (self.faceDir == "+z" and Wheelaxis == "X"):
            pl = self.ExtractedFaces[1].Placement

        elif self.faceDir == "+z" and Wheelaxis == "Y":
            faced.RealRotateObjectToAnAxis(s, ax, 0, 0, -90)
            pl = self.ExtractedFaces[1].Placement

        elif self.faceDir == "-z" and Wheelaxis == "Y":
            faced.RealRotateObjectToAnAxis(s, ax, 0, 0, 90)
            pl = self.ExtractedFaces[1].Placement

        # Now we have 45Degrees :
        if self.faceDir == "+x" and Wheelaxis == "45":
            faced.RotateObjectToCenterPoint(s, 0, 45, 0)
            pl = self.ExtractedFaces[1].Placement

        elif self.faceDir == "-x" and Wheelaxis == "45":
            faced.RotateObjectToCenterPoint(s, 0, 45, 0)
            pl = self.ExtractedFaces[1].Placement

        # Now we have 45 Degrees :
        if self.faceDir == "+y" and Wheelaxis == "45":
            faced.RotateObjectToCenterPoint(s, 0, 0, -45)
            pl = self.ExtractedFaces[1].Placement

        elif self.faceDir == "-y" and Wheelaxis == "45":
            faced.RotateObjectToCenterPoint(s, 0, 0, -45)
            pl = self.ExtractedFaces[1].Placement

            # Now we have 45 and 135 Degrees :
        if self.faceDir == "+z" and Wheelaxis == "45":
            faced.RotateObjectToCenterPoint(s, 0, 0, 45)
            pl = self.ExtractedFaces[1].Placement

        elif self.faceDir == "-z" and Wheelaxis == "45":
            faced.RotateObjectToCenterPoint(s, 0, 0, 45)
            pl = self.ExtractedFaces[1].Placement

        # Now we have 135 Degrees :
        if self.faceDir == "+x" and Wheelaxis == "135":
            faced.RotateObjectToCenterPoint(s, 0, 135, 0)
            pl = self.ExtractedFaces[1].Placement

        elif self.faceDir == "-x" and Wheelaxis == "135":
            faced.RotateObjectToCenterPoint(s, 0, 135, 0)
            pl = self.ExtractedFaces[1].Placement

        if self.faceDir == "+y" and Wheelaxis == "135":
            faced.RotateObjectToCenterPoint(s, 0, 0, -135)
            pl = self.ExtractedFaces[1].Placement

        elif self.faceDir == "-y" and Wheelaxis == "135":
            faced.RotateObjectToCenterPoint(s, 0, 0, -135)
            pl = self.ExtractedFaces[1].Placement

        if self.faceDir == "+z" and Wheelaxis == "135":
            faced.RotateObjectToCenterPoint(s, 0, 0, 135)
            pl = self.ExtractedFaces[1].Placement

        elif self.faceDir == "-z" and Wheelaxis == "135":
            faced.RotateObjectToCenterPoint(s, 0, 0, 135)
            pl = self.ExtractedFaces[1].Object.Placement

        return pl

    # TODO: FIXME:

    def reCreateRevolveObj(self, angle):
        try:
            # Create the Revolution
            # remove totally the second face, not required anymore.
            startY = self.wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Qt_y
            startX = self.wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Qt_x
            self.newObject = App.ActiveDocument.addObject(
                "Part::Revolution", "ExtendRotate")
            App.ActiveDocument.removeObject(self.ExtractedFaces[1].Name)
            self.ExtractedFaces[1] = None
            # to allow the creation other wise you get OCCT error, angl<>0
            self.newObject.Angle = angle
            self.newObject.Solid = True
            self.newObject.Symmetric = False
            self.newObject.Source = self.ExtractedFaces[0]
            nor = faced.getNormalized(self.ExtractedFaces[0])
            bas = faced.getBase(self.ExtractedFaces[0])
            self.newObject.Base = bas
            self.newObject.Axis = nor
            # Try this .. might be correct
            self.wheelObj.w_Rotation[0] = nor.x
            self.wheelObj.w_Rotation[1] = nor.y
            self.wheelObj.w_Rotation[2] = nor.z

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'create revolve -Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def calculateNewVector(self):
        """[Calculate the new position that will be used for the Wheel drawing]
        Returns:
            [App.Vector]: [Position where the Wheel will be moved to]
        """
        # For now the Wheel will be at the top
        rotAxis = App.Vector(0, 0, 0)  # Axis of the rotation for face2
        faceAngle = 0  # New angle due to the rotation of face2
        # New location for Face2 due to the rotation of the face
        base = App.Vector(0, 0, 0)
        try:
            # TODO:FIXME
            pl = self.calculateRotatedNormal(self.direction)
            if(self.ExtractedFaces[1] != None):
                self.ExtractedFaces[1].Placement = pl
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
            # Setup calculation.
            if (face2.Surface.Rotation is None):
                calAn = math.degrees(nv.getAngle(App.Vector(1, 1, 0)))
                rotation = [0, 1, 0, calAn]
            else:
                rotation = [face2.Surface.Rotation.Axis.x,
                            face2.Surface.Rotation.Axis.y,
                            face2.Surface.Rotation.Axis.z,
                            math.degrees(face2.Surface.Rotation.Angle)]

            if (self.extrudeLength == 0):
                d = self.extrudeLength = 1
            else:
                d = self.extrudeLength
            # The face itself
            self.ExtractedFaces[1].Placement.Base = face2.Placement.Base + d * nv
            if (self.wheelObj is not None):
                self.wheelObj.w_vector[0] = yL + d * nv  # the wheel

            self.FirstLocation = yL + d * nv  # the wheel
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

            o = App.ActiveDocument.addObject("Part::Feature", "BaseFace")
            o.Shape = sh.getElement(name)
            self.ExtractedFaces.append(
                Gui.ActiveDocument.getObject(o.Label).Object)
            o = App.ActiveDocument.addObject("Part::Feature", "MovableFace")
            o.Shape = sh.getElement(name)
            self.ExtractedFaces.append(
                Gui.ActiveDocument.getObject(o.Label).Object)
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
            App.ActiveDocument.openTransaction(
                translate("Design456", "SmartExtrudeRotate"))
            self.ExtractedFaces.clear()
            if self.isFaceOf3DObj():  # We must know if the selection is a 2D face or a face from a 3D object
                # We have a 3D Object. Extract a face and start to Extrude
                self.extractFaces()
            else:
                # We have a 2D Face - Extract it directly
                print("2d object copy the face itself")
                sh = self.selectedObj.Object.Shape.copy()
                o = App.ActiveDocument.addObject(
                    "Part::Feature", "MovableFace")
                o.Shape = sh
                self.ExtractedFaces.append(self.selectedObj.Object)
                self.ExtractedFaces.append(
                    App.ActiveDocument.getObject(o.Name))

            # Deside how the Degree Wheel be drawn
            self.setupRotation = self.calculateNewVector()
            if self.faceDir == "+z" or self.faceDir == "-z":
                self.wheelObj = Fr_DegreeWheel_Widget([self.FirstLocation, App.Vector(0, 0, 0)], str(
                    round(self.w_rotation[3], 2)) + "°", 1, FR_COLOR.FR_RED, [0, 0, 0, 0],
                    self.setupRotation, [2.0, 2.0, 2.0], 2)
            else:
                self.wheelObj = Fr_DegreeWheel_Widget([self.FirstLocation, App.Vector(0, 0, 0)], str(
                    round(self.w_rotation[3], 2)) + "°", 1, FR_COLOR.FR_RED, [0, 0, 0, 0],
                    self.setupRotation, [2.0, 2.0, 2.0], 1)

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
            self.newObject = App.ActiveDocument.addObject(
                'Part::Loft', 'ExtendFace')
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
            self.editing = False
            App.ActiveDocument.recompute()
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
            self.extrudeLength = 0.0
            # We will make two object, one for visual effect and the other is the original
            self.selectedObj = None
            self.selected = None

            self.direction = None
            self.setupRotation = [0, 0, 0, 0]
            # Used only with the center (cylinder)
            self.Rotation = [0, 0, 0, 0]
            # We use this to simplify the code - for both, 2D and 3D object, the face variable is this
            self.newObject = None
            self.mouseOffset = App.Vector(0, 0, 0)
            self.OperationOption = 0  # default is zero
            self.objChangedTransparency = []
            self.ExtractedFaces = []
            self.FirstLocation = None
            self.isItRotation = False
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
            oldsize = self.tab.count()
            self.dialog = QtGui.QDialog()
            self.tab.addTab(self.dialog, "Smart Extrude Rotate")
            self.frmRotation = QtGui.QFrame(self.dialog)
            self.dialog.resize(200, 450)
            self.frmRotation.setGeometry(QtCore.QRect(10, 190, 231, 181))
            self.frame_2 = QtGui.QFrame(self.dialog)
            self.frame_2.setGeometry(QtCore.QRect(10, 195, 231, 151))
            self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
            self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
            self.frame_2.setObjectName("frame_2")
            self.gridLayoutWidget_3 = QtGui.QWidget(self.frame_2)
            self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 40, 211, 101))
            self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
            self.gridExtrusionResult = QtGui.QGridLayout(
                self.gridLayoutWidget_3)
            self.gridExtrusionResult.setContentsMargins(0, 0, 0, 0)
            self.gridExtrusionResult.setObjectName("gridExtrusionResult")
            self.radioAsIs = QtGui.QRadioButton(self.gridLayoutWidget_3)
            self.radioAsIs.setObjectName("radioAsIs")
            self.gridExtrusionResult.addWidget(self.radioAsIs, 0, 0, 1, 1)
            self.radioMerge = QtGui.QRadioButton(self.gridLayoutWidget_3)
            self.radioMerge.setObjectName("radioMerge")
            self.gridExtrusionResult.addWidget(self.radioMerge, 1, 0, 1, 1)
            self.lblExtrusionResult = QtGui.QLabel(self.frame_2)
            self.lblExtrusionResult.setGeometry(QtCore.QRect(10, 0, 191, 61))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.lblExtrusionResult.setFont(font)
            self.lblExtrusionResult.setObjectName("lblExtrusionResult")
            self.btnOK = QtGui.QDialogButtonBox(self.dialog)
            self.btnOK.setGeometry(QtCore.QRect(270, 360, 111, 61))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.btnOK.setFont(font)
            self.btnOK.setObjectName("btnOK")
            self.btnOK.setStandardButtons(QtGui.QDialogButtonBox.Ok)
            self.lblTitle = QtGui.QLabel(self.dialog)
            self.lblTitle.setGeometry(QtCore.QRect(10, 10, 281, 91))
            font = QtGui.QFont()
            font.setFamily("Times New Roman")
            font.setPointSize(10)
            self.lblTitle.setFont(font)
            self.lblTitle.setObjectName("lblTitle")
            self.ExtrudeLBL = QtGui.QLabel(self.dialog)
            self.ExtrudeLBL.setGeometry(QtCore.QRect(10, 145, 321, 40))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.ExtrudeLBL.setFont(font)
            self.ExtrudeLBL.setObjectName("ExtrudeLBL")
            self.RotateLBL = QtGui.QLabel(self.dialog)
            self.RotateLBL.setGeometry(QtCore.QRect(10, 100, 281, 40))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.RotateLBL.setFont(font)
            self.RotateLBL.setObjectName("RotateLBL")

            _translate = QtCore.QCoreApplication.translate
            self.dialog.setWindowTitle(_translate(
                "Dialog", "Smart Extrude Rotate"))

            self.radioAsIs.setText(_translate("Dialog", "As Is"))
            self.radioMerge.setText(_translate("Dialog", "Merge"))
            self.lblExtrusionResult.setText(
                _translate("Dialog", "Extrusion Result"))
            self.lblTitle.setText(_translate("Dialog", "(Smart Extrude Rotate)\n"
                                             "For quicker applying Extrude"))
            self.ExtrudeLBL.setText(_translate("Dialog", "Extrusion Length="))
            self.RotateLBL.setText(_translate("Dialog", "Extrusion Angle="))

            self.radioAsIs.setChecked(True)
            # self.radioBottom.setChecked(True)

            self.radioAsIs.toggled.connect(
                lambda: self.btnState(self.radioAsIs))
            self.radioMerge.toggled.connect(
                lambda: self.btnState(self.radioMerge))

            QtCore.QObject.connect(
                self.btnOK, QtCore.SIGNAL("accepted()"), self.hide)
            QtCore.QMetaObject.connectSlotsByName(self.dialog)
            self.tab.setCurrentWidget(self.dialog)

            return self.dialog

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Design456_ExtrudeRotate' ExtractFace-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def btnState(self, button):
        if (button == None):
            print("button was none why?")
            return
        if button.text() == "As Is":
            if button.isChecked() is True:
                self.OperationOption = 0  # 0 as Is default, 1 Merged, 2 Subtracted
        elif button.text() == "Merge":
            if button.isChecked() is True:
                self.OperationOption = 1

    def hide(self):
        """
        Hide the widgets. Remove also the tab.
        TODO:
        For this tool, I decide to choose the hide to merge, or leave it "as is" here. 
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
            if (self.isFaceOf3DObj() is True):
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
