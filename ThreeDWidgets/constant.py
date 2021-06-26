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
    FR_ARROW=          "Arrow Widget"
    FR_BOX=            "Box Widget"    
    FR_WHEEL=          "Wheel Widget"
    

class FR_COLOR:
    #Transparency - No color will be applied
    
    FR_TRANSPARENCY            =  (-1.0000  ,  -1.0000  ,  -1.0000  )  #No color 
    FR_PINK                    =  (	1.0000	,	0.7529	,	0.7961	)
    FR_BLUE                    =  (	0.0000	,	0.0000	,	1.0000	)
    FR_BLUEG                   =  ( 0.6941  ,   0.8700  ,   0.9216  )
    FR_HONEYDEW                =  (	0.9412	,	1.0000	,	0.9412	)
    FR_PURPLE                  =  (	0.5020	,	0.0000	,	0.5020	)
    FR_FUCHSIA                 =  (	1.0000	,	0.0000	,	1.0000	)
    FR_LAWNGREEN               =  (	0.4863	,	0.9882	,	0.0000	)
    FR_AMETHYST                =  (	0.6000	,	0.4000	,	0.8000	)
    FR_CRIMSON                 =  (	0.8627	,	0.0784	,	0.2353	)
    FR_WHITE                   =  (	1.0000	,	1.0000	,	1.0000	)
    FR_NAVAJOWHITE             =  (	1.0000	,	0.8706	,	0.6784	)
    FR_CORNSILK                =  (	1.0000	,	0.9725	,	0.8627	)
    FR_BISQUE                  =  (	1.0000	,	0.8941	,	0.7686	)
    FR_PALEGREEN               =  (	0.5961	,	0.9843	,	0.5961	)
    FR_BROWN                   =  (	0.6471	,	0.1647	,	0.1647	)
    FR_DARKTURQUOISE           =  (	0.0000	,	0.8078	,	0.8196	)
    FR_DARKGREEN               =  (	0.0000	,	0.3922	,	0.0000	)
    FR_MEDIUMORCHID            =  (	0.7294	,	0.3333	,	0.8275	)
    FR_CHOCOLATE               =  (	0.8235	,	0.4118	,	0.1176	)
    FR_PAPAYAWHIP              =  (	1.0000	,	0.9373	,	0.8353	)
    FR_OLIVE                   =  (	0.5020	,	0.5020	,	0.0000	)
    FR_SILVER                  =  (	0.7529	,	0.7529	,	0.7529	)
    FR_PEACHPUFF               =  (	1.0000	,	0.8549	,	0.7255	)
    FR_PLUM                    =  (	0.8667	,	0.6275	,	0.8667	)
    FR_DARKGOLDENROD           =  (	0.7216	,	0.5255	,	0.0431	)
    FR_SLATEGREY               =  (	0.4392	,	0.5020	,	0.5647	)
    FR_MINTCREAM               =  (	0.9608	,	1.0000	,	0.9804	)
    FR_CORNFLOWERBLUE          =  (	0.3922	,	0.5843	,	0.9294	)
    FR_GOLD                    =  (	1.0000	,	0.8431	,	0.0000	)
    FR_HOTPINK                 =  (	1.0000	,	0.4118	,	0.7059	)
    FR_DARKBLUE                =  (	0.0000	,	0.0000	,	0.5451	)
    FR_LIMEGREEN               =  (	0.1961	,	0.8039	,	0.1961	)
    FR_DEEPSKYBLUE             =  (	0.0000	,	0.7490	,	1.0000	)
    FR_DARKKHAKI               =  (	0.7412	,	0.7176	,	0.4196	)
    FR_LIGHTGREY               =  (	0.8275	,	0.8275	,	0.8275	)
    FR_YELLOW                  =  (	1.0000	,	1.0000	,	0.0000	)
    FR_GAINSBORO               =  (	0.8627	,	0.8627	,	0.8627	)
    FR_MISTYROSE               =  (	1.0000	,	0.8941	,	0.8824	)
    FR_SANDYBROWN              =  (	0.9569	,	0.6431	,	0.3765	)
    FR_DEEPPINK                =  (	1.0000	,	0.0784	,	0.5765	)
    FR_MAGENTA                 =  (	1.0000	,	0.0000	,	1.0000	)
    FR_ALICEBLUE               =  (	0.9412	,	0.9725	,	1.0000	)
    FR_DARKCYAN                =  (	0.0000	,	0.5451	,	0.5451	)
    FR_DARKSLATEGREY           =  (	0.1843	,	0.3098	,	0.3098	)
    FR_GREENYELLOW             =  (	0.6784	,	1.0000	,	0.1843	)
    FR_DARKORCHID              =  (	0.6000	,	0.1961	,	0.8000	)
    FR_OLIVEDRAB               =  (	0.4196	,	0.5569	,	0.1373	)
    FR_CHARTREUSE              =  (	0.4980	,	1.0000	,	0.0000	)
    FR_PERU                    =  (	0.8039	,	0.5216	,	0.2471	)
    FR_ORANGE                  =  (	1.0000	,	0.6471	,	0.0000	)
    FR_RED                     =  (	1.0000	,	0.0000	,	0.0000	)
    FR_WHEAT                   =  (	0.9608	,	0.8706	,	0.7020	)
    FR_LIGHTCYAN               =  (	0.8784	,	1.0000	,	1.0000	)
    FR_LIGHTSEAGREEN           =  (	0.1255	,	0.6980	,	0.6667	)
    FR_BLUEVIOLET              =  (	0.5412	,	0.1686	,	0.8863	)
    FR_LIGHTSLATEGREY          =  (	0.4667	,	0.5333	,	0.6000	)
    FR_CYAN                    =  (	0.0000	,	1.0000	,	1.0000	)
    FR_MEDIUMPURPLE            =  (	0.5765	,	0.4392	,	0.8588	)
    FR_MIDNIGHTBLUE            =  (	0.0980	,	0.0980	,	0.4392	)
    FR_FIREBRICK               =  (	0.6980	,	0.1333	,	0.1333	)
    FR_PALETURQUOISE           =  (	0.6863	,	0.9333	,	0.9333	)
    FR_PALEGOLDENROD           =  (	0.9333	,	0.9098	,	0.6667	)
    FR_GRAY                    =  (	0.5020	,	0.5020	,	0.5020	)
    FR_MEDIUMSEAGREEN          =  (	0.2353	,	0.7020	,	0.4431	)
    FR_MOCCASIN                =  (	1.0000	,	0.8941	,	0.7098	)
    FR_IVORY                   =  (	1.0000	,	1.0000	,	0.9412	)
    FR_DARKSLATEBLUE           =  (	0.2824	,	0.2392	,	0.5451	)
    FR_BEIGE                   =  (	0.9608	,	0.9608	,	0.8627	)
    FR_GREEN                   =  (	0.0000	,	0.5020	,	0.0000	)
    FR_SLATEBLUE               =  (	0.4157	,	0.3529	,	0.8039	)
    FR_TEAL                    =  (	0.0000	,	0.5020	,	0.5020	)
    FR_AZURE                   =  (	0.9412	,	1.0000	,	1.0000	)
    FR_LIGHTSTEELBLUE          =  (	0.6902	,	0.7686	,	0.8706	)
    FR_DIMGREY                 =  (	0.4118	,	0.4118	,	0.4118	)
    FR_TAN                     =  (	0.8235	,	0.7059	,	0.5490	)
    FR_ANTIQUEWHITE            =  (	0.9804	,	0.9216	,	0.8431	)
    FR_SKYBLUE                 =  (	0.5294	,	0.8078	,	0.9216	)
    FR_GHOSTWHITE              =  (	0.9725	,	0.9725	,	1.0000	)
    FR_MEDIUMTURQUOISE         =  (	0.2824	,	0.8196	,	0.8000	)
    FR_FLORALWHITE             =  (	1.0000	,	0.9804	,	0.9412	)
    FR_LAVENDERBLUSH           =  (	1.0000	,	0.9412	,	0.9608	)
    FR_SEAGREEN                =  (	0.1804	,	0.5451	,	0.3412	)
    FR_LAVENDER                =  (	0.9020	,	0.9020	,	0.9804	)
    FR_BLANCHEDALMOND          =  (	1.0000	,	0.9216	,	0.8039	)
    FR_DARKOLIVEGREEN          =  (	0.3333	,	0.4196	,	0.1843	)
    FR_DARKSEAGREEN            =  (	0.5608	,	0.7373	,	0.5608	)
    FR_SPRINGGREEN             =  (	0.0000	,	1.0000	,	0.4980	)
    FR_NAVY                    =  (	0.0000	,	0.0000	,	0.5020	)
    FR_ORCHID                  =  (	0.8549	,	0.4392	,	0.8392	)
    FR_SADDLEBROWN             =  (	0.5451	,	0.2706	,	0.0745	)
    FR_INDIANRED               =  (	0.8039	,	0.3608	,	0.3608	)
    FR_SNOW                    =  (	1.0000	,	0.9804	,	0.9804	)
    FR_STEELBLUE               =  (	0.2745	,	0.5098	,	0.7059	)
    FR_MEDIUMSLATEBLUE         =  (	0.4824	,	0.4078	,	0.9333	)
    FR_BLACK                   =  (	0.0000	,	0.0000	,	0.0000	)
    FR_LIGHTBLUE               =  (	0.6784	,	0.8471	,	0.9020	)
    FR_TURQUOISE               =  (	0.2510	,	0.8784	,	0.8157	)
    FR_MEDIUMVIOLETRED         =  (	0.7804	,	0.0824	,	0.5216	)
    FR_DARKVIOLET              =  (	0.5804	,	0.0000	,	0.8275	)
    FR_DARKGRAY                =  (	0.6627	,	0.6627	,	0.6627	)
    FR_SALMON                  =  (	0.9804	,	0.5020	,	0.4471	)
    FR_DARKMAGENTA             =  (	0.5451	,	0.0000	,	0.5451	)
    FR_TOMATO                  =  (	1.0000	,	0.3882	,	0.2784	)
    FR_WHITESMOKE              =  (	0.9608	,	0.9608	,	0.9608	)
    FR_GOLDENROD               =  (	0.8549	,	0.6471	,	0.1255	)
    FR_MEDIUMSPRINGGREEN       =  (	0.0000	,	0.9804	,	0.6039	)
    FR_DODGERBLUE              =  (	0.1176	,	0.5647	,	1.0000	)
    FR_AQUA                    =  (	0.0000	,	1.0000	,	1.0000	)
    FR_FORESTGREEN             =  (	0.1333	,	0.5451	,	0.1333	)
    FR_LEMONCHIFFON            =  (	1.0000	,	0.9804	,	0.8039	)
    FR_LIGHTSLATEGRAY          =  (	0.4667	,	0.5333	,	0.6000	)
    FR_SLATEGRAY               =  (	0.4392	,	0.5020	,	0.5647	)
    FR_LIGHTGRAY               =  (	0.8275	,	0.8275	,	0.8275	)
    FR_INDIGO                  =  (	0.2941	,	0.0000	,	0.5098	)
    FR_CADETBLUE               =  (	0.3725	,	0.6196	,	0.6275	)
    FR_LIGHTYELLOW             =  (	1.0000	,	1.0000	,	0.8784	)
    FR_DARKORANGE              =  (	1.0000	,	0.5490	,	0.0000	)
    FR_POWDERBLUE              =  (	0.6902	,	0.8784	,	0.9020	)
    FR_ROYALBLUE               =  (	0.2549	,	0.4118	,	0.8824	)
    FR_SIENNA                  =  (	0.6275	,	0.3216	,	0.1765	)
    FR_THISTLE                 =  (	0.8471	,	0.7490	,	0.8471	)
    FR_LIME                    =  (	0.0000	,	1.0000	,	0.0000	)
    FR_SEASHELL                =  (	1.0000	,	0.9608	,	0.9333	)
    FR_DARKRED                 =  (	0.5451	,	0.0000	,	0.0000	)
    FR_LIGHTSKYBLUE            =  (	0.5294	,	0.8078	,	0.9804	)
    FR_YELLOWGREEN             =  (	0.6039	,	0.8039	,	0.1961	)
    FR_AQUAMARINE              =  (	0.4980	,	1.0000	,	0.8314	)
    FR_LIGHTCORAL              =  (	0.9412	,	0.5020	,	0.5020	)
    FR_DARKSLATEGRAY           =  (	0.1843	,	0.3098	,	0.3098	)
    FR_KHAKI                   =  (	0.9412	,	0.9020	,	0.5490	)
    FR_DARKGREY                =  (	0.6627	,	0.6627	,	0.6627	)
    FR_BURLYWOOD               =  (	0.8706	,	0.7216	,	0.5294	)
    FR_LIGHTGOLDENRODYELLOW    =  (	0.9804	,	0.9804	,	0.8235	)
    FR_MEDIUMBLUE              =  (	0.0000	,	0.0000	,	0.8039	)
    FR_DARKSALMON              =  (	0.9137	,	0.5882	,	0.4784	)
    FR_ROSYBROWN               =  (	0.7373	,	0.5608	,	0.5608	)
    FR_LIGHTSALMON             =  (	1.0000	,	0.6275	,	0.4784	)
    FR_PALEVIOLETRED           =  (	0.8588	,	0.4392	,	0.5765	)
    FR_CORAL                   =  (	1.0000	,	0.4980	,	0.3137	)
    FR_VIOLET                  =  (	0.9333	,	0.5098	,	0.9333	)
    FR_GREY                    =  (	0.5020	,	0.5020	,	0.5020	)
    FR_LIGHTGREEN              =  (	0.5647	,	0.9333	,	0.5647	)
    FR_LINEN                   =  (	0.9804	,	0.9412	,	0.9020	)
    FR_ORANGERED               =  (	1.0000	,	0.2706	,	0.0000	)
    FR_DIMGRAY                 =  (	0.4118	,	0.4118	,	0.4118	)
    FR_MAROON                  =  (	0.5020	,	0.0000	,	0.0000	)
    FR_LIGHTPINK               =  (	1.0000	,	0.7137	,	0.7569	)
    FR_MEDIUMAQUAMARINE        =  (	0.4000	,	0.8039	,	0.6667	)
    FR_OLDLACE                 =  (	0.9922	,	0.9608	,	0.9020	)

#Box type when for widgets
class FR_BoxType: #There will not be any boundary box or bkg box
    FR_NoBox=                 0
    FR_FLAT_BOX=             10
    FR_TOP_BOX=              20
    FR_BOTTOM_BOX=           30
    FR_BORDER_FRAME=         40      
    FR_ROUNDED_BOX=          50
    FR_ROUNDED_FRAME=        60
    FR_ROUND_FLAT_BOX=       70
    FR_ROUND_TOP_BOX=        80
    FR_ROUND_BOTTOM_BOX=     90
    FR_OVAL_BOX=            100
    FR_OVAL_FRAME=          110
    FR_TRIANGLE_BOX=        120
    FR_TRIANGLE_FRAME=      130

#This constant should determine the type of redraw required 
class FR_DAMAGE:
    FR_ALL_DAMAGE=     0
    FR_LBL_DAMAGE=    10
    FR_DRAW_DAMAGE=   20
     
           
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

class FR_ALIGN:
    '''
    Alignment constants: 
    If TOP/BOTTOM not specified, always default is BOTTOM
    '''
    FR_NO_ALIGN             = 0
    FR_ALIGN_LEFT           =10
    FR_ALIGN_RIGHT          =20
    FR_ALIGN_TOP            =30
    FR_ALIGN_BOTTOM         =40
    FR_ALIGN_H_CENTER       =50
    FR_ALIGN_V_CENTER       =60
    FR_ALIGN_CENTER         =FR_ALIGN_H_CENTER
        
    FR_ALIGN_LEFT_BOTTOM    =FR_ALIGN_LEFT+FR_ALIGN_BOTTOM
    FR_ALIGN_LEFT_TOP       =FR_ALIGN_LEFT+FR_ALIGN_TOP
    
    FR_ALIGN_RIGHT_TOP      =FR_ALIGN_RIGHT+FR_ALIGN_TOP
    FR_ALIGN_RIGHT_BOTTOM   =FR_ALIGN_RIGHT+FR_ALIGN_BOTTOM

    FR_ALIGN_CENTER_TOP     =FR_ALIGN_H_CENTER+FR_ALIGN_TOP
    FR_ALIGN_CENTER_BOTTOM  =FR_ALIGN_H_CENTER+FR_ALIGN_BOTTOM

    FR_ALIGN_CENTER_TOP     =FR_ALIGN_V_CENTER+FR_ALIGN_TOP
    FR_ALIGN_CENTER_BOTTOM  =FR_ALIGN_V_CENTER+FR_ALIGN_BOTTOM

    FR_ALIGN_CENTER_TOP     =FR_ALIGN_CENTER+FR_ALIGN_TOP
    FR_ALIGN_CENTER_BOTTOM  =FR_ALIGN_CENTER+FR_ALIGN_BOTTOM

    FR_ALIGN_CENTER_CENTER  =FR_ALIGN_CENTER+FR_ALIGN_TOP
    
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
         PAGE_TOP, PAGE_BOTTOM, END,
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