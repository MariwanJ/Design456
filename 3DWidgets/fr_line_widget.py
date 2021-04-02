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

import os,sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import Design456Init
import fr_draw
import fr_widget
import constant


class Fr_Line_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a line in  coin3D
    """

    def __init__(self, x, y, z, w, h, t, l=""):
        self.WidgetType = constant.FR_WidgetType.FR_EDGE
        super().__init__(x, y, z, w, h, t, l)

    def handle(self, event):
        """
        This function is responsbile of taking events and processing 
        the actions required. If the object is not targeted, 
        the function will skip the events. But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. Window object is responsible for distributing the events.
        """
        if self.parent.lastEvent == constant.FR_EVENTS.MOUSE_LEFT_PUSH:
            clickedNode = fr.objectCMouse_Coin3d(self.parent.lastEventXYZ.pos).getEditNode()
            find = False
            for i in self.WidgetCoinNode:
                if i == None or clickedNode == None:
                    break
                if i.getClassTypeId() == clickedNode.getClassTypeId():
                    find = True
                    break  # We don't need to search more
            if find == True:
                self.take_focus()
                return 1
            else:
                self.remove_focus()
                return event # We couldn't use the event .. so return the event itself

    def draw(self):
        """
        Main draw function. It is responsible to create the node,
        and draw the line on the screen. It creates a node for 
        the line.
        """
        p1 = (self.x, self.y, self.z)
        p2 = (self.x+self.w, self.y+self.h, self.z+self.t)
        self.color1 = constant.FR_COLOR.FR_GREEN
        self.color2 = constant.FR_COLOR.FR_YELLOW  # Focus
        LineWidth = 4
        if self.has_focus():
            self.WidgetCoinNode = fr_draw.draw_line(
                p1, p2, self.color1, LineWidth)
        else:
            self.WidgetCoinNode = fr_draw.draw_line(
                p1, p2, self.color2, LineWidth)
        self.parent.addSeneNode(self.WidgetCoinNode)

    def redraw(self):
        """ When drawing damages, a redraw must be done.
        This function will redraw the widget on the 3D
        Scene"""
        
        self.parent.removeSeneNode(self.WidgetCoinNode)
        self.WidgetCoinNode = None
        self.draw()

    def move(self, x, y, z):
        """
        Move the object to the new location referenced by the 
        left-top corner of the object. Or the start of the line
        if it is a line.
        """
        self.resize(x, y, z, self.w, self.h, self.t)

    def getVertexStart(self):
        """Return the vertex of the start point"""
        return App.Vertex(self.x, self.y, self.z)

    def getVertexEnd(self):
        """Return the vertex of the end point"""
        return App.Vertex(self.x+self.w, self.y+self.h, self.z+self.t)
