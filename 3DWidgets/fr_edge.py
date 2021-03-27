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

import os,sys
import FreeCAD  as App
import FreeCADGui as Gui
import pivy.coin as coin
import fr_widget
import Design456Init
import fr_draw
import constant

#Group class. Use this to collect several widgets.
class Fr_Edge(fr_widget.Fr_Widget):
    coinNode=None
    def __init__(self, x,y,z,h,w,t,l):
        super().__init__(x,y,z,h,w,t,l)
        self.type=constant.FR_WidgetType.Face
        
    def draw(self):
        p1=(self.x,self.y,self.z)
        p2=(self.x+self.w,self.y+self.h,self.z)                   
        self.coinNode=fr_draw.draw_line(p1,p2,self.color(),self.t)   #(p1, p2,color,LineWidth)
    def redraw(self):
        del self.coinNode
        self.draw()
    def  handle(self,events):
        if self.active():
            if events ==constant.FR_EVENTS.MOUSE_LEFT_CLICK():
                self.color1=constant.FR_COLOR.FR_Select1()
                self.redraw()
                return 1          
    def Activate(self):
        self.draw()
    def Deactivate(self):
        del self.coinNode
        