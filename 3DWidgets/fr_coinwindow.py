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
import fr_coin3d


'''
This is a class for coin3D Window
'''

class Fr_CoinWindow(fr_group.Fr_Group):

    global view

    # This is the holder of all objects.It should be here not inside the Fr_Group
    global Root_SeneGraph
    global link_to_root_handle

    callbackMove = None
    callbackClick = None
    callbackKey = None

    def __init__(self, args:fr_widget.VECTOR=None,l=""):
        if args==None:
            args=[App.Vector(0,0,0), App.Vector(400,400,0)]  #Default vector
        self.view = Gui.ActiveDocument.ActiveView
        self.parent = self    # No parent and this is the main window
        self.lastKeyEvent = []  # Might be more than one key.
        self.WidgetType = constant.FR_WidgetType.FR_COINWINDOW
        self.link_to_root_handle=fr_coin3d.root_handle()
        self.link_to_root_handle.wind=self
        # Activate callbacks
        super().__init__(args, l)

    # All event come to this function. We classify the event to be processed by each widget later.

    def handle(self, events):
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
            if (wdg.active and wdg.visible and wdg.type != constant.FR_WidgetType.FR_WIDGET):
                if wdg.handle(events) == 1:
                    break

    def exitFr_Window(self):
        fr_coin3d.root_handle.removeCallbacks()
        # Call Fr_Groups deactivate to remove all widgets.
        self.parent.deactivate()

    def draw(self):
        '''Fr_CoinWindow itself, will not have any real drawing. 
        It will keep control of drawing the children but itself, nothing
        will be drawn.  
        '''
        # call group(parent)'s draw
        fr_group.Fr_Group.draw(self)

    def hide(self):
        self.deactivate()

    def addChild(self, childWdg):
        self.children.append(childWdg)
        childWdg.parent = self

    def show(self):
        """
        Show the window on the 3D World
        Normally if you don't have any widget, 
        this will draw nothing. But the callbacks
        will be created. Fr_CoinWindow will 
        not have any boarder or drawing itself.
        Its purpose is to keep the children, distribute
        handle and other things which might be added 
        later to this class.
        """
        self.draw()

    def removeChild(self, childWdg):
        try:
            self.children.remove(childWdg)
        except:
            print("not found")

    def deactivate(self):
        """
        Like exit in normal window. This will end the windows
        """
        self.exitFr_Window()
        self.parent.deactivate()
    def callback(self,data):
        #not sure what I should do here yet.
        pass 
    