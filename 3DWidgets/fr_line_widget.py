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
"""
Example how to use this widget. 

import fr_coinwindow as wn
import fr_line_widget as line
import FreeCAD as App
g=[]
p1=(0,0,0)     # first point in the line and for the windows
g=[]
p2=(400,400,0) # width and hight of the window .. z is not a matter (generally this has no effect)
p3=(20,20,0)   # Second point in the line 
g.append(p1)
g.append(p2)
wn=wn.Fr_CoinWindow(g,"MyWindow")  # Create the window, label has no effect at the moment
g.clear()
g.append(p1)
g.append(p3)
ln =line.Fr_Line_Widget(g)   # draw the line - nothing will be visible yet
wn.addChild(ln)              # Add it to the window as a child 
ln.parent=wn                 # define parent for the widget
wn.show()                    # show the window and it's widgets. 


"""


class Fr_Line_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a line in coin3D world
    """
    global _lineWidth

    def __init__(self, args: fr_widget.VECTOR = None, l=""):
        if args == None:
            args = []
        self.WidgetType = constant.FR_WidgetType.FR_EDGE
        self._lineWidth = 1  # Default line width
        super().__init__(args, l)

    def lineWidth(self, width):
        """ Set the line width"""
        self._lineWidth = width

    def handle(self, event):
        """
        This function is responsbile of taking events and processing 
        the actions required. If the object is not targeted, 
        the function will skip the events. But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. Window object is responsible for distributing the events.
        """
        if self.parent.link_to_root_handle.lastEvent == constant.FR_EVENTS.FR_MOUSE_LEFT_PUSH:
            clickedNode = fr_coin3d.objectMouseClick_Coin3d(
                self.parent.link_to_root_handle.lastEventXYZ.pos, self.pick_radius)
            find = False
            for i in self._widgetCoinNode:
                if i == None or clickedNode == None:
                    break
                if i.getClassTypeId() == clickedNode.getClassTypeId() and i == clickedNode:
                    find = True
                    break  # We don't need to search more
            if find == True:
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
        if len(self._vector) < 2:
            raise ValueError('Must be 2 Vectors')
        p1 = self._vector[0]
        p2 = self._vector[1]

        if self.is_active() and self.has_focus():
            usedColor = self.selCol
        elif self.is_active() and (self.has_focus() != 1):
            usedColor = self.activeCol
        elif self.is_active() != 1:
            usedColor = self.inactiveCol
        if self.is_visible():
            self._widgetCoinNode = fr_draw.draw_line(
                p1, p2, usedColor, self._lineWidth)
            self.parent.addSeneNode(self._widgetCoinNode)
        else:
            return  # We draw nothing .. This is here just for clarity of the code

    def redraw(self):
        """ When drawing damages, a redraw must be done.
        This function will redraw the widget on the 3D
        Scene"""
        if self.is_visible():
            self.parent.removeSeneNode(self._widgetCoinNode)
            self._widgetCoinNode = None
            self.draw()

    def move(self, newVecPos):
        """
        Move the object to the new location referenced by the 
        left-top corner of the object. Or the start of the line
        if it is a line.
        """
        self.resize(newVecPos[0], newVecPos[1])

    def getVertexStart(self):
        """Return the vertex of the start point"""
        return App.Vertex(self._vector[0])

    def getVertexEnd(self):
        """Return the vertex of the end point"""
        return App.Vertex(self.x+self.w, self.y+self.h, self.z+self.t)

    def show(self):
        self._visible = True
        self._wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all children
        self.redraw()
