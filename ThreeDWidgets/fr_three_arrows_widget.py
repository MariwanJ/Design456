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
#TODO :FIXME:
    def __init__(self):
        self.PadObjs = None      # the Pad widget object
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

# TODO : FIXME:
# Implementation should be based on the one-arrow-widget
# This must be much much simpler than it was. 
# All functions here must be rewritten to implement
# 


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
        self.axisList = []

        self.w_color = _lblColor  # not used for this widget
        self.w_PadAxis_color = _padColor
        self.w_selColor = [i * 1.2 for i in self.w_selColor]
        self.w_Scale = _scale
        self.w_inactiveColor = [i * 0.5 for i in self.w_selColor]
 
        self.w_userData = userDataObject()  # Keep info about the widget
        self.w_userData.PadObjs = self

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
        
        # Don't care events, return the event to other widgets
        return 0  # We couldn't use the event .. so return 0

    def draw(self):
        """
        Main draw function. It is responsible to create the node,
        and draw the Pad on the screen. It creates a node for each 
        element and for each Pad.
        """
        try:
            #TODO : FIXME:
            if (len(self.w_vector) < 1):
                raise ValueError('Must be a vector')

            usedColor = self.w_color
            if self.is_active() and self.has_focus():
                usedColor = self.w_selColor
            elif self.is_active() and (self.has_focus() != 1):
                pass  # usedColor = self.w_color  we did that already ..just for reference
            elif self.is_active() != 1:
                usedColor = self.w_inactiveColor


        except Exception as err:
            App.Console.PrintError("'draw Fr_Pad_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
