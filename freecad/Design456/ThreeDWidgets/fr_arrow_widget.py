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

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import ThreeDWidgets
import pivy.coin as coin
from ThreeDWidgets import fr_draw
from ThreeDWidgets import fr_draw1
from PySide import QtGui, QtCore
from ThreeDWidgets import fr_widget
from ThreeDWidgets import constant
from typing import List
from ThreeDWidgets import fr_label_draw

from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from dataclasses import dataclass

"""
Example how to use this widget. 

import fr_coinwindow as wn
import fr_arrow_widget as frarrow
import FreeCAD as App
g=[]
p1=App.Vector(10,1,0)     # first point in the arrow and for the windows
p2=App.Vector(20,20,0)   # Second point in the arrow (not used)
wny=wn.Fr_CoinWindow()  # Create the window, label has no effect at the moment
g.append(p1)
g.append(p2)
ln =frarrow.Fr_Arrow_Widget(g,"My label",7)   # draw the arrow - nothing will be visible yet
wny.addWidget(ln)              # Add it to the window as a child 
wny.show()                    # show the window and it's widgets. 

"""
__updated__ = '2022-11-02 20:38:50'


# class object will be used as object holder between arrow widget and the callback
@dataclass
class userDataObject:
    __slots__ = ['ArrowObj', 'events', 'callerObject']
    def __init__(self):
        self.ArrowObj = None     # the arrow widget object
        self.events = None     # events - save handle events here
        self.callerObject = None   # Class uses the fr_arrow_widget


def callback(userData: userDataObject = None):
    """
            This function will run the when the arrow is clicked 
            event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy arrow-widget callback")


class Fr_Arrow_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a arrow in coin3D world
    """
    def __init__(self, vectors: List[App.Vector] = [],
                 label: str = [[]], lineWidth=1,
                 _color=FR_COLOR.FR_BLACK,
                 _lblColor=FR_COLOR.FR_WHITE,
                 _rotation=[0.0, 0.0, 1.0, 0.0],
                  _scale: List[float] = [3, 3, 3],
                 _arrowType=0,
                 _opacity: float = 0.0):
        # Must be initialized first as per the following discussion.
        # https://stackoverflow.com/questions/67877603/how-to-override-a-function-in-an-inheritance-hierarchy#67877671
        super().__init__(vectors, label)

        self.w_lineWidth = lineWidth  # Default line width
        self.w_widgetType = constant.FR_WidgetType.FR_ARROW

        self.w_callback_ = callback  # External function
        self.w_lbl_calback_ = callback  # External function
        self.w_KB_callback_ = callback  # External function
        self.w_move_callback_ = callback  # External function
        self.w_wdgsoSwitch = coin.SoSwitch()
        self.w_color = _color  # Default color is green
        self.w_rotation = _rotation  # (x,y,z), Angle
        self.w_userData = userDataObject()   # Keep info about the widget
        self.w_userData.ArrowObj = self
        self.releaseDrag = -1  # -1 mouse no clicked not dragging, 0 is clicked, 1 is dragging
        self.arrowType = _arrowType  # 0 3D Default , 1= 2D, 2=2D
        self.w_lbluserData = fr_widget.propertyValues()
        self.w_lblColor = _lblColor
        self.w_opacity = _opacity
        self.w_scale = _scale


    def lineWidth(self, width):
        """ Set the line width"""
        self.w_lineWidth = width

    def handle(self, event):
        """
        This function is responsible for taking events and processing 
        the actions required. If the object != targeted, 
        the function will skip the events. But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. Window object is responsible for distributing the events.
        """

        self.w_userData.events = event   # Keep the event always here
        if type(event) == int:
            if event == FR_EVENTS.FR_NO_EVENT:
                return 1    # we treat this event. Nothing to do

        clickwdgdNode = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                              self.w_pick_radius, self.w_widgetSoNodes)
        clickwdglblNode = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                                self.w_pick_radius, self.w_widgetlblSoNodes)

        # Execute callback_relese when enter key pressed or E pressed
        if (self.w_parent.w_lastEvent == FR_EVENTS.FR_ENTER or
            self.w_parent.w_lastEvent == FR_EVENTS.FR_PAD_ENTER or
                self.w_parent.w_lastEvent == FR_EVENTS.FR_E):
            self.do_callback(self.w_userData)
            return 1

        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK:
            # Double click event. Only when the widget is double clicked
            if clickwdglblNode is not None:

                # if not self.has_focus():
                #    self.take_focus()
                self.do_lblcallback()
                return 1

        elif self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_RELEASE:
            # Release is accepted even if the mouse is not over the widget
            if self.releaseDrag == 1 or self.releaseDrag == 0:
                self.releaseDrag = -1
                # Release callback should be activated even if the arrow != under the mouse
                self.do_callback(self.w_userData)
                return 1

            if (clickwdgdNode is not None) or (clickwdglblNode is not None):
                if not self.has_focus():
                    self.take_focus()
                self.do_callback(self.w_userData)
                return 1
            else:
                self.remove_focus()
                return 0
        # Mouse first click and then mouse with movement is here
        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_DRAG:
            if ((clickwdgdNode is not None) or
                    (clickwdglblNode is not None)) and self.releaseDrag == -1:
                self.releaseDrag = 0  # Mouse clicked
                self.take_focus()
                return 1

            elif ((clickwdgdNode is not None) or (clickwdglblNode is not None)) and self.releaseDrag == 0:
                self.releaseDrag = 1  # Drag if will continue it will be a drag always
                self.take_focus()
                self.do_move_callback(self.w_userData)
                return 1

            elif self.releaseDrag == 1:
                # As far as we had DRAG before, we will continue run callback.
                # This is because if the mouse is not exactly on the widget, it should still take the drag.
                # Continue run the callback as far as it releaseDrag=1
                self.do_move_callback(self.w_userData)        # We use the same callback,
                return 1
        # Don't care events, return the event to other widgets
        return 0  # We couldn't use the event .. so return 0

    def draw(self):
        """
        Main draw function. It is responsible to create the node,
        and draw the arrow on the screen. It creates a node for 
        the arrow.
        """
        try:
            if self.is_active() and self.has_focus():
                usedColor = self.w_selColor
            elif self.is_active() and (self.has_focus() != 1):
                usedColor = self.w_color
            elif self.is_active() != 1:
                usedColor = self.w_inactiveColor
            if self.is_visible():
                if self.arrowType == 0:
                #                                   draw_arrow(_Points=[], _color = FR_COLOR.FR_GOLD, _ArrSize=[1.0, 1.0, 1.0], _rotation=[0.0, 0.0, 1.0, 0.0]):
                    self.w_widgetSoNodes = fr_draw.draw_arrow(self.w_vector[0], usedColor,self.w_scale, self.w_rotation)
                elif self.arrowType == 1:
                    self.w_widgetSoNodes = fr_draw.draw_2Darrow(
                        self.w_vector[0], usedColor, self.w_scale, 0, self.w_opacity, self.w_rotation)
                elif self.arrowType == 2:
                    self.w_widgetSoNodes = fr_draw.draw_2Darrow(
                        self.w_vector[0], usedColor, self.w_scale, 1, self.w_opacity, self.w_rotation)
                elif self.arrowType == 3:
                    self.w_widgetSoNodes = fr_draw.draw_DoubleSidedArrow(
                        self.w_vector[0], usedColor, self.w_scale, self.w_opacity, self.w_rotation)
                elif self.arrowType == 4:
                    self.w_widgetSoNodes = fr_draw1.draw_DoubleSide2DdArrow(
                        self.w_vector[0], usedColor, self.w_scale, self.w_opacity, self.w_rotation)
                self.w_lbluserData.linewidth = self.w_lineWidth
                self.w_lbluserData.labelcolor = self.w_lblColor
                self.w_lbluserData.vectors = self.w_vector
                self.w_lbluserData.rotation = [0, 0, 0, 0]
                # self.w_lbluserData.SetupRotation = self.w_rotation This causes a problem. TODO:FIXME:

                self.draw_label(self.w_lblColor)
                self.addSoNodeToSoSwitch(self.w_widgetSoNodes)
                self.addSoNodeToSoSwitch(self.w_widgetlblSoNodes)
            else:
                return  # We draw nothing .. This is here just for clarifying the code

        except Exception as err:
            App.Console.PrintError("'draw Fr_Arrow_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_label(self, usedColor):
        self.w_lbluserData.linewidth = self.w_lineWidth
        self.w_lbluserData.labelcolor = usedColor
        self.w_lbluserData.vectors = self.w_vector 
        #self.w_lbluserData.vectors[0] += App.Vector(0 , 0 , 3)
        lbl = fr_label_draw.draw_label(self.w_label, self.w_lbluserData)
        self.saveSoNodeslblToWidget(lbl)

    def move(self, newVecPos):
        """
        Move the object to the new location referenced by the 
        left-top corner of the object. Or the start of the arrow
        if it is an arrow.
        """
        self.resize([newVecPos[0], newVecPos[1]])

    @property
    def getVertexStart(self):
        """Return the vertex of the start point"""
        return App.Vertex(self.w_vector[0])

    @property
    def getVertexEnd(self):
        """Return the vertex of the end point"""
        return App.Vertex(self.w_vector[1])

    def show(self):
        self.w_visible = 1
        self.w_wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all children

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

    def take_focus(self):
        """
        Set focus to the widget. Which should redraw it also.
        """
        if self.w_hasFocus == 1:
            return  # nothing to do here
        self.w_hasFocus = 1
        self.redraw()

    def activate(self):
        if self.w_active:
            return  # nothing to do
        self.w_active = 1
        self.redraw()

    def deactivate(self):
        """
        Deactivate the widget. which causes that no handle comes to the widget
        """
        if self.w_active == 0:
            return  # Nothing to do
        self.w_active = 0

    def __del__(self):
        """
        Class Destructor. 
        This will remove the widget totally. 
        """
        self.hide()
        try:
            if self.w_parent is not None:
                # Parent should be the windows widget.
                self.w_parent.removeWidget(self)

            if self.w_parent is not None:
                self.w_parent.removeSoSwitchFromSceneGraph(self.w_wdgsoSwitch)

            self.removeSoNodeFromSoSwitch()
            self.removeSoNodes()
            self.removeSoSwitch()

        except Exception as err:
            App.Console.PrintError("'del Fr_Arrow_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def hide(self):
        if self.w_visible == 0:
            return  # nothing to do
        self.w_visible = 0
        self.w_wdgsoSwitch.whichChild = coin.SO_SWITCH_NONE  # hide all children
        self.redraw()

    def remove_focus(self):
        """
        Remove the focus from the widget. 
        This happens by clicking anything 
        else than the widget itself
        """
        if self.w_hasFocus == 0:
            return  # nothing to do
        else:
            self.w_hasFocus = 0
            self.redraw()

    def resize(self, vectors: List[App.Vector]):  # Width, height, thickness
        """Resize the widget by using the new vectors"""
        self.w_vector = vectors
        self.redraw()

    def size(self, vectors: List[App.Vector]):
        """Resize the widget by using the new vectors"""
        self.resize(vectors)

    def label_move(self, newPos):
        pass

    def setRotationAngle(self, axis_angle):
        ''' 
        Set the rotation axis and the angle
        Axis is coin.SbVec3f((x,y,z)
        angle=float number
        '''
        self.w_rotation = axis_angle
