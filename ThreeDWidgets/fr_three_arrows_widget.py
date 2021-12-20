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
import ThreeDWidgets.fr_one_arrow_widget as wd
import ThreeDWidgets.fr_coinwindow as wnn
from ThreeDWidgets.constant import FR_COLOR

class test:
	global runOunce
	def __init__(self):
		self.runOunce = None

	def callback_move(self,userData : wd.userDataObject = None):
     
	     PadObj = userData.PadObj  # Arrow object
	     click=App.Vector(PadObj.w_parent.w_lastEventXYZ.Coin_x,
                                            PadObj.w_parent.w_lastEventXYZ.Coin_y,
                                            PadObj.w_parent.w_lastEventXYZ.Coin_z)
	     if self.runOunce == None:
	           self.runOunce = click.sub(PadObj.w_vector[0])

	     PadObj.w_vector[0]=click.sub(self.runOunce)
	     
	     PadObj.redraw()

	     print(self.runOunce,"self.runOunce")

	def runme(self):
		mywin = wnn.Fr_CoinWindow()
		vectors=[App.Vector(0,0,0), App.Vector(0,0,0)] 
		rot=[0,0,0,0]
		root=wd.Fr_OneArrow_Widget(vectors, "X-Axis")
		root.w_move_callback_=self.callback_move
		root.enableDisc()
		mywin.addWidget(root)
		mywin.show()

a=test()
a.runme()
a=test()

OR another example :

import ThreeDWidgets.fr_one_arrow_widget as wd
import ThreeDWidgets.fr_coinwindow as wnn
from ThreeDWidgets.constant import FR_COLOR



mywin = wnn.Fr_CoinWindow()
v1=[App.Vector(0,0,0), App.Vector(0,0,0)] 
v2=[App.Vector(20,0,0), App.Vector(0,0,0)] 
r1=wd.Fr_OneArrow_Widget(v1, "X-Axis")
r1.enableDisc()
r2=wd.Fr_OneArrow_Widget(v2, "y-Axis")
r1.enableDisc()
r2.enableDisc()

mywin.addWidget(r1)
mywin.addWidget(r2)
mywin.show()

"""


@dataclass
class userDataObject:

    def __init__(self):
        self.events = None        # events - save handle events here
        self.callerObject = None  # Class/Tool uses the fr_disc_widget
        self.Axis = []
        self.discObj = []      # the disc widget object

# *******************************CALLBACKS - DEMO *****************************
def xAxis_cb(userData: userDataObject = None):
    """
        This function executes when the XAxis
        event callback.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy XAxis -3Arrows callback")


def xDisc_cb(userData: userDataObject = None):
    """
        This function executes when the rotary disc
        angel changed event callback.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy Xangle changed callback", userData.discObj.w_discAngle)


def yAxis_cb(userData: userDataObject = None):
    """
        This function executes when the XAxis
        event callback.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy YAxis -3Arrows callback")


def yDisc_cb(userData: userDataObject = None):
    """
        This function executes when the rotary disc
        angel changed event callback.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy Yangle changed callback", userData.discObj.w_discAngle)


def zAxis_cb(userData: userDataObject = None):
    """
        This function executes when the XAxis
        event callback.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy ZAxis -3Arrows callback")


def zDisc_cb(userData: userDataObject = None):
    """
        This function executes when the rotary disc
        angel changed event callback.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy Zangle changed callback", userData.discObj.w_discAngle)

# ******************************

# Whole widget callback  - Might not be used
# *************************************************************


def callback(userData: userDataObject = None):
    """
        This function executes when lblCallbak (double click callback)
        or general widget callback occurs
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy callback")

# *************************************************************


def callback(userData: userDataObject = None):
    """
        This function executes when lblCallbak 
        or general widget callback occurs
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy callback")

# *************************************************************


class Fr_ThreeArrow_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a one Degrees disc
    This will be used later to create 3D disc. 
    Or it can be used as a singel rotate/move widget
    """

    def __init__(self, vectors: List[App.Vector] = [],
                 label: str = [[]],
                 _lblColor=FR_COLOR.FR_WHITE,
                 _axisColor=[FR_COLOR.FR_RED,
                             FR_COLOR.FR_GREEN,
                             FR_COLOR.FR_BLUE],
                 # Whole widget rotation
                 _rotation: List[float] = [0.0, 0.0, 0.0, 0.0],
                 # Pre-rotation
                 _setupRotation: List[float] =[0.0, 0.0, 0.0],
                 _scale: List[float] = [3.0, 3.0, 3.0],
                 _type: int = 1,
                 _opacity: float = 0.0,
                 _distanceBetweenThem: float = 5.0):
        super().__init__(vectors, label)

        self.w_lbluserData = fr_widget.propertyValues()
        self.w_widgetType = constant.FR_WidgetType.FR_THREE_DISC
        # General widget callback (mouse-button) function - External function
        self.w_callback_ = callback
        self.w_lbl_calback_ = callback              # Label callback
        self.w_KB_callback_ = callback              # Keyboard

        # Dummy callback Axis
        self.w_ArrowXaxis_cb_ = xAxis_cb
        self.w_ArrowYaxis_cb_ = yAxis_cb
        self.w_ArrowZaxis_cb_ = zAxis_cb

        # Dummy callback          disc
        self.w_rotaryX_cb_ = xDisc_cb
        self.w_rotaryY_cb_ = yDisc_cb
        self.w_rotaryZ_cb_ = zDisc_cb

        self.Opacity = _opacity
        self.DrawingType = _type
        # Use this to separate the arrows/lbl from the origin of the widget
        self.distanceBetweenThem = _distanceBetweenThem

        self.w_wdgsoSwitch = coin.SoSwitch()
        
        self.w_XarrowSeparator = None
        self.w_XdiscSeparator = None
        
        self.w_YarrowSeparator = None
        self.w_YdiscSeparator = None
        
        self.w_ZarrowSeparator = None
        self.w_ZdiscSeparator = None

        self.w_color = _axisColor
        self.w_rotaryDisc_color = _axisColor
        self.w_selColor = [i * 1.2 for i in self.w_color]
        self.w_Scale = _scale
        self.w_inactiveColor = [i * 0.5 for i in self.w_selColor]

        self.w_userData = userDataObject()  # Keep info about the widget
        self.w_userData.discObj = self
        self.w_discAngle = [0.0, 0.0, 0.0]      # Only disc rotation.
        self.oldAngle = [0.0, 0.0, 0.0]
        self.rotationDirection = [1,1,1]   # +1 CCW , -1 ACCW

        # This affect only the Widget label - nothing else
        self.w_lbluserData.linewidth = self.w_lineWidth
        self.w_lbluserData.vectors = self.w_vector

        # We must make it higher or it will intersect the object and won't be visible
        # TODO:Check if this works always?
        self.w_lbluserData.vectors[0].x = self.w_lbluserData.vectors[0].x + \
            self.distanceBetweenThem
        self.w_lbluserData.vectors[0].y = self.w_lbluserData.vectors[0].y + \
            self.distanceBetweenThem
        self.w_lbluserData.vectors[0].z = self.w_lbluserData.vectors[0].z + \
            self.distanceBetweenThem
        self.w_lbluserData.labelcolor = _lblColor

        # Use this to save rotation degree of the disk which is the whole widget angle.
        self.w_WidgetDiskRotation = [0.0, 0.0, 0.0]

        self.w_rotation = _rotation       # Whole object Rotation

        self.w_discEnabled = [False,False,False]
        
        # Used to avoid running drag code while it is in drag mode
        self.XreleaseDragAxis = -1
        self.YreleaseDragAxis = -1
        self.ZreleaseDragAxis = -1
        
        # -1 no click, 0 mouse clicked, 1 mouse dragging
        # Used to avoid running drag code while it is in drag mode
        self.XreleaseDragDisc = -1
        self.YreleaseDragDisc = -1
        self.ZreleaseDragDisc = -1
        
        # -1 no click, 0 mouse clicked, 1 mouse dragging
        self.Xrun_Once = False
        self.Yrun_Once = False
        self.Yrun_Once = False
        
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
        clickwdglblNode = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                                self.w_pick_radius, self.w_widgetlblSoNodes)

        #X Axis 
        XclickwdgdNode = [False, False]
        YclickwdgdNode = [False, False]
        ZclickwdgdNode = [False, False]
        
        # In this widget, we have 2 coin drawings that we need to capture event for them
        
        #   ------------- X Axis  ------------- 
        if(self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                 self.w_pick_radius, self.w_XarrowsSeparator) is not None):
            XclickwdgdNode[0] = True

        if self.w_discEnabled[0]:
            if (self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                      self.w_pick_radius, self.w_XdiscSeparator) is not None):
                XclickwdgdNode[1] = True

        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK:
            if (clickwdglblNode is not None):
                # Double click event.
                print("Double click detected")
                # if not self.has_focus():
                #    self.take_focus()
                self.do_lblcallback()
                return 1

        elif self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_RELEASE:
            # disc's part
            if XclickwdgdNode[1] is True:
                # When the discs rotates, we don't accept
                # the arrow dragging. Disk rotation has priority
                if self.XreleaseDragDisc == 1 or self.XreleaseDragDisc == 0:
                    self.XreleaseDragDisc = -1
                    # Release callback should be activated
                    self.do_callbacks(0)
                    return 1
                # Axis's part
            elif XclickwdgdNode[0] is True:
                if self.XreleaseDragAxis == 1 or self.XreleaseDragAxis == 0:
                    self.XreleaseDragAxis = -1
                    self.do_callback(1)
                    return 1
            else:  # None of them -- remove the focus
                self.remove_focus()
                return 0
        # Mouse first click and then mouse with movement is here
        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_DRAG:
            # X-DISC
            if((XclickwdgdNode[1] is True) and (self.XreleaseDragDisc == -1)):
                # This part will be active only once when for the first time user click on the coin drawing.
                # Later DRAG should be used
                self.XreleaseDragDisc = 0
                self.XreleaseDragAxis = -1
                self.take_focus()
                return 1
            # X-DISC
            elif ((XclickwdgdNode[1] is True) and (self.XreleaseDragDisc == 0)):
                self.XreleaseDragDisc = 1  # Rotation will continue it will be a drag always
                self.XreleaseDragAxis = -1
                self.take_focus()
                self.cb_XdiscRotate()
                self.do_callbacks(2)  # disc callback
                return 1

            # X-DISC
            elif self.XreleaseDragDisc == 1 and (XclickwdgdNode[1] is True):
                # As far as we had DRAG before, we will continue run callback.
                # This is because if the mouse is not exactly on the widget, it should still take the drag.
                # Continue run the callback as far as it releaseDrag=1
                self.cb_XdiscRotate()
                self.do_callbacks(2)        # We use the same callback,
                return 1

            # X-Axis
            elif ((((clickwdglblNode is not None)
                    or (XclickwdgdNode[0] is True))
                   and (self.XreleaseDragAxis == -1))):
                # This part will be active only once when for the first time user click on the coin drawing.
                # Later DRAG should be used
                self.XreleaseDragAxis = 0
                self.XreleaseDragDisc = -1  # Not possible to have rotation while arrow is active
                self.take_focus()
                return 1
            # X-Axis
            elif ((
                (XclickwdgdNode[0] is True) or (clickwdglblNode is not None))
                  and (self.XreleaseDragAxis == 0)
                  ) :
                self.XreleaseDragAxis = 1  # Drag  will continue, it will be a drag always
                self.XreleaseDragDisc = -1
                self.take_focus()
                self.do_callbacks(1)
                return 1
            # X-Axis
            elif self.XreleaseDragAxis == 1:
                # As far as we had DRAG before, we will continue run callback.
                # This is because if the mouse is not exactly on the widget, it should still take the drag.
                # Continue run the callback as far as it releaseDrag=1
                self.do_callbacks(1)        # We use the same callback,
                return 1



        #   ------------- Y Axis  ------------- 
        if(self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                 self.w_pick_radius, self.w_YarrowsSeparator) is not None):
            YclickwdgdNode[0] = True

        if self.w_discEnabled[0]:
            if (self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                      self.w_pick_radius, self.w_YdiscSeparator) is not None):
                YclickwdgdNode[1] = True

        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK:
            if (clickwdglblNode is not None):
                # Double click event.
                print("Double click detected")
                # if not self.has_focus():
                #    self.take_focus()
                self.do_lblcallback()
                return 1

        elif self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_RELEASE:
            # disc's part
            if YclickwdgdNode[1] is True:
                # When the discs rotates, we don't accept
                # the arrow dragging. Disk rotation has priority
                if self.YreleaseDragDisc == 1 or self.YreleaseDragDisc == 0:
                    self.YreleaseDragDisc = -1
                    # Release callback should be activated
                    self.do_callbacks(0)
                    return 1
                # Axis's part
            elif YclickwdgdNode[0] is True:
                if self.YreleaseDragAxis == 1 or self.YreleaseDragAxis == 0:
                    self.YreleaseDragAxis = -1
                    self.do_callback(1)
                    return 1
            else:  # None of them -- remove the focus
                self.remove_focus()
                return 0
        
        # Mouse first click and then mouse with movement is here
        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_DRAG:
            # Y-DISC
            if((YclickwdgdNode[1] is True) and (self.YreleaseDragDisc == -1)):
                # This part will be active only once when for the first time user click on the coin drawing.
                # Later DRAG should be used
                self.YreleaseDragDisc = 0
                self.YreleaseDragAxis = -1
                self.take_focus()
                return 1
            # Y-DISC
            elif ((YclickwdgdNode[1] is True) and (self.YreleaseDragDisc == 0)):
                self.YreleaseDragDisc = 1  # Rotation will continue it will be a drag always
                self.YreleaseDragAxis = -1
                self.take_focus()
                self.cb_YdiscRotate()
                self.do_callbacks(2)  # disc callback
                return 1

            # Y-DISC
            elif self.YreleaseDragDisc == 1 and (YclickwdgdNode[1] is True):
                # As far as we had DRAG before, we will continue run callback.
                # This is because if the mouse is not exactly on the widget, it should still take the drag.
                # Continue run the callback as far as it releaseDrag=1
                self.cb_YdiscRotate()
                self.do_callbacks(2)        # We use the same callback,
                return 1

            # Y-Axis
            elif ((((clickwdglblNode is not None)
                    or (YclickwdgdNode[0] is True))
                   and (self.YreleaseDragAxis == -1))):
                # This part will be active only once when for the first time user click on the coin drawing.
                # Later DRAG should be used
                self.YreleaseDragAxis = 0
                self.YreleaseDragDisc = -1  # Not possible to have rotation while arrow is active
                self.take_focus()
                return 1
            # Y-Axis
            elif ((
                (YclickwdgdNode[0] is True) or (clickwdglblNode is not None))
                  and (self.YreleaseDragAxis == 0)
                  ) :
                self.YreleaseDragAxis = 1  # Drag  will continue, it will be a drag always
                self.YreleaseDragDisc = -1
                self.take_focus()
                self.do_callbacks(1)
                return 1
            # Y-Axis
            elif self.YreleaseDragAxis == 1:
                # As far as we had DRAG before, we will continue run callback.
                # This is because if the mouse is not exactly on the widget, it should still take the drag.
                # Continue run the callback as far as it releaseDrag=1
                self.do_callbacks(1)        # We use the same callback,
                return 1


        #   ------------- Z Axis  ------------- 
        if(self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                 self.w_pick_radius, self.w_ZarrowsSeparator) is not None):
            ZclickwdgdNode[0] = True

        if self.w_discEnabled[0]:
            if (self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                      self.w_pick_radius, self.w_ZdiscSeparator) is not None):
                ZclickwdgdNode[1] = True

        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK:
            if (clickwdglblNode is not None):
                # Double click event.
                print("Double click detected")
                # if not self.has_focus():
                #    self.take_focus()
                self.do_lblcallback()
                return 1

        elif self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_RELEASE:
            # disc's part
            if ZclickwdgdNode[1] is True:
                # When the discs rotates, we don't accept
                # the arrow dragging. Disk rotation has priority
                if self.ZreleaseDragDisc == 1 or self.ZreleaseDragDisc == 0:
                    self.ZreleaseDragDisc = -1
                    # Release callback should be activated
                    self.do_callbacks(0)
                    return 1
                # Axis's part
            elif ZclickwdgdNode[0] is True:
                if self.ZreleaseDragAxis == 1 or self.ZreleaseDragAxis == 0:
                    self.ZreleaseDragAxis = -1
                    self.do_callback(1)
                    return 1
            else:  # None of them -- remove the focus
                self.remove_focus()
                return 0
        
        # Mouse first click and then mouse with movement is here
        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_DRAG:
            # Z-DISC
            if((ZclickwdgdNode[1] is True) and (self.ZreleaseDragDisc == -1)):
                # This part will be active only once when for the first time user click on the coin drawing.
                # Later DRAG should be used
                self.ZreleaseDragDisc = 0
                self.ZreleaseDragAxis = -1
                self.take_focus()
                return 1
            # Z-DISC
            elif ((ZclickwdgdNode[1] is True) and (self.ZreleaseDragDisc == 0)):
                self.ZreleaseDragDisc = 1  # Rotation will continue it will be a drag always
                self.ZreleaseDragAxis = -1
                self.take_focus()
                self.cb_ZdiscRotate()
                self.do_callbacks(2)  # disc callback
                return 1

            # Z-DISC
            elif self.ZreleaseDragDisc == 1 and (ZclickwdgdNode[1] is True):
                # As far as we had DRAG before, we will continue run callback.
                # This is because if the mouse is not exactly on the widget, it should still take the drag.
                # Continue run the callback as far as it releaseDrag=1
                self.cb_ZdiscRotate()
                self.do_callbacks(2)        # We use the same callback,
                return 1

            # Z-Axis
            elif ((((clickwdglblNode is not None)
                    or (ZclickwdgdNode[0] is True))
                   and (self.ZreleaseDragAxis == -1))):
                # This part will be active only once when for the first time user click on the coin drawing.
                # Later DRAG should be used
                self.ZreleaseDragAxis = 0
                self.ZreleaseDragDisc = -1  # Not possible to have rotation while arrow is active
                self.take_focus()
                return 1
            # Z-Axis
            elif ((
                (ZclickwdgdNode[0] is True) or (clickwdglblNode is not None))
                  and (self.ZreleaseDragAxis == 0)
                  ) :
                self.ZreleaseDragAxis = 1  # Drag  will continue, it will be a drag always
                self.ZreleaseDragDisc = -1
                self.take_focus()
                self.do_callbacks(1)
                return 1
            # Z-Axis
            elif self.ZreleaseDragAxis == 1:
                # As far as we had DRAG before, we will continue run callback.
                # This is because if the mouse is not exactly on the widget, it should still take the drag.
                # Continue run the callback as far as it releaseDrag=1
                self.do_callbacks(1)        # We use the same callback,
                return 1

        # Don't care events, return the event to other widgets
        return 0  # We couldn't use the event .. so return 0

    def draw(self):
        """
        Main draw function. It is responsible for creating the node,
        and draw the disc on the screen. It creates a node for each 
        element and for each disc.
        """
        try:

            if (len(self.w_vector) < 2):
                raise ValueError('Must be 2 vector at least')

            usedColor = self.w_color
            if self.is_active() and self.has_focus():
                usedColor = self.w_selColor
            elif self.is_active() and (self.has_focus() != 1):
                pass  # usedColor = self.w_color  we did that already ..just for reference
            elif self.is_active() != 1:
                usedColor = self.w_inactiveColor
            # TODO: FIXME:
            preRotVal =[0.0, 0.0,0.0]
            distance = [0.0, 0.0, 0.0]
            if self.is_visible():
                preRotVal[1] = [0.0, 90.0, 0.0]  # pre-Rotation
                distance[1] = [self.distanceBetweenThem, 0.0, 0.0]
                preRotVal[1] = [0.0, 90.0, 90.0]  # pre-Rotation
                distance[1] = [0.0, self.distanceBetweenThem, 0.0]
                preRotVal[2] = [0.0, 0.0, 0.0]
                distance[2] = [0.0, 0.0, self.distanceBetweenThem]
                self.w_XarrowSeparator = draw_2Darrow(App.Vector(self.w_vector[0].x +
                                                                 distance[0],
                                                                 self.w_vector[0].y +
                                                                 distance[0],
                                                                 self.w_vector[0].z + distance[2]),
                                                      # default FR_COLOR.FR_RED
                                                      self.w_color, self.w_Scale,
                                                      self.DrawingType, self.Opacity,
                                                      preRotVal[0])
                self.w_YarrowSeparator = draw_2Darrow(App.Vector(self.w_vector[0].x +
                                                                 distance[0],
                                                                 self.w_vector[0].y +
                                                                 distance[1],
                                                                 self.w_vector[0].z + distance[2]),
                                                      # default FR_COLOR.FR_RED
                                                      self.w_color, self.w_Scale,
                                                      self.DrawingType, self.Opacity,
                                                      preRotVal[1])

                self.w_ZarrowSeparator = draw_2Darrow(App.Vector(self.w_vector[0].x +
                                                                 distance[0],
                                                                 self.w_vector[0].y +
                                                                 distance[2],
                                                                 self.w_vector[0].z + distance[2]),
                                                      # default FR_COLOR.FR_RED
                                                      self.w_color[2], self.w_Scale,
                                                      self.DrawingType, self.Opacity,
                                                      preRotVal[2])

                preRotValdisc=[]
                if self.w_discEnabled[0]:
                    preRotValdisc[0] = [self.w_discAngle, 0.0, 90.0]
                elif self.w_discEnabled[1]:  # YAxis default GREEN
                        preRotValdisc[2] = [self.w_discAngle, 0.0, 0.0]
                elif self.w_discEnabled[1]:
                    preRotValdisc[2] = [0.0, 270.0, -self.w_discAngle]

                    self.w_XdiscSeparator = draw_RotationPad(self.w_vector[0],
                                                            self.w_rotaryDisc_color[0],
                                                            self.w_Scale, self.Opacity,
                                                            preRotValdisc[0])  # RED
                    
                    self.w_YdiscSeparator = draw_RotationPad(self.w_vector[0],
                                                            self.w_rotaryDisc_color[1],
                                                            self.w_Scale, self.Opacity,
                                                            preRotValdisc[1])  # GREEN
                    self.w_ZdiscSeparator = draw_RotationPad(self.w_vector[0],
                                                            self.w_rotaryDisc_color[2],
                                                            self.w_Scale, self.Opacity,
                                                            preRotValdisc[2])  # BLUE
                    
                    self.w_userData.RotaryDisc = [self.w_XdiscSeparator,
                                                  self.w_YdiscSeparator,
                                                  self.w_ZdiscSeparator]

                transformRot = coin.SoTransform()
                separtorAll = coin.SoSeparator()
                tR = coin.SbVec3f()
                tR.setValue(
                    self.w_rotation[0], self.w_rotation[1], self.w_rotation[2])
                transformRot.rotation.setValue(tR, math.radians(self.w_rotation[3]))

                separtorAll.addChild(transformRot)
                separtorAll.addChild(self.w_XarrowSeparator)
                separtorAll.addChild(self.w_YarrowSeparator)
                separtorAll.addChild(self.w_ZarrowSeparator)
                
                if self.w_discEnabled:
                    separtorAll.addChild(self.w_XdiscSeparator)
                    separtorAll.addChild(self.w_YdiscSeparator)
                    separtorAll.addChild(self.w_ZdiscSeparator)
                self.draw_label()
                self.saveSoNodesToWidget(separtorAll)

                # add SoSeparator to the switch
                # We can put them in a tuple but it is better not doing so
                self.addSoNodeToSoSwitch(self.w_widgetSoNodes)
                self.addSoNodeToSoSwitch(self.w_widgetlblSoNodes)

        except Exception as err:
            App.Console.PrintError("'draw Fr_one_Arrow_widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

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
                            'labelcolor', 'alignment', 'rotation', setupRotation,
                            'scale']
                vectors: VECTOR  # List[App.Vector] two vectors must be provided
                linewidth: int
                fontName: str
                fontsize: int
                labelcolor: tuple
                alignment: int  # This will not be used .. not good
                rotation: tuple    # three float value and an angle 
                setupRotation: Three angle values for the xyz axis
                scale: tuple  # Three float numbers for scaling
            ]
        """
        self.w_lbluserData.SetupRotation = App.Vector(0, 0, 0)
        #self.w_lbluserData.SetupRotation[1] = App.Vector(0, 0, 90)
        #self.w_lbluserData.SetupRotation[2] = App.Vector(0, -90, 180)
        self.w_lbluserData.labelcolor = self.w_color
        lbl = fr_label_draw.draw_newlabel(self.w_label, self.w_lbluserData)
        self.saveSoNodeslblToWidget(lbl)

    def move(self, newVecPos=App.Vector(0, 0, 0)):
        """[Move the widget to a new location referenced by the 
            left-top corner of the object. Or the start of the disc
            if it is an disc.]

        Args:
            newVecPos ([App.Vector], optional): [Move the label to a new position]. Defaults to App.Vector(0,0,0).
        """
        self.w_lbluserData.vectors = [newVecPos, ]

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
            App.Console.PrintError("'del Fr_disc_Widget' Failed. "
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

    def setRotationAngle(self, axis_and_angle):
        ''' 
        Set the rotation axis and the angle. This is for the whole widget.
        Axis is coin.SbVec3f((x,y,z)
        angle=float number
        '''
        self.w_rotation = axis_and_angle

    def calculateWidgetDiskRotationAfterDrag(self, v1, v2):
        self.w_WidgetDiskRotation = math.degrees(v1.getAngle(v2))

    def enableDisc(self):
        """[Enable rotation disc. You need to redraw the widget]
        """
        self.w_discEnabled = True

    def setDistanceBetweenThem(self, newvalue):
        """[Change distance between the arrows to the origin of the widget. ]

        Args:
            newvalue ([float]): [new distance in mm]
        """
        self.distanceBetweenThem = newvalue

    def disableDisc(self):
        """[Disable rotation disc. You need to redraw the widget]
        """
        self.w_discEnabled = False

    def calculateMouseAngle(self, val1, val2):
        """[Calculate Angle of two coordinates ( xy, yz or xz).
            This function is useful to calculate mouse position
            in Angle depending on the mouse position.
        ]

        Args:
            val1 ([Horizontal coordinate]): [x, y]
            val2 ([Vertical coordinate ]): [y or z]

        Returns:
            [int]: [Calculated value in degrees]
        """
        if(val2 == 0):
            return None  # divide by zero
        result = 0
        if (val1 > 0 and val2 > 0):
            result = int(math.degrees(math.atan2(float(val1),
                                                 float(val2))))
        if (val1 < 0 and val2 > 0):
            result = int(math.degrees(math.atan2(float(val1),
                                                 float(val2))))+360
        if (val1 > 0 and val2 < 0):
            result = int(math.degrees(math.atan2(float(val1),
                                                 float(val2))))
        if (val1 < 0 and val2 < 0):
            result = int(math.degrees(math.atan2(float(val1),
                                                 float(val2))))+360
        return result

    def cb_XdiscRotate(self, userData: userDataObject = None):
        """
        Internal callback function, runs when the disc
        rotation event happens.
        self.w_discEnabled must be True
        """
        boundary = self.getWidgetsBoundary(self.w_discSeparator)
        center = self.getWidgetsCentor(self.w_discSeparator)
        try:

            self.endVector[0] = App.Vector(self.w_parent.w_lastEventXYZ.Coin_x,
                                        self.w_parent.w_lastEventXYZ.Coin_y,
                                        self.w_parent.w_lastEventXYZ.Coin_z)
            if self.run_Once[0] is False:
                self.run_Once[0] = True
                self.startVector[0] = self.endVector[0]

            # Keep the old value only first time when drag start
                self.startVector[0] = self.endVector[0]
                if not self.has_focus():
                    self.take_focus()
            newValue = self.endVector[0]

            print(center, "center")
            mx = my = mz = 0.0

            # Right
            # It means that we have changes in Z and Y only
            # If the mouse moves at the >center in Z direction :
            # Z++  means   -Angel, Z--  means  +Angle    --> When Y is +                   ^
            # Z++  means   +Angel, Z--  means  -Angle    --> When Y is -                   v
            # Y++  means   +Angel, Y--  means  -Angel    -->  when Z is +
            # Y++  means   -Angel, Y--  means  +Angel    -->  when Z is -
            my = (newValue.y - center.y)
            mz = (newValue.z - center.z)
            if (mz == 0):
                return  # Invalid
            self.w_discAngle[0] = faced.calculateMouseAngle(my, mz)
            if (self.w_discAngle == 360):
                self.w_discAngle[0] = 0
            if (self.oldAngle[0] < 45 and self.oldAngle[0] >= 0) and (self.w_discAngle[0] > 270):
                self.rotationDirection = -1
                self.w_discAngle[0] = self.w_discAngle[0]-360

            elif(self.rotationDirection[0] == -1
                 and self.w_discAngle[0] > 0
                 and self.w_discAngle[0] < 45
                 and self.oldAngle[0] < -270):
                self.rotationDirection[0] = 1

            # we don't accept an angel grater or smaller than 360 degrees
            if(self.rotationDirection[0] < 0):
                self.w_discAngle[0] = self.w_discAngle[0]-360

            if(self.w_discAngle[0] > 359):
                self.w_discAngle[0] = 359
            elif(self.w_discAngle[0] < -359):
                self.w_discAngle[0]= -359
            if self.w_discAngle[0] == -360:
                self.w_discAngle[0] = 0
            self.oldAngle[0] = self.w_discAngle[0]
            print("XAngle=", self.w_discAngle[0])
            self.redraw()

        except Exception as err:
            App.Console.PrintError("'disc Callback' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


    def cb_YdiscRotate(self, userData: userDataObject = None):
        """
        Internal callback function, runs when the disc
        rotation event happens.
        self.w_discEnabled must be True
        """
        boundary = self.getWidgetsBoundary(self.w_discSeparator)
        center = self.getWidgetsCentor(self.w_discSeparator)
        try:

            self.endVector[1] = App.Vector(self.w_parent.w_lastEventXYZ.Coin_x,
                                        self.w_parent.w_lastEventXYZ.Coin_y,
                                        self.w_parent.w_lastEventXYZ.Coin_z)
            if self.run_Once[1] is False:
                self.run_Once[1] = True
                self.startVector[1] = self.endVector[1]

            # Keep the old value only first time when drag start
                self.startVector[1] = self.endVector[1]
                if not self.has_focus():
                    self.take_focus()
            newValue = self.endVector[1]

            print(center, "center")
            mx = my = mz = 0.0
            # Front
            # It means that we have changes in Z and X only
            # Z++  means   -Angel, Z--  means  +Angle    -->  When X is +                   ^
            # Z++  means   +Angel, Z--  means  -Angle    -->  When X is -                   v
            # X++  means   -Angel, x--  means  +Angel    -->  when Z is +
            # X++  means   +Angel, x--  means  -Angel    -->  when Z is -
            mx = (newValue.x - center.x)
            mz = (newValue.z - center.z)
            if (mz == 0):
                return  # Invalid
            self.w_discAngle[1] = faced.calculateMouseAngle(mx, mz)
            if (self.w_discAngle[1] == 360):
                self.w_discAngle[1] = 0
            if (self.oldAngle[1] < 45 and self.oldAngle[1] >= 0) and (self.w_discAngle[1] > 270):
                self.rotationDirection[1] = -1
                self.w_discAngle[1] = self.w_discAngle[1]-360

            elif(self.rotationDirection[1] == -1
                 and self.w_discAngle[1] > 0
                 and self.w_discAngle[1] < 45
                 and self.oldAngle1[1] < -270):
                self.rotationDirection[1] = 1

            # we don't accept an angel grater or smaller than 360 degrees
            if(self.rotationDirection[1] < 0):
                self.w_discAngle[1] = self.w_discAngle[1]-360

            if(self.w_discAngle [1]> 359):
                self.w_discAngle[1] = 359
            elif(self.w_discAngle[1] < -359):
                self.w_discAngle [1]= -359
            if self.w_discAngle[1]== -360:
                self.w_discAngle[1]= 0
            self.oldAngle[1] = self.w_discAngle[1]
            print("YAngle=", self.w_discAngle[1])
            self.redraw()

        except Exception as err:
            App.Console.PrintError("'disc Callback' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


    def cb_ZdiscRotate(self, userData: userDataObject = None):
        """
        Internal callback function, runs when the disc
        rotation event happens.
        self.w_discEnabled must be True
        """
        boundary = self.getWidgetsBoundary(self.w_discSeparator[2])
        center = self.getWidgetsCentor(self.w_discSeparator[2])
        try:

            self.endVector[2] = App.Vector(self.w_parent.w_lastEventXYZ.Coin_x,
                                        self.w_parent.w_lastEventXYZ.Coin_y,
                                        self.w_parent.w_lastEventXYZ.Coin_z)
            if self.run_Once [2] is False:
                self.run_Once[2]  = True
                self.startVector[2] = self.endVector[2]

            # Keep the old value only first time when drag start
                self.startVector[2] = self.endVector[2]
                if not self.has_focus():
                    self.take_focus()
            newValue = self.endVector[2]

            print(center, "center")
            mx = my = mz = 0.0

            # It means that we have changes in X and Y only
            # Y++  means   -Angel, Y--  means  +Angle    -->  When X is +                   ^
            # Y++  means   +Angel, Y--  means  -Angle    -->  When X is -                   v
            # x++  means   -Angel, X--  means  +Angel    -->  when Y is +
            # x++  means   +Angel, X--  means  -Angel    -->  when Y is -
            mx = (newValue.x - center.x)
            my = (newValue.y - center.y)
            if (my == 0):
                return  # Invalid
            self.w_discAngle[2] = faced.calculateMouseAngle(mx, my)
            if (self.w_discAngle[2] == 360):
                self.w_discAngle[2] = 0
            if (self.oldAngle[2] < 45 and self.oldAngle[2] >= 0) and (self.w_discAngle[2] > 270):
                self.rotationDirection[2] = -1
                self.w_discAngle[2] = self.w_discAngle[2]-360

            elif(self.rotationDirection == -1
                 and self.w_discAngle[2]> 0
                 and self.w_discAngle[2]< 45
                 and self.oldAngle[2] < -270):
                self.rotationDirection[2] = 1

            # we don't accept an angel grater or smaller than 360 degrees
            if(self.rotationDirection[2] < 0):
                self.w_discAngle[2] = self.w_discAngle[2]-360

            if(self.w_discAngle [2]> 359):
                self.w_discAngle[2]= 359
            elif(self.w_discAngle[2] < -359):
                self.w_discAngle [2]= -359
            if self.w_discAngle [2]== -360:
                self.w_discAngle[2] = 0
            self.oldAngle[2] = self.w_discAngle[2]
            print("ZAngle=", self.w_discAngle[2])
            self.redraw()

        except Exception as err:
            App.Console.PrintError("'disc Callback' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    @property
    def getAngle(self):
        return self.w_discAngle

    def do_callbacks(self, callbackType=-1):
        """[summarize the call of the callbacks]

        Args:
            callbackType (int, optional): 
            [Call specific callback depending on the callback type]. Defaults to -1.
            userData will hold the direction dependently.
            Axis   : holds the axis name ('X','Y' or 'Z') as letter
            _rotaryDisc: holds the discs (wheel) rotation axis ('X','Y' or 'Z') 
            as letters.  
        """
        if(callbackType == 0):
            # normal callback This represent the whole widget.
            # Use this to finalize the action.
            self.do_callback()

        # Move callback - Axis
        elif(callbackType == 1):
            self.w_userData.discObj = None
            self.w_XarrowAxis_cb_(self.w_userData)
        elif(callbackType == 2):
            # Rotate callback
            if self.w_discEnabled[0]:
                # Rotation callback - Disc
                self.w_userData.Axis = None
                self.w_rotary_cb_(self.w_userData)
