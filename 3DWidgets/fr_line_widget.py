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
from constant import FR_EVENTS
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
        self.lineWidth = lineWidth  # Default line width
        self.widgetType = constant.FR_WidgetType.FR_EDGE
        super(Fr_Line_Widget,self).__init__(_vectors, label)
    
    #Getter method for lineWidth
    @property
    def lineWidth(self):
        return self.lineWidth
    
    #Setter method for lineWidth
    @lineWidth.setter 
    def lineWidth(self, width):
        """ Set the line width"""
        self.lineWidth = width
    
    def handle(self, event):
        """
        This function is responsbile of taking events and processing 
        the actions required. If the object is not targeted, 
        the function will skip the events. But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. Window object is responsible for distributing the events.
        """
        if self.parent.link_to_root_handle.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_PUSH:
            clickwdgdNode = fr_coin3d.objectMouseClick_Coin3d(
                self.parent.link_to_root_handle.w_lastEventXYZ.pos, self.pick_radius, self.widgetCoinNode)
            clickwdglblNode = fr_coin3d.objectMouseClick_Coin3d(
                self.parent.link_to_root_handle.w_lastEventXYZ.pos, self.pick_radius, self.widgetlblCoinNode)

            if clickwdgdNode != None or clickwdglblNode != None:
                self.take_focus()
                self.do_callback(self.userData)
                return 1
            else:
                self.remove_focus()
                return event  # We couldn't use the event .. so return the event itself

        if self.parent.link_to_root_handle.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK:
            # Double click event.
            print("Double click detected")
            

    def draw(self):
        """
        Main draw function. It is responsible to create the node,
        and draw the line on the screen. It creates a node for 
        the line.
        """
        try:
            
            if len(self.vectors) < 2:
                raise ValueError('Must be 2 Vectors')
            p1 = self.vectors[0]
            p2 = self.vectors[1]

            if self.has_focus:
                usedColor = self.w_selColor
            elif self.is_active and (self.has_focus != 1):
                usedColor = self.w_color
            elif self.is_active != 1:
                usedColor = self.w_inactiveColor
            if self.is_visible():
                linedraw = fr_draw.draw_line(p1, p2, usedColor, self.lineWidth)
                _lbl = self.draw_label()

                self.addSeneNodeslbl(_lbl)
                self.addSeneNodes(linedraw)  # Add SoSeparator. Will be added to switch automatically                            
            else:
                return  # We draw nothing .. This is here just for clarifying the code

        except Exception as err:
            App.Console.PrintError("'Fr_Line_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_label(self):
        LabelData = fr_widget.propertyValues()
        LabelData.linewidth = self.lineWidth
        LabelData.labelfont = self.font
        LabelData.fontsize = self.fontsize
        LabelData.labelcolor = self.w_lblColor
        LabelData.vectors = self.vectors
        LabelData.alignment = FR_ALIGN.FR_ALIGN_LEFT_BOTTOM
        lbl = fr_label_draw.draw_label(self.label, LabelData)
        self.widgetlblCoinNode = lbl
        return lbl

    def move(self, newVecPos):
        """
        Move the object to the new location referenced by the 
        left-top corner of the object. Or the start of the line
        if it is a line.
        """
        self.resize([newVecPos[0], newVecPos[1]])

    @property
    def getVertexStart(self):
        """Return the vertex of the start point"""
        return App.Vertex(self.vectors[0])
    
    @property
    def getVertexEnd(self):
        """Return the vertex of the end point"""
        return App.Vertex(self.vectors[1])

    def show(self):
        self.is_visible = True
        self.wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all children
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
            self.parent.removeSoSwitch(self.wdgsoSwitch)
            self.draw()

    def take_focus(self):
        """
        Set focus to the widget. Which should redraw it also.
        """
        if self.has_focus == True:
            return  # nothing to do here
        self.has_focus = True
        self.redraw()

    def activate(self):
        if self.is_active:
            return  # nothing to do
        self.is_active = True
        self.redraw()

    def deactivate(self):
        """
        Deactivate the widget. which causes that no handle comes to the widget
        """
        if self.is_active == False:
            return  # Nothing to do
        self.is_active = False

    def destructor(self):
        """
        This will remove the widget totally. 
        """
        self.removeSeneNodes()
        
    @property
    def is_active(self):
        return self.is_active

    def hide(self):
        if self.is_visible == False:
            return  # nothing to do
        self.is_visible = False
        self.wdgsoSwitch.whichChild = coin.SO_SWITCH_NONE  # hide all children
        self.redraw()

    def remove_focus(self):
        """
        Remove the focus from the widget. 
        This happens by clicking anything 
        else than the widget itself
        """
        if self.has_focus == False:
            return  # nothing to do
        else:
            self.has_focus = False
            self.redraw()

    def resize(self, vectors: List[App.Vector]):  # Width, height, thickness
        """Resize the widget by using the new vectors"""
        self.vectors = vectors
        self.redraw()

    def size(self, vectors: List[App.Vector]):
        """Resize the widget by using the new vectors"""
        self.resize(vectors)

    def label_move(self, newPos):
        pass
