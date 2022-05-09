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
import os, sys
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
from draftutils.translate import translate  # for translation
import Design456Init 

from Design456Pref import Design456pref_var  #Variable shared between preferences and other tools

__updated__ = '2022-04-27 18:37:54'

#Design some command for deciding which grid we should use for all mouse movements_sizes 
#In PartMover, Paint ..etc


class GridSizePointOne:
    def Activated(self):
        Design456pref_var.MouseStepSize=0.10   #0.1 mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizePointOne.svg',
                'MenuText': "Grid1.0mm",
                'ToolTip': "Grid Size 1.0 mm"}
Gui.addCommand('GridSizePointOne', GridSizePointOne())

class GridSizeOne:
    def Activated(self):
        Design456pref_var.MouseStepSize=1.0   #mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizeOne.svg',
                'MenuText': "Grid1.0mm",
                'ToolTip': "Grid Size 1.0 mm"}
Gui.addCommand('GridSizeOne', GridSizeOne())

class GridSizeTwo:
    def Activated(self):
        Design456pref_var.MouseStepSize=2.0   #mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizeTwo.svg',
                'MenuText': "Grid2.0mm",
                'ToolTip': "Grid Size 2.0 mm"}
Gui.addCommand('GridSizeTwo', GridSizeTwo())

class GridSizeThree:
    def Activated(self):
        Design456pref_var.MouseStepSize=3.0   #mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizeThree.svg',
                'MenuText': "Grid3.0mm",
                'ToolTip': "Grid Size 3.0 mm"}
Gui.addCommand('GridSizeThree', GridSizeThree())

class GridSizeFour:
    def Activated(self):
        Design456pref_var.MouseStepSize=4.0   #mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizeFour.svg',
                'MenuText': "Grid4.0mm",
                'ToolTip': "Grid Size 4.0 mm"}
Gui.addCommand('GridSizeFour', GridSizeFour())


class GridSizeFive:
    def Activated(self):
        Design456pref_var.MouseStepSize=5.0   #mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizeFive.svg',
                'MenuText': "Grid5.0mm",
                'ToolTip': "Grid Size 5.0 mm"}
Gui.addCommand('GridSizeFive', GridSizeFive())

class GridSizeSix:
    def Activated(self):
        Design456pref_var.MouseStepSize=6.0   #mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizeSix.svg',
                'MenuText': "Grid6.0mm",
                'ToolTip': "Grid Size 6.0 mm"}
Gui.addCommand('GridSizeSix', GridSizeSix())

class GridSizeSeven:
    def Activated(self):
        Design456pref_var.MouseStepSize=7.0   #mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizeSeven.svg',
                'MenuText': "Grid7.0mm",
                'ToolTip': "Grid Size 7.0 mm"}
Gui.addCommand('GridSizeSeven', GridSizeSeven())

class GridSizeEight:
    def Activated(self):
        Design456pref_var.MouseStepSize=8.0   #mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizeEight.svg',
                'MenuText': "Grid8.0mm",
                'ToolTip': "Grid Size 8.0 mm"}
Gui.addCommand('GridSizeEight', GridSizeEight())

class GridSizeNine:
    def Activated(self):
        Design456pref_var.MouseStepSize=9.0   #mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizeNine.svg',
                'MenuText': "Grid9.0mm",
                'ToolTip': "Grid Size 9.0 mm"}
Gui.addCommand('GridSizeNine', GridSizeNine())

class GridSizeTen:
    def Activated(self):
        Design456pref_var.MouseStepSize=10.0   #mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizeTen.svg',
                'MenuText': "Grid10.0mm",
                'ToolTip': "Grid Size 10.0 mm"}
Gui.addCommand('GridSizeTen', GridSizeTen())

class GridSizeFifteen:
    def Activated(self):
        Design456pref_var.MouseStepSize=15.0   #mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizeFifteen.svg',
                'MenuText': "Grid15.0mm",
                'ToolTip': "Grid Size 15.0 mm"}
Gui.addCommand('GridSizeFifteen', GridSizeFifteen())

class GridSizeTwenty:
    def Activated(self):
        Design456pref_var.MouseStepSize=20.0   #mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizeTwenty.svg',
                'MenuText': "Grid20.0mm",
                'ToolTip': "Grid Size 20.0 mm"}
Gui.addCommand('GridSizeTwenty', GridSizeTwenty())

class GridSizeThirty:
    def Activated(self):
        Design456pref_var.MouseStepSize=20.0   #mm Size
    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'GridSizeThirty.svg',
                'MenuText': "Grid30.0mm",
                'ToolTip': "Grid Size 30.0 mm"}
Gui.addCommand('GridSizeThirty', GridSizeThirty())



#############################


class Design456_GridSize:
    list = ["GridSizePointOne",
            
            "GridSizeThirty",
            
            ]

    """Design456 Grid Size Toolbar"""

    def GetResources(self):
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'GridSize.svg',
            'MenuText': 'GridSize',
            'ToolTip':  'GridSize'
        }

    def IsActive(self):
        """Return True when this command should be available."""
        if Gui.activeDocument():
            return True
        else:
            return False
        
    def Activated(self):
        self.appendToolbar("Design456_GridSize", self.list)
