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
import math
from PySide.QtCore import QT_TRANSLATE_NOOP
from draftobjects.base import DraftObject
import Design456_Paint
import Design456_Hole
from draftutils.translate import translate  # for translation

__updated__ = '2022-01-19 20:46:12'

# Move an object to the location of the mouse click on another surface


# ***************************************************************************
# * Modified by: Mariwan Jalal    mariwan.jalal@gmail.com    04/03/2021     *
#                                                                           *
# *__title__   = "Macro_Make_Arc_3_points"                                  *
# *__author__  = "Mario52"                                                  *
# *__url__     = "https://www.freecadweb.org/index-fr.html"                  *
# *__version__ = "00.01"                                                    *
# *__date__    = "14/07/2016"                                               *
# ***************************************************************************


class Design456_Arc3Points:
    def Activated(self):
        try:
            App.ActiveDocument.openTransaction(
                translate("Design456", "Arc3points"))
            oneObject = False
            selected = Gui.Selection.getSelectionEx()
            selectedOne1 = Gui.Selection.getSelectionEx()[0]
            selectedOne2 = Gui.Selection.getSelectionEx()[0]
            selectedOne3 = Gui.Selection.getSelectionEx()[0]
            allSelected = []
            if ((len(selected) < 3 or len(selected) > 3) and (selectedOne1.HasSubObjects is False or selectedOne2.HasSubObjects is False or selectedOne3.HasSubObjects is False)):
                # Two object must be selected
                errMessage = "Select two or more objects to useArc3Points Tool"
                faced.errorDialog(errMessage)
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
            # Remove only if it != one object
            if oneObject is False:
                for n in selected:
                    App.ActiveDocument.removeObject(n.ObjectName)
            del allSelected[:]
            App.ActiveDocument.recompute()
            App.ActiveDocument.commitTransaction()  # undo

        except Exception as err:
            App.Console.PrintError("'Arc3Points' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Arc3Points.svg',
            'MenuText': 'Arc3Points',
                        'ToolTip':  'Arc 3Points'
        }


Gui.addCommand('Design456_Arc3Points', Design456_Arc3Points())


class Design456_MultiPointsToWire:
    def __init__(self, type):
        self.type = type

    def Activated(self):
        try:
            App.ActiveDocument.openTransaction(
                translate("Design456", "MultipointsToWire"))
            selected = Gui.Selection.getSelectionEx()

            if (len(selected) < 2):
                # Two object must be selected
                if (not selected[0].HasSubObjects):
                    errMessage = "Select two or more objects to use MultiPointsToLineOpen Tool"
                    faced.errorDialog(errMessage)
                    return

            allSelected = []
            for t in selected:
                if type(t) == list:
                    for tt in t:
                        allSelected.append(App.Vector(
                            tt.Shape.Vertexes[0].Point))
                else:
                    if t.HasSubObjects and hasattr(t.SubObjects[0], "Vertexes"):
                        for v in t.SubObjects:
                            allSelected.append(App.Vector(v.Point))
                    elif t.HasSubObjects and hasattr(t.SubObjects[0], "Surface"):
                        errMessage = "Only Vertexes are allowed. You selected a face"
                        faced.errorDialog(errMessage)
                        return
                    else:
                        allSelected.append(App.Vector(t.Object.Shape.Point))

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
            App.ActiveDocument.commitTransaction()  # undo

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
            'Pixmap': Design456Init.ICON_PATH + 'MultiPointsToWireClosed.svg',
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
            'Pixmap': Design456Init.ICON_PATH + 'MultiPointsToWireOpen.svg',
            'MenuText': 'Multi-Points To Wire Open',
                        'ToolTip':  'Multi-Points To Wire Open'
        }


Gui.addCommand('Design456_MultiPointsToWireOpen',
               Design456_MultiPointsToWireOpen())
Gui.addCommand('Design456_MultiPointsToWireClose',
               Design456_MultiPointsToWireClose())


# Trim all selected lines/vertices, and leave the object open
# Warning: This command destroys the 2D shape and will loose the face.

class Design456_2DTrim:
    def Activated(self):

        try:
            sel = Gui.Selection.getSelectionEx()
            if len(sel) < 1:
                # several selections - Error
                errMessage = "Select one or more edges to trim"
                faced.errorDialog(errMessage)
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
                objType = selectedObjectType(sel1)
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
                if closedShape is True:
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
                            WireOrEdgeMadeOfPoints.pop(index)

                        pnew2DObject1 = _draft.makeWire(
                            _all_points2, placement=None, closed=False, face=False, support=None)
                        pnew2DObject1.Label = 'Wire'
                        pnew2DObject1.Start = _all_points2[0]
                        pnew2DObject1.End = _all_points2[len(_all_points2)-1]

                    elif position1 == 0 and position2 != totalPoints-1:
                        # First Points, remove  'closed' and start = pos+1
                        print("in the beginning")
                        StartPoint = WireOrEdgeMadeOfPoints[position2]
                        WireOrEdgeMadeOfPoints.pop(position1)
                        EndPoint = WireOrEdgeMadeOfPoints[len(
                            WireOrEdgeMadeOfPoints)-1]
                        # don't add first point
                    elif position2 == totalPoints-1:
                        # point 2 is the last point in the shape
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
                faced.errorDialog(errMessage)
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
            'Pixmap': Design456Init.ICON_PATH + '2D_TrimLine.svg',
            'MenuText': 'Trim Line',
                        'ToolTip':  'Trim Line or edge in a 2D shape'
        }


Gui.addCommand('Design456_2DTrim', Design456_2DTrim())


def selectedObjectType(obj):
    if isinstance(obj.Object, _part.Shape):
        return "Shape"
    if hasattr(obj.Object, 'Proxy'):
        if hasattr(obj.Object.Proxy, "Type"):
            return obj.Object.Proxy.Type
    if hasattr(obj.Object, 'TypeId'):
        return obj.Object.TypeId
    return "Unknown"


class ViewProviderBox:

    obj_name = "Star"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderBox.obj_name
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
        return (Design456Init.ICON_PATH + 'Design456_Star.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

# ===========================================================================

# Create 2D Star


class Star:
    """
    Create a 2D Star based on the Inner radius outer radius, corners and the angle.
    """

    def __init__(self, obj, _InnerRadius=10, _OuterRadius=20, _Angle=2*math.pi, _Corners=40):
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
            if obj.OuterRadius < obj.InnerRadius:
                # you cannot have it smaller
                obj.OuterRadius = obj.InnerRadius
            self.points = []

            for i in range(0, obj.Corners):
                alpha = math.pi * (2 * i + 2 - obj.Corners % 2)/(obj.Corners)
                if i % 2 == 1:
                    radius = obj.InnerRadius
                else:
                    radius = obj.OuterRadius
                x = _math.cos(alpha) * radius
                y = _math.sin(alpha) * radius
                self.points.append(App.Vector(x, y, 0.0))
                if i == 0:
                    saveFirstPoint = App.Vector(x, y, 0.0)
                if alpha > obj.Angle:
                    break
            self.points.append(saveFirstPoint)
            test = _part.makePolygon(self.points)
            obj.Shape = _part.Face(test)
            if hasattr(obj, "Area") and hasattr(obj.Shape, "Area"):
                obj.Area = obj.Shape.Area
            return obj  # Allow getting the

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
            newObj = App.ActiveDocument.addObject(
                "Part::FeaturePython", "Star")
            ViewProviderBox(newObj.ViewObject, "Star")
            f = Star(newObj)
            plc = App.Placement()
            f.Placement = plc
            App.ActiveDocument.recompute()
            return newObj
        except Exception as err:
            App.Console.PrintError("'StarCommand' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Design456_Star.svg',
                'MenuText': "Star",
                'ToolTip': "Draw a Star"}


Gui.addCommand('Design456_Star', Design456_Star())


class Design456_joinTwoLines:
    """[Join two lines, edges or a series of edges to one edge
        This is useful when you want to simplify an edge or a line.
    ]
    """
    def Activated(self):
        import DraftGeomUtils
        try:
            s = Gui.Selection.getSelectionEx()
            if hasattr(s, "Point"):
                return
            e1 = None
            e2 = None
            if len(s) > 2:
                # Two objects must be selected
                errMessage = "Select only two vertices "
                faced.errorDialog(errMessage)
                return
            elif len(s) == 1:
                errMessage = "Not implemented "
                faced.errorDialog(errMessage)
                return
            elif len(s) == 2:
                s1 = s[0]
                s2 = s[1]                
                if ( 'Vertex' in str(s1.SubElementNames)):
                    # Vertexes are selected
                    p1 = s1.SubObjects[0].Vertexes[0].Point
                    p2 = s2.SubObjects[0].Vertexes[0].Point
                elif ( 'Edge' in str(s1.SubElementNames)):
                    # Edges are selected
                    # We have to find the nearest two vector. 
                    # Joining here means the two edges will 
                    # attach to each other while they are 
                    # separate.
                    vert1=[]
                    for e in s1.Object.Shape.OrderedEdges:
                        for v in e.Vertexes:
                            vert1.append(v.Point)
                    vert2 = []
                    for e in s2.Object.Shape.OrderedEdges:
                        for v in e.Vertexes:
                            vert2.append(v.Point)
                    # Now we need to find one point from each edge
                    # that are nearest to each other   
                    index1=DraftGeomUtils.findClosest(vert1[0],vert2)
                    index2=DraftGeomUtils.findClosest(vert1[len(vert1)-1],vert2)
                    dist1 = math.sqrt( pow((vert1[0].x-vert2[index1].x),2)+ 
                                  pow((vert1[0].y-vert2[index1].y),2)+
                                  pow((vert1[0].z-vert2[index1].z),2))
                    dist2 = math.sqrt( pow((vert1[len(vert1)-1].x-vert2[index2].x),2)+ 
                                  pow((vert1[len(vert1)-1].y-vert2[index2].y),2)+ 
                                  pow((vert1[len(vert1)-1].y-vert2[index2].z),2))
                    
                    if dist1 == dist2 or dist1 < dist2:
                        p1=vert1[0]
                        p2=vert2[index1]
                    elif dist2 < dist1:
                        p1=vert1[len(vert1)-1]
                        p2=vert2[index2]

                if hasattr(s1.Object.Shape, "OrderedEdges"):
                    Edges1 = s1.Object.Shape.OrderedEdges
                else:
                    Edges1 = s1.Object.Shape.Edges
                if hasattr(s2.Object.Shape, "OrderedEdges"):
                    Edges2 = s2.Object.Shape.OrderedEdges
                else:
                    Edges2 = s2.Object.Shape.Edges

                if len(Edges1) > 1:
                    for ed in Edges1:
                        for v in ed.Vertexes:
                            if v.Point == p1:
                                e1 = ed
                                Edges1.remove(e1)
                                break
                else:
                    e1 = Edges1[0]
                    Edges1 = []

            # We have the edges and the points
            if e1 is not None:
                if (e1.Vertexes[0].Point != p1):
                    p1 = e1.Vertexes[0].Point
                else:
                    p1 = e1.Vertexes[1].Point
            p1 = App.Vector(p1.x, p1.y, p1.z)
            p2 = App.Vector(p2.x, p2.y, p2.z)
            App.ActiveDocument.openTransaction(
                translate("Design456", "Join2Lines"))
            l1 = _draft.makeLine(p1, p2)
            App.ActiveDocument.recompute()
            newEdg = l1.Shape.Edges[0]
            if type(Edges1) == list and type(Edges2) == list:
                totalE = Edges1 + Edges2 + [newEdg]
            elif type(Edges1) == list and type(Edges2) != list:
                totalE = Edges1 + [Edges2]+[newEdg]
            elif type(Edges1) != list and type(Edges2) == list:
                # Only one edge in the first line, so not included
                totalE = Edges2 + [newEdg]
            else:
                # None of them is multiple edges. so only new edge should be use
                totalE = [Edges2]+[newEdg]

            newList = []
            for e in totalE:
                newList.append(e.copy())
            sortEdg = _part.sortEdges(newList)
            W = [_part.Wire(e) for e in sortEdg]
            for wire in W:
                newobj = App.ActiveDocument.addObject("Part::Feature", "Wire")
                newobj.Shape = wire
            App.ActiveDocument.removeObject(l1.Name)
            App.ActiveDocument.removeObject(s1.Object.Name)
            App.ActiveDocument.removeObject(s2.Object.Name)
            App.ActiveDocument.recompute()
            App.ActiveDocument.commitTransaction()  # undo reg.de here

        except Exception as err:
            App.Console.PrintError("'Part Surface' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Join two lines")
        return {'Pixmap':  Design456Init.ICON_PATH + 'Design456_JoinLines.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "joinTwoLines"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand('Design456_joinTwoLines', Design456_joinTwoLines())


class Design456_SimplifyEdges:
    """[Simplify a list of line, wire, or edges to one edge.
        This is useful if you want to repair a shape that has 
        multiple complex edges that not make sense.
    ]
    """
    def Activated(self):
        try:

            s = Gui.Selection.getSelectionEx()
            if len(s) > 1:
                # TODO: FIXME: Should we accept more than one object?
                errMessage = "Select edges from one object"
                faced.errorDialog(errMessage)
                return
            selObj = s[0]
            selEdges = selObj.Object.Shape.OrderedEdges
            selVertexes = []
            for e in selEdges:
                for v in e.Vertexes:
                    selVertexes.append(v.Point)

            # To eliminate multiple vertices
            # incide the same edge, we take only
            # first and last entities and then
            # we make a line and convert it to
            # an edge. which should replace the
            # old edge
            v1 = selVertexes[0]
            v2 = selVertexes[len(selVertexes)-1]
            l1 = _draft.makeLine(v1, v2)
            App.ActiveDocument.recompute()
            newobj = App.ActiveDocument.addObject("Part::Feature", "Wire")
            sh = l1.Shape
            newobj.Shape = sh.copy()
            App.ActiveDocument.recompute()
            App.ActiveDocument.removeObject(selObj.Object.Name)
            App.ActiveDocument.removeObject(l1.Name)

        except Exception as err:
            App.Console.PrintError("'Design456_SimplifyEdges' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Simplify Edges")
        return {'Pixmap':  Design456Init.ICON_PATH + 'SimplifyEdge.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "SimplifyEdges"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand('Design456_SimplifyEdges', Design456_SimplifyEdges())


class Design456_SimplifyFace:
    def Activated(self):
        try:

            s = Gui.Selection.getSelectionEx()
            if len(s) > 1:
                # TODO: FIXME: Should we accept more than one object?
                errMessage = "Select edges from one object"
                faced.errorDialog(errMessage)
                return
            sel = s[0]
            

        except Exception as err:
            App.Console.PrintError("'Design456_SimplifyEdges' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Simplify Edges")
        return {'Pixmap':  Design456Init.ICON_PATH + 'SimplifyFace.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "SimplifyFace"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand('Design456_SimplifyFace', Design456_SimplifyFace())


##################################################################################
#       Toolbar group definition
class Design456_2Ddrawing:
    list = ["Design456_Arc3Points",
            "Design456_MultiPointsToWireOpen",
            "Design456_MultiPointsToWireClose",
            "Design456_2DTrim",
            "Design456_joinTwoLines",
            "Design456_SimplifyEdges",
            "Design456_SimplifyFace",
            "Design456_Star",
            "Design456_Paint",
            "Design456_Hole",


            ]
    """Design456 Design456_2Ddrawing Toolbar"""

    def GetResources(self):
        return{
            'Pixmap':    Design456Init.ICON_PATH + '2D_Drawing.svg',
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
