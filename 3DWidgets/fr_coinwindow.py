# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from fr_group import Fr_Group
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

import os, sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import Design456Init
import fr_group
import fr_widget
import constant


class mouseDimension:
    Coin_x = 0
    Coin_y = 0
    Coin_z = 0
    Qt_x = 0
    Qt_y = 0

'''
This is a class for coin3D Window

'''
class Fr_CoinWindow(fr_group.Fr_Group):
    __view = None
    __lastEvent = None
    __lastKeyEvent = []  # Might be more than one key.
    # This should keep the mouse pointer position on the 3D view
    __lastEventXYZ = mouseDimension()

    def __init__(self, x, y, z, h, w, t, l):
        super().__init__(x, y, z, h, w, t, l)
        __view = Gui.ActiveDocument.ActiveView
        self.addCallbacks

    def removeCallbacks(self):
        pass

    def addCallbacks(self):
        self.callback = self.view.addEventCallbackPivy(
            coin.SoMouseButtonEvent.getClassTypeId(), self.handle)  # Mouse buttons
        self.callback = self.view.addEventCallbackPivy(
            coin.SoKeyboardEvent.getClassTypeId(), self.handle)     # Keyboard
        self.view.removeEventCallbackPivy(coin.SoLocation2Event.getClassTypeId(
        ), self.handle(events))                # Mouse Move

    # All event come to this function. We classify the event to be processed by each widget later.

    def handle(self, events):
        # write down all possible events.
        getEvent = events.getEvent()
        if (type(getEvent) == coin.SoMouseButtonEvent):
            if (type(getEvent) == coin.SoMouseButtonEvent and getEvent.getState() == coin.SoMouseButtonEvent.DOWN and getEvent.getButton() == coin.SoMouseButtonEvent.BUTTON1):
                lastEvent = constant.Fr_Events.MOUSE_LEFT_CLICK
            if (type(getEvent) == coin.SoMouseButtonEvent and getEvent.getState() == coin.SoMouseButtonEvent.DOWN and getEvent.getButton() == coin.SoMouseButtonEvent.BUTTON3):
                lastEvent = constant.Fr_Events.MOUSE_MIDDLE_CLICK
            if (type(getEvent) == coin.SoMouseButtonEvent and getEvent.getState() == coin.SoMouseButtonEvent.DOWN and getEvent.getButton() == coin.SoMouseButtonEvent.BUTTON2):
                lastEvent = constant.Fr_Events.MOUSE_RIGHT_CLICK
               # mouse movement
        elif (type(event) == coin.SoLocation2Event):
            pos = Gui.ActiveDocument.ActiveView.getCursorPos()
            pnt = self.view.getPoint(pos)
            __lastEventXYZ.coin_x = pnt.x
            __lastEventXYZ.coin_y = pnt.y
            __lastEventXYZ.coin_z = pnt.z
            __lastEventXYZ.Qt_x = pos[0]
            __lastEventXYZ.Qt_y = pos[1]
        # Take care of Keyboard events
        elif (type(event) == coin.SoKeyboardEvent):
            key = ""
            try:
                key = event.getKey()
            # Take care of CTRL,SHIFT,ALT
                if (key == coin.SoKeyboardEvent.LEFT_CONTROL or coin.SoKeyboardEvent.RIGHT_CONTROL) and event.getState() == coin.SoButtonEvent.DOWN:
                    __lastKeyEvent.append(key)
                elif(key == coin.SoKeyboardEvent.LEFT_SHIFT or coin.SoKeyboardEvent.RIGHT_SHIFT) and event.getState() == coin.SoButtonEvent.DOWN:
                    __lastKeyEvent.append(key)
                elif(key == coin.SoKeyboardEvent.LEFT_ALT or coin.SoKeyboardEvent.RIGHT_ALT) and event.getState() == coin.SoButtonEvent.DOWN:
                    __lastKeyEvent.append(key)
                # Take care of all other keys.
                if(event.getState() == coin.SoButtonEvent.UP):
                    _lastKeyEvent.append(key)
            except ValueError:
                # there is no character for this value
                key = ""

            """
                When handle return 1, it means that the widgets (child) used the event
                No more widgets should get the event. Coin can use the rest of the event
                if that is required.
                If an object is not active, the event will not reach it.
                or if it is not visible.
                Be aware that the EVENT must be inside the dimension of the widget.
                Since parent don't know that directly. Widget itself should take care
                of that. You must check that always.
            """
            for wdg in self._widgets:
                if wdg.active() and wdg.visible():
                    if wdg.handel(events) == 1:
                        break
    '''
        Remove all callbacks registered for Fr_Window widget
    '''

    def checkIfEventIsRelevantForWidget(self, widget):
        if __lastEventXYZ.x >= widget.x and __lastEventXYZ.x <= (widget.x+widget.w) and __lastEventXYZ.y >= widget.y and __lastEventXYZ.y <= (widget.y+widget.h) and __lastEventXYZ.z >= widget.z and __lastEventXYZ.z <= (widget.z+widget.t):
            return True
        else:
            return False

    def exitFr_Window(self):
        self.view.removeEventCallbackPivy(
            coin.SoKeyboSoMouseButtonEvent.getClassTypeId(), self.event_process)
        self.view.removeEventCallbackPivy(
            coin.SoKeyboardEvent.getClassTypeId(), self.event_process)
        self.view.removeEventCallbackPivy(
            coin.SoLocation2Event.getClassTypeId(), self.event_process)
    
    def draw(self):
        super().draw()
        '''For this object itself, it will not have any real drawing. 
         It will keep control of drawing the children but itself, nothing
         will be drawn.  
         '''
    def hide(self):
        print("Not implemented")
        
    def addChild(self,childWdg):
        self._widgets.append(childWdg)

    def show(self):
        self.draw()
        
    def removeChild(self,childWdg):
        try:
            self._widgets.remove(childWdg)
        except:
            print("not found")