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
    FR_Widget=          0
    FR_Edge=           10
    FR_Face=           20   #2D Shape
    FR_BOX=            30    #3D Shape
    FR_Button=         20
    FR_Wheel=          30
    
class FR_COLOR:
    #Transparency - No color will be applied
    
    Fr_Transparency = (-1.00,-1.00,-100)  #No color 
    FR_White =        (1.00, 1.00, 1.00)
    FR_Silver=        (0.75, 0.75, 0.75)
    FR_Gray=          (0.50, 0.50, 0.50)
    FR_Gray0=         (0.41, 0.41, 0.41)
    FR_Gray1=         (0.67, 0.67, 0.67)
    FR_Gray2=         (0.78, 0.78, 0.78)
    FR_Gray3=         (0.90, 0.90, 0.90)

    FR_Black=         (0.00, 0.00, 0.00)
    FR_Red=           (1.00, 0.00, 0.00)
    FR_Maroon=        (0.50, 0.00, 0.00)
    FR_Yellow=        (1.00, 1.00, 0.00)
    FR_Select1=       (0.92, 0.96, 0.00)
    FR_Select2=       (0.97, 0.99, 0.41)
    FR_Select3=       (1.00, 0.85, 0.44)    
    FR_Olive=         (0.50, 0.50, 0.00)
    FR_Lime=          (0.00, 1.00, 0.00)
    FR_Green=         (0.00, 0.50, 0.00)
    FR_Aqua=          (0.00, 1.00, 1.00)
    FR_Teal=          (0.00, 0.50, 0.50)
    FR_Blue=          (0.00, 0.00, 1.00)
    FR_Blue1=         (0.25, 0.03, 0.95)
    FR_Blue2=         (0.45, 0.46, 0.91)
    FR_Blue3=         (0.40, 0.62, 0.94)
    FR_Blue4=         (0.38, 0.75, 0.94)
    FR_Blue5=         (0.30, 0.85, 0.98)
    FR_Navy=          (0.00, 0.00, 0.50)
    FR_Fuchsia=       (1.00, 0.00, 1.00)
    FR_Purple=        (0.50, 0.00, 0.50)
    FR_White=         (1.00, 1.00, 1.00)

#Box type when for widgets
class FR_BoxType: #There will not be any boundary box or bkg box
    FR_NoBox=                 0
    FR_FLAT_BOX=             10
    FR_UP_BOX=               20
    FR_DOWN_BOX=             30
    FR_BORDER_FRAME=         40      
    FR_ROUNDED_BOX=          50
    FR_ROUNDED_FRAME=        60
    FR_ROUND_FLAT_BOX=       70
    FR_ROUND_UP_BOX=         80
    FR_ROUND_DOWN_BOX=       90
    FR_OVAL_BOX=            100
    FR_OVAL_FRAME=          110
    FR_TRIANGLE_BOX=        120
    FR_TRIANGLE_FRAME=      130
        

class FR_EVENTS:    
    SKIP_EVENT=               0
    MOUSE_LEFT_CLICK=        10
    MOUSE_RIGHT_CLICK=       20
    MOUSE_MIDDLE_CLICK=      30
    MOUSE_ENTER_CLICK=       40
    MOUSE_DRAG=              50
    MOUSE_MOVE=              60

    MOUSE_KEY_UP=            70
    MOUSE_KEY_DOWN=          80
    FR_ENTER=                90
    FR_CTRL=                 100
    FR_SHIFT=                110
    FR_ALT=                  120
