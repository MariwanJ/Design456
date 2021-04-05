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
import Design456Init
import fr_draw
import fr_widget
import constant
import fr_coin3d
from typing import List


class Fr_SquareFrame_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a line in  coin3D
    """
    global _lineWidth

    # def __init__(self, args:fr_widget.VECTOR=[],l=""):
    def __init__(self, args: List[App.Vector] = [], label: str = "",lineWidth=1):
        if args == None:
            args = []
        self._widgetType = constant.FR_WidgetType.Fr_SquareFrame_Widget
        self._lineWidth = lineWidth # default line width
        self._label=label
        self._vector=args
        super().__init__(args, label)

    def addVertices(self, vertices):
        self._vector.clear()
        self._vector = vertices

    def LineWidth(self, width):
        self._linewidth = width

    def handle(self, event):
        """
        This function is responsbile of taking events and processing 
        the actions required. If the object is not targeted, 
        the function will skip the events. But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. Window object is responsible for distributing the events.
        """
        if self._parent.link_to_root_handle._lastEvent == constant.FR_EVENTS.MOUSE_LEFT_PUSH:
            clickedNode = fr_coin3d.objectMouseClick_Coin3d(
                self.parent.link_to_root_handle.lastEventXYZ.pos, self.pick_radius)
            found = False
            for i in self._widgetCoinNode:
                if i == None or clickedNode == None:
                    break
                if i.getClassTypeId() == clickedNode.getClassTypeId() and i == clickedNode:
                    found = True
                    break  # We don't need to search more
            if found == True:
                self.take_focus()
                return 1
            else:
                self.remove_focus()
                return event  # We couldn't use the event .. so return the event itself

    def draw(self):
        """
        Main draw function. It is responsible to create the node,
        and draw the line on the screen. It creates a node for 
        the line.
        """
        if len(self._vector) < 4:
            raise ValueError('Vertices must be 4')
        if self.is_active() and self.has_focus():
            usedColor = self._selColor
        elif self.is_active() and (self.has_focus() != 1):
            usedColor = self._activeColor
        elif self.is_active() != 1:
            usedColor = self._inactiveColor
        if self.is_visible():
            list= fr_draw.draw_square_frame(self._vector, usedColor, self._lineWidth)
            if list is not None:
                # put the node inside the switch
                self.addSoNodeToSoSwitch(list)
                self._parent.addSoSwitch(self._wdgsoSwitch)
            else:
                raise ValueError("Couldn't draw the Fr_SquareFrame_Widget")
        else:
            return  # We draw nothing .. This is here just for clarity of the code

    # def redraw(self):
    #    """ When drawing damages, a redraw must be done.
    #    This function will redraw the widget on the 3D
    #    Scene"""
    #    self.removeSoNodeFromSoSwitch()   # Remove the node from the switch as a child
    #    self.removeSeneNodes()            # Remove the seneNodes from the widget
    #    self._parent.removeSoSwitch()     # Remove the SoSwitch from fr_coinwindow
    #    self._widgetCoinNode.clear()      # clear the list
    #    self.draw()                       # Redraw the whole object

    def move(self, newVector):
        """
        Move the object to the new location referenced by the 
        left-top corner of the object. Or the start of the line
        if it is a line.
        """
        self.resize(newVector)

    def show(self):
        self._visible = True
        self._wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all children
        # self.redraw()

    def hide(self):
        self._wdgsoSwitch.whichChild = coin.SO_SWITCH_NONE  # Show all children
