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
    FR_WIDGET=          0
    FR_GROUP=          10 
    FR_COINWINDOW=     20    #3D World
    FR_QTWINDOW=       30    #2D World
    FR_EDGE=           40
    FR_FACE=           50    
    FR_BOX=            60    
    FR_BUTTON=         70
    FR_WHEEL=          80

class FR_COLOR:
    #Transparency - No color will be applied
    
    FR_TRANSPARENCY = (-1.00,-1.00,-100)  #No color 
    FR_WHITE =        (1.00, 1.00, 1.00)
    FR_SILVER=        (0.75, 0.75, 0.75)
    FR_GRAY=          (0.50, 0.50, 0.50)
    FR_GRAY0=         (0.41, 0.41, 0.41)
    FR_GRAY1=         (0.67, 0.67, 0.67)
    FR_GRAY2=         (0.78, 0.78, 0.78)
    FR_GRAY3=         (0.90, 0.90, 0.90)

    FR_BLACK=         (0.00, 0.00, 0.00)
    FR_RED=           (1.00, 0.00, 0.00)
    FR_MAROON=        (0.50, 0.00, 0.00)
    FR_YELLOW=        (1.00, 1.00, 0.00)
    FR_SELECT1=       (0.92, 0.96, 0.00)
    FR_SELECT2=       (0.97, 0.99, 0.41)
    FR_SELECT3=       (1.00, 0.85, 0.44)    
    FR_OLIVE=         (0.50, 0.50, 0.00)
    FR_LIME=          (0.00, 1.00, 0.00)
    FR_GREEN=         (0.00, 0.50, 0.00)
    FR_AQUA=          (0.00, 1.00, 1.00)
    FR_TEAL=          (0.00, 0.50, 0.50)
    FR_BLUE=          (0.00, 0.00, 1.00)
    FR_BLUE1=         (0.25, 0.03, 0.95)
    FR_BLUE2=         (0.45, 0.46, 0.91)
    FR_BLUE3=         (0.40, 0.62, 0.94)
    FR_BLUE4=         (0.38, 0.75, 0.94)
    FR_BLUE5=         (0.30, 0.85, 0.98)
    FR_NAVY=          (0.00, 0.00, 0.50)
    FR_FUCHSIA=       (1.00, 0.00, 1.00)
    FR_PURPLE=        (0.50, 0.00, 0.50)
    FR_WHITE=         (1.00, 1.00, 1.00)

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
    FR_NO_EVENT		                 = 0,
    MOUSE_LEFT_PUSH                  = 1,
    MOUSE_LEFT_RELEASE               = 2,
    MOUSE_RIGHT_PUSH                 = 3,
    MOUSE_RIGHT_RELEASE              = 4,
    MOUSE_MIDDLE_PUSH                = 5,
    MOUSE_MIDDLE_RELEASE             = 6,
    FR_ENTER		                 = 7,
    FR_DRAG		                     = 8,
    FR_FOCUS		                 = 9,
    FR_UNFOCUS		                 =10,
    FR_KEYDOWN		                 =11,
    FR_KEYUP		                 =12,
    FR_CLOSE		                 =13,
    FR_MOUSE_MOVE                    =14,
    FR_MOUSE_DRAG                    =15,
    FR_SHORTCUT		                 =16,
    FR_DEACTIVATE	                 =17,
    FR_ACTIVATE		                 =18,
    FR_HIDE		                     =19,
    FR_SHOW		                     =20,
    FR_SELECTIONCLEAR	             =21,
    FR_MOUSEWHEEL		             =22
        
    #No constant for keyboard as it is defined already in coin.
    # Regarding the enum key definition in COIN3D. We don't want to redefine them. 
    # to find them use coin.SoKeyboardEvent.(Key name here without brackets)

class FR_WINDOWTYPE:
    WIN_COIN3D=0
    WIN_QT=1
    
class Fr_When: 
    """
    Fr_Widget.when()
    This decide when the callback is called
    """
    FR_WHEN_NEVER		      = 0  # Never call the callback
    FR_WHEN_CHANGED	          = 1  # Do the callback only when the widget value changes
    FR_WHEN_NOT_CHANGED	      = 2  # Do the callback whenever the user interacts with the widget
    FR_WHEN_RELEASE	          = 4  # Do the callback when the button or key is released and the value changes
    FR_WHEN_RELEASE_ALWAYS    = 6  # Do the callback when the button or key is released, even if the value doesn't change
    FR_WHEN_ENTER_KEY	      = 8  # Do the callback when the user presses the ENTER key and the value changes
    FR_WHEN_ENTER_KEY_ALWAYS  =10  # Do the callback when the user presses the ENTER key, even if the value doesn't change