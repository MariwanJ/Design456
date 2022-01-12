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



"""
__updated__ = '2022-01-12 19:55:02'


# class object will be used as object holder between Align widget and the callback
@dataclass
class userDataObject:
    __slots__ = ['Align', 'events', 'callerObject']
    def __init__(self):
        self.Align = None     # the Align widget object
        self.events = None     # events - save handle events here
        self.callerObject = None   # Class uses the fr_Align_widget


def callback(userData: userDataObject = None):
    """
            This function will run the when the Align is clicked 
            event callback. 
    """
    # Subclass this and impalement the callback or just change the callback function
    print("dummy Align-widget callback")


class Fr_Align_Widget(fr_widget.Fr_Widget):

    """
    This class is for drawing a Align in coin3D world
    """
    # Big mistake  regarding the Aligns: Read https://grey.colorado.edu/coin3d/classSoTransform.html#a357007d906d1680a72cd73cf974a6869
    # Don't do that

    def __init__(self, vectors: List[App.Vector] = [],
                 label: str = [[]], lineWidth=1,
                 _color=FR_COLOR.FR_BLACK,
                 _lblColor=FR_COLOR.FR_WHITE,
                 _rotation=[0.0, 0.0, 1.0, 0.0],
                  _scale: List[float] = [3, 3, 3],
                 _AlignType=0,
                 _opacity: float = 0.0):
        super().__init__(vectors, label)

        self.w_lineWidth = lineWidth  # Default line width
        self.w_widgetType = constant.FR_WidgetType.FR_ALIGN

        self.w_callback_ = callback  # External function
        self.w_lbl_calback_ = callback  # External function
        self.w_KB_callback_ = callback  # External function
        self.w_btn_callback_ = callback  # External function
        self.w_wdgsoSwitch = coin.SoSwitch()
        self.w_color = _color  # Default color is green
        self.w_rotation = _rotation  # (x,y,z), Angle
        self.w_userData = userDataObject()   # Keep info about the widget
        self.w_userData.Align = self
        self.releaseDrag = -1  # -1 mouse no clicked not dragging, 0 is clicked, 1 is dragging
        self.w_lbluserData = fr_widget.propertyValues()
        self.w_lblColor = _lblColor
        self.w_opacity = _opacity
        self.w_scale = _scale
        self.sphereObjs = [] #9 sphere objects
        self.BaseObjs =  None   #


    def lineWidth(self, width):
        """ Set the line width"""
        self.w_lineWidth = width

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

        btn0 = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                              self.w_pick_radius, self.w_widgetSoNodes)
        btn1 = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                              self.w_pick_radius, self.w_widgetSoNodes)
        btn2 = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                              self.w_pick_radius, self.w_widgetSoNodes)
        btn3 = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                              self.w_pick_radius, self.w_widgetSoNodes)
        btn4 = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                              self.w_pick_radius, self.w_widgetSoNodes)
        btn5 = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                              self.w_pick_radius, self.w_widgetSoNodes)
        btn6 = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                              self.w_pick_radius, self.w_widgetSoNodes)
        btn7 = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                              self.w_pick_radius, self.w_widgetSoNodes)
        btn8 = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                              self.w_pick_radius, self.w_widgetSoNodes)





        clickwdglblNode = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                                self.w_pick_radius, self.w_widgetlblSoNodes)

        # Execute callback_relese when enter key pressed or E pressed
        if (self.w_parent.w_lastEvent == FR_EVENTS.FR_ENTER or
            self.w_parent.w_lastEvent == FR_EVENTS.FR_PAD_ENTER or
                self.w_parent.w_lastEvent == FR_EVENTS.FR_E):
            self.do_callback()

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
                # Release callback should be activated even if the Align != under the mouse
                self.do_callback()
                return 1

            if (clickwdgdNode is not None) or (clickwdglblNode is not None):
                if not self.has_focus():
                    self.take_focus()
                self.do_callback()
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
                self.do_move_callback()
                return 1

            elif self.releaseDrag == 1:
                # As far as we had DRAG before, we will continue run callback.
                # This is because if the mouse is not exactly on the widget, it should still take the drag.
                # Continue run the callback as far as it releaseDrag=1
                self.do_move_callback()        # We use the same callback,
                return 1
        # Don't care events, return the event to other widgets
        return 0  # We couldn't use the event .. so return 0

    def draw(self):
        """
        Main draw function. It is responsible to create the node,
        and draw the whole widget.
        We have many lines to draw and several sphere 
        """
        try:
            if self.is_active() and self.has_focus():
                usedColor = self.w_selColor
            elif self.is_active() and (self.has_focus() != 1):
                usedColor = self.w_color
            elif self.is_active() != 1:
                usedColor = self.w_inactiveColor
            if self.is_visible():
 

                self.draw_label(self.w_lblColor)
                self.addSoNodeToSoSwitch(self.w_widgetSoNodes)
                self.addSoNodeToSoSwitch(self.w_widgetlblSoNodes)
            else:
                return  # We draw nothing .. This is here just for clarifying the code

        except Exception as err:
            App.Console.PrintError("'draw Fr_Align_Widget' Failed. "
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
    
    def clicked_obj(userData: fr_Align_widget.userDataObject = None):
        try:
            events = userData.events
            linktocaller = userData.callerObject
            if type(events) != int:
                return

            btn1 = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                            self.w_pick_radius, self.w_widgetSoNodes)
            
            
            clickwdglblNode = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                                self.w_pick_radius, self.w_widgetlblSoNodes)
            linktocaller.endVector = App.Vector(self.w_parent.w_lastEventXYZ.Coin_x,
                                                self.w_parent.w_lastEventXYZ.Coin_y,
                                                self.w_parent.w_lastEventXYZ.Coin_z)

            if clickwdgdNode is None and clickwdglblNode is None:
                if linktocaller.run_Once is False:
                    return 0  # nothing to do

            if linktocaller.run_Once is False:
                linktocaller.run_Once = True
                linktocaller.mouseToArrowDiff = linktocaller.endVector.sub(
                    userData.ArrowObj.w_vector[0])
                # Keep the old value only first time when drag start
                linktocaller.startVector = linktocaller.endVector
                if not self.has_focus():
                    self.take_focus()

            scale = 1.0

            MovementsSize = linktocaller.endVector.sub(
                linktocaller.mouseToArrowDiff)
            (scaleX, scaleY, scaleZ) = calculateScale(
                self, linktocaller, MovementsSize)

            if self.w_color == FR_COLOR.FR_OLIVEDRAB:
                scale = scaleY
    #            self.w_vector[0].y = MovementsSize.y #+linktocaller.mmAwayFrom3DObject

            elif self.w_color == FR_COLOR.FR_RED:
                #            self.w_vector[0].x = MovementsSize.x #+linktocaller.mmAwayFrom3DObject
                scale = scaleX

            elif self.w_color == FR_COLOR.FR_BLUE:
                #            self.w_vector[0].z = MovementsSize.z #+linktocaller.mmAwayFrom3DObject
                scale = scaleZ

            linktocaller.scaleLBL.setText("scale= "+str(scale))

            linktocaller.smartInd[1].changeLabelstr(
                "  Scale= " + str(round(scaleX, 4)))
            linktocaller.smartInd[0].changeLabelstr(
                "  Scale= " + str(round(scaleY, 4)))
            linktocaller.smartInd[2].changeLabelstr(
                "  Scale= " + str(round(scaleZ, 4)))
            linktocaller.resizeArrowWidgets()
            linktocaller.smartInd[0].redraw()
            linktocaller.smartInd[1].redraw()
            linktocaller.smartInd[2].redraw()

            ResizeObject(self, linktocaller, MovementsSize)

        except Exception as err:
            App.Console.PrintError("'callback' Failed. "
                                "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


    def buttonPress_cb(self, button):
        if(button==0):
            pass
        elif (button==1):
            pass
        elif (button==2):
            pass
        elif (button==3):
            pass
        elif (button==4):
            pass
        elif (button==5):
            pass
        elif (button==6):
            pass
        elif (button==7):
            pass
        elif (button==8):
            pass

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
