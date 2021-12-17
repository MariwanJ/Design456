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
from ThreeDWidgets.fr_one_arrow_widget import Fr_OneArrow_Widget
import math
"""
Example how to use this widget.

import ThreeDWidgets.fr_coinwindow as wnn
import math
import fr_three_arrows_widget as w
mywin = wnn.Fr_CoinWindow()

vec=[]
vec.append(App.Vector(0,0,0))
vec.append(App.Vector(0,0,0))  #Dummy won't be used
arrows=w.Fr_ThreeArrows_Widget(vec,"Pad")
arrows.Activated()
mywin.addWidget(arrows.getWidgets)
mywin.show()


"""
# TODO: FIXME: old implementation was to complex. we will uses one arrow widget 3 times.


@dataclass
class userDataObject:

    def __init__(self):
        self.PadObj = None      # the Pad widget object
        self.events = None        # events - save handle events here
        self.callerObject = None  # Class/Tool uses the fr_Pad_widget
        self.padAxis = None
        self.Axis = None


# *******************************CALLBACKS - DEMO *****************************
def xAxis_cb(userData: userDataObject = None):
    """
        This function executes when the XAxis
        event callback.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy XAxis callback")


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
    print("dummy YAxis callback")


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
    print("dummy ZAxis callback")


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


class Fr_ThreeArrows_Widget(object):

    """
    This class is for drawing a one Degrees Pad
    This will be used later to create 3D Pad. 
    Or it can be used as a singel rotate/move widget
    """

    def __init__(self, _vectors: List[App.Vector] = [],
                 _label: str = "",
                 _lblColor=FR_COLOR.FR_WHITE,
                 _padColors=[FR_COLOR.FR_RED,
                             FR_COLOR.FR_GREEN,
                             FR_COLOR.FR_BLUE],
                 # User controlled rotation. This is only for the 3Pads
                 _rotation: List[float] = [0.0, 0.0, 0.0, 0.0],
                 # Face position-direction controlled rotation at creation. Whole widget
                 _scale=[3, 3, 3],
                 _type=1,
                 _opacity=[0.0, 0.0, 0.0],
                 _distanceBetweenThem=[5, 5, 5]
                 ):

        self.w_axisList = []
        self.w_vector = _vectors
        self.w_label = _label
        self.w_labelColor = _lblColor
        self.w_padColors = _padColors
        self.w_rotation = _rotation
        self.w_scale = _scale
        self.w_type = _type
        self.w_opacity = _opacity
        self.w_distanceBetweenThem = _distanceBetweenThem
        self.w_parent=None

    def Activated(self):

        self.w_axisList.append(Fr_OneArrow_Widget(
            self.w_vector, "X-Axis", "X",
            self.w_labelColor, self.w_padColors[0],
            self.w_rotation, self.w_scale, self.w_type,
            self.w_opacity[0], self.w_distanceBetweenThem[0]))
        self.w_axisList.append(Fr_OneArrow_Widget(
            self.w_vector, "Y-Axis", "Y",
            self.w_labelColor, self.w_padColors[1],
            self.w_rotation, self.w_scale, self.w_type,
            self.w_opacity[1], self.w_distanceBetweenThem[0]))
        self.w_axisList.append(Fr_OneArrow_Widget(
            self.w_vector, "Z-Axis", "Z",
            self.w_labelColor, self.w_padColors[2],
            self.w_rotation, self.w_scale, self.w_type,
            self.w_opacity[2], self.w_distanceBetweenThem[0]))

        self.w_axisList[0].w_ArrowAxis_cb_ = xAxis_cb
        self.w_axisList[0].w_rotary_cb_ = xDisc_cb
        self.w_axisList[1].w_ArrowAxis_cb_ = yAxis_cb
        self.w_axisList[1].w_rotary_cb_ = yDisc_cb
        self.w_axisList[2].w_ArrowAxis_cb_ = zAxis_cb
        self.w_axisList[2].w_rotary_cb_ = zDisc_cb
        


    @property
    def getWidgets(self):
        return self.w_axisList

    def enableXDisc(self):
        self.w_axisList[0].enableDisc

    def enableYDisc(self):
        self.w_axisList[1].enableDisc

    def enableZDisc(self):
        self.w_axisList[2].enableDisc

    def enableDiscs(self):
        for obj in self.w_axisList:
            obj.enableDisc()

    def draw(self):
        for obj in self.w_axisList:
            obj.redraw()

    def redraw(self):
        for obj in self.w_axisList:
            obj.redraw()
    
    def hide(self):
        for obj in self.w_axisList:
            obj.hide()

    def show(self):
        for obj in self.w_axisList:
            obj.redraw()

        for obj in self.w_axisList:
            obj.show()
    @property        
    def getparent(self):
        """
            Get parent windows
        """
        return self.w_parent

    def parent(self, parent):
        """ 
            Set the parent to the widget
        """
        self.w_parent = parent
    
    def getDiscEnabled(self):
        return (self.w_axisList[0].w_discEnabled,
                self.w_axisList[1].w_discEnabled,
                self.w_axisList[2].w_discEnabled)