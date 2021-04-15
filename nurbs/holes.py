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
import Part
import Design456Init
import random


class holes:
    """ holes """
    def Activated(self):
        self.run()

    def run(self):
        sel = Gui.Selection.getSelectionEx()

        face = sel[0].Shape.Face1.Surface.toShape()
        # Part.show(face)

        # face=sel[0].Shape.Face1

        wireobs = sel[1:]

        print(face)
        wires = []
        for w in wireobs:
            print(w.Shape.Wires)
            wires += [w.Shape.Wires[0]]

        es = wires
        if len(es) > 0:
            splita = []
            for i, e in enumerate(es):

                edges = e.Edges
                ee = edges[0]
                # if dirs[i]: ee.reverse()

                e.reverse()
                splita += [(e, face)]

            r = Part.makeSplitShape(face, splita)
            print(r)
            for fs in r:
                for f in fs:
                    Part.show(f)
                    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor = (
                        random.random(), random.random(), random.random(),)

        else:
            Part.show(face)
            App.ActiveDocument.ActiveObject.ViewObject.ShapeColor = (
                random.random(), random.random(), random.random(),)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.NURBS_ICON_PATH + 'holes.svg',
            'MenuText': 'holes',
            'ToolTip':  'holes'
        }


Gui.addCommand('holes', holes())
holes.__doc__ = """holes: Tobe added later     """


class Nurbs_extractWires:
    def Activated(self):
        '''extract the wires'''
        sel = Gui.Selection.getSelection()
        w = sel[0]
        print(w.Shape.Wires)
        for i, wire in enumerate(w.Shape.Wires):
            Part.show(wire)
            App.ActiveDocument.ActiveObject.Label = "wire " + \
                str(i+1) + " for " + w.Label + " "
            wire.reverse()
            Part.show(wire)
            App.ActiveDocument.ActiveObject.Label = "wire " + \
                str(i+1) + " for " + w.Label + " reverse "

    def GetResources(self):
        return {
            'Pixmap': Design456Init.NURBS_ICON_PATH + 'extractwire.svg',
            'MenuText': 'Nurbs_extractWires',
            'ToolTip':  'Nurbs_extractWires'
        }


Gui.addCommand('Nurbs_extractWires', Nurbs_extractWires())
Nurbs_extractWires.__doc__ = """Nurbs_extractWires: Tobe added later     """
