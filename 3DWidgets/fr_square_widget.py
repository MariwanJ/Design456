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
import Design456Init
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import constant
import fr_draw
import fr_widget
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
        This function is responsbile of taking events and doing 
        the action(s) required. If the object is not targeted, 
        the function will skip the event(s). But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. fr_coinwindow object is responsible for distributing the events.
        """

        if self._parent.link_to_root_handle._lastEvent == constant.FR_EVENTS.FR_MOUSE_LEFT_PUSH:
            clickedNode = fr_coin3d.objectMouseClick_Coin3d(
                self._parent.link_to_root_handle._lastEventXYZ.pos, self._pick_radius)
            found = False
            if self._wdgsoSwitch.findChild(clickedNode) != -1:
                found = True
            if found == True:
                self.take_focus()
                self.do_callback(self._userData)
                found=False
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
        self._widgetType = constant.FR_WidgetType.FR_SQUARE_FRAME
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
                self.addSeneNodes(list)                         #Add SoSeparator
                for i in list: 
                    self.addSoNodeToSoSwitch(i)  #Add SoSeparator as child to Switch
                self._parent.addSoSwitch(self._wdgsoSwitch)     #Add the switch to the SeneGraph
            else:
                raise ValueError("Couldn't draw the Fr_SquareFrame_Widget")
        else:
            return  # We draw nothing .. This is here just for clarifying the code

    def show(self):
        self._visible = True
        self._wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all children
        self.redraw()

    def redraw(self):
        """
        After the widgets damages, this function should be called.        
        """
        if self.is_visible():
            # Remove the node from the switch as a child
            self.removeSoNodeFromSoSwitch()
            # Remove the seneNodes from the widget
            self.removeSeneNodes()
            # Remove the SoSwitch from fr_coinwindo
            self._parent.removeSoSwitch(self._wdgsoSwitch)
            self.draw()

    def take_focus(self):
        """
        Set focus to the widget. Which should redraw it also.
        """
        if self._hasFocus == True:
            return  # nothing to do here
        self._hasFocus = True
        self.redraw()

    def activate(self):
        if self._active:
            return  # nothing to do
        self._active = True
        self.redraw()

    def deactivate(self):
        """
        Deactivate the widget. which causes that no handle comes to the widget
        """
        if self._active == False:
            return  # Nothing to do
        self._active = False

    def destructor(self):
        """
        This will remove the widget totally. 
        """
        self.removeSeneNodes()

    def is_active(self):
        return self._active

    def hide(self):
        if self._visible == False:
            return  # nothing to do
        self._visible = False
        self._wdgsoSwitch.whichChild = coin.SO_SWITCH_NONE  # hide all children
        self.redraw()

    def remove_focus(self):
        """
        Remove the focus from the widget. 
        This happens by clicking anything 
        else than the widget itself
        """
        if self._hasFocus == False:
            return  # nothing to do
        else:
            self._hasFocus = False
            self.redraw()

    def resize(self, args: List[App.Vector]):  # Width, height, thickness
        """Resize the widget by using the new vectors"""
        self._vector = args
        self.redraw()

    def size(self, args: List[App.Vector]):
        """Resize the widget by using the new vectors"""
        self.resize(args)
        
    def move(self, newVecPos):
        """
        Move the object to the new location referenced by the 
        left-top corner of the object. Or the start of the line
        if it is a line.
        """
        self.resize(newVecPos)
