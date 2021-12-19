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


'''
This is a class for coin3D Window
'''


class Fr_CoinWindow(fr_group.Fr_Group):
    """
    Main window which acts like a server for the children. 
    It distribute the events, keep track of adding switches to
    the SceneGraph. Switches keep track of nodes and their 
    drawing. So the tree is like that SceneGraph-->Switches->Node->drawings
    """
    # This is the holder of all objects.It should be here not inside the Fr_Group
    # this is the root scenegraph. It keeps all switch. Switches will keep drawing
    from ThreeDWidgets import fr_coin3d
    Root_SceneGraph = None
    view = None
    link_to_root_handle = fr_coin3d.root_handle()

    def __init__(self, vectors: List[App.Vector] = [App.Vector(0, 0, 0), App.Vector(
            400, 400, 0)], label: str = [[]]):
        Fr_CoinWindow.link_to_root_handle.w_wind=self
        super().__init__(vectors, label)

        Fr_CoinWindow.Root_SceneGraph = Gui.ActiveDocument.ActiveView.getSceneGraph()
        self.w_mainfrCoinWindow = self
        self.w_parent = self  # No parent and this is the main window
        self.w_widgetType = FR_WidgetType.FR_COINWINDOW
        Fr_CoinWindow.link_to_root_handle.addCallbacks()

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
        Fr_CoinWindow.link_to_root_handle.w_wind = self
        Fr_CoinWindow.view = Gui.ActiveDocument.ActiveView
        self.draw()
        super().show()  # Show all children also

    def __del__(self):
        """
        Class destructor 
        Like exit in normal window. This will end the windows
        """
        self.hide()
        if Fr_CoinWindow.link_to_root_handle is not None:
            del Fr_CoinWindow.link_to_root_handle
            Fr_CoinWindow.link_to_root_handle = None
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
