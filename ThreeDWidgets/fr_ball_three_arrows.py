# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2022                                                    *
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
from types import coroutine
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import Design456Init
from typing import List
from ThreeDWidgets.constant import FR_COLOR
# draw a line in 3D world
import math
from dataclasses import dataclass

__updated__ = '2022-10-02 22:06:32'
'''
    This widget will be used with the smart sweep. 
    It should consist of three arrows and a ball. 
    There will be four callbacks. 
    -One for the ball,
    -One for the X-Arrow
    -One for the Y-Arrow
    -One for the Z-Arrow
    The ball's callback should freely without restrictions move the ball's position.
    After the change of each of these callbacks, there is a general callback which should be
    given to the widget and will be executed. 
    That callback should update the related object in FreeCAD not coin3d.

'''

"""
Example how to use this widget.

# show the window and it's widgets.
import ThreeDWidgets.fr_one_arrow_widget as wd
import ThreeDWidgets.fr_coinwindow as wnn
from ThreeDWidgets.constant import FR_COLOR


"""

# *************************************************************


class Fr_BallThreeArrows_Widget(fr_widget.Fr_Widget):

    def __init__(self, vectors: List[App.Vector] = [],
                 label: str = [[]],
                 _lblColor=FR_COLOR.FR_WHITE,
                 _axisColor=FR_COLOR.FR_RED,
                 _opacity: float = 0.0):
        super().__init__(vectors, label)

 

    def handle(self, event):
        return 0  # We couldn't use the event .. so return 0

    def draw(self):
        """
        Main draw function. It is responsible for creating the node,
        and draw the disc on the screen. It creates a node for each 
        element and for each disc.
        """
        try:
            pass
        except Exception as err:
            App.Console.PrintError("'draw Fr_one_Arrow_widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_label(self):
        pass

 
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
            App.Console.PrintError("'del fr_ball_three_arrows' Failed. "
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
