# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from PySide.QtCore import QT_TRANSLATE_NOOP
from draftobjects.base import DraftObject
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
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Draft as _draft
import Part as _part
import Design456Init
from pivy import coin
import FACE_D as faced
import math as _math
# Move an object to the location of the mouse click on another surface


class Design456_2Ddrawing:
    list = ["Design456_Arc3Points",
            "Design456_MultiPointsToWireOpen",
            "Design456_MultiPointsToWireClose",
            "Design456_2DTrim",
            "Design456_2DExtend",
            "Design456_Star"

            ]
    """Design456 Design456_2Ddrawing Toolbar"""

    def GetResources(self):
        return{
            'Pixmap':    Design456Init.ICON_PATH + '/2D_Drawing.svg',
            'MenuText': '2Ddrawing',
            'ToolTip':  '2Ddrawing'
        }

    def IsActive(self):
        if App.ActiveDocument is None:
            return False
        else:
            return True

    def Activated(self):
        self.appendToolbar("Design456_2Ddrawing", self.list)

# ***************************************************************************
# * Author : __title__   = "Macro_Make_Arc_3_points"                       *
# *__author__  = "Mario52"                                                 *
# *__url__     = "http://www.freecadweb.org/index-fr.html"                 *
# *__version__ = "00.01"                                                   *
# *__date__    = "14/07/2016"                                              *
#                                                                          *
# * Modfied by: Mariwan Jalal    mariwan.jalal@gmail.com    04/03/2021     *
# ***************************************************************************


class Design456_Arc3Points:
    def Activated(self):
        try:
            oneObject = False
            selected = Gui.Selection.getSelectionEx()
            selectedOne1 = Gui.Selection.getSelectionEx()[0]
            selectedOne2 = Gui.Selection.getSelectionEx()[0]
            selectedOne3 = Gui.Selection.getSelectionEx()[0]
            allSelected = []
            if ((len(selected) < 3 or len(selected) > 3) and (selectedOne1.HasSubObjects == False or selectedOne2.HasSubObjects == False or selectedOne3.HasSubObjects == False)):
                # Two object must be selected
                errMessage = "Select two or more objects to useArc3Points Tool"
                faced.getInfo(selected).errorDialog(errMessage)
                return
            if selectedOne1.HasSubObjects and len(selected) == 1:
                # We have only one object that we take vertices from
                oneObject = True
                subObjects = selected[0].SubObjects
                for n in subObjects:
                    allSelected.append(n.Point)
            elif len(selected) == 3:
                for t in selected:
                    allSelected.append(
                        t.Object.Shape.Vertexes[0].Placement.Base)
                    print(len(allSelected))
            else:
                oneObject = False
                print("A combination of objects")
                print("Not implemented")
                return
            C1 = _part.Arc(App.Vector(allSelected[0]), App.Vector(
                allSelected[1]), App.Vector(allSelected[2]))
            S1 = _part.Shape([C1])
            W = _part.Wire(S1.Edges)
            _part.show(W)
            App.ActiveDocument.recompute()
            App.ActiveDocument.ActiveObject.Label = "Arc_3_Points"
            # Remove only if it is not one object
            if oneObject == False:
                for n in selected:
                    App.ActiveDocument.removeObject(n.ObjectName)
            del allSelected[:]
            App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'Arc3Points' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Arc3Points.svg',
            'MenuText': 'Arc3Points',
                        'ToolTip':  'Arc 3Points'
        }


Gui.addCommand('Design456_Arc3Points', Design456_Arc3Points())


class Design456_MultiPointsToWire:
    def __init__(self, type):
        self.type = type

    def Activated(self):
        try:
            selected = Gui.Selection.getSelectionEx()
            oneObject = False

            for n in selected:
                if n.HasSubObjects == True:
                    oneObject = True
            if (len(selected) < 2):
                # Two object must be selected
                errMessage = "Select two or more objects to use MultiPointsToLineOpen Tool"
                faced.getInfo(selected).errorDialog(errMessage)
                return
            allSelected = []
            for t in selected:
                allSelected.append(t.PickedPoints[0])
            print(allSelected)
            if self.type == 0:
                Wire1 = _draft.makeWire(allSelected, closed=True)
            else:
                Wire1 = _draft.makeWire(allSelected, closed=False)
            """
            I have to find a way to avoid deleting Vertices if they are a part from another object.
            This is disabled at the moment.

            for n in selected:
                App.ActiveDocument.removeObject(n.Object.Name)
            """
            del allSelected[:]
            App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'MultiPointsToWire' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class Design456_MultiPointsToWireClose:
    def Activated(self):
        try:
            newObj = Design456_MultiPointsToWire(0)
            newObj.Activated()
        except Exception as err:
            App.Console.PrintError("'MultiPointsToWireClose' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/MultiPointsToWireClosed.svg',
            'MenuText': 'Multi-Points To Wire Closed',
                        'ToolTip':  'Multi-Points To Wire Closed'
        }


class Design456_MultiPointsToWireOpen:
    def Activated(self):
        try:
            newObj = Design456_MultiPointsToWire(1)
            newObj.Activated()

        except Exception as err:
            App.Console.PrintError("'MultiPointsToWireOpen' Failed. "
                                   "{err}\n".format(err=str(err)))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/MultiPointsToWireOpen.svg',
            'MenuText': 'Multi-Points To Wire Open',
                        'ToolTip':  'Multi-Points To Wire Open'
        }


Gui.addCommand('Design456_MultiPointsToWireOpen',
               Design456_MultiPointsToWireOpen())
Gui.addCommand('Design456_MultiPointsToWireClose',
               Design456_MultiPointsToWireClose())


# Trim all selected lines, vertices and leave the object open
# Warning: This command destroy the 2D shape and will loose the face.

class Design456_2DTrim:
    def Activated(self):

        try:
            sel = Gui.Selection.getSelectionEx()
            if len(sel) < 1:
                # several selections - Error
                errMessage = "Select one or more edges to trim"
                faced.getInfo(sel).errorDialog(errMessage)
                return
            SelectedPoints = []
            sel1 = sel[0]

            if sel1.HasSubObjects:
                # We have several objects that has subobject(Edges) that should be trimmed

                # Save position and angle
                _placement = sel1.Object.Placement
                _placement.Rotation.Q = sel1.Object.Placement.Rotation.Q
                currentObject = App.ActiveDocument.getObject(sel1.Object.Name)
                SelectedPoints.clear()  # points in the targeted line to be trimmed
                _edg = sel1.SubObjects[0]
                # TODO: trim only 2 points at the moment
                Vert = _edg.Vertexes

                # Save all points we have in the edge or line/wire which should be trimmed
                for n in Vert:
                    SelectedPoints.append(App.Vector(n.Point))

                WireOrEdgeMadeOfPoints = []
                # Bring all points from the object
                for item in sel1.Object.Shape.Vertexes:
                    WireOrEdgeMadeOfPoints.append(App.Vector(item.Point))
                totalPoints = len(WireOrEdgeMadeOfPoints)
                position1 = position2 = None
                count = 0
                # First find their locations

                for j in range(totalPoints):
                    if SelectedPoints[0] == WireOrEdgeMadeOfPoints[j]:
                        position1 = count
                    elif (SelectedPoints[1] == WireOrEdgeMadeOfPoints[j]):
                        position2 = count
                    count = count+1
                # Try to reconstruct the shape/wire
                TestTwoObjectCreate = False
                _all_points2 = []
                objType = faced.getInfo(sel1).selectedObjectType()
                closedShape = None
                EndPoint = StartPoint = None
                if (objType == 'Wire' or objType == 'Line'):
                    closedShape = sel1.Object.Closed
                elif objType == 'Unknown':
                    closedShape = False
                    return  # We don't know what the shape is
                elif objType == 'Arc':
                    App.ActiveDocument.removeObject(sel1.Object.Name)
                    return
                else:
                    closedShape = True
                if closedShape == True:
                    # We have a shape with closed lines
                    # Here we need to do 2 things, 1 remove closed, 2 rearrange start-end
                    scan1 = min(position1, position2)
                    scan2 = max(position1, position2)
                    sortAll = 0
                    Index = scan2
                    EndPoint = WireOrEdgeMadeOfPoints[scan1]
                    StartPoint = WireOrEdgeMadeOfPoints[scan2]
                    while(sortAll < totalPoints):
                        _all_points2.append(WireOrEdgeMadeOfPoints[Index])
                        Index = Index+1
                        if Index >= totalPoints:
                            Index = 0
                        sortAll = sortAll+1
                    WireOrEdgeMadeOfPoints.clear()
                    WireOrEdgeMadeOfPoints = _all_points2

                elif(abs(position2-position1) == 1):
                    # It must be a line and not closed
                    if position1 != 0 and position2 != totalPoints-1:
                        # In the middle of the array.
                        # Two objects must be created.
                        print("between first and last")
                        _all_points2.clear()
                        plusOrMinus = 0
                        scan1 = min(position1, position2)
                        scan2 = max(position1, position2)
                        SaveValue = None
                        index = 0
                        while (index <= scan1):
                            _all_points2.append(WireOrEdgeMadeOfPoints[index])
                            index = index+1
                        index = 0
                        StartPoint = WireOrEdgeMadeOfPoints[scan2]
                        EndPoint = WireOrEdgeMadeOfPoints[len(
                            WireOrEdgeMadeOfPoints)-1]

                        for index in range(0, scan2):
                            print(index)
                            WireOrEdgeMadeOfPoints.pop(index)

                        pnew2DObject1 = _draft.makeWire(
                            _all_points2, placement=None, closed=False, face=False, support=None)
                        pnew2DObject1.Label = 'Wire'
                        pnew2DObject1.Start = _all_points2[0]
                        pnew2DObject1.End = _all_points2[len(_all_points2)-1]

                    elif position1 == 0 and position2 != totalPoints-1:
                        # First Points, remove  'closed' and start = pos+1
                        print("in the begining")
                        StartPoint = WireOrEdgeMadeOfPoints[position2]
                        WireOrEdgeMadeOfPoints.pop(position1)
                        EndPoint = WireOrEdgeMadeOfPoints[len(
                            WireOrEdgeMadeOfPoints)-1]
                        # don't add first point
                    elif position2 == totalPoints-1:
                        # point 2 is the last point in the shape
                        print("at the end")
                        StartPoint = WireOrEdgeMadeOfPoints[0]
                        EndPoint = WireOrEdgeMadeOfPoints[position2-1]
                        WireOrEdgeMadeOfPoints.pop(position2-1)

                        # don't add last point

                pnew2DObject2 = _draft.makeWire(
                    WireOrEdgeMadeOfPoints, placement=None, closed=False, face=False, support=None)
                App.ActiveDocument.removeObject(sel1.ObjectName)
                App.ActiveDocument.recompute()
                pnew2DObject2.Label = 'Wire'

                pnew2DObject2.End = EndPoint
                pnew2DObject2.Start = StartPoint

                # If nothing left, remove the object
                if len(pnew2DObject2.Shape.Vertexes) == 0:
                    App.ActiveDocument.removeObject(pnew2DObject2.Label)
                App.ActiveDocument.recompute()

            else:
                # No Edges found
                errMessage = "Select one or more edges to trim"
                faced.getInfo(sel1).errorDialog(errMessage)
                return
        except Exception as err:
            App.Console.PrintError("'Trim 2D' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        import Design456Init
        return {
            'Pixmap': Design456Init.ICON_PATH + '/2D_TrimLine.svg',
            'MenuText': 'Trim Line',
                        'ToolTip':  'Trim Line or edge in a 2D shape'
        }


Gui.addCommand('Design456_2DTrim', Design456_2DTrim())


class Design456_2DExtend:
    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()

            if len(s) < 1:
                # several selections - Error
                errMessage = "Select a line or a point to extend."
                faced.getInfo(s).errorDialog(errMessage)
                return
            sel = s[0]
            _type = faced.getInfo(sel).selectedObjectType()
            if not (_type == 'Wire' or _type == 'Line'):
                print(_type)
                print("Wrong object selected")
                return  # Not supported yet.
                # TODO: Is it necessary to extend Arc, Square ..etc shapes? Don't know now
            # User decided where to extend the line.
            # Otherwise we extend the line only to the end of the line
            VertPoint = None
            if hasattr(sel.SubObjects[0], 'Point'):
                VertPoint = sel.SubObjects[0].Point
            elif hasattr(sel.SubObjects[0], 'Edges'):
                _point = sel.SubObjects[0].Vertexes[1].Point
                VertPoint = sel.SubObjects[0].Vertexes[1].Point  # last point
            newPoint = []
            _point = sel.Object.Points
            positionSave = 0

            for i in _point:
                newPoint.append(App.Vector(i))
                if VertPoint == i:
                    positionSave = newPoint.index(i)
            if VertPoint == newPoint[len(newPoint)-1]:
                # add last point and then moved
                newPoint.append(App.Vector(newPoint[len(newPoint)-1]))
                sel.Object.Points = newPoint
                sel.Object.End = VertPoint
            elif positionSave == 0:
                # add last point and then

                newPoint.insert(0, App.Vector(VertPoint))
                sel.Object.Points = newPoint
                sel.Object.Start = VertPoint
            _view = Gui.ActiveDocument.ActiveView

            faced.mousePointMove(sel, _view)
            del newPoint[:]

        except Exception as err:
            App.Console.PrintError("'Extend' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/2D_ExtendLine.svg',
            'MenuText': 'Extend Line',
                        'ToolTip':  'Extend Existing Line'
        }


Gui.addCommand('Design456_2DExtend', Design456_2DExtend())


class ViewProviderBox:

    obj_name = "Star"

    def __init__(self, obj, obj_name):
        self.obj_name = obj_name
        obj.Proxy = self

    def attach(self, obj):
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self, obj):
        return "As Is"

    def getDefaultDisplayMode(self):
        return "As Is"

    def setDisplayMode(self, mode):
        return "As Is"

    def onChanged(self, vobj, prop):
        pass

    def getIcon(self):
        # return str(App.getUserAppDataDir()) + 'Mod' + '/Pyramids-and-Polyhedrons/Resources/Icons/' + (self.obj_name).lower() + '.svg'
        return (Design456Init.ICON_PATH + '/Design456_Star.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

# ===========================================================================

"""
Create a 2D Star based on the Inner radius outer radius, corners and the angle.
"""
class Star:

    def __init__(self, obj, _InnerRadius=10, _OuterRadius=20, _Angle=2*_math.pi, _Corners=40):
        _tip = QT_TRANSLATE_NOOP("App::Property", "Star Angel")
        obj.addProperty("App::PropertyAngle", "Angle",
                        "Star", _tip).Angle = _Angle
        _tip = QT_TRANSLATE_NOOP("App::Property", "Inner Radius of the star")
        obj.addProperty("App::PropertyLength", "InnerRadius",
                        "Star", _tip).InnerRadius = _InnerRadius
        _tip = QT_TRANSLATE_NOOP("App::Property", "Outer Radius of the star")
        obj.addProperty("App::PropertyLength", "OuterRadius",
                        "Star", _tip).OuterRadius = _OuterRadius
        _tip = QT_TRANSLATE_NOOP("App::Property", "Corners of the star")
        obj.addProperty("App::PropertyInteger", "Corners",
                        "Star", _tip).Corners = _Corners
        _tip = QT_TRANSLATE_NOOP("App::Property", "Make Face")
        obj.addProperty("App::PropertyBool", "MakeFace",
                        "Star", _tip).MakeFace = True
        _tip = QT_TRANSLATE_NOOP("App::Property", "The area of this object")
        obj.addProperty("App::PropertyArea", "Area", "Star", _tip).Area
        obj.Proxy = self

    def execute(self, obj):
        try:
            if obj.OuterRadius< obj.InnerRadius  :
                #you cannot have it smaller 
                obj.OuterRadius=obj.InnerRadius
            _points = []

            for i in range(0, obj.Corners):
                alpha = _math.pi *(2 * i + 2 - obj.Corners % 2)/(obj.Corners) 
                if i % 2 == 1:
                    radius = obj.InnerRadius
                else:
                    radius = obj.OuterRadius
                y = _math.cos(alpha) * radius
                x = _math.sin(alpha) * radius
                _points.append(App.Vector(x, y, 0.0))
                if i==0: 
                    saveFirstPoint=App.Vector(x,y,0.0)
                if alpha>obj.Angle : 
                    break
            _points.append(saveFirstPoint)
            test = _part.makePolygon(_points)
            obj.Shape = _part.Face(test)
            if hasattr(obj, "Area") and hasattr(obj.Shape, "Area"):
                obj.Area = obj.Shape.Area
            

        except Exception as err:
            App.Console.PrintError("'Star' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return



class Design456_Star:
    def Activated(self):
        try:
            newObj = App.ActiveDocument.addObject("Part::FeaturePython", "Star")
            ViewProviderBox(newObj.ViewObject, "Star")
            newObj=Star(newObj)
            plc = App.Placement()
            newObj.Placement=plc
            newObj.Placement.Rotation.Axis=App.Vector(0,0,1)
            App.ActiveDocument.recompute()
                
        except Exception as err:
            App.Console.PrintError("'StarCommand' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return
            
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH+ '/Design456_Star.svg',
                'MenuText': "Star",
                'ToolTip': "Draw a Star"}


Gui.addCommand('Design456_Star', Design456_Star())
