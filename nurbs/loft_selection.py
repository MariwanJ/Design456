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
# * Modified and adapted to Desing456 by:                                  *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

import FreeCAD as App
import FreeCADGui as Gui
import os, sys

import NURBSinit


from FreeCAD import Base
import Part
App=FreeCAD



# todo: parametric source
# flags 

class Nurbs_LoftSelectionEdge:
    def Activated(self):
        self.runOnEdges()

    def runOnEdges(self):
        '''version bei selektierten geschlossenen Kanten'''
        import FreeCADGui as Gui 
        import Part
        wx=Gui.Selection.getSelection()

        sls=[]
        for w in wx:
            sob=w.SubObjects[0]
            if  sob.__class__.__name__ == 'Face':
                sls += [w.SubObjects[0].Wires[0]]
            else:
                sls += [w.SubObjects[0]]

        l=Part.makeLoft(sls,True,True,False)
        Part.show(l)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_LoftSelectionEdge")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_LoftSelectionEdge"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_LoftSelectionEdge", Nurbs_LoftSelectionEdge())

class Nurb_LoftSelection:
    def Activated(self):
        self.runme()
        
    def runme(self):
        ribs=Gui.Selection.getSelection()
        l=App.ActiveDocument.addObject('Part::Loft','Loft')
        l.Ruled = True
        l.Sections=ribs
        App.ActiveDocument.recompute()

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurb_LoftSelection")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurb_LoftSelection"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurb_LoftSelection", Nurb_LoftSelection())


