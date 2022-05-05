# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *                                                                         *
# *                                                                         *
# *  This library is free software; you can redistribute it and/or          *
# *  modify it under the terms of the GNU Lesser General Public             *
# *  License as published by the Free Software Foundation; either           *
# *  version 2 of the License, or (at your option) any later version.       *
# *                                                                         *
# *  This library is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# *  Lesser General Public License for more details.                        *
# *                                                                         *
# *  You should have received a copy of the GNU Lesser General Public       *
# *  License along with this library; if not, If not, see                   *
# *  <http://www.gnu.org/licenses/>.                                        *
# *                                                                         *
# *  Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# ***************************************************************************
import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import math
from draftutils.translate import translate  # for translation
from Design456Init import DefaultGridSize

__updated__ = '2022-04-27 18:37:54'

#Design some command for deciding which grid we should use for all mouse movements_sizes 
#In PartMover, Paint ..etc


def setGridSize(_gridSize):
        DefaultGridSize=_gridSize


# def setgridSize_1mm():
#     setGridSize(1.0)    
# def setgridSize_1mm():
#     setGridSize(2.0)    
# def setgridSize_2mm():
#     setGridSize(1.0)    
# def setgridSize_3mm():
#     setGridSize(3.0)    
# def setgridSize_4mm():
#     setGridSize(4.0)    
# def setgridSize_5mm():
#     setGridSize(5.0)    
# def setgridSize_6mm():
#     setGridSize(6.0)    
# def setgridSize_7mm():
#     setGridSize(7.0)    
# def setgridSize_8mm():
#     setGridSize(8.0)    
# def setgridSize_8mm():
#     setGridSize(8.0)    
# def setgridSize_9mm():
#     setGridSize(9.0)    
# def setgridSize_9mm():
#     setGridSize(10.0)    
