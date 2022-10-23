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
from re import X
import sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
from ThreeDWidgets import fr_widget
from ThreeDWidgets import constant
from typing import List
import FACE_D as faced
from dataclasses import dataclass
from ThreeDWidgets.fr_draw import draw_2Darrow
from ThreeDWidgets.fr_draw import draw_ball

from ThreeDWidgets import fr_label_draw
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from ThreeDWidgets.fr_draw1 import draw_RotationPad
import math
from Design456Pref import Design456pref_var

__updated__ = '2022-10-22 17:37:22'
'''
    This widget will be used with the smart sweep. 
    It should consist of three arrows and a ball. 
    There will be four callbacks. 
    -One for the ball,
    -One for the X-Arrow
    -One for the Y-Arrow
    -One for the Z-Arrow
    The ball's callback should freely without restrictions move the ball's position.
    After the change of each of these callbacks, there is a general callback which should be
    given to the widget and will be executed. 
    That callback should update the related object in FreeCAD not coin3d.

'''

"""
Example how to use this widget.

# show the window and it's widgets.
import ThreeDWidgets.fr_coinwindow as wnn
from ThreeDWidgets.constant import FR_COLOR
import ThreeDWidgets.fr_ball_three_arrows as wd

mywin = wnn.Fr_CoinWindow()
v1=[App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, 0.0),App.Vector(0.0, 0.0, 0.0)] 
r1=wd.Fr_BallThreeArrows_Widget(v1, ["BallThreeAxis",])
mywin.addWidget(r1)
mywin.show()

"""



@dataclass
class userDataObject:
    __slots__ = ['ActiveAxis','events', 'callerObject', 'ballArrows']

    def __init__(self):
        self.events = None          # events - save handle events here
        self.callerObject = None    # Link to the Tool that creates this widget
        self.ballArrows= None       # will consists of a link to the whole widget
        self.ActiveAxis=""

# *******************************CALLBACKS - DEMO *****************************
def xAxis_cb(userData: userDataObject = None):
    """
        This function executes when the XAxis
        event callback occurs.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy XAxis -3Arrows callback")


def yAxis_cb(userData: userDataObject = None):
    """
        This function executes when the rotary ball
        angel changed event callback occurs.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy YAxis -3Arrows callback")


def zAxis_cb(userData: userDataObject = None):
    """
        This function executes when the XAxis
        event callback occurs.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy ZAxis -3Arrows callback")
    
def ball_cb(userData: userDataObject = None):
    """
        This function executes when the ball (is clicked)
        event callback occurs.
    """
    # Subclass this and impalement the callback or
    # just change the callback function
    print("dummy ball - callback")
    
# *************************
# Whole widget callback  - Might not be used
# *************************************************************
def callback(userData: userDataObject = None):
    """
        This function executes when lblCallbak (double click callback)
        or general widget callback occurs
    """
    # Subclass the widget and impalement the callback or just change the callback function
    print("dummy General Widget callback")

# *************************************************************




#Widget class - definitions and functions
# *************************************************************
class Fr_BallThreeArrows_Widget(fr_widget.Fr_Widget):

    def __init__(self, vectors: List[App.Vector] = [],
                 label: str = [[]],
                 _lblColor=FR_COLOR.FR_WHITE,
                 _axisColor=[FR_COLOR.FR_RED,
                             FR_COLOR.FR_GREEN,
                             FR_COLOR.FR_BLUE],
                 # Whole widget rotation
                 _rotation: List[float] = [0.0, 0.0, 0.0, 0.0],
                 
                 # Pre-rotation
                 _setupRotation: List[float] = [0.0, 0.0, 0.0],
                 _scale: List[float] = [6.0, 6.0, 6.0],
                 _ballScale:List[float] = [1, 1, 1],
                 _type: int = 1,
                 _opacity: float = 0.0,
                 _linkToFreeCADObj=None,
                 _stepSize =Design456pref_var.MouseStepSize,   #This is based on the stepsize defined by Design456 WB
                 _distanceBetweenThem: float = 0.5):
        super().__init__(vectors, label)
        
        self.w_lbluserData = fr_widget.propertyValues()  # Only for label
        self.w_widgetType = constant.FR_WidgetType.FR_THREE_BALL
        # General widget callback (mouse-button) function - External function
        self.w_callback_ = callback
        self.w_lbl_calback_ = callback              # Label callback
        self.w_KB_callback_ = callback              # Keyboard

        # Dummy callback Axis
        self.w_xAxis_cb_ = xAxis_cb
        self.w_yAxis_cb_ = yAxis_cb
        self.w_zAxis_cb_ = zAxis_cb
        self.w_ball_cb_ =  ball_cb

        self.Opacity = _opacity
        self.DrawingType = _type
        # Use this to separate the arrows/lbl from the origin of the widget
        self.distanceBetweenThem = _distanceBetweenThem

        self.w_wdgsoSwitch = coin.SoSwitch()

        self.w_XarrowSeparator = None
        self.w_YarrowSeparator = None
        self.w_ZarrowSeparator = None
        self.w_BallSeparator = None
        
        self.w_color = _axisColor
        self.w_selColor = [[i * 1.5 for i in self.w_color[0]],
                           [j * 1.5 for j in self.w_color[1]],
                           [k * 1.5 for k in self.w_color[2]]]
        self.w_Scale = _scale
        self.ballScale=_ballScale
        self.w_inactiveColor = [[i * 0.9 for i in self.w_color[0]],
                                [j * 0.9 for j in self.w_color[1]],
                                [k * 0.9 for k in self.w_color[2]]]

        self.w_userData = userDataObject()  # Keep info about the whole widget
        # This affect only the Widget label - nothing else
        self.w_lbluserData.linewidth = self.w_lineWidth
        self.w_lbluserData.vectors = self.w_vector
        self.w_userData.ballArrows= self
                
        # We must make it higher or it will intersect the object and won't be visible
        # TODO:Check if this works always?
        self.w_lbluserData.vectors[0].x = self.w_lbluserData.vectors[0].x + \
            self.distanceBetweenThem
        self.w_lbluserData.vectors[0].y = self.w_lbluserData.vectors[0].y + \
            self.distanceBetweenThem
        self.w_lbluserData.vectors[0].z = self.w_lbluserData.vectors[0].z + \
            self.distanceBetweenThem
        self.w_lbluserData.labelcolor = _lblColor

        self.w_rotation = _rotation       # Whole object Rotation
        self.w_arrowsEnabled = [True, True, True]

        # -1 no click, 0 mouse clicked, 1 mouse dragging
        # Used to avoid running drag code while it is in drag mode
        self.XreleaseDragAxis = -1
        self.YreleaseDragAxis = -1
        self.ZreleaseDragAxis = -1

        # -1 no click, 0 mouse clicked, 1 mouse dragging
        # Used to avoid running drag code while it is in drag mode
        self.AreleaseDragAxis = -1

        self.run_Once = [False, False, False]
        self.startVector = App.Vector(0.0, 0.0, 0.0)
        self.endVector = App.Vector(0.0, 0.0, 0.0)
        #link to any object that it's placement will be based on this widget 
        self.linkToFreeCADObj=_linkToFreeCADObj 
        self.StepSize=_stepSize
        self.oldPosition=None
        self.mouseToArrowDiff=App.Vector(0, 0, 0)
    
    def setFreeCADObj(self,OBJECT):
        self.linkToFreeCADObj=OBJECT
    #TODO: NOT SURE IF THIS NECESSARY :FIXME:
    def setStepSize(self,step):
        self.StepSize=step
        
    def KeyboardEvent(self, events):
        try:
            key = events.getKey() 
            eventState = events.getState()
            if key == coin.SoKeyboardEvent.E and eventState == coin.SoButtonEvent.UP:
                self.w_parent.w_lastEvent = FR_EVENTS.FR_NO_EVENT
            if self.XreleaseDragAxis==1 or self.YreleaseDragAxis==1 or self.ZreleaseDragAxis==1 or self.AreleaseDragAxis==1:
                self.do_callback()
                self.XreleaseDragAxis=-1  #drag is finished
                self.YreleaseDragAxis=-1  #drag is finished
                self.ZreleaseDragAxis=-1  #drag is finished
                self.AreleaseDragAxis=-1
                self.mouseToArrowDiff=App.Vector(0,0,0)
                return 1
            return 0
        except Exception as err:
            App.Console.PrintError("'KeyBoardEvent' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    
    def handle(self, event):

        """
        This function is responsible for taking events and processing 
        the actions required. If the object != targeted, 
        the function will skip the events. But if the widget was
        targeted, it returns 1. Returning 1 means that the widget
        processed the event and no other widgets needs to get the 
        event. Window object is responsible for distributing the events.
        """
        try:
            newPosition=App.Vector(0.0,0.0,0.0)
            if type(event) == int:
                if event == FR_EVENTS.FR_NO_EVENT:
                    return 1  # we treat this event. Nothing to do
            self.w_userData.events = event  # Keep the event always here
            if self.w_parent is None:
                print("self.w_parent is NOne")
                return
            self.StepSize=Design456pref_var.MouseStepSize  # this must be updated always.
             
            self.endVector = App.Vector(self.w_parent.w_lastEventXYZ.Coin_x,
                                            self.w_parent.w_lastEventXYZ.Coin_y,
                                            self.w_parent.w_lastEventXYZ.Coin_z)

            if (type(event) == coin.SoKeyboardEvent):
                return self.KeyboardEvent(event)
                            
            
            # This is for the widgets label - Not the axes label - be aware.
            clickwdglblNode = self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                        self.w_pick_radius, self.w_widgetlblSoNodes)
            # In this widget, we have 4 coin drawings that we need to capture event for them

            clickwdgdNode = [False, False,False,False]
            if(self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                    self.w_pick_radius, self.w_XarrowSeparator) is not None):
                clickwdgdNode[0] = True
            elif (self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                    self.w_pick_radius, self.w_YarrowSeparator) is not None):
                clickwdgdNode[1] = True
            elif (self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                    self.w_pick_radius, self.w_ZarrowSeparator) is not None):
                clickwdgdNode[2] = True
            elif (self.w_parent.objectMouseClick_Coin3d(self.w_parent.w_lastEventXYZ.pos,
                                                    self.w_pick_radius, self.w_BallSeparator) is not None):
                clickwdgdNode[3] = True

            # else:
            #     return 0  # We couldn't use the event .. so return 0
            
            if self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK:
                #Prioritized callback TODO: is it correct
                self.mouseToArrowDiff=App.Vector(0,0,0)
                if clickwdglblNode is not None:
                    self.do_lblcallback()
                    return 1

            elif self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_RELEASE:
                if self.XreleaseDragAxis==1 or self.YreleaseDragAxis==1 or self.ZreleaseDragAxis==1 or self.AreleaseDragAxis==1:
                    self.do_callback()
                    self.XreleaseDragAxis=-1  #drag is finished
                    self.YreleaseDragAxis=-1  #drag is finished
                    self.ZreleaseDragAxis=-1  #drag is finished
                    self.AreleaseDragAxis=-1
                    self.mouseToArrowDiff=App.Vector(0,0,0)
                    return 

            elif self.w_parent.w_lastEvent == FR_EVENTS.FR_MOUSE_DRAG:
                if self.oldPosition is None:
                    self.oldPosition = self.endVector
                    self.mouseToArrowDiff=self.endVector.sub(self.w_vector[0]) #difference between mouse click and start of the coin widget
                delta = (self.endVector.sub(self.oldPosition)).sub(self.mouseToArrowDiff)
                result = 0
                resultVector = App.Vector(0, 0, 0)
                if abs(delta.x) > 0 and abs(delta.x) >= self.StepSize:
                    result = int(delta.x / self.StepSize)
                    resultVector.x = (result * self.StepSize)
                if abs(delta.y) > 0 and abs(delta.y) >= self.StepSize:
                    result = int(delta.y / self.StepSize)
                    resultVector.y = (result * self.StepSize)

                if abs(delta.z) > 0 and abs(delta.z) >= self.StepSize:
                    result = int(delta.z / self.StepSize)
                    resultVector.z = (result * self.StepSize)
                newPosition = self.oldPosition.add(resultVector)
                self.oldPosition = newPosition       
                #X-Axis and arrow
                if clickwdgdNode[0] is True and self.XreleaseDragAxis==-1:
                    self.XreleaseDragAxis=0 # Arrow clicked first time it will just change this value
                    self.w_userData.ActiveAxis="X"
                    return 1
                elif clickwdgdNode[0] is True and self.XreleaseDragAxis==0:
                    self.XreleaseDragAxis=1
                    self.w_userData.ActiveAxis="X"
                    if (hasattr(self.linkToFreeCADObj,"X")):
                        #Draft Point
                        self.linkToFreeCADObj.X=newPosition.x
                    else:
                        #other objects if they are not like Point :TODO: FIXME: Don't know if this is correct
                        self.linkToFreeCADObj.Placement.Base.x=newPosition.x
                    self.w_vector[0].x=newPosition.x                
                    self.w_xAxis_cb_(self.w_userData)
                    return 1
                elif self.XreleaseDragAxis==1:
                    #continue X drag 
                    self.w_xAxis_cb_(self.w_userData)
                    if (hasattr(self.linkToFreeCADObj,"X")):
                        #Draft Point
                        self.linkToFreeCADObj.X=newPosition.x
                    else:
                        #other objects if they are not like Point :TODO: FIXME: Don't know if this is correct
                        self.linkToFreeCADObj.Placement.Base.x=newPosition.x
                    self.w_vector[0].x=newPosition.x       
                    self.redraw()
                    return 1                

                #Y-Axis and arrow
                if clickwdgdNode[1] is True and self.YreleaseDragAxis==-1:
                    self.YreleaseDragAxis=0 # Arrow clicked first time it will just change this value
                    self.w_userData.ActiveAxis="Y"
                    return 1
                elif clickwdgdNode[1] is True and self.YreleaseDragAxis==0:
                    self.YreleaseDragAxis=1
                    self.w_userData.ActiveAxis="Y"
                    if (hasattr(self.linkToFreeCADObj,"Y")):
                        #Draft Point
                        self.linkToFreeCADObj.Y=newPosition.y
                    else:
                        #other objects if they are not like Point :TODO: FIXME: Don't know if this is correct
                        self.linkToFreeCADObj.Placement.Base.y=newPosition.y                
                    self.w_vector[0].y=newPosition.y   
                    self.w_yAxis_cb_(self.w_userData)
                    return 1
                elif self.YreleaseDragAxis==1:
                    #continue Y drag 
                    if (hasattr(self.linkToFreeCADObj,"Y")):
                        #Draft Point
                        self.linkToFreeCADObj.Y=newPosition.y
                    else:
                        #other objects if they are not like Point :TODO: FIXME: Don't know if this is correct
                        self.linkToFreeCADObj.Placement.Base.y=newPosition.y                
                    self.w_vector[0].y=newPosition.y  
                    self.w_yAxis_cb_(self.w_userData)
                    self.redraw()
                    return 1     

                #Z-Axis
                if clickwdgdNode[2] is True and self.ZreleaseDragAxis==-1:
                    self.ZreleaseDragAxis=0 # Arrow clicked first time it will just change this value
                    self.w_userData.ActiveAxis="Z"
                    return 1
                elif clickwdgdNode[2] is True and self.ZreleaseDragAxis==0:
                    self.ZreleaseDragAxis=1
                    self.w_userData.ActiveAxis="Z"
                    if (hasattr(self.linkToFreeCADObj,"Z")):
                        #Draft Point
                        self.linkToFreeCADObj.Z=newPosition.z
                    else:
                        #other objects if they are not like Point :TODO: FIXME: Don't know if this is correct
                        self.linkToFreeCADObj.Placement.Base.z=newPosition.z                
                    self.w_vector[0].z=newPosition.z   
                    self.w_zAxis_cb_(self.w_userData)
                    return 1
                elif self.ZreleaseDragAxis==1:
                    #continue drag 
                    if (hasattr(self.linkToFreeCADObj,"Z")):
                        #Draft Point
                        self.linkToFreeCADObj.Z=newPosition.z
                    else:
                        #other objects if they are not like Point :TODO: FIXME: Don't know if this is correct
                        self.linkToFreeCADObj.Placement.Base.z=newPosition.z                
                    self.w_zAxis_cb_(self.w_userData)
                    self.redraw()
                    return 1      

                #Ball 
                if clickwdgdNode[3] is True and self.AreleaseDragAxis==-1:
                    self.AreleaseDragAxis=0 # Arrow clicked first time it will just change this value
                    self.w_userData.ActiveAxis="A"
                    return 1
                elif clickwdgdNode[3] is True and self.AreleaseDragAxis==0:
                    self.AreleaseDragAxis=1
                    self.w_userData.ActiveAxis="A"
                    if (hasattr(self.linkToFreeCADObj,"X")):
                        #Draft Point
                        self.linkToFreeCADObj.X=newPosition.x
                        self.linkToFreeCADObj.Y=newPosition.y
                        self.linkToFreeCADObj.Z=newPosition.z
                    else:
                        #other objects if they are not like Point :TODO: FIXME: Don't know if this is correct
                        self.linkToFreeCADObj.Placement.Base=newPosition                
                    self.w_vector[0]=newPosition                   
                    self.w_ball_cb_(self.w_userData)
                    return 1
                elif self.AreleaseDragAxis==1:
                    #continue drag 
                    if (hasattr(self.linkToFreeCADObj,"X")):
                        #Draft Point
                        self.linkToFreeCADObj.X=newPosition.x
                        self.linkToFreeCADObj.Y=newPosition.y
                        self.linkToFreeCADObj.Z=newPosition.z
                    else:
                        #other objects if they are not like Point :TODO: FIXME: Don't know if this is correct
                        self.linkToFreeCADObj.Placement.Base=newPosition                
                    self.w_vector[0]=newPosition                   
                    self.w_ball_cb_(self.w_userData)
                    self.redraw()
                    return 1         
            return 0 

        except Exception as err:
            App.Console.PrintError("'handle ball3arrows' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw(self):
        """
        Main draw function. It is responsible for creating the node,
        and draw the ball on the screen. It creates a node for each 
        element and for each ball.
        """
        try:
            if (len(self.w_vector) < 2):
                raise ValueError('Must be 2 vector at least')

            usedColor = self.w_color
            if self.is_active() and self.has_focus():
                usedColor = self.w_selColor
            elif self.is_active() and (self.has_focus() != 1):
                pass  # usedColor = self.w_color  we did that already ..just for reference
            elif self.is_active() != 1:
                usedColor = self.w_inactiveColor

            XpreRotVal = [0.0, 90.0, 0.0]   # pre-Rotation
            YpreRotVal = [0.0, 90.0, 90.0]  # pre-Rotation
            ZpreRotVal = [0.0, 0.0, 0.0]
            if not self.is_visible():
                return
            self.w_XarrowSeparator = draw_2Darrow(App.Vector(self.w_vector[0].x + self.distanceBetweenThem, self.w_vector[0].y, self.w_vector[0].z),
                                                    # default FR_COLOR.FR_RED
                                                    usedColor[0], self.w_Scale, self.DrawingType, self.Opacity, XpreRotVal)
            self.w_YarrowSeparator = draw_2Darrow(App.Vector(self.w_vector[0].x, self.w_vector[0].y + self.distanceBetweenThem, self.w_vector[0].z),
                                                    # default FR_COLOR.FR_GREEN
                                                    usedColor[1], self.w_Scale, self.DrawingType, self.Opacity, YpreRotVal)
            self.w_ZarrowSeparator = draw_2Darrow(App.Vector(self.w_vector[0].x, self.w_vector[0].y, self.w_vector[0].z + self.distanceBetweenThem),
                                                    # default FR_COLOR.FR_BLUE
                                                    usedColor[2], self.w_Scale, self.DrawingType, self.Opacity, ZpreRotVal)

            self.w_BallSeparator=draw_ball(self.w_vector,FR_COLOR.FR_RED,self.ballScale,)
            #Remove all drawings and label
            self.removeSoNodes()

            self.draw_label(usedColor[0])
            
            self.saveSoNodesToWidget([self.w_XarrowSeparator,
                                        self.w_YarrowSeparator,
                                        self.w_ZarrowSeparator,self.w_BallSeparator])

            # add SoSeparator to the switch
            # We can put them in a tuple but it is better not doing so
            self.addSoNodeToSoSwitch(self.w_widgetSoNodes)
            self.addSoNodeToSoSwitch(self.w_widgetlblSoNodes)

        except Exception as err:
            App.Console.PrintError("'draw Fr_one_Arrow_widget' Failed. "
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

    def show(self):
        """[This function will show the widget. But it doesn't draw it. ]
        """
        self.w_visible = 1
        self.w_wdgsoSwitch.whichChild = coin.SO_SWITCH_ALL  # Show all children

    def take_focus(self):
        """
        Set focus to the widget. Which should redraw it also.
        """
        if self.w_hasFocus == 1:
            return  # nothing to do here
        self.w_hasFocus = 1
        self.redraw()

    def activate(self):
        """[Activate the widget so it can take events]

        """
        if self.w_active:
            return  # nothing to do
        self.w_active = 1
        self.redraw()

    def deactivate(self):
        """
        Deactivate the widget. which causes that no handle comes to the widget
        """
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
            App.Console.PrintError("'del fr_ball_three_arrows' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def hide(self):
        """[Hide the widget - but the widget is not destroyed]

        Returns:
            [type]: [description]
        """
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

    def resize(self, _scale: tuple = [1.0, 1.0, 1.0]):
        """Resize the widget by using the new vectors"""
        self.w_Scale = _scale
        self.redraw()

    def size(self, _scale: tuple = [1.0, 1.0, 1.0]):
        """[Scale the widget for the three directions]

        Args:
            _scale (tuple, Three float values): [Scale the widget using three float values for x,y,z axis]. 
            Defaults to [1.0, 1.0, 1.0].
        """
        self.resize(_scale)

    def label(self, newlabel):
        self.w_label = newlabel

    # Keep in mind you must run lblRedraw
    def label_font(self, name="sans"):
        """[Change Label Font]

        Args:
            name (str, optional): [Change label font]. Defaults to "sans".
        """
        self.w_lbluserData.fontName = name

    # Keep in mind you must run lblRedraw
    def label_fontsize(self, newsize=1):
        """[Change label font size ]

        Args:
            newsize (int, optional): [Change fontsize of the label ]. Defaults to 1.
        """
        self.w_lbluserData.fontsize = newsize

    # Must be App.Vector
    def label_move(self, newPos=App.Vector(0.0, 0.0, 0.0)):
        """[Move location of the label]
        
        Args:
            newPos ([App.Vector], optional): [Change placement of the label]. Defaults to App.Vector(0.0, 0.0, 0.0).
        """
        self.w_lbluserData.vectors = [newPos, ]