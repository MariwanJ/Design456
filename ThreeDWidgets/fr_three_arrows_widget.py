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
import ThreeDWidgets
import pivy.coin as coin
from ThreeDWidgets import fr_widget
from ThreeDWidgets import constant
from ThreeDWidgets import fr_coin3d
from typing import List
from ThreeDWidgets import fr_label_draw
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
import FACE_D as faced
from dataclasses import dataclass
from fr_draw import draw_2Darrow
import math
"""
Example how to use this widget. 

# show the window and it's widgets. 
import ThreeDWidgets.fr_coinwindow as wnn
import math
import fr_three_arrows_widget as w 
mywin = wnn.Fr_CoinWindow()

rotation=0
color=(.8,0.8,1)
vec=[]
vec.append(App.Vector(0,0,0))
vec.append(App.Vector(0,5,5))

rotation=[0.0, 0.0, 0.0, 0.0]
arrows=w.Fr_ThreeArrows_Widget(vec,"Wheel")
mywin.addWidget(arrows)
mywin.show()


"""


@dataclass
class userDataObject:

    def __init__(self):
        self.wheelObj = None      # the wheel widget object
        self.events = None        # events - save handle events here
        self.callerObject = None  # Class/Tool uses the fr_wheel_widget


# *******************************CALLBACKS DEMO *********************************************
def callback(userData: userDataObject = None):
    """
        This function executes when the Widget as whole got an event
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy FR_WHELL_WIDGET General callback")


def callback1(userData: userDataObject = None):
    """
        This function executes when the Center has an event 
        event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy Center-wheel-widget callback1")


def callback2(userData: userDataObject = None):
    """
        This function executes when the XAxis 
        event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy XAxis callback")


def callback3(userData: userDataObject = None):
    """
        This function executes when the YAxis 
        event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy YAxis callback")


def callback4(userData: userDataObject = None):
    """
        This function executes when the 45Axis 
        event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy 45Axis callback")


def callback5(userData: userDataObject = None):
    """
        This function executes when the 135Axis 
        event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy 135Axis callback")

# *************************************************************


def callback6(userData: userDataObject = None):
    """
        This function executes when the 135Axis 
        event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy 135Axis callback")

# *************************************************************


class Fr_ThreeArrows_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a one Degrees wheel
    This will be used later to create 3D wheel. 
    Or it can be used as a singel rotate/move widget
    """

    def __init__(self, vectors: List[App.Vector] = [],
                 label: str = "",
                 _lblColor=FR_COLOR.FR_BLACK,
                 arrColor=[FR_COLOR.FR_RED,
                           FR_COLOR.FR_GREEN, FR_COLOR.FR_BLUE, ],
                 _Rotation=[0.0, 0.0, 0.0],
                 _prerotation=[0.0, 0.0, 0.0],
                 _scale=[1, 1, 1], _type=1,
                 _opacity = 0):

        super().__init__(vectors, label)

        self.w_widgetType = constant.FR_WidgetType.FR_WHEEL
        # General widget callback (mouse-button) function - External function
        self.w_callback_ = callback
        self.w_lbl_calback_ = callback              # Label callback
        self.w_KB_callback_ = callback              # Keyboard
        self.w_move_callback_ = callback            # Mouse movement callback
        self.Opacity = _opacity
        self.DrawingType = _type
        # Dummy callback
        self.w_xAxis_cb_ = callback1
        # Dummy callback
        self.w_yAxis_cb_ = callback2
        # Dummy callback
        self.w_zAxis_cb_ = callback3

        # Dummy callback          XWheel
        self.w_wheelXAxis_cb_ = callback4
        # Dummy callback          YWheel
        self.w_wheelYAxis_cb_ = callback5
        # Dummy callback          ZWheel
        self.w_wheelZAxis_cb_ = callback6

        self.w_wdgsoSwitch = coin.SoSwitch()

        self.w_XsoSeparator = coin.SoSeparator()
        self.w_YsoSeparator = coin.SoSeparator()
        self.w_ZsoSeparator = coin.SoSeparator()

        self.w_padXsoSeparator = coin.SoSeparator()
        self.w_padYsoSeparator = coin.SoSeparator()
        self.w_padZsoSeparator = coin.SoSeparator()

        self.w_color = arrColor
        self.w_selColor = [i * 1.2 for i in self.w_selColor]
        self.w_Scale = _scale
        self.w_inactiveColor = [i * 0.5 for i in self.w_selColor]

        self.w_Xrotation = [0, 0, 0]
        self.w_Yrotation = [0, 0, 0]
        self.w_Zrotation = [0, 0, 0]

        self.w_userData = userDataObject()  # Keep info about the widget
        self.w_userData.wheelObj = self

        self.releaseDrag = False  # Used to avoid running drag code while it is in drag mode
        # Use this to keep the selected so during push-drag, after release it should be none
        self.currentSo = None

        # This affect only the Widget label - nothing else
        self.w_lbluserData.linewidth = self.w_lineWidth

        # Use this to save rotation degree of the disk which is the whole widget angle.
        self.w_WidgetDiskRotation = 0.0
        self.w_Rotation = _Rotation
        self.w_PRErotation = _prerotation

    def handle(self, event):
        """
        This function is responsbile of taking events and processing 
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
                return 1  # we treat this event. Nonthing to do

        # This is for the widgets label - Not the axises label - be aware.
        clickwdglblNode = fr_coin3d.objectMouseClick_Coin3d(self.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                                                            self.w_pick_radius, self.w_widgetlblSoNodes)

        # In this widget, we have 5 coin drawings that we need to capture event for them
        clickwdgdNode = []
        # 0 = X-     Axis movement
        # 1 = Y-     Axis movement
        # 2 = Z-     Axis movement

        # 3 = X-     PAD Rotation
        # 4 = Y-     PAD Rotation
        # 5 = Z-     PAD Rotation

        allObjects = None
        clickwdgdNode = [False, False, False, False, False, False]

        if(fr_coin3d.objectMouseClick_Coin3d(
            self.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                self.w_pick_radius, self.w_XsoSeparator) is not None):
            clickwdgdNode[0] = True
        elif(fr_coin3d.objectMouseClick_Coin3d(
            self.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                self.w_pick_radius, self.w_YsoSeparator) is not None):
            clickwdgdNode[1] = True
        elif(fr_coin3d.objectMouseClick_Coin3d(
            self.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                self.w_pick_radius, self.w_ZsoSeparator) is not None):
            clickwdgdNode[2] = True
        elif(fr_coin3d.objectMouseClick_Coin3d(
            self.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                self.w_pick_radius, self.w_padXsoSeparator) is not None):
            clickwdgdNode[3] = True
        elif (fr_coin3d.objectMouseClick_Coin3d(
                self.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                self.w_pick_radius, self.w_padYsoSeparator) is not None):
            clickwdgdNode[4] = True
        elif(fr_coin3d.objectMouseClick_Coin3d(
                self.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                self.w_pick_radius, self.w_padZsoSeparator) is not None):
            clickwdgdNode[5] = True

        # Execute callback_relese when enter key pressed or E pressed
        if (self.w_parent.link_to_root_handle.w_lastEvent == FR_EVENTS.FR_ENTER or
            self.w_parent.link_to_root_handle.w_lastEvent == FR_EVENTS.FR_PAD_ENTER or
                self.w_parent.link_to_root_handle.w_lastEvent == FR_EVENTS.FR_E):
            self.do_callback()
            return 1

        if self.w_parent.link_to_root_handle.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK:
            if (clickwdglblNode is not None):
                # Double click event.
                print("Double click detected")
                # if not self.has_focus():
                #    self.take_focus()
                self.do_lblcallback()
                return 1

        elif self.w_parent.link_to_root_handle.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_RELEASE:
            self.currentSo = None
            if self.releaseDrag is True:
                self.releaseDrag is False
                # Release callback should be activated even if the wheel != under the mouse
                self.do_callback()
                return 1

            if (len(clickwdgdNode) > 0 or clickwdglblNode is not None):
                if not self.has_focus():
                    self.take_focus()
                return 1
            else:
                self.remove_focus()
                return 0

        if self.w_parent.link_to_root_handle.w_lastEvent == FR_EVENTS.FR_MOUSE_DRAG:
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

        # Don't care events, return the event to other widgets
        return 0  # We couldn't use the event .. so return 0

    def draw(self):
        """
        Main draw function. It is responsible to create the node,
        and draw the wheel on the screen. It creates a node for 
        the wheel.
        """
        try:
            lablVar = fr_widget.propertyValues()
            if (len(self.w_vector) < 1):
                raise ValueError('Must be one vector')

            usedColor = self.w_color
            if self.is_active() and self.has_focus():
                usedColor = self.w_selColor
            elif self.is_active() and (self.has_focus() != 1):
                pass  # usedColor = self.w_color  we did that alread ..just for reference
            elif self.is_active() != 1:
                usedColor = self.w_inactiveColor

            if self.is_visible():
                allDraw = []
                #(p1=App.Vector(0,0,0),color=FR_COLOR.FR_GOLD,scale=[0.5,0.5,0.5],type=0,opacity=0, _rotation=[0.0, 0.0, 0.0]):
                self.w_XsoSeparator = draw_2Darrow(self.w_vector[0],
                                                                 FR_COLOR.FR_RED, self.w_Scale,
                                                                 self.Opacity, self.DrawingType,
                                                                 [0.0, 90.0, 0.0])  # RED
                self.w_YsoSeparator = draw_2Darrow(self.w_vector[0],
                                                                 FR_COLOR.FR_GREEN, self.w_Scale,
                                                                 self.Opacity, self.DrawingType,
                                                                 [0.0, 90.0, 90.0])  # GREEN
                self.w_ZsoSeparator = draw_2Darrow(self.w_vector[0],
                                                                 FR_COLOR.FR_BLUE, self.w_Scale,
                                                                 self.Opacity, self.DrawingType,
                                                                 [0.0, 0.0, 90.0])  # BLUE

                allDraw.append(self.w_XsoSeparator)
                allDraw.append(self.w_YsoSeparator)
                allDraw.append(self.w_ZsoSeparator)
                allDraw.append(self.w_padXsoSeparator)
                allDraw.append(self.w_padYsoSeparator)
                allDraw.append(self.w_padZsoSeparator)

#                CollectThemAllRot = coin.SoTransform()
                CollectThemAll = coin.SoSeparator()
                #tR = coin.SbVec3f()
                #tR.setValue(
                #    self.w_Rotation[0], self.w_Rotation[1], self.w_Rotation[2])
#                CollectThemAllRot.rotation.setValue(
#                    tR, math.radians(self.w_Rotation[3]))

#                CollectThemAll.addChild(CollectThemAllRot)
                CollectThemAll.addChild(self.w_XsoSeparator)
                CollectThemAll.addChild(self.w_YsoSeparator)
                CollectThemAll.addChild(self.w_ZsoSeparator)

                CollectThemAll.addChild(self.w_padXsoSeparator)
                CollectThemAll.addChild(self.w_padYsoSeparator)
                CollectThemAll.addChild(self.w_padZsoSeparator)

                self.saveSoNodeslblToWidget(self.draw_label(usedColor))
                self.saveSoNodesToWidget(CollectThemAll)
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
        return lbl

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

    def calculateWidgetDiskRotationAfterDrag(self, v1, v2):
        self.w_WidgetDiskRotation = faced.calculateAngle(v1, v2)

    def do_callbacks(self, callbackType=-1):
        if (callbackType == 100):
            # run all
            self.do_callback()
            self.w_xAxis_cb_(self.w_userData)
            self.w_yAxis_cb_(self.w_userData)
            self.w_zAxis_cb_(self.w_userData)
            
            self.w_wheelXAxis_cb_(self.w_userData)
            self.w_wheelYAxis_cb_(self.w_userData)
            self.w_wheelZAxis_cb_(self.w_userData)
        elif(callbackType == 10):
            # normal callback This represent the whole widget. Might not be used here TODO:Do we want this?
            self.do_callback()

        elif(callbackType == 0):
            self.w_xAxis_cb_(self.w_userData)
        
        elif(callbackType == 1):
            self.w_yAxis_cb_(self.w_userData)

        elif(callbackType == 2):
            self.w_zAxis_cb_(self.w_userData)

        elif(callbackType == 3):
            self.w_wheelXAxis_cb_(self.w_userData)

        elif(callbackType == 4):
            self.w_wheelYAxis_cb_(self.w_userData)

        elif(callbackType == 5):
            self.w_wheelZAxis_cb_(self.w_userData)
