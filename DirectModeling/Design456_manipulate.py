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
from OCC.Core import ChFi2d
from OCC import Core
import FACE_D as faced

#   import Part
#   __s__=App.ActiveDocument.Compound.Shape.Faces
#   __s__=Part.Solid(Part.Shell(__s__))
#   __o__=App.ActiveDocument.addObject("Part::Feature","Compound_solid")
#   __o__.Label="Compound (Solid)"
#   __o__.Shape=__s__
#   del __s__, __o__
"""
    - For square, rectangle, multisided-wire shapes :draft.wire should do the job
    - For Circle  - Loft should do the job. 
    - For curvature shapes - should be treated as squre. 
    
    We need to distinguish between : Circle edge, and wire edges
    circle selectedEdge.Closed=true -->use this
    others are not closed.

"""


class Design456_ExtendEdge:
    """[Extend the edge's position to a new position. 
    This will affect the faces share the edge.

    ]
    """
    selectedObj = None
    selectedEdge = None     # Original vectors that will be changed by mouse.
    oldEdgeVertexes = None
    newEdge = None      # Keep new vectors for the moved old edge-vectors
    # facess needed to be recreated - resized
    # First time it is from the object, but later will be the created faces
    view = None  # used for captureing mouse events
    # Based on the sewShape from De-featuring WB,
    # but simplified- Thanks for the author
    MoveMentDirection = None
    _newFaces = []
    clickOccurrence = 0

    def setTolerance(self, sel):
        if len(sel) != 1:
            msg = "Select one object!\n"
            App.Console.PrintWarning(msg)
            return

        o = sel[0]
        if hasattr(o, 'Shape'):
            ns = o.Shape.copy()
            new_tol = 0.001
            ns.fixTolerance(new_tol)
            o.Object.ViewObject.Visibility = False
            sl = App.ActiveDocument.addObject("Part::Feature", "Solid")
            sl.Shape = ns
            sl.ShapeColor = o.Object.ViewObject.ShapeColor
            sl.Object.ViewObject.LineColor = o.Object.ViewObject.LineColor
            sl.Object.ViewObject.PointColor = o.Object.ViewObject.PointColor
            sl.Object.ViewObject.DiffuseColor = o.Object.ViewObject.DiffuseColor
            sl.Object.ViewObject.Transparency = o.Object.ViewObject.Transparency
            sl.Label = 'Solid'

    # Based on the sewShape from De-featuring WB,
    # but simplified- Thanks for the author

    def sewShape(self, sel):
        """[Fix issues might be in the created object]

        Args:
            sel ([3D Object]): [Final object that needs repair. 
                                Always new object creates as result of sew]
        """
        if len(sel) != 1:
            msg = "Select one object!\n"
            App.Console.PrintWarning(msg)
            return

        o = sel[0]
        if hasattr(o, 'Shape'):
            sh = o.Shape.copy()
            sh.sewShape()
            sl = App.ActiveDocument.addObject("Part::Feature", "Solid")
            sl.Shape = sh
            sl.ShapeColor = App.ActiveDocument.getObject(o.Name).ShapeColor
            sl.LineColor = App.ActiveDocument.getObject(o.Name).LineColor
            sl.PointColor = App.ActiveDocument.getObject(o.Name).PointColor
            sl.DiffuseColor = App.ActiveDocument.getObject(
                o.Name).DiffuseColor
            sl.Transparency = App.ActiveDocument.getObject(
                o.Name).Transparency
            App.ActiveDocument.removeObject(o.Name)
            App.ActiveDocument.recompute()

    # def findEdgeInFace(self, face, specialEdg):
    #     """[Find Edg in a face]

    #     Args:
    #         face ([Face Obj]): [Face has the specialEdg]
    #         specialEdg ([Edge Obj]): [An Edge to search for]

    #     Returns:
    #         [Boolean]: [True if the face found or False if not found ]
    #     """
    #     for edg in face.Edges:
    #         if specialEdg == edg:
    #             return True
    #     return False

    def ExtractTheEdge(self):
        """[Extract the edge for movement]
        """
        self.newEdge = App.ActiveDocument.addObject(
            "Part::Feature", "Edge")
        sh = self.selectedEdge.copy()
        self.newEdge.Shape = sh
        self.selectedEdge = self.newEdge  # TODO: SHOULD WE DO THAT: FIXME:
        App.ActiveDocument.recompute()

    # def findFacesWithSharedEdge(self, edg):
    #     """[Find out the faces have the same edge which will be dragged by the mouse]

    #     Args:
    #         edg ([Edge]): [Edge object shared between diffrent faces]
    #     """

    #     for face in self.selectedObj.Shape.Faces:
    #         if self.findEdgeInFace(edg):
    #             self.AffectedFaced.append(face)
    #     if len(self.AffectedFaced) == 0:
    #         errMessage = "Please select an edge which is part of other objects"
    #         faced.errorDialog(errMessage)
    #         return

    # def getVerticesFromFace(self, face):
    #     """
    #     [Get Vertices found in the corners of the remained faces]
    #     """
    #     # TODO: FIXME:
    #     vectors = []
    #     for vertex in face.Vertexes:
    #         vectors.append(vertex.Point)
    def FixSequenceOfVertices(self, inVertices):
        """[Sort the vertices to allow making face without problem]

        Args:
            inVertices ([list of vertices]): [description]
        """
        try:
            sortedV = []
            (AllX, AllY, AllZ) = faced.getSortedXYZFromVertices(inVertices)
            print(AllX, AllY, AllZ)
            print("AllX,AllY,AllZ")
            correctX = True
            correctY = True
            correctZ = True
            for i in range(0, len(inVertices)-2):
                correctX = correctX and (inVertices[i].x == inVertices[i+1].x)
                correctY = correctY and (inVertices[i].y == inVertices[i+1].y)
                correctZ = correctZ and (inVertices[i].z == inVertices[i+1].z)

            print(correctX, correctY, correctZ)
            print("-----------------------------")

            if correctX:
                for i in inVertices:
                    if (i.y == AllY[0] and i.z == AllZ[0]):  # lowest x,z
                        sortedV.append(i)
                        inVertices.remove(i)  # we don't need it anymore
                        del AllY[0]  # remove it
                        del AllZ[0]
                for i in inVertices:
                    if (i.y == AllY[0] and i.z == AllZ[len(AllZ)-1]):
                        sortedV.append(i)
                        inVertices.remove(i)  # we don't need it anymore
                        del AllY[0]  # remove it
                        del AllZ[len(AllZ)-1]
                for i in inVertices:
                    if (i.y == AllY[0] and i.z == AllZ[len(AllZ)-1]):
                        sortedV.append(i)
                        inVertices.remove(i)  # we don't need it anymore
                        del AllY[0]  # remove it
                        del AllZ[len(AllZ)-1]

            elif correctY:
                for i in inVertices:
                    if (i.x == AllX[0] and i.z == AllZ[0]):  # lowest x,z
                        sortedV.append(i)
                        inVertices.remove(i)  # we don't need it anymore
                        del AllX[0]  # remove it
                        del AllZ[0]
                for i in inVertices:
                    if (i.x == AllX[0] and i.z == AllZ[len(AllZ)-1]):
                        sortedV.append(i)
                        inVertices.remove(i)  # we don't need it anymore
                        del AllX[0]  # remove it
                        del AllZ[len(AllZ)-1]
                for i in inVertices:
                    if (i.x == AllX[0] and i.z == AllZ[len(AllZ)-1]):
                        sortedV.append(i)
                        inVertices.remove(i)  # we don't need it anymore
                        del AllX[0]  # remove it
                        del AllZ[len(AllZ)-1]

            elif correctZ:
                for i in inVertices:
                    if (i.x == AllX[0] and i.y == AllY[0]):  # lowest x,z
                        sortedV.append(i)
                        inVertices.remove(i)  # we don't need it anymore
                        del AllX[0]  # remove it
                        del AllY[0]
                for i in inVertices:
                    if (i.x == AllX[0] and i.y == AllY[len(AllY)-1]):
                        sortedV.append(i)
                        inVertices.remove(i)  # we don't need it anymore
                        del AllX[0]  # remove it
                        del AllY[len(AllY)-1]
                for i in inVertices:
                    if (i.x == AllX[0] and i.y == AllY[len(AllY)-1]):
                        sortedV.append(i)
                        inVertices.remove(i)  # we don't need it anymore
                        del AllX[0]  # remove it
                        del AllY[len(AllY)-1]
            for i in inVertices:
                sortedV.append(i)
            return sortedV  # results

        except Exception as err:
            App.Console.PrintError("'FixSequenceOfVertices' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def recreateObject(self):
        # FIXME:
        # Here we have two sides to recreate and then compound them.
        # We try to create a wire-closed to replace the sides we delete.
        # This will be way to complex .. with many bugs :(
        try:
            _vertices = []
            faces = None
            if self._newFaces == []:
                print("selectedObject")
                faces = self.selectedObj.Shape.Faces
            else:
                print("new faces ")
                faces = self._newFaces
            if faces == None:
                return #TODO CHECKME
            
            self._newFaces.clear()
            for i in range(0, len(faces)):
                _vertices.clear()
                # Change allways the edges vertices to moved one
                #for vertex in faces[i].OuterWire.OrderedVertexes:
                for vertex in faces[i].Vertexes:
                    if vertex.Point == self.oldEdgeVertexes[0].Point:
                        print("found 0")
                        _vertices.append(self.newEdge.Shape.Vertexes[0].Point)
                    elif vertex.Point == self.oldEdgeVertexes[1].Point:
                        print("found 1")
                        _vertices.append(self.newEdge.Shape.Vertexes[0].Point)
                    else:
                        _vertices.append(vertex.Point)
                # Now we have new vertices for one face .. create the face object
                
                print("before i _vertices", i, _vertices)
                _Newvertices = self.FixSequenceOfVertices(_vertices)
                #_Newvertices =_vertices
                print("i _vertices", i, _Newvertices)
                newPolygon = _part.makePolygon(_Newvertices, True)
                App.ActiveDocument.recompute()
                #newFace = _part.makeFilledFace(newPolygon.Edges)
                _part.show(newPolygon)

                #if newFace.isNull():
                #    raise RuntimeError('Failed to create face')

                #self._newFaces.append(newFace)
                print("self._newFaces", self._newFaces)

        except Exception as err:
            App.Console.PrintError("'recreateObject' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Activated(self):
        try:

            sel = Gui.Selection.getSelectionEx()
            if len(sel) > 2:
                errMessage = "Please select only one edge and try again"
                faced.errorDialog(errMessage)
                return
            self.clickOccurrence = 0
            self.MoveMentDirection = 'A'

            self.view = Gui.ActiveDocument.activeView()
            # The whole 3D object
            self.selectedObj = sel[0].Object
            self.selectedObj.Visibility = False

            self.selectedEdge = sel[0].SubObjects[0]
            if(hasattr (self.selectedEdge ,"Vertexes")):
                self.oldEdgeVertexes = self.selectedEdge.Vertexes
            else:
                self.oldEdgeVertexes = self.selectedEdge.Shape.Vertexes
            if not hasattr(self.selectedEdge, 'Edges'):
                raise Exception("Please select only one edge and try again")

            self.ExtractTheEdge()
            # Start callbacks for mouse events.
            self.callbackClick = self.view.addEventCallbackPivy(
                coin.SoMouseButtonEvent.getClassTypeId(), self.MouseClick_cb)
            # Start callbacks for mouse events.
            self.callbackMove = self.view.addEventCallbackPivy(
                coin.SoLocation2Event.getClassTypeId(), self.MouseMovement_cb)
            self.callbackKey = self.view.addEventCallbackPivy(
                coin.SoKeyboardEvent.getClassTypeId(), self.KeyboardEvent)

        except Exception as err:
            App.Console.PrintError("'MouseClick_cb' Failed. "
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
            event = events.getEvent()
            pos = event.getPosition().getValue()
            tempPos = self.view.getPoint(pos[0], pos[1])
            position = App.Vector(int(tempPos[0]), int(tempPos[1]), int(tempPos[2]))
            #viewAxis = Gui.ActiveDocument.ActiveView.getViewDirection()
            if position != self.newEdge.Placement.Base:
                self.oldEdgeVertexes = self.newEdge.Shape.Vertexes
                # All direction when A or decide which direction
                if (self.MoveMentDirection == 'A'):
                    self.newEdge.Placement.Base = position
                elif (self.MoveMentDirection == 'X'):
                    self.newEdge.Placement.Base.x = position.x
                elif (self.MoveMentDirection == 'Y'):
                    self.newEdge.Placement.Base.y = position.y
                elif (self.MoveMentDirection == 'Z'):
                    self.newEdge.Placement.Base.z = position.z
                self.recreateObject()


        except Exception as err:
            App.Console.PrintError("'MouseMovement_cb' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

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
                if self.clickOccurrence == 0:
                    self.clickOccurrence = 1
                    # Start callbacks for mouse events.
                    self.callbackMove = self.view.addEventCallbackPivy(
                        coin.SoLocation2Event.getClassTypeId(), self.MouseMovement_cb)
                    self.callbackKey = self.view.addEventCallbackPivy(
                        coin.SoKeyboardEvent.getClassTypeId(), self.KeyboardEvent)
                    return
                elif self.clickOccurrence == 1:
                    self.newEdge = None
                    self.remove_callbacks()
                    App.ActiveDocument.recompute()
                    
            App.ActiveDocument.removeObject(self.selectedObj.Name)
            #myShell = _part.makeShell(self._newFaces)
            #App.ActiveDocument.recompute()
            #_part.show(myShell)
            #mySolid = _part.makeSolid(myShell)
            #self.selectedObj = mySolid
            self.clickOccurrence = 0

        except Exception as err:
            App.Console.PrintError("'MouseClick_cb' Failed. "
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

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_ExtendEdge.svg',
            'MenuText': 'Edge Extender',
                        'ToolTip':  ' Design456 Edge Extender'
        }


Gui.addCommand('Design456_ExtendEdge', Design456_ExtendEdge())
#******************************************************************************************************