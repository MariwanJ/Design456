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

#Widgets type. QT widget will get QT in their names.
class FR_WidgetType:
    """ Internal names of the widgets. QT widget will get 'qt' in their names """
    FR_WIDGET=         "Base Widget"
    FR_VERTEX=         "Single Vertex"
    FR_GROUP=          "Group Widget" 
    FR_COINWINDOW=     "Coin3D Window"    #3D World
    FR_QTWINDOW=       "QT Window"        #2D World
    FR_EDGE=           "Edge Widget"
    FR_FACE=           "Face Widget"    
    FR_SQUARE_FRAME=   "Square frame"
    FR_TRIANGLE=       "Triangle frame"
    FR_POLYGON=        "Polygon Widget"
    
    FR_BOX=            "Box Widget"    
    FR_WHEEL=          "Wheel Widget"
    

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
        
#No constant for keyboard as it is defined already in coin.
class FR_EVENTS:    
    FR_NO_EVENT=                0
    FR_MOUSE_LEFT_PUSH=        10
    FR_MOUSE_RIGHT_PUSH=       20
    FR_MOUSE_MIDDLE_PUSH=      30
    FR_MOUSE_LEFT_RELEASE=     40
    FR_MOUSE_RIGHT_RELEASE=    50
    FR_MOUSE_MIDDLE_RELEASE=   60
    FR_MOUSE_LEFT_DOUBLECLICK= 70
    FR_MOUSE_DRAG=             80
    FR_MOUSE_MOVE=             90
    
class FR_WHEN:
    FR_WHEN_NEVER	 	       = 0    # Never call the callback
    FR_WHEN_CHANGED	           = 1    # Do the callback only when the widget value changes
    FR_WHEN_NOT_CHANGED	       = 2    # Do the callback whenever the user interacts with the widget
    FR_WHEN_RELEASE	           = 4    # Do the callback when the button or key is released and the value changes
    FR_WHEN_RELEASE_ALWAYS     = 6    # Do the callback when the button or key is released, even if the value doesn't change
    FR_WHEN_ENTER_KEY	       = 8    # Do the callback when the user presses the ENTER key and the value changes
    FR_WHEN_ENTER_KEY_ALWAYS   =10    # Do the callback when the user presses the ENTER key, even if the value doesn't change

    #The enum key definition in COIN3D. We don't want to redefine them. 
    # to find them use coin.SoKeyboardEvent.(Key name here without brackets)
    '''
    enum Key {
         ANY = 0,
         UNDEFINED = 1,
    
         LEFT_SHIFT = 0xffe1, RIGHT_SHIFT, LEFT_CONTROL, RIGHT_CONTROL,
         LEFT_ALT = 0xffe9, RIGHT_ALT,
    
         NUMBER_0 = 0x0030, NUMBER_1, NUMBER_2, NUMBER_3, NUMBER_4, NUMBER_5,
         NUMBER_6, NUMBER_7, NUMBER_8, NUMBER_9,
    
         A = 0x0061, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T,
         U, V, W, X, Y, Z,
    
         HOME = 0xff50, LEFT_ARROW, UP_ARROW, RIGHT_ARROW, DOWN_ARROW,
         PAGE_UP, PAGE_DOWN, END,
         PRIOR = 0xff55, NEXT,
    
         PAD_ENTER = 0xff8d,
         PAD_F1 = 0xff91, PAD_F2, PAD_F3, PAD_F4,
         PAD_0 = 0xff9e, PAD_1 = 0xff9c, PAD_2 = 0xff99, PAD_3 = 0xff9b,
         PAD_4 = 0xff96, PAD_5 = 0xff9d, PAD_6 = 0xff98, PAD_7 = 0xff95,
         PAD_8 = 0xff97, PAD_9 = 0xff9a,
         PAD_ADD = 0xffab, PAD_SUBTRACT = 0xffad,
         PAD_MULTIPLY = 0xffaa, PAD_DIVIDE = 0xffaf,
         PAD_SPACE = 0xff8d, PAD_TAB = 0xff89,
         PAD_INSERT = 0xff9e, PAD_DELETE = 0xff9f, PAD_PERIOD = 0xff9f,
    
         F1 = 0xffbe, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12,
    
         BACKSPACE = 0xff08, TAB = 0xff09,
         RETURN = 0xff0d, ENTER = 0xff0d,
         PAUSE = 0xff13, SCROLL_LOCK = 0xff14,
         ESCAPE = 0xff1b, DELETE = 0xffff, KEY_DELETE = DELETE,
         PRINT = 0xff61, INSERT = 0xff63,
         NUM_LOCK = 0xff7f, CAPS_LOCK = 0xffe5, SHIFT_LOCK = 0xffe6,
    
         SPACE = 0x0020, APOSTROPHE = 0x0027,
         COMMA = 0x002c, MINUS = 0x002d, PERIOD = 0x002e, SLASH = 0x002f,
         SEMICOLON = 0x003b, EQUAL = 0x003d,
         BRACKETLEFT = 0x005b, BACKSLASH = 0x005c,
         BRACKETRIGHT = 0x005d, GRAVE = 0x0060
       };
    '''