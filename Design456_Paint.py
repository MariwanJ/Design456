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
import FACE_D as faced
import math as _math
from PySide.QtCore import QT_TRANSLATE_NOOP
from PySide import QtGui, QtCore
from ThreeDWidgets.constant import FR_BRUSHES
import math
from pivy import coin

# TODO: . FIXME:


class Design456_Paint:

    brushType: FR_BRUSHES = FR_BRUSHES.FR_SQUARE_BRUSH
    mw = None
    dialog = None  # Dialog for the tool
    tab = None  # Tabs
    smartInd = None  # ?
    _mywin = None                           #
    b1 = None                               #
    PaintLBL = None  # Label
    pl = App.Placement()
    pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)  # Initial position
    # Initial position - will be changed by the mouse
    pl.Base = App.Vector(0.0, 0.0, 0.0)
    AllObjects = []  # Merged shapes
    lstBrushSize = None  # GUI combobox -brush size
    lstBrushType = None  # GUI combobox -brush type
    # current created shape (circle, square, triangles,..etc)
    currentObj = None
    view = None  # used for captureing mouse events
    Observer = None  # Used for captureing mouse events
    continuePainting = True
    brushSize = 1  # Brush Size
    brushType = 0
    resultObj = None  # Extruded shape
    runOnce = False  # Create the merge object once only
    MoveMentDirection = 'A'
    firstSize = 0.1

    listOfDrawings = ["CIRCLE",
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
                      "EQUALSIDES_PARALLELOGRAM3",
                      "EQUALSIDES_PARALLELOGRAM4",
                      "RECTANGLE1",
                      "RECTANGLE2",
                      "PARALLELOGRAM1",
                      "PARALLELOGRAM2",
                      "PARALLELOGRAM3",
                      "PARALLELOGRAM4",
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
                      "MOON4"]

    def setSize(self):
        #text = self.lstBrushSize.currentItem().text()
        self.brushSize = self.lstBrushSize.currentRow()

    def setType(self):
        #text = self.lstBrushType.currentItem().text()
        self.brushType = self.lstBrushType.currentRow()

    def draw_circle(self):
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
        try:
            first = App.ActiveDocument.addObject("Part::Cylinder", "Circle")
            first.Radius = self.brushSize
            first.Height = self.firstSize
            second = App.ActiveDocument.addObject("Part::Box", "Circle")
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
        # Convert/ or get Gui object not App object
        try:
            pl = App.Placement()
            ellipse = None
            pl.Base = App.Vector(0, 0, 0.0)
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
                f, '', needSubElement=False, refine=False)
            s = App.ActiveDocument.addObject('Part::Feature', 'Oval')
            s.Shape = newShape
            App.ActiveDocument.recompute()
            # Remove old objects
            # App.ActiveDocument.clearUndos()
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
        try:
            print("Append them to the list")
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
        try:
            pl = App.Placement()
            pl.Rotation.Q = (0.0, 0.0, 0, 1.0)
            pl.Base = App.Vector(0, 0, 0.0)
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
                f, '', needSubElement=False, refine=False)
            s = App.ActiveDocument.addObject(
                'Part::Feature', 'SpecialTriangle')
            s.Shape = newShape
            App.ActiveDocument.recompute()
            # Remove old objects
            # App.ActiveDocument.clearUndos()
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
        try:
            pl = App.Placement()
            pl.Rotation.Q = (0.0, 0.0, 0, 1.0)
            pl.Base = App.Vector(0, 0, 0.0)
            points = None
            if typeOfParallelogram == 1:
                points = [App.Vector(0.0, 0.0, 0.0),
                          App.Vector(self.brushSize, self.brushSize, 0.0),
                          App.Vector(self.brushSize+self.brushSize,
                                     self.brushSize, 0.0),
                          App.Vector(self.brushSize, 0.0, 0.0)]
            elif typeOfParallelogram == 2:
                points = [App.Vector(0.0, 0.0, 0.0),
                          App.Vector(-self.brushSize, self.brushSize, 0.0),
                          App.Vector(-self.brushSize-self.brushSize,
                                     self.brushSize, 0.0),
                          App.Vector(-self.brushSize, 0.0, 0.0)]
            elif typeOfParallelogram == 3:
                points = [App.Vector(0.0, 0.0, 0.0),
                          App.Vector(self.brushSize, self.brushSize, 0.0),
                          App.Vector(self.brushSize+self.brushSize,
                                     self.brushSize, 0.0),
                          App.Vector(self.brushSize+self.brushSize/2, 0.0, 0.0)]
            elif typeOfParallelogram == 4:
                points = [App.Vector(0.0, 0.0, 0.0),
                          App.Vector(-self.brushSize, self.brushSize, 0.0),
                          App.Vector(-self.brushSize-self.brushSize,
                                     self.brushSize, 0.0),
                          App.Vector(-self.brushSize-self.brushSize/2, 0.0, 0.0)]

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
                f, '', needSubElement=False, refine=False)
            s = App.ActiveDocument.addObject(
                'Part::Feature', 'Parallelogram')
            s.Shape = newShape
            App.ActiveDocument.recompute()
            # Remove old objects
            # App.ActiveDocument.clearUndos()
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
            
    #TODO:FIXME:
    def draw_Parallelogram(self, typeOfParallelogram):
        try:
            pl = App.Placement()
            pl.Rotation.Q = (0.0, 0.0, 0, 1.0)
            pl.Base = App.Vector(0, 0, 0.0)
            points = None
            if typeOfParallelogram == 1:
                points = [App.Vector(0.0, 0.0, 0.0),
                          App.Vector(self.brushSize/2, self.brushSize, 0.0),
                          App.Vector(self.brushSize+self.brushSize,
                                     self.brushSize, 0.0),
                          App.Vector(self.brushSize/4, 0.0, 0.0)]
            elif typeOfParallelogram == 2:
                points = [App.Vector(0.0, 0.0, 0.0),
                          App.Vector(-self.brushSize*2, self.brushSize*2, 0.0),
                          App.Vector(-self.brushSize-self.brushSize,
                                     self.brushSize*2, 0.0),
                          App.Vector(-self.brushSize/4, 0.0, 0.0)]
            elif typeOfParallelogram == 3:
                points = [App.Vector(0.0, 0.0, 0.0),
                          App.Vector(self.brushSize, self.brushSize*4, 0.0),
                          App.Vector(self.brushSize+self.brushSize,
                                     self.brushSize*4, 0.0),
                          App.Vector(self.brushSize+self.brushSize/2, 0.0, 0.0)]
            elif typeOfParallelogram == 4:
                points = [App.Vector(0.0, 0.0, 0.0),
                          App.Vector(-self.brushSize, self.brushSize, 0.0),
                          App.Vector(-self.brushSize-self.brushSize,
                                     self.brushSize, 0.0),
                          App.Vector(-self.brushSize-self.brushSize/2, 0.0, 0.0)]

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
                f, '', needSubElement=False, refine=False)
            s = App.ActiveDocument.addObject(
                'Part::Feature', 'Parallelogram')
            s.Shape = newShape
            App.ActiveDocument.recompute()
            # Remove old objects
            # App.ActiveDocument.clearUndos()
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
        try:
            pass

        except Exception as err:
            App.Console.PrintError("'draw_MOON' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_Star(self, starType):
        try:
            pass

        except Exception as err:
            App.Console.PrintError("'draw_MOON' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def draw_MOON(self, MoonType):
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
                newObj, '', needSubElement=False, refine=False)
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

    def MouseMovement_cb(self, events):
        try:
            event = events.getEvent()
            pos = event.getPosition().getValue()
            tempPos = self.view.getPoint(pos[0], pos[1])
            position = App.Vector(tempPos[0], tempPos[1], tempPos[2])
            if self.currentObj is not None:
                if(self.currentObj.Object.Placement.Base.z == 0):
                    position.z = 0
                elif (self.currentObj.Object.Placement.Base.y == 0):
                    position.y = 0
                elif (self.currentObj.Object.Placement.Base.x == 0):
                    position.x = 0
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

    def MouseClick_cb(self, events):
        try:
            event = events.getEvent()
            eventState = event.getState()
            getButton = event.getButton()
            viewAxis = Gui.ActiveDocument.ActiveView.getViewDirection()
            angle = 0
            if eventState == coin.SoMouseButtonEvent.DOWN and getButton == coin.SoMouseButtonEvent.BUTTON1:
                print("Place callback!!")
                self.appendToList()
                App.ActiveDocument.recompute()

                if(self.currentObj is not None):
                    # Normal view - Top
                    if(viewAxis == App.Vector(0, 0, 1)):
                        self.pl.Base.z = 0.0
                        self.pl.Rotation(0.0, 0.0, 0.0, 1.0)
                    elif(viewAxis == App.Vector(0, 0, 1)):
                        self.pl.Base.z = 0.0
                        self.pl.Rotation = (1.0, 0.0, 0.0, 1.0)
                    # FrontSide
                    elif(viewAxis == App.Vector(0, 1, 0)):
                        self.pl.Base.y = 0
                        self.pl.Rotation = (0, 0, 0, -90)
                    elif (viewAxis == App.Vector(0, -1, 0)):
                        self.pl.Base.y = 0
                        self.pl.Rotation = (0, 0, 0, 90)
                    # RightSideView
                    elif(viewAxis == App.Vector(-1, 0, 0)):
                        self.pl.Base.x = 0
                        self.pl.Rotation = (0, -90, 0)
                    elif (viewAxis == App.Vector(1, 0, 0)):
                        self.pl.Base.x = 0
                        self.pl.Rotation = (0, 90, 0)
                    # self.pl=self.currentObj.Placement
                self.currentObj = None
                self.setSize()
                self.setType()
                self.recreateObject()

        except Exception as err:
            App.Console.PrintError("'MouseClick_cb' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def recreateObject(self):
        try:
            if(self.currentObj is not None):
                print("remove object - recreate object",
                      self.currentObj.Name)
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
            elif self.brushType == FR_BRUSHES.FR_EQUALSIDES_PARALLELOGRAM3_BRUSH:
                self.currentObj = self.draw_equalParallelogram(3)
            elif self.brushType == FR_BRUSHES.FR_EQUALSIDES_PARALLELOGRAM4_BRUSH:
                self.currentObj = self.draw_equalParallelogram(4)

            # 2X & 2Y equal sides
            elif self.brushType == FR_BRUSHES.FR_PARALLELOGRAM1_BRUSH:
                self.currentObj = self.draw_Parallelogram(1)
            elif self.brushType == FR_BRUSHES.FR_PARALLELOGRAM2_BRUSH:
                self.currentObj = self.draw_Parallelogram(2)
            elif self.brushType == FR_BRUSHES.FR_PARALLELOGRAM3_BRUSH:
                self.currentObj = self.draw_Parallelogram(3)
            elif self.brushType == FR_BRUSHES.FR_PARALLELOGRAM4_BRUSH:
                self.currentObj = self.draw_Parallelogram(4)

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
            if key == coin.SoKeyboardEvent.ESCAPE and eventState == coin.SoButtonEvent.UP:
                self.remove_callbacks()
            # self.hide()

        except Exception as err:
            App.Console.PrintError("'KeyboardEvent' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Activated(self):
        self.c1 = None
        self.c2 = None
        print(type(self.currentObj))
        try:
            self.getMainWindow()
            self.view = Gui.ActiveDocument.activeView()
            self.setType()
            self.setSize()
            self.recreateObject()            # Initial
            if(self.currentObj is None):
                print("what is that")
            App.ActiveDocument.recompute()
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
        self.view.removeEventCallbackPivy(
            coin.SoLocation2Event.getClassTypeId(), self.callbackMove)
        self.view.removeEventCallbackPivy(
            coin.SoMouseButtonEvent.getClassTypeId(), self.callbackClick)
        self.view.removeEventCallbackPivy(
            coin.SoKeyboardEvent.getClassTypeId(), self.callbackKey)
        self.view = None

    def __del__(self):
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
            self.PaintLBL = QtGui.QLabel("Paint Radius=")
            e1.setFont(commentFont)

            self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
            self.formLayout.setContentsMargins(0, 0, 0, 0)
            self.formLayout.setObjectName("formLayout")
            self.lblPaint = QtGui.QLabel(self.formLayoutWidget)
            self.dialog.setObjectName("Pint")
            self.formLayout.setWidget(
                0, QtGui.QFormLayout.LabelRole, self.lblPaint)
            self.lstBrushType = QtGui.QListWidget(self.dialog) 
            self.lstBrushType.setGeometry(10, 10, 100, 40)
            self.lstBrushType.setObjectName("lstBrushType")
            self.formLayout.setWidget(
                0, QtGui.QFormLayout.FieldRole, self.lstBrushType)
            self.lstBrushSize = QtGui.QListWidget(self.dialog)
            self.lstBrushSize.setGeometry(10, 110, 100, 20)

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
            # self.lstBrushSize.currentItem().text()anged.connect(self.BrushChanged_cb)
            self.lstBrushSize.currentItemChanged.connect(
                self.BrushSizeChanged_cb)
            # self.lstBrushType.currentItem().text()anged.connect(self.BrushChanged_cb)
            self.lstBrushType.currentItemChanged.connect(
                self.BrushTypeChanged_cb)

            _translate = QtCore.QCoreApplication.translate
            self.dialog.setWindowTitle(_translate("Pain", "Pint"))
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
            App.Console.PrintError("'Design456_Paint' getMainWindwo-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def hide(self):
        """
        Hide the widgets. Remove also the tab.
        """
        try:
            if (self.currentObj is not None):
                App.ActiveDocument.removeObject(self.currentObj.Object.Name)
                self.currentObj = None
            self.dialog.hide()
            del self.dialog
            dw = self.mw.findChildren(QtGui.QDockWidget)
            newsize = self.tab.count()  # Todo : Should we do that?
            self.tab.removeTab(newsize-1)  # it ==0,1,2,3 ..etc
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
