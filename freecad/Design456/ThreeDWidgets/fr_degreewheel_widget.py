from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2025                                                    *
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
import ThreeDWidgets
import pivy.coin as coin
from ThreeDWidgets import fr_widget
from ThreeDWidgets import constant
from typing import List
from ThreeDWidgets import fr_label_draw
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
import FACE_D as faced
from dataclasses import dataclass
from ThreeDWidgets import fr_wheel_draw
import math
"""
Example how to use this widget. 

# show the window and it's widgets. 
import ThreeDWidgets.fr_arrow_widget as wd
import ThreeDWidgets.fr_coinwindow as wnn
import math
from ThreeDWidgets import fr_degreewheel_widget as w 
mywin = wnn.Fr_CoinWindow()

rotation=0
color=(1,0,1)
vec=[]
vec.append(App.Vector(0.0, 0.0, 0.0))
vec.append(App.Vector(5,0,0))
preRot=[0,0,0,0]
scale=[1,1,1]
rotation=[0.0, 0.0, 0.0, 0.0]
arrows=w.Fr_DegreeWheel_Widget(vec,"Test",1, color,rotation,preRot,scale,0)
mywin.addWidget(arrows)
mywin.show()

"""
__updated__ = '2022-11-02 20:35:57'


@dataclass
class userDataObject:
    __slots__ = ['wheelObj', 'events', 'callerObject']
    def __init__(self):
        self.wheelObj = None      # the wheel widget object
        self.events = None        # events - save handle events here
        self.callerObject = None  # Class/Tool uses the fr_wheel_widget


# *******************************CALLBACKS DEMO *********************************************
def callback(userData: userDataObject = None):
    """
        This function executes when the Widget as whole got an event
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy FR_WHELL_WIDGET General callback")


def callback1(userData: userDataObject = None):
    """
        This function executes when the Center has an event 
        event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy Center-wheel-widget callback1")


def callback2(userData: userDataObject = None):
    """
        This function executes when the XAxis 
        event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy XAxis callback")


def callback3(userData: userDataObject = None):
    """
        This function executes when the YAxis 
        event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy YAxis callback")


def callback4(userData: userDataObject = None):
    """
        This function executes when the 45Axis 
        event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy 45Axis callback")


def callback5(userData: userDataObject = None):
    """
        This function executes when the 135Axis 
        event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy 135Axis callback")

# *************************************************************


class Fr_DegreeWheel_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a one Degrees wheel
    This will be used later to create 3D wheel.
    Or it can be used as a single rotate/move widget
    """

    def __init__(self, vectors: List[App.Vector] = [],
                 label: str = "", lineWidth=1,
                 _color=FR_COLOR.FR_BLACK,
                 _Rotation=[0.0, 0.0, 1.0, 0.0],
                 _prerotation=[0.0, 0.0, 0.0, 0.0],
                 _scale=[1, 1, 1],
                 _wheelLBLType=0,
                 _wheelAxis='XY'): 
        """_summary_

        Args:
            vectors (List[App.Vector], optional): _description_. Defaults to [].
            label (str, optional): _description_. Defaults to "".
            lineWidth (int, optional): _description_. Defaults to 1.
            _color (_type_, optional): _description_. Defaults to FR_COLOR.FR_BLACK.
            _Rotation (list, optional): _description_. Defaults to [0.0, 0.0, 0.0, 0.0].
            _prerotation (list, optional): _description_. Defaults to [0.0, 0.0, 0.0, 0.0].
            _scale (list, optional): _description_. Defaults to [1, 1, 1].
            _wheelLBLType (int, optional): Decide how the label will be drawn. Defaults to 0. Options: 0,1,2
            _wheelAxis (str, optional): Wheel Placement on different Plane . Defaults to 'XY'. Options =XY,XZ,YZ
        """
        super().__init__(vectors, label)
        
        self.w_lbluserData= fr_widget.propertyValues()
        self.w_lineWidth = lineWidth  # Default line width
        self.w_widgetType = constant.FR_WidgetType.FR_WHEEL
        self.w_wheelLBLType = _wheelLBLType
        # General widget callback (mouse-button) function - External function
        self.w_callback_ = callback
        self.w_lbl_calback_ = callback              # Label callback
        self.w_KB_callback_ = callback              # Keyboard
        self.w_move_callback_ = callback            # Mouse movement callback
        # **************************************************************************
        # We have to define the three wheels here :                               *
        #     ZX  is the first  one -- It has Front Camera View   =0 in the list  *
        #     ZY  is the second one -- It has Right Camera View   =1 in the list  *
        #     XY  is the Third  one -- It has the Top Camera View =2 in the list  *
        # **************************************************************************

        # Dummy callback          Movement in the disk rotation (mouse click-release)
        self.w_wheel_cb_ = callback1
        # Dummy callback         Movement in the X direction (mouse click-release)
        self.w_xAxis_cb_ = callback2
        # Dummy callback         Movement in the y direction (mouse click-release)
        self.w_yAxis_cb_ = callback3
        # Dummy callback          Movement in the 45degree direction (mouse click-release)
        self.w_45Axis_cb_ = callback4
        # Dummy callback          Movement in the 135degree direction (mouse click-release)
        self.w_135Axis_cb_ = callback5

        self.w_wdgsoSwitch = coin.SoSwitch()           # the whole widget
        self.w_XsoSeparator = coin.SoSeparator()         # X cylinder
        self.w_YsoSeparator = coin.SoSeparator()         # Y cylinder
        self.w_45soSeparator = coin.SoSeparator()        # 45degree cylinder
        self.w_135soSeparator = coin.SoSeparator()       # 135degree cylinder
        self.w_CenterSoSeparator = coin.SoSeparator()    # center disk cylinder

        self.w_color = _color  # TODO: Not sure if we use this

        self.w_Scale = _scale

        self.w_Xrotation = [0, 0, 0, 0]
        self.w_Yrotation = [0, 0, 0, 0]
        self.w_Zrotation = [0, 0, 0, 0]

        self.w_userData = userDataObject()  # Keep info about the widget
        self.w_userData.wheelObj = self
        # self.w_userData.color=_color
        self.releaseDrag = False  # Used to avoid running drag code while it is in drag mode
        # Use this to keep the selected so during push-drag, after release it should be none
        self.currentSo = None
        
        self.oldAngle = 0.0
        self.w_wheelAngle = _Rotation[3]
        self.run_Once = None
        self.axisType = _wheelAxis # This is the direction of the wheel. . 
        self.rotationDirection = 1  # +1 CCW , -1 ACCWs
        
        # This affect only the whole-Widget label - nothing else
        self.w_lbluserData.linewidth = self.w_lineWidth
        if (self.w_wheelLBLType == 0):
            self.w_lbluserData.SetupRotation = App.Vector(
                0, 0, 0)  # OK Don't change
        elif(self.w_wheelLBLType == 1):
            self.w_lbluserData.SetupRotation = App.Vector(
                90, 0, 0)  # OK Don't change
        elif(self.w_wheelLBLType == 2):
            self.w_lbluserData.SetupRotation = App.Vector(90, 90, 0)

        # Use this to save rotation degree of the disk which is the whole widget angle.
        self.w_WidgetDiskRotation = 0.0
        self.w_Rotation = _Rotation
        self.w_PRErotation = _prerotation
        # TODO: FIXME:
        if(self.w_wheelLBLType == 0):  # This affect only the Widget label position- nothing else
            # When is is Top view.
            self.w_lbluserData.vectors = [
                (self.w_vector[0].x+2, self.w_vector[0].y+6, self.w_vector[0].z), (0, 0, 0)]  # OK Don't change
        elif (self.w_wheelLBLType == 1):
            # When is
            self.w_lbluserData.vectors = [
                (self.w_vector[0].x, self.w_vector[0].y+2, self.w_vector[0].z+6), (0, 0, 0)]

        elif (self.w_wheelLBLType == 2):
            # When is
            self.w_lbluserData.vectors = [
                (self.w_vector[0].x+1, self.w_vector[0].y, self.w_vector[0].z+6), (0, 0, 0)]

    def lineWidth(self, width):
        """ Set line-width 
        """
        self.w_lineWidth = width

    def handle(self, event):
        """
        This function is responsible for taking events and processing 
        the actions required. If the object != targeted, 
        the function will skip the events. But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. Window object is responsible for distributing the events.
        """
        lastHandledObj = None

        self.w_userData.events = event  # Keep the event always here
        if type(event) == int:
            if event == FR_EVENTS.FR_NO_EVENT:
                return 1  # we treat this event. Nothing to do

        # This is for the widgets label - Not the axes label - be aware.
        clickwdglblNode = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                            self.w_pick_radius, self.w_widgetlblSoNodes)

        # In this widget, we have 5 coin drawings that we need to capture event for them
        clickwdgdNode = []
        # 0 = Center cylinder (disk)
        # 1 = X-     Axis movement
        # 2 = Y-     Axis movement
        # 3 = 45°    Axis movement
        # 4 = 135°   Axis movement
        allObjects = None
        clickwdgdNode = [False, False, False, False, False]

        if(self.w_parent.objectMouseClick_Coin3d(
                self.w_parent.w_lastEventXYZ.pos,
                self.w_pick_radius, self.w_CenterSoSeparator) is not None):
            clickwdgdNode[0] = True
        elif(self.w_parent.objectMouseClick_Coin3d(
            self.w_parent.w_lastEventXYZ.pos,
                self.w_pick_radius, self.w_XsoSeparator) is not None):
            clickwdgdNode[1] = True
        elif(self.w_parent.objectMouseClick_Coin3d(
            self.w_parent.w_lastEventXYZ.pos,
                self.w_pick_radius, self.w_YsoSeparator) is not None):
            clickwdgdNode[2] = True
        elif(self.w_parent.objectMouseClick_Coin3d(
            self.w_parent.w_lastEventXYZ.pos,
                self.w_pick_radius, self.w_45soSeparator) is not None):
            clickwdgdNode[3] = True
        elif(self.w_parent.objectMouseClick_Coin3d(
            self.w_parent.w_lastEventXYZ.pos,
                self.w_pick_radius, self.w_135soSeparator) is not None):
            clickwdgdNode[4] = True

            # Execute callback_release when enter key pressed or E pressed
        if (self.w_parent.w_lastEvent == FR_EVENTS.FR_ENTER or
            self.w_parent.w_lastEvent == FR_EVENTS.FR_PAD_ENTER or
                self.w_parent.w_lastEvent == FR_EVENTS.FR_E):
            self.do_callback(self.w_userData)
            return 1

        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK:
            if (clickwdglblNode is not None):
                # Double click event.
                print("Double click detected")
                # if not self.has_focus():
                #    self.take_focus()
                self.do_lblcallback()
                return 1

        elif self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_RELEASE:
            self.currentSo = None
            if self.releaseDrag is True:
                self.releaseDrag is False
                #print("Mouse Release Occurred")
                # Release callback should be activated even if the wheel != under the mouse
                self.do_callback(self.w_userData)
                return 1
            # TODO FIXME: NOT CORRECT
            if (len(clickwdgdNode) > 0 or clickwdglblNode is not None):
                if not self.has_focus():
                    self.take_focus()
                # self.do_callbacks(100)
                return 1
            else:
                self.remove_focus()
                return 0
        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_DRAG:
            # This part will be active only once when for the first time user click on the coin drawing.
            # Later DRAG should be used
            if self.releaseDrag is False:
                self.releaseDrag = True
                self.take_focus()
            # These Object reacts only with dragging .. Clicking will not do anything useful
            # We don't accept more than one elements clicked at once
            if (self.currentSo is None):
                for counter in range(0, 5):
                    if clickwdgdNode[counter] is True:
                        self.currentSo = counter
                        self.do_callbacks(counter)
                        return 1
                return 0   # None of them was True.
            else:
                self.do_callbacks(self.currentSo)
                return 1

                # 0 The Center is clicked
                # 1 The Xaxis is clicked
                # 2 The Yaxis is clicked
                # 3 The 45Degree is clicked
                # 4 The 135Degree is clicked

        # Don't care events, return the event to other widgets
        return 0  # We couldn't use the event .. so return 0

    def draw(self):
        """
        Main draw function. It is responsible to create the node,
        and draw the wheel on the screen. It creates a node for 
        the wheel.
        """
        try:
            SETUPwheelTypeRotation = None
            SetupTextRotation = None
            lablVar = fr_widget.propertyValues()
            if (len(self.w_vector) < 1):
                raise ValueError('Must be one vector')

            usedColor = usedColor = self.w_selColor
            if self.is_active() and self.has_focus():
                usedColor = self.w_selColor
            elif self.is_active() and (self.has_focus() != 1):
                usedColor = self.w_color
            elif self.is_active() != 1:
                usedColor = self.w_inactiveColor
            if self.is_visible():

                if self.axisType == "XY":
                    # TOP         #OK Don't change
                    SETUPwheelTypeRotation = [0.0, 0.0, 0.0]
                    SetupTextRotation = [0.0, 0.0, 0.0]  # OK Don't change
                elif self.axisType == "XZ":
                    # FRONT       #OK Don't change
                    SETUPwheelTypeRotation = [90.0, 0.0, 0.0] 
                    SetupTextRotation = [90.0, 0.0, 0.0]  # OK Don't change
                elif self.axisType == "YZ":
                    # RIGHT       #OK Don't change
                    SETUPwheelTypeRotation = [270.0, 0.0, 0.0]
                    SetupTextRotation = [270.0, -180.0, 180.0]  # OK Don't change

                self.w_CenterSoSeparator = fr_wheel_draw.draw_AllParts( "Center",
                                                                       usedColor, SETUPwheelTypeRotation,
                                                                       self.w_Scale, 1)
                self.w_XsoSeparator = fr_wheel_draw.draw_AllParts( "Xaxis",
                                                                  usedColor, SETUPwheelTypeRotation,
                                                                   self.w_Scale, 1)  # RED
                self.w_YsoSeparator = fr_wheel_draw.draw_AllParts( "Yaxis",
                                                                  usedColor, SETUPwheelTypeRotation,
                                                                  self.w_Scale, 1)  # GREEN
                self.w_45soSeparator = fr_wheel_draw.draw_AllParts( "45axis", usedColor,
                                                                   SETUPwheelTypeRotation,
                                                                    self.w_Scale, 1)  # 45
                self.w_135soSeparator = fr_wheel_draw.draw_AllParts( "135axis", usedColor,
                                                                    SETUPwheelTypeRotation,
                                                                     self.w_Scale, 1)  # 135
                self.w_degreeSeparator = fr_wheel_draw.draw_Text_Wheel(usedColor,
                                                                       SetupTextRotation, 
                                                    [element * 2 for element in self.w_Scale], 1)  # White

                RootSoTransform = coin.SoTransform()
                rootTranslate=coin.SoTranslation()
                transR=coin.SbVec3f()
                transR.setValue(self.w_vector[0].x,self.w_vector[0].y,self.w_vector[0].z)
                rootTranslate.translation.setValue(transR)
                RootSO= coin.SoSeparator()
                preGroup = coin.SoSeparator()
                tR = coin.SbVec3f()
                tR.setValue(self.w_Rotation[0], self.w_Rotation[1], self.w_Rotation[2])
                RootSoTransform.rotation.setValue(tR, math.radians(self.w_wheelAngle))
                preRotation=coin.SoTransform()
                preRot=coin.SbVec3f()
                preRot.setValue(self.w_PRErotation[0],self.w_PRErotation[1],self.w_PRErotation[2])
                preRotation.rotation.setValue(preRot, math.radians(self.w_PRErotation[3]))
                
                preGroup.addChild(preRotation)
                preGroup.addChild(self.w_CenterSoSeparator)
                preGroup.addChild(self.w_XsoSeparator)
                preGroup.addChild(self.w_YsoSeparator)
                preGroup.addChild(self.w_45soSeparator)
                preGroup.addChild(self.w_135soSeparator)
                preGroup.addChild(self.w_degreeSeparator)
                
                RootSO.addChild(rootTranslate)
                RootSO.addChild(RootSoTransform)
                RootSO.addChild(preGroup)
                
                self.draw_label(usedColor)
                self.saveSoNodesToWidget(RootSO)
                # add SoSeparator to the switch
                # We can put them in a tuple but it is better not doing so
                self.addSoNodeToSoSwitch(self.w_widgetSoNodes)
                self.addSoNodeToSoSwitch(self.w_widgetlblSoNodes)

        except Exception as err:
            App.Console.PrintError("'draw Fr_wheel_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_label(self, usedColor):

        self.w_lbluserData.labelcolor = usedColor
        lbl = fr_label_draw.draw_newlabel(self.w_label, self.w_lbluserData)
        self.w_widgetlblSoNodes = lbl
        self.saveSoNodeslblToWidget(lbl)


    def move(self, newVecPos):
        """
        Move the object to the new location referenced by the 
        left-top corner of the object. Or the start of the wheel
        if it is an wheel.
        """
        self.resize(newVecPos[0])

    def show(self):
        self.w_visible = 1
        self.w_wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all children

    def redraw(self):
        """
        After the widgets damages, this function should be called.        
        """
        if self.is_visible():
            # Remove the SoSwitch from fr_coinwindow
            self.w_parent.removeSoSwitchFromSceneGraph(self.w_wdgsoSwitch)

            # Remove the node from the switch as a child
            self.removeSoNodeFromSoSwitch()

            # Remove the sceneNodes from the widget
            self.removeSoNodes()
            # Redraw label

            self.lblRedraw()
            self.draw()

    def lblRedraw(self):
        if(self.w_widgetlblSoNodes is not None):
            self.w_widgetlblSoNodes.removeAllChildren()

    def take_focus(self):
        """
        Set focus to the widget. Which should redraw it also.
        """
        if self.w_hasFocus == 1:
            return  # nothing to do here
        self.w_hasFocus = 1
        self.redraw()

    def activate(self):
        if self.w_active:
            return  # nothing to do
        self.w_active = 1
        self.redraw()

    def deactivate(self):
        """
        Deactivate the widget. which causes that no handle comes to the widget
        """
        if self.w_active == 0:
            return  # Nothing to do
        self.w_active = 0

    def ChangeScale(self, newScale=[1, 1, 1]):
        """[Scale the whole widget default is no scaling ]

        Args:
            newScale (list, optional): [New scale to apply to the widget]. Defaults to [1,1,1].
        """
        self.w_Scale = newScale

    def __del__(self):
        """
        Class Destructor. 
        This will remove the widget totally. 
        """
        self.hide()
        try:
            if self.w_parent is not None:
                # Parent should be the windows widget.
                self.w_parent.removeWidget(self)

            if self.w_parent is not None:
                self.w_parent.removeSoSwitchFromSceneGraph(self.w_wdgsoSwitch)

            self.removeSoNodeFromSoSwitch()
            self.removeSoNodes()
            self.removeSoSwitch()

        except Exception as err:
            App.Console.PrintError("'del Fr_wheel_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def hide(self):
        if self.w_visible == 0:
            return  # nothing to do
        self.w_visible = 0
        self.w_wdgsoSwitch.whichChild = coin.SO_SWITCH_NONE  # hide all children
        self.redraw()

    def remove_focus(self):
        """
        Remove the focus from the widget. 
        This happens by clicking anything 
        else than the widget itself
        """
        if self.w_hasFocus == 0:
            return  # nothing to do
        else:
            self.w_hasFocus = 0
            self.redraw()

    def resize(self, vectors: List[App.Vector]):  # Width, height, thickness
        """Resize the widget by using the new vectors"""
        self.w_vector = vectors
        self.redraw()

    def size(self, vectors: List[App.Vector]):
        """Resize the widget by using the new vectors"""
        self.resize(vectors)

    def label_move(self, newPos):
        pass

    def setRotationAngle(self, axis_angle):
        ''' 
        Set the rotation axis and the angle. This is for the whole widget.
        Axis is coin.SbVec3f((x,y,z)
        angle=float number
        '''
        self.w_PRErotation = axis_angle

    def do_callbacks(self, callbackType=-1):
        if (callbackType == 100):
            # run all
            self.cb_wheelRotate()
            self.do_callback(self.w_userData)
            self.w_wheel_cb_(self.w_userData)
            self.w_xAxis_cb_(self.w_userData)
            self.w_yAxis_cb_(self.w_userData)
            self.w_45Axis_cb_(self.w_userData)
            self.w_135Axis_cb_(self.w_userData)
        elif(callbackType == 10):
            # normal callback This represent the whole widget. Might not be used here TODO:Do we want this?
            self.do_callback(self.w_userData)
            # cylinder callback
        elif(callbackType == 0):
            self.cb_wheelRotate()
            self.w_wheel_cb_(self.w_userData)
            # Xaxis callback
        elif(callbackType == 1):
            self.w_xAxis_cb_(self.w_userData)
            # Yaxis callback
        elif(callbackType == 2):
            self.w_yAxis_cb_(self.w_userData)
            # Zaxis callback
        elif(callbackType == 3):
            self.w_45Axis_cb_(self.w_userData)
            # Zaxis callback
        elif(callbackType == 4):
            self.w_135Axis_cb_(self.w_userData)
 
    def cb_wheelRotate(self):
        """
        Internal callback function, runs when the wheel
        rotation event happens.
        self.w_wheelEnabled must be True
        """
        boundary = self.getWidgetsBoundary(self.w_CenterSoSeparator)
        center = self.getWidgetsCenter(self.w_CenterSoSeparator)
        try:

            self.endVector = App.Vector(self.w_parent.w_lastEventXYZ.Coin_x,
                                        self.w_parent.w_lastEventXYZ.Coin_y,
                                        self.w_parent.w_lastEventXYZ.Coin_z)
            if self.run_Once is False:
                self.run_Once = True
                self.startVector = self.endVector

            # Keep the old value only first time when drag start
                self.startVector = self.endVector
                if not self.has_focus():
                    self.take_focus()
            newValue = self.endVector

            print(center, "center")
            mx = my = mz = 0.0
            print("Now axis type =",self.axisType)
            
            if self.axisType == 'YZ':                                                      # Front
                # It means that we have changes in Z and X only
                # Z++  means   -Angel, Z--  means  +Angle    -->  When X is +                   ^
                # Z++  means   +Angel, Z--  means  -Angle    -->  When X is -                   v
                # X++  means   -Angel, x--  means  +Angel    -->  when Z is +
                # X++  means   +Angel, x--  means  -Angel    -->  when Z is -
                my = (newValue.y - center.y)
                mz = (newValue.z - center.z)
                if (mz == 0):
                    return  # Invalid
                self.w_wheelAngle = -faced.calculateMouseAngle(my, mz)

            elif self.axisType == 'XZ':                                                     # Right
                # It means that we have changes in Z and Y only
                # If the mouse moves at the >center in Z direction :
                # Z++  means   -Angel, Z--  means  +Angle    --> When Y is +                   ^
                # Z++  means   +Angel, Z--  means  -Angle    --> When Y is -                   v
                # Y++  means   +Angel, Y--  means  -Angel    -->  when Z is +
                # Y++  means   -Angel, Y--  means  +Angel    -->  when Z is -
                mx = (newValue.x - center.x)
                mz = (newValue.z - center.z)
                if (mz == 0):
                    return  # Invalid
                self.w_wheelAngle = faced.calculateMouseAngle(mx, mz)

            elif self.axisType == 'XY':
                # It means that we have changes in X and Y only
                # Y++  means   -Angel, Y--  means  +Angle    -->  When X is +                   ^
                # Y++  means   +Angel, Y--  means  -Angle    -->  When X is -                   v
                # x++  means   -Angel, X--  means  +Angel    -->  when Y is +
                # x++  means   +Angel, X--  means  -Angel    -->  when Y is -
                mx = (newValue.x - center.x)
                my = (newValue.y - center.y)
                if (my == 0):
                    return  # Invalid
                self.w_wheelAngle =- faced.calculateMouseAngle(mx, my)
            
            if (self.w_wheelAngle == 360):
                self.w_wheelAngle = 0
            if (self.oldAngle < 45 and self.oldAngle >= 0) and (self.w_wheelAngle > 270):
                self.rotationDirection = -1
                self.w_wheelAngle = self.w_wheelAngle-360

            elif(self.rotationDirection == -1
                and self.w_wheelAngle > 0
                and self.w_wheelAngle < 45
                and self.oldAngle < -270):
                self.rotationDirection = 1

            # # we don't accept an angel grater or smaller than 360 degrees
            # if(self.rotationDirection < 0):
            #     self.w_wheelAngle = self.w_wheelAngle-360

            # if(self.w_wheelAngle > 359):
            #     self.w_wheelAngle = 359
            # elif(self.w_wheelAngle < -359):
            #     self.w_wheelAngle = -359
            # if self.w_wheelAngle == -360:
            #     self.w_wheelAngle = 0
            self.oldAngle = self.w_wheelAngle
            print("w_wheelAngle=", self.w_wheelAngle)
            self.redraw()
                
        except Exception as err:
            App.Console.PrintError("'Wheel Rotate callback'. Failed "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)