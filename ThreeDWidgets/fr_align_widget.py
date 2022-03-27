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
import ThreeDWidgets
import pivy.coin as coin
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



"""
__updated__ = '2022-01-13 21:09:06'


# class object will be used as object holder between Align widget and the callback
@dataclass
class userDataObject:
    __slots__ = ['Align', 'events', 'callerObject', 'clickedBTN']

    def __init__(self):
        self.Align = None     # the Align widget object
        self.events = None     # events - save handle events here
        self.callerObject = None   # Class uses the fr_Align_widget
        self.clickedBTN: tuple = []  # used to identify the clicked button



def callback(userData: userDataObject = None):
    """
            This function will run Release happens
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy Align-widget callback")


# All buttons callbacks
def callback_btn0(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy Align-widget btn0 callback")

def callback_btn1(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy Align-widget btn1 callback")

def callback_btn2(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy Align-widget btn2 callback")

def callback_btn3(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy Align-widget btn3 callback")


def callback_btn4(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy Align-widget btn4 callback")

def callback_btn5(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy Align-widget btn5 callback")

def callback_btn6(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy Align-widget btn6 callback")

def callback_btn7(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy Align-widget btn7 callback")

def callback_btn8(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy Align-widget btn8 callback")


class Fr_Align_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a Align in coin3D world
    Example how to use the widget:
    
    
    import ThreeDWidgets.fr_align_widget as wd
    import ThreeDWidgets.fr_coinwindow as wnn

    mywin = wnn.Fr_CoinWindow()
    # You need to select an object
    s=Gui.Selection.getSelectionEx()[0]
    sh=s.Object.Shape
    b=sh.BoundBox        
    root=wd.Fr_Align_Widget(b)
    mywin.addWidget(root)
    mywin.show()


    """


    def __init__(self, _boundary: None,
                 label: str = [[]],
                 _color=[FR_COLOR.FR_RED,FR_COLOR.FR_GREEN,FR_COLOR.FR_BLUE],
                 _lblColor=FR_COLOR.FR_WHITE,
                 _AlignType=0,
                 _opacity: float = 0.0):
        # Vectors are not used, but I need to return something to Fr_Widget
        super().__init__([App.Vector(0, 0, 0), App.Vector(0, 0, 0)], label)

        self.w_lineWidth = 1  # Default line width
        self.w_widgetType = constant.FR_WidgetType.FR_ALIGN

        self.w_callback_ = callback  # External function
        self.w_lbl_calback_ = callback  # External function
        self.w_KB_callback_ = callback  # External function
        self.w_wdgsoSwitch = coin.SoSwitch()
        self.w_color = _color  # Default color is red, green & blue
        self.w_userData = userDataObject()   # Keep info about the widget
        self.w_userData.Align = self
        self.w_lbluserData = fr_widget.propertyValues()
        self.w_lblColor = _lblColor
        self.w_opacity = _opacity
        self.w_btnObjs = []  # 9 sphere objects
        self.w_baseObjs = None   #
        # This must be provided or we can not draw anything
        self.w_boundary = _boundary
        self.w_btnCallbacks_ = [callback_btn0, 
                                callback_btn1, 
                                callback_btn2, 
                                callback_btn3,
                                callback_btn4,
                                callback_btn5,
                                callback_btn6,
                                callback_btn7,
                                callback_btn8]
        self.w_selColor = [[i * 1.5 for i in self.w_color[0]],
                           [j * 1.5 for j in self.w_color[1]],
                           [k * 1.5 for k in self.w_color[2]]]
        self.w_inactiveColor = [[i * 0.9 for i in self.w_color[0]],
                                [j * 0.9 for j in self.w_color[1]],
                                [k * 0.9 for k in self.w_color[2]]]

    def setBoundary(self, bnd):
        if self.w_boundary is not None:
            del self.w_boundary
        self.w_boundary = bnd

    def handle(self, event):
        """
        This function is responsbile of taking events and processing 
        the actions required. If the object != targeted, 
        the function will skip the events. But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. Window object is responsible for distributing the events.
        """

        self.w_userData.events = event   # Keep the event always here
        if type(event) == int:
            if event == FR_EVENTS.FR_NO_EVENT:
                return 1    # we treat this event. Nonthing to do

        self.w_userData.clickedBTN = [False, False, False, False, False, False, False, False, False]
        for i in range(0, 9):
            if (self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                      self.w_pick_radius, self.w_btnObjs[i]) is not None):
                self.w_userData.clickedBTN[i] = True

        clickwdglblNode = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                                self.w_pick_radius, self.w_widgetlblSoNodes)
        #We don't use double click here
        
        if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_RELEASE:
            for i in range(0, 9):
                if self.w_userData.clickedBTN[i] is True:
                    self.clicked_obj()
                    self.do_callback()
                    return 1

            if (clickwdglblNode is not None):
                if not self.has_focus():
                    self.take_focus()
                self.do_callback()
                return 1
            else:
                self.remove_focus()
                return 0
        # Don't care events, return the event to other widgets
        return 0  # We couldn't use the event .. so return 0

    def draw(self):
        """
        Main draw function. It is responsible to create the node,
        and draw the whole widget.
        We have many lines to draw and several sphere 
        """
        try:
            #use minimum x,y and z to draw the label
            if self.w_boundary is None : 
                raise ValueError("w_boundary must be specified")    
            self.w_vector[0]=App.Vector(self.w_boundary.XMin,self.w_boundary.YMin,self.w_boundary.ZMin)
            if self.is_active() and self.has_focus():
                usedColor = self.w_selColor
            elif self.is_active() and (self.has_focus() != 1):
                usedColor = self.w_color
            elif self.is_active() != 1:
                usedColor = self.w_inactiveColor
            if self.is_visible():
                drawing = fr_draw1.drawAlignmentBars(
                    self.w_boundary, usedColor)
                (self.w_baseObjs, self.w_btnObjs) = drawing.Activate()
                allSoParts = self.w_btnObjs
                allSoParts.append( self.w_baseObjs)
                self.saveSoNodesToWidget(allSoParts)

                self.draw_label(self.w_lblColor)
                self.addSoNodeToSoSwitch(self.w_widgetSoNodes)
                self.addSoNodeToSoSwitch(self.w_widgetlblSoNodes)
            else:
                return  # We draw nothing .. This is here just for clarifying the code

        except Exception as err:
            App.Console.PrintError("'draw Fr_Align_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type,  exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_label(self, usedColor):
        self.w_lbluserData.labelcolor = usedColor
        self.w_lbluserData.vectors = self.w_vector
        lbl = fr_label_draw.draw_label(self.w_label, self.w_lbluserData)
        self.saveSoNodeslblToWidget(lbl)

    def clicked_obj(self):
        try:
            for i in range(0,9):
                if self.w_userData.clickedBTN[i] is True:
                    self.w_btnCallbacks_[i](self.w_userData)

        except Exception as err:
            App.Console.PrintError("'callback' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type,  exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

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
            App.Console.PrintError("'del Fr_Align_Widget' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type,  exc_tb = sys.exc_info()
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