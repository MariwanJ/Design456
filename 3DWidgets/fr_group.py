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
import Design456Init
import Draft as _draft
import fr_widget
import constant
from typing import List

# Group class. Use this to collect several widgets.


class Fr_Group(fr_widget.Fr_Widget):
    # Any drawign/Every thing should be added to this later
    # This will keep the link to the main window.
    global mainfrCoinWindow
    global mainfrQtWindow
    global children

    def __init__(self, args: List[App.Vector] = [], l: str = ""):
        if args == None:
            args = []
        self.widgetType = constant.FR_WidgetType.FR_GROUP
        # Root of the children (coin)

        self.children = []
        # Initialize them as None.
        self.mainfrCoinWindow = self.mainfrQtWindow = None
        super().__init__(args, l)
    @property
    def mainfrCoinWindow(self):
        return self.mainfrCoinWindow
    
    @mainfrCoinWindow.setter
    def mainfrCoinWindow(self, win):
        self.mainfrCoinWindow=win
    
    @property
    def mainfrQtWindow(self):
        return self.mainfrQtWindow
    
    @mainfrQtWindow.setter
    def mainfrQtWindow(self, win):
        self.mainfrQtWindow=win
        
    @property
    def children(self):
        return children
    
    @children.setter
    def children(self, values):
        self.children=values

    def addWidget(self, widg):
        widg.parent=self.mainfrCoinWindow
        self.children.append(widg)
        
    def removeWidget(self, widg):
        try:
            self.children.remove(widg)
        except:
            print("not found")

    def draw(self):
        for i in self.children:
            i.draw()

    def draw_label(self):
        for i in self.children:
            i.draw_label()

    def redraw(self):
        for i in self.children:
            i.redraw()
    """     TODO: THIS SHOULD BE DONE IN ANOTHER WAY.
    def deactivate(self):
    
    #Before deactivating the group, we have to remove all children.
    #Think about, you might have several groups inside the Fr_CoinWindow
    
        try:
            for widget in self.children:
                # Remove objects in the Root_SeneGraph
                self.removeSeneNode(widget.wdgsoSwitch)
                self.removeSeneNode(widget.widgetCoinNode)
                # Remove the widget itself from the group
                del widget
            del self.children
        except Exception:
            pass   # just go out
    """
    # All events distributed by this function. We classify the event to be processed by each widget later.
    def handle(self, events):
        """send events to all widgets
        Targeted Widget should return 1 if it uses the event 
        Sometimes there might be several widgets that need to get the event, 
        at that time return the event to achieve that. 
        To find the target widget, you have to 
        calculate find  the clicked object related to the mouse position.
        Widgets shouldn't get the event if they are not targeted.
        """
        for wdg in self.children:
            if (wdg.is_active and wdg.is_visible and wdg.widgetType != constant.FR_WidgetType.FR_WIDGET):
                if wdg.handle(events) == 1:
                    return 1
