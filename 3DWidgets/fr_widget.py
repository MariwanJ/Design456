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

"""
This class is the base class for all widgets created in coin3D

"""
import os,sys
import FreeCAD  as App
import FreeCADGui as Gui
import pivy.coin as coin
import Design456Init
import Draft as _draft
import fr_draw 
import constant



      
class Fr_Widget (object):
    """
    Abstract Base class used to create all Widgets
    You need to subclass this object 
    to be able to create other objects,
    and you should always have a Fr_Group 
    widget which acts like a container for the widgets.
    fr_window widget will take care of that,
    events will be distributed by fr_window
    and it is a subclassed object from fr_group.
    fr_group doesn't need to be drawn, but 
    you can implement draw function
    """
    global x
    global y
    global z
    global h
    global w
    global t
    global l
    global WidgetCoinNode  #This is for the children or the widget itself
    global visible
    global bkgColor
    global frgColor
    global color1
    global color2
    global box
    global active
    global parent
    global WidgetType
    global hasFocus
    global wdgsoSwitch
    global pick_radius
     
    #Coin SoSeparator (node)

    def __init__(self, x=0,y=0,z=0,h=0,w=0,t=0,l=""):
        self.x=x
        self.y=y
        self.z=z=0
        self.h=h
        self.w=w
        self.t=t
        self.l=l
        self.WidgetCoinNode=coin.SoSeparator
        self.visible=True
        self.bkgColor=constant.FR_COLOR.FR_GRAY
        self.frgColor=constant.FR_COLOR.FR_WHITE
        self.color1=constant.FR_COLOR.FR_GRAY
        self.color2=constant.FR_COLOR.FR_BLACK
        self.box=None
        self.active=True
        self.parent=None
        self.WidgetType=constant.FR_WidgetType.FR_WIDGET
        self.hasFocus=False
        self.wdgsoSwitch=coin.SoSwitch()
        self.pick_radius= 3 # See if this must be a parameter in the GUI /Mariwan
        self.wdgsoSwitch.whichChild =coin.SO_SWITCH_ALL  #Show all
        
    def redraw(self):
        raise NotImplementedError()
    def take_focus(self):
        if self.has_focus==True:
            return # nothing to do here
        self.hasFocus=True
        self.redraw()
    
    def move(self,x,y,z):
        """ Move the widget to a new location.
        The new location is reference to the 
        left-upper corner"""
        raise NotImplementedError()

    def move_centerOfMass(self,x,y,z):
        """ Move the widget to a new location.
        The new location is reference to the 
        center of mass"""
        raise NotImplementedError()

    def has_focus(self):
        return self.hasFocus
    def remove_focus(self):
        if self.hasFocus==False:
            return # nothing to do
        else:
            self.hasFocus=False
            self.redraw()

    #Activate, deactivate, get status of widget
    def is_visible(self):
        return self.visible
    def activate(self):
        if self.active:
            return #nothing to do 
        self.active=True
        self.redraw()
    def deactivate(self):
        if self.active==False :
            return #Nothing to do 
        self.active=False
        self.redraw()
    def is_active(self):
        return self.active
        
    def hide():
        if self.visible==False:
            return # nothing to do 
        self.visible=False
        self.wdgsoSwitch.whichChild =coin.SO_SWITCH_NONE #hide all children
        self.redraw()

    def show(self):
        self.visible=True
        self.wdgsoSwitch.whichChild =coin.SO_SWITCH_ALL #Show all children
        self.redraw()
        
    def draw_box(self):
        raise NotImplementedError()
    def draw():
        raise NotImplementedError()
    def draw_label():
        raise NotImplementedError()
    def parent(self):
        return self.parent
    def parent(self,parent):
        self.parent=parent
    def type(self):
        return self.type
    def getPosition(self):
        return (x,y,z)
    def getPositionAsVertex(self):
        return App.Vertex(x,y,z)
    
    def position(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def resize(self,x,y,z,W,H,T): #Width, height, thickness
        self.x=x
        self.y=y
        self.z=z
        self.w=W
        self.h=H
        self.t=T
        self.redraw()
        
    def size (self,W,H,Z):
        self.resize(self.x,self.y,self.z,W,H,T)
            
    #Take care of all events 
    def handle(self,events):
        raise NotImplementedError()

    #Callbacks 
    def callbackDeactivate(self):
        raise NotImplementedError()
    def callbackClicked(self):
        raise NotImplementedError()        
    def callbackRedraw(self):
        raise NotImplementedError()
    def callbackMove(self):
        raise NotImplementedError()
    def callbackRotate(self):
        raise NotImplementedError()

    #This section is from DRAFT
    #It must help in finding the correct node 
    #which represent the widget.
    def getEditNode(self, pos):
        """Get edit node from given screen position."""
        node = self.sendRay(pos)
        return node
    
    def sendRay(self, mouse_pos):
        """Send a ray through the scene and return the nearest entity."""
        try:
            viewer = Gui.ActiveDocument.ActiveView.getViewer()
            render_manager = viewer.getSoRenderManager()
            ray_pick = coin.SoRayPickAction(render_manager.getViewportRegion())
            ray_pick.setPoint(coin.SbVec2s(*mouse_pos))
            ray_pick.setRadius(self.pick_radius)
            ray_pick.setPickAll(True)
            ray_pick.apply(render_manager.getSceneGraph())
            picked_point = ray_pick.getPickedPoint()
            return self.searchEditNode(picked_point)
        except Exception as err:
            App.Console.PrintError("'SplitObject' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def searchEditNode(self, picked_point):
        """Search edit node inside picked point list and return node ."""
        try:
            if picked_point !=None and picked_point!= 0: 
                path = picked_point.getPath()
                pickedNode = path.getTail()       
                return pickedNode
        except Exception as err:
            App.Console.PrintError("'SplitObject' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            