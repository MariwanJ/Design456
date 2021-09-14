# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - App.  *
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
import Design456Init
sys.path.append(Design456Init.WIDGETS3D_PATH)
"""Notice that if you don't put these imports in order
    Loading the workbench might fail
    Don't change their positions.
"""
from constant import FR_COLOR
import pivy.coin as coin
import FreeCADGui as Gui
import FreeCAD as App


def dim_dash(p1, p2, color, LineWidth):
    dash = coin.SoSeparator()
    v = coin.SoVertexProperty()
    v.vertex.set1Value(0, p1)
    v.vertex.set1Value(1, p2)
    line = coin.SoLineSet()
    line.vertexProperty = v
    style = coin.SoDrawStyle()
    style.lineWidth = LineWidth
    my_transparency = coin.SoMaterial()
    my_transparency.transparency.setValue(0.5)
    dash.addChild(style)
    dash.addChild(my_transparency)
    dash.addChild(color)
    dash.addChild(line)
    return dash


class Grid:
    collectGarbage = []
    sg=None
    def __init__(self, view):
        self.view = view
        self.sg = None
        self.collectGarbage = []  # Keep the nodes for removing

    def Deactivated(self):
        self.removeGarbage()
        
    def Activated(self):
        try:
            self.sg = Gui.ActiveDocument.ActiveView.getSceneGraph()
            # Draw xy plane
            self.drawXYPlane()
            # Draw Z plane
            self.drawZAxis()
            # Draw Axis
            self.draw_XandYandZZeroAxis()

        except Exception as err:
            App.Console.PrintError("'Plane' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def drawZAxis(self):
        col = coin.SoBaseColor()
        col.rgb = FR_COLOR.FR_YELLOW  # (237, 225, 0) # Yellow
        LengthOfGrid = 500  # mm
        bothSideLength = LengthOfGrid / 2
        GridSize = 5
        counter = LengthOfGrid
        try:
            line = []
            for i in range(0, counter, GridSize):
                # X direction
                P1x = -2
                P1y = 0
                P2x = +2
                P1y = 0
                line.append(dim_dash((P1x, P1y, -bothSideLength + i),
                            (P2x, P1y, -bothSideLength + i), col, 1))  # x
            for i in line:
                self.sg.addChild(i)
                self.collectGarbage.append(i)

        except Exception as err:
            App.Console.PrintError("'Plane' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_XandYandZZeroAxis(self):

        col1 = coin.SoBaseColor()
        col2 = coin.SoBaseColor()
        col3 = coin.SoBaseColor()
        col1.rgb = FR_COLOR.FR_RED  # RED
        col2.rgb = FR_COLOR.FR_GREEN  # GREEN
        col3.rgb = FR_COLOR.FR_BLUE  # BLUE

        LengthOfGrid = 1000  # mm
        try:
            line = []
            line.append(dim_dash((-LengthOfGrid, 0.0, 0.0),
                        (+LengthOfGrid, 0.0, 0.0), col1, 5))  # x
            line.append(dim_dash((0.0, -LengthOfGrid, 0.0),
                        (0.0, +LengthOfGrid, 0.0), col2, 5))  # y
            line.append(dim_dash((0.0, 0.0, -LengthOfGrid),
                        (0.0, 0.0, LengthOfGrid), col3, 5))  # y

            for i in range(0, 3):
                self.sg.addChild(line[i])
                self.collectGarbage.append(line[i])

        except Exception as err:
            App.Console.PrintError("'Plane' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def removeGarbage(self):
        for i in (self.collectGarbage):
            self.sg.removeChild(i)

        self.collectGarbage.clear()
        del self

    def drawXYPlane(self):
        col = coin.SoBaseColor()
        col.rgb = FR_COLOR.FR_BLUEG
        LengthOfGrid = 1000  # mm
        bothSideLength = LengthOfGrid / 2
        GridSize = 2
        counter = LengthOfGrid
        try:
            line = []
            count5Cells = 0
            lineSize = 1
            for i in range(0, counter, GridSize):
                # X direction
                P1x = -bothSideLength
                P1y = -bothSideLength + i

                # y direction
                P3x = -bothSideLength + i
                P3y = -bothSideLength

                if count5Cells == 0:
                    lineSize = 2
                else:
                    lineSize = 1
                # don't draw line at 0,±y and ±x,0
                # TODO: Draw x, y using correct color
                if P1y != 0:
                    line.append(dim_dash((P1x, P1y, 0.0),
                                (-P1x, P1y, 0.0), col, lineSize))  # x

                if P3x != 0:
                    line.append(dim_dash((P3x, P3y, 0.0),
                                (P3x, -P3y, 0.0), col, lineSize))  # y

                count5Cells = count5Cells + 1
                if count5Cells == 5:
                    count5Cells = 0
            for i in line:
                self.sg.addChild(i)
                self.collectGarbage.append(i)

        except Exception as err:
            App.Console.PrintError("'Plane' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
            
class DocObserver:
    linkToParent = None

    def slotCreatedDocument(self, doc):
        v = Gui.ActiveDocument.ActiveView
        if (self.linkToParent != None):
            if(self.linkToParent.planeShow == None):
                self.linkToParent.planeShow = Grid(v)
                self.linkToParent.planeShow.Activated()

    def setLink(self, linkToParent=None):
        self.linkToParent = linkToParent
        
    #def slotDeletedDocument(self, doc):
    #    "This function is executed when the workbench is deactivated"
    #    #App.removeDocumentObserver(doc)
    #    if (self.linkToParent is not None):
    #        self.linkToParent.planeShow.Deactivated()
    #        #self.linkToParent.planeShow = None
    #        #del self.linkToParent
    #        #self.linkToParent = None
