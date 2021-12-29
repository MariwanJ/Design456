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
import Draft as _draft
import Part as _part
import Design456Init
from pivy import coin
import math
from PySide.QtCore import QT_TRANSLATE_NOOP
from PySide import QtGui, QtCore
from ThreeDWidgets.constant import FR_BRUSHES
import Design456_2Ddrawing
import FACE_D as faced


class Design456_Paint:
    """[Paint different shapes on any direction and with a custom sizes.
        They are 3D shapes that are merged if they are intersecting each other.
    ]

    """

    def __init__(self):
        self.brushType: FR_BRUSHES = FR_BRUSHES.FR_SQUARE_BRUSH
        self.mw = None
        self.dialog = None  # Dialog for the tool
        self.tab = None  # Tabs
        self.smartInd = None  # ?
        self._mywin = None                           #
        self.b1 = None                               #
        self.PaintLBL = None  # Label
        self.pl = App.Placement()
        self.pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)  # Initial position
        # Initial position - will be changed by the mouse
        self.pl.Base = App.Vector(0.0, 0.0, 0.0)
        self.AllObjects = []  # Merged shapes
        self.lstBrushSize = None  # GUI combobox -brush size
        self.lstBrushType = None  # GUI combobox -brush type
        # current created shape (circle, square, triangles,..etc)
        self.currentObj = None
        self.view = None  # used for captureing mouse events
        self.Observer = None  # Used for captureing mouse events
        self.continuePainting = True
        self.brushSize = 1  # Brush Size
        self.brushType = 0
        self.resultObj = None  # Extruded shape
        self.runOnce = False  # Create the merge object once only
        self.MoveMentDirection = 'A'
        self.firstSize = 0.1
        # used to correct the Placement of the final object
        self.AverageDistanceToOrigion = App.Vector(0, 0, 0)
        self.SelectedObj = None
        self.planeVector = App.Vector(0, 0, 0)
        self.workingPlane = None
        
        # List of the shapes - to add more add it here, in constant and make
        # an "if" statement and a function to draw it
        self.listOfDrawings = ["CIRCLE",
                               "SEMI_CIRCLE",
                               "QUARTER_CIRCLE",
                               "OVAL1",
                               "OVAL2",
                               "EGG",
                               "TRIANGLE",
                               "RIGHT_TRIANGLE",
                               "SCALENE_TRIANGLE",
                               "SQUARE",
                               "EQUALSIDES_PARALLELOGRAM1",
                               "EQUALSIDES_PARALLELOGRAM2",
                               "RECTANGLE1",
                               "RECTANGLE2",
                               "PARALLELOGRAM1",
                               "PARALLELOGRAM2",
                               "RHOMBUS",
                               "PENTAGON",
                               "HEXAGON",
                               "HEPTAGON",
                               "OCTAGON",
                               "ENNEAGON",
                               "DECAGON",
                               "ARROW1",
                               "ARROW2",
                               "ARROW3",
                               "ARROW4",
                               "STAR1",
                               "STAR2",
                               "STAR3",
                               "MOON1",
                               "MOON2",
                               "MOON3",
                               "MOON4",
                               "FILLET1",
                               "FILLET2",
                               "FILLET3",
                               "FILLET4",
                               ]

    def setSize(self):
        """
            [Change the size of the shape]
        """
        self.brushSize = self.lstBrushSize.currentRow()+1
        self.PaintLBL = QtGui.QLabel(
            "Use X,Y,Z to limit the movements\nAnd A for free movement\nPaint Radius or side=" + self.lstBrushSize.currentItem().text())

    def setType(self):
        """[Change the shape type drawn]
        """
        self.brushType = self.lstBrushType.currentRow()

    def draw_circle(self):
        """[Draw a circle (filled)]
        """
        # Convert/ or get Gui object not App object
        try:
            s = App.ActiveDocument.addObject("Part::Cylinder", "Circle")
            s.Radius = self.brushSize
            s.Height = self.firstSize
            return(Gui.ActiveDocument.getObject(s.Name))

        except Exception as err:
            App.Console.PrintError("'draw_circle' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_Semi_circle(self):
        """
            [Draw a semi circle (filled)]
        """
        try:
            first = App.ActiveDocument.addObject("Part::Cylinder", "Circle")
            first.Radius = self.brushSize
            first.Height = self.firstSize
            second = App.ActiveDocument.addObject("Part::Box", "Box")
            second.Width = self.brushSize
            second.Length = self.brushSize*6
            second.Height = self.firstSize
            second.Placement.Base.x = second.Placement.Base.x-self.brushSize*3
            newObj = App.ActiveDocument.addObject("Part::Cut", "cut")
            newObj.Base = first
            newObj.Tool = second
            App.ActiveDocument.recompute()
            # simple copy
            newShape = _part.getShape(
                newObj, '', needSubElement=False, refine=True)
            s = App.ActiveDocument.addObject('Part::Feature', 'HalfCircle')
            s.Shape = newShape
            App.ActiveDocument.removeObject(first.Name)
            App.ActiveDocument.removeObject(second.Name)
            App.ActiveDocument.removeObject(newObj.Name)
            App.ActiveDocument.recompute()
            return(Gui.ActiveDocument.getObject(s.Name))

        except Exception as err:
            App.Console.PrintError("'draw_Semi_circle' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_Quarter_circle(self):
        """[Draw a Quarter of a circle]
        """
        try:
            first = App.ActiveDocument.addObject("Part::Cylinder", "Circle")
            first.Radius = self.brushSize
            first.Height = self.firstSize
            second = App.ActiveDocument.addObject("Part::Box", "Box")
            second.Width = self.brushSize
            second.Length = self.brushSize
            second.Height = self.firstSize
            second.Placement.Base.x = second.Placement.Base.x+self.brushSize/2
            second.Placement.Base.y = second.Placement.Base.y+self.brushSize/2
            newObj = App.ActiveDocument.addObject(
                "Part::MultiCommon", "Common")
            newObj.Shapes = [first, second]
            App.ActiveDocument.recompute()
            # simple copy
            newShape = _part.getShape(
                newObj, '', needSubElement=False, refine=True)
            s = App.ActiveDocument.addObject('Part::Feature', 'QuarterCircle')
            s.Shape = newShape
            App.ActiveDocument.removeObject(first.Name)
            App.ActiveDocument.removeObject(second.Name)
            App.ActiveDocument.removeObject(newObj.Name)
            App.ActiveDocument.recompute()
            return(Gui.ActiveDocument.getObject(s.Name))

        except Exception as err:
            App.Console.PrintError("'draw_Quarter_circle' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_Oval(self, Ovaltype):
        """[Draw Oval - Different types]

        Args:
            Ovaltype ([Integer]): [Type of the oval]
        """
        # Convert/ or get Gui object not App object
        try:
            pl = App.Placement()
            ellipse = None
            pl.Base = self.planeVector
            pl.Rotation.Axis = (0.0, 0.0, 1)
            if Ovaltype == 1:
                pl.Rotation.Angle = math.radians(90.0)
            else:
                pl.Rotation.Angle = 0.0
            ellipse = _draft.makeEllipse(
                self.brushSize, self.brushSize/2, placement=pl, face=True, support=None)
            _draft.autogroup(ellipse)
            App.ActiveDocument.recompute()
            f = App.ActiveDocument.addObject('Part::Extrusion', 'Original')
            f.Base = ellipse
            f.DirMode = "Normal"
            f.DirLink = None
            f.LengthFwd = 0.1
            f.LengthRev = 0.0
            f.Solid = True
            f.Reversed = False
            f.Symmetric = False
            f.TaperAngle = 0.0
            f.TaperAngleRev = 0.0

            f.Dir = ellipse.Shape.normalAt(0, 0)  # Normal line
            if (f.Dir.x != 1 or f.Dir.y != 1 or f.Dir.z != 1):
                f.DirMode = "Custom"
            # Make a simple copy of the object
            App.ActiveDocument.recompute()
            newShape = _part.getShape(
                f, '', needSubElement=False, refine=True)
            s = App.ActiveDocument.addObject('Part::Feature', 'Oval')
            s.Shape = newShape
            App.ActiveDocument.recompute()
            # Remove old objects

            App.ActiveDocument.recompute()
            App.ActiveDocument.removeObject(f.Name)
            App.ActiveDocument.removeObject(ellipse.Name)
            App.ActiveDocument.recompute()
            return(Gui.ActiveDocument.getObject(s.Name))

        except Exception as err:
            App.Console.PrintError("'draw_Oval' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_Egg(self):
        print("Not implemented Yet")

    def appendToList(self):
        """[Add the new released shape to the fusion object]
        """
        try:
            #print("Append them to the list")
            if self.currentObj is None:
                return
            self.AllObjects.append(self.currentObj.Object)

        except Exception as err:
            App.Console.PrintError("'appendToList' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_SpecialTriangle(self, TriType):
        """[Draw Special type of Triangles]

        Args:
            TriType ([integer]): [Types]
        """
        try:
            pl = App.Placement()
            pl.Rotation.Q = (0.0, 0.0, 0, 1.0)
            pl.Base = self.planeVector
            if TriType == 1:
                points = [App.Vector(0.0, 0.0, 0.0), App.Vector(
                    0, self.brushSize, 0.0), App.Vector(self.brushSize, 0, 0.0)]
            elif TriType == 2:
                points = [App.Vector(0.0, 0.0, 0.0), App.Vector(
                    self.brushSize/4, self.brushSize/2, 0.0), App.Vector(self.brushSize, 0, 0.0)]
            first = _draft.makeWire(
                points, placement=pl, closed=True, face=True, support=None)
            _draft.autogroup(first)
            App.ActiveDocument.recompute()
            f = App.ActiveDocument.addObject('Part::Extrusion', 'Original')
            f.Base = first
            f.DirMode = "Normal"
            f.DirLink = None
            f.LengthFwd = -0.1
            f.LengthRev = 0.0
            f.Solid = True
            f.Reversed = False
            f.Symmetric = False
            f.TaperAngle = 0.0
            f.TaperAngleRev = 0.0

            f.Dir = first.Shape.normalAt(0, 0)  # Normal line
            if (f.Dir.x != 1 or f.Dir.y != 1 or f.Dir.z != 1):
                f.DirMode = "Custom"
            # Make a simple copy of the object
            App.ActiveDocument.recompute()
            newShape = _part.getShape(
                f, '', needSubElement=False, refine=True)
            s = App.ActiveDocument.addObject(
                'Part::Feature', 'SpecialTriangle')
            s.Shape = newShape
            App.ActiveDocument.recompute()
            # Remove old objects

            App.ActiveDocument.recompute()
            App.ActiveDocument.removeObject(f.Name)
            App.ActiveDocument.removeObject(first.Name)
            App.ActiveDocument.recompute()
            return(Gui.ActiveDocument.getObject(s.Name))
        except Exception as err:
            App.Console.PrintError("'draw_SpecialTriangle' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_Square(self, typeOfSquare):
        """[Draw different types of Square shapes]

        Args:
            typeOfSquare ([integer]): [Type of the square shape]
        """
        # Convert/ or get Gui object not App object
        try:
            s = App.ActiveDocument.addObject("Part::Box", "Square")
            # Square
            if(typeOfSquare == 1):
                s.Width = self.brushSize
                s.Length = self.brushSize
            # Rectangle
            elif (typeOfSquare == 2):
                s.Length = self.brushSize
                s.Width = self.brushSize*2
            elif (typeOfSquare == 3):
                s.Length = self.brushSize*2
                s.Width = self.brushSize
            s.Height = self.firstSize
            App.ActiveDocument.recompute()
            return(Gui.ActiveDocument.getObject(s.Name))

        except Exception as err:
            App.Console.PrintError("'draw_Square' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_equalParallelogram(self, typeOfParallelogram):
        """[Draw different types of equal-sided parallelogram]

        Args:
            typeOfParallelogram ([integer]): [type of the parallelogram]
        """
        try:
            pl = App.Placement()
            pl.Rotation.Q = (0.0, 0.0, 0, 1.0)
            pl.Base = self.planeVector
            points = None
            if typeOfParallelogram == 1:
                points = [App.Vector(0.0, 0.0, 0.0),
                          App.Vector(self.brushSize/2, self.brushSize, 0.0),
                          App.Vector(self.brushSize/2 +
                                     self.brushSize/2, self.brushSize, 0.0),
                          App.Vector(self.brushSize/2, 0.0, 0.0)]
            elif typeOfParallelogram == 2:
                points = [App.Vector(0.0, 0.0, 0.0),
                          App.Vector(0, self.brushSize, 0.0),
                          App.Vector(self.brushSize, self.brushSize +
                                     self.brushSize/2, 0.0),
                          App.Vector(self.brushSize, self.brushSize/2, 0.0)]

            first = _draft.makeWire(
                points, placement=pl, closed=True, face=True, support=None)
            _draft.autogroup(first)
            App.ActiveDocument.recompute()
            f = App.ActiveDocument.addObject('Part::Extrusion', 'Original')
            f.Base = first
            f.DirMode = "Normal"
            f.DirLink = None
            f.LengthFwd = -self.firstSize
            f.LengthRev = 0.0
            f.Solid = True
            f.Reversed = False
            f.Symmetric = False
            f.TaperAngle = 0.0
            f.TaperAngleRev = 0.0

            f.Dir = first.Shape.normalAt(0, 0)  # Normal line
            if (f.Dir.x != 1 or f.Dir.y != 1 or f.Dir.z != 1):
                f.DirMode = "Custom"
            # Make a simple copy of the object
            App.ActiveDocument.recompute()
            newShape = _part.getShape(
                f, '', needSubElement=False, refine=True)
            s = App.ActiveDocument.addObject(
                'Part::Feature', 'Parallelogram')
            s.Shape = newShape
            App.ActiveDocument.recompute()
            # Remove old objects

            App.ActiveDocument.recompute()
            App.ActiveDocument.removeObject(f.Name)
            App.ActiveDocument.removeObject(first.Name)
            App.ActiveDocument.recompute()
            return(Gui.ActiveDocument.getObject(s.Name))

        except Exception as err:
            App.Console.PrintError("'draw_SpecialTriangle' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_Parallelogram(self, typeOfParallelogram):
        """[Draw different parallelogram types (not equal side-sizes)]

        Args:
            typeOfParallelogram ([integer]): [type of the parallelogram]
        """
        try:
            pl = App.Placement()
            pl.Rotation.Q = (0.0, 0.0, 0, 1.0)
            pl.Base = self.planeVector
            points = None
            if typeOfParallelogram == 1:
                points = [App.Vector(0, self.brushSize*0.4, 0.0),
                          App.Vector(self.brushSize, self.brushSize*0.4, 0.0),
                          App.Vector(self.brushSize*0.4 +
                                     self.brushSize*0.2, 0, 0.0),
                          App.Vector(self.brushSize*0.4, 0.0, 0.0)]

            elif typeOfParallelogram == 2:
                points = [App.Vector(0, self.brushSize*3/4, 0.0),
                          App.Vector(self.brushSize*2/4,
                                     self.brushSize*4/4, 0.0),
                          App.Vector(self.brushSize*2/4, 0, 0.0),
                          App.Vector(self.brushSize, 0.0, 0.0)]
            first = _draft.makeWire(
                points, placement=pl, closed=True, face=True, support=None)
            _draft.autogroup(first)
            App.ActiveDocument.recompute()
            f = App.ActiveDocument.addObject('Part::Extrusion', 'Original')
            f.Base = first
            f.DirMode = "Normal"
            f.DirLink = None
            f.LengthFwd = -0.1
            f.LengthRev = 0.0
            f.Solid = True
            f.Reversed = False
            f.Symmetric = False
            f.TaperAngle = 0.0
            f.TaperAngleRev = 0.0

            f.Dir = first.Shape.normalAt(0, 0)  # Normal line
            if (f.Dir.x != 1 or f.Dir.y != 1 or f.Dir.z != 1):
                f.DirMode = "Custom"
            # Make a simple copy of the object
            App.ActiveDocument.recompute()
            newShape = _part.getShape(
                f, '', needSubElement=False, refine=True)
            s = App.ActiveDocument.addObject(
                'Part::Feature', 'Parallelogram')
            s.Shape = newShape
            App.ActiveDocument.recompute()
            # Remove old objects

            App.ActiveDocument.recompute()
            App.ActiveDocument.removeObject(f.Name)
            App.ActiveDocument.removeObject(first.Name)
            App.ActiveDocument.recompute()
            return(Gui.ActiveDocument.getObject(s.Name))

        except Exception as err:
            App.Console.PrintError("'draw_SpecialTriangle' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_polygon(self, Sides):
        """[Draw different types of polygon]

        Args:
            Sides ([integer]): [Number of sides]
        """
        try:
            # Convert/ or get Gui object not App object
            s = App.ActiveDocument.addObject("Part::Prism", "Polygon")
            s.Circumradius = self.brushSize
            s.Polygon = Sides
            s.Height = self.firstSize
            App.ActiveDocument.recompute()
            if (s is None):
                raise ValueError("s must be an object")
            return(Gui.ActiveDocument.getObject(s.Name))

        except Exception as err:
            App.Console.PrintError("'draw_polygon' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_Arrow(self, arrowType):
        """[Draw arrow-head different directions]

        Args:
            arrowType ([integer]): [arrow direction]
        """
        try:
            pl = App.Placement()
            pl.Rotation.Q = (0.0, 0.0, 0, 1.0)
            pl.Base = self.planeVector
            points = None
            if arrowType == 1:
                points = [App.Vector(0.0, self.brushSize, 0.0),
                          App.Vector(0.0, self.brushSize*2, 0.0),
                          App.Vector(self.brushSize*2, 0.0, 0.0),
                          App.Vector(0.0, -self.brushSize*2, 0.0),
                          App.Vector(0.0, -self.brushSize, 0.0),
                          App.Vector(self.brushSize, 0.0, 0.0),
                          App.Vector(0.0, self.brushSize, 0.0),
                          ]
            elif arrowType == 2:
                points = [App.Vector(0.0, self.brushSize, 0.0),
                          App.Vector(-self.brushSize, 0.0, 0.0),
                          App.Vector(0.0, -self.brushSize, 0.0),
                          App.Vector(0.0, -self.brushSize*2, 0.0),
                          App.Vector(-self.brushSize*2, 0.0, 0.0),
                          App.Vector(0.0, self.brushSize*2, 0.0),
                          App.Vector(0.0, self.brushSize, 0.0),
                          ]

            if arrowType == 3:
                points = [App.Vector(self.brushSize, 0.0, 0.0),
                          App.Vector(0.0, self.brushSize, 0.0),
                          App.Vector(0.0, self.brushSize, 0.0),
                          App.Vector(-self.brushSize, 0.0, 0.0),
                          App.Vector(-self.brushSize*2, 0.0,  0.0),
                          App.Vector(0.0, self.brushSize*2, 0.0),
                          App.Vector(self.brushSize*2, 0.0,  0.0),
                          App.Vector(self.brushSize, 0.0, 0.0)]
            elif arrowType == 4:
                points = [App.Vector(self.brushSize, 0.0, 0.0),
                          App.Vector(self.brushSize*2, 0.0, 0.0),
                          App.Vector(0.0, -self.brushSize*2, 0.0),
                          App.Vector(-self.brushSize*2, 0.0, 0.0),
                          App.Vector(-self.brushSize, 0.0, 0.0),
                          App.Vector(0.0, -self.brushSize, 0.0),
                          App.Vector(self.brushSize, 0.0, 0.0),
                          ]

            first = _draft.makeWire(
                points, placement=pl, closed=True, face=True, support=None)
            _draft.autogroup(first)
            App.ActiveDocument.recompute()
            f = App.ActiveDocument.addObject('Part::Extrusion', 'Original')
            f.Base = first
            f.DirMode = "Normal"
            f.DirLink = None
            f.LengthFwd = -self.firstSize
            f.LengthRev = 0.0
            f.Solid = True
            f.Reversed = False
            f.Symmetric = False
            f.TaperAngle = 0.0
            f.TaperAngleRev = 0.0

            f.Dir = first.Shape.normalAt(0, 0)  # Normal line
            if (f.Dir.x != 1 or f.Dir.y != 1 or f.Dir.z != 1):
                f.DirMode = "Custom"
            # Make a simple copy of the object
            App.ActiveDocument.recompute()
            newShape = _part.getShape(
                f, '', needSubElement=False, refine=True)
            s = App.ActiveDocument.addObject(
                'Part::Feature', 'Parallelogram')
            s.Shape = newShape
            App.ActiveDocument.recompute()
            # Remove old objects

            App.ActiveDocument.recompute()
            App.ActiveDocument.removeObject(f.Name)
            App.ActiveDocument.removeObject(first.Name)
            App.ActiveDocument.recompute()
            return(Gui.ActiveDocument.getObject(s.Name))

        except Exception as err:
            App.Console.PrintError("'draw_SpecialTriangle' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_Star(self, starType):
        try:
            first = App.ActiveDocument.addObject(
                "Part::FeaturePython", "Star")
            Design456_2Ddrawing.ViewProviderBox(first.ViewObject, "Star")
            Design456_2Ddrawing.Star(first)
            plc = App.Placement()
            first.Placement = plc

            if starType == 1:
                first.Corners = 8
            elif starType == 2:
                first.Corners = 10
            elif starType == 3:
                first.Corners = 12
            first.OuterRadius = self.brushSize
            first.InnerRadius = self.brushSize/2
            App.ActiveDocument.recompute()
            f = App.ActiveDocument.addObject('Part::Extrusion', 'Original')
            f.Base = App.ActiveDocument.getObject(first.Name)
            f.DirMode = "Normal"
            f.DirLink = None
            f.LengthFwd = self.firstSize
            f.LengthRev = 0.0
            f.Solid = True
            f.Reversed = False
            f.Symmetric = False
            f.TaperAngle = 0.0
            f.TaperAngleRev = 0.0

            f.Dir = first.Shape.normalAt(0, 0)  # Normal line
            if (f.Dir.x != 1 or f.Dir.y != 1 or f.Dir.z != 1):
                f.DirMode = "Custom"
            # Make a simple copy of the object
            App.ActiveDocument.recompute()
            newShape = _part.getShape(
                f, '', needSubElement=False, refine=True)
            s = App.ActiveDocument.addObject(
                'Part::Feature', 'Star')
            s.Shape = newShape
            App.ActiveDocument.recompute()
            # Remove old objects

            App.ActiveDocument.recompute()
            App.ActiveDocument.removeObject(f.Name)
            App.ActiveDocument.removeObject(first.Name)
            App.ActiveDocument.recompute()
            return(Gui.ActiveDocument.getObject(s.Name))

        except Exception as err:
            App.Console.PrintError("'draw_Star' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_MOON(self, MoonType):
        """[Draw Moon shapes - different directions]

        Args:
            MoonType ([integer]): [moon direction]
        """
        try:
            first = App.ActiveDocument.addObject("Part::Cylinder", "Circle")
            first.Radius = self.brushSize
            first.Height = self.firstSize
            second = App.ActiveDocument.addObject("Part::Cylinder", "Circle")
            second.Radius = self.brushSize
            second.Height = self.firstSize
            if(MoonType == 1):
                second.Placement.Base.y = second.Placement.Base.y+3
            if(MoonType == 2):
                second.Placement.Base.y = second.Placement.Base.y-3
            if(MoonType == 3):
                second.Placement.Base.x = second.Placement.Base.x+3
            if(MoonType == 4):
                second.Placement.Base.x = second.Placement.Base.x-3

            newObj = App.ActiveDocument.addObject("Part::Cut", "tempSubtract")
            newObj.Base = first
            newObj.Tool = second
            App.ActiveDocument.recompute()
            # simple copy
            newShape = _part.getShape(
                newObj, '', needSubElement=False, refine=True)
            s = App.ActiveDocument.addObject('Part::Feature', 'MOON')
            s.Shape = newShape
            App.ActiveDocument.removeObject(first.Name)
            App.ActiveDocument.removeObject(second.Name)
            App.ActiveDocument.removeObject(newObj.Name)
            App.ActiveDocument.recompute()
            return(Gui.ActiveDocument.getObject(s.Name))

        except Exception as err:
            App.Console.PrintError("'draw_MOON' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_Fillet(self, FilletType):
        try:
            pl = App.Placement()
            pl.Rotation.Q = (0.0, 0.0, 0, 1.0)
            pl.Base = self.planeVector
            first = App.ActiveDocument.addObject("Part::Box", "Box")
            first.Width = self.brushSize
            first.Length = self.brushSize
            first.Height = self.firstSize

            second = App.ActiveDocument.addObject("Part::Cylinder", "Circle")
            second.Radius = self.brushSize
            second.Height = self.firstSize

            newObj = App.ActiveDocument.addObject("Part::Cut", "cut")
            newObj.Base = first
            newObj.Tool = second
            newObj.Placement = pl
            if FilletType == 1:
                first.Placement = pl
                second.Placement = pl
                second.Placement.Base = App.Vector(
                    self.brushSize, self.brushSize, 0)
            elif FilletType == 2:
                first.Placement = pl
                second.Placement = pl
            elif FilletType == 3:
                first.Placement = pl
                second.Placement = pl
                second.Placement.Base.y = self.brushSize
            elif FilletType == 4:
                first.Placement = pl
                second.Placement = pl
                second.Placement.Base.x = self.brushSize
            App.ActiveDocument.recompute()
            newShape = _part.getShape(
                newObj, '', needSubElement=False, refine=True)
            s = App.ActiveDocument.addObject('Part::Feature', 'Fillet')
            s.Shape = newShape
            App.ActiveDocument.removeObject(first.Name)
            App.ActiveDocument.removeObject(second.Name)
            App.ActiveDocument.removeObject(newObj.Name)
            App.ActiveDocument.recompute()
            return(Gui.ActiveDocument.getObject(s.Name))

        except Exception as err:
            App.Console.PrintError("'Paint-Fillet' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def recreateObject(self):
        """[Recreates the object after a mouse-movement. 
        It will update the position. 
        Or the size/shape is changed and new shape needs to be drawn.]
        """
        try:
            if(self.currentObj is not None):
                App.ActiveDocument.removeObject(self.currentObj.Name)
                self.currentObj = None
            # Rounded shapes
            if self.brushType == FR_BRUSHES.FR_CIRCLE_BRUSH:
                self.currentObj = self.draw_circle()
            elif self.brushType == FR_BRUSHES.FR_SEMI_CIRCLE_BRUSH:
                self.currentObj = self.draw_Semi_circle()
            elif self.brushType == FR_BRUSHES.FR_QUARTER_CIRCLE_BRUSH:
                self.currentObj = self.draw_Quarter_circle()
            elif self.brushType == FR_BRUSHES.FR_OVAL1_BRUSH:
                self.currentObj = self.draw_Oval(1)
            elif self.brushType == FR_BRUSHES.FR_OVAL2_BRUSH:
                self.currentObj = self.draw_Oval(2)
            elif self.brushType == FR_BRUSHES.FR_EGG_BRUSH:
                self.currentObj = self.draw_Egg()

            # 3 Sides shapes
            elif self.brushType == FR_BRUSHES.FR_TRIANGLE_BRUSH:
                self.currentObj = self.draw_polygon(3)  # Triangle
            elif self.brushType == FR_BRUSHES.FR_RIGHT_TRIANGLE_BRUSH:
                self.currentObj = self.draw_SpecialTriangle(
                    1)  # Right-angle-Triangle
            elif self.brushType == FR_BRUSHES.FR_SCALENE_TRIANGLE_BRUSH:
                self.currentObj = self.draw_SpecialTriangle(
                    2)  # scalene-Triangle

            # 4 Sides shapes
            elif self.brushType == FR_BRUSHES.FR_SQUARE_BRUSH:
                self.currentObj = self.draw_Square(1)

            # Equal sides
            elif self.brushType == FR_BRUSHES.FR_EQUALSIDES_PARALLELOGRAM1_BRUSH:
                self.currentObj = self.draw_equalParallelogram(1)
            elif self.brushType == FR_BRUSHES.FR_EQUALSIDES_PARALLELOGRAM2_BRUSH:
                self.currentObj = self.draw_equalParallelogram(2)

            # 2X & 2Y equal sides
            elif self.brushType == FR_BRUSHES.FR_PARALLELOGRAM1_BRUSH:
                self.currentObj = self.draw_Parallelogram(1)
            elif self.brushType == FR_BRUSHES.FR_PARALLELOGRAM2_BRUSH:
                self.currentObj = self.draw_Parallelogram(2)

            elif self.brushType == FR_BRUSHES.FR_RECTANGLE1_BRUSH:
                self.currentObj = self.draw_Square(2)
            elif self.brushType == FR_BRUSHES.FR_RECTANGLE2_BRUSH:
                self.currentObj = self.draw_Square(3)

            elif self.brushType == FR_BRUSHES.FR_RHOMBUS_BRUSH:
                self.currentObj = self.draw_polygon(4)
            elif self.brushType == FR_BRUSHES.FR_PENTAGON_BRUSH:
                self.currentObj = self.draw_polygon(5)
            elif self.brushType == FR_BRUSHES.FR_HEXAGON_BRUSH:
                self.currentObj = self.draw_polygon(6)
            elif self.brushType == FR_BRUSHES.FR_HEPTAGON_BRUSH:
                self.currentObj = self.draw_polygon(7)
            elif self.brushType == FR_BRUSHES.FR_OCTAGON_BRUSH:
                self.currentObj = self.draw_polygon(8)
            elif self.brushType == FR_BRUSHES.FR_ENNEAGON_BRUSH:
                self.currentObj = self.draw_polygon(9)
            elif self.brushType == FR_BRUSHES.FR_DECAGON_BRUSH:
                self.currentObj = self.draw_polygon(10)

            elif self.brushType == FR_BRUSHES.FR_ARROW1_BRUSH:
                self.currentObj = self.draw_Arrow(1)
            elif self.brushType == FR_BRUSHES.FR_ARROW2_BRUSH:
                self.currentObj = self.draw_Arrow(2)
            elif self.brushType == FR_BRUSHES.FR_ARROW3_BRUSH:
                self.currentObj = self.draw_Arrow(3)
            elif self.brushType == FR_BRUSHES.FR_ARROW4_BRUSH:
                self.currentObj = self.draw_Arrow(4)

            elif self.brushType == FR_BRUSHES.FR_STAR1_BRUSH:
                self.currentObj = self.draw_Star(1)
            elif self.brushType == FR_BRUSHES.FR_STAR2_BRUSH:
                self.currentObj = self.draw_Star(2)
            elif self.brushType == FR_BRUSHES.FR_STAR3_BRUSH:
                self.currentObj = self.draw_Star(3)

            elif self.brushType == FR_BRUSHES.FR_MOON1_BRUSH:
                self.currentObj = self.draw_MOON(1)
            elif self.brushType == FR_BRUSHES.FR_MOON2_BRUSH:
                self.currentObj = self.draw_MOON(2)
            elif self.brushType == FR_BRUSHES.FR_MOON3_BRUSH:
                self.currentObj = self.draw_MOON(3)
            elif self.brushType == FR_BRUSHES.FR_MOON4_BRUSH:
                self.currentObj = self.draw_MOON(4)
            elif self.brushType == FR_BRUSHES.FR_FILLET1_BRUSH:
                self.currentObj = self.draw_Fillet(1)
            elif self.brushType == FR_BRUSHES.FR_FILLET2_BRUSH:
                self.currentObj = self.draw_Fillet(2)
            elif self.brushType == FR_BRUSHES.FR_FILLET3_BRUSH:
                self.currentObj = self.draw_Fillet(3)
            elif self.brushType == FR_BRUSHES.FR_FILLET4_BRUSH:
                self.currentObj = self.draw_Fillet(4)

            # Merge object creation.
            if (self.resultObj is None):
                if (len(self.AllObjects) > 1):
                    if(self.runOnce == False):
                        self.runOnce = True
                        self.resultObj = App.ActiveDocument.addObject(
                            "Part::MultiFuse", "Paint")
                        self.resultObj.Refine = True
                        self.resultObj.Shapes = self.AllObjects
            else:
                # Update the Merge object
                self.resultObj.Shapes = self.AllObjects

        except Exception as err:
            App.Console.PrintError("'recreateObject Paint Obj' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def KeyboardEvent(self, events):
        """[Key board events. Used to limit the movement axis and finalize the last drawing by pressing ESC key]

        Args:
            events ([COIN3D events]): [events type]
        """
        try:
            event = events.getEvent()
            eventState = event.getState()
            if (type(event) == coin.SoKeyboardEvent):
                key = event.getKey()
            if key == coin.SoKeyboardEvent.X and eventState == coin.SoButtonEvent.UP:
                self.MoveMentDirection = 'X'
            elif key == coin.SoKeyboardEvent.Y and eventState == coin.SoButtonEvent.UP:
                self.MoveMentDirection = 'Y'
            elif key == coin.SoKeyboardEvent.Z and eventState == coin.SoButtonEvent.UP:
                self.MoveMentDirection = 'Z'
            else:
                self.MoveMentDirection = 'A'  # All
            # TODO:This line causes a crash to FreeCAD .. don't know why :(
            # if key == coin.SoKeyboardEvent.ESCAPE and eventState == coin.SoButtonEvent.UP:
            #    self.hide()

        except Exception as err:
            App.Console.PrintError("'KeyboardEvent' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def MouseMovement_cb(self, events):
        """[Mouse movement callback. It will move the object
        and update the drawing's position depending on the mouse-position and the plane]

        Args:
            events ([Coin3D events]): [Type of the event]
        """
        try:
            self.workingPlane = App.DraftWorkingPlane
            self.planeVector = App.DraftWorkingPlane.position
            offset = self.workingPlane.offsetToPoint(App.Vector(0,0,0))
            
            #projectPoint(App.Vector(0, 0, 0))
            event = events.getEvent()
            pos = event.getPosition().getValue()
            tempPos = self.view.getPoint(pos[0], pos[1])
            position = App.Vector(tempPos[0], tempPos[1], tempPos[2])
            viewAxis = App.DraftWorkingPlane.getNormal()
            # Get plane rotation
            self.pl = App.DraftWorkingPlane.getPlacement()
            self.pl.Rotation.Q = App.DraftWorkingPlane.getRotation().Rotation.Q
            self.pl.Rotation.Axis =App.DraftWorkingPlane.axis
            self.pl.Rotation.Angle = App.DraftWorkingPlane.getRotation().Rotation.Angle

            if self.currentObj is not None:
                # Normalview - Top
                self.pl.Base = App.DraftWorkingPlane.projectPoint(position) #App.DraftWorkingPlane.position #self.currentObj.Object.Placement
                print(self.pl, "self.pl")
                print(self.pl.Rotation.Angle, "self.pl.Rotation.Angle")
                print(self.pl.Rotation, "self.pl.Rotation")
                #self.pl.Rotation.Axis = App.DraftWorkingPlane.getNormal()
                #self.currentObj.Object.Placement = self.pl

                # All direction when A or decide which direction
                if (self.MoveMentDirection == 'A'):
                    self.currentObj.Object.Placement.Base = position
                elif (self.MoveMentDirection == 'X'):
                    self.currentObj.Object.Placement.Base.x = position.x

                elif (self.MoveMentDirection == 'Y'):
                    self.currentObj.Object.Placement.Base.y = position.y
                elif (self.MoveMentDirection == 'Z'):
                    self.currentObj.Object.Placement.Base.z = position.z
                App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'MouseMovement_cb' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def FixPlacementIssue(self):
        """[Find center of the merged objects and make it as placement]
        """
        try:
            if(self.resultObj is None):
                return
            Average = App.Vector(0, 0, 0)
            for obj in self.AllObjects:
                objBase = obj.Placement.Base  # obj.Shape.CenterOfGravity
                if Average == App.Vector(0.0, 0.0, 0.0):
                    # First time we should accept it without division
                    Average = objBase
                Average = App.Vector((Average.x+objBase.x)/2,
                                     (Average.y+objBase.y)/2,
                                     (Average.z+objBase.z)/2)
            for obj in self.AllObjects:
                obj.Placement.Base = obj.Placement.Base.sub(Average)

            self.resultObj.Placement.Base = Average

        except Exception as err:
            App.Console.PrintError("'FixPlacementIssue' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def MouseClick_cb(self, events):
        """[Mouse Release callback. 
        It will place the object after last movement
        and merge the object to older objects]

        Args:
            events ([COIN3D events]): [events type]
        """
        try:
            event = events.getEvent()
            eventState = event.getState()
            getButton = event.getButton()
            angle = 0
            if eventState == coin.SoMouseButtonEvent.DOWN and getButton == coin.SoMouseButtonEvent.BUTTON1:
                self.appendToList()
                App.ActiveDocument.recompute()
                self.currentObj = None
                self.setSize()
                self.setType()
                self.recreateObject()
                App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'MouseClick_cb' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Activated(self):
        """[Design456_Paint tool activation function.]
        """
        self.c1 = None
        self.c2 = None
        s = Gui.Selection.getSelectionEx()
        if (len(s) > 1):
            # One object must be selected at least
            errMessage = "Select Only one face to use the tool"
            faced.errorDialog(errMessage)
            return
        elif len(s) == 1:
            self.SelectedObj = s[0]
            self.workingplane = App.DraftWorkingPlane
            self.workingplane.reset()
            f = self.SelectedObj.SubObjects[0]
            self.workingplane.alignToFace(f)
            Gui.Snapper.grid.on()
            Gui.Snapper.forceGridOff = False

        try:
            self.getMainWindow()
            self.view = Gui.ActiveDocument.activeView()
            self.setType()
            self.setSize()
            self.recreateObject()            # Initial
            if(self.currentObj is None):
                print("Why is this None?")
            App.ActiveDocument.recompute()

            # Start callbacks for mouse events.
            self.callbackMove = self.view.addEventCallbackPivy(
                coin.SoLocation2Event.getClassTypeId(), self.MouseMovement_cb)
            self.callbackClick = self.view.addEventCallbackPivy(
                coin.SoMouseButtonEvent.getClassTypeId(), self.MouseClick_cb)
            self.callbackKey = self.view.addEventCallbackPivy(
                coin.SoKeyboardEvent.getClassTypeId(), self.KeyboardEvent)

        except Exception as err:
            App.Console.PrintError("'PaintCommand' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def remove_callbacks(self):
        """[Remove COIN32D/Events callback]
        """
        self.view.removeEventCallbackPivy(
            coin.SoLocation2Event.getClassTypeId(), self.callbackMove)
        self.view.removeEventCallbackPivy(
            coin.SoMouseButtonEvent.getClassTypeId(), self.callbackClick)
        self.view.removeEventCallbackPivy(
            coin.SoKeyboardEvent.getClassTypeId(), self.callbackKey)
        self.view = None

    def __del__(self):
        """[Python destructor for the object. Otherwise next drawing might get wrong parameters]
        """
        App.DraftWorkingPlane.reset()
        Gui.Snapper.grid.off()
        Gui.Snapper.forceGridOff = True
        self.remove_callbacks()
        self.mw = None
        self.dialog = None
        self.tab = None
        self.smartInd = None
        self._mywin = None
        self.b1 = None
        self.PaintLBL = None
        self.pl = None
        self.AllObjects = []
        self.lstBrushSize = None
        self.lstBrushType = None
        self.currentObj = None
        self.view = None
        self.Observer = None
        self.continuePainting = True
        self.brushSize = 1
        self.brushType = 0
        self.resultObj = None
        self.runOnce = False

    def BrushTypeChanged_cb(self):
        """[Brush change callback - Activates when the selected-bursh is changed in the listobx]
        """
        try:
            if (self.currentObj is not None):
                App.ActiveDocument.removeObject(self.currentObj.Object.Name)
                self.currentObj = None
            self.setType()
            self.recreateObject()
            App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'TypeChanged_cb' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def BrushSizeChanged_cb(self):
        """[Brush size change - callback . Activates when the size of the brush is changed  in the listbox]
        """
        try:
            if (self.currentObj is not None):
                App.ActiveDocument.removeObject(self.currentObj.Object.Name)
                self.currentObj = None
            self.setSize()
            self.recreateObject()
            App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'SizeChanged_cb' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def getMainWindow(self):
        """[Create the tab for the tool]

        Returns:
            [QTtab]: [The tab created which should be added to the FreeCAD]
        """
        try:
            toplevel = QtGui.QApplication.topLevelWidgets()
            self.mw = None
            for i in toplevel:
                if i.metaObject().className() == "Gui::MainWindow":
                    self.mw = i
            if self.mw is None:
                raise Exception("No main window found")
            dw = self.mw.findChildren(QtGui.QDockWidget)
            for i in dw:
                if str(i.objectName()) == "Combo View":
                    self.tab = i.findChild(QtGui.QTabWidget)
                elif str(i.objectName()) == "Python Console":
                    self.tab = i.findChild(QtGui.QTabWidget)
            if self.tab is None:
                raise Exception("No tab widget found")

            self.dialog = QtGui.QDialog()
            oldsize = self.tab.count()
            self.tab.addTab(self.dialog, "Paint")
            self.tab.setCurrentWidget(self.dialog)
            self.dialog.resize(200, 450)
            self.dialog.setWindowTitle("Paint")
            self.formLayoutWidget = QtGui.QWidget(self.dialog)
            self.formLayoutWidget.setGeometry(QtCore.QRect(10, 80, 281, 67))
            self.formLayoutWidget.setObjectName("formLayoutWidget")

            la = QtGui.QVBoxLayout(self.dialog)
            e1 = QtGui.QLabel("Paint")
            commentFont = QtGui.QFont("Times", 12, True)
            e1.setFont(commentFont)

            self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
            self.formLayout.setContentsMargins(0, 0, 0, 0)
            self.formLayout.setObjectName("formLayout")
            self.lblPaint = QtGui.QLabel(self.formLayoutWidget)
            self.dialog.setObjectName("Paint")
            self.formLayout.setWidget(
                0, QtGui.QFormLayout.LabelRole, self.lblPaint)
            self.lstBrushType = QtGui.QListWidget(self.dialog)
            self.lstBrushType.setGeometry(10, 10, 50, 40)
            self.lstBrushType.setObjectName("lstBrushType")
            self.formLayout.setWidget(
                0, QtGui.QFormLayout.FieldRole, self.lstBrushType)
            self.lstBrushSize = QtGui.QListWidget(self.dialog)
            self.lstBrushSize.setGeometry(10, 55, 50, 20)

            self.lstBrushSize.setObjectName("lstBrushSize")
            self.formLayout.setWidget(
                1, QtGui.QFormLayout.FieldRole, self.lstBrushSize)
            self.lblBrushSize = QtGui.QLabel(self.formLayoutWidget)
            self.lblBrushSize.setObjectName("lblBrushSize")
            self.formLayout.setWidget(
                1, QtGui.QFormLayout.LabelRole, self.lblBrushSize)
            self.formLayoutWidget_2 = QtGui.QWidget(self.dialog)
            self.formLayoutWidget_2.setGeometry(QtCore.QRect(10, 160, 160, 80))
            self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
            self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget_2)
            self.formLayout_2.setContentsMargins(0, 0, 0, 0)
            self.formLayout_2.setObjectName("formLayout_2")
            self.radioAsIs = QtGui.QRadioButton(self.formLayoutWidget_2)
            self.radioAsIs.setObjectName("radioAsIs")
            self.formLayout_2.setWidget(
                0, QtGui.QFormLayout.FieldRole, self.radioAsIs)
            self.radioMerge = QtGui.QRadioButton(self.formLayoutWidget_2)
            self.radioMerge.setObjectName("radioMerge")
            self.formLayout_2.setWidget(
                1, QtGui.QFormLayout.FieldRole, self.radioMerge)
            self.PaintLBL = QtGui.QLabel(
                "Use X,Y,Z to limit the movements\nAnd A for free movement\nPaint Radius or side=7")

            la.addWidget(self.formLayoutWidget)
            la.addWidget(e1)
            la.addWidget(self.PaintLBL)
            self.okbox = QtGui.QDialogButtonBox(self.dialog)
            self.okbox.setOrientation(QtCore.Qt.Horizontal)
            self.okbox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
            la.addWidget(self.okbox)
            # Add All shape names to the combobox
            for nameOfObject in self.listOfDrawings:
                self.lstBrushType.addItem(nameOfObject)

            for i in range(1, 1000):
                self.lstBrushSize.addItem(str(i))
            self.lstBrushSize.setCurrentRow(6)
            self.lstBrushType.setCurrentRow(FR_BRUSHES.FR_CIRCLE_BRUSH)

            self.lstBrushSize.currentItemChanged.connect(
                self.BrushSizeChanged_cb)

            self.lstBrushType.currentItemChanged.connect(
                self.BrushTypeChanged_cb)

            _translate = QtCore.QCoreApplication.translate
            self.dialog.setWindowTitle(_translate("Paint", "Paint"))
            self.lblPaint.setText(_translate("Dialog", "Brush Type"))
            self.lstBrushType.setToolTip(_translate("Dialog", "Brush Type"))
            self.lstBrushSize.setToolTip(_translate("Dialog", "Brush Type"))
            self.lblBrushSize.setText(_translate("Dialog", "Brush Size"))
            self.radioAsIs.setText(_translate("Dialog", "As is"))
            self.radioMerge.setText(_translate("Dialog", "Merge"))

            QtCore.QMetaObject.connectSlotsByName(self.dialog)
            QtCore.QObject.connect(
                self.okbox, QtCore.SIGNAL("accepted()"), self.hide)
            return self.dialog

        except Exception as err:
            App.Console.PrintError("'Design456_Paint' getMainWindow-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def hide(self):
        """
        Hide the widgets. Remove also the tab.
        """
        try:
            self.FixPlacementIssue()
            if (self.currentObj is not None):
                App.ActiveDocument.removeObject(self.currentObj.Object.Name)
                self.currentObj = None
            self.dialog.hide()

            dw = self.mw.findChildren(QtGui.QDockWidget)
            newsize = self.tab.count()  # Todo : Should we do that?
            self.tab.removeTab(newsize-1)  # it ==0,1,2,3 ..etc
            del self.dialog
            App.ActiveDocument.recompute()
            self.__del__()  # Remove all Paint 3dCOIN widgets

        except Exception as err:
            App.Console.PrintError("'recreate Paint Obj' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Design456_Paint.svg',
                'MenuText': "Paint",
                'ToolTip': "Draw or Paint"}


Gui.addCommand('Design456_Paint', Design456_Paint())
