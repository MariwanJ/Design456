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
from ThreeDWidgets.fr_three_arrows_widget import Fr_ThreeArrows_Widget
from ThreeDWidgets.fr_draw import draw_FaceSet
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from draftutils.translate import translate  # for translation
import Part as _part
import FACE_D as faced
import math

# Some get problem with this.. not used but Might be used in the future.
# I might remove it for this tool. But lets leave it now.
try:
    from OCC import Core
    from OCC.Core import ChFi2d
except:
    pass


class Design456_ExtendFace:
    """[Extend the face's position to a new position.
     This will affect the faces share the face.]
     """
    _Vector = None
    mw = None
    dialog = None
    tab = None
    padObj = None
    w_rotation = None
    _mywin = None
    b1 = None
    TweakLBL = None
    RotateLBL = None
    endVector = None
    startVector = None
    setupRotation = None
    savedVertices = None
    counter = None
    run_Once = None
    tweakLength = None
    oldTweakLength = None
    isItRotation = None
    newObject = None
    selectedObj = None
    selectedFace = None
    # Original vectors that will be changed by mouse.
    oldEdgeVertexes = None
    newFaceVertexes = None
    newFace = None      # Keep new vectors for the moved old face-vectors

    view = None  # used for captureing mouse events
    MoveMentDirection = None
    newFaces = None
    faceDir = None
    FirstLocation = None
    coinFaces = None
    sg = None  # SceneGraph

    # Based on the setTolerance from De-featuring WB,
    # but simplified- Thanks for the author
    def setTolerance(self, sel):
        try:
            if hasattr(sel, 'Shape'):
                ns = sel.Shape.copy()
                new_tol = 0.001
                ns.fixTolerance(new_tol)
                sel.ViewObject.Visibility = False
                sl = App.ActiveDocument.addObject("Part::Feature", "Solid")
                sl.Shape = ns
                g = Gui.ActiveDocument.getObject(sel.Name)
                g.ShapeColor = sel.ViewObject.ShapeColor
                g.LineColor = sel.ViewObject.LineColor
                g.PointColor = sel.ViewObject.PointColor
                g.DiffuseColor = sel.ViewObject.DiffuseColor
                g.Transparency = sel.ViewObject.Transparency
                App.ActiveDocument.removeObject(sel.Name)
                sl.Label = 'Extending'
                return sl

        except Exception as err:
            App.Console.PrintError("'sewShape' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    # Based on the sewShape from De-featuring WB,
    # but simplified- Thanks for the author
    def sewShape(self, sel):
        """[Fix issues might be in the created object]

        Args:
            sel ([3D Object]): [Final object that needs repair.
                                Always new object creates as result of sew]
        """
        try:
            if hasattr(sel, 'Shape'):
                sh = sel.Shape.copy()
                sh.sewShape()
                sl = App.ActiveDocument.addObject("Part::Feature", "compSolid")
                sl.Shape = sh

                g = Gui.ActiveDocument.getObject(sl.Name)
                g.ShapeColor = Gui.ActiveDocument.getObject(
                    sel.Name).ShapeColor
                g.LineColor = Gui.ActiveDocument.getObject(sel.Name).LineColor
                g.PointColor = Gui.ActiveDocument.getObject(
                    sel.Name).PointColor
                g.DiffuseColor = Gui.ActiveDocument.getObject(
                    sel.Name).DiffuseColor
                g.Transparency = Gui.ActiveDocument.getObject(
                    sel.Name).Transparency
                App.ActiveDocument.removeObject(sel.Name)
                App.ActiveDocument.recompute()
                return (sl)

        except Exception as err:
            App.Console.PrintError("'sewShape' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def ExtractTheEdge(self):
        """[Extract the face for movement]
        """
        self.newFace = App.ActiveDocument.addObject(
            "Part::Feature", "Face")
        sh = self.selectedFace.copy()
        self.newFace.Shape = sh
        # self.selectedFace = self.newFace  # TODO: SHOULD WE DO THAT: FIXME:
        # App.ActiveDocument.recompute()

    def COIN_recreateObject(self):
        self.sg.removeChild(self.coinFaces)
        for i in range(0, len(self.savedVertices)):
            for j in range(0, len(self.savedVertices[i])):
                if self.savedVertices[i][j].Point == self.oldEdgeVertexes[0].Point:
                    self.savedVertices[i][j] = self.newFaceVertexes[0]
                elif self.savedVertices[i][j].Point == self.oldEdgeVertexes[1].Point:
                    self.savedVertices[i][j] = self.newFaceVertexes[1]

        # We have the new vertices
        self.coinFaces.removeAllChildren()
        for i in self.savedVertices:
            a = []
            for j in i:
                a.append(j.Point)
            self.coinFaces.addChild(draw_FaceSet(
                a, [len(a), ], FR_COLOR.FR_LIGHTGRAY))
        self.sg.addChild(self.coinFaces)

    def recreateObject(self):
        # FIXME:
        # Here we have
        # We try to create a wire-closed to replace the sides we delete.
        # This will be way to complex . with many bugs :(
        try:
            App.ActiveDocument.removeObject(self.newFace.Name)
            _result = []
            _resultFace = []
            _result.clear()
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
                _result.append(nFace)
                _resultFace.append(newFace)
            self.newFaces = _result

            solidObjShape = _part.Solid(_part.Shell(_resultFace))
            newObj = App.ActiveDocument.addObject("Part::Feature", "comp")
            newObj.Shape = solidObjShape
            newObj = self.sewShape(newObj)
            newObj = self.setTolerance(newObj)
            solidObjShape = _part.Solid(newObj.Shape)
            final = App.ActiveDocument.addObject("Part::Feature", "Extended")
            final.Shape = solidObjShape
            App.ActiveDocument.removeObject(newObj.Name)
            for face in self.newFaces:
                App.ActiveDocument.removeObject(face.Name)

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

            self.FirstLocation = yL + d * nv  # the 3 arrows-pads
            self.FirstLocation.z = self.selectedObj.Shape.BoundBox.ZMax

            return rotation

        except Exception as err:

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

        except Exception as err:

            App.Console.PrintError("'saveVertices' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Activated(self):
        """[ Executes when the tool is used   ]
        """
        self.coinFaces = coin.SoSeparator()
        self.w_rotation = [0.0, 0.0, 0.0, 0.0]  # pads rotation
        self.setupRotation = [0, 0, 0, 0]
        self._Vector = App.Vector(0.0, 0.0, 0.0)  # pads POSITION
        self.counter = 0
        self.run_Once = False
        self.tweakLength = 0
        self.oldTweakLength = 0
        self.isItRotation = False
        self.newFaces = []
        self.savedVertices = [[]]
        self.tweakLength = 0
        self.oldTweakLength = 0

        try:
            self.view = Gui.ActiveDocument.ActiveView
            self.sg = self.view.getSceneGraph()
            sel = Gui.Selection.getSelectionEx()

            if len(sel) > 2:
                errMessage = "Please select only one face and try again"
                faced.errorDialog(errMessage)
                return

            self.MoveMentDirection = 'A'

            # Register undo

            self.selectedObj = sel[0].Object
            self.selectedObj.Visibility = False
            if (hasattr(sel[0], "SubObjects")):
                self.selectedFace = sel[0].SubObjects[0]
            else:
                raise Exception("Not implemented")

            if self.selectedFace.ShapeTyp != 'Face':
                errMessage = "Please select only one face and try again, was: " + \
                    str(self.selectedFace.ShapeTyp)
                faced.errorDialog(errMessage)
                return

            # Recreate the object in separated shapes.
            self.saveVertices()

            if(hasattr(self.selectedFace, "Vertexes")):
                self.oldEdgeVertexes = self.selectedFace.Vertexes
            if not hasattr(self.selectedFace, 'Edges'):
                raise Exception("Please select only one face and try again")

            if not(type(self.selectedFace.Curve) == _part.Line or
                   type(self.selectedFace.Curve) == _part.BezierCurve):
                msg = "Curve edges are not supported yet"
                faced.errorDialog(msg)
                self.hide()

            self.setupRotation = self.calculateNewVector()

            self.ExtractTheEdge()
            self.newFaceVertexes = self.newFace.Shape.Vertexes
            App.ActiveDocument.removeObject(self.selectedObj.Name)

            # Undo
            App.ActiveDocument.openTransaction(
                translate("Design456", "ExtendFace"))

            # Deside how the Degree pad be drawn
            self.padObj = Fr_ThreeArrows_Widget([self.FirstLocation, App.Vector(0, 0, 0)],  #
                                                # label
                                                (str(
                                                    round(self.w_rotation[3], 2)) + "°"),
                                                FR_COLOR.FR_WHITE,  # lblcolor
                                                [FR_COLOR.FR_RED, FR_COLOR.FR_GREEN,
                                                 FR_COLOR.FR_BLUE],  # arrows color
                                                [0, 0, 0, 0],  # rotation
                                                self.setupRotation,  # setup rotation
                                                [10.0, 10.0, 10.0],  # scale
                                                0,  # type
                                                0,  # opacity
                                                [10, 10, 10])  # distance between them

            # Different callbacks for each action.
            self.padObj.w_xAxis_cb_ = self.MouseMovement_cb
            self.padObj.w_yAxis_cb_ = self.MouseMovement_cb
            self.padObj.w_zAxis_cb_ = self.MouseMovement_cb

            self.padObj.w_padXAxis_cb_ = self.callback_Rotate
            self.padObj.w_padYAxis_cb_ = self.callback_Rotate
            self.padObj.w_padZAxis_cb_ = self.callback_Rotate

            self.padObj.w_callback_ = self.callback_release
            self.padObj.w_userData.callerObject = self

            self.COIN_recreateObject()

            if self._mywin is None:
                self._mywin = win.Fr_CoinWindow()

            self._mywin.addWidget(self.padObj)
            mw = self.getMainWindow()
            self._mywin.show()

            App.ActiveDocument.recompute()

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
            self.tab.addTab(self.dialog, "Extend Face")
            self.frmRotation = QtGui.QFrame(self.dialog)
            self.dialog.resize(200, 450)
            self.frmRotation.setGeometry(QtCore.QRect(10, 190, 231, 181))
            self.lblTweakResult = QtGui.QLabel(self.dialog)
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
            self.TweakLBL = QtGui.QLabel(self.dialog)
            self.TweakLBL.setGeometry(QtCore.QRect(10, 145, 321, 40))
            font = QtGui.QFont()
            font.setPointSize(10)
            font = QtGui.QFont()
            font.setPointSize(10)

            _translate = QtCore.QCoreApplication.translate
            self.dialog.setWindowTitle(_translate(
                "Dialog", "Extend Face"))

            self.lblTitle.setText(_translate("Dialog", "(Extend Face)\n"
                                             "Tweak an object\n Use X, Y, or Z axis to pull/push an"))
            self.TweakLBL.setFont(font)

            self.TweakLBL.setText(_translate("Dialog", "Length = 0.0"))
            QtCore.QObject.connect(
                self.btnOK, QtCore.SIGNAL("accepted()"), self.hide)
            QtCore.QMetaObject.connectSlotsByName(self.dialog)
            self.tab.setCurrentWidget(self.dialog)
            return self.dialog

        except Exception as err:
            App.Console.PrintError("'Activated' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def MouseMovement_cb(self, userData=None):

        events = userData.events
        if type(events) != int:
            print("event was not int")
            return

        if self.padObj.w_userData.Axis is None:
            if self.padObj.w_userData.padAxis is not None:
                self.callback_Rotate()
                return
            else:
                return  # We cannot allow this tool

        self.endVector = App.Vector(self.padObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_x,
                                    self.padObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_y,
                                    self.padObj.w_parent.link_to_root_handle.w_lastEventXYZ.Coin_z)
        if self.run_Once is False:
            self.run_Once = True
            # only once
            self.startVector = self.endVector

        self.tweakLength = round((
            self.endVector - (self.startVector+self._Vector)).dot(self.normalVector), 1)

        if abs(self.oldTweakLength-self. tweakLength) < 1:
            return  # we do nothing
        self.TweakLBL.setText(
            "Length = " + str(round(self.tweakLength, 1)))
        # must be tuple
        self.padObj.label(["Length = " + str(round(self.tweakLength, 1)), ])
        self.padObj.lblRedraw()
        self.oldEdgeVertexes = self.newFaceVertexes
        if self.padObj.w_userData.Axis == 'X':
            self.newFace.Placement.Base.x = self.endVector.x
            self.padObj.w_vector[0].x = self.endVector.x
        elif self.padObj.w_userData.Axis == 'Y':
            self.newFace.Placement.Base.y = self.endVector.y
            self.padObj.w_vector[0].y = self.endVector.y
        elif self.padObj.w_userData.Axis == 'Z':
            self.newFace.Placement.Base.z = self.endVector.z
            self.padObj.w_vector[0].z = self.endVector.z
        else:
            # nothing to do here  #TODO : This shouldn't happen
            return

        self.newFaceVertexes = self.newFace.OuterWire.OrderedVertexes
        self.COIN_recreateObject()
        self.padObj.redraw()

    def callback_release(self, userData=None):
        try:
            events = userData.events
            print("mouse release")
            self.padObj.remove_focus()
            self.run_Once = False

        except Exception as err:
            App.Console.PrintError("'Activated' Release Filed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def smartlbl_callback(self):
        print("lbl callback")
        pass

    def callback_Rotate(self):
        initialAng=0
        #padCenter= 
        
        
        
        
        print("Not impolemented ")

    def hide(self):
        """
        Hide the widgets. Remove also the tab.
        TODO:
        For this tool, I decide to choose the hide to merge, or leave it "as is" here.
        I can do that during the extrusion (moving the pad), but that will be an action
        without undo. Here the user will be finished with the extrusion and want to leave the tool
        TODO: If there will be a discussion about this, we might change this behavior!!
        """
        self.dialog.hide()
        self.recreateObject()

        # Remove coin objects
        self.coinFaces.removeAllChildren()
        self.sg.removeChild(self.coinFaces)

        del self.dialog
        dw = self.mw.findChildren(QtGui.QDockWidget)
        newsize = self.tab.count()  # Todo : Should we do that?
        self.tab.removeTab(newsize - 1)  # it ==0,1,2,3 .etc

        App.ActiveDocument.commitTransaction()  # undo reg.

        self.__del__()  # Remove all smart Extrude Rotate 3dCOIN widgets

    def __del__(self):
        """
            class destructor
            Remove all objects from memory even fr_coinwindow
        """
        try:
            self.padObj.hide()
            self.padObj.__del__()  # call destructor
            if self._mywin is not None:
                self._mywin.hide()
                del self._mywin
                self._mywin = None
            del self.padObj
            self.mw = None
            self.dialog = None
            self.tab = None
            self._mywin = None
            self.b1 = None
            self.TweakLBL = None
            self.run_Once = None
            self.endVector = None
            self.startVector = None
            self.tweakLength = None
            # We will make two object,
            # one for visual effect and the other is the original
            self.selectedObj = None
            self.direction = None
            self.setupRotation = None
            self.Rotation = None
            self.mouseOffset = None
            self.FirstLocation = None
            del self.selectedObj
            del self.selectedFace
            del self.savedVertices
            del self.newFaceVertexes
            del self.oldEdgeVertexes
            self.coinFaces.removeAllChildren()
            del self.coinFaces
            self.sg.removeChild(self.coinFaces)
            self.coinFaces = None
            del self

        except Exception as err:
            App.Console.PrintError("'Activated' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_ExtendFace.svg',
            'MenuText': ' Extend Face',
            'ToolTip':  ' Extend Face'
        }


Gui.addCommand('Design456_ExtendFace', Design456_ExtendFace())
