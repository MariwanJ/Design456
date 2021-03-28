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

import os
import sys
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

    view = Gui.ActiveDocument.ActiveView
    lastEvent = None
    lastKeyEvent = []  # Might be more than one key.
    # This should keep the mouse pointer position on the 3D view
    lastEventXYZ = mouseDimension()
    WidgetType=constant.FR_WidgetType.FR_COINWINDOW

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
        ), self.handle)                # Mouse Move

    # All event come to this function. We classify the event to be processed by each widget later.

    def handle(self, events):
        # write down all possible events.
        getEvent = events.getEvent()
        # Mouse position must be registered always
        pos = Gui.ActiveDocument.ActiveView.getCursorPos()
        pnt = self.view.getPoint(pos)
        self.lastEventXYZ.coin_x = pnt.x
        self.lastEventXYZ.coin_y = pnt.y
        self.lastEventXYZ.coin_z = pnt.z
        self.lastEventXYZ.Qt_x = pos[0]
        self.lastEventXYZ.Qt_y = pos[1]
        print("00000")
        print(self.lastEventXYZ.coin_x)
        print(self.lastEventXYZ.coin_y)
        print(self.lastEventXYZ.coin_z)
        print("00000")
        if (type(getEvent) == coin.SoMouseButtonEvent):
            if (type(getEvent) == coin.SoMouseButtonEvent and getEvent.getState() == coin.SoMouseButtonEvent.DOWN and getEvent.getButton() == coin.SoMouseButtonEvent.BUTTON1):
                lastEvent = constant.FR_EVENTS.MOUSE_LEFT_CLICK
            if (type(getEvent) == coin.SoMouseButtonEvent and getEvent.getState() == coin.SoMouseButtonEvent.DOWN and getEvent.getButton() == coin.SoMouseButtonEvent.BUTTON3):
                lastEvent = constant.FR_EVENTS.MOUSE_MIDDLE_CLICK
            if (type(getEvent) == coin.SoMouseButtonEvent and getEvent.getState() == coin.SoMouseButtonEvent.DOWN and getEvent.getButton() == coin.SoMouseButtonEvent.BUTTON2):
                lastEvent = constant.FR_EVENTS.MOUSE_RIGHT_CLICK
               # mouse movement
        # Take care of Keyboard events
        elif (type(getEvent) == coin.SoKeyboardEvent):
            key = ""
            try:
                key = getEvent.getKey()
            # Take care of CTRL,SHIFT,ALT
                if (key == coin.SoKeyboardEvent.LEFT_CONTROL or coin.SoKeyboardEvent.RIGHT_CONTROL) and getEvent.getState() == coin.SoButtonEvent.DOWN:
                    self.lastKeyEvent.append(key)
                elif(key == coin.SoKeyboardEvent.LEFT_SHIFT or coin.SoKeyboardEvent.RIGHT_SHIFT) and getEvent.getState() == coin.SoButtonEvent.DOWN:
                    self.lastKeyEvent.append(key)
                elif(key == coin.SoKeyboardEvent.LEFT_ALT or coin.SoKeyboardEvent.RIGHT_ALT) and getEvent.getState() == coin.SoButtonEvent.DOWN:
                    self.lastKeyEvent.append(key)
                # Take care of all other keys.
                if(getEvent.getState() == coin.SoButtonEvent.UP):
                    self.lastKeyEvent.append(key)
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
                Here we will distribute the event to the children
            """

        for wdg in self.children:
            if (wdg.active() and wdg.visible() and wdg.type != constant.FR_WidgetType.FR_Widget):
                if(self.checkIfEventIsRelevantForWidget(wdg)):
                    if wdg.handle(getEvent) == 1:
                        break
    '''
        Remove all callbacks registered for Fr_Window widget
    '''

    def checkIfEventIsRelevantForWidget(self, widget):
        handelV = App.Vector(self.lastEventXYZ.Coin_x,self.lastEventXYZ.Coin_y, self.lastEventXYZ.Coin_z)
        v1 = App.Vector(widget.x, widget.y, widget.z)
        v2 = App.Vector(widget.x+widget.w, widget.y +widget.h, widget.z+widget.t)
        distance = handelV.distanceToLine(handelV, v2)
        print("-----------------")
        print(handelV)
        print(v1)
        print(v2)
        print("-------------------")
        print("Distans=")
        print(distance)
        if distance == 0:
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
        # call group(parent)'s draw
        fr_group.Fr_Group.draw(self)
        '''For this object itself, it will not have any real drawing. 
         It will keep control of drawing the children but itself, nothing
         will be drawn.  
         '''

    def hide(self):
        print("Not implemented")

    def addChild(self, childWdg):
        self.children.append(childWdg)
        childWdg.parent = self

    def show(self):
        self.draw()
        self.addCallbacks()

    def removeChild(self, childWdg):
        try:
            self.children.remove(childWdg)
            self.removeCallbacks()
        except:
            print("not found")
