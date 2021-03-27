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

      
class Fr_Widget (object):
    x=0
    y=0
    z=0
    h=0
    w=0
    t=0
    l=""
    coinNode=coin.SoSeparator
    visible=True
    bkgColor=constant.FR_COLOR.FR_Gray
    frgColor=constant.FR_COLOR.FR_White
    color1=constant.FR_COLOR.FR_Gray
    color2=constant.FR_COLOR.FR_Black
    box=None
    active=False
    parent=None
    type=constant.FR_WidgetType.FR_Widget
    hasFocus=False
    

     
    #Coin SoSeparator (node)

    def __init__(self, x,y,z,h,w,t=0,l=""):
        self.x=x
        self.y=y
        self.z=z=0
        self.h=h
        self.w=w
        self.t=t
        self.l=l
        
    def remove_drawing(self):
        raise NotImplementedError()
    def redraw(self):
        raise NotImplementedError()
    def take_focus(self):
        hasFocus=True
    def remove_focus(self):
        hasFocus=False
    """    #get private values     
    def x(self):
        return self.__x
    def y(self):
        return self.__y
    def z(self):
        return self.__z
    def l(self):
        return self.__l
    def w(self):
        return self.__w
    def h(self):
        return self.__h
    def l(self):
        return self.__l
            
    #set private variables
    def x(self,x):
        self.__x=x
    def y(self,y):
        self.__y=y
    def z(self,z):
        self.__z=z
    def w(self,w):
        self.__w=w
    def h(self,h):
        self.__h=h
    def t(self,t):
        self.__t=t
    def l(self,l):
        self.__l=l
    """
    #Activate, deactivate, get status of widget
    def visible(self):
        return self.__visible
    def show(self):
        self.visible=True
        self.redraw()
    def hide(self):
        self.visible=False
        self.redraw()
    def activate(self):
        self.active=True
        self.redraw()
    def deactivate(self):
        self.active=False
        self.redraw()
    def active(self):
        return self.active
        
    def hide():
        raise NotImplementedError()
    def show():
        raise NotImplementedError()
    def draw_box(self):
        raise NotImplementedError()
    def draw():
        raise NotImplementedError()
    def draw_label():
        raise NotImplementedError()
    def handle (self,event):
        raise NotImplementedError()
    def parent(self):
        return self.parent
    def parent(self,parent):
        self.parent=parent
    def type(self):
        return self.type
    def position(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def resize(self,x,y,z,W,H,T): #Width, height, thickness
        x=x
        y=y
        z=z
        w=W
        h=H
        t=T
        self.redraw()
    def size (self,W,H,Z):
        self.resize(self._x,self._y,self._z,W,H,T)
            
    #Take care of all events 
    def handle():
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
