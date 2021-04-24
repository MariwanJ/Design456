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

'''
display knots and poles of a selected curve
'''

import FreeCAD as App
import FreeCADGui as Gui
import os, sys

import NURBSinit

import Draft

class Nurbs_DisplayKontsandPolseForCurve:
    def Activated(self):
        ''' for all selected curves two wires are created
        one displays all poles and the other all knotes
        the created objects are not parametric
        '''

        sx=Gui.Selection.getSelection()
        for s in sx:
            print (s,s.SubObjects)
            for i,e in enumerate(s.SubObjects):
                edge=e
                name=s.SubElementNames[i]

                bc=e.Curve
                pts=e.Curve.getPoles()
                print ("Poles", len(pts))
                _t=Draft.makeWire(pts,closed=True,face=False)
                App.ActiveDocument.ActiveObject.Label="Poles of "+s.Object.Label + " " + name
                App.ActiveDocument.ActiveObject.ViewObject.PointSize=5
                App.ActiveDocument.ActiveObject.ViewObject.PointColor=(1.,0.,1.)
                App.ActiveDocument.ActiveObject.ViewObject.LineColor=(1.,0.,1.)

                pts2=[bc.value(k) for k in bc.getKnots()]
                print ("Knots:",len(pts2))
                _t=Draft.makeWire(pts2,closed=True,face=False)
                App.ActiveDocument.ActiveObject.Label="Knotes of "+s.Object.Label +   " " + name
                App.ActiveDocument.ActiveObject.ViewObject.PointSize=10
                App.ActiveDocument.ActiveObject.ViewObject.PointColor=(0.,1.,1.)
                App.ActiveDocument.ActiveObject.ViewObject.LineColor=(0.,1.,1.)
    #dont run make a class
    #ThousandsOfRunWhatShouldIdo()

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("DisplayKontsandPolseForCurve")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "DisplayKontsandPolseForCurve"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_DisplayKontsandPolseForCurve", Nurbs_DisplayKontsandPolseForCurve())

