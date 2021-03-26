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

#Widgets type 
class FR_WidgetType:
    #FR_Widget is a generic definition, FR_Group will be such a widget
    def FR_Widget():
        return 0
    def FR_Edge(): 
        return 10
    def FR_Face():
        return 20   #2D Shape
    def FR_BOX():
        return 30    #3D Shape
    def FR_Button():
        return 20
    def FR_Wheel():
        return 30
    
class FR_COLOR:
    #Transparency - No color will be applied
    def Fr_Transparency():
        return None 

    def FR_White():
        return (1, 1, 1)
    def FR_Silver():
        return (0.75, 0.75,0.75)

    def FR_Gray():
        return (0.5, 0.5, 0.5)
    def FR_Gray0():
        return (0.411, 0.411, 0.411)
    def FR_Gray1():
        return (0.670, 0.670, 0.670)
    def FR_Gray2():
        return (0.780, 0.780, 0.780)
    def FR_Gray3():
        return (0.901, 0.901, 0.901)

    def FR_Black():
        return (0, 0, 0)
    def FR_Red():
        return (1, 0, 0)
    def FR_Maroon():
        return (0.5, 0, 0)
    def FR_Yellow():
        return (1, 1, 0)
    
    def FR_Select1():
        return (0.917, 0.960, 0)
    def FR_Select1():
        return (0.917, 0.960, 0)
    def FR_Select1():
        return (0.917, 0.960, 0)
    def FR_Select2():
        return (0.968, 0.992, 0.407)
    def FR_Select3():
        return (1, 0.847, 0.439)
        
    def FR_Olive():
        return (0.5, 0.5, 0)
    def FR_Lime():
        return (0, 1,  0)
    def FR_Green():
        return (0, 0.5, 0)
    def FR_Aqua():
        return (0, 1,  1)
    def FR_Teal():
        return (0, 0.5, 0.5)
    def FR_Blue():
        return (0, 0,  1)
        
    def FR_Blue1():
        return (0.250, 0.027, 0.949)
    def FR_Blue2():
        return(0.450, 0.462, 0.909)
    def FR_Blue3():
        return (0.4, 0.623, 0.941)
    def FR_Blue4():
        return(0.384, 0.749, 0.937)
    def FR_Blue5():
        return (0.301, 0.854, 0.976)

    def FR_Navy():
        return (0, 0,  0.5)

    def FR_Fuchsia():
        return (1, 0,  1)
    def FR_Purple():
        return (0.5, 0,  0.5)
    def FR_White():
        return (1, 1, 1)

#Box type when for widgets
class FR_BoxType:
    def FR_NoBox():         #There will not be any boundary box or bkg box
        return 0
    def FR_FLAT_BOX():
        return 10
    def FR_UP_BOX():
        return 20
    def FR_DOWN_BOX():
        return 30
    def FR_BORDER_FRAME():
        return 40      
    def FR_ROUNDED_BOX():
        return 50
    def FR_ROUNDED_FRAME():
        return 60
    def FR_ROUND_FLAT_BOX():
        return 70
    def FR_ROUND_UP_BOX():
        return 80
    def FR_ROUND_DOWN_BOX():
        return 90
    def FR_OVAL_BOX():
        return 100
    def FR_OVAL_FRAME():
        return 110
    def FR_TRIANGLE_BOX():
        return 110
    def FR_TRIANGLE_FRAME():
        return 110
        

class FR_EVENTS:    
    def SKIP_EVENT():
        return 0
    def MOUSE_LEFT_CLICK():
        return 10
    def MOUSE_RIGHT_CLICK():
        return 20
    def MOUSE_SCROLL_CLICK():
        return 70
    def MOUSE_MIDDLE_CLICK():
        return 70
    def MOUSE_ENTER_CLICK():
        return 30
    def MOUSE_KEY_UP():
        return 60
    def MOUSE_KEY_DOWN():
        return 70
    def KEYBOARD_ENTER():
        return 80
    def MOUSE_DRAG():
        return 90
    def MOUSE_MOVE():
        return 100
    def MOUSE_():
        return 110

    
    

