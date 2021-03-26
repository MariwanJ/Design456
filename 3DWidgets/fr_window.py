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

import os,sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import init
import fr_group
import fr_widget
import constant

class mouseDimension:
      Coin_x=0
      Coin_y=0
      Coin_z=0
      Qt_x=0
      Qt_y=0
      
class Fr_Window(fr_group.Fr_Group):
    __view=None
    __lastEvent=None
    __lastKeyEvent=[]                     #Might be more than one key.
    __lastEventXYZ=mouseDimension()       #This should keep the mouse pointer position on the 3D view   
    
    def __init__(self, x,y,z,h,w,t,l):
        super().__init__(x,y,z,h,w,t,l)
        __view=Gui.ActiveDocument.ActiveView
        self.addCallbacks
    
    def removeCallbacks(self):
        pass
    def addCallbacks(self):
        self.callback = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.event_process)  # Mouse buttons
        self.callback = self.view.addEventCallbackPivy(coin.SoKeyboardEvent.getClassTypeId(), self.event_process)     # Keyboard 
        self.view.removeEventCallbackPivy(coin.SoLocation2Event.getClassTypeId(), self.event_process)                # Mouse Move
        
    #All event come to this function. We classify the event to be processed by each widget later.  
    
    def event_process(self,events):
        #write down all possible events.
        getEvent = events.getEvent()
        if (type(getEvent) == coin.SoMouseButtonEvent):
            if (type(getEvent) == coin.SoMouseButtonEvent and getEvent.getState() == coin.SoMouseButtonEvent.DOWN and getEvent.getButton() == coin.SoMouseButtonEvent.BUTTON1):
                lastEvent=constant.Fr_Events.MOUSE_LEFT_CLICK
            if (type(getEvent) == coin.SoMouseButtonEvent and getEvent.getState() == coin.SoMouseButtonEvent.DOWN and getEvent.getButton() == coin.SoMouseButtonEvent.BUTTON3):
                lastEvent=constant.Fr_Events.MOUSE_MIDDLE_CLICK
            if (type(getEvent) == coin.SoMouseButtonEvent and getEvent.getState() == coin.SoMouseButtonEvent.DOWN and getEvent.getButton() == coin.SoMouseButtonEvent.BUTTON2):
                lastEvent=constant.Fr_Events.MOUSE_RIGHT_CLICK
               #mouse movement        
        elif (type(event) == coin.SoLocation2Event):
            pos = Gui.ActiveDocument.ActiveView.getCursorPos()
            pnt = self.view.getPoint(pos)
            __lastEventXYZ.coin_x=pnt.x
            __lastEventXYZ.coin_y=pnt.y
            __lastEventXYZ.coin_z=pnt.z
            __lastEventXYZ.Qt_x=pos[0]
            __lastEventXYZ.Qt_y=pos[1]
        #Take care of Keyboard events     
        elif (type(event) == coin.SoKeyboardEvent):
            key = ""
            try:
                key = event.getKey()
            #Take care of CTRL,SHIFT,ALT
                if (key == coin.SoKeyboardEvent.LEFT_CONTROL or coin.SoKeyboardEvent.RIGHT_CONTROL ) and event.getState() == coin.SoButtonEvent.DOWN:
                    __lastKeyEvent.append(key)
                elif(key == coin.SoKeyboardEvent.LEFT_SHIFT or coin.SoKeyboardEvent.RIGHT_SHIFT ) and event.getState() == coin.SoButtonEvent.DOWN:
                    __lastKeyEvent.append(key)
                elif(key == coin.SoKeyboardEvent.LEFT_ALT or coin.SoKeyboardEvent.RIGHT_ALT ) and event.getState() == coin.SoButtonEvent.DOWN:
                    __lastKeyEvent.append(key)
                #Take care of all other keys.
                if(event.getState() == coin.SoButtonEvent.UP):
                    _lastKeyEvent.append(key)
            except ValueError:
                # there is no character for this value
                key = ""
 
            for wdg in self._widgets:
                if wdg.isActive():
                    wdg.handel(events)
    ''' 
        Remove all callbacks registered for Fr_Window widget
    '''    
    def exitFr_Window(self):
        self.view.removeEventCallbackPivy( coin.SoKeyboSoMouseButtonEvent.getClassTypeId(), self.event_process)
        self.view.removeEventCallbackPivy( coin.SoKeyboardEvent.getClassTypeId(), self.event_process)
        self.view.removeEventCallbackPivy( coin.SoLocation2Event.getClassTypeId(), self.event_process)