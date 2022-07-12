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
import Draft 
import Part 
import Design456Init
from pivy import coin
import math
from PySide.QtCore import QT_TRANSLATE_NOOP
from PySide import QtGui, QtCore
from ThreeDWidgets.constant import FR_BRUSHES
import Design456_2Ddrawing
import FACE_D as faced
from Design456Pref import Design456pref_var

__updated__ = '2022-07-11 21:49:47'

class Design456_Paint:
    """[Paint different shapes on any direction and with a custom sizes.
        They are 3D shapes that are merged if they are intersecting each other.
        Select the correct plane for drawing before you click.
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
        self.resultObj = None  # Extruded shape1248
        
        self.runOnce = False  # Create the merge object once only
        self.MoveMentDirection = 'A'
        self.stepSize = 0.1
        self.firstSize = 0.1
        self.SelectedObj = None
        self.oldPosition = App.Vector(0, 0, 0)
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
                               "FILLET5",
                               "FILLET6",
                               "FILLET7",
                               "FILLET8",
                               "CHAMFER1",
                               "CHAMFER2",
                               "CHAMFER3",
                               "CHAMFER4"
                               
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
            newShape = Part.getShape(
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
            newShape = Part.getShape(
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
            
    def defineFirstPlacement(self):
        self.pl = App.DraftWorkingPlane.getPlacement()
        self.pl.Base = App.DraftWorkingPlane.projectPoint(self.oldPosition)

        
    def draw_Oval(self, Ovaltype):
        """[Draw Oval - Different types]

        Args:
            Ovaltype ([Integer]): [Type of the oval]
        """
        # Convert/ or get Gui object not App object
        try:
            pl = App.Placement()
            ellipse = None
            pl.Base = App.Vector(0, 0, 0)
            pl.Rotation.Axis = (0.0, 0.0, 1)
            if Ovaltype == 1:
                pl.Rotation.Angle = math.radians(90.0)
            else:
                pl.Rotation.Angle = 0.0
            ellipse = Draft.makeEllipse(
                self.brushSize, self.brushSize/2, placement=pl, face=True, support=None)
            Draft.autogroup(ellipse)
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
            newShape = Part.getShape(
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
            
            if TriType == 1:
                points = [App.Vector(0.0, 0.0, 0.0), App.Vector(
                    0, self.brushSize, 0.0), App.Vector(self.brushSize, 0, 0.0)]
            elif TriType == 2:
                points = [App.Vector(0.0, 0.0, 0.0), App.Vector(
                    self.brushSize/4, self.brushSize/2, 0.0), App.Vector(self.brushSize, 0, 0.0)]
            first = Draft.makeWire(
                points, placement=pl, closed=True, face=True, support=None)
            Draft.autogroup(first)
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
            newShape = Part.getShape(
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
            
            points = None
            if typeOfParallelogram == 1:
                points = [App.Vector(0.0, 0.0, 0.0),
                          App.Vector(self.brushSize/2, self.brushSize, 0.0),
                          App.Vector(self.brushSize, self.brushSize, 0.0),
                          App.Vector(self.brushSize/2, 0.0, 0.0)]
            elif typeOfParallelogram == 2:
                points = [App.Vector(0.0, 0.0, 0.0),
                          App.Vector(0, self.brushSize, 0.0),
                          App.Vector(self.brushSize, self.brushSize +
                                     self.brushSize/2, 0.0),
                          App.Vector(self.brushSize, self.brushSize/2, 0.0)]

            first = Draft.makeWire(
                points, placement=pl, closed=True, face=True, support=None)
            Draft.autogroup(first)
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
            newShape = Part.getShape(
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
            
            points = None
            if typeOfParallelogram == 1:
                points = [App.Vector(0, self.brushSize*0.4, 0.0),
                          App.Vector(self.brushSize, self.brushSize*0.4, 0.0),
                          App.Vector(self.brushSize*0.4 +
                                     self.brushSize*0.2, 0, 0.0),
                          App.Vector(self.brushSize*0.4, 0.0, 0.0)]

            elif typeOfParallelogram == 2:
                points = [App.Vector(self.brushSize*0.4, 0.0, 0.0),
                          App.Vector(self.brushSize*0.4 +self.brushSize*0.2, 0.0, 0.0),
                          App.Vector(self.brushSize, -self.brushSize*0.4, 0.0),
                            App.Vector(0, -self.brushSize*0.4, 0.0),]
            first = Draft.makeWire(
                points, placement=pl, closed=True, face=True, support=None)
            Draft.autogroup(first)
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
            newShape = Part.getShape(
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

            first = Draft.makeWire(
                points, placement=pl, closed=True, face=True, support=None)
            Draft.autogroup(first)
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
            newShape = Part.getShape(
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
            Design456_2Ddrawing.ViewProviderStar(first.ViewObject, "Star")
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
            newShape = Part.getShape(
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
            newShape = Part.getShape(
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

    def draw_Chamfer(self,chamferType):
        try:
            pl = App.Placement()
            V1=V2=V3=V4=V5=V6=V7=None
            if chamferType==1:
                V1=App.Vector(self.brushSize/2,self.brushSize*0.1,0)
                V2=App.Vector(self.brushSize/2,0,0)
                V3=App.Vector(0,0,0)
                V4=App.Vector(0,self.brushSize,0)
                V5=App.Vector(self.brushSize/2,self.brushSize,0)
                V6=App.Vector(self.brushSize/2,self.brushSize-0.1*self.brushSize,0)
                V7=App.Vector(self.brushSize*0.1,self.brushSize/2,0)
            elif chamferType==2:
                V1=App.Vector(-self.brushSize/2,self.brushSize*0.1,0)
                V2=App.Vector(-self.brushSize/2,0,0)
                V3=App.Vector(0,0,0)
                V4=App.Vector(0,self.brushSize,0)
                V5=App.Vector(-self.brushSize/2,self.brushSize,0)
                V6=App.Vector(-self.brushSize/2,self.brushSize-0.1*self.brushSize,0)
                V7=App.Vector(-self.brushSize*0.1,self.brushSize/2,0)
            
            elif chamferType==3:
                V1=App.Vector(self.brushSize*0.1,self.brushSize/2,0)
                V2=App.Vector(0,self.brushSize/2,0)
                V3=App.Vector(0,0,0)
                V4=App.Vector(self.brushSize,0,0)
                V5=App.Vector(self.brushSize,self.brushSize/2,0)
                V6=App.Vector(self.brushSize-0.1*self.brushSize,self.brushSize/2,0)
                V7=App.Vector(self.brushSize/2,self.brushSize*0.1,0)
                
            elif chamferType==4:
                V1=App.Vector(self.brushSize*0.1,-self.brushSize/2,0)
                V2=App.Vector(0,-self.brushSize/2,0)
                V3=App.Vector(0,0,0)
                V4=App.Vector(self.brushSize,0,0)
                V5=App.Vector(self.brushSize,-self.brushSize/2,0)
                V6=App.Vector(self.brushSize-0.1*self.brushSize,-self.brushSize/2,0)
                V7=App.Vector(self.brushSize/2,-self.brushSize*0.1,0)
            else:
                print("ERROR - INVALID OPTION")
                return
            E1= Part.makePolygon([V1,V2,V3,V4,V5,V6,V7,V1])
            W=Part.Wire([*E1.Edges])
            F=Part.Face(W)
            extrude=F.extrude(App.Vector(0,0,self.firstSize))
            s = App.ActiveDocument.addObject('Part::Feature', "Chamfer")
            s.Placement= pl 
            s.Shape=extrude
            App.ActiveDocument.recompute()
            return(Gui.ActiveDocument.getObject(s.Name))
        
        except Exception as err:
            App.Console.PrintError("'Paint-Chamfer' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
                 
    def draw_Fillet(self, FilletType):
        try: 
            pl = App.Placement()
            
            if (FilletType <=4):
                pl.Rotation.Q = (0.0, 0.0, 0, 1.0)
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
                newShape = Part.getShape(
                newObj, '', needSubElement=False, refine=True)
                s = App.ActiveDocument.addObject('Part::Feature', 'Fillet')
                s.Shape = newShape
                App.ActiveDocument.removeObject(first.Name)
                App.ActiveDocument.removeObject(second.Name)
                App.ActiveDocument.removeObject(newObj.Name)
            else:
                V1=V2=V3=V4=V5=V6=V7=None
                if FilletType==5:
                    V1=App.Vector(self.brushSize/2,self.brushSize*0.1,0)
                    V2=App.Vector(self.brushSize/2,0,0)
                    V3=App.Vector(0,0,0)
                    V4=App.Vector(0,self.brushSize,0)
                    V5=App.Vector(self.brushSize/2,self.brushSize,0)
                    V6=App.Vector(self.brushSize/2,self.brushSize-0.1*self.brushSize,0)
                    V7=App.Vector(self.brushSize*0.1,self.brushSize/2,0)
                elif FilletType==6:
                    V1=App.Vector(-self.brushSize/2,self.brushSize*0.1,0)
                    V2=App.Vector(-self.brushSize/2,0,0)
                    V3=App.Vector(0,0,0)
                    V4=App.Vector(0,self.brushSize,0)
                    V5=App.Vector(-self.brushSize/2,self.brushSize,0)
                    V6=App.Vector(-self.brushSize/2,self.brushSize-0.1*self.brushSize,0)
                    V7=App.Vector(-self.brushSize*0.1,self.brushSize/2,0)
                
                elif FilletType==7:
                    V1=App.Vector(self.brushSize*0.1,self.brushSize/2,0)
                    V2=App.Vector(0,self.brushSize/2,0)
                    V3=App.Vector(0,0,0)
                    V4=App.Vector(self.brushSize,0,0)
                    V5=App.Vector(self.brushSize,self.brushSize/2,0)
                    V6=App.Vector(self.brushSize-0.1*self.brushSize,self.brushSize/2,0)
                    V7=App.Vector(self.brushSize/2,self.brushSize*0.1,0)
                    
                elif FilletType==8:
                    V1=App.Vector(self.brushSize*0.1,-self.brushSize/2,0)
                    V2=App.Vector(0,-self.brushSize/2,0)
                    V3=App.Vector(0,0,0)
                    V4=App.Vector(self.brushSize,0,0)
                    V5=App.Vector(self.brushSize,-self.brushSize/2,0)
                    V6=App.Vector(self.brushSize-0.1*self.brushSize,-self.brushSize/2,0)
                    V7=App.Vector(self.brushSize/2,-self.brushSize*0.1,0)
                else:
                    print("ERROR - INVALID OPTION")
                    return
                E1= Part.makePolygon([V1,V2,V3,V4,V5,V6])
                arc=Part.Arc(V6,V7,V1).toShape()
                W=Part.Wire([*E1.Edges,*arc.Edges])
                F=Part.Face(W)
                extrude=F.extrude(App.Vector(0,0,self.firstSize))
                s = App.ActiveDocument.addObject('Part::Feature', "Fillet")
                s.Placement= pl 
                s.Shape=extrude

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
                App.ActiveDocument.removeObject(self.currentObj.Object.Name)
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
            elif self.brushType == FR_BRUSHES.FR_FILLET5_BRUSH:
                self.currentObj = self.draw_Fillet(5)
            elif self.brushType == FR_BRUSHES.FR_FILLET6_BRUSH:
                self.currentObj = self.draw_Fillet(6)
            elif self.brushType == FR_BRUSHES.FR_FILLET7_BRUSH:
                self.currentObj = self.draw_Fillet(7)
            elif self.brushType == FR_BRUSHES.FR_FILLET8_BRUSH:
                self.currentObj = self.draw_Fillet(8)
            elif self.brushType == FR_BRUSHES.FR_CHAMFER1_BRUSH:
                self.currentObj = self.draw_Chamfer(1)
            elif self.brushType == FR_BRUSHES.FR_CHAMFER2_BRUSH:
                self.currentObj = self.draw_Chamfer(2)
            elif self.brushType == FR_BRUSHES.FR_CHAMFER3_BRUSH:
                self.currentObj = self.draw_Chamfer(3)
            elif self.brushType == FR_BRUSHES.FR_CHAMFER4_BRUSH:
                self.currentObj = self.draw_Chamfer(4)
 
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
                
            #Placement on current plane 
            self.defineFirstPlacement() 
            self.currentObj.Object.Placement= self.pl

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
            
            self.stepSize = Design456pref_var.MouseStepSize
            event = events.getEvent()
            pos = event.getPosition().getValue()
            tempPos = self.view.getPoint(pos[0], pos[1])
            position = App.Vector(tempPos[0], tempPos[1], tempPos[2])
            self.pl = App.DraftWorkingPlane.getPlacement()
            self.pl.Base = App.DraftWorkingPlane.projectPoint(position)
            if self.currentObj is not None:
                # All direction when A or decide which direction
                if (self.MoveMentDirection == 'A'):
                    self.currentObj.Object.Placement.Base = self.pl.Base
                elif (self.MoveMentDirection == 'X'):
                    self.currentObj.Object.Placement.Base.x = self.pl.Base.x
                elif (self.MoveMentDirection == 'Y'):
                    self.currentObj.Object.Placement.Base.y = self.pl.Base.y
                elif (self.MoveMentDirection == 'Z'):
                    self.currentObj.Object.Placement.Base.z = self.pl.Base.z

                delta=self.currentObj.Object.Placement.Base.sub(self.oldPosition)
                resultVector = App.Vector(0, 0, 0)
                if abs(delta.x) > 0 and abs(delta.x) >= self.stepSize:
                    resultVector.x=self.stepSize*(int(delta.x/self.stepSize))
                if abs(delta.y) > 0 and abs(delta.y) >= self.stepSize:
                    resultVector.y=self.stepSize*(int(delta.y/self.stepSize))
                if abs(delta.z) > 0 and abs(delta.z) >= self.stepSize:
                    resultVector.z=self.stepSize*(int(delta.z/self.stepSize))   
                self.currentObj.Object.Placement.Base=self.oldPosition.add(resultVector)     
                self.oldPosition=self.currentObj.Object.Placement.Base
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
            self.getDialogWindow()
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
        if self.view is None:
            return
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
        self.stepSize=0.1

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

    def comboChanged(self, text):
        print("text=", text)
        self.stepSize= float(text.rstrip("m"))


    def getDialogWindow(self):
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
                "Use X,Y & Z Keys to limit the movements\nAnd A for free movement\nPaint Radius or side=7")

            self.combListExtrudeStep = QtGui.QComboBox(self.dialog)
            self.combListExtrudeStep.setGeometry(QtCore.QRect(20, 100, 240, 20))
            self.combListExtrudeStep.addItem("0.1mm")      #   0.1 mm
            self.combListExtrudeStep.addItem("0.5mm")      #   0.5 mm
            self.combListExtrudeStep.addItem("1.0mm")      #   1.0 mm
            self.combListExtrudeStep.addItem("2.0mm")      #   2.0 mm
            self.combListExtrudeStep.addItem("3.0mm")      #   3.0 mm
            self.combListExtrudeStep.addItem("4.0mm")      #   4.0 mm
            self.combListExtrudeStep.addItem("5.0mm")      #   5.0 mm
            self.combListExtrudeStep.addItem("6.0mm")      #   6.0 mm
            self.combListExtrudeStep.addItem("7.0mm")      #   7.0 mm
            self.combListExtrudeStep.addItem("8.0mm")      #   8.0 mm
            self.combListExtrudeStep.addItem("9.0mm")      #   9.0 mm
            self.combListExtrudeStep.addItem("10.0mm")     #  10.0 mm

            self.combListExtrudeStep.addItem("20.0mm")     #  20.0 mm
            self.combListExtrudeStep.addItem("30.0mm")     #  30.0 mm
            self.combListExtrudeStep.addItem("40.0mm")     #  40.0 mm
            self.combListExtrudeStep.addItem("50.0mm")     #  50.0 mm
            self.combListExtrudeStep.addItem("60.0mm")     #  60.0 mm
            self.combListExtrudeStep.addItem("70.0mm")     #  70.0 mm
            self.combListExtrudeStep.addItem("80.0mm")     #  80.0 mm
            self.combListExtrudeStep.addItem("90.0mm")     #  90.0 mm
            self.combListExtrudeStep.addItem("100.0mm")    # 100.0 mm


            self.combListExtrudeStep.activated[str].connect(self.comboChanged)
            
            la.addWidget(self.formLayoutWidget)
            la.addWidget(e1)
            la.addWidget(self.combListExtrudeStep)
            la.addWidget(self.PaintLBL)

            self.combListExtrudeStep.setCurrentIndex(2)

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
            App.Console.PrintError("'Design456_Paint' getDialogWindow-Failed. "
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
            faced.showFirstTab()
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
############################################################333

#TODO:FIXME : DOESN'T WORK -----------------------> Do we need this?????????????2022-07-11

import sys

from PySide.QtCore import Qt
from PySide import QtGui, QtCore
from PySide2 import QtWidgets

class Design456_FreeDraw:
    def __init__(self):
        self.frmMain=None
        
    def findInChildren(self,obj, searched):
        
        for child in obj.children():
            if isinstance(child, searched):
                return child
            else:
                res = self.findInChildren(child, searched)
                if res:
                    return res
        return None

    def Activated(self):
        view = self.findInChildren(Gui.getMainWindow(),QtWidgets.QGraphicsView)

        self.frmMain=Gui.getMainWindow()
        self.label = QtGui.QLabel
        canvas = QtGui.QPixmap(300,300)
        canvas.fill(QtGui.QColor("white"))
        self.label.setPixmap(canvas)
        view.scene().addWidget(self.label)
        self.last_x, self.last_y = None, None

    def mouseMoveEvent(self, e):
        if self.last_x is None: # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return # Ignore the first time.

        painter = QtGui.QPainter(self.label.pixmap())
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
    
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'freedraw.svg',
                'MenuText': "Freedraw",
                'ToolTip': "Draw  "}
        
Gui.addCommand('Design456_FreeDraw', Design456_FreeDraw())
