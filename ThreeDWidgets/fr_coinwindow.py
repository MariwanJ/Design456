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
import pivy.coin as coin
from ThreeDWidgets import fr_group
from typing import List
from ThreeDWidgets.constant import FR_WidgetType
from ThreeDWidgets.constant import FR_EVENTS
from dataclasses import dataclass
import time  # For double click detection



'''
This is a class for coin3D Window
'''

@dataclass
class mouseDimension:
    global Coin_x
    global Coin_y
    global Coin_z
    global Qt_x
    global Qt_y
    global pos


# Implementation of double click detection


# get Object under mouse

def objectUnderMouse_Coin3d(self, win):
    pass
# get Object clicked in COIN3D


def objectMouseClick_Coin3d(mouse_pos, pick_radius, TargetNode):
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



    if picked_point is not None and picked_point != 0:
        path = picked_point.getPath()
        if type(TargetNode) == list:
            for nodeInList in TargetNode:
                if path.containsNode(nodeInList):
                    # print("found",nodeInList)
                    # Not sure if we need it #TODO should we return only true?
                    return (path.getNode(path.findNode(nodeInList)))
            return None  # Not found
        else:
            if path.containsNode(TargetNode):
                # Not sure if we need it #TODO should we return only true?
                return (path.getNode(path.findNode(TargetNode)))
    else:
        return None

# TODO: At the moment, we implement only Fr_CoinWindow for COIN3D, 
#       the remained must be implemented later



class Fr_CoinWindow(fr_group.Fr_Group):
    """
    Main window which acts like a server for the children. 
    It distribute the events, keep track of adding switches to
    the SceneGraph. Switches keep track of nodes and their 
    drawing. So the tree is like that SceneGraph-->Switches->Node->drawings
    """
    # This is the holder of all objects.It should be here not inside the Fr_Group
    # this is the root scenegraph. It keeps all switch. Switches will keep drawing
    from ThreeDWidgets.fr_coin3d import Fr_CoinWindow
    Root_SceneGraph = None
    view = None

    # This should keep the mouse pointer position on the 3D view 
    #from fr_coin3d
    w_lastEvent = None
    w_lastEventXYZ = None
    w_view = None
    w_wind = None
    w_countMouseCLICK = 0
    w_clicked_time = 0
    w_typeofevent = None
    w_get_event = None
    w_events = None
    w_e_state = None  # Keep the CTL,SHIFT, ALT KEY SAVED HERE

    def __init__(self, vectors: List[App.Vector] = [App.Vector(0, 0, 0), App.Vector(
            400, 400, 0)], label: str = [[]]):
        super().__init__(vectors, label)
        
        self.callbackMove = None
        self.callbackClick = None
        self.callbackKey = None
        Fr_CoinWindow.w_lastEvent = FR_EVENTS.FR_NO_EVENT
        Fr_CoinWindow.w_lastEventXYZ = mouseDimension()
        Fr_CoinWindow.w_view = Gui.ActiveDocument.ActiveView
        self.addCallbacks()

        Fr_CoinWindow.Root_SceneGraph = Gui.ActiveDocument.ActiveView.getSceneGraph()
        self.w_mainfrCoinWindow = self
        self.w_parent = self  # No parent and this is the main window
        self.w_widgetType = FR_WidgetType.FR_COINWINDOW

        Fr_CoinWindow.addCallbacks()

        # Activate the window

    def show(self):
        """
        Show the window on the 3D World
        Normally if you don't have any widget, 
        this will draw nothing. But the callbacks
        will be created. Fr_CoinWindow will 
        not have any boarder,label or drawing by itself.
        The purpose of this object is to keep the children, 
        distribute events and other things that might be added 
        later to this class.
        """
        Fr_CoinWindow.view = Gui.ActiveDocument.ActiveView
        self.draw()
        super().show()  # Show all children also

    def __del__(self):
        """
        Class destructor 
        Like exit in normal window. This will end the windows
        """
        self.hide()
        if Fr_CoinWindow.link_to_Fr_CoinWindow is not None:
            del Fr_CoinWindow.link_to_Fr_CoinWindow
            Fr_CoinWindow.link_to_Fr_CoinWindow = None
        super().__del__()  # call group destructor
        # Call Fr_Groups deactivate to remove all widgets.

    # Remove the switches and their children.
    def removeSoSwitchFromSceneGraph(self, _soSwitch):
        """ remove switch tree from the SceneGraph"""
        if type(_soSwitch) == list:
            for i in _soSwitch:
                Fr_CoinWindow.Root_SceneGraph.removeChild(i)
        else:
            Fr_CoinWindow.Root_SceneGraph.removeChild(_soSwitch)

    def callback(self, data):
        # not sure what I should do here yet.
        pass

    def addSoSwitchToSceneGraph(self, _soSwitch):
        """ Add new switch tree to the SceneGraph"""
        if type(_soSwitch) == list:
            for i in _soSwitch:
                Fr_CoinWindow.Root_SceneGraph.addChild(
                    i)  # add scene to the root
        else:
            Fr_CoinWindow.Root_SceneGraph.addChild(_soSwitch)

    ##########         FROM COIN3D                  #################

   # COIN3D related functions - START
    def shiftwasclicked(self):
        """
        if shift was pushed but not released this function will return TRUE
        """
        result = (Fr_CoinWindow.w_e_state == coin.SoKeyboardEvent.LEFT_SHIFT)
        result = result or (Fr_CoinWindow.w_e_state ==
                            coin.SoKeyboardEvent.RIGHT_SHIFT)
        return (result)

    def ctrlwasclicked(self):
        """
        if CTRL was pushed but not released this function will return TRUE
        """
        result = (Fr_CoinWindow.w_e_state == coin.SoKeyboardEvent.LEFT_CONTROL)
        result = result or (
            Fr_CoinWindow.w_e_state == coin.SoKeyboardEvent.RIGHT_CONTROL)
        return (result)

    def altwasclicked(self):
        """
        if ALT was pushed but not released this function will return TRUE
        """
        result = (Fr_CoinWindow.w_e_state == coin.SoKeyboardEvent.LEFT_ALT)
        result = result or (Fr_CoinWindow.w_e_state ==
                            coin.SoKeyboardEvent.RIGHT_ALT)
        return (result)
        # COIN3D related functions -END

    def eventProcessor(self, events):
        Fr_CoinWindow.w_events = events
        Fr_CoinWindow.w_get_event = Fr_CoinWindow.w_events.getEvent()
        Fr_CoinWindow.w_typeofevent = type(Fr_CoinWindow.w_get_event)

        # write down all possible events.
        # First mouse move event

        if(Fr_CoinWindow.w_typeofevent == coin.SoMotion3Event):
            """ represents 3D relative motion events in the 
                Open Inventor event model.
                sub functions: 
                getTranslation()          # Gets the relative change in translation since the last translation event.
                setRotation(SbRotation r) # Sets the relative change in rotation since the last rotation event.
                setTranslation(SbVec3f t) # Sets the relative change in translation since the last translation event.
                SbRotation getRotation()  #Gets the relative change in rotation since the last rotation event.
            """
            raise NotImplementedError()  # will not be uses  2021-04-02

        elif(Fr_CoinWindow.w_typeofevent == coin.SoLocation2Event):
            """ 2D location events. SoLocation2Event represents 2D location events, for example, mouse move events """
            Fr_CoinWindow.w_lastEventXYZ.pos = Fr_CoinWindow.w_get_event.getPosition()
            pos = Fr_CoinWindow.w_lastEventXYZ.pos.getValue()
            pnt = Fr_CoinWindow.w_view.getPoint(pos[0], pos[1])
            Fr_CoinWindow.w_lastEventXYZ.Coin_x = pnt.x
            Fr_CoinWindow.w_lastEventXYZ.Coin_y = pnt.y
            Fr_CoinWindow.w_lastEventXYZ.Coin_z = pnt.z
            Fr_CoinWindow.w_lastEventXYZ.Qt_x = pos[0]
            Fr_CoinWindow.w_lastEventXYZ.Qt_y = pos[1]
            # if we hade mouse drag or push (not release) and there is a movement
            if(Fr_CoinWindow.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_PUSH or Fr_CoinWindow.w_lastEvent == FR_EVENTS.FR_MOUSE_DRAG):
                Fr_CoinWindow.w_lastEvent = FR_EVENTS.FR_MOUSE_DRAG
            else:
                Fr_CoinWindow.w_lastEvent = FR_EVENTS.FR_MOUSE_MOVE

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

        elif(Fr_CoinWindow.w_typeofevent == coin.SoMouseButtonEvent):
            """
            Mouse button press and release events.
            SoMouseButtonEvent represents mouse button press and release
            """
            eventState = Fr_CoinWindow.w_get_event.getState()  # pressed down , or it is released
            getButton = Fr_CoinWindow.w_get_event.getButton()
            Fr_CoinWindow.w_lastEvent = FR_EVENTS.FR_NO_EVENT
            if eventState == coin.SoMouseButtonEvent.DOWN and getButton == coin.SoMouseButtonEvent.BUTTON1:
                # detect double click here. COIN3D has no function for that
                if self.Detect_DblClick() is True:
                    Fr_CoinWindow.w_lastEvent = FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK
                else:
                    Fr_CoinWindow.w_lastEvent = FR_EVENTS.FR_MOUSE_LEFT_PUSH

            elif eventState == coin.SoMouseButtonEvent.UP and getButton == coin.SoMouseButtonEvent.BUTTON1:
                Fr_CoinWindow.w_lastEvent = FR_EVENTS.FR_MOUSE_LEFT_RELEASE

            elif eventState == coin.SoMouseButtonEvent.DOWN and getButton == coin.SoMouseButtonEvent.BUTTON2:
                Fr_CoinWindow.w_lastEvent = FR_EVENTS.FR_MOUSE_RIGHT_PUSH

            elif eventState == coin.SoMouseButtonEvent.UP and getButton == coin.SoMouseButtonEvent.BUTTON2:
                Fr_CoinWindow.w_lastEvent = FR_EVENTS.FR_MOUSE_RIGHT_RELEASE

            elif eventState == coin.SoMouseButtonEvent.DOWN and getButton == coin.SoMouseButtonEvent.BUTTON3:
                Fr_CoinWindow.w_lastEvent = FR_EVENTS.FR_MOUSE_MIDDLE_PUSH

            elif eventState == coin.SoMouseButtonEvent.UP and getButton == coin.SoMouseButtonEvent.BUTTON3:
                Fr_CoinWindow.w_lastEvent = FR_EVENTS.FR_MOUSE_MIDDLE_RELEASE

        # Take care of Keyboard events
        elif (Fr_CoinWindow.w_typeofevent == coin.SoKeyboardEvent):
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
            # print("Key-Event")
            key = ""
            try:
                key = Fr_CoinWindow.w_get_event.getKey()
                # Take care of CTRL,SHIFT,ALT Only when it is down.
                # We don't send the shift key ..
                test = (key == coin.SoKeyboardEvent.LEFT_CONTROL and Fr_CoinWindow.w_get_event.getState(
                ) == coin.SoButtonEvent.DOWN)
                test = test or (key == coin.SoKeyboardEvent.RIGHT_CONTROL and Fr_CoinWindow.w_get_event.getState(
                ) == coin.SoButtonEvent.DOWN)
                test = test or (key == coin.SoKeyboardEvent.LEFT_SHIFT and Fr_CoinWindow.w_get_event.getState(
                ) == coin.SoButtonEvent.DOWN)
                test = test or (key == coin.SoKeyboardEvent.RIGHT_SHIFT and Fr_CoinWindow.w_get_event.getState(
                ) == coin.SoButtonEvent.DOWN)
                test = test or (key == coin.SoKeyboardEvent.LEFT_ALT and Fr_CoinWindow.w_get_event.getState(
                ) == coin.SoButtonEvent.DOWN)
                test = test or (key == coin.SoKeyboardEvent.RIGHT_ALT and Fr_CoinWindow.w_get_event.getState(
                ) == coin.SoButtonEvent.DOWN)
                if test == 1:
                    Fr_CoinWindow.w_e_state = key
                else:
                    # Take care of all other keys.
                    Fr_CoinWindow.w_e_state = None
                    Fr_CoinWindow.w_lastEvent = key

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

        # Now send the event to th window widget to distribute it over the children widgets
        Fr_CoinWindow.w_wind.handle(Fr_CoinWindow.w_lastEvent)

    def Detect_DblClick(self):
        t = time.time()
        if t - Fr_CoinWindow.w_clicked_time <= 0.500:   # suitable value must be found 500msec is windows default
            Fr_CoinWindow.w_countMouseCLICK += 1
        else:
            Fr_CoinWindow.w_countMouseCLICK = 0
            Fr_CoinWindow.w_clicked_time = time.time()
        if Fr_CoinWindow.w_countMouseCLICK == 2:
            return True
        else:
            return False

    def removeCallbacks(self):
        '''
        Remove all callbacks registered for Fr_Window widget
        '''
        Fr_CoinWindow.w_view.removeEventCallbackPivy(
            coin.SoLocation2Event.getClassTypeId(), self.callbackMove)
        Fr_CoinWindow.w_view.removeEventCallbackPivy(
            coin.SoMouseButtonEvent.getClassTypeId(), self.callbackClick)
        Fr_CoinWindow.w_view.removeEventCallbackPivy(
            coin.SoKeyboardEvent.getClassTypeId(), self.callbackKey)

    def addCallbacks(self):
        '''
        add all callbacks registered for Fr_Window widget
        '''
        Fr_CoinWindow.callbackMove = Fr_CoinWindow.w_view.addEventCallbackPivy(
            coin.SoLocation2Event.getClassTypeId(), self.eventProcessor)
        Fr_CoinWindow.callbackClick = Fr_CoinWindow.w_view.addEventCallbackPivy(
            coin.SoMouseButtonEvent.getClassTypeId(), self.eventProcessor)
        Fr_CoinWindow.callbackKey = Fr_CoinWindow.w_view.addEventCallbackPivy(
            coin.SoKeyboardEvent.getClassTypeId(), self.eventProcessor)

    def __del__(self):
        ''' 
        class destructor. 
        Remove all callbacks. 
        '''
        self.removeCallbacks()
