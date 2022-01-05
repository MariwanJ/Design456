# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# **************************************************************************
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
import FreeCAD as App
import FreeCADGui as Gui
from pivy import coin
import FACE_D as faced
from PySide.QtCore import QT_TRANSLATE_NOOP
from typing import List
import Design456Init
from PySide import QtGui, QtCore
from ThreeDWidgets.fr_arrow_widget import Fr_Arrow_Widget
from ThreeDWidgets import fr_arrow_widget
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from draftutils.translate import translate  # for translation
import math


MouseScaleFactor = 1.5

__updated__ = ''

def callback_move(userData: fr_arrow_widget.userDataObject = None):
    pass

def callback_release(userData: fr_arrow_widget.userDataObject = None):
    pass

# This tool should easily more, rotate and place any object. 
# Rotation Axis must be changable. Default will be centerofmass
# but it can also choose other by moving the Axis bar which will be
# a COIN3D bar or line. 
# This must make placement of object much much easier and simpler. 

class Design456_SmartMove:
    """
        Apply Move to any 3D object by selecting the object.
    """
    def __init__(self):
        pass

    def Activated(self):
        pass

    def __del__(self):
        pass
    
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_Move.svg',
            'MenuText': ' Smart Move',
                        'ToolTip':  ' Smart Move'
        }


Gui.addCommand('Design456_SmartMove', Design456_SmartMove())
