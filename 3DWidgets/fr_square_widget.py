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
import fr_coin3d
from typing import List
import fr_line_widget
import FACE_D as faced
import fr_widget

class Fr_SquareFrame_Widget(fr_widget.Fr_Widget):
    """
    This class is for drawing a line in  coin3D
    """
    # def __init__(self, args:fr_widget.VECTOR=[],l=""):
    def __init__(self, args: List[App.Vector] = [], label:List[str]=[] ,lineWidth=1):
        if args == None:
            args = []
        self._lineWidth = lineWidth # default line width        # Here we have a list (4 labels)
        self._EdgeSection: List[fr_line_widget.Fr_Line_Widget]=[]
        if type(label)!=List:
            templabel=label
            label=[]
            for i in range(0,3):
                label.append(templabel)
                    
        for i in range(0,3):
            nextI=i+1
            #We have four sections.
            if(i==3):
                nextI=0 
            self._EdgeSection.append(fr_line_widget.Fr_Line_Widget( [args[i],args[nextI]], label[i],lineWidth))

        super().__init__(args, label)
        
    def addVertices(self, vertices):
        if(len(vertices)!=4):
                # must be four vertices
                errMessage = "Four Vertices are required"
                faced.getInfo(None).errorDialog(errMessage)
                return
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
        for i in range(0,3):
            self._EdgeSection[0].handle(event)


    def draw(self):
        """
        Main draw function. It is responsible to create the node,
        and draw the line on the screen. It creates a node for 
        the line.
        """
        print(self._label)
        print(self._vector)
        self._widgetType = constant.FR_WidgetType.FR_SQUARE_FRAME
        for i in range(0,3):
            self._EdgeSection[0].draw()

    def show(self):
        self._visible = True
        self._wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all children
        self.redraw()

    def redraw(self):
        """
        After the widgets damages, this function should be called.        
        """
        for i in range(0,3):
            self._EdgeSection[0].redraw()

    def take_focus(self):
        """
        Set focus to the widget. Which should redraw it also.
        """
        if self._hasFocus == True:
            return  # nothing to do here
        for i in range(0,3):
            self._EdgeSection[0].take_focus()
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
        self.redraw()

    def destructor(self):
        """
        This will remove the widget totally. 
        """
        for i in range(0,3):
           self._EdgeSection[0].removeSeneNodes()

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
        if(len(args)!=4):
            # must be four vertices
            errMessage = "Four Vertices are required"
            faced.getInfo(None).errorDialog(errMessage)
            return
        self._vector = args
        self.redraw()

    def size(self, args: List[App.Vector]):
        """Resize the widget by using the new vectors"""
        if(len(args)!=4):
            # must be four vertices
            errMessage = "Four Vertices are required"
            faced.getInfo(None).errorDialog(errMessage)
            return
        self.resize(args)
        
    def move(self, newVecPos):
        """
        Move the object to the new location referenced by the 
        left-top corner of the object. Or the start of the line
        if it is a line.
        """
        if(len(newVecPos)!=4):
            # must be four vertices
            errMessage = "Four Vertices are required"
            faced.getInfo(None).errorDialog(errMessage)
            return
        self.resize(newVecPos)
