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
import fr_draw
import constant
from dataclasses import dataclass
from typing import List


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

    def __init__(self, args: List[App.Vector] = [], label: str = ""):
        """ 
        Default values which is shared with all objects.

        """
        self._vector = args        # This should be like App.vectors
        self._label = [label]      # This must be a list, to have several raw, append str
        self._lblPosition=None     # Should be defined when lbl is created. 
        self._visible = True
        self._bkgColor = constant.FR_COLOR.FR_TRANSPARENCY
        self._color = constant.FR_COLOR.FR_BLACK
        self._inactiveColor = constant.FR_COLOR.FR_GRAY2
        self._selColor = constant.FR_COLOR.FR_YELLOW
        self._lblColor= constant.FR_COLOR.FR_BLACK
        self._box = None
        self._active = True
        self._parent = None
        self._widgetType = constant.FR_WidgetType.FR_WIDGET
        self._hasFocus = False
        self._font='sans'
        self._fontsize=8
        self._pick_radius = 5  # See if this must be a parameter in the GUI /Mariwan
        self._widgetCoinNode = None     #Should be defined in the widget either one or a list
        self._widgetlblCoinNode = None  #Should be defined in the widget either one or a list
        self._wdgsolblSwitch=coin.SoSwitch()
        # each node is a child of one switch, Add drawings a children for this switch
        self._wdgsoSwitch = coin.SoSwitch()        
        self._wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all
        self._wdgsolblSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all
        self._when = constant.FR_WHEN.FR_WHEN_NEVER
        self._userData = None

    def draw_box(self):
        raise NotImplementedError()

    def draw(self):
        """ main draw function. This is responsible for all draw on screen"""
        raise NotImplementedError()

    def draw_label(self):
        """ draw label for the widget 
        for coin3d Class SoText2 should be used 
        """
        raise NotImplementedError()
    
    def Font(self, newFont):
        self._font=newFont
        
    def FontSize(self,newSize):
        self._fontsize=newSize
        
    def redraw(self):
        """
        After the widgets damages, this function should be called.        
        """
        raise NotImplementedError()

    def take_focus(self):
        """
        Set focus to the widget. Which should redraw it also.
        """
        raise NotImplementedError()
    
    def label_move(self,newPos):
        """ Move the label to a new location"""    
        raise NotImplementedError()
    
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
        return self._hasFocus

    def remove_focus(self):
        """
        Remove the focus from the widget. 
        This happens by clicking anything 
        else than the widget itself
        """
        raise NotImplementedError()
    # Activated, deactivate, get status of widget

    def is_visible(self):
        """ 
        return the internal variable which keep 
        the status of the widgets visibility
        """
        return self._visible

    def activate(self):
        raise NotImplementedError()

    def deactivate(self):
        """
        Deactivate the widget. which causes that no handle comes to the widget
        """
        raise NotImplementedError()

    def destructor(self):
        """
        This will remove the widget totally. 
        """
        self.removeSeneNodes()

    def is_active(self):
        return self._active

    def hide(self):
        raise NotImplementedError()

    def show(self):
        self.draw()

    def getparent(self):
        return self._parent

    def parent(self, parent):
        self._parent = parent

    def type(self):
        return self._widgetType

    def getPosition(self):
        """
        If args is defined, return the first point
        which is the first point in the widget
        """
        if len(self._vector) > 0:
            return (self._vector[0])
        return None

    def getPositionAsVertex(self):
        """
        if args is defined, return the vertex of the 
        first point in the widget
        """
        if(self.getPosition()):
            return App.Vertex(self._vector[0])
        else:
            return None

    def position(self, x, y, z):
        """put the position of the object, Reference to the first vector """
        raise NotImplementedError()

    def resize(self, args: List[App.Vector]):  # Width, height, thickness
        raise NotImplementedError()

    def size(self, args: List[App.Vector]):
        NotImplementedError()

    # Take care of all events
    def handle(self, events):
        raise NotImplementedError()
        
    def callback_labelChanged(self,data):
        """ This callback will be used 
            to run code that will be 
            related to the label change.
            Often it is not necessary,
            but if the object is 
            type Input_box. At that
            time you need a callback
            mechanism. This is for that.
            """
        pass

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
        pass  # Subclassed widget must create callback function. Abstract class has no callback
        #raise NotImplementedError()

    # call the main callback for the widget
    def do_callback(self, data):
        """
        This will activate the callback call. 
        Use this function to run the callback.
        This will be controlled by _when value
        This is implemented here but the callback
        should be implemented by the widget you create
        """
        self.callback(data)

    def Color(self, color):
        """ Foreground color at normal status"""
        self._color = color

    def SelectionColor(self, color):
        """ Foreground color when widget selected i.e. has focus"""
        self._selCol = color

    def InActiveColor(self, color):
        """ Foreground color when widget is disabled - not active """
        self._inactiveCol = color

    def BkgColor(self, color):
        """ Background color . To disable background color use FR_COLOR.FR_TRANSPARENCY which is the default """
        self._bkgColor = color

    def When(self, value):
        """
        When do the callback should be run?
        values are in constant.Fr_When
        """
        self._when = value

    def getWhen(self):
        """"
        Internal value of when. This will decide when the widget-callback will happen.
        """
        return self._when
    
    def addSenelblNodes(self,_list):
        if type(_list)==list:
            for i in _list:
                self._wdgsolblSwitch.addChild(i)
        else:
            self._wdgsolblSwitch.addChild(_list)
        self._widgetCoinNode=list
        self.addSoNodeToSoSwitch(list)
    
    def addSeneNodes(self,_list):
        if type(_list)==list:
            for i in _list:
                self._wdgsoSwitch.addChild(i)
        else:
            self._wdgsoSwitch.addChild(_list)
        self._widgetCoinNode=list
        self.addSoNodeToSoSwitch(list)
        
    def removeSeneNodes(self):
        """ Remove SeneNodes children and itself"""
        if len(self._widgetCoinNode)!=0:
            for i in self._widgetCoinNode: 
                del i 
        if len(self._widgetlblCoinNode)!=0:
            for i in self._widgetlblCoinNode: 
                del i 

    def addSoNodeToSoSwitch(self, listOfSoSeparator):
        """ add all small sosseparator which holds widgets drawings, color, linewidth ..etc
        to the switch. The switch should be able to hide/visible them by a command
        """
        if type(listOfSoSeparator)==list:
            for i in listOfSoSeparator:
                self._wdgsoSwitch.addChild(i)
        else:
            self._wdgsoSwitch.addChild(listOfSoSeparator)
            
        # Add the switch to the SeneGrap
        self._parent.addSoSwitchToSeneGraph(self._wdgsoSwitch)

    def removeSoNodeFromSoSwitch(self):
        """
            Remove the children from the widgetCOINnode which is the soseparators
            i.e. all drawing, color ..etc for the widget 
        """
        self._wdgsoSwitch.removeAllChildren()
        
    def addSoNodelblToSoSwitch(self,listOfSoSeparator):
        """ add all small sosseparator which holds widgets lable, color,  ..etc
        to the switch. The switch should be able to hide/visible them by a command
        """
        if type(listOfSoSeparator)==list:
            for i in listOfSoSeparator:
                self._wdgsolblSwitch.addChild(i)
        else:
            self._wdgsolblSwitch.addChild(listOfSoSeparator)
        self._parent.addSoSwitchToSeneGraph(self._wdgsolblSwitch)

    def removeSolblNodeFromSoSwitch(self):
        """
            Remove the children from the widgetCOINnode which is the soseparators
            i.e. all drawing, color ..etc for the widget 
        """
        self._wdgsolblSwitch.removeAllChildren()
        
    
#********************************************************************************************************
from dataclasses import dataclass

@dataclass
class point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0


#List of points which should be used everywhere 
VECTOR = List[point]

class propertyValues:
    '''
    Property-holder  class for drawing labels
    ''' 
    __slots__ = ['vectors','linewidth','labelfont','fontsize','labelcolor','alignment']
    vectors   : VECTOR        #List[App.Vector]
    linewidth : int 
    labelfont : str
    fontsize  : int
    labelcolor: tuple
    alignment : int                   
    '''
    from dataclasses import dataclass


    @dataclass
    class Point:
    x: float
    y: float
    z: float = 0.0
    '''