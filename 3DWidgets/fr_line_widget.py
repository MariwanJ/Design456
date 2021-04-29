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
import fr_label_draw
from constant import FR_ALIGN

"""
Example how to use this widget. 

import fr_coinwindow as wn
import fr_line_widget as line
import FreeCAD as App
g=[]
p1=App.Vector(10,1,0)     # first point in the line and for the windows
p2=App.Vector(20,20,0)   # Second point in the line 
wny=wn.Fr_CoinWindow()  # Create the window, label has no effect at the moment
g.append(p1)
g.append(p2)
ln =line.Fr_Line_Widget(g,"My label",7)   # draw the line - nothing will be visible yet
wny.addWidget(ln)              # Add it to the window as a child 
wny.show()                    # show the window and it's widgets. 


"""


class Fr_Line_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a line in coin3D world
    """

    def __init__(self, _vectors: List[App.Vector] = [], label: str = "", lineWidth=1):
        self._lineWidth = lineWidth  # Default line width
        super().__init__(_vectors, label)

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
        if self._parent.link_to_root_handle._lastEvent == constant.FR_EVENTS.FR_MOUSE_LEFT_PUSH:
            clickedNode = fr_coin3d.objectMouseClick_Coin3d(
                self._parent.link_to_root_handle._lastEventXYZ.pos, self._pick_radius)

            if self._wdgsoSwitch.findChild(clickedNode) != -1:
                self.take_focus()
                self.do_callback(self._userData)
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
        try:
            self._widgetType = constant.FR_WidgetType.FR_EDGE
            if len(self._vector) < 2:
                raise ValueError('Must be 2 Vectors')
            p1 = self._vector[0]
            p2 = self._vector[1]

            if self.is_active() and self.has_focus():
                usedColor = self._selColor
            elif self.is_active() and (self.has_focus() != 1):
                usedColor = self._color
            elif self.is_active() != 1:
                usedColor = self._inactiveColor
            if self.is_visible():
                linedraw =fr_draw.draw_line(p1, p2, usedColor, self._lineWidth)
                _lbl=self.draw_label()
                #self._parent.addSoNodeToSoSwitch(_lbl)
                # put the node inside the switch
                self.addSeneNodes(linedraw)  # Add SoSeparator
                # Add SoSeparator as child to Switch
                self.addSoNodeToSoSwitch(_lbl)
                self.addSoNodeToSoSwitch(self._widgetCoinNode)
                # Add the switch to the SeneGrap
                self._parent.addSoSwitchToSeneGraph(self._wdgsoSwitch)
                #self._parent.addSoSwitchToSeneGraph(_lbl)
            else:
                return  # We draw nothing .. This is here just for clarifying the code
        except Exception as err:
            App.Console.PrintError("'Fr_Line_Widget' Failed. "
                                       "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        
    def draw_label(self):
        LabelData=fr_widget.propertyValues()
        LabelData.linewidth=self._lineWidth
        LabelData.labelfont=self._font
        LabelData.fontsize=self._fontsize
        LabelData.labelcolor=self._lblColor
        LabelData.vectors=self._vector
        LabelData.alignment=FR_ALIGN.FR_ALIGN_LEFT_BOTTOM
        lbl=fr_label_draw.draw_label(self._label,LabelData)
        return lbl
        
    
    def move(self, newVecPos):
        """
        Move the object to the new location referenced by the 
        left-top corner of the object. Or the start of the line
        if it is a line.
        """
        self.resize([newVecPos[0], newVecPos[1]])

    def getVertexStart(self):
        """Return the vertex of the start point"""
        return App.Vertex(self._vector[0])

    def getVertexEnd(self):
        """Return the vertex of the end point"""
        return App.Vertex(self._vector[1])

    def show(self):
        self._visible = True
        self._wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all children
        self.redraw()

    def redraw(self):
        """
        After the widgets damages, this function should be called.        
        """
        if self.is_visible():
            # Remove the seneNodes from the widget
            self.removeSeneNodes()
            # Remove the node from the switch as a child
            self.removeSoNodeFromSoSwitch()
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

    def resize(self, vectors: List[App.Vector]):  # Width, height, thickness
        """Resize the widget by using the new vectors"""
        self._vector = vectors
        self.redraw()

    def size(self, vectors: List[App.Vector]):
        """Resize the widget by using the new vectors"""
        self.resize(vectors)
        
    def label_move(self,newPos):
        pass
 