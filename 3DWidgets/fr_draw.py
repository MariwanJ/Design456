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

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import Design456Init

# draw a line in 3D world


def draw_line(p1, p2, color, LineWidth):
    try:
        dash = coin.SoSeparator()
        v = coin.SoVertexProperty()
        v.vertex.set1Value(0, p1)
        v.vertex.set1Value(1, p2)
        coords = coin.SoTransform()
        line = coin.SoLineSet()
        line.vertexProperty = v
        style = coin.SoDrawStyle()
        style.lineWidth = LineWidth
        dash.addChild(style)
        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = color
        dash.addChild(col1)
        dash.addChild(line)
        dash.addChild(coords)
        return dash

    except Exception as err:
        App.Console.PrintError("'makeIt' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def draw_box(*vertices, color, LineWidth):
    """
        Draw any box. This will be the base of all multi-point drawing.
        Curves, and arc is not here.
    """
    if len(vertices) < 4:
        raise ValueError('Vertices must be 4')
    dash = coin.SoSeparator()
    v = coin.SoVertexProperty()
    coords = coin.SoTransform()
    square = coin.SbBox3f(p1, p2, p3, p4)
    square.vertexProperty = v
    style = coin.SoDrawStyle()
    style.lineWidth = LineWidth
    dash.addChild(style)
    dash.addChild(color)
    dash.addChild(square)
    dash.addChild(coords)
    return draw_square


def draw_polygon(vertices, color, LineWidth):
    """
        Draw any polygon. This will be the base of all multi-point drawing.
        Curves, and arc is not here.
    """
    if len(vertices) < 4:
        raise ValueError('Vertices must be 4')
    _polygon = coin.SoSeparator()
    col=coin.SoBaseColor()
    col.rgb= color
    coords = coin.SoTransform()
    data=coin.SoCoordinate3()
    face=coin.SoIndexedFaceSet()
    style = coin.SoDrawStyle()
    style.lineWidth = LineWidth
    _polygon.addChild(style)
    _polygon.addChild(col)
    _polygon.addChild(coords)
    _polygon.addChild(data)
    _polygon.addChild(face)
 
    i = 0   
    for vr in vertices:
        data.point.set1Value(i, vr[0], vr[1], vr[2])
    i += 1;
    polygons = [0, 1, 2, 3, -1] # -1 means that the n-gon is terminated and a new one can be created with the next points

    i = 0
    for p in polygons:
        face.coordIndex.set1Value(i, p)
    i += 1;
    return _polygon


# Draw a square 3D World
def draw_square(vector, color, LineWidth):
    """ Draw a square and return the SoSeparator"""
    return draw_polygon([p1, p2, p3, p4], color, LineWidth)


def draw_square_frame(vertices, color, LineWidth):
    if len(vertices) < 3:
        raise ValueError('Vertices must be more than 2')
    result = []

    result.append(draw_line(vertices[0], vertices[1], color, LineWidth))
    result.append(draw_line(vertices[1], vertices[2], color, LineWidth))
    result.append(draw_line(vertices[2], vertices[3], color, LineWidth))
    result.append(draw_line(vertices[3], vertices[0], color, LineWidth))
    return result
