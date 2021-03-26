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
import init
import Draft as _draft
import fr_draw 
import constant

"""
Base class used to create all Widgets
You need to subclass this object 
to be able to create other widgets.
and you should always have a Fr_Group 
widget which acts like a container for widget.
fr_window widget will take care of events 
and is subclassed from fr_group
"""

      
class Fr_Widget (object):
    __x=0
    __y=0
    __z=0
    __h=0
    __w=0
    __t=0
    __l=""
    __coinNode=coin.SoSeparator
    __visible=True
    __bkgColor=constant.Fr_Color.FR_Gray()
    __frgColor=constant.Fr_Color.FR.White()
    __color1=constant.FR_Color.FR_Gray()
    __color2=constant.FR_Color.FR_Black()
    __box=None
    __active=False
    __parent=None
    __type=constant.FR_WidgetType.FR_Widget():

     
    #Coin SoSeparator (node)

    def __init__(self, x,y,z=0,h,w,t=1,l=""):
        self.__x=x
        self.__y=y
        self.__z=z
        self.__h=h
        self.__w=w
        self.__t=t
        self.__l=l
        
    def remove_drawing(self):
        raise NotImplementedError()
    def redraw(self):
        raise NotImplementedError()
    
    #get private values     
    def x(self):
        return self.__x
    def y(self):
        return self.__x
    def z(self):
        return self.__x
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

    #Activate, deactivate, get status of widget
    def visible(self):
        return self.__visible
    def show(self):
        self.__visible=True
        self.redraw()
    def hide(self):
        self.__visible=False
        self.redraw()
    def activate(self):
        self.__active=True
        self.redraw()
    def deactivate(self):
        self.__active=False
        self.redraw()
    def active(self):
        return self.__active
    
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
        return self.__parent
    def type(self):
        return self.__type
    def position(self,x,y,z):
        self.__x=x
        self.__y=y
        self.__z=z
    def resize(self,x,y,z,W,H,T): #Width, height, thickness
        __x=x
        __y=y
        __z=z
        __w=W
        __h=H
        __t=T
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
