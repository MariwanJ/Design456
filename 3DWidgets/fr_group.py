
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
import FreeCAD  as App
import FreeCADGui as Gui
import pivy.coin as coin
import Design456Init
import Draft as _draft
import fr_widget 
import constant 

#Group class. Use this to collect several widgets.
class Fr_Group(fr_widget.Fr_Widget):
    #Any drawign/Every thing should be added to this later 
    SeneGraph = Gui.ActiveDocument.ActiveView.getSceneGraph()
    children=[]
    pick_radius= 3 # See if this must be a parameter in the GUI /Mariwan
    def __init__(self, x,y,z,h,w,t,l):
        WidgetType=constant.FR_WidgetType.FR_GROUP
        super().__init__(x,y,z,h,w,t,l)
        
    def addWidget(self,widget):
        self.children.append(widget)
        
    def draw(self):
        for i in self.children:
            i.draw()
    def draw_label(self):
        for i in self.children:
           i.draw_label() 
    
    def redraw(self):
        for i in self.children:
            i.draw(self)

    def deactivate(self):
        for widget in self.children:
            del widget
        self.children.clear()

    def addSeneNode(self, sen):
        self.SeneGraph.addChild(sen)
        self.wdgsoSwitch.addChild(sen)
        
    def removeSeneNode(self, sen):
        self.SeneGraph.removeChild(sen)

        
    """send event to all widgets
       Targeted Widget should return 1 if it uses the event 
       Sometimes it several widgets needs to get the event, 
       at that time it can do the job it has and later return the
       events itself. 
       To know if the widget was the target, you have to 
       calculate the dimension and the mouse position.
       If the mouse position is inside the same 
       dimension of the widget, the widget was the target,
       otherwise it should just neglect it.
    """
    def handle(self,events):
        for widg in self.children:
            if widg.handle(events) == 1:
                #Events reached the targeted widget go out
                return 1
 
    #This section is from DRAFT
    #It must help in finding the correct node 
    #which represent the widget.
    def getEditNode(self, pos):
        """Get edit node from given screen position."""
        node = self.sendRay(pos)
        return node
    
    def sendRay(self, mouse_pos):
        """Send a ray through the scene and return the nearest entity."""
        ray_pick = coin.SoRayPickAction(self.render_manager.getViewportRegion())
        ray_pick.setPoint(coin.SbVec2s(*mouse_pos))
        ray_pick.setRadius(self.pick_radius)
        ray_pick.setPickAll(True)
        ray_pick.apply(self.render_manager.getSceneGraph())
        picked_point = ray_pick.getPickedPointList()
        return self.searchEditNode(picked_point)

    def searchEditNode(self, picked_point):
        """Search edit node inside picked point list and return node number."""
        for point in picked_point:
            path = point.getPath()
            length = path.getLength()
            point = path.getNode(length - 2)
            #import DraftTrackers
            if hasattr(point,"subElementName") and 'EditNode' in str(point.subElementName.getValue()):
                return point
        return None