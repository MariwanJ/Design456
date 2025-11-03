from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2025                                                    *
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
'''
        This file contains some help and debug functions. Not meant to be used in the wb. Just for debug
'''

def eventEmuToText(event):
    if event == 0x0000     :   return"FR_NO_EVENT"
    if event == 0xDD10     :   return"FR_MOUSE_LEFT_PUSH"
    if event == 0xDD20     :   return"FR_MOUSE_RIGHT_PUSH"
    if event == 0xDD30     :   return"FR_MOUSE_MIDDLE_PUSH"
    if event == 0xDD40     :   return"FR_MOUSE_LEFT_RELEASE"
    if event == 0xDD50     :   return"FR_MOUSE_RIGHT_RELEASE"
    if event == 0xDD60     :   return"FR_MOUSE_MIDDLE_RELEASE"
    if event == 0xDD70     :   return"FR_MOUSE_LEFT_DOUBLECLICK"
    if event == 0xDD80     :   return"FR_MOUSE_DRAG"
    if event == 0xDD90     :   return"FR_MOUSE_MOVE"
    if event == 1          :   return"FR_UNDEFINED"
    if event == 0XFFE1     :   return"FR_LEFT_SHIFT"
    if event == 0XFFE2     :   return"FR_RIGHT_SHIFT"
    if event == 0XFFE3     :   return"FR_LEFT_CONTROL"
    if event == 0XFFE4     :   return"FR_RIGHT_CONTROL"
    if event == 0XFFE9     :   return"FR_LEFT_ALT"
    if event == 0XFFEA     :   return"FR_RIGHT_ALT"
    if event == 0X0030     :   return"FR_NUMBER_0"
    if event == 0X0031     :   return"FR_NUMBER_1"
    if event == 0X0032     :   return"FR_NUMBER_2"
    if event == 0X0033     :   return"FR_NUMBER_3"
    if event == 0X0034     :   return"FR_NUMBER_4"
    if event == 0X0035     :   return"FR_NUMBER_5"
    if event == 0X0036     :   return"FR_NUMBER_6"
    if event == 0X0037     :   return"FR_NUMBER_7"
    if event == 0X0038     :   return"FR_NUMBER_8"
    if event == 0X0039     :   return"FR_NUMBER_9"
    if event == 0X0061     :   return"FR_A"
    if event == 0X0062     :   return"FR_B"
    if event == 0X0063     :   return"FR_C"
    if event == 0X0064     :   return"FR_D"
    if event == 0X0065     :   return"FR_E"
    if event == 0X0066     :   return"FR_F"
    if event == 0X0067     :   return"FR_G"
    if event == 0X0068     :   return"FR_H"
    if event == 0X0069     :   return"FR_I"
    if event == 0X006A     :   return"FR_J"
    if event == 0X006B     :   return"FR_K"
    if event == 0X006C     :   return"FR_L"
    if event == 0X006D     :   return"FR_M"
    if event == 0X006E     :   return"FR_N"
    if event == 0X006F     :   return"FR_O"
    if event == 0X0070     :   return"FR_P"
    if event == 0X0071     :   return"FR_Q"
    if event == 0X0072     :   return"FR_R"
    if event == 0X0073     :   return"FR_S"
    if event == 0X0074     :   return"FR_T"
    if event == 0X0075     :   return"FR_U"
    if event == 0X0076     :   return"FR_V"
    if event == 0X0077     :   return"FR_W"
    if event == 0X0078     :   return"FR_X"
    if event == 0X0079     :   return"FR_Y"
    if event == 0X007A     :   return"FR_Z"
    if event == 0XFF50     :   return"FR_HOME"
    if event == 0XFF51     :   return"FR_LEFT_ARROW"
    if event == 0XFF52     :   return"FR_UP_ARROW"
    if event == 0XFF53     :   return"FR_RIGHT_ARROW"
    if event == 0XFF54     :   return"FR_DOWN_ARROW"
    if event == 0XFF55     :   return"FR_PAGE_TOP"
    if event == 0XFF56     :   return"FR_PAGE_BOTTOM"
    if event == 0XFF57     :   return"FR_END"
    if event == 0XFF8D     :   return"FR_PAD_ENTER"
    if event == 0XFF91     :   return"FR_PAD_F1"
    if event == 0XFF92     :   return"FR_PAD_F2"                        
    if event == 0XFF93     :   return"FR_PAD_F3"                        
    if event == 0XFF94     :   return"FR_PAD_F4"
    if event == 0XFF9E     :   return"FR_PAD_0"
    if event == 0XFF9C     :   return"FR_PAD_1"
    if event == 0XFF99     :   return"FR_PAD_2"
    if event == 0XFF9B     :   return"FR_PAD_3"
    if event == 0XFF96     :   return"FR_PAD_4"
    if event == 0XFF9D     :   return"FR_PAD_5"
    if event == 0XFF98     :   return"FR_PAD_6"
    if event == 0XFF95     :   return"FR_PAD_7"
    if event == 0XFF97     :   return"FR_PAD_8"
    if event == 0XFF9A     :   return"FR_PAD_9"
    if event == 0XFFAB     :   return"FR_PAD_ADD"
    if event == 0XFFAD     :   return"FR_PAD_SUBTRACT"
    if event == 0XFFAA     :   return"FR_PAD_MULTIPLY"
    if event == 0XFFAF     :   return"FR_PAD_DIVIDE"
    if event == 0XFF8D     :   return"FR_PAD_SPACE"
    if event == 0XFF89     :   return"FR_PAD_TAB"
    if event == 0XFF9E     :   return"FR_PAD_INSERT"
    if event == 0XFF9F     :   return"FR_PAD_DELETE"
    if event == 0XFF9F     :   return"FR_PAD_PERIOD"
    if event == 0XFF08     :   return"FR_BACKSPACE"
    if event == 0XFF09     :   return"FR_TAB"
    if event == 0XFF0D     :   return"FR_RETURN"
    if event == 0XFF0D     :   return"FR_ENTER"
    if event == 0XFF13     :   return"FR_PAUSE"
    if event == 0XFF14     :   return"FR_SCROLL_LOCK"
    if event == 0XFF1B     :   return"FR_ESCAPE"
    if event == 0XFFFF     :   return"FR_DELETE"
    if event == 0XFFFF     :   return"FR_KEY_DELETE"
    if event == 0XFF61     :   return"FR_PRINT"
    if event == 0XFF63     :   return"FR_INSERT"
    if event == 0XFF7F     :   return"FR_NUM_LOCK"
    if event == 0XFFE5     :   return"FR_CAPS_LOCK"
    if event == 0XFFE6     :   return"FR_SHIFT_LOCK"
    if event == 0X0020     :   return"FR_SPACE"
    if event == 0X0027     :   return"FR_APOSTROPHE"
    if event == 0X002C     :   return"FR_COMMA"
    if event == 0X002D     :   return"FR_MINUS"
    if event == 0X002E     :   return"FR_PERIOD"
    if event == 0X002F     :   return"FR_SLASH"
    if event == 0X003B     :   return"FR_SEMICOLON"
    if event == 0X003D     :   return"FR_EQUAL"
    if event == 0X005B     :   return"FR_BRACKETLEFT"
    if event == 0X005C     :   return"FR_BACKSLASH"
    if event == 0X005D     :   return"FR_BRACKETRIGHT"
    if event == 0X0060     :   return"FR_GRAVE"
                                                    
                                        
                                    
                                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    