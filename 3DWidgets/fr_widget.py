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

"""
This class is the base class for all widgets created in coin3D

"""
import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import Design456Init
import Draft as _draft
import fr_draw
import constant


class Fr_Widget (object):
    """
    Abstract Base class used to create all Widgets
    You need to subclass this object 
    to be able to create other objects,
    and you should always have a Fr_Group 
    widget which acts like a container for the widgets.
    fr_window widget will take care of that,
    events will be distributed by fr_window
    and it is a subclassed object from fr_group.
    fr_group doesn't need to be drawn, but 
    you can implement draw function
    """
    import FreeCAD as App
    global _vector
    global l
    global WidgetCoinNode  # This is for the children or the widget itself
    global visible
    global bkgColor  # Background color
    global activeColor  # When widget not selected (normal)
    global selColor  # When widget is selected
    global inactiveColor  # Inactive widget.
    global box
    global active
    global parent
    global WidgetType
    global hasFocus
    global wdgsoSwitch
    global pick_radius
    global when_

    # Coin SoSeparator (node)
    VECTOR = list[App.Base.Vector]
    def __init__(self, args:VECTOR=None,l=""):
        if args==None : 
            args=[]
        self._vector=args       # This should be like App.vectors 
        self.l = l       
        self.WidgetCoinNode = coin.SoSeparator
        self.visible = True
        self.bkgColor = constant.FR_COLOR.FR_TRANSPARENCY
        self.activeCol = constant.FR_COLOR.FR_GRAY0
        self.inactiveCol = constant.FR_COLOR.FR_GRAY2
        self.selCol = constant.FR_COLOR.FR_BLACK
        self.box = None
        self.active = True
        self.parent = None
        self.WidgetType = constant.FR_WidgetType.FR_WIDGET
        self.hasFocus = False
        self.wdgsoSwitch = coin.SoSwitch()
        self.pick_radius = 3  # See if this must be a parameter in the GUI /Mariwan
        self.wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all
        self.when_ = constant.Fr_When.FR_WHEN_NEVER

    def draw_box(self):
        raise NotImplementedError()

    def draw():
        """ main draw function. This is responsible for all draw on screen"""
        raise NotImplementedError()

    def draw_label():
        """ draw label for the widget 
        for coin3d Class SoText2 should be used 
        """
        raise NotImplementedError()

    def redraw(self):
        """
        After the widgets damages, this function should be called.        
        """
        raise NotImplementedError()

    def take_focus(self):
        """
        Set focus to the widget. Which should redraw it also.
        """
        if self.has_focus == True:
            return  # nothing to do here
        self.hasFocus = True
        self.redraw()

    def move(self, x, y, z):
        """ Move the widget to a new location.
        The new location is reference to the 
        left-upper corner"""
        raise NotImplementedError()

    def move_centerOfMass(self, x, y, z):
        """ Move the widget to a new location.
        The new location is reference to the 
        center of mass"""
        raise NotImplementedError()

    def has_focus(self):
        """
        Check if the widget has focus
        """
        return self.hasFocus

    def remove_focus(self):
        """
        Remove the focus from the widget. 
        This happend by clicking anything 
        else than the widget itself
        """
        if self.hasFocus == False:
            return  # nothing to do
        else:
            self.hasFocus = False
            self.redraw()

    # Activate, deactivate, get status of widget
    def is_visible(self):
        """ 
        return the internal variable which keep 
        the status of the widgets visibility
        """
        return self.visible

    def activate(self):
        if self.active:
            return  # nothing to do
        self.active = True
        self.redraw()

    def deactivate(self):
        """
        Deactivate the widget. which causes that no handle comes to the widget
        """
        if self.active == False:
            return  # Nothing to do
        self.active = False

    def destructor(self):
        """
        This will remove the widget totally. 
        """

    def is_active(self):
        return self.active

    def hide():
        if self.visible == False:
            return  # nothing to do
        self.visible = False
        self.wdgsoSwitch.whichChild = coin.SO_SWITCH_NONE  # hide all children
        self.redraw()

    def show(self):
        self.visible = True
        self.wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all children
        self.redraw()

    def parent(self):
        return self.parent

    def parent(self, parent):
        self.parent = parent

    def type(self):
        return self.type

    def getPosition(self):
        return (x, y, z)

    def getPositionAsVertex(self):
        return App.Vertex(x, y, z)

    def position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def resize(self,args:VECTOR):  # Width, height, thickness
        self._vector=args
        self.redraw()

    def size(self, args:VECTOR):
        self.resize(args)

    # Take care of all events
    def handle(self, events):
        raise NotImplementedError()

    # Callbacks
    def callback(self, data):
        """ Each widget has a single callback.
            But you can add as many call back as you 
            want if you sub class any widget
            and at the handle you call them.
            Depending on what kind of widget
            you make, this callback could 
            be used there. run do_callback 
            to activate this.
        """
        raise NotImplementedError()

    # call the main callback for the widget
    def do_callback(self, data):
        """
        This will activate the callback. 
        Use this function to run the callback.
        This is implemented here but the callback
        should be implemented by the widget you create
        """
        self.callback(data)

    def ActiveColor(self, color):
        """ Foreground color at normal status"""
        self.activeCol = color

    def SelectionColor(self, color):
        """ Foreground color when widget selected i.e. has focus"""
        self.selCol = color

    def InActiveColor(self, color):
        """ Foreground color when widget is disabled - not active """
        self.inactiveCol = color

    def InActiveColor(self, color):
        """ Background color . To disable background color use FR_COLOR.FR_TRANSPARENCY which is the default """
        self.inactiveCol = color

    def When(self, value):
        """
        When do the callback should be run?
        values are in constant.Fr_When
        """
        self.when = value

    def When(self):
        """"
        Internal value of when
        """
        return self.when
