# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the Design456 addon.

from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2025                                                    *
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
from ThreeDWidgets import fr_draw
from ThreeDWidgets import constant
from dataclasses import dataclass
from typing import List
from abc import abstractmethod

# ********************************************************************************************************
from dataclasses import dataclass

__updated__ = '2022-11-03 19:13:51'


@dataclass
class propertyValues:
    '''
    Property-holder class for drawing labels
    '''
    __slots__ = ['vectors', 'linewidth', 'fontName', 'fontsize',
                 'labelcolor', 'SetupRotation', 'rotation', 
                 'scale']
    # vectors: List[App.Vector]  # List[App.Vector] two vectors must be provided. 
    #                  # We cannot accept one vector as it will cause a huge problem.
    #                  # Some will require several vectors, and other just one.
    #                  # There is no way to avoid requiring more than 1 vector.
    # linewidth: int
    # fontName: str
    # fontsize: int
    # labelcolor: List[float]
    # SetupRotation: List[float]    # three angels in degree
    # rotation: List[float] # four float values - three axis and one angle 
    # scale: List[float]  # Three float numbers for scaling

    def __init__(self):
        self.vectors = [App.Vector(0, 0, 0), ]
        self.linewidth = 1
        self.fontName = 'sans'
        self.fontsize = 2
        self.labelcolor = constant.FR_COLOR.FR_BLACK
        self.rotation = [0.0, 0.0, 0.0, 0.0] # Normal rotation like you have in FreeCAD objects
        self.SetupRotation = [0.0, 0.0, 0.0] # degrees
        self.scale = [1.0, 1.0, 1.0]
# ***********************************************************************************************************


def defaultCallback(obj, userData = None):
    """
    Dummy callback. This should be overdriven to call the real callback
    """
    raise NotImplementedError()


class Fr_Widget (object):
    """
    Abstract Base class used to create all Widget.
    You need to subclass this object 
    to be able to create any widget,
    and you should always have a Fr_Group 
    widget which acts like a container for the widgets.
    fr_window widget will take care of that,
    events will be distributed by fr_window
    and it is a subclassed object from fr_group.
    fr_group doesn't need to be drawn, but 
    you can implement draw function
    """
    # Static Variables should be here 
    
    ########################################################################
    #  {w_callback_, w_lbl_calback_}  is a pointer to a function.          #
    #  It should be used only like that.                                   #
    #  Each widget has several callbacks, 'handle' will call them.         #
    #  Depending on what kind of widget you create, the callback can do    #
    #  different tasks. run do_callback, do_lblcallback,                   #
    #  w_move_callback, w_KB_Callback activates them.                      #
    # ######################################################################
    __slots__ =['w_vector',
                'w_label',
                'w_visible',
                'w_bkgColor',
                'w_color',
                'w_inactiveColor',
                'w_selColor',
                'w_box',
                'w_active',
                'w_parent',
                'w_widgetType',
                'w_hasFocus',
                'w_lbluserData',
                'w_pick_radius',
                'w_widgetSoNodes',
                'w_widgetlblSoNodes',
                'w_wdgsoSwitch',
                'w_when',
                'w_userData',
                'w_label',
                'w_lineWidth',
                'w_callback_',
                'w_lbl_calback_',
                'w_move_callback_',
                'w_KB_callback_'   ]

    def __init__(self, args: List[App.Vector] = [], label: str = [[]]):
        # All Class variables which are not static should be here
        # Look at 
        # https://stackoverflow.com/questions/9056957/correct-way-to-define-class-variables-in-python 
        
        self.w_vector = args    # List[App.Vector] two vectors must be provided. 
                                # We cannot accept one vector as it causes a huge problem.
                                # Some will require several vectors, and other just one.
                                # There is no way to avoid requiring more than 1 vector.
        # This must be a list, to have several raw, append st
        self.w_label = [[]]
        
        # Default values which is the same for new created objects.
        self.w_visible = 1      # 1 active, 0 inactive
        self.w_bkgColor = constant.FR_COLOR.FR_TRANSPARENCY
        self.w_color = constant.FR_COLOR.FR_BLACK
        self.w_inactiveColor = constant.FR_COLOR.FR_DIMGRAY
        self.w_selColor = constant.FR_COLOR.FR_YELLOW
        self.w_box = None
        self.w_active = 1  # 1 active , 0 inactive
        self.w_parent = None # Is the main window widget
        self.w_widgetType = constant.FR_WidgetType.FR_WIDGET
        self.w_hasFocus = 0           # 0 No focus , 1 Focus

        # Use this to send any object or value to the lbl drawing/callback(propertyValues object)
        self.w_lbluserData = None

        self.w_pick_radius = 5  # See if this must be a parameter in the GUI /Mariwan
        self.w_widgetSoNodes = None  # Should be defined in the widget either one or a list
        self.w_widgetlblSoNodes = None  # Should be defined in the widget either one or a list
        # each node is a child of one switch, Add drawings a children for this switch
        self.w_wdgsoSwitch = None
        self.w_when = constant.FR_WHEN.FR_WHEN_NEVER
        self.w_userData = None  # Use this to send any object or value to the callback
        self.w_label = label
        self.w_lineWidth = 1
        
        #             -  CALLBACK FUNCTIONS  -
        # Subclassed widget must create callback functions.
        self.w_callback_ = defaultCallback
        self.w_lbl_calback_ = defaultCallback  # Abstract class has no callback.
        self.w_move_callback_ = defaultCallback  # Abstract class has no callback.
        self.w_KB_callback_ = defaultCallback  # Abstract class has no callback.


    @abstractmethod
    def draw_box(self):
        raise NotImplementedError()

    @abstractmethod
    def draw(self):
        """ main draw function. This is responsible for all draw on screen"""
        raise NotImplementedError()

    @abstractmethod
    def draw_label(self):
        """ draw label for the widget 
        for coin3d Class SoText2 should be used 
        """
        raise NotImplementedError()

    def Font(self, newFont):
        self.w_lbluserData.fontName = newFont

    def FontSize(self, newSize):
        self.w_lbluserData.fontsize = newSize

    def setLblData(self, newData: propertyValues):
        self.w_lbluserData = newData

    def redraw(self):
        """
        After the widgets damages, this function should be called.        
        """
        if self.is_visible():
            # Remove the SoSwitch from fr_coinwindo
            self.w_parent.removeSoSwitchFromSceneGraph(self.w_wdgsoSwitch)

            # Remove the node from the switch as a child
            self.removeSoNodeFromSoSwitch()

            # Remove the sceneNodes from the widget
            self.removeSoNodes()
            # Redraw label

            self.lblRedraw()
            self.draw()

    def lblRedraw(self):
        if(self.w_widgetlblSoNodes is not None):
            self.w_widgetlblSoNodes.removeAllChildren()


    @abstractmethod
    def take_focus(self):
        """
        Set focus to the widget. Which should be redrawn also.
        """
        raise NotImplementedError()

    @abstractmethod
    def label_move(self, newPos):
        """ Move the label to a new location"""
        raise NotImplementedError()

    @abstractmethod
    def move(self, x, y, z):
        """ Move the widget to a new location.
        The new location is reference to the 
        left-upper corner"""
        raise NotImplementedError()

    @abstractmethod
    def move_centerOfMass(self, x, y, z):
        """ Move the widget to a new location.
        The new location is reference to the 
        center of mass"""
        raise NotImplementedError()

    # @property
    def has_focus(self):
        """
        Check if the widget has focus
        """
        return self.w_hasFocus

    @abstractmethod
    def remove_focus(self):
        """
        Remove the focus from the widget. 
        This happens by clicking anything 
        else than the widget itself
        """
        raise NotImplementedError()
    # Activated, deactivate, get status of widget

    # @property
    def is_visible(self):
        """ 
        return the internal variable which keeps
        the status of the widgets visibility
        """
        return self.w_visible

    @abstractmethod
    def activate(self):
        raise NotImplementedError()

    @abstractmethod
    def deactivate(self):
        """
        Deactivate the widget. which causes that no handle comes to the widget
        """
        raise NotImplementedError()

    def __del__(self):
        """
        This will remove the widget totally. 
        """
        print("fr_widget Destructor")
        self.hide()
        self.removeSoNodes()
        if self.w_parent is not None:
            # Parent should be the windows widget.
            self.w_parent.removeWidget(self)

    # @property
    def is_active(self):
        return self.w_active

    @abstractmethod
    def hide(self):
        """
            Hide the widget and its children
        """
        raise NotImplementedError()

    def show(self):
        """
            Show the widget and its children.
        """
        self.w_visible = 1
        self.draw()

    def getparent(self):
        """
            Get parent windows
        """
        return self.w_parent

    def parent(self, parent):
        """ 
            Set the parent to the widget
        """
        self.w_parent = parent

    @property
    def type(self):
        return self.w_widgetType

    @property
    def getPosition(self):
        """
        If args is defined, return the first point
        which is the first point in the widget
        """
        if len(self.w_vector) > 0:
            return (self.w_vector[0])
        return None

    @abstractmethod
    def position(self, x, y, z):
        """put the position of the object, which is reference to the first vector """
        raise NotImplementedError()

    @abstractmethod
    def resize(self, args: List[App.Vector]):  # Width, height, thickness
        raise NotImplementedError()

    def size(self, args: List[App.Vector]):
        raise NotImplementedError()

    # Take care of all events

    def handle(self, events):
        raise NotImplementedError()

    # callback related to t
    def do_lblcallback(self, userData):
        """
            This function will run the label-changed 
            event callback. 
            self.w_lbluserData: could be any object (for ex @dataclass, class, number, vectors ..etc)
        """
        try:
            if (self.w_lbl_calback_ is not None):
                self.w_lbl_calback_(self.w_lbluserData)

        except Exception as err:
            App.Console.PrintError("'lblcallback' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    # call the main callback for the widget
    def do_callback(self, userData):
        """
        This will activate the callback call. 
        Use this function to run the callback.
        This will be controlled by _when value
        This is implemented here but the callback
        should be implemented by the widget you create.
        self.w_userData: could be any object (for ex @dataclass, class, number, vectors ..etc)
        """
        try:
            if(self.w_callback_ is not None):
                self.w_callback_(self.w_userData)

        except Exception as err:
            App.Console.PrintError("'callback' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    # call the main callback for the widget

    def do_move_callback(self, userData):
        """
        This will activate the move-callback call. 
        Use this function to run the callback.
        This will be controlled by _when value
        This is implemented here but the callback
        should be implemented by the widget you subclass.
        self.w_userData: could be any object (for ex @dataclass, class, number, vectors ..etc)
        """
        try:
            if(self.w_move_callback_ is not None):
                self.w_move_callback_(self.w_userData)

        except Exception as err:
            App.Console.PrintError("'move callback' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Color(self, color):
        """ Foreground color at normal status"""
        self.w_color = color

    def SelectionColor(self, color):
        """ Foreground color when widget selected i.e. has focus"""
        self.w_selColor = color

    def InActiveColor(self, color):
        """ Foreground color when widget is disabled - not active """
        self.w_inactiveColor = color

    def BkgColor(self, color):
        """ Background color . To disable background color use FR_COLOR.FR_TRANSPARENCY which is the default """
        self.w_bkgColor = color

    def When(self, value):
        """
        When do the callback should be run?
        values are in constant.Fr_When
        """
        self.w_when = value

    @property
    def getWhen(self):
        """"
        Internal value of when. This will decide when the widget-callback will happen.
        """
        return self.w_when

    def saveSoNodesToWidget(self, _Value):
        """ Keep sceneNodes in the fr_xxx object in the w_widgetSoNodes variable """
        if type(_Value)== list:
            self.w_widgetSoNodes = coin.SoSeparator()
            for obj in _Value:
                self.w_widgetSoNodes.addChild(obj)
        else:
            self.w_widgetSoNodes = _Value

    def saveSoNodeslblToWidget(self, _Value):
        """ Keep the Label sceneNodes in the fr_xxx object in the w_widgetlblSoNodes variable"""
        if type(_Value) == list:
            self.w_widgetlblSoNodes = coin.SoSeparator()
            for obj in _Value:
                self.w_widgetlblSoNodes.addChild(obj)
        else:
            self.w_widgetlblSoNodes = _Value
   
    # todo: Do we need an argument here? as we should add w_widgetSoNodes and w_widgetlblSoNodes
    def addSoNodeToSoSwitch(self, listOfSoSeparator):
        """ add all small sosseparator which holds widgets drawings, color, linewidth ..etc
        to the switch. The switch should be able to show/hide them by a command
        """
        try:
            if self.w_wdgsoSwitch is None:
                self.w_wdgsoSwitch = coin.SoSwitch()
                self.w_wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all
            # We might have a list inside the widget
            if type(listOfSoSeparator) == list:
                for sub in listOfSoSeparator:
                    if type(sub) == list:
                        # we have many SoSeparator inside the widget
                        for subSub in sub:
                            self.w_wdgsoSwitch.addChild(subSub)
                    else:
                        self.w_wdgsoSwitch.addChild(sub)
            else:
                self.w_wdgsoSwitch.addChild(listOfSoSeparator)
            if self.w_parent is None:
                raise ValueError("parent was none")
            # Add the switch to the SceneGraph
            self.w_parent.addSoSwitchToSceneGraph(self.w_wdgsoSwitch)
            
        except Exception as err:
            App.Console.PrintError("'Fr_Widget addSoNodeToSoSwitch' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def removeSoNodes(self):
        """ Remove CoinNodes and their children """
        try:
            if self.w_widgetSoNodes is not None:
                if type(self.w_widgetSoNodes) == list:
                    for so in self.w_widgetSoNodes:
                        so.removeAllChildren()
                        del so
                else:
                    self.w_widgetSoNodes.removeAllChildren()
                    del self.w_widgetSoNodes
            if self.w_widgetlblSoNodes is not None:
                if type(self.w_widgetlblSoNodes) == list:
                    for so in self.w_widgetlblSoNodes:
                        so.removeAllChildren()
                        del so
                else:
                    self.w_widgetlblSoNodes.removeAllChildren()
                    del self.w_widgetlblSoNodes

            self.w_widgetSoNodes = None
            self.w_widgetlblSoNodes = None

        except Exception as err:
            App.Console.PrintError("'Remove SceneNodes' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def removeSoNodeFromSoSwitch(self):
        """
            Remove the children from the widget COIN3D node which is the soseparators
            i.e. all drawing, color ..etc for the widget 
        """
        if self.w_wdgsoSwitch is not None:
            self.w_wdgsoSwitch.removeAllChildren()

    def removeSoSwitch(self):
        if self.w_wdgsoSwitch is not None:
            try:
                del self.w_wdgsoSwitch
            except:
                pass  # must be already removed .. don't care
        self.w_wdgsoSwitch = None

    def changeLabelstr(self, newlabel: str = ""):
        self.w_label = [newlabel,]

    def changeLabelfloat(self, newlabel: float = 0.0):
        self.w_label = ["{:.2f}".format(newlabel)]

    def getWidgetsCenter(self, SoseparatorToCheck=None):
        """[Get Center of the Widget]

        Returns:
            [App.Vector]: [Return a vector represents the centor of the widget]
        """
        try:
            if SoseparatorToCheck is None:
                boundary = self.getWidgetsBoundary(self.w_wdgsoSwitch)
            else:
                boundary = self.getWidgetsBoundary(SoseparatorToCheck)

            center = App.Vector((boundary[0].x+boundary[1].x)/2,
                                (boundary[0].y+boundary[1].y)/2,
                                (boundary[0].z+boundary[1].z)/2)
            
            return center

        except Exception as err:
            App.Console.PrintError("'getWidgetsCenter' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def getWidgetsBoundary(self, SoseparatorToCheck=None):
        """[Retrieve the Max size of the 3D coin object by returning the Min vector and Max vector]

        Returns:
            [Tuple]: [Two vectors first is for the Min Boundary, second is for the Max Boundary]
        """
        try:
            viewPort = coin.SbViewportRegion()
            BoundaryAction = coin.SoGetBoundingBoxAction(viewPort)
            if(SoseparatorToCheck is None):
                BoundaryAction.apply(self.w_wdgsoSwitch)
            else:
                BoundaryAction.apply(SoseparatorToCheck)
            
            Boundary = BoundaryAction.getBoundingBox()
            BoundMax = Boundary.getMax()
            BoundMin = Boundary.getMin()
            return ([App.Vector(round(BoundMin[0],1), 
                                round(BoundMin[1],1), 
                                round(BoundMin[2],1)),
                    App.Vector(round(BoundMax[0],1), 
                               round(BoundMax[1],1), 
                               round(BoundMax[2],1))])
        except Exception as err:
            App.Console.PrintError("'getWidgetsBoundary' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
