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


class Fr_Window(fr_group.Fr_Group):
    __view=None
    __lastEvent=None
    __lastKeyEvent=[]       #Might be more than one key.
    __lastEventXYZ=App.Vertex(0,0,0)       #This should keep the mouse pointer position on the 3D view
    
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
                lastEvent=constant.Fr_Events.MOUSE_LEFT_CLICK()
            if (type(getEvent) == coin.SoMouseButtonEvent and getEvent.getState() == coin.SoMouseButtonEvent.DOWN and getEvent.getButton() == coin.SoMouseButtonEvent.BUTTON3):
                lastEvent=constant.Fr_Events.MOUSE_MIDDLE_CLICK()
            if (type(getEvent) == coin.SoMouseButtonEvent and getEvent.getState() == coin.SoMouseButtonEvent.DOWN and getEvent.getButton() == coin.SoMouseButtonEvent.BUTTON2):
                lastEvent=constant.Fr_Events.MOUSE_RIGHT_CLICK()
            
        elif (type(event) == coin.SoKeyboardEvent):
            key = ""
            try:
                key = event.getKey()
            except ValueError:
                # there is no character for this value
                key = ""
            
            if (key == coin.SoKeyboardEvent.LEFT_CONTROL() or coin.SoKeyboardEvent.RIGHT_CONTROL() ) and 
                    event.getState() == coin.SoButtonEvent.DOWN:
                __lastKeyEvent.append(constant.FR_EVENTS        
                
                    self.snap = True
                elif event.getState() == coin.SoButtonEvent.UP:
                    self.snap = False
            elif key == coin.SoKeyboardEvent.RETURN:
                self.accept()
                self.finish()
            elif key == coin.SoKeyboardEvent.BACKSPACE and event.getState() == coin.SoButtonEvent.UP:
                self.removePole()
            elif key == coin.SoKeyboardEvent.I and event.getState() == coin.SoButtonEvent.UP:
                self.increaseDegree()
            elif key == coin.SoKeyboardEvent.D and event.getState() == coin.SoButtonEvent.UP:
                self.decreaseDegree()
            elif key == coin.SoKeyboardEvent.ESCAPE:
                self.abort()
                self.finish()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        elif (type(event) == coin.SoLocation2Event):
            pos = App.ActiveDocument.ActiveView.getCursorPos()
            
            pnt = self.view.getPoint(pos)
           FreeCAD.Console.PrintMessage("World coordinates: " + str(pnt) + "\n")
           info = self.view.getObjectInfo(pos)
            
            
            self.point = self.view.getPoint(pos[0],pos[1])
            if self.snap:
                self.getSnapPoint(pos)
            self.cursorUpdate()
    ''' 
        Remove all callbacks registerd for Fr_Window widget
    '''    
    def exitFr_Window(self):
        self.view.removeEventCallbackPivy( coin.SoKeyboSoMouseButtonEvent.getClassTypeId(), self.event_process)
        self.view.removeEventCallbackPivy( coin.SoKeyboardEvent.getClassTypeId(), self.event_process)
        self.view.removeEventCallbackPivy( coin.SoLocation2Event.getClassTypeId(), self.event_process)