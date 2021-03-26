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


"""
    def mouseEvents(self, mouseEvent):
        #Address mouse activities.
        event = mouseEvent.getEvent()
        if event.getTypeId() == coin.SoLocation2Event.getClassTypeId():
            FreeCAD.Console.PrintMessage("We are in SoLocation2Event\n")
        elif event.getTypeId() == coin.SoMouseButtonEvent.getClassTypeId():
            FreeCAD.Console.PrintMessage("We are in SoMouseButtonEvent\n")
        else:
            
            FreeCAD.Console.PrintMessage("We are in nothing")
                def mouseEvents(self, mouseEvent):


            #Address mouse activities.
        event = mouseEvent.getEvent()
        if type(event) == coin.SoMouseButtonEvent:
            FreeCAD.Console.PrintMessage("We are in SoMouseButtonEvent")
        elif type(event) == coin.SoLocation2Event:
            FreeCAD.Console.PrintMessage("We are in SoLocation2Event")
        else:
            FreeCAD.Console.PrintMessage("We are in nothing")




class ButtonTest:
    def __init__(self):
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.callback = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.getMouseClick) 

    def getMouseClick(self, event_cb):
        event = event_cb.getEvent()
        if event.getState() == coin.SoMouseButtonEvent.DOWN:
            print("Alert!!! A mouse button has been improperly clicked!!!")
            self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)

ButtonTest()



SoFile.getClassId()


"""

class Fr_Window(fr_group.Fr_Group):
    __view=None
    __event=None
    __eventXYZ=App.Vertex(0,0,0)       #This should keep the mouse pointer position on the 3D view
    def __init__(self, x,y,z,h,w,t,l):
        super().__init__(x,y,z,h,w,t,l)
        __view=Gui.ActiveDocument.ActiveView
        self.addCallbacks
    
    def removeCallbacks(self):
        pass
    def addCallbacks(self):
        self.callback = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.event_process) 
        self.callback = self.view.addEventCallbackPivy(coin.SoKeyboardEvent.getClassTypeId(), self.event_process)
    #All event come to this function. We classify the event to be processed by each widget later.  
    def event_process(self,events):
        event = events.getEvent()
        #write down all possible events.
        if event == self.__event.isKeyPressEvent(event, event.ESC):