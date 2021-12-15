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
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from ThreeDWidgets.fr_one_arrow_widget import Fr_OneArrow_Widget
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
# TODO: FIXME: old implementation was to complex. we will uses one arrow widget 3 times.


@dataclass
class userDataObject:
    # TODO :FIXME:
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
                 _Rotation: List[float] = [0.0, 0.0, 0.0, 0.0],
                 _scale: List[float] = [3, 3, 3],
                 _type: int = 1,
                 _opacity: float = 0,
                 _distanceBetweenThem: List[float] = [5, 5, 5]):
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

        self.w_color = _lblColor  # not used for this widget
        self.w_PadAxis_color = _padColor
        self.w_selColor = [i * 1.2 for i in self.w_selColor]
        self.w_scale = _scale
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
        self.w_padEnabled = False
        self.created = False  # Use this to call the creation of the arrows and discs once
        self.axisList = []
        self.w_wdgsoSwitch = coin.SoSwitch()
        self.axisList.append(Fr_OneArrow_Widget(self.w_vector, "",
                                                'X', FR_COLOR.FR_WHITE,
                                                FR_COLOR.FR_RED,
                                                self.w_Rotation,
                                                self.w_scale, self.type, self.Opacity, self.distanceBetweenThem[0]))
        self.axisList.append(Fr_OneArrow_Widget(self.w_vector, "",
                                                'Y', FR_COLOR.FR_WHITE,
                                                FR_COLOR.FR_GREEN,
                                                self.w_Rotation,
                                                self.w_scale, self.type, self.Opacity, self.distanceBetweenThem[1]))
        self.axisList.append(Fr_OneArrow_Widget(self.w_vector, "",
                                                'Z', FR_COLOR.FR_WHITE,
                                                FR_COLOR.FR_BLUE,
                                                self.w_Rotation,
                                                self.w_scale, self.type, self.Opacity, self.distanceBetweenThem[2]))

    def draw(self):
        try:
            collectAll = []
            collectAllLBL = []
            for obj in self.axisList:
                obj.parent(self.w_parent)
                obj.draw()
                collectAllLBL.append(obj.w_widgetlblSoNodes)
                collectAll.append(obj.w_widgetSoNodes)
            print(self.w_parent,"self.w_parent")
            self.saveSoNodesToWidget(collectAll)
            self.saveSoNodeslblToWidget(collectAllLBL)

            self.addSoNodeToSoSwitch(self.w_widgetSoNodes)
            self.addSoNodeToSoSwitch(self.w_widgetlblSoNodes)

        except Exception as err:
            App.Console.PrintError("'Fr_ThreeArrows_Widget draw' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def redraw(self):
        for obj in self.axisList:
            obj.redraw()

    def show(self):
        for obj in self.axisList:
            obj.show()
        self.w_wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all children

    def hide(self):
        for obj in self.axisList:
            obj.hide()

    def enableDisc(self, discNr='ALL'):
        if discNr == 'ALL' or discNr == "XYZ":
            for obj in self.axisList:
                obj.enableDisc()
        elif discNr == 'X':
            self.axisList[0].enableDisc()
        elif discNr == 'Y':
            self.axisList[1].enableDisc()
        elif discNr == 'Z':
            self.axisList[2].enableDisc()
        elif discNr == "XY":
            self.axisList[0].enableDisc()
            self.axisList[1].enableDisc()
        elif discNr == 'XZ':
            self.axisList[0].enableDisc()
            self.axisList[2].enableDisc()
        elif discNr == 'YZ':
            self.axisList[1].enableDisc()
            self.axisList[2].enableDisc()

    def handle(self, event):

        # Don't care events, return the event to other widgets
        return 0  # We couldn't use the event .. so return 0

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
        for obj in self.axisList:
            obj.resize(_scale)

    def label(self, newlabel, _axis="ALL"):
        self.w_label = newlabel
        if _axis == "ALL" or _axis == "XYZ":
            for obj in self.axisList:
                obj.label(newlabel)
        elif _axis == 'X':
            self.axisList[0].label(newlabel)
        elif _axis == 'Y':
            self.axisList[1].label(newlabel)
        elif _axis == 'Z':
            self.axisList[2].label(newlabel)
        elif _axis == "XY":
            self.axisList[0].label(newlabel)
            self.axisList[1].label(newlabel)
        elif _axis == 'XZ':
            self.axisList[0].label(newlabel)
            self.axisList[2].label(newlabel)
        elif _axis == 'YZ':
            self.axisList[1].label(newlabel)
            self.axisList[2].label(newlabel)

    def draw_label(self):
        for obj in self.axisList:
            obj.draw_label()

    def lblRedraw(self):
        """[Redraw the label]
        """
        for obj in self.axisList:
            obj.lblRedraw()

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
        self.w_Rotation = axis_and_angle
