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

class Fr_SquareFrame_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a line in  coin3D
    """
    global _lineWidth

    def __init__(self, args:fr_widget.VECTOR=[],l=""):
        if args==None:
            args=[]
        self.WidgetType = constant.FR_WidgetType.FR_EDGE
        self._lineWidth = 1  # default line width
        super().__init__(args,l)

    def addVertices(self, vertices):
        self.vertices.clear()
        self.vertices = vertices

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
        if self.parent.link_to_root_handle.lastEvent == constant.FR_EVENTS.MOUSE_LEFT_PUSH:
            clickedNode = fr_coin3d.objectMouseClick_Coin3d(
                self.parent.link_to_root_handle.lastEventXYZ.pos, self.pick_radius)
            find = False
            for i in self.WidgetCoinNode:
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
        if len(self._vector) < 4:
            raise ValueError('Vertices must be 4')
        if self.active() and self.has_focus():
            usedColor = self.selCol
        elif self.active() and (self.has_focus() != 1):
            usedColor = self.activeCol
        elif self.active() != 1:
            usedColor = self.inactiveCol
        if self.is_visible():
            self.WidgetCoinNode.append(fr_draw.draw_line(self_vector[0], self_vector[1], usedColor, self.lineWidth))
            self.WidgetCoinNode.append(fr_draw.draw_line(self_vector[1], self_vector[2], usedColor, self.lineWidth))
            self.WidgetCoinNode.append(fr_draw.draw_line(self_vector[2], self_vector[3], usedColor, self.lineWidth))
            self.WidgetCoinNode.append(fr_draw.draw_line(self_vector[3], self_vector[0], usedColor, self.lineWidth))

            self.parent.addSeneNode(self.WidgetCoinNode[0])
            self.parent.addSeneNode(self.WidgetCoinNode[1])
            self.parent.addSeneNode(self.WidgetCoinNode[2])
            self.parent.addSeneNode(self.WidgetCoinNode[3])

        else:
            return  # We draw nothing .. This is here just for clarity of the code

    def redraw(self):
        """ When drawing damages, a redraw must be done.
        This function will redraw the widget on the 3D
        Scene"""
        for i in self.WidgetCoinNode:
            self.parent.removeSeneNode(i)
        self.WidgetCoinNode = None
        self.draw()

    def move(self, newVector):
        """
        Move the object to the new location referenced by the 
        left-top corner of the object. Or the start of the line
        if it is a line.
        """
        self.resize(newVector)
