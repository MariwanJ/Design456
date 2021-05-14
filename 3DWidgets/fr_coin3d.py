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
This file will contain all event, handle, constants related to the interactive
part of the new widgets. It will keeps the events and translate them
to the desired standardized names.
Events will be defined here, mouse position will be saved here, last event..etc.
To understand how I think in making this widgets, please consider reading about
the FLTK toolkit. This is a flavour of https://www.fltk.org/.
Notice that we have two different windows system. One is for the Coin3D and 
the other is for QT Widget. 
That is why you will see different definitions here for each system.
This is only for coin3D. 
"""
# Struct to keep the mouse position in both world

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import Design456Init
import constant
from dataclasses import dataclass
import time # For double click detection

@dataclass
class mouseDimension:
    global Coin_x
    global Coin_y
    global Coin_z
    global Qt_x
    global Qt_y
    global pos


#Implementation of double click detection
import time
import threading

# get Object under mouse

def objectUnderMouse_Coin3d(self, win):
    pass
# get Object clicked in COIN3D


def objectMouseClick_Coin3d(mouse_pos, pick_radius,TargetNode):
    # This section is from DRAFT
    # It must help in finding the correct node
    # which represent the widget.
    """Get edit node from given screen position."""
    viewer = Gui.ActiveDocument.ActiveView.getViewer()
    render_manager = viewer.getSoRenderManager()
    ray_pick = coin.SoRayPickAction(render_manager.getViewportRegion())
    ray_pick.setPoint(coin.SbVec2s(*mouse_pos))
    ray_pick.setRadius(pick_radius)
    ray_pick.setPickAll(True)
    ray_pick.apply(render_manager.getSceneGraph())
    picked_point = ray_pick.getPickedPoint()
    
    if picked_point != None and picked_point != 0:
        if type(TargetNode)==list:
            for nodeInList in TargetNode:
                path=picked_point.getPath()
                if path.containsNode(nodeInList):
                    return (path.getNode(path.findNode(nodeInList)))  #Not sure if we need it #TODO should we return only true?
            return None # Not found
        else:        
            path = picked_point.getPath()
            if path.containsNode(TargetNode):
                return (path.getNode(path.findNode(TargetNode)))  #Not sure if we need it #TODO should we return only true?
    else:
        return None


class root_handle():
    """
        The most critical part of the widgets. This will take care of 
        translating the events from COIN3D to our system.
        Both QT and COIN3D windows will call this function.
        But they will be treated differently as they are different.
    """
    # Save last mouse event
    global w_lastEvent
    global w_view
    # Keep the CTL,SHIFT, ALT KEY SAVED HERE
    global w_e_state

    callbackMove = None
    callbackClick = None
    callbackKey = None
    
    global w_events 
    global w_get_event
    global w_typeofevent
    #these two variable are used for double click detection
    global w_countMouseCLICK
    global w_clicked_time 

    # This should keep the mouse pointer position on the 3D view
    global w_lastEventXYZ

    def __init__(self):
        self.w_lastEvent = constant.FR_EVENTS.FR_NO_EVENT
        self.w_lastEventXYZ = mouseDimension()
        self.w_view = Gui.ActiveDocument.ActiveView
        self.w_wind = None
        self.addCallbacks()
        self.w_countMouseCLICK=0
        self.w_clicked_time=0
    # COIN3D related functions - START

    def shiftwasclicked(self):
        """
        if shift was pushed but not released this function will return TRUE
        """
        result = (self.w_e_state == coin.SoKeyboardEvent.LEFT_SHIFT)
        result = result or (self.w_e_state == coin.SoKeyboardEvent.RIGHT_SHIFT)
        return (result)

    def ctrlwasclicked(self):
        """
        if CTRL was pushed but not released this function will return TRUE
        """
        result = (self.w_e_state == coin.SoKeyboardEvent.LEFT_CONTROL)
        result = result or (self.w_e_state == coin.SoKeyboardEvent.RIGHT_CONTROL)
        return (result)

    def altwasclicked(self):
        """
        if ALT was pushed but not released this function will return TRUE
        """
        result = (self.w_e_state == coin.SoKeyboardEvent.LEFT_ALT)
        result = result or (self.w_e_state == coin.SoKeyboardEvent.RIGHT_ALT)
        return (result)
        # COIN3D related functions -END

    def eventProcessor(self, events):
        self.w_events = events
        self.w_get_event = self.w_events.getEvent()
        self.w_typeofevent = type(self.w_get_event)
        
        # write down all possible events.
        # First mouse move event

        if(self.w_typeofevent == coin.SoMotion3Event):
            """ represents 3D relative motion events in the 
               Open Inventor event model.
                sub functions: 
                getTranslation()          # Gets the relative change in translation since the last translation event.
                setRotation(SbRotation r) # Sets the relative change in rotation since the last rotation event.
                setTranslation(SbVec3f t) # Sets the relative change in translation since the last translation event.
                SbRotation getRotation()  #Gets the relative change in rotation since the last rotation event.
            """
            raise NotImplementedError()  # will not be uses at least now 2021-04-02

        elif(self.w_typeofevent == coin.SoLocation2Event):
            """ 2D location events. SoLocation2Event represents 2D location events, for example, mouse move events """
            self.w_lastEventXYZ.pos = self.w_get_event.getPosition()
            pos = self.w_lastEventXYZ.pos.getValue()
            pnt = self.w_view.getPoint(pos[0], pos[1])
            self.w_lastEventXYZ.Coin_x = pnt.x
            self.w_lastEventXYZ.Coin_y = pnt.y
            self.w_lastEventXYZ.Coin_z = pnt.z
            self.w_lastEventXYZ.Qt_x = pos[0]
            self.w_lastEventXYZ.Qt_y = pos[1]

        # Doesn't work, don't know why
        # elif(_typeofevent == coin.SoMouseWheelEvent):
        #   """  Mouse wheel events. SoMouseWheelEvent represents a change in
        #    mouse wheel rotation event in the Open Inventor event model.
        #    function to this event:
        #    getDelta()    # Gets the mouse wheel delta
        #
        #    """
        #    window.handle(fr.FR_MOUSEWHEEL)

        # elif(_typeofevent == coin.SoControllerButtonEvent):
        #    """
        #    Controller button press and release event.
        #    SoControllerButtonEvent represents controller button press and
        #    release events in the Open Inventor event model.
        #    A controller device generally has associated 3D tracker information.
        #    """
        #    raise NotImplementedError()  # will not be uses at least now 2021-04-02

        elif(self.w_typeofevent == coin.SoMouseButtonEvent):
            """
            Mouse button press and release events.
            SoMouseButtonEvent represents mouse button press and release
            """
            eventState = self.w_get_event.getState()  # pressed down , or it is released
            getButton = self.w_get_event.getButton()
            self.w_lastEvent = constant.FR_EVENTS.FR_NO_EVENT

            if eventState == coin.SoMouseButtonEvent.DOWN and getButton == coin.SoMouseButtonEvent.BUTTON1:
                self.w_lastEvent = constant.FR_EVENTS.FR_MOUSE_LEFT_PUSH
            if eventState == coin.SoMouseButtonEvent.UP and getButton == coin.SoMouseButtonEvent.BUTTON1:
                #detect double click here. COIN3D has no function for that
                if self.Detect_DblClick()==True:
                    self.w_lastEvent = constant.FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK
                else:
                    self.w_lastEvent = constant.FR_EVENTS.FR_MOUSE_LEFT_RELEASE

            if eventState == coin.SoMouseButtonEvent.DOWN and getButton == coin.SoMouseButtonEvent.BUTTON2:
                self.w_lastEvent = constant.FR_EVENTS.FR_MOUSE_RIGHT_PUSH
            if eventState == coin.SoMouseButtonEvent.UP and getButton == coin.SoMouseButtonEvent.BUTTON2:
                self.w_lastEvent = constant.FR_EVENTS.FR_MOUSE_RIGHT_RELEASE

            if eventState == coin.SoMouseButtonEvent.DOWN and getButton == coin.SoMouseButtonEvent.BUTTON3:
                self.w_lastEvent = constant.FR_EVENTS.FR_MOUSE_MIDDLE_PUSH
            if eventState == coin.SoMouseButtonEvent.UP and getButton == coin.SoMouseButtonEvent.BUTTON3:
                self.w_lastEvent = constant.FR_EVENTS.FR_MOUSE_MIDDLE_RELEASE
            self.w_wind.handle(self.w_lastEvent)

        # Take care of Keyboard events
        elif (self.w_typeofevent == coin.SoKeyboardEvent):
            """
            Keyboard key press and keyrelease event. 
            functions used with this event: 
            Returns:                         Function                                                    Details
            SoKeyboardEvent.Keys 	         getKey()                                                    Gets which key generated the event.
            static SoKeyboardEvent.Keys      getKeySym​(int key) 	             
            byte 	                         getPrintableCharacter()                                     Convenience routine that returns the 
                                                                                                         character representing the key, 
                                                                                                         if it's printable.
            static boolean 	                 isKeyPressEvent​(SoEvent e, SoKeyboardEvent.Keys whichKey)   Returns whether the passed event is a keyboard press event of the passed key.
            static boolean 	                 isKeyReleaseEvent​(SoEvent e, SoKeyboardEvent.Keys whichKey) Returns whether the passed event is a keyboard release event of the passed key.
            void 	                         setKey​(SoKeyboardEvent.Keys whichKey) 	                  Sets which key generated the event.
            """

            key = ""
            try:
                key = self.w_get_event.getKey()
                # Take care of CTRL,SHIFT,ALT Only when it is down.
                # We don't send the shift key ..
                test = (key == coin.SoKeyboardEvent.LEFT_CONTROL and self.w_get_event.getState(
                ) == coin.SoButtonEvent.DOWN)
                test = test or (key == coin.SoKeyboardEvent.RIGHT_CONTROL and self.w_get_event.getState(
                ) == coin.SoButtonEvent.DOWN)
                test = test or (key == coin.SoKeyboardEvent.LEFT_SHIFT and self.w_get_event.getState(
                ) == coin.SoButtonEvent.DOWN)
                test = test or (key == coin.SoKeyboardEvent.RIGHT_SHIFT and self.w_get_event.getState(
                ) == coin.SoButtonEvent.DOWN)
                test = test or (key == coin.SoKeyboardEvent.LEFT_ALT and self.w_get_event.getState(
                ) == coin.SoButtonEvent.DOWN)
                test = test or (key == coin.SoKeyboardEvent.RIGHT_ALT and self.w_get_event.getState(
                ) == coin.SoButtonEvent.DOWN)
                if test == 1:
                    self.w_e_state = key
                else:
                    # Take care of all other keys.
                    self.w_e_state = None
                self.w_wind.handle(events)

            except ValueError:
                # there is no character for this value
                key = ""

        # THE Below events will not be treated by our widget system, at least not for now 2020-04-02 Mariwan
        # elif(_typeofevent==coin.SoSpaceballButtonEvent)     :
        #
        # elif(_typeofevent==coin.SoHandleEventAction)        :
        #
        # elif(_typeofevent==coin.SoEventCallback)            :
        # elif(_typeofevent==coin.SoSelection)                :
        # elif(_typeofevent==coin.SoInteraction)              :
        # elif(_typeofevent==coin.SoWinDevice)                :
        # elif(_typeofevent==coin.SoWinRenderArea)            :
        # elif(_typeofevent==coin.SoGestureEvent)             :
        # elif(_typeofevent == coin.SoGestureEvent):
        # elif(_typeofevent) == coin.SoTouchEvent:
        # elif(_typeofevent) == coin.SoTrackerEvent:
    def Detect_DblClick(self):
        t = time.time()
        if t - self.w_clicked_time <= 0.25:
            self.w_countMouseCLICK += 1
        else:
            self.w_countMouseCLICK = 0
            self.w_clicked_time = time.time()
        if  self.w_countMouseCLICK==2:
            return True
        else:
            return False
        
    def removeCallbacks(self):
        '''
        Remove all callbacks registered for Fr_Window widget
        '''
        self.w_view.removeEventCallbackPivy(
            coin.SoLocation2Event.getClassTypeId(), self.callbackMove)
        self.w_view.removeEventCallbackPivy(
            coin.SoMouseButtonEvent.getClassTypeId(), self.callbackClick)
        self.w_view.removeEventCallbackPivy(
            coin.SoKeyboardEvent.getClassTypeId(), self.callbackKey)

    def addCallbacks(self):
        '''
        add all callbacks registered for Fr_Window widget
        '''
        print("callback activated")
        self.callbackMove = self.w_view.addEventCallbackPivy(
            coin.SoLocation2Event.getClassTypeId(), self.eventProcessor)
        self.callbackClick = self.w_view.addEventCallbackPivy(
            coin.SoMouseButtonEvent.getClassTypeId(), self.eventProcessor)
        self.callbackKey = self.w_view.addEventCallbackPivy(
            coin.SoKeyboardEvent.getClassTypeId(), self.eventProcessor)
