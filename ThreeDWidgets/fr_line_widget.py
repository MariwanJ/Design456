# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2022                                                    *
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
from ThreeDWidgets import fr_draw
from ThreeDWidgets import fr_widget
from ThreeDWidgets import constant
from typing import List
from ThreeDWidgets import fr_label_draw

from ThreeDWidgets.constant import FR_EVENTS
import math

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

__updated__ = '2022-02-10 21:24:44'


def movecallback(userData=None):
    """
            This function will run the drag-move 
            event callback. 
    """
    # TODO : Subclass this and impalement the callback
    #          to get the desired effect
    print("dummy line-widget move callback")


def KBcallback(userData=None):
    """
            This function will run the KB 
            event callback. 
    """
    # TODO : Subclass this and impalement the callback
    #          to get the desired effect
    print("dummy line-widget KB callback")


def lblcallback(userData=None):
    """
            This function will run the label-changed 
            event callback.
    """
    # TODO : Subclass this and impalement the callback
    #          to get the desired effect
    print("dummy line-widget-label callback")


def callback(userData=None):
    """
            This function will run the when the line is clicked 
            event callback. 
    """
    # TODO : Subclass this and impalement the callback
    #          to get the desired effect
    print("dummy line-widget callback")


class Fr_Line_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a line in coin3D world
    """

    def __init__(self, vectors: List[App.Vector] = [], label: str = "", lineWidth=1):
        super().__init__(vectors, label)
        # Must be initialized first as per the following discussion.
        # https://stackoverflow.com/questions/67877603/how-to-override-a-function-in-an-inheritance-hierarchy#67877671
        self.w_lineWidth = lineWidth  # Default line width
        self.w_widgetType = constant.FR_WidgetType.FR_EDGE
        self.w_callback_ = callback  # External function
        self.w_lbl_calback_ = lblcallback  # External function
        self.w_KB_callback_ = KBcallback  # External function
        self.w_move_callback_ = movecallback  # External function
        self.w_wdgsoSwitch = coin.SoSwitch()
        self.w_wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all
        self.w_lbluserData = fr_widget.propertyValues()

    def calculateLineSpherical(self):
        # Calculate the three angles we have ref to xyz axis
        # phi - angle to the Z axis
        # thi - angle to the x axis
        # refer to https://en.wikipedia.org/wiki/Spherical_coordinate_system
        # 180 Degree must be added to thi when x<0
        
        thi = 0.0 #Z axis angle
        phi = 0.0 #x-y axis angle
        try:
            p1 = self.w_vector[0]
            p2 = self.w_vector[1]
            px2_px1 = p2.x-p1.x
            py2_py1 = p2.y-p1.y
            pz2_pz1 = p2.z-p1.z

            # Bring back the p2 to the reference of origin
            p1x_p2x = -px2_px1
            p1y_p2y = -py2_py1
            p1z_p2z = -pz2_pz1

            # Enough to take p1 as a coordinate
            r = math.sqrt(math.pow(p1x_p2x, 2) +
                          math.pow(p1y_p2y, 2)+math.pow(p1z_p2z, 2))

            if p1x_p2x < 0:
                thi = math.radians(90)+math.radians(180) + \
                    math.asin((p2.x-p1.x)/r)
            else:
                thi = math.radians(90) + math.asin((p2.x-p1.x)/r)

            if(p1z_p2z == 0):
                phi = math.radians(0)
            else:
                phi = (math.radians(
                    90)+(math.atan(math.sqrt(math.pow(p1x_p2x, 2)+math.pow(p1y_p2y, 2))/p1z_p2z)))
            return (math.degrees(thi), math.degrees(phi))

        except Exception as err:
            App.Console.PrintError("'calculateLineSpherical' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def lineWidth(self, width):
        """ Set the line width"""
        self.w_lineWidth = width

    def handle(self, event):
        """
        This function is responsible of taking events and processing 
        it. Required action will be executed here. If the object != targeted, 
        the function will skip the events. But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. Window object is responsible for distributing the events.
        """
        if type(event) == int:
            if event == FR_EVENTS.FR_NO_EVENT:
                return 1    # we treat this event. Nothing to do

            clickwdgdNode = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                                  self.w_pick_radius, self.w_widgetSoNodes)
            clickwdglblNode = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                                    self.w_pick_radius, self.w_widgetlblSoNodes)


            if ((clickwdgdNode is None) and (clickwdglblNode is None)):
                # SoSnodes not found
                self.remove_focus()
                return 0
            if event == FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK:
                # Double click event.
                if (clickwdglblNode is not None) or (clickwdgdNode is not None):
                    self.do_lblcallback()
                    return 1

            elif event == FR_EVENTS.FR_MOUSE_LEFT_RELEASE:
                if (clickwdgdNode is not None) or (clickwdglblNode is not None):
                    if not self.has_focus():
                        self.take_focus()
                    self.do_callback()
                    return 1

            # Don't care events, return the event to other widgets
        return 0  # We couldn't use the event .. so return 0

    def draw(self):
        """
        Main draw function. It is responsible for creating the SoSeparator node,
        and draw the line on the screen - in the COIN3D world.        
        """
        try:

            if len(self.w_vector) < 2:
                raise ValueError('Must be 2 Vectors')
            p1 = self.w_vector[0]
            p2 = self.w_vector[1]
            usedColor = usedColor = self.w_selColor
            if self.is_active() and self.has_focus():
                usedColor = self.w_selColor
            elif self.is_active() and (self.has_focus() != 1):
                usedColor = self.w_color
            elif self.is_active() != 1:
                usedColor = self.w_inactiveColor
            _rotation = (0, 0, 1, 0)
            vec = [p1, p2]
            if self.is_visible():
                self.w_widgetSoNodes=fr_draw.draw_line(
                    vec, usedColor, _rotation, self.w_lineWidth)
                self.draw_label(usedColor)
                # add both to the same switch. and add them to the scenegraph automatically
                allToSwitch = []
                allToSwitch.append(self.w_widgetSoNodes)
                allToSwitch.append(self.w_widgetlblSoNodes)
                self.addSoNodeToSoSwitch(allToSwitch)
            else:
                return  # We draw nothing .. This is here just for clarifying the code

        except Exception as err:
            App.Console.PrintError("'Fr_Line_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_label(self, usedColor):
        self.w_lbluserData.linewidth = self.w_lineWidth
        self.w_lbluserData.labelcolor = usedColor
        self.w_lbluserData.vectors = self.w_vector
        (thi, phi) = self.calculateLineSpherical()
        self.w_lbluserData.SetupRotation = [0, -phi, thi]
        self.w_widgetlblSoNodes = fr_label_draw.draw_label(self.w_label, self.w_lbluserData)

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
            App.Console.PrintError("'Fr_Line_Widget' Failed. "
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
