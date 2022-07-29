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
import Design456Init
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import constant
from typing import List
import FACE_D as faced
from ThreeDWidgets import fr_draw
from ThreeDWidgets import fr_widget

from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets import fr_label_draw
"""
#Example how to use the widget: 
#Notice that you should activate Design456 WB before you can use this widget.
import fr_coinwindow as wn
import fr_square_widget as square
import FreeCAD as App
g=[]
p1=App.Vector(2,2,5)
p2=App.Vector(22,2,5)
p3=App.Vector(22,22,5)
p4=App.Vector(2,22,5)
g.append(p1)
g.append(p2)
wny=wn.Fr_CoinWindow("MyWindow")
g.clear()

g.append(p1)
g.append(p2)
g.append(p3)
g.append(p4)
col=(0.0, 0.0, 0.0)

square_ =square.Fr_SquareFrame_Widget(g,'square',2)
wny.addWidget(square_)
wny.show()

"""
__updated__ = '2021-12-31 08:57:43'


# FIXME: Handle is not correct . Make it like arrow widget.


def callback_default(obj, userData=None):
    print("fr_square widget default callback")


def callback_defaultlbl(obj, userData=None):
    print("fr_square widget default LBL callback")


class Fr_SquareFrame_Widget(fr_widget.Fr_Widget):
    """
    This class is for drawing a line in  coin3D
    """

    def __init__(self, vectors: List[App.Vector] = [], labels: str = "", lineWidth=1):
        # It must be initialized first refer to fr_line_widget for more info
        super().__init__(vectors, labels)
        self.w_vector = vectors
        # default line width        # Here we have a list (4 labels)
        self.w_lineWidth = lineWidth
        self.w_label = labels
        self.w_widgetType = constant.FR_WidgetType.FR_SQUARE_FRAME
        self.w_callback_ = callback_default
        self.w_lbl_calback_ = callback_defaultlbl
        self.w_lbluserData = fr_widget.propertyValues()

    # def addVertices(self, vertices):
    #     if(len(vertices)!=4):
    #             # must be four vertices
    #             errMessage = "Four Vertices are required"
    #             faced.errorDialog(errMessage)
    #             return
    #     self.w_vector.clear()
    #     self.w_vector = vertices

    def LineWidth(self, width):
        self.w_linewidth = width

    def handle(self, event):
        """
        This function is responsible for taking events and doing 
        the action(s) required. If the object != targeted, 
        the function will skip the event(s). But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. fr_coinwindow object is responsible for distributing the events.
        """
        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_PUSH:
            clickwdgdNode = self.w_parent.objectMouseClick_Coin3d(
                self.w_parent.w_lastEventXYZ.pos, self.w_pick_radius, self.w_widgetSoNodes)
            clickwdglblNode = self.w_parent.objectMouseClick_Coin3d(
                self.w_parent.w_lastEventXYZ.pos, self.w_pick_radius, self.w_widgetlblSoNodes)

            if clickwdgdNode is not None or clickwdglblNode is not None:
                self.take_focus()
                self.do_callback()
                self.do_lblcallback()
                return 1
            else:
                self.remove_focus()
                return event  # We couldn't use the event .. so return the event itself

        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK:
            # Double click event.
            print("Double click detected")

    def draw(self):
        """
        Main draw function. It is responsible to create the node,
        and draw the line on the screen. It creates a node for 
        the line.
        """
        try:

            if len(self.w_vector) != 4:
                raise ValueError('Must be 4 Vectors')
            if self.is_active() and self.has_focus():
                usedColor = self.w_selColor
            elif self.is_active() and (self.has_focus() != 1):
                usedColor = self.w_color
            elif self.is_active() != 1:
                usedColor = self.w_inactiveColor
            if self.is_visible():
                square = fr_draw.draw_square_frame(
                    self.w_vector, usedColor, self.w_lineWidth)
                self.draw_label()

                # Add SoSeparator. Will be added to switch automatically
                self.saveSoNodesToWidget(square)
                self.addSoNodeToSoSwitch(self.w_widgetSoNodes)
                self.addSoNodeToSoSwitch(self.w_widgetlblSoNodes)
                print(self.w_wdgsoSwitch)

            else:
                return  # We draw nothing .. This is here just for clarifying the code

        except Exception as err:
            App.Console.PrintError("'Fr_SquareFrame_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_label(self):
        self.w_lbluserData.linewidth = self.w_lineWidth
        self.w_lbluserData.labelcolor = self.w_lblColor
        firstTwovertices: List[App.Vector] = []
        firstTwovertices.append(self.w_vector[0])
        firstTwovertices.append(self.w_vector[1])

        self.w_lbluserData.vectors = firstTwovertices
        lbl = fr_label_draw.draw_label([self.w_label], self.w_lbluserData)
        self.saveSoNodeslblToWidget(lbl)

    def move(self, newVecPos):
        """
        Move the object to the new location referenced by the 
        left-top corner of the object. Or the start of the line
        if it is a line.
        """
        self.resize(newVecPos)

    def getVertexStart(self):
        """Return the vertex of the start point"""
        return App.Vertex(self.w_vector[0])

    def getVertexEnd(self):
        """Return the vertex of the end point"""
        return App.Vertex(self.w_vector[3])

    def show(self):
        self.w_visible = 1
        self.redraw()

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
        This will remove the widget totally. 
        """
        self.removeSoNodes()

    def is_active(self):
        return self.w_active

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


"**************************************************************************************************************************"


"""
#Example how to use the widget: 
#Notice that you should activate Design456 WB before you can use this widget.
import fr_coinwindow as wn
import fr_square_widget as square
import FreeCAD as App
g=[]
p1=App.Vector(2,2,5)
p2=App.Vector(22,2,5)
p3=App.Vector(22,22,5)
p4=App.Vector(2,22,5)
g.append(p1)
g.append(p2)
wny=wn.Fr_CoinWindow("MyWindow")
g.clear()

g.append(p1)
g.append(p2)
g.append(p3)
g.append(p4)
col=(0.0, 0.0, 0.0)

square_ =square.Fr_SquareFace_Widget(g,'square',2)
wny.addWidget(square_)
wny.show()

"""


class Fr_SquareFace_Widget(fr_widget.Fr_Widget):
    """
    This class is for drawing a line in  coin3D
    """

    def __init__(self, vectors: List[App.Vector] = [], labels: str = "", lineWidth=1):
        # It must be initialized first refer to fr_line_widget for more info
        super().__init__(vectors, labels)
        self.w_vector = vectors
        # default line width        # Here we have a list (4 labels)
        self.w_lineWidth = lineWidth
        self.w_label = labels
        self.w_widgetType = constant.FR_WidgetType.FR_SQUARE_FRAME
        self.w_callback_ = callback_default
        self.w_lbl_calback_ = callback_defaultlbl

    # def addVertices(self, vertices):
    #     if(len(vertices)!=4):
    #             # must be four vertices
    #             errMessage = "Four Vertices are required"
    #             faced.errorDialog(errMessage)
    #             return
    #     self.w_vector.clear()
    #     self.w_vector = vertices

    def LineWidth(self, width):
        self.w_linewidth = width

    def handle(self, event):
        """
        This function is responsible for taking events and doing 
        the action(s) required. If the object != targeted, 
        the function will skip the event(s). But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. fr_coinwindow object is responsible for distributing the events.
        """
        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_PUSH:
            clickwdgdNode = self.w_parent.objectMouseClick_Coin3d(
                self.w_parent.w_lastEventXYZ.pos, self.w_pick_radius, self.w_widgetSoNodes)
            clickwdglblNode = self.w_parent.objectMouseClick_Coin3d(
                self.w_parent.w_lastEventXYZ.pos, self.w_pick_radius, self.w_widgetlblSoNodes)

            if clickwdgdNode is not None or clickwdglblNode is not None:
                self.take_focus()
                self.do_callback()
                self.do_lblcallback()
                return 1
            else:
                self.remove_focus()
                return event  # We couldn't use the event .. so return the event itself

        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK:
            # Double click event.
            print("Double click detected")

    def draw(self):
        """
        Main draw function. It is responsible to create the node,
        and draw the line on the screen. It creates a node for 
        the line.
        """
        try:

            if len(self.w_vector) != 4:
                raise ValueError('Must be 4 Vectors')
            if self.is_active() and self.has_focus():
                usedColor = self.w_selColor
            elif self.is_active() and (self.has_focus() != 1):
                usedColor = self.w_color
            elif self.is_active() != 1:
                usedColor = self.w_inactiveColor
            if self.is_visible():
                square = fr_draw.draw_fourSidedShape(
                    self.w_vector, usedColor, self.w_lineWidth).Activated()
                self.draw_label()

                # Add SoSeparator. Will be added to switch automatically
                self.saveSoNodesToWidget(square)
                self.addSoNodeToSoSwitch(self.w_widgetSoNodes)
                self.addSoNodeToSoSwitch(self.w_widgetlblSoNodes)

            else:
                return  # We draw nothing .. This is here just for clarifying the code

        except Exception as err:
            App.Console.PrintError("'Fr_SquareFrame_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_label(self):
        self.w_lbluserData.linewidth = self.w_lineWidth
        self.w_lbluserData.labelcolor = self.w_lblColor
        firstTwovertices: List[App.Vector] = []

        firstTwovertices.append(self.w_vector[0])
        firstTwovertices.append(self.w_vector[1])

        self.w_lbluserData.vectors = firstTwovertices
        lbl = fr_label_draw.draw_label([self.w_label], self.w_lbluserData)
        self.saveSoNodeslblToWidget(lbl)

    def move(self, newVecPos):
        """
        Move the object to the new location referenced by the 
        left-top corner of the object. Or the start of the line
        if it is a line.
        """
        self.resize(newVecPos)

    def getVertexStart(self):
        """Return the vertex of the start point"""
        return App.Vertex(self.w_vector[0])

    def getVertexEnd(self):
        """Return the vertex of the end point"""
        return App.Vertex(self.w_vector[3])

    def show(self):
        self.w_visible = 1
        self.redraw()

    def redraw(self):
        """
        After the widgets damages, this function should be called.        
        """
        if self.is_visible():
            # Remove the sceneNodes from the widget
            self.removeSoNodes()
            # Remove the node from the switch as a child
            self.removeSoNodeFromSoSwitch()
            # Remove the SoSwitch from fr_coinwindo
            self.w_parent.removeSoSwitchFromSceneGraph(self.w_wdgsoSwitch)
            self.draw()

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
        This will remove the widget totally. 
        """
        self.removeSoNodes()

    def is_active(self):
        return self.w_active

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
