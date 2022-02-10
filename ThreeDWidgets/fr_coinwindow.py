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

__updated__ = '2022-02-10 21:25:00'


@dataclass
class mouseDimension:
    
    """[Static variables used for keeping mouse coordinators and position]
    """
    __slots__ = ['Coin_x', 'Coin_y', 'Coin_z', 'Qt_x','Qt_y','pos']
    def __init__(self):
        self.Coin_x = None
        self.Coin_y = None
        self.Coin_z = None
        self.Qt_x = None
        self.Qt_y = None
        self.pos = None


# Implementation of double click detection


# get Object under mouse


class Fr_CoinWindow(fr_group.Fr_Group):
    """
    Main window which acts like a server for the children. 
    It distribute the events, keep track of adding switches to
    the SceneGraph. Switches keep track of nodes and their 
    drawing. So the tree is like that SceneGraph-->Switches->Node->drawings
    """
    # This is the holder of all objects.It should be here not inside the Fr_Group
    # this is the root scenegraph. It keeps all switch. Switches will keep drawing
    w_countMouseCLICK = 0.0
    def __init__(self, vectors: List[App.Vector] = [App.Vector(0, 0, 0), App.Vector(
            400, 400, 0)], label: str = [[]]):
        super().__init__(vectors, label)
        self.w_view =  Gui.ActiveDocument.ActiveView
        self.callbackMove = None
        self.callbackClick = None
        self.callbackKey = None
        self.Root_SceneGraph = None

        # This should keep the mouse pointer position on the 3D view
        # from old-fr_coin3d
        self.w_lastEvent = FR_EVENTS.FR_NO_EVENT
        self.w_lastEventXYZ = mouseDimension()
        Fr_CoinWindow.w_countMouseCLICK = 0
        self.w_clicked_time = 0
        self.w_typeofevent = None
        self.w_get_event = None
        self.w_events = None
        self.w_e_state = None  # Keep the CTL,SHIFT, ALT KEY SAVED HERE

        self.Root_SceneGraph = self.w_view.getSceneGraph()
        self.w_mainfrCoinWindow = self
        self.w_parent = self  # No parent and this is the main window
        self.w_widgetType = FR_WidgetType.FR_COINWINDOW


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
        self.w_view = Gui.ActiveDocument.ActiveView
        self.addCallbacks()
        self.draw()
        super().show()  # Show all children also

    def __del__(self):
        """
        Class destructor 
        Like exit in normal window. This will end the windows
        """
        self.hide()
        if self.link_to_Fr_CoinWindow is not None:
            del self.link_to_Fr_CoinWindow
            self.link_to_Fr_CoinWindow = None
        super().__del__()  # call group destructor
        # Call Fr_Groups deactivate to remove all widgets.

    # Remove the switches and their children.
    def removeSoSwitchFromSceneGraph(self, _soSwitch):
        """ remove switch tree from the SceneGraph"""
        if type(_soSwitch) == list:
            for i in _soSwitch:
                self.Root_SceneGraph.removeChild(i)
        else:
            self.Root_SceneGraph.removeChild(_soSwitch)

    def callback(self, data):
        # not sure what I should do here yet.
        pass

    def addSoSwitchToSceneGraph(self, _soSwitch):
        """ Add new switch tree to the SceneGraph"""
        if type(_soSwitch) == list:
            for i in _soSwitch:
                self.Root_SceneGraph.addChild(
                    i)  # add scene to the root
        else:
            self.Root_SceneGraph.addChild(_soSwitch)

    ##########         FROM COIN3D                  #################

   # COIN3D related functions - START
    def shiftwasclicked(self):
        """
        if shift was pushed but not released this function will return TRUE
        """
        result = (self.w_e_state == coin.SoKeyboardEvent.LEFT_SHIFT)
        result = result or (self.w_e_state ==
                            coin.SoKeyboardEvent.RIGHT_SHIFT)
        return (result)

    def ctrlwasclicked(self):
        """
        if CTRL was pushed but not released this function will return TRUE
        """
        result = (self.w_e_state == coin.SoKeyboardEvent.LEFT_CONTROL)
        result = result or (
            self.w_e_state == coin.SoKeyboardEvent.RIGHT_CONTROL)
        return (result)

    def altwasclicked(self):
        """
        if ALT was pushed but not released this function will return TRUE
        """
        result = (self.w_e_state == coin.SoKeyboardEvent.LEFT_ALT)
        result = result or (self.w_e_state ==
                            coin.SoKeyboardEvent.RIGHT_ALT)
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
            raise NotImplementedError()  # will not be uses  2021-04-02

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
            # if we hade mouse drag or push (not release) and there is a movement
            if(self.w_lastEvent == FR_EVENTS.FR_MOUSE_LEFT_PUSH or self.w_lastEvent == FR_EVENTS.FR_MOUSE_DRAG):
                self.w_lastEvent = FR_EVENTS.FR_MOUSE_DRAG
            else:
                self.w_lastEvent = FR_EVENTS.FR_MOUSE_MOVE

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
            self.w_lastEvent = FR_EVENTS.FR_NO_EVENT
            if eventState == coin.SoMouseButtonEvent.DOWN and getButton == coin.SoMouseButtonEvent.BUTTON1:
                # detect double click here. COIN3D has no function for that
                if self.Detect_DblClick() is True:
                    self.w_lastEvent = FR_EVENTS.FR_MOUSE_LEFT_DOUBLECLICK
                else:
                    self.w_lastEvent = FR_EVENTS.FR_MOUSE_LEFT_PUSH

            elif eventState == coin.SoMouseButtonEvent.UP and getButton == coin.SoMouseButtonEvent.BUTTON1:
                self.w_lastEvent = FR_EVENTS.FR_MOUSE_LEFT_RELEASE

            elif eventState == coin.SoMouseButtonEvent.DOWN and getButton == coin.SoMouseButtonEvent.BUTTON2:
                self.w_lastEvent = FR_EVENTS.FR_MOUSE_RIGHT_PUSH

            elif eventState == coin.SoMouseButtonEvent.UP and getButton == coin.SoMouseButtonEvent.BUTTON2:
                self.w_lastEvent = FR_EVENTS.FR_MOUSE_RIGHT_RELEASE

            elif eventState == coin.SoMouseButtonEvent.DOWN and getButton == coin.SoMouseButtonEvent.BUTTON3:
                self.w_lastEvent = FR_EVENTS.FR_MOUSE_MIDDLE_PUSH

            elif eventState == coin.SoMouseButtonEvent.UP and getButton == coin.SoMouseButtonEvent.BUTTON3:
                self.w_lastEvent = FR_EVENTS.FR_MOUSE_MIDDLE_RELEASE

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
            # print("Key-Event")
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
                    self.w_lastEvent = key

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
        self.handle(self.w_lastEvent)

    def Detect_DblClick(self):
        """[Detect double click. If user clicks the object two times between 0 to 0.5 sec, 
            this had to be counted as a double click]

        Returns:
            [Boolean]: [True if double click was detected and false otherwise]
        """
        t = time.time()
        if (t - self.w_clicked_time) <= 0.500:   # suitable value must be found 500msec is windows default
            Fr_CoinWindow.w_countMouseCLICK += 1
        else:
            Fr_CoinWindow.w_countMouseCLICK = 0
            self.w_clicked_time = time.time()
        #First time it is zero, double click MUST BE 1 not 2
        if Fr_CoinWindow.w_countMouseCLICK == 1:
            return True
        else:
            Fr_CoinWindow.w_countMouseCLICK = 0
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
        self.callbackMove = self.w_view.addEventCallbackPivy(
            coin.SoLocation2Event.getClassTypeId(), self.eventProcessor)
        self.callbackClick = self.w_view.addEventCallbackPivy(
            coin.SoMouseButtonEvent.getClassTypeId(), self.eventProcessor)
        self.callbackKey = self.w_view.addEventCallbackPivy(
            coin.SoKeyboardEvent.getClassTypeId(), self.eventProcessor)

    def objectUnderMouse_Coin3d(self, win):
        pass
    # get Object clicked in COIN3D

    # TODO: At the moment, we implement only Fr_CoinWindow for COIN3D,
    #       the remained must be implemented later

    def objectMouseClick_Coin3d(self, mouse_pos, pick_radius, TargetNode):
        # This section is from DRAFT
        # It must help in finding the correct node
        # which represent the widget.
        """[Get the node from given mouse / screen position.]

        Args:
            mouse_pos ([type]): [mouse position clicked or mouse is over the position]
            pick_radius ([tuple]): [ Radius of the circle where the mouse position is surrounded by]
            TargetNode ([SoSeparator]): [coin SoSeparator]

        Returns:
            [SoSeparator]: [Return the coin object if it is found. None if not found]
        """
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

    def __del__(self):
        ''' 
        class destructor. 
        Remove all callbacks. 
        '''
        self.removeCallbacks()
