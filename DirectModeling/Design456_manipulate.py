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
import Design456Init
from pivy import coin
import ThreeDWidgets.fr_coinwindow as win
from ThreeDWidgets import fr_coin3d
from typing import List
from PySide import QtGui, QtCore
from PySide.QtCore import QT_TRANSLATE_NOOP
from ThreeDWidgets.fr_degreewheel_widget import Fr_DegreeWheel_Widget
from ThreeDWidgets.fr_draw import draw_FaceSet
from ThreeDWidgets import fr_degreewheel_widget
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from draftutils.translate import translate  # for translate
import Part as _part
import FACE_D as faced
import math

from OCC import Core
from OCC.Core import ChFi2d


# #   import Part
# #   __s__=App.ActiveDocument.Compound.Shape.Faces
# #   __s__=Part.Solid(Part.Shell(__s__))
# #   __o__=App.ActiveDocument.addObject("Part::Feature","Compound_solid")
# #   __o__.Label="Compound (Solid)"
# #   __o__.Shape=__s__
# #   del __s__, __o__
# """
#     - For square, rectangle, multisided-wire shapes :draft.wire should do the job
#     - For Circle  - Loft should do the job.
#     - For curvature shapes - should be treated as squre.

#     We need to distinguish between : Circle edge, and wire edges
#     circle selectedEdge.Closed=true -->use this
#     others are not closed.

# """

class Design456_ExtendEdge:
    """[Extend the edge's position to a new position.
     This will affect the faces share the edge.    ]
     """
    _Vector = App.Vector(0.0, 0.0, 0.0)  # WHEEL POSITION
    mw = None
    dialog = None
    tab = None
    wheelObj = None
    editing = False
    w_rotation = [0.0, 0.0, 0.0, 0.0]  # Center/Wheel rotation
    _mywin = None
    b1 = None
    ExtrudeLBL = None
    RotateLBL = None
    run_Once = False
    endVector = None
    startVector = None
    savedVertices = [[]]
    counter = 0

    setupRotation = [0, 0, 0, 0]

    tweakLength = 0
    oldTweakLength = 0
    isItRotation = False
    newObject = None
    selectedObj = None
    # Original vectors that will be changed by mouse.
    selectedEdge = None
    oldEdgeVertexes = None
    newEdgeVertexes = None
    newEdge = None      # Keep new vectors for the moved old edge-vectors

    view = None  # used for captureing mouse events
    MoveMentDirection = None
    newFaces = []
    faceDir = None
    FirstLocation = None
    coinFaces = coin.SoSeparator()
    # facess needed to be recreated - resized
    # First time it is from the object, but later will be the created faces

    # Based on the sewShape from De-featuring WB,
    # but simplified- Thanks for the author
    def recomputeAll(self):
        self.counter = self.counter + 1
        print(self.counter)
        App.ActiveDocument.recompute()

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

    def ExtractTheEdge(self):
        """[Extract the edge for movement]
        """
        self.newEdge = App.ActiveDocument.addObject(
            "Part::Feature", "Edge")
        sh = self.selectedEdge.copy()
        self.newEdge.Shape = sh
        # self.selectedEdge = self.newEdge  # TODO: SHOULD WE DO THAT: FIXME:
        # App.ActiveDocument.recompute()

    def FixSequenceOfVertices(self, inVertices):
        """[Sort the vertices to allow making face without problem]

        Args:
            inVertices ([list of vertices]): [description]
        """
        try:
            sortedV = []
            (AllX, AllY, AllZ) = faced.getSortedXYZFromVertices(inVertices)
            correctX = True
            correctY = True
            correctZ = True
            for i in range(0, len(inVertices)-2):
                correctX = correctX and (
                    inVertices[i].x == inVertices[i+1].x)
                correctY = correctY and (
                    inVertices[i].y == inVertices[i+1].y)
                correctZ = correctZ and (
                    inVertices[i].z == inVertices[i+1].z)

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

    def COIN_recreateObject(self):
        for i in range(0, len(self.savedVertices)):
            for j in range(0, len(self.savedVertices[i])):
                if self.savedVertices[i][j].Point == self.oldEdgeVertexes[0].Point:
                    self.savedVertices[i][j] = self.newEdgeVertexes[0]
                elif self.savedVertices[i][j].Point == self.oldEdgeVertexes[1].Point:
                    self.savedVertices[i][j] = self.newEdgeVertexes[1]

        # We have the new vertices
        self.coinFaces.removeAllChildren()
        for i in self.savedVertices:
            a = []
            for j in i:
                a.append(j.Point)
            self.coinFaces.addChild(draw_FaceSet(
                a, [len(a), ], FR_COLOR.FR_LIGHTGRAY))

    def recreateObject(self):
        # FIXME:
        # Here we have two sides to recreate and then compound them.
        # We try to create a wire-closed to replace the sides we delete.
        # This will be way to complex . with many bugs :(
        try:

            _result = []
            for faceVert in self.savedVertices:
                convert = []
                for vert in faceVert:
                    convert.append(vert.Point)
                _Newvertices = convert
                newPolygon = _part.makePolygon(_Newvertices, True)
                convert.clear()
                newFace = _part.makeFilledFace(newPolygon.Edges)
                if newFace.isNull():
                    raise RuntimeError('Failed to create face')
                nFace = App.ActiveDocument.addObject("Part::Feature", "nFace")
                nFace.Shape = newFace
                self.newFaces.append(nFace)
                _result.append(nFace)
            self.newFaces.clear()
            self.newFaces = _result

        except Exception as err:
            App.Console.PrintError("'recreate Object' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def calculateNewVector(self):
        try:
            self.faceDir = faced.getDirectionAxis()  # face direction
            faces = faced.findFaceSHavingTheSameEdge()
            # TODO: SHOULD WE DO ANY CALCULATION TO FIND BETTER FACE?
            if type(faces) == list:
                face = faces[0]
            elif faces is not None:
                face = faces
            else:
                raise ValueError("Face returned was none")

            yL = face.CenterOfMass
            uv = face.Surface.parameter(yL)
            nv = face.normalAt(uv[0], uv[1])
            self.normalVector = nv
            # Setup calculation.
            if (face.Surface.Rotation is None):
                calAn = math.degrees(nv.getAngle(App.Vector(1, 1, 0)))
                rotation = [0, 1, 0, calAn]
            else:
                rotation = [face.Surface.Rotation.Axis.x,
                            face.Surface.Rotation.Axis.y,
                            face.Surface.Rotation.Axis.z,
                            math.degrees(face.Surface.Rotation.Angle)]

            d = self.tweakLength

            self.FirstLocation = yL + d * nv  # the wheel
            return rotation

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Calculate new Vector. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def saveVertices(self):
        # Save the vertices for the faces.
        try:
            if len(self.savedVertices) > 0:
                del self.savedVertices[len(self.savedVertices)-1]
            for face in self.selectedObj.Shape.Faces:
                newPoint = []
                for v in face.OuterWire.OrderedVertexes:
                    newPoint.append(v)
                self.savedVertices.append(newPoint)
            print(self.savedVertices)
            for i in self.savedVertices:
                for j in i: 
                    print (j.Point)
                print("..........")
        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'saveVertices' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Activated(self):
        """[ Executes when the tool is used   ]
        """
        try:
            sel = Gui.Selection.getSelectionEx()

            if len(sel) > 2:
                errMessage = "Please select only one edge and try again"
                faced.errorDialog(errMessage)
                return

            self.MoveMentDirection = 'A'
            self.selectedObj = sel[0].Object
            self.selectedObj.Visibility = False
            if (hasattr(sel[0], "SubObjects")):
                self.selectedEdge = sel[0].SubObjects[0]
            else:
                raise Exception("Not implemented")

            # Recreate the object in separated shapes.
            self.saveVertices()

            if(hasattr(self.selectedEdge, "Vertexes")):
                self.oldEdgeVertexes = self.selectedEdge.Vertexes
            if not hasattr(self.selectedEdge, 'Edges'):
                raise Exception("Please select only one edge and try again")

            if not(type(self.selectedEdge.Curve) == _part.Line or
                   type(self.selectedEdge.Curve) == _part.BezierCurve):
                msg = "Curve edges are not supported yet"
                faced.errorDialog(msg)
                self.hide()

            self.setupRotation = self.calculateNewVector()

            self.ExtractTheEdge()
            self.newEdgeVertexes = self.newEdge.Shape.Vertexes
            # App.ActiveDocument.removeObject(self.selectedObj.Name)

            # Undo
            App.ActiveDocument.openTransaction(
                translate("Design456", "ExtendEdge"))

            # Deside how the Degree Wheel be drawn
            if self.faceDir == "+z" or self.faceDir == "-z":
                self.wheelObj = Fr_DegreeWheel_Widget([self.FirstLocation, App.Vector(0, 0, 0)], str(
                    round(self.w_rotation[3], 2)) + "°", 1, FR_COLOR.FR_RED, [0, 0, 0, 0],
                    self.setupRotation, [2.0, 2.0, 2.0], 2)
            else:
                self.wheelObj = Fr_DegreeWheel_Widget([self.FirstLocation, App.Vector(0, 0, 0)], str(
                    round(self.w_rotation[3], 2)) + "°", 1, FR_COLOR.FR_RED, [0, 0, 0, 0],
                    self.setupRotation, [2.0, 2.0, 2.0], 1)

            # Different callbacks for each action.
            self.wheelObj.w_wheel_cb_ = self.callback_Rotate
            self.wheelObj.w_xAxis_cb_ = self.MouseMovement_cb
            self.wheelObj.w_yAxis_cb_ = self.MouseMovement_cb
            self.wheelObj.w_45Axis_cb_ = self.MouseMovement_cb
            self.wheelObj.w_135Axis_cb_ = self.MouseMovement_cb

            self.wheelObj.w_callback_ = self.callback_release
            self.wheelObj.w_userData.callerObject = self

            self.COIN_recreateObject()

            if self._mywin is None:
                self._mywin = win.Fr_CoinWindow()

            self._mywin.addWidget(self.wheelObj)
            mw = self.getMainWindow()
            self._mywin.show()

            App.ActiveDocument.recompute()

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Activated' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def __del__(self):
        """
            class destructor
            Remove all objects from memory even fr_coinwindow
        """
        faced.EnableAllToolbar(True)
        try:
            self.wheelObj.hide()
            self.wheelObj.__del__()  # call destructor
            if self._mywin is not None:
                self._mywin.hide()
                del self._mywin
                self._mywin = None
            self.editing = False
            App.ActiveDocument.recompute()
            self.mw = None
            self.dialog = None
            self.tab = None
            self.wheelObj = None
            self._mywin = None
            self.b1 = None
            self.ExtrudeLBL = None
            self.run_Once = False
            self.endVector = None
            self.startVector = None
            self.tweakLength = 0.0
            # We will make two object, one for visual effect and the other is the original
            self.selectedObj = None
            self.direction = None
            self.setupRotation = [0, 0, 0, 0]
            # Used only with the center (cylinder)
            self.Rotation = [0, 0, 0, 0]
            # We use this to simplify the code - for both, 2D and 3D object, the face variable is this
            self.mouseOffset = App.Vector(0, 0, 0)
            self.FirstLocation = None
            del self

        except Exception as err:
            App.Console.PrintError("'Activated' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def getMainWindow(self):
        """[Create the tab for the tool]

        Raises:
            Exception: [If no tabs were found]
            Exception: [If something unusual happen]

        Returns:
            [dialog]: [the new dialog which will be added as a tab to the tab section of FreeCAD]
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
            oldsize = self.tab.count()
            self.dialog = QtGui.QDialog()
            self.tab.addTab(self.dialog, "Extend Edge")
            self.frmRotation = QtGui.QFrame(self.dialog)
            self.dialog.resize(200, 450)
            self.frmRotation.setGeometry(QtCore.QRect(10, 190, 231, 181))
            self.frame_2 = QtGui.QFrame(self.dialog)
            self.frame_2.setGeometry(QtCore.QRect(10, 195, 231, 151))
            self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
            self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
            self.frame_2.setObjectName("frame_2")
            self.gridLayoutWidget_3 = QtGui.QWidget(self.frame_2)
            self.gridLayoutWidget_3.setGeometry(
                QtCore.QRect(10, 40, 211, 101))
            self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
            self.gridTweakResult = QtGui.QGridLayout(
                self.gridLayoutWidget_3)
            self.gridTweakResult.setContentsMargins(0, 0, 0, 0)
            self.gridTweakResult.setObjectName("gridTweakResult")
            self.radioAsIs = QtGui.QRadioButton(self.gridLayoutWidget_3)
            self.lblTweakResult = QtGui.QLabel(self.frame_2)
            self.lblTweakResult.setGeometry(QtCore.QRect(10, 0, 191, 61))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.lblTweakResult.setFont(font)
            self.lblTweakResult.setObjectName("lblTweakResult")
            self.btnOK = QtGui.QDialogButtonBox(self.dialog)
            self.btnOK.setGeometry(QtCore.QRect(270, 360, 111, 61))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.btnOK.setFont(font)
            self.btnOK.setObjectName("btnOK")
            self.btnOK.setStandardButtons(QtGui.QDialogButtonBox.Ok)
            self.lblTitle = QtGui.QLabel(self.dialog)
            self.lblTitle.setGeometry(QtCore.QRect(10, 10, 281, 91))
            font = QtGui.QFont()
            font.setFamily("Times New Roman")
            font.setPointSize(10)
            self.lblTitle.setFont(font)
            self.lblTitle.setObjectName("lblTitle")
            self.ExtrudeLBL = QtGui.QLabel(self.dialog)
            self.ExtrudeLBL.setGeometry(QtCore.QRect(10, 145, 321, 40))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.ExtrudeLBL.setFont(font)
            self.ExtrudeLBL.setObjectName("ExtrudeLBL")
            self.RotateLBL = QtGui.QLabel(self.dialog)
            self.RotateLBL.setGeometry(QtCore.QRect(10, 100, 281, 40))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.RotateLBL.setFont(font)
            self.RotateLBL.setObjectName("RotateLBL")

            _translate = QtCore.QCoreApplication.translate
            self.dialog.setWindowTitle(_translate(
                "Dialog", "Extend Edge"))

            self.lblTweakResult.setText(
                _translate("Dialog", "Tweak Result"))
            self.lblTitle.setText(_translate("Dialog", "(Extend Edge)\n"
                                             "Tweak an object"))
            self.ExtrudeLBL.setText(_translate("Dialog", "Length="))
            self.RotateLBL.setText(_translate("Dialog", "Rotation Angle="))
            QtCore.QObject.connect(
                self.btnOK, QtCore.SIGNAL("accepted()"), self.hide)
            QtCore.QMetaObject.connectSlotsByName(self.dialog)
            self.tab.setCurrentWidget(self.dialog)

            return self.dialog

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Activated' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def hide(self):
        """
        Hide the widgets. Remove also the tab.
        TODO:
        For this tool, I decide to choose the hide to merge, or leave it "as is" here.
        I can do that during the extrusion (moving the Wheel), but that will be an action
        without undo. Here the user will be finished with the extrusion and want to leave the tool
        TODO: If there will be a discussion about this, we might change this behavior!!
        """
        self.dialog.hide()
        del self.dialog
        dw = self.mw.findChildren(QtGui.QDockWidget)
        newsize = self.tab.count()  # Todo : Should we do that?
        self.tab.removeTab(newsize - 1)  # it ==0,1,2,3 .etc
        # App.ActiveDocument.recompute()
        self.__del__()  # Remove all smart Extrude Rotate 3dCOIN widgets

    def MouseMovement_cb(self, userData=None):
        events = userData.events
        # print("mouseMove")
        if self.isItRotation is True:
            self.callback_Rotate()
            return  # We cannot allow this tool
        if type(events) != int:
            print("event was not int")
            return
        clickwdgdNode = fr_coin3d.objectMouseClick_Coin3d(self.wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.pos,
                                                          self.wheelObj.w_pick_radius, self.wheelObj.w_XsoSeparator)

        self.endVector = App.Vector(self.wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_x,
                                    self.wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_y,
                                    self.wheelObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_z)
        if self.run_Once is False:
            self.run_Once = True
            # only once
            self.startVector = self.endVector
            # self.wheelObj.w_vector[0].sub(self.startVector)
            self.mouseOffset = App.Vector(0, 0, 0)

        self.tweakLength = round((
            self.endVector - self.startVector).dot(self.normalVector), 1)

        if abs(self.oldTweakLength-self. tweakLength) < 1:
            return  # we do nothing
        self.ExtrudeLBL.setText(
            "Length= " + str(round(self.tweakLength, 1)))

        self.oldEdgeVertexes = self.newEdgeVertexes
        self.newEdge.Placement.Base = self.endVector
        self.newEdgeVertexes = self.newEdge.Shape.Vertexes
        self.COIN_recreateObject()
        self.wheelObj.w_vector[0] = self.endVector
        self.wheelObj.redraw()
        view = Gui.ActiveDocument.ActiveView
        sg = view.getSceneGraph()
        sg.addChild(self.coinFaces)

    # TODO FIXME:
    def callback_release(self, userData=None):
        try:
            events = userData.events
            self.recreateObject()
            print("mouse release")
            self.wheelObj.remove_focus()
            self.run_Once = False
            self.startVector = None
            view = Gui.ActiveDocument.ActiveView
            sg = view.getSceneGraph()
            self.coinFaces.removeAllChildren()
            sg.removeChild(self.coinFaces)

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Activated' Release Filed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def smartlbl_callback(self):
        print("lbl callback")
        pass

    # Rotation only TODO: FIXME:
    def callback_Rotate(self):
        print("Not impolemented ")

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_ExtendEdge.svg',
            'MenuText': ' Extend Edge',
                        'ToolTip':  ' Extend Edge'
        }


Gui.addCommand('Design456_ExtendEdge', Design456_ExtendEdge())
