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
from typing import List
from dataclasses import dataclass
from ThreeDWidgets.constant import FR_COLOR
from ThreeDWidgets.fr_one_arrow_widget import Fr_OneArrow_Widget
from ThreeDWidgets.constant import FR_WidgetType
from ThreeDWidgets import fr_widget
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
arrows=w.Fr_ThreeArrows_Widget(vec,["Pad",])
arrows.Activated()
arrows.enableDiscs()
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


class Fr_ThreeArrows_Widget(object):

    """
    This class is for drawing a one Degrees Pad
    This will be used later to create 3D Pad. 
    Or it can be used as a singel rotate/move widget
    """

    def __init__(self, _vectors: List[App.Vector] = [],
                 _label: str = [[]],
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
        self.w_parent = None
        self.w_widgetType = FR_WidgetType.FR_THREE_DISC
        self.w_lbluserData = fr_widget.propertyValues()
        self.w_color = FR_COLOR.FR_RED
        self.w_selColor = [i * 1.2 for i in self.w_color]
        self.w_userData = userDataObject()  # Keep info about the widget
        self.w_userData.discObj = self
        self.w_discAngle = 0.0      # Only disc rotation.
        self.oldAngle = 0.0
        self.rotationDirection = 1   # +1 CCW , -1 ACCW
        self.w_lineWidth =1
        # This affect only the Widget label - nothing else
        self.w_lbluserData.linewidth = self.w_lineWidth
        self.w_lbluserData.vectors = self.w_vector

        

    def Activated(self):

        self.w_axisList.append(Fr_OneArrow_Widget(
            self.w_vector, ["X-Axis", ], "X",
            self.w_labelColor, self.w_padColors[0],
            self.w_rotation, self.w_scale, self.w_type,
            self.w_opacity[0], self.w_distanceBetweenThem[0]))
        self.w_axisList.append(Fr_OneArrow_Widget(
            self.w_vector, ["Y-Axis", ], "Y",
            self.w_labelColor, self.w_padColors[1],
            self.w_rotation, self.w_scale, self.w_type,
            self.w_opacity[1], self.w_distanceBetweenThem[0]))
        self.w_axisList.append(Fr_OneArrow_Widget(
            self.w_vector, ["Z-Axis", ], "Z",
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
        self.w_axisList[0].enableDisc()

    def enableYDisc(self):
        self.w_axisList[1].enableDisc()

    def enableZDisc(self):
        self.w_axisList[2].enableDisc()

    def enableDiscs(self):
        for obj in self.w_axisList:
            obj.enableDisc()

    def disableXDisc(self):
        self.w_axisList[0].disableDisc()

    def disableYDisc(self):
        self.w_axisList[1].disableDisc()

    def disableZDisc(self):
        self.w_axisList[2].disableDisc()

    def disableDiscs(self):
        for obj in self.w_axisList:
            obj.disableDisc()

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
            obj.show()

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
        for obj in self.w_axisList:
            obj.w_parent = parent

    @property
    def getDiscEnabled(self):
        return (self.w_axisList[0].w_discEnabled,
                self.w_axisList[1].w_discEnabled,
                self.w_axisList[2].w_discEnabled)

    def handle(self, event):
        t2 = self.w_axisList[1].handle(event)
        t3 = self.w_axisList[2].handle(event)
        t1 = self.w_axisList[0].handle(event)
        return(t1 or t2 or t3)
    
    def take_focus(self):
        """
        Set focus to the widget. Which should redraw it also.
        """ 
        for obj in self.w_axisList:
            obj.w_hasFocus = 1
            obj.redraw()

    def activate(self):
        """[Activate the widget so it can take events]

        """
        for obj in self.w_axisList:
            obj.w_active = 1

    def deactivate(self):
        """
        Deactivate the widget. which causes that no handle comes to the widget
        """
        for obj in self.w_axisList:
            obj.w_active = 0

    def ChangeScale(self, newScale=[1, 1, 1]):
        """[Scale the whole widget default is no scaling ]

        Args:
            newScale (list, optional): [New scale to apply to the widget]. Defaults to [1.0,1.0,1.0].
        """
        for obj in self.w_axisList:
            obj.w_Scale = newScale

    def __del__(self):
        """
        Class Destructor.
        This will remove the widget totally.
        """
        self.hide()
        try:
            if self.w_parent is not None:
                # Parent should be the windows widget.
                for obj in self.w_axisList:
                    obj.w_parent.removeWidget(obj)
                    obj.w_parent.removeSoSwitchFromSceneGraph(obj.w_wdgsoSwitch)
                    obj.removeSoNodeFromSoSwitch()
                    obj.removeSoNodes()
                    obj.removeSoSwitch()

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
        for obj in self.w_axisList:
            obj.w_visible = 0
            obj.w_wdgsoSwitch.whichChild = coin.SO_SWITCH_NONE  # hide all children
        self.redraw()

    def remove_focus(self):
        """
        Remove the focus from the widget. 
        This happens by clicking anything 
        else than the widget itself
        """
        for obj in self.w_axisList:
            obj.w_hasFocus = 0
            obj.redraw()

    def resize(self, _scale: tuple = [1.0, 1.0, 1.0]):
        """Resize the widget by using the new vectors"""
        for obj in self.w_axisList:
            obj.w_Scale = _scale
            obj.redraw()

    def size(self, _scale: tuple = [1.0, 1.0, 1.0]):
        """[Scale the widget for the three directions]

        Args:
            _scale (tuple, Three float values): [Scale the widget using three float values for x,y,z axis]. 
            Defaults to [1.0, 1.0, 1.0].
        """
        for obj in self.w_axisList:
            obj.resize(_scale)

    def label(self, newlabel):
        for obj in self.w_axisList:
            obj.w_label = newlabel

    # Keep in mind you must run lblRedraw
    def label_font(self, name="sans"):
        """[Change Label Font]

        Args:
            name (str, optional): [Change label font]. Defaults to "sans".
        """
        for obj in self.w_axisList:
            obj.w_lbluserData.fontName = name

    # Keep in mind you must run lblRedraw
    def label_scale(self, newsize: tuple = [1.0, 1.0, 1.0]):
        """[Scale the font using three float values. This is not the font size.
        You must redraw the label to get this scaling done.
        ]

        Args:
            newsize (int, optional): [Change font label ]. Defaults to 1.
        """
        for obj in self.w_axisList:
            obj.w_lbluserData.scale = newsize

    # Keep in mind you must run lblRedraw
    def label_fontsize(self, newsize=1):
        """[Change label font size ]

        Args:
            newsize (int, optional): [Change fontsize of the label ]. Defaults to 1.
        """
        for obj in self.w_axisList:
            obj.w_lbluserData.fontsize = newsize

    # Must be App.Vector TODO:FIXME: 
    def label_move(self, newPos=App.Vector(0.0, 0.0, 0.0)):
        """[Move location of the label]

        Args:
            newPos ([App.Vector], optional): [Change placement of the label]. Defaults to App.Vector(0.0, 0.0, 0.0).
        """
        for obj in self.w_axisList:
            obj.w_lbluserData.vectors[0] = newPos