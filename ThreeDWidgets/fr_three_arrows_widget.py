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
import pivy.coin as coin
from ThreeDWidgets import fr_widget
from ThreeDWidgets import constant
from ThreeDWidgets import fr_coin3d
from typing import List
import FACE_D as faced
from dataclasses import dataclass
from ThreeDWidgets.fr_draw import draw_2Darrow
from ThreeDWidgets import fr_label_draw
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from ThreeDWidgets.fr_draw1 import draw_RotationPad
import math
"""
Example how to use this widget.

# show the window and it's widgets.
import ThreeDWidgets.fr_coinwindow as wnn
import math
import fr_three_arrows_widget as w
mywin = wnn.Fr_CoinWindow()

vec=[]
vec.append(App.Vector(0,0,0))
vec.append(App.Vector(0,0,0))  #Dummy won't be used
arrows=w.Fr_ThreeArrows_Widget(vec,"Pad")
mywin.addWidget(arrows)
mywin.show()

"""
#TODO: FIXME: old implementation was to complex. we will uses one arrow widget 3 times. 

@dataclass
class userDataObject:

    def __init__(self):
        self.PadObj = None      # the Pad widget object
        self.events = None        # events - save handle events here
        self.callerObject = None  # Class/Tool uses the fr_Pad_widget
        self.padAxis = None
        self.Axis = None


# *******************************CALLBACKS - DEMO *****************************
def callback1(userData: userDataObject = None):
    """
        This function executes when the XAxis
        event callback.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy XAxis callback")


def callback2(userData: userDataObject = None):
    """
        This function executes when the YAxis
        event callback.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy YAxis callback")


def callback3(userData: userDataObject = None):
    """
        This function executes when the ZAxis
        event callback.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy ZAxis callback")


def callback4(userData: userDataObject = None):
    """
        This function executes when the PadX
        event callback.
        self.w_padEnabled must be True
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy PadX callback")


def callback5(userData: userDataObject = None):
    """
        This function executes when the PadY
        event callback.
        self.w_padEnabled must be True
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy PadY callback")

# *************************************************************


def callback6(userData: userDataObject = None):
    """
        This function executes when the PadZ
        event callback.
        self.w_padEnabled must be True
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy PadZ callback")

# *************************************************************


def callback(userData: userDataObject = None):
    """
        This function executes when lblCallbak 
        or general widget callback occurs
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy callback")

# *************************************************************


class Fr_ThreeArrows_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a one Degrees Pad
    This will be used later to create 3D Pad. 
    Or it can be used as a singel rotate/move widget
    """

    def __init__(self, vectors: List[App.Vector] = [],
                 label: str = "",
                 _lblColor=FR_COLOR.FR_WHITE,
                 _padColor=[FR_COLOR.FR_RED,
                              FR_COLOR.FR_GREEN,
                              FR_COLOR.FR_BLUE],
                 # User controlled rotation. This is only for the 3Pads
                 _Rotation=[0.0, 0.0, 0.0],
                 # Face position-direction controlled rotation at creation. Whole widget
                 _prerotation=[0.0, 0.0, 0.0, 0.0],
                 _scale=[3, 3, 3],
                 _type=1,
                 _opacity=0,
                 _distanceBetweenThem=[5, 5, 5]):
        super().__init__(vectors, label)

        self.w_widgetType = constant.FR_WidgetType.FR_THREE_PAD
        # General widget callback (mouse-button) function - External function
        self.w_callback_ = callback
        self.w_lbl_calback_ = callback              # Label callback
        self.w_KB_callback_ = callback              # Keyboard

        self.Opacity = _opacity
        self.DrawingType = _type
        # Use this to separate the arrows/lbl from the origin of the widget
        self.distanceBetweenThem = _distanceBetweenThem
        # Dummy callback X-Axis
        self.w_xAxis_cb_ = callback1
        # Dummy callback Y-Axis
        self.w_yAxis_cb_ = callback2
        # Dummy callback  Z-Axis
        self.w_zAxis_cb_ = callback3

        # Dummy callback          XPad
        self.w_padXAxis_cb_ = callback4
        # Dummy callback          YPad
        self.w_padYAxis_cb_ = callback5
        # Dummy callback          ZPad
        self.w_padZAxis_cb_ = callback6

        self.w_wdgsoSwitch = coin.SoSwitch()

        self.w_XsoSeparator = coin.SoSeparator()
        self.w_YsoSeparator = coin.SoSeparator()
        self.w_ZsoSeparator = coin.SoSeparator()

        self.w_padXsoSeparator = coin.SoSeparator()
        self.w_padYsoSeparator = coin.SoSeparator()
        self.w_padZsoSeparator = coin.SoSeparator()

        self.w_color = _lblColor  # not used for this widget
        self.w_PadAxis_color = _padColor
        self.w_selColor = [i * 1.2 for i in self.w_selColor]
        self.w_Scale = _scale
        self.w_inactiveColor = [i * 0.5 for i in self.w_selColor]

        self.rotationDirection = None

        self.w_userData = userDataObject()  # Keep info about the widget
        self.w_userData.PadObj = self

        self.releaseDrag = False  # Used to avoid running drag code while it is in drag mode
        # Use this to keep the selected so during push-drag, after release it should be none
        self.currentSo = None

        # This affect only the Widget label - nothing else
        self.w_lbluserData.linewidth = self.w_lineWidth
        self.w_lbluserData.vectors = self.w_vector
        # We must make it higher or it will intersect the object and won't be visible
        # TODO:Check if this works always?
        self.w_lbluserData.vectors[0].z = self.w_lbluserData.vectors[0].z + 2
        self.w_lbluserData.labelcolor = _lblColor

        # Use this to save rotation degree of the disk which is the whole widget angle.
        self.w_WidgetDiskRotation = 0.0
        self.w_Rotation = _Rotation
        self.w_PRErotation = _prerotation
        self.w_padEnabled = False

    def handle(self, event):
        """
        This function is responsbile of taking events and processing 
        the actions required. If the object != targeted, 
        the function will skip the events. But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. Window object is responsible for distributing the events.
        """

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
        if self.w_padEnabled:
            if (fr_coin3d.objectMouseClick_Coin3d(
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
                # Release callback should be activated even if the Pad != under the mouse
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
            # We don't accept more than one element- clicking at the time
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
        and draw the Pad on the screen. It creates a node for each 
        element and for each Pad.
        """
        try:

            if (len(self.w_vector) < 1):
                raise ValueError('Must be a vector')

            usedColor = self.w_color
            if self.is_active() and self.has_focus():
                usedColor = self.w_selColor
            elif self.is_active() and (self.has_focus() != 1):
                pass  # usedColor = self.w_color  we did that already ..just for reference
            elif self.is_active() != 1:
                usedColor = self.w_inactiveColor

            if self.is_visible():

                self.w_XsoSeparator = draw_2Darrow(App.Vector(self.w_vector[0].x +
                                                              self.distanceBetweenThem[0],
                                                              self.w_vector[0].y,
                                                              self.w_vector[0].z),
                                                   # default FR_COLOR.FR_RED
                                                   self.w_PadAxis_color[0], self.w_Scale,
                                                   self.DrawingType, self.Opacity,
                                                   [0.0, 90.0, 0.0])    #pre-Rotation # RED
                self.w_YsoSeparator = draw_2Darrow(App.Vector(self.w_vector[0].x,
                                                              self.w_vector[0].y +
                                                              self.distanceBetweenThem[1],
                                                              self.w_vector[0].z),
                                                   # default FR_COLOR.FR_GREEN
                                                   self.w_PadAxis_color[1], self.w_Scale,
                                                   self.DrawingType, self.Opacity,
                                                   [0.0, 90.0, 90.0])  #pre-Rotation GREEN
                self.w_ZsoSeparator = draw_2Darrow(App.Vector(self.w_vector[0].x,
                                                              self.w_vector[0].y,
                                                              self.w_vector[0].z +
                                                              self.distanceBetweenThem[2]),
                                                   # default FR_COLOR.FR_BLUE
                                                   self.w_PadAxis_color[2], self.w_Scale,
                                                   self.DrawingType, self.Opacity,
                                                   [0.0, 0.0, 0.0])  #pre-Rotation BLUE
                if self.w_padEnabled:
                    # Hint: def draw_RotationPad(p1=App.Vector(0.0, 0.0, 0.0), color=FR_COLOR.FR_GOLD,
                    # scale=(1, 1, 1), opacity=0, _rotation=[0.0, 0.0, 0.0]):
                    self.w_padXsoSeparator = draw_RotationPad(self.w_vector[0], self.w_PadAxis_color[0], self.w_Scale,
                                                              self.Opacity, [0.0, 0.0, 90.0])  # RED
                    self.w_padYsoSeparator = draw_RotationPad(self.w_vector[0], self.w_PadAxis_color[1], self.w_Scale,
                                                              self.Opacity, [0.0, 0.0, 0.0])  # GREEN
                    self.w_padZsoSeparator = draw_RotationPad(self.w_vector[0], self.w_PadAxis_color[2], self.w_Scale,
                                                              self.Opacity, [90.0, 0.0, 0.0])  # BLUE

                CollectThemAllRot = coin.SoTransform()
                CollectThemAll = coin.SoSeparator()
                tR = coin.SbVec3f()
                tR.setValue(
                    self.w_PRErotation[0], self.w_PRErotation[1], self.w_PRErotation[2])
                CollectThemAllRot.rotation.setValue(
                    tR, math.radians(self.w_PRErotation[3]))

                CollectThemAll.addChild(CollectThemAllRot)
                CollectThemAll.addChild(self.w_XsoSeparator)
                CollectThemAll.addChild(self.w_YsoSeparator)
                CollectThemAll.addChild(self.w_ZsoSeparator)

                if self.w_padEnabled:
                    CollectThemAll.addChild(self.w_padXsoSeparator)
                    CollectThemAll.addChild(self.w_padYsoSeparator)
                    CollectThemAll.addChild(self.w_padZsoSeparator)

                self.saveSoNodeslblToWidget(self.draw_label())
                self.saveSoNodesToWidget(CollectThemAll)
                # add SoSeparator to the switch
                # We can put them in a tuple but it is better not doing so
                self.addSoNodeToSoSwitch(self.w_widgetSoNodes)
                self.addSoNodeToSoSwitch(self.w_widgetlblSoNodes)

        except Exception as err:
            App.Console.PrintError("'draw Fr_Pad_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def redraw(self):
        """
        When the widget is damaged, use this function to redraw it.        
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

    def draw_label(self):
        """[Draw 3D text in the scenegraph]

        Returns:
            [type]: [Use w_lbluserData variable to setup the label shape, size, font ..etc

            w_lebluserData is of type  propertyValues

            @dataclass
            class propertyValues:
                '''
                Property-holder class for drawing labels
                '''
                __slots__ = ['vectors', 'linewidth', 'fontName', 'fontsize',
                            'labelcolor', 'alignment', 'rotation', 'rotationAxis',
                            'scale']
                vectors: VECTOR  # List[App.Vector] two vectors must be provided
                linewidth: int
                fontName: str
                fontsize: int
                labelcolor: tuple
                alignment: int  # This will not be used .. not good
                rotation: tuple    # three angels in degree
                rotationAxis: VECTOR
                scale: tuple  # Three float numbers for scaling
            ]
        """

        lbl = fr_label_draw.draw_newlabel(self.w_label, self.w_lbluserData)
        self.w_widgetlblSoNodes = lbl
        return lbl

    def lblRedraw(self):
        """[Redraw the label]
        """
        if(self.w_widgetlblSoNodes is not None):
            self.w_widgetlblSoNodes.removeAllChildren()
        self.draw_label()

    def move(self, newVecPos=App.Vector(0, 0, 0)):
        """[Move the widget to a new location referenced by the 
            left-top corner of the object. Or the start of the Pad
            if it is an Pad.]

        Args:
            newVecPos ([App.Vector], optional): [Move the label to a new position]. Defaults to App.Vector(0,0,0).
        """
        self.w_lbluserData.vector = [newVecPos, ]

    def show(self):
        """[This function will show the widget. But it doesn't draw it. ]
        """
        self.w_visible = 1
        self.w_wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all children

    def take_focus(self):
        """
        Set focus to the widget. Which should redraw it also.
        """
        if self.w_hasFocus == 1:
            return  # nothing to do here
        self.w_hasFocus = 1
        self.redraw()

    def activate(self):
        """[Activate the widget so it can take events]

        """
        if self.w_active:
            return  # nothing to do
        self.w_active = 1
        self.redraw()

    def deactivate(self):
        """
        Deactivate the widget. which causes that no handle comes to the widget
        """
        self.w_active = 0

    def ChangeScale(self, newScale=[1, 1, 1]):
        """[Scale the whole widget default is no scaling ]

        Args:
            newScale (list, optional): [New scale to apply to the widget]. Defaults to [1.0,1.0,1.0].
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
            App.Console.PrintError("'del Fr_Pad_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def hide(self):
        """[Hide the widget - but the widget is not destroyed]

        Returns:
            [type]: [description]
        """
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

    def resize(self, _scale: tuple = [1.0, 1.0, 1.0]):
        """Resize the widget by using the new vectors"""
        self.w_Scale = _scale
        self.redraw()

    def size(self, _scale: tuple = [1.0, 1.0, 1.0]):
        """[Scale the widget for the three directions]

        Args:
            _scale (tuple, Three float values): [Scale the widget using three float values for x,y,z axis]. 
            Defaults to [1.0, 1.0, 1.0].
        """
        self.resize(_scale)

    def label(self, newlabel):
        self.w_label = newlabel

    # Keep in mind you must run lblRedraw
    def label_font(self, name="sans"):
        """[Change Label Font]

        Args:
            name (str, optional): [Change label font]. Defaults to "sans".
        """
        self.w_lbluserData.fontName = name

    # Keep in mind you must run lblRedraw
    def label_scale(self, newsize: tuple = [1.0, 1.0, 1.0]):
        """[Scale the font using three float values. This is not the font size.
        You must redraw the label to get this scaling done.
        ]

        Args:
            newsize (int, optional): [Change font label ]. Defaults to 1.
        """
        self.w_lbluserData.scale = newsize

    # Keep in mind you must run lblRedraw
    def label_fontsize(self, newsize=1):
        """[Change label font size ]

        Args:
            newsize (int, optional): [Change fontsize of the label ]. Defaults to 1.
        """
        self.w_lbluserData.fontsize = newsize

    # Must be App.Vector
    def label_move(self, newPos=App.Vector(0.0, 0.0, 0.0)):
        """[Move location of the label]

        Args:
            newPos ([App.Vector], optional): [Change placement of the label]. Defaults to App.Vector(0.0, 0.0, 0.0).
        """
        self.w_lbluserData.vectors = [newPos, ]

    def setRotationAngle(self, axis_angle):
        ''' 
        Set the rotation axis and the angle. This is for the whole widget.
        Axis is coin.SbVec3f((x,y,z)
        angle=float number
        '''
        self.w_PRErotation = axis_angle

    def calculateWidgetDiskRotationAfterDrag(self, v1, v2):
        self.w_WidgetDiskRotation = math.degrees(v1.getAngle(v2))

    def enablePAD(self):
        """[Enable X,Y & Z rotation pad. You need to redraw the widget]
        """
        self.w_padEnabled = True

    def setDistanceBetweenThem(self, newvalue):
        """[Change distance between the arrows to the origin of the widget. ]

        Args:
            newvalue ([float]): [new distance in mm]
        """
        self.distanceBetweenThem = newvalue

    def disablePAD(self):
        """[Disable X,Y & Z rotation pad. You need to redraw the widget]
        """
        self.w_padEnabled = False

    def do_callbacks(self, callbackType=-1):
        """[summarize the call of the callbacks]

        Args:
            callbackType (int, optional): 
            [Call specific callback depending on the callback type]. Defaults to -1.
            userData will hold the direction dependently.
            Axis   : holds the axis name ('X','Y' or 'Z') as letter
            padAxis: holds the pads (wheel) rotation axis ('X','Y' or 'Z') 
            as letters.  
        """
        if (callbackType == 100):
            # run all
            self.do_callback()
            self.w_xAxis_cb_(self.w_userData)
            self.w_yAxis_cb_(self.w_userData)
            self.w_zAxis_cb_(self.w_userData)
            if self.w_padEnabled:
                self.w_padXAxis_cb_(self.w_userData)
                self.w_padYAxis_cb_(self.w_userData)
                self.w_padZAxis_cb_(self.w_userData)
        elif(callbackType == 10):
            # normal callback This represent the whole widget.
            # Might not be used here TODO:Do we want this?
            self.do_callback()

        elif(callbackType == 0):
            self.w_userData.Axis = "X"
            self.w_userData.padAxis = None
            self.w_xAxis_cb_(self.w_userData)

        elif(callbackType == 1):
            self.w_userData.Axis = "Y"
            self.w_userData.padAxis = None
            self.w_yAxis_cb_(self.w_userData)

        elif(callbackType == 2):
            self.w_userData.Axis = "Z"
            self.w_userData.padAxis = None
            self.w_zAxis_cb_(self.w_userData)
        if self.w_padEnabled:
            if(callbackType == 3):
                self.w_userData.padAxis = "X"
                self.w_userData.Axis = None
                self.w_padXAxis_cb_(self.w_userData)

            elif(callbackType == 4):
                self.w_userData.padAxis = "Y"
                self.w_userData.Axis = None
                self.w_padYAxis_cb_(self.w_userData)

            elif(callbackType == 5):
                self.w_userData.padAxis = "Z"
                self.w_userData.Axis = None
                self.w_padZAxis_cb_(self.w_userData)