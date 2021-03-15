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
# * Author :Copyright 2021 Jaise James <jaisekjames at gmail dot com>      *
# * Modified and added to Desgin456 WB by                                  *
# *  Mariwan Jalal   mariwan.jalal@gmail.com                               *
# **************************************************************************
import Part
import math
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
import os,sys

def angleBetween(ve1, ve2):
    # Find angle between two vectors in degrees
    return math.degrees(ve1.getAngle(ve2))


def face_direction(face):
    # Find normal of face & center of mass
    yL = face.CenterOfMass
    uv = face.Surface.parameter(yL)
    nv = face.normalAt(uv[0], uv[1])
    direction = yL.sub(nv + yL)
    #print([direction, yL])
    return direction, yL


def transform_tool(tool, base_face, tool_face, point=App.Vector(0, 0, 0), angle=0.0):
    # Find normal of faces & center to align faces
    direction1, yL1 = face_direction(base_face)
    direction2, yL2 = face_direction(tool_face)

    # Find angle between faces, axis of rotation & center of axis
    rot_angle = angleBetween(direction1, direction2)
    rot_axis = direction1.cross(direction2)
    if rot_axis == App.Vector(0.0, 0.0, 0.0):
        rot_axis = App.Vector(0, 1, 0).cross(direction2)
    rot_center = yL2
    #print([rot_center, rot_axis, rot_angle])
    tool.rotate(rot_center, rot_axis, -rot_angle)
    tool.translate(-yL2 + yL1)
    #Part.show(tool, "tool")

    tool.rotate(yL1, direction1, angle)
    tool.translate(point)
    # Part.show(tool,"tool")
    return tool


def faceArray(tool, tool_face, base_faces, skip_edges, offset, align):
    tool_list = []
    for base_face in base_faces:
        skiplist = []
        # generate hashcode for skiped edges
        for skip_edge in skip_edges:
            skiplist.append(skip_edge.hashCode())
        # print(skiplist)

        make_face=None
        tool_copy=None
        offsetPoint=None
        wire_list = []
        
        # remove wires with skip edge specified based on hashcode
        for i, wire in enumerate(base_face.Wires):
            if i != 0:
                for edge in wire.Edges:
                    if edge.hashCode() in skiplist:
                        break
                if edge.hashCode() not in skiplist:
                    wire_list.append(wire)

        for wire in wire_list:
            tool_copy = tool.copy()
            make_face = Part.Face(wire)
            dir, point = face_direction(make_face)
            offsetPoint = point - base_face.CenterOfMass + dir * offset

            # Aligned, if align option specified
            if align:
                # Alignment Based on Largest edge of both faces
                size = 0.0
                for medge in make_face.Edges:
                    if medge.Length > size and issubclass(type(medge.Curve), (Part.Line)):
                        base_face_edge = medge
                        size = medge.Length
                # print(size)
                #Part.show(base_face_edge, "base_face_edge")
                base_vec = base_face_edge.valueAt(
                    base_face_edge.LastParameter) - base_face_edge.valueAt(base_face_edge.FirstParameter)

                size = 0.0
                for nedge in tool_face.Edges:
                    if nedge.Length > size and issubclass(type(nedge.Curve), (Part.Line)):
                        tool_face_edge = nedge
                        size = nedge.Length
                # print(size)
                #Part.show(tool_face_edge, "tool_face_edge")
                tool_vec = tool_face_edge.valueAt(
                    tool_face_edge.LastParameter) - tool_face_edge.valueAt(tool_face_edge.FirstParameter)

                #        # Alignment Based on boundbox (useful, if oriented boundbox available)
                #        base_vec = FreeCAD.Vector (make_face.BoundBox.XMax, make_face.BoundBox.YMax, make_face.BoundBox.ZMax)
                #              - FreeCAD.Vector (make_face.BoundBox.XMin, make_face.BoundBox.YMin, make_face.BoundBox.ZMin)
                #        tool_vec = FreeCAD.Vector (tool_face.BoundBox.XMax, tool_face.BoundBox.YMax, tool_face.BoundBox.ZMax)
                #                - FreeCAD.Vector (tool_face.BoundBox.XMin, tool_face.BoundBox.YMin, tool_face.BoundBox.ZMin)
                angle = angleBetween(base_vec, tool_vec)
                # print(angle)
                tool_tran = transform_tool(
                    tool_copy, base_face, tool_face, offsetPoint, angle)
            else:
                tool_tran = transform_tool(
                    tool_copy, base_face, tool_face, offsetPoint)
                #Part.show(tool_tran, "tool_tran")
            tool_list.append(tool_tran)
    return tool_list


class MakeFaceArray:
    def __init__(self, obj):
        '''"Add wall or Wall with radius bend" '''
        self.selobj=obj
        self.selobj = Gui.Selection.getSelectionEx()
        facelist = [(baseobj.Object, baseobj.SubElementNames)
                    for baseobj in self.selobj[1:]]

        obj.addProperty("App::PropertyDistance", "Offset",
                        "Parameters", "Offset for Array").Offset = 0.0
        obj.addProperty("App::PropertyLinkSub", "Base", "Parameters", "The base object that will be dupicated").Base = (
            self.selobj[0].Object, self.selobj[0].SubElementNames)
        obj.addProperty("App::PropertyLinkSubList", "Faces",
                        "Parameters", "Linked Faces").Faces = facelist
        obj.addProperty("App::PropertyLinkSubList", "SkipEdges",
                        "Parameters", "Skipped Linked Edges")
        obj.addProperty("App::PropertyBool", "Fuse", "Parameters",
                        "Specifies, if array should be fused").Fuse = False
        obj.addProperty("App::PropertyBool","Align","Parameters","Specifies, if Base Aligned to largest line edge").Align = False
        obj.Proxy = self

    def execute(self, fp):
        '''"Print a short message when doing a recomputation, this method is mandatory" '''
        try:
            face_array=None
            base = fp.Base[0].Shape
            base_face = base.getElement(fp.Base[1][0])
            linked_faces = [element[0].Shape.getElement(
                element[1][i]) for element in fp.Faces for i in range(len(element[1]))]
            if fp.SkipEdges:
                skip_edges = [element[0].Shape.getElement(
                    element[1][i]) for element in fp.SkipEdges for i in range(len(element[1]))]
            else:
                skip_edges = []

            face_array = faceArray(
                base, base_face, linked_faces, skip_edges, -fp.Offset.Value, fp.Align)

            # Fuses, if Fuse pption set to True
            if fp.Fuse:
                array = face_array[0].multiFuse(face_array[1:])
            else:
                array = Part.Compound(face_array)
            #Part.show(array, "array")

            fp.Shape = array
            Gui.ActiveDocument.getObject(fp.Base[0].Name).Visibility = False
        except Exception as err:
            App.Console.PrintError("'Part::Subtract' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class FaceArrayViewProvider:
    "A View provider that nests children objects under the created one"

    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj.Object

    def attach(self, obj):
        self.Object = obj.Object
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self, obj):
        modes = []
        return modes

    def setDisplayMode(self, mode):
        return mode

    def onChanged(self, vp, prop):
        return

    def __getstate__(self):
        #        return {'ObjectName' : self.Object.Name}
        return None

    def __setstate__(self, state):
        if state is not None:
            doc = App.ActiveDocument  # crap
            self.Object = doc.getObject(state['ObjectName'])

    def claimChildren(self):
        objs = []
        if hasattr(self.Object, "Base"):
            objs.append(self.Object.Base[0])
        return objs

#  def getIcon(self):
#    return os.path.join( iconPath , 'AddBase.svg')

# class FaceArrayCommandClass():
#  """Add Face based Array command"""
#
#  def GetResources(self):
#    return {'Pixmap'  : os.path.join( iconPath , 'AddBase.svg'), # the name of a svg file available in the resources
#            'MenuText': QtCore.QT_TRANSLATE_NOOP('Draft','Make Face Array'),
#            'ToolTip' : QtCore.QT_TRANSLATE_NOOP('Draft','Create Face/s based Array')}
#
#  def Activated(self):
#    doc = FreeCAD.ActiveDocument
#    doc.openTransaction("FaceArray")
#    a = doc.addObject("Part::FeaturePython","FaceArray")
#    MakeFaceArray(a)
#    FaceArrayViewProvider(a.ViewObject)
#    doc.recompute()
#    doc.commitTransaction()
#    return
#
#  def IsActive(self):
#    if len(Gui.Selection.getSelection()) < 2 :
#      return False
#    for selFace in Gui.Selection.getSelectionEx()[0].SubObjects:
#      if type(selFace) != Part.Face :
#        return False
#    return True
#
# Gui.addCommand('FaceArray',FaceArrayCommandClass())


class Design456_MakeFaceArray():
    def Activated(self):
        array = App.ActiveDocument.addObject(
            "Part::FeaturePython", "FaceArray")
        MakeFaceArray(array)
        FaceArrayViewProvider(array.ViewObject)
        App.ActiveDocument.recompute()

    def GetResources(self):
        return{
            'Pixmap':   Design456Init.ICON_PATH + '/MakeFaceArray.svg',
            'MenuText': 'Make Face Array',
            'ToolTip': 'Make Face Array'
        }


Gui.addCommand('Design456_MakeFaceArray', Design456_MakeFaceArray())