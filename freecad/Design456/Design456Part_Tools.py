# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2025 Mariwan Jalal ( mariwan.jalal@gmail.com )
# SPDX-FileNotice: Part of the Design456 addon.

from __future__ import unicode_literals

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init

import  Design456_3DTools
import  Design456_2DTools

__updated__ = '2022-06-08 19:08:23'

class Design456Part_Tools:
    list = ["Design456_3DToolsGroup",
            "Design456_2DToolsGroup"
            
            ]

    """Design456 Part Tools Toolbar"""

    def GetResources(self):
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'Part_Tools.svg',
            'MenuText': 'Tools',
            'ToolTip':  'Tools'
        }

    def IsActive(self):
        """Return True when this command should be available."""
        if Gui.activeDocument():
            return True
        else:
            return False
        
    def Activated(self):
        self.appendToolbar("Design456Part_Tools", self.list)
