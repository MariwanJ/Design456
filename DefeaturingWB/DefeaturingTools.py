# -*- coding: utf-8 -*-

#
# ***************************************************************************
# *                                                                         *
# *  This file is a part of the Open Source Design456 Workbench - App.  *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *                                                                         *
# *                                                                         *
# *  This library is free software; you can redistribute it and/or          *
# *  modify it under the terms of the GNU Lesser General Public             *
# *  License as published by the Free Software Foundation; either           *
# *  version 2 of the License, or (at your option) any later version.       *
# *                                                                         *
# *  This library is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# *  Lesser General Public License for more details.                        *
# *                                                                         *
# *  You should have received a copy of the GNU Lesser General Public       *
# *  License along with this library; if not, If not, see                   *
# *  <http://www.gnu.org/licenses/>.                                        *
# *                                                                         *
# *  Modified and added                                                     *
# *  to Design456 by : Mariwan Jalal   mariwan.jalal@gmail.com              *
# ***************************************************************************

# ****************************************************************************
# *                                                                          *
# *  Copyright (c) 2017                                                      *
# *  Maurice easyw@katamail.com                                              *
# *                                                                          *
#                                                                           *
#   Repair Defeaturing Macro                                 *
#                                                                           *
#  (C) Maurice easyw-fc 2018                                               *
#    This program is free software; you can redistribute it and/or modify   *
#    it under the terms of the GNU Library General Public License (LGPL)    *
#    as published by the Free Software Foundation; either version 2 of      *
#    the License, or (at your option) any later version.                    *
#    for detail see the LICENCE text file.                                  *
# ****************************************************************************


import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import Draft
import Part
import re
import os
import sys
import OpenSCADCommands
import OpenSCAD2Dgeom
import OpenSCADFeatures
from PySide import QtCore, QtGui
import tempfile
import Design456Init
import base64
import DefeaturingWB.DefeaturingCMD
from DefeaturingWB.image_file import *
from draftutils.translate import translate  # for translation
try:
    from PathScripts.PathUtils import horizontalEdgeLoop
    from PathScripts.PathUtils import horizontalFaceLoop
    from PathScripts.PathUtils import loopdetect
except:
    App.Console.PrintError('Path WB not found\n')

from __future__ import unicode_literals
import DefeaturingWB.image_file
from sys import platform as _platform


global rh_edges, rh_faces, rh_obj
global rh_edges_names, rh_faces_names, rh_obj_name
global created_faces, rh_faces_indexes, rh_edges_to_connect
global force_recompute, invert

__version__ = "v1.3.5"


# window GUI dimensions parameters
wdsRHx = 260
wdsRHy = 534
pt_osx = False
if _platform == "linux" or _platform == "linux2":
    # linux
    sizeX = wdsRHx
    sizeY = wdsRHy-22+34  # 516 #536
else:
    sizeX = wdsRHx
    sizeY = wdsRHy-22  # 482#502
if _platform == "darwin":
    pt_osx = True

btn_sizeX = 28
btn_sizeY = 28


invert = True
rh_edges = []
rh_edges_names = []
rh_edges_to_connect = []
rh_faces = []
rh_faces_names = []
rh_faces_indexes = []
created_faces = []
rh_obj = []
rh_obj_name = []
force_recompute = False  # True


def mk_str(input):
    if (sys.version_info > (3, 0)):  # py3
        if isinstance(input, str):
            return input
        else:
            input = input.encode('utf-8')
            return input
    else:  # py2
        if type(input) == unicode:
            input = input.encode('utf-8')
            return input
        else:
            return input
##


def i_say(msg):
    App.Console.PrintMessage(msg)
    App.Console.PrintMessage('\n')


def i_sayw(msg):
    App.Console.PrintWarning(msg)
    App.Console.PrintWarning('\n')


def i_sayerr(msg):
    App.Console.PrintError(msg)
    App.Console.PrintWarning('\n')

##


def checkBOP(shape):
    """ checking BOP errors of a shape 
    returns:
      - True if Shape is Valid
      - the Shape errors 
    """

    # enabling BOP check
    paramGt = App.ParamGet(
        "User parameter:BaseApp/Preferences/Mod/Part/CheckGeometry")
    paramGt.SetBool("RunBOPCheck", True)

    try:
        shape.check(True)
        return True
    except:
        return sys.exc_info()[1]  # ValueError #sys.exc_info() #False
##


def checking_BOP(o):
    if hasattr(o, 'Shape'):
        chks = checkBOP(o.Shape)
        if chks is not True:
            i_sayerr('shape \''+o.Name+'\' \'' +
                     mk_str(o.Label)+'\' is INVALID!\n')

            i_sayw(str(chks))

            if 'No error' in str(chks):
                if len(o.Shape.Shells) > 0:
                    for sh in o.Shape.Shells:
                        try:
                            sh.check(True)
                        except:
                            i_sayerr(mk_str(o.Label)+'.shell errors:')
                            i_sayw(mk_str(sys.exc_info()[1]))
        else:
            i_say('shape \''+o.Name+'\' \''+mk_str(o.Label)+'\' is valid\n')
##


def check_TypeId_RH():
    try:
        if Gui.Selection.getSelection():
            sel = Gui.Selection.getSelection()

            if len(sel) < 1:
                msg = "Select one or more object(s) to be checked!\n"
                reply = QtGui.QMessageBox.information(None, "Warning", msg)
                App.Console.PrintWarning(msg)
            else:
                non_solids = ''
                solids = ''
                for o in sel:
                    if hasattr(o, "Shape"):
                        if '.[compsolid]' in o.Label or '.[solid]' in o.Label or '.[shell]' in o.Label\
                                or '.[compound]' in o.Label or '.[face]' in o.Label or '.[edge]' in o.Label or '.[wire]' in o.Label\
                                or '.[vertex]' in o.Label:
                            o.Label = mk_str(o.Label).replace('.[solid]', '').replace('.[shell]', '').replace('.[compsolid]', '').replace('.[compound]', '')\
                                .replace('.[face]', '').replace('.[wire]', '').replace('.[edge]', '').replace('.[vertex]', '')
                        else:
                            len_shapes = len(o.Shape.Solids)+len(o.Shape.Shells)+len(o.Shape.Compounds)+len(o.Shape.CompSolids) +\
                                len(o.Shape.Faces)+len(o.Shape.Edges) + \
                                len(o.Shape.Wires)+len(o.Shape.Vertexes)
                            lbl = mk_str(o.Label)
                            i_say('\n'+lbl + '-> Shape Content: '+str(len_shapes) +
                                  ' shapes -------------------------------')
                            if len(o.Shape.Solids) == 0:
                                i_sayerr(mk_str(o.Label) +
                                         ' object is a NON Solid')
                            if len(o.Shape.CompSolids) > 0:
                                i_say(
                                    mk_str(o.Label)+' CompSolids object(s) NBR : '+str(len(o.Shape.CompSolids)))
                                if '.[compsolid]' not in o.Label and '.[solid]' not in o.Label and '.[shell]' not in o.Label\
                                        and '.[compound]' not in o.Label and '.[face]' not in o.Label and '.[edge]' not in o.Label:
                                    o.Label = mk_str(o.Label)+'.[compsolid]'
                            if len(o.Shape.Compounds) > 0:
                                i_say(
                                    mk_str(o.Label)+' Compound object(s) NBR : '+str(len(o.Shape.Compounds)))
                                if '.[compound]' not in o.Label and '.[solid]' not in o.Label and '.[shell]' not in o.Label:
                                    o.Label = mk_str(o.Label)+'.[compound]'
                            if len(o.Shape.Solids) > 0:
                                i_say(
                                    mk_str(o.Label)+' Solid object(s) NBR : '+str(len(o.Shape.Solids)))
                                solids += mk_str(o.Label)+'<br>'
                                if '.[solid]' not in o.Label and '.[compsolid]' not in o.Label and '.[compound]' not in o.Label:
                                    o.Label = mk_str(o.Label)+'.[solid]'
                            else:

                                non_solids += mk_str(o.Label)+'<br>'
                            if len(o.Shape.Shells) > 0:
                                i_say(
                                    mk_str(o.Label)+' Shell object(s) NBR : '+str(len(o.Shape.Shells)))
                                if '.[shell]' not in o.Label and '.[solid]' not in o.Label and '.[compsolid]' not in o.Label and '.[compound]' not in o.Label:
                                    o.Label = mk_str(o.Label)+'.[shell]'
                            if len(o.Shape.Faces) > 0:
                                i_say(
                                    mk_str(o.Label)+' Face object(s) NBR : '+str(len(o.Shape.Faces)))
                                if '.[compsolid]' not in o.Label and '.[solid]' not in o.Label and '.[shell]' not in o.Label\
                                        and '.[compound]' not in o.Label and '.[face]' not in o.Label and '.[edge]' not in o.Label:
                                    o.Label = mk_str(o.Label)+'.[face]'
                            if len(o.Shape.Wires) > 0:
                                i_say(
                                    mk_str(o.Label)+' Wire object(s) NBR : '+str(len(o.Shape.Wires)))
                                if '.[compsolid]' not in o.Label and '.[solid]' not in o.Label and '.[shell]' not in o.Label\
                                        and '.[compound]' not in o.Label and '.[face]' not in o.Label and '.[wire]' not in o.Label:
                                    o.Label = mk_str(o.Label)+'.[wire]'
                            if len(o.Shape.Edges) > 0:
                                i_say(
                                    mk_str(o.Label)+' Edge object(s) NBR : '+str(len(o.Shape.Edges)))
                                if '.[compsolid]' not in o.Label and '.[solid]' not in o.Label and '.[shell]' not in o.Label\
                                        and '.[compound]' not in o.Label and '.[face]' not in o.Label and '.[edge]' not in o.Label and '.[wire]' not in o.Label:
                                    o.Label = mk_str(o.Label)+'.[edge]'
                            if len(o.Shape.Vertexes) > 0:
                                i_say(
                                    mk_str(o.Label)+' Vertex object(s) NBR : '+str(len(o.Shape.Vertexes)))
                                if '.[compsolid]' not in o.Label and '.[solid]' not in o.Label and '.[shell]' not in o.Label\
                                        and '.[compound]' not in o.Label and '.[face]' not in o.Label and '.[edge]' not in o.Label\
                                        and '.[wire]' not in o.Label and '.[vertex]' not in o.Label:
                                    o.Label = mk_str(o.Label)+'.[vertex]'
                    else:
                        App.Console.PrintWarning(
                            "Select object with a \"Shape\" to be checked!\n")

        else:

            reply = QtGui.QMessageBox.information(
                None, "Warning", "Select one or more object(s) to be checked!")
            App.Console.PrintWarning(
                "Select one or more object(s) to be checked!\n")
    except Exception as err:
        App.Console.PrintError("'check_TypeId_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def clear_all_RH():
    try:
        global rh_edges, rh_faces, rh_obj
        global rh_edges_names, rh_faces_names, rh_obj_name
        global created_faces, rh_faces_indexes, rh_edges_to_connect

        rh_edges = []
        rh_edges_names = []
        rh_edges_to_connect = []
        created_faces = []
        RHDockWidget.ui.TE_Edges.setPlainText("")
        rh_faces = []
        rh_faces_names = []
        rh_faces_indexes = []
        created_faces = []
        RHDockWidget.ui.TE_Faces.setPlainText("")
        rh_obj = []
        rh_obj_name = []
        RHDockWidget.ui.Edge_Nbr.setText("0")
        RHDockWidget.ui.Face_Nbr.setText("0")
        RHDockWidget.ui.Obj_Nbr.setText("0")
        RHDockWidget.ui.Obj_Nbr_2.setText("0")
    except Exception as err:
        App.Console.PrintError("'clear_all_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def refine_parametric_RH():
    try:
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        sel = Gui.Selection.getSelectionEx()
        if len(sel) > 0:
            for selobj in sel:
                if hasattr(selobj.Object, "Shape"):
                    newobj = selobj.Document.addObject(
                        "Part::FeaturePython", 'refined')
                    OpenSCADFeatures.RefineShape(newobj, selobj.Object)
                    OpenSCADFeatures.ViewProviderTree(newobj.ViewObject)
                    # to do: see if it is possible to conserve colors in refining
                    ao = App.ActiveDocument.ActiveObject
                    docG.ActiveObject.ShapeColor = docG.getObject(
                        selobj.Object.Name).ShapeColor
                    docG.ActiveObject.LineColor = docG.getObject(
                        selobj.Object.Name).LineColor
                    docG.ActiveObject.PointColor = docG.getObject(
                        selobj.Object.Name).PointColor
                    docG.ActiveObject.DiffuseColor = docG.getObject(
                        selobj.Object.Name).DiffuseColor
                    docG.ActiveObject.Transparency = docG.getObject(
                        selobj.Object.Name).Transparency

                    newobj.Label = selobj.Object.Label
                    selobj.Object.ViewObject.hide()
            doc.recompute()
    except Exception as err:
        App.Console.PrintError("'refine_parametric_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def refine_RH():
    try:
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        sel = Gui.Selection.getSelection()
        App.ActiveDocument.openTransaction(translate("Design456", "refine_RH"))
        if len(sel):
            for o in sel:
                if hasattr(o, "Shape"):
                    doc.addObject('Part::Feature',
                                  'refined').Shape = o.Shape.removeSplitter()
                    doc.ActiveObject.Label = o.Label
                    docG.getObject(o.Name).hide()
                    docG.ActiveObject.ShapeColor = docG.getObject(
                        o.Name).ShapeColor
                    docG.ActiveObject.LineColor = docG.getObject(
                        o.Name).LineColor
                    docG.ActiveObject.PointColor = docG.getObject(
                        o.Name).PointColor
                    docG.ActiveObject.DiffuseColor = docG.getObject(
                        o.Name).DiffuseColor
                    docG.ActiveObject.Transparency = docG.getObject(
                        o.Name).Transparency
                    doc.recompute()

        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'refine_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def edges_clear_RH():
    try:
        global rh_edges, rh_faces, rh_obj
        global rh_edges_names, rh_faces_names, rh_obj_name
        global created_faces, rh_faces_indexes, rh_edges_to_connect

        rh_edges = []
        rh_edges_names = []
        rh_edges_to_connect = []
        created_faces = []
        RHDockWidget.ui.TE_Edges.setPlainText("")
        rh_faces = []
        rh_faces_names = []
        rh_faces_indexes = []
        created_faces = []
        RHDockWidget.ui.TE_Faces.setPlainText("")
        rh_obj = []
        rh_obj_name = []
        RHDockWidget.ui.Edge_Nbr.setText("0")
        RHDockWidget.ui.Face_Nbr.setText("0")
    except Exception as err:
        App.Console.PrintError("'edges_clear_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def faces_clear_RH():
    try:
        global rh_edges, rh_faces, rh_obj
        global rh_edges_names, rh_faces_names, rh_obj_name
        global created_faces, rh_faces_indexes, rh_edges_to_connect

        rh_faces = []
        rh_faces_names = []
        rh_faces_indexes = []
        created_faces = []
        RHDockWidget.ui.TE_Faces.setPlainText("")
        rh_edges = []
        rh_edges_names = []
        rh_edges_to_connect = []
        created_faces = []
        rh_obj = []
        rh_obj_name = []
        RHDockWidget.ui.TE_Edges.setPlainText("")
        RHDockWidget.ui.Edge_Nbr.setText("0")
        RHDockWidget.ui.Face_Nbr.setText("0")
    except Exception as err:
        App.Console.PrintError("'faces_clear_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def close_RH():
    """closing dialog"""
    RHDockWidget.deleteLater()


def merge_selected_faces_RH():
    """merging Faces of selected shapes"""
    try:
        App.ActiveDocument.openTransaction(
            translate("Design456", "merge_selected_faces_RH"))
        global rh_edges, rh_faces, rh_obj
        global rh_edges_names, rh_faces_names, rh_obj_name
        global created_faces, rh_faces_indexes, rh_edges_to_connect

        af_faces = rh_faces

        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        _test = None

        if len(af_faces) > 0:

            try:
                _test = Part.makeShell(af_faces)
                if _test.isNull():

                    App.Console.PrintWarning('Failed to create shell\n')
            except:
                App.Console.PrintWarning('Failed to create shell\n')
                for f in af_faces:
                    Part.show(f)
                    doc.ActiveObject.Label = "face"
                return
            if RHDockWidget.ui.checkBox_Refine.isChecked():
                try:
                    _test.removeSplitter()
                except:
                    print('not refined')
            if _test.ShapeType != 'Shell':
                raise RuntimeError('Part object is not a shell')
            _test = Part.Solid(_test)
            if _test.isNull():
                raise RuntimeError('Failed to create solid')
            if RHDockWidget.ui.checkBox_Refine.isChecked():
                try:
                    _test.removeSplitter()
                except:
                    print('not refined')
            if RHDockWidget.ui.checkBox_Refine.isChecked():
                doc.addObject('Part::Feature',
                              'SolidRefined').Shape = _test.removeSplitter()
            else:
                doc.addObject('Part::Feature', 'Solid').Shape = _test

            mysolidr = doc.ActiveObject
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'merge_selected_faces_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def checkShape():
    """checking Shape"""

    doc = App.ActiveDocument
    docG = Gui.ActiveDocument

    sel = Gui.Selection.getSelection()
    if len(sel) == 1:
        o = sel[0]
        checking_BOP(o)
    else:
        msg = "Select one or more object(s) to be checked!\n"
        reply = QtGui.QMessageBox.information(None, "Warning", msg)
        App.Console.PrintWarning(msg)


def sewShape():
    """checking Shape"""
    try:
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        App.ActiveDocument.openTransaction(translate("Design456", "sewShape"))
        sel = Gui.Selection.getSelection()
        if len(sel) == 1:
            o = sel[0]
            if hasattr(o, 'Shape'):
                sh = o.Shape.copy()
                sh.sewShape()
                sl = Part.Solid(sh)
                docG.getObject(o.Name).Visibility = False
                Part.show(sl)
                ao = App.ActiveDocument.ActiveObject
                ao.Label = 'Solid'
                docG.ActiveObject.ShapeColor = docG.getObject(
                    o.Name).ShapeColor
                docG.ActiveObject.LineColor = docG.getObject(o.Name).LineColor
                docG.ActiveObject.PointColor = docG.getObject(
                    o.Name).PointColor
                docG.ActiveObject.DiffuseColor = docG.getObject(
                    o.Name).DiffuseColor
                docG.ActiveObject.Transparency = docG.getObject(
                    o.Name).Transparency
        else:
            msg = "Select one or more object(s) to be checked!\n"
            reply = QtGui.QMessageBox.information(None, "Warning", msg)
            App.Console.PrintWarning(msg)
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'sewShape' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def getTolerance():
    """getting Tolerance"""

    doc = App.ActiveDocument
    docG = Gui.ActiveDocument

    sel = Gui.Selection.getSelection()
    if len(sel) == 1:
        o = sel[0]
        if hasattr(o, 'Shape'):
            tol = o.Shape.getTolerance(0)
            i_say(mk_str(o.Label)+' tolerance = '+str(tol))
    else:
        msg = "Select one or more object(s) to be checked!\n"
        reply = QtGui.QMessageBox.information(None, "Warning", msg)
        App.Console.PrintWarning(msg)
##


def setTolerance():
    """getting Tolerance"""
    try:
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        App.ActiveDocument.openTransaction(translate("Design456", "Star"))
        sel = Gui.Selection.getSelection()
        if len(sel) == 1:
            o = sel[0]
            if hasattr(o, 'Shape'):
                ns = o.Shape.copy()
                i_say(mk_str(o.Label)+' tolerance = '+str(ns.getTolerance(0)))
                new_tol = float(RHDockWidget.ui.tolerance_value.text())
                ns.fixTolerance(new_tol)  # 1e-4)
                docG.getObject(o.Name).Visibility = False
                Part.show(ns)
                ao = App.ActiveDocument.ActiveObject
                docG.ActiveObject.ShapeColor = docG.getObject(
                    o.Name).ShapeColor
                docG.ActiveObject.LineColor = docG.getObject(o.Name).LineColor
                docG.ActiveObject.PointColor = docG.getObject(
                    o.Name).PointColor
                docG.ActiveObject.DiffuseColor = docG.getObject(
                    o.Name).DiffuseColor
                docG.ActiveObject.Transparency = docG.getObject(
                    o.Name).Transparency
                ao.Label = 'Solid'
                i_say(mk_str(ao.Label)+' tolerance = ' +
                      str(ao.Shape.getTolerance(0)))
        else:
            msg = "Select one or more object(s) to be checked!\n"
            reply = QtGui.QMessageBox.information(None, "Warning", msg)
            App.Console.PrintWarning(msg)

        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'setTolerance' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def merge_faces_from_selected_objects_RH(refobj=None):
    """merging Faces of selected shapes"""
    try:
        faces = []
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        App.ActiveDocument.openTransaction(
            translate("Design456", "merge_faces_from_selected_objects_RH"))
        _test = None
        sel = Gui.Selection.getSelection()
        if len(sel):
            for o in sel:
                for f in o.Shape.Faces:
                    if f.Area > 0:
                        faces.append(f)
            # print faces
            try:
                _test = Part.makeShell(faces)
                if _test.isNull():
                    #raise RuntimeError('Failed to create shell')
                    App.Console.PrintWarning('Failed to create shell\n')
            except:
                App.Console.PrintWarning('Failed to create shell\n')
                for f in faces:
                    Part.show(f)
                    doc.ActiveObject.Label = "face"
                return
            if RHDockWidget.ui.checkBox_Refine.isChecked():
                try:
                    _test.removeSplitter()
                except:
                    print('not refined')
            if _test.ShapeType != 'Shell':
                raise RuntimeError('Part object is not a shell')
            _test = Part.Solid(_test)
            if _test.isNull():
                raise RuntimeError('Failed to create solid')
            if RHDockWidget.ui.checkBox_Refine.isChecked():
                try:
                    _test.removeSplitter()
                except:
                    print('not refined')
            if RHDockWidget.ui.checkBox_Refine.isChecked():
                doc.addObject('Part::Feature',
                              'SolidRefined').Shape = _test.removeSplitter()
            else:
                doc.addObject('Part::Feature', 'Solid').Shape = _test

            mysolidr = doc.ActiveObject

            if refobj is not None and hasattr(refobj, 'Name'):
                docG.ActiveObject.ShapeColor = docG.getObject(
                    refobj.Name).ShapeColor
                docG.ActiveObject.LineColor = docG.getObject(
                    refobj.Name).LineColor
                docG.ActiveObject.PointColor = docG.getObject(
                    refobj.Name).PointColor
                docG.ActiveObject.DiffuseColor = docG.getObject(
                    refobj.Name).DiffuseColor
                docG.ActiveObject.Transparency = docG.getObject(
                    refobj.Name).Transparency
            else:
                docG.ActiveObject.ShapeColor = docG.getObject(
                    sel[0].Name).ShapeColor
                docG.ActiveObject.LineColor = docG.getObject(
                    sel[0].Name).LineColor
                docG.ActiveObject.PointColor = docG.getObject(
                    sel[0].Name).PointColor
                docG.ActiveObject.DiffuseColor = docG.getObject(
                    sel[0].Name).DiffuseColor
                docG.ActiveObject.Transparency = docG.getObject(
                    sel[0].Name).Transparency
            if RHDockWidget.ui.checkBox_keep_original.isChecked():
                for o in sel:
                    docG.getObject(o.Name).Visibility = False
            else:
                for o in sel:
                    doc.removeObject(o.Name)

        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'merge_faces_from_selected_objects_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def edges_confirmed_RH():
    try:
        global rh_edges, rh_faces, rh_obj
        global rh_edges_names, rh_faces_names, rh_obj_name
        global created_faces, rh_faces_indexes, rh_edges_to_connect

        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        App.ActiveDocument.openTransaction(
            translate("Design456", "edges_confirmed_RH"))
        en = None
        selEx = Gui.Selection.getSelectionEx()
        if len(selEx):
            for selEdge in selEx:
                for i, e in enumerate(selEdge.SubObjects):

                    if 'Edge' in selEdge.SubElementNames[i]:
                        edge_in_list = False
                        for en in rh_edges_names:
                            if en == selEdge.ObjectName+'.'+selEdge.SubElementNames[i]:
                                edge_in_list = True
                        if not edge_in_list:
                            rh_edges.append(e)
                            rh_edges_names.append(
                                selEdge.ObjectName+'.'+selEdge.SubElementNames[i])
                            rh_obj.append(selEdge.Object)
                            rh_obj_name.append(selEdge.ObjectName)
                            if (e.isClosed()):
                                cf = (Part.Face(Part.Wire(e)))
                                created_faces.append(cf)
                                i_say('face created from closed edge')
                                if RHDockWidget.ui.checkBox_keep_faces.isChecked():

                                    Part.show(cf)
                                    doc.ActiveObject.Label = 'Face'
                                    docG.ActiveObject.Visibility = False
                            else:

                                rh_edges_to_connect.append(e)

            i_say(selEdge.ObjectName)
            if len(rh_edges_to_connect) > 0:
                try:

                    cf = Part.Face(
                        Part.Wire(Part.__sortEdges__(rh_edges_to_connect)))
                    created_faces.append(cf)
                    i_say('face created from open edges')
                    if RHDockWidget.ui.checkBox_keep_faces.isChecked():
                        Part.show(cf)
                        doc.ActiveObject.Label = 'Face'
                        docG.ActiveObject.Visibility = False
                    rh_edges_to_connect = []
                except:
                    i_sayerr("make Face failed")

            if 0:
                try:
                    cf = Part.makeFilledFace(
                        Part.__sortEdges__(rh_edges_to_connect))

                    created_faces.append(cf)
                    if RHDockWidget.ui.checkBox_keep_faces.isChecked():
                        Part.show(Part.makeSolid(Part.makeShell(cf)))
                        docG.ActiveObject.Visibility = False
                    rh_edges_to_connect = []
                except:
                    print('edge outline not closed')
            print('To Do: collect connected edges to create a Wire')
            e_list = ""
            for e in rh_edges_names:
                e_list = e_list+str(e)+'\n'
            RHDockWidget.ui.TE_Edges.setPlainText(e_list)
            RHDockWidget.ui.Edge_Nbr.setText(str(len(rh_edges)))
            unique_obj = set(rh_obj)
            unique_obj_count = len(unique_obj)
            RHDockWidget.ui.Obj_Nbr.setText(str(unique_obj_count))
            for ob in App.ActiveDocument.Objects:
                Gui.Selection.removeSelection(ob)

        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'edges_confirmed_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def faces_confirmed_RH():
    try:
        global rh_edges, rh_faces, rh_obj
        global rh_edges_names, rh_faces_names, rh_obj_name
        global created_faces, rh_faces_indexes, rh_edges_to_connect

        doc = App.ActiveDocument
        App.ActiveDocument.openTransaction(
            translate("Design456", "faces_confirmed_RH"))
        selEx = Gui.Selection.getSelectionEx()

        if len(selEx):
            for selFace in selEx:
                for i, f in enumerate(selFace.SubObjects):

                    if 'Face' in selFace.SubElementNames[i]:
                        face_in_list = False
                        for fn in rh_faces_names:
                            if fn == selFace.ObjectName+'.'+selFace.SubElementNames[i]:
                                face_in_list = True

                        if not face_in_list:
                            rh_faces.append(f)
                            rh_faces_indexes.append(
                                re.search(r'\d+', selFace.SubElementNames[i]).group())
                            rh_faces_names.append(
                                selFace.ObjectName+'.'+selFace.SubElementNames[i])
                            rh_obj.append(selFace.Object)
                            rh_obj_name.append(selFace.ObjectName)

                        print(selFace.ObjectName+'.' +
                              selFace.SubElementNames[i])
            f_list = ""
            for f in rh_faces_names:
                f_list = f_list+str(f)+'\n'
            RHDockWidget.ui.TE_Faces.setPlainText(f_list)

            RHDockWidget.ui.Face_Nbr.setText(str(len(rh_faces)))
            unique_obj = set(rh_obj)
            unique_obj_count = len(unique_obj)
            RHDockWidget.ui.Obj_Nbr_2.setText(str(unique_obj_count))
            for ob in App.ActiveDocument.Objects:
                Gui.Selection.removeSelection(ob)
            App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'faces_confirmed_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def removeHoles_RH():
    try:
        global rh_edges, rh_faces, rh_obj
        global rh_edges_names, rh_faces_names, rh_obj_name
        global created_faces, rh_faces_indexes, rh_edges_to_connect
        global force_recompute, invert
        App.ActiveDocument.openTransaction(
                translate("Design456", "removeHoles_RH"))
        _test = None
        doc=App.ActiveDocument
        docG = Gui.ActiveDocument
        print('Removing Holes')
        unique_obj = set(rh_obj)
        unique_obj_count = len(unique_obj)
        if unique_obj_count == 1:
            RHDockWidget.ui.TE_Edges.setPlainText("")
            RHDockWidget.ui.TE_Faces.setPlainText("")
            myshape = rh_obj[0]
            i = 0
            faces = []
            for f in myshape.Shape.Faces:
                i+=1
                idx_found = False
                for j in rh_faces_indexes:
                    if int(j) == i:
                        idx_found = True
                        print('index found '+str(j))
                if not idx_found:
                    faces.append(f)
            if len(rh_edges_to_connect) > 0:
                if not invert:
                    try:
                        print("try to create a Face w/ OpenSCAD2Dgeom")
                        cf = OpenSCAD2Dgeom.edgestofaces(Part.__sortEdges__(rh_edges_to_connect))
                    except:
                        print("OpenSCAD2Dgeom failed\ntry to makeFilledFace")
                        cf=Part.makeFilledFace(Part.__sortEdges__(rh_edges_to_connect))
                else:
                    try:
                        print("try to makeFilledFace")
                        cf=Part.makeFilledFace(Part.__sortEdges__(rh_edges_to_connect))
                    except:
                        print("makeFilledFace failed\ntry to create a Face w/ OpenSCAD2Dgeom")
                        cf = OpenSCAD2Dgeom.edgestofaces(Part.__sortEdges__(rh_edges_to_connect))
                created_faces.append(cf)
                if RHDockWidget.ui.checkBox_keep_faces.isChecked():
                    #_ = Part.Solid(Part.makeShell([cf]))
                    #doc.addObject('Part::Feature','Face_Solid').Shape = _
                    #doc.ActiveObject.Label = 'Face_Solid'
                    Part.show(cf)
                    doc.ActiveObject.Label = 'Face'
                    docG.ActiveObject.Visibility=False
                rh_edges_to_connect = []
            if 0:
                for f in created_faces:
                    faces.append(f)
                res_faces = []
                _test =  Part.makeShell(faces)
                if _test.isNull(): 
                    raise RuntimeError('Failed to create shell')
            _test =  Part.makeShell(faces)
            if _test.isNull(): 
                raise RuntimeError('Failed to create shell')
                _test=Part.makeSolid(_test)
            if _test.isNull(): 
                raise RuntimeError('Failed to create solid')
            if RHDockWidget.ui.checkBox_Refine.isChecked():
                try:
                    _test.removeSplitter()
                except:
                    print ('not refined')    
            for f in created_faces:
                new_faces = []
                for nf in _test.Faces:
                    new_faces.append(nf)
                new_faces.append(f)
                del _test
                _test =  Part.makeShell(new_faces)
                i_sayw('added 1 face')
                if _test.isNull(): raise RuntimeError('Failed to create shell')
                if RHDockWidget.ui.checkBox_Refine.isChecked():
                    try:
                        _test.removeSplitter()
                    except:
                        print ('not refined')
                if _test.ShapeType != 'Shell': 
                    raise RuntimeError('Part object is not a shell')
                _test=Part.Solid(_test)
                if _test.isNull(): 
                    raise RuntimeError('Failed to create solid')
                if RHDockWidget.ui.checkBox_Refine.isChecked():
                    try:
                        _test.removeSplitter()
                    except:
                        print ('not refined')
            if RHDockWidget.ui.checkBox_Refine.isChecked():
                doc.addObject('Part::Feature','SolidRefined').Shape=_test.removeSplitter()
            else:
                doc.addObject('Part::Feature','Solid').Shape=_test

            mysolidr = doc.ActiveObject
            original_label = myshape.Label
            docG.ActiveObject.ShapeColor=docG.getObject(myshape.Name).ShapeColor
            docG.ActiveObject.LineColor=docG.getObject(myshape.Name).LineColor
            docG.ActiveObject.PointColor=docG.getObject(myshape.Name).PointColor
            docG.ActiveObject.DiffuseColor=docG.getObject(myshape.Name).DiffuseColor
            docG.ActiveObject.Transparency=docG.getObject(myshape.Name).Transparency
            if RHDockWidget.ui.checkBox_keep_original.isChecked():
                docG.getObject(myshape.Name).Visibility=False
            else:
                doc.removeObject(myshape.Name)
            if RHDockWidget.ui.checkBox_Refine.isChecked():
                mysolidr.Label = original_label  
            else:
                mysolidr.Label = original_label
 
            clear_all_RH()
            if force_recompute:
                for obj in App.ActiveDocument.Objects:
                    obj.touch()
            doc.recompute() 
            print('ToDo Apply colors to corresponding faces') 
        else:
            i_sayerr('select only one object')
            
        App.ActiveDocument.commitTransaction()  # undo reg.

    except Exception as err:
        App.Console.PrintError("'removeHoles_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

##


def removeFaces_RH():
    try:
        
        App.ActiveDocument.openTransaction(
            translate("Design456", "removeFaces_RH"))
        global rh_edges, rh_faces, rh_obj
        global rh_edges_names, rh_faces_names, rh_obj_name
        global created_faces, rh_faces_indexes, rh_edges_to_connect
        global force_recompute

        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        print('Removing Holes')

        _test = None
        unique_obj = set(rh_obj)
        unique_obj_count = len(unique_obj)
        if unique_obj_count == 1:  # ToDo manage multi objs faces selection

            myshape = rh_obj[0]
            i = 0
            faces = []
            for f in myshape.Shape.Faces:
                i += 1
                idx_found = False
                for j in rh_faces_indexes:
                    if int(j) == i:
                        idx_found = True
                        print('index found '+str(j))
                if not idx_found:
                    faces.append(f)
            if 1:
                try:
                    _test = Part.makeShell(faces)
                    if _test.isNull():
                        App.Console.PrintWarning('Failed to create shell\n')
                except:
                    App.Console.PrintWarning('Failed to create shell\n')
                    if RHDockWidget.ui.checkBox_keep_faces.isChecked():
                        for f in faces:
                            Part.show(f)
                            doc.ActiveObject.Label = "face"
                    return

                if RHDockWidget.ui.checkBox_Refine.isChecked():
                    try:
                        _test.removeSplitter()
                    except:
                        print('not refined')

                if _test.ShapeType != 'Shell':
                    raise RuntimeError('Part object is not a shell')
                _test = Part.Solid(_test)
                if _test.isNull():
                    raise RuntimeError('Failed to create solid')
                if RHDockWidget.ui.checkBox_Refine.isChecked():
                    try:
                        _test.removeSplitter()
                    except:
                        print('not refined')

                if RHDockWidget.ui.checkBox_Refine.isChecked():
                    doc.addObject('Part::Feature',
                                  'SolidRefined').Shape = _test.removeSplitter()
                else:
                    doc.addObject('Part::Feature', 'Solid').Shape = _test

            mysolidr = doc.ActiveObject
            original_label = myshape.Label
            docG.ActiveObject.ShapeColor = docG.getObject(
                myshape.Name).ShapeColor
            docG.ActiveObject.LineColor = docG.getObject(
                myshape.Name).LineColor
            docG.ActiveObject.PointColor = docG.getObject(
                myshape.Name).PointColor
            docG.ActiveObject.DiffuseColor = docG.getObject(
                myshape.Name).DiffuseColor
            docG.ActiveObject.Transparency = docG.getObject(
                myshape.Name).Transparency
            if RHDockWidget.ui.checkBox_keep_original.isChecked():
                docG.getObject(myshape.Name).Visibility = False
            else:
                doc.removeObject(myshape.Name)
            if RHDockWidget.ui.checkBox_Refine.isChecked():
                mysolidr.Label = original_label  # + "_refined"
            else:
                mysolidr.Label = original_label

            clear_all_RH()
            if force_recompute:
                for obj in App.ActiveDocument.Objects:
                    obj.touch()
            doc.recompute()
        print('ToDo Apply colors to corresponding faces')
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'removeFaces_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def addFaces_RH():
    try:
        App.ActiveDocument.openTransaction(
            translate("Design456", "addFaces_RH"))
        global rh_edges, rh_faces, rh_obj
        global rh_edges_names, rh_faces_names, rh_obj_name
        global created_faces, rh_faces_indexes, rh_edges_to_connect
        global force_recompute, invert

        doc = App.ActiveDocument
        docG = Gui.ActiveDocument

        if len(rh_edges) > 0:

            if not invert:
                try:
                    print("try to create a Face w/ OpenSCAD2Dgeom")
                    cf = OpenSCAD2Dgeom.edgestofaces(rh_edges)
                except:
                    print("OpenSCAD2Dgeom failed\ntry to makeFilledFace")
                    cf = Part.makeFilledFace(Part.__sortEdges__(rh_edges))
            else:
                try:
                    print("try to makeFilledFace")
                    cf = Part.makeFilledFace(Part.__sortEdges__(rh_edges))
                except:
                    print(
                        "makeFilledFace failed\ntry to create a Face w/ OpenSCAD2Dgeom")
                    cf = OpenSCAD2Dgeom.edgestofaces(rh_edges)

            Part.show(cf)
            doc.ActiveObject.Label = "Face"

        if len(rh_edges) > 0 or len(rh_edges_to_connect) > 0:
            clear_all_RH()
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'addFaces_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def offsetFaces_RH():
    try:
        App.ActiveDocument.openTransaction(
            translate("Design456", "offsetFaces_RH"))
        global rh_edges, rh_faces, rh_obj
        global rh_edges_names, rh_faces_names, rh_obj_name
        global created_faces, rh_faces_indexes, rh_edges_to_connect
        global force_recompute, invert

        doc = App.ActiveDocument
        docG = Gui.ActiveDocument

        if len(rh_faces) > 0:
            for f in rh_faces:
                Part.show(f)
                fname = doc.ActiveObject.Name
                s = doc.ActiveObject.Shape.copy()
                offset_dir = RHDockWidget.ui.offset_input.text().split(':')
                if len(offset_dir) > 1:
                    offset = float(offset_dir[0])
                    if 'x' in offset_dir[1]:
                        norm = App.Vector(1, 0, 0)
                    elif 'y' in offset_dir[1]:
                        norm = App.Vector(0, 1, 0)
                    elif 'z' in offset_dir[1]:
                        norm = App.Vector(0, 0, 1)
                    elif 'n' in offset_dir[1]:
                        norm = f.normalAt(0, 0)
                    else:
                        i_sayerr('direction not inserted, using norm to face')
                        norm = f.normalAt(0, 0)
                        RHDockWidget.ui.offset_input.setText(str(offset)+':n')
                else:
                    offset = float(RHDockWidget.ui.offset_input.text())
                    i_sayerr('direction not inserted, using norm to face')
                    norm = f.normalAt(0, 0)
                    RHDockWidget.ui.offset_input.setText(str(offset)+':n')
                s.translate(norm*offset)
                doc.removeObject(fname)
                Part.show(s)
                doc.ActiveObject.Label = "Face"
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'offsetFaces_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def offsetEdges_RH():
    try:
        App.ActiveDocument.openTransaction(
            translate("Design456", "offsetEdges_RH"))
        global rh_edges, rh_faces, rh_obj
        global rh_edges_names, rh_faces_names, rh_obj_name
        global created_faces, rh_faces_indexes, rh_edges_to_connect
        global force_recompute, invert

        doc = App.ActiveDocument
        docG = Gui.ActiveDocument

        if len(rh_edges) > 0:
            for e in rh_edges:
                Part.show(e)

                offset_dir = RHDockWidget.ui.offset_input.text().split(':')
                if len(offset_dir) > 1:
                    offset = float(offset_dir[0])
                    if 'x' in offset_dir[1]:
                        norm = App.Vector(1, 0, 0)
                    elif 'y' in offset_dir[1]:
                        norm = App.Vector(0, 1, 0)
                    elif 'z' in offset_dir[1]:
                        norm = App.Vector(0, 0, 1)
                    else:
                        i_sayerr('direction not inserted, using z axis')
                        norm = App.Vector(0, 0, 1)
                else:
                    offset = float(RHDockWidget.ui.offset_input.text())
                    i_sayerr('direction not inserted, using z axis')
                    norm = App.Vector(0, 0, 1)
                    RHDockWidget.ui.offset_input.setText(str(offset)+':x')
                fname = doc.ActiveObject.Name
                s = doc.ActiveObject.Shape.copy()
                s.translate(norm*offset)
                doc.removeObject(fname)
                Part.show(s)
                doc.ActiveObject.Label = "Edge"
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'offsetEdges_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def copyFaces_RH():
    global rh_edges, rh_faces, rh_obj
    global rh_edges_names, rh_faces_names, rh_obj_name
    global created_faces, rh_faces_indexes, rh_edges_to_connect
    global force_recompute, invert

    doc = App.ActiveDocument
    docG = Gui.ActiveDocument

    if len(rh_faces) > 0:
        for f in rh_faces:
            Part.show(f)
            doc.ActiveObject.Label = "Face"

    if len(rh_faces) > 0:
        clear_all_RH()
##


def removesubtree(objs):
    try:
        App.ActiveDocument.openTransaction(
            translate("Design456", "removesubtree"))

        def addsubobjs(obj, toremoveset):
            toremove.add(obj)
            for subobj in obj.OutList:
                addsubobjs(subobj, toremoveset)

        toremove = set()
        for obj in objs:
            addsubobjs(obj, toremove)
        checkinlistcomplete = False
        while not checkinlistcomplete:
            for obj in toremove:
                if (obj not in objs) and (frozenset(obj.InList) - toremove):
                    toremove.remove(obj)
                    break
            else:
                checkinlistcomplete = True
        for obj in toremove:
            try:
                obj.Document.removeObject(obj.Name)
            except:
                pass
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'removesubtree' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
###


def cleaningFaces_RH():
    """merge two faces"""
    try:
        
        App.ActiveDocument.openTransaction(
            translate("Design456", "cleaningFaces_RH"))
        global force_recompute, invert
        myshape = None
        i_sayw('merging faces')
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        selEx = Gui.Selection.getSelectionEx()
        fcs = []
        fcs_names = []
        fcs_outW = []
        fcs_indexes = []
        new_faces = []
        _test = None
        o = None

        if len(selEx) > 0:
            for selobj in selEx:
                for i, f in enumerate(selobj.SubObjects):
                    if 'Face' in selobj.SubElementNames[i]:
                        fcs.append(f)
                        fcs_names.append(selobj.SubElementNames[i])
                        fcs_indexes.append(
                            re.search(r'\d+', selobj.SubElementNames[i]).group())
                        fcs_outW.append(f.OuterWire)
                        print(selobj.SubElementNames[i])

            if len(fcs) > 1:
                sps = []
                for w in fcs_outW:
                    s = w.copy()
                    obj = App.ActiveDocument.addObject(
                        'Part::Feature', "Shape")
                    # Part.show(s)
                    obj.Shape = s
                    sps.append(obj)

                wf = doc.addObject("Part::MultiFuse", "Wfuse")
                # wf=doc.ActiveObject
                obj.Shapes = sps
                wc = doc.addObject("Part::MultiCommon", "Wcommon")
                # wc=doc.ActiveObject
                wc.Shapes = sps
                wct = doc.addObject("Part::Cut", "Wcut")
                # wct=doc.ActiveObject
                wct.Base = wf
                wct.Tool = wc
                doc.recompute()
                i_say('outer wire created')

                if not invert:
                    try:
                        print("try to create a Face w/ OpenSCAD2Dgeom")
                        cf = OpenSCAD2Dgeom.edgestofaces((wct.Shape.Edges))
                    except:
                        print("OpenSCAD2Dgeom failed\ntry to makeFilledFace")
                        cf = Part.makeFilledFace(
                            Part.__sortEdges__(wct.Shape.Edges))
                else:
                    try:
                        print("try to makeFilledFace")
                        cf = Part.makeFilledFace(
                            Part.__sortEdges__(wct.Shape.Edges))
                    except:
                        print(
                            "makeFilledFace failed\ntry to create a Face w/ OpenSCAD2Dgeom")
                        cf = OpenSCAD2Dgeom.edgestofaces((wct.Shape.Edges))

                w = cf.Faces[0].OuterWire
                removesubtree([wct])
                if not invert:
                    try:
                        print("try to create a Face w/ OpenSCAD2Dgeom")
                        cf2 = OpenSCAD2Dgeom.edgestofaces((w.Edges))
                    except:
                        print("OpenSCAD2Dgeom failed\ntry to makeFilledFace")
                        cf2 = Part.makeFilledFace(Part.__sortEdges__(w.Edges))
                else:
                    try:
                        print("try to makeFilledFace")
                        cf2 = Part.makeFilledFace(Part.__sortEdges__(w.Edges))
                    except:
                        print(
                            "makeFilledFace failed\ntry to create a Face w/ OpenSCAD2Dgeom")
                        cf2 = OpenSCAD2Dgeom.edgestofaces((w.Edges))

                Part.show(cf2)
                new_faces.append(doc.ActiveObject)
            elif len(fcs) == 1:
                w = fcs[0].OuterWire
                s = w.copy()
                sw = App.ActiveDocument.addObject('Part::Feature', "Shape")
                sw.Shape = s
                # sw=(doc.ActiveObject)
                o = doc.addObject("Part::Face", "Face")
                o.Sources = (sw, )
                doc.recompute()
                # o=doc.ActiveObject
                newObj = doc.addObject('Part::Feature', 'face')
                newObj.Shape = o.Shape
                new_faces.append(newObj)
                removesubtree([o])

            else:
                print('Error')
            doc.ActiveObject.Label = "Face"
            doc.recompute()
            if len(selEx) == 1:
                myshape = selEx[0].Object
                i = 0
                faces = []
                for f in myshape.Shape.Faces:
                    i += 1
                    idx_found = False
                    for j in fcs_indexes:
                        if int(j) == i:
                            idx_found = True
                            print('index found '+str(j))
                    if not idx_found:
                        faces.append(f)
                try:
                    _test = Part.makeShell(faces)
                    if _test.isNull():
                        App.Console.PrintWarning('Failed to create shell\n')
                except:
                    App.Console.PrintWarning('Failed to create shell\n')
                    if RHDockWidget.ui.checkBox_keep_faces.isChecked():
                        for f in faces:
                            newObj = App.ActiveDocument.addObject(
                                'Part::Feature', "Face")
                            newObj.Shape = f
                            newObj.Label = "face"
                    App.ActiveDocument.recompute()
                    return

                if RHDockWidget.ui.checkBox_Refine.isChecked():
                    try:
                        _test.removeSplitter()
                    except:
                        print('not refined')
                if _test.ShapeType != 'Shell':
                    raise RuntimeError('Part object is not a shell')
                _test = Part.Solid(_test)
                if _test.isNull():
                    raise RuntimeError('Failed to create solid')
                if RHDockWidget.ui.checkBox_Refine.isChecked():
                    try:
                        _test.removeSplitter()
                    except:
                        print('not refined')
                newObj = None
                if RHDockWidget.ui.checkBox_Refine.isChecked():
                    newObj = doc.addObject('Part::Feature', 'SolidRefined')
                    newObj.Shape = _test.removeSplitter()
                else:
                    newObj = doc.addObject('Part::Feature', 'Solid')
                    newObj.Shape = _test
                mysolidr = newObj
                original_label = myshape.Label
                docG.ActiveObject.ShapeColor = docG.getObject(
                    myshape.Name).ShapeColor
                docG.ActiveObject.LineColor = docG.getObject(
                    myshape.Name).LineColor
                docG.ActiveObject.PointColor = docG.getObject(
                    myshape.Name).PointColor
                docG.ActiveObject.DiffuseColor = docG.getObject(
                    myshape.Name).DiffuseColor
                docG.ActiveObject.Transparency = docG.getObject(
                    myshape.Name).Transparency
                if RHDockWidget.ui.checkBox_keep_original.isChecked():
                    docG.getObject(myshape.Name).Visibility = False
                else:
                    doc.removeObject(myshape.Name)
                if RHDockWidget.ui.checkBox_Refine.isChecked():
                    mysolidr.Label = original_label  # + "_refined"
                Gui.Selection.addSelection(mysolidr)
                for fn in new_faces:
                    Gui.Selection.addSelection(fn)
            Gui.Selection.removeSelection(myshape)
            merge_faces_from_selected_objects_RH(myshape)
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'cleaningFaces_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def makeEdge_RH():
    try:
        App.ActiveDocument.openTransaction(
            translate("Design456", "makeEdge_RH"))
        global force_recompute
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        verts = []
        verts_names = []
        selEx = Gui.Selection.getSelectionEx()
        verts = []
        if len(selEx):
            for selV in selEx:
                for i, v in enumerate(selV.SubObjects):

                    if 'Vertex' in selV.SubElementNames[i]:
                        verts.append(v)
                        verts_names.append(selV.SubElementNames[i])
                        print(selV.SubElementNames[i])
        if len(verts) == 2:
            try:
                i_say("try to create an Edge w/ makeLine")
                ce = Part.makeLine(verts[0].Point, verts[1].Point)
                Part.show(ce)
                del ce
                doc.ActiveObject.Label = "Edge"
            except:
                i_sayerr("failed to create a Line")
        else:
            i_sayerr("select only 2 Vertexes")
        for ob in App.ActiveDocument.Objects:
            Gui.Selection.removeSelection(ob)
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'makeEdge_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def addEdges_RH():
    try:
        App.ActiveDocument.openTransaction(
            translate("Design456", "addEdges_RH"))
        global rh_edges, rh_faces, rh_obj
        global rh_edges_names, rh_faces_names, rh_obj_name
        global created_faces, rh_faces_indexes, rh_edges_to_connect
        global force_recompute
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument

        ae_edges = rh_edges
        ae_edges_names = rh_edges_names
        selEx = Gui.Selection.getSelectionEx()
        if len(selEx):
            for selEdge in selEx:
                for i, e in enumerate(selEdge.SubObjects):
                    if 'Edge' in selEdge.SubElementNames[i]:
                        ae_edges.append(e)
                        ae_edges_names.append(selEdge.SubElementNames[i])
                        print(selEdge.SubElementNames[i])
        if len(ae_edges) > 0:

            if not invert:
                try:
                    print("try to create an Edge w/ OpenSCAD2Dgeom")
                    ce = Part.Wire(OpenSCAD2Dgeom.edgestowires(ae_edges))

                except:
                    print("OpenSCAD2Dgeom failed\ntry to makeWire")
                    ce = Part.Wire(Part.__sortEdges__(ae_edges))

            else:
                try:
                    print("try to makeWire")
                    ce = Part.Wire(Part.__sortEdges__(ae_edges))
                except:
                    print("makeWire failed\ntry to create an Edge w/ OpenSCAD2Dgeom")
                    ce = OpenSCAD2Dgeom.edgestofaces(ae_edges)
            # created_faces.append(cf)
            Part.show(ce)
            doc.ActiveObject.Label = "Edge"
            if len(rh_edges) > 0:
                clear_all_RH()
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:
        App.Console.PrintError("'addEdges_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def showEdges_RH():
    global rh_edges, rh_faces, rh_obj
    global rh_edges_names, rh_faces_names, rh_obj_name
    global created_faces, rh_faces_indexes, rh_edges_to_connect
    global force_recompute
    doc = App.ActiveDocument
    docG = Gui.ActiveDocument

    for en in rh_edges_names:
        Gui.Selection.addSelection(doc.getObject(
            en.split('.')[0]), en.split('.')[1])

##


def showFaces_RH():
    global rh_edges, rh_faces, rh_obj
    global rh_edges_names, rh_faces_names, rh_obj_name
    global created_faces, rh_faces_indexes, rh_edges_to_connect
    global force_recompute
    doc = App.ActiveDocument
    docG = Gui.ActiveDocument

    for fn in rh_faces_names:
        Gui.Selection.addSelection(doc.getObject(
            fn.split('.')[0]), fn.split('.')[1])

##


def PartDefeaturing_RH():
    try:
        # pass
        global rh_edges, rh_faces, rh_obj
        global rh_edges_names, rh_faces_names, rh_obj_name
        global created_faces, rh_faces_indexes, rh_edges_to_connect
        global force_recompute
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument

        import Part
        import DefeaturingFeature
        unique_obj = set(rh_obj)
        unique_obj_count = len(unique_obj)

        # ToDo manage multi objs faces selection
        if unique_obj_count == 1 and len(rh_faces) > 0:
            newobj = doc.addObject("Part::FeaturePython", 'defeat')
            DefeaturingFeature.DefeatShape(rh_faces_names, newobj, rh_obj[0])
            DefeaturingFeature.ViewProviderTree(newobj.ViewObject)
            newobj.Label = 'defeat_%s' % rh_obj[0].Label
            rh_obj[0].ViewObject.hide()
            App.ActiveDocument.recompute()

        def GetResources(self):
            return {'Pixmap': os.path.join(DefeaturingWB_icons_path, 'DefeaturingParametric.svg'), 'MenuText':
                    QtCore.QT_TRANSLATE_NOOP('DefeatShapeFeature',
                    'Defeat Shape Feature'), 'ToolTip':
                    QtCore.QT_TRANSLATE_NOOP('DefeatShapeFeature',
                    'Create Defeat Shape Parametric Feature')}
    except Exception as err:

        App.Console.PrintError("'PartDefeaturing_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def makeSolidExpSTEP_RH():
    try:
        App.ActiveDocument.openTransaction(
            translate("Design456", "makeSolidExpSTEP_RH"))
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        if doc is not None:
            fname = doc.FileName
            if len(fname) == 0:
                fname = 'untitled'
            tempdir = tempfile.gettempdir()  # get the current temporary directory
            tempfilepath = os.path.join(tempdir, fname + u'.stp')
            sel = Gui.Selection.getSelection()
            if len(sel) == 1:
                __objs__ = []
                __objs__.append(sel[0])
                import ImportGui
                ImportGui.export(__objs__, tempfilepath)
                del __objs__
                docG.getObject(sel[0].Name).Visibility = False
                ImportGui.insert(tempfilepath, doc.Name)
                Gui.SendMsgToActiveView("ViewFit")
            else:
                i_sayerr('select only one object')
        else:
            i_sayerr('select only one object')
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:

        App.Console.PrintError("'makeSolidExpSTEP_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def shape_Connect_RH():
    try:
        App.ActiveDocument.openTransaction(
            translate("Design456", "shape_Connect_RH"))
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        sel = Gui.Selection.getSelection()
        if len(sel) == 1:
            import PartGui
            from PartGui import BOPTools
            j = BOPTools.JoinFeatures.makeConnect(name='Connect')
            j.Objects = [sel[0]]
            j.Proxy.execute(j)
            j.purgeTouched()
            connected_obj = doc.ActiveObject
            connected_objG = docG.ActiveObject
            for obj in j.ViewObject.Proxy.claimChildren():
                obj.ViewObject.hide()
                connected_objG.ShapeColor = docG.getObject(obj.Name).ShapeColor
                connected_objG.LineColor = docG.getObject(obj.Name).LineColor
                connected_objG.PointColor = docG.getObject(obj.Name).PointColor
                connected_objG.DiffuseColor = docG.getObject(
                    obj.Name).DiffuseColor
                connected_objG.Transparency = docG.getObject(
                    obj.Name).Transparency
        else:
            i_sayerr('select only one object')
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:

        App.Console.PrintError("'shape_Connect_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def simplecopy_RH():
    try:
        App.ActiveDocument.openTransaction(
            translate("Design456", "simplecopy_RH"))
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        sel = Gui.Selection.getSelection()
        if len(sel):
            for o in sel:
                if hasattr(o, "Shape"):
                    # .removeSplitter()
                    doc.addObject('Part::Feature', 'Copy').Shape = o.Shape
                    doc.ActiveObject.Label = o.Label
                    docG.getObject(o.Name).hide()
                    docG.ActiveObject.ShapeColor = docG.getObject(
                        o.Name).ShapeColor
                    docG.ActiveObject.LineColor = docG.getObject(
                        o.Name).LineColor
                    docG.ActiveObject.PointColor = docG.getObject(
                        o.Name).PointColor
                    docG.ActiveObject.DiffuseColor = docG.getObject(
                        o.Name).DiffuseColor
                    docG.ActiveObject.Transparency = docG.getObject(
                        o.Name).Transparency
                    doc.recompute()
        else:
            i_sayerr('select object(s) with a Shape')
        App.ActiveDocument.commitTransaction()  # undo reg.
    except Exception as err:

        App.Console.PrintError("'simplecopy_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
##


def loop_edges_RH():
    try:
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        sl = Gui.Selection.getSelection()
        if len(sl) > 0:
            sel = Gui.Selection.getSelectionEx()[0]
            obj = sel.Object
            edge1 = sel.SubObjects[0]
            if 'Face' in sel.SubElementNames[0]:
                loop = horizontalFaceLoop(
                    sel.Object, sel.SubObjects[0], sel.SubElementNames)
                if loop:
                    Gui.Selection.clearSelection()
                    Gui.Selection.addSelection(sel.Object, loop)
                loopwire = []
            elif len(sel.SubObjects) == 1:
                loopwire = horizontalEdgeLoop(obj, edge1)
            else:
                edge2 = sel.SubObjects[1]
                loopwire = loopdetect(obj, edge1, edge2)

            if loopwire:
                Gui.Selection.clearSelection()
                elist = obj.Shape.Edges
                for e in elist:
                    for i in loopwire.Edges:
                        if e.hashCode() == i.hashCode():
                            Gui.Selection.addSelection(
                                obj, "Edge"+str(elist.index(e)+1))
    except Exception as err:

        App.Console.PrintError("'loop_edges_RH' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


# import the image data. /Mariwan


class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(260, 534)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons-new/Center-Align.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DockWidget.setWindowIcon(icon)
        DockWidget.setToolTip("Defeaturing tools")
        DockWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        DockWidget.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        DockWidget.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        DockWidget.setWindowTitle("Defeaturing Tools")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.PB_RHoles = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_RHoles.setGeometry(QtCore.QRect(12, 288, 32, 32))
        self.PB_RHoles.setToolTip("remove Hole from Face")
        self.PB_RHoles.setText("")
        self.PB_RHoles.setObjectName("PB_RHoles")
        self.PB_Edges = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_Edges.setGeometry(QtCore.QRect(220, 20, 32, 32))
        self.PB_Edges.setToolTip("add selected Edges to List")
        self.PB_Edges.setText("")
        self.PB_Edges.setObjectName("PB_Edges")
        self.TE_Faces = QtGui.QPlainTextEdit(self.dockWidgetContents)
        self.TE_Faces.setGeometry(QtCore.QRect(24, 164, 190, 71))
        self.TE_Faces.setToolTip("List of Face(s)")
        self.TE_Faces.setObjectName("TE_Faces")
        self.checkBox_keep_original = QtGui.QCheckBox(self.dockWidgetContents)
        self.checkBox_keep_original.setGeometry(
            QtCore.QRect(124, 252, 110, 33))
        self.checkBox_keep_original.setToolTip("keep the original object")
        self.checkBox_keep_original.setText("keep Object")
        self.checkBox_keep_original.setChecked(True)
        self.checkBox_keep_original.setObjectName("checkBox_keep_original")
        self.InfoLabel = QtGui.QLabel(self.dockWidgetContents)
        self.InfoLabel.setGeometry(QtCore.QRect(24, 0, 196, 36))
        self.InfoLabel.setText("Select Edge(s)\n"
                               "Ctrl+Click")
        self.InfoLabel.setObjectName("InfoLabel")
        self.TE_Edges = QtGui.QPlainTextEdit(self.dockWidgetContents)
        self.TE_Edges.setEnabled(True)
        self.TE_Edges.setGeometry(QtCore.QRect(24, 36, 190, 66))
        self.TE_Edges.setToolTip("List of Edge(s)")
        self.TE_Edges.setPlainText("")
        self.TE_Edges.setObjectName("TE_Edges")
        self.PB_Faces = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_Faces.setGeometry(QtCore.QRect(220, 164, 32, 32))
        self.PB_Faces.setToolTip("add selected Faces to List")
        self.PB_Faces.setText("")
        self.PB_Faces.setObjectName("PB_Faces")
        self.PB_Edges_Clear = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_Edges_Clear.setGeometry(QtCore.QRect(220, 92, 32, 32))
        self.PB_Edges_Clear.setToolTip("clear List")
        self.PB_Edges_Clear.setText("")
        self.PB_Edges_Clear.setObjectName("PB_Edges_Clear")
        self.PB_Faces_Clear = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_Faces_Clear.setGeometry(QtCore.QRect(220, 200, 32, 32))
        self.PB_Faces_Clear.setToolTip("clear List")
        self.PB_Faces_Clear.setText("")
        self.PB_Faces_Clear.setObjectName("PB_Faces_Clear")
        self.Edge_Nbr = QtGui.QLabel(self.dockWidgetContents)
        self.Edge_Nbr.setGeometry(QtCore.QRect(48, 104, 53, 16))
        self.Edge_Nbr.setText("0")
        self.Edge_Nbr.setObjectName("Edge_Nbr")
        self.Face_Nbr = QtGui.QLabel(self.dockWidgetContents)
        self.Face_Nbr.setGeometry(QtCore.QRect(48, 236, 53, 16))
        self.Face_Nbr.setText("0")
        self.Face_Nbr.setObjectName("Face_Nbr")
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setGeometry(QtCore.QRect(24, 124, 177, 45))
        self.label.setText("Select Face(s)\n"
                           "Ctrl+Click")
        self.label.setObjectName("label")
        self.checkBox_Refine = QtGui.QCheckBox(self.dockWidgetContents)
        self.checkBox_Refine.setGeometry(QtCore.QRect(12, 260, 89, 20))
        self.checkBox_Refine.setToolTip("refine the resulting solid\n"
                                        "after the operation ")
        self.checkBox_Refine.setText("refine")
        self.checkBox_Refine.setChecked(False)
        self.checkBox_Refine.setObjectName("checkBox_Refine")
        self.checkBox_keep_faces = QtGui.QCheckBox(self.dockWidgetContents)
        self.checkBox_keep_faces.setGeometry(QtCore.QRect(128, 140, 100, 20))
        self.checkBox_keep_faces.setToolTip("keep construction faces")
        self.checkBox_keep_faces.setText("keep faces")
        self.checkBox_keep_faces.setObjectName("checkBox_keep_faces")
        self.PB_RFaces = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_RFaces.setGeometry(QtCore.QRect(68, 288, 32, 32))
        self.PB_RFaces.setToolTip("remove \'in List\' Faces")
        self.PB_RFaces.setText("")
        self.PB_RFaces.setObjectName("PB_RFaces")
        self.PB_AFaces = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_AFaces.setGeometry(QtCore.QRect(124, 288, 32, 32))
        self.PB_AFaces.setToolTip("add Faces from \'in List\' Edges")
        self.PB_AFaces.setText("")
        self.PB_AFaces.setObjectName("PB_AFaces")
        self.PB_makeShell = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_makeShell.setGeometry(QtCore.QRect(12, 360, 32, 32))
        self.PB_makeShell.setToolTip("make Solid from in list Faces")
        self.PB_makeShell.setText("")
        self.PB_makeShell.setObjectName("PB_makeShell")
        self.PB_makeShell_2 = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_makeShell_2.setGeometry(QtCore.QRect(68, 360, 32, 32))
        self.PB_makeShell_2.setToolTip("make Solid from the Faces\n"
                                       "of the selected Objects")
        self.PB_makeShell_2.setText("")
        self.PB_makeShell_2.setObjectName("PB_makeShell_2")
        self.PB_check_TypeId = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_check_TypeId.setGeometry(QtCore.QRect(124, 468, 32, 32))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setItalic(False)
        font.setUnderline(False)
        font.setBold(False)
        self.PB_check_TypeId.setFont(font)
        self.PB_check_TypeId.setToolTip("show/hide TypeId of the Shape")
        self.PB_check_TypeId.setText("")
        self.PB_check_TypeId.setObjectName("PB_check_TypeId")
        self.Obj_Nbr = QtGui.QLabel(self.dockWidgetContents)
        self.Obj_Nbr.setGeometry(QtCore.QRect(164, 104, 53, 16))
        self.Obj_Nbr.setText("0")
        self.Obj_Nbr.setObjectName("Obj_Nbr")
        self.Obj_Nbr_2 = QtGui.QLabel(self.dockWidgetContents)
        self.Obj_Nbr_2.setGeometry(QtCore.QRect(164, 236, 53, 16))
        self.Obj_Nbr_2.setText("0")
        self.Obj_Nbr_2.setObjectName("Obj_Nbr_2")
        self.PB_AEdges = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_AEdges.setGeometry(QtCore.QRect(220, 288, 32, 32))
        self.PB_AEdges.setToolTip("create a copy of the \'in List\' Edges")
        self.PB_AEdges.setText("")
        self.PB_AEdges.setObjectName("PB_AEdges")
        self.PB_showEdgeList = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_showEdgeList.setGeometry(QtCore.QRect(12, 396, 32, 32))
        self.PB_showEdgeList.setToolTip("show \'in List\' Edge(s)")
        self.PB_showEdgeList.setText("")
        self.PB_showEdgeList.setObjectName("PB_showEdgeList")
        self.PB_showFaceList = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_showFaceList.setGeometry(QtCore.QRect(68, 396, 32, 32))
        self.PB_showFaceList.setToolTip("show \'in List\' Face(s)")
        self.PB_showFaceList.setText("")
        self.PB_showFaceList.setObjectName("PB_showFaceList")
        self.PB_Refine = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_Refine.setGeometry(QtCore.QRect(124, 396, 32, 32))
        self.PB_Refine.setToolTip("refine")
        self.PB_Refine.setText("")
        self.PB_Refine.setObjectName("PB_Refine")
        self.PB_RefineParametric = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_RefineParametric.setGeometry(QtCore.QRect(220, 396, 32, 32))
        self.PB_RefineParametric.setToolTip("parametric Refine")
        self.PB_RefineParametric.setText("")
        self.PB_RefineParametric.setObjectName("PB_RefineParametric")
        self.PB_CFaces = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_CFaces.setGeometry(QtCore.QRect(12, 324, 32, 32))
        self.PB_CFaces.setToolTip("copy Faces from \'in List\' Edges")
        self.PB_CFaces.setText("")
        self.PB_CFaces.setObjectName("PB_CFaces")
        self.PB_TFace = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_TFace.setGeometry(QtCore.QRect(68, 324, 32, 32))
        self.PB_TFace.setToolTip("copy Faces from \'in List\' Edges")
        self.PB_TFace.setText("")
        self.PB_TFace.setObjectName("PB_TFace")
        self.offset_input = QtGui.QLineEdit(self.dockWidgetContents)
        self.offset_input.setGeometry(QtCore.QRect(128, 328, 73, 22))
        self.offset_input.setToolTip("Face offset to apply")
        self.offset_input.setText("0.0")
        self.offset_input.setObjectName("offset_input")
        self.PB_TEdge = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_TEdge.setGeometry(QtCore.QRect(220, 324, 32, 32))
        self.PB_TEdge.setToolTip("copy Faces from \'in List\' Edges")
        self.PB_TEdge.setText("")
        self.PB_TEdge.setObjectName("PB_TEdge")
        self.PB_close = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_close.setGeometry(QtCore.QRect(-1, -1, 20, 20))
        self.PB_close.setToolTip("add selected Edges to List")
        self.PB_close.setText("")
        self.PB_close.setObjectName("PB_close")
        self.Version = QtGui.QLabel(self.dockWidgetContents)
        self.Version.setGeometry(QtCore.QRect(200, 0, 53, 16))
        self.Version.setText("0")
        self.Version.setObjectName("Version")
        self.PB_left = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_left.setGeometry(QtCore.QRect(-1, 17, 20, 20))
        self.PB_left.setToolTip("dock left")
        self.PB_left.setText("")
        self.PB_left.setObjectName("PB_left")
        self.PB_right = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_right.setGeometry(QtCore.QRect(-1, 34, 20, 20))
        self.PB_right.setToolTip("dock right")
        self.PB_right.setText("")
        self.PB_right.setObjectName("PB_right")
        self.PB_makeEdge = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_makeEdge.setGeometry(QtCore.QRect(12, 468, 32, 32))
        self.PB_makeEdge.setToolTip("make Edge from selected Vertexes")
        self.PB_makeEdge.setText("")
        self.PB_makeEdge.setObjectName("PB_makeEdge")
        self.PB_expSTEP = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_expSTEP.setGeometry(QtCore.QRect(124, 360, 32, 32))
        self.PB_expSTEP.setToolTip("make Solid from the Faces\n"
                                   "of the selected Objects")
        self.PB_expSTEP.setText("")
        self.PB_expSTEP.setObjectName("PB_expSTEP")
        self.PB_PartDefeaturing = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_PartDefeaturing.setEnabled(False)
        self.PB_PartDefeaturing.setGeometry(QtCore.QRect(172, 288, 32, 32))
        self.PB_PartDefeaturing.setToolTip("show \'in List\' Edge(s)")
        self.PB_PartDefeaturing.setText("")
        self.PB_PartDefeaturing.setObjectName("PB_PartDefeaturing")
        self.PB_CleaningFaces = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_CleaningFaces.setGeometry(QtCore.QRect(220, 360, 32, 32))
        self.PB_CleaningFaces.setToolTip("clean Face(s) removing\n"
                                         "holes and merging Outwire")
        self.PB_CleaningFaces.setText("")
        self.PB_CleaningFaces.setObjectName("PB_CleaningFaces")
        self.PB_checkS = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_checkS.setGeometry(QtCore.QRect(12, 432, 32, 32))
        self.PB_checkS.setToolTip("show \'in List\' Edge(s)")
        self.PB_checkS.setText("")
        self.PB_checkS.setObjectName("PB_checkS")
        self.tolerance_value = QtGui.QLineEdit(self.dockWidgetContents)
        self.tolerance_value.setGeometry(QtCore.QRect(128, 436, 73, 22))
        self.tolerance_value.setToolTip("Face offset to apply")
        self.tolerance_value.setText("0.0")
        self.tolerance_value.setObjectName("tolerance_value")
        self.PB_setTol = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_setTol.setGeometry(QtCore.QRect(220, 432, 32, 32))
        self.PB_setTol.setToolTip("copy Faces from \'in List\' Edges")
        self.PB_setTol.setText("")
        self.PB_setTol.setObjectName("PB_setTol")
        self.PB_getTol = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_getTol.setGeometry(QtCore.QRect(68, 432, 32, 32))
        self.PB_getTol.setToolTip("copy Faces from \'in List\' Edges")
        self.PB_getTol.setText("")
        self.PB_getTol.setObjectName("PB_getTol")
        self.PB_sewS = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_sewS.setGeometry(QtCore.QRect(220, 468, 32, 32))
        self.PB_sewS.setToolTip("copy Faces from \'in List\' Edges")
        self.PB_sewS.setText("")
        self.PB_sewS.setObjectName("PB_sewS")
        self.PB_RHhelp = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_RHhelp.setGeometry(QtCore.QRect(172, 468, 32, 32))
        self.PB_RHhelp.setToolTip("Help")
        self.PB_RHhelp.setText("")
        self.PB_RHhelp.setObjectName("PB_RHhelp")
        self.PB_Connect = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_Connect.setGeometry(QtCore.QRect(172, 360, 32, 32))
        self.PB_Connect.setToolTip("connect")
        self.PB_Connect.setText("")
        self.PB_Connect.setObjectName("PB_Connect")
        self.PB_SimpleCopy = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_SimpleCopy.setGeometry(QtCore.QRect(172, 396, 32, 32))
        self.PB_SimpleCopy.setToolTip("simple copy")
        self.PB_SimpleCopy.setText("")
        self.PB_SimpleCopy.setObjectName("PB_SimpleCopy")

        self.PB_LoopEdge = QtGui.QPushButton(self.dockWidgetContents)
        self.PB_LoopEdge.setGeometry(QtCore.QRect(220, 56, 32, 32))
        self.PB_LoopEdge.setToolTip("add Loop Edges to List")
        self.PB_LoopEdge.setText("")
        self.PB_LoopEdge.setObjectName("PB_LoopEdge")
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

################################################################################################

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(copy_edges_b64))
        self.PB_AEdges.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_AEdges.setIcon(QtGui.QIcon(pm))
        self.PB_AEdges.clicked.connect(addEdges_RH)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(mk_solid1_b64))
        self.PB_makeShell.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_makeShell.setIcon(QtGui.QIcon(pm))
        self.PB_makeShell.clicked.connect(merge_selected_faces_RH)
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(mk_solid2_b64))
        self.PB_makeShell_2.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_makeShell_2.setIcon(QtGui.QIcon(pm))
        self.PB_makeShell_2.clicked.connect(
            merge_faces_from_selected_objects_RH)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(check_type_b64))
        self.PB_check_TypeId.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_check_TypeId.setIcon(QtGui.QIcon(pm))
        self.PB_check_TypeId.clicked.connect(check_TypeId_RH)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(add_edges_b64))
        self.PB_Edges.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_Edges.setIcon(QtGui.QIcon(pm))
        self.PB_Edges.clicked.connect(edges_confirmed_RH)
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(loop_edges_b64))
        self.PB_LoopEdge.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_LoopEdge.setIcon(QtGui.QIcon(pm))
        self.PB_LoopEdge.clicked.connect(loop_edges_RH)
        self.PB_LoopEdge.setToolTip("create a loop Edge\nof edge selection")

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(clear_b64))
        self.PB_Edges_Clear.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_Edges_Clear.setIcon(QtGui.QIcon(pm))
        self.PB_Edges_Clear.clicked.connect(clear_all_RH)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(clear_b64))
        self.PB_Faces_Clear.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_Faces_Clear.setIcon(QtGui.QIcon(pm))
        self.PB_Faces_Clear.clicked.connect(clear_all_RH)
        self.PB_Faces_Clear.clicked.connect(clear_all_RH)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(add_faces_b64))
        self.PB_Faces.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_Faces.setIcon(QtGui.QIcon(pm))
        self.PB_Faces.clicked.connect(faces_confirmed_RH)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(del_hole_b64))
        self.PB_RHoles.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_RHoles.setIcon(QtGui.QIcon(pm))
        self.PB_RHoles.clicked.connect(removeHoles_RH)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(del_face_b64))
        self.PB_RFaces.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_RFaces.setIcon(QtGui.QIcon(pm))
        self.PB_RFaces.clicked.connect(removeFaces_RH)
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(add_face_b64))
        self.PB_AFaces.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_AFaces.setIcon(QtGui.QIcon(pm))
        self.PB_AFaces.clicked.connect(addFaces_RH)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(copy_face_b64))
        self.PB_CFaces.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_CFaces.setIcon(QtGui.QIcon(pm))
        self.PB_CFaces.clicked.connect(copyFaces_RH)
        self.PB_CFaces.setToolTip("copy Faces from \'in List\' Faces")
        self.checkBox_keep_original.setChecked(True)
        self.checkBox_keep_faces.setChecked(False)
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(refine_b64))
        self.PB_Refine.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_Refine.setIcon(QtGui.QIcon(pm))
        self.PB_Refine.clicked.connect(refine_RH)
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(refine_feature_b64))
        self.PB_RefineParametric.setIconSize(
            QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_RefineParametric.setIcon(QtGui.QIcon(pm))
        self.PB_RefineParametric.clicked.connect(refine_parametric_RH)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(show_edges_b64))
        self.PB_showEdgeList.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_showEdgeList.setIcon(QtGui.QIcon(pm))
        self.PB_showEdgeList.clicked.connect(showEdges_RH)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(show_faces_b64))
        self.PB_showFaceList.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_showFaceList.setIcon(QtGui.QIcon(pm))
        self.PB_showFaceList.clicked.connect(showFaces_RH)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(offset_face_b64))
        self.PB_TFace.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_TFace.setIcon(QtGui.QIcon(pm))
        self.PB_TFace.setToolTip('offset face')
        self.PB_TFace.clicked.connect(offsetFaces_RH)
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(offset_edge_b64))
        self.PB_TEdge.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_TEdge.setIcon(QtGui.QIcon(pm))
        self.PB_TEdge.setToolTip('offset edge')
        self.PB_TEdge.clicked.connect(offsetEdges_RH)
        self.offset_input.setText("1.0:n")
        self.offset_input.setToolTip(
            "offset in mm\n separator ':'\ndirection [n=normal, x,y,z]")

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(create_edge_b64))
        self.PB_makeEdge.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_makeEdge.setIcon(QtGui.QIcon(pm))
        self.PB_makeEdge.clicked.connect(makeEdge_RH)
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(mk_solid3_b64))
        self.PB_expSTEP.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_expSTEP.setIcon(QtGui.QIcon(pm))
        self.PB_expSTEP.clicked.connect(makeSolidExpSTEP_RH)
        self.PB_expSTEP.setToolTip(
            "select ONE object to try to make a Solid\nthrough STEP import/export process")
        self.TE_Edges.setReadOnly(True)
        self.TE_Faces.setReadOnly(True)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(defeaturing_b64))
        self.PB_PartDefeaturing.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_PartDefeaturing.setIcon(QtGui.QIcon(pm))
        self.PB_PartDefeaturing.clicked.connect(PartDefeaturing_RH)

        self.PB_PartDefeaturing.setVisible(True)
        self.PB_PartDefeaturing.setToolTip(
            "select Faces to be Parametric defeatured")

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(clean_face_b64))
        self.PB_CleaningFaces.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_CleaningFaces.setIcon(QtGui.QIcon(pm))
        self.PB_CleaningFaces.clicked.connect(cleaningFaces_RH)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(check_geo_b64))
        self.PB_checkS.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_checkS.setIcon(QtGui.QIcon(pm))
        self.PB_checkS.clicked.connect(checkShape)
        self.PB_checkS.setToolTip("geometry check")

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(setTol_b64))
        self.PB_setTol.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_setTol.setIcon(QtGui.QIcon(pm))
        self.PB_setTol.clicked.connect(setTolerance)
        self.PB_setTol.setToolTip("set Tolerance value")

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(getTol_b64))
        self.PB_getTol.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_getTol.setIcon(QtGui.QIcon(pm))
        self.PB_getTol.clicked.connect(getTolerance)
        self.PB_getTol.setToolTip("get Tolerance value")
        self.PB_sewS.clicked.connect(sewShape)
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(sew_shape_b64))
        self.PB_sewS.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_sewS.setIcon(QtGui.QIcon(pm))
        self.PB_sewS.setToolTip("sew a shape")
        self.tolerance_value.setToolTip("tolerance value to be applied")
        self.tolerance_value.setText("0.0001")

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(connect_b64))
        self.PB_Connect.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_Connect.setIcon(QtGui.QIcon(pm))
        self.PB_Connect.clicked.connect(shape_Connect_RH)
        self.PB_Connect.setToolTip("Connect")
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(simple_copy_b64))
        self.PB_SimpleCopy.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_SimpleCopy.setIcon(QtGui.QIcon(pm))
        self.PB_SimpleCopy.clicked.connect(simplecopy_RH)
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(help_b64))
        self.PB_RHhelp.setIconSize(QtCore.QSize(btn_sizeX, btn_sizeY))
        self.PB_RHhelp.setIcon(QtGui.QIcon(pm))
        self.PB_RHhelp.clicked.connect(onHelp)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(closeW_b64))
        self.PB_close.setGeometry(QtCore.QRect(-1, -1, 20, 20))
        self.PB_close.setToolTip("close")
        self.PB_close.setText("")
        self.PB_close.setIconSize(QtCore.QSize(16, 16))
        self.PB_close.setIcon(QtGui.QIcon(pm))
        self.PB_close.clicked.connect(close_RH)
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(dock_left_b64))
        self.PB_left.setGeometry(QtCore.QRect(-1, 19, 20, 20))
        self.PB_left.setToolTip("dock left")
        self.PB_left.setText("")
        self.PB_left.setIconSize(QtCore.QSize(16, 16))
        self.PB_left.setIcon(QtGui.QIcon(pm))
        self.PB_left.clicked.connect(dock_left_RH)

        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(dock_right_b64))
        self.PB_right.setGeometry(QtCore.QRect(-1, 39, 20, 20))
        self.PB_right.setToolTip("dock right")
        self.PB_right.setText("")
        self.PB_right.setIconSize(QtCore.QSize(16, 16))
        self.PB_right.setIcon(QtGui.QIcon(pm))
        self.PB_right.clicked.connect(dock_right_RH)
        if pt_osx:
            self.InfoLabel.setText("Select Edge(s)\nCmd+Click")
            self.label.setText("Select Face(s)\nCmd+Click")
################################################################################################

    def retranslateUi(self, DockWidget):
        pass


##############################################################
global instance_nbr
instance_nbr = 0


def RH_singleInstance():

    app = QtGui.QApplication  # QtGui.qApp
    for i in app.topLevelWidgets():

        if i.objectName() == "DefeaturingTools":
            return False
    t = Gui.getMainWindow()
    dw = t.findChildren(QtGui.QDockWidget)

    for i in dw:

        # "kicad StepUp 3D tools":
        if str(i.objectName()) == "DefeaturingTools":

            return False
    return True
##


def dock_right_RH():
    global instance_nbr

    RHmw = Gui.getMainWindow()
    t = Gui.getMainWindow()
    dw = t.findChildren(QtGui.QDockWidget)
    looping = False
    ldw = len(dw)
    if ldw > 0:
        looping = True
    idw = 0
    cv = None
    while looping and idw < ldw:
        d = dw[idw]
        idw += 1
        area = t.dockWidgetArea(d)

        if area == QtCore.Qt.RightDockWidgetArea:
            print(d.windowTitle(), '(Right)')
            r_w = str(d.objectName())  # ;print(r_w)
            cv = t.findChild(QtGui.QDockWidget, r_w)
            looping = False
    RHmw.addDockWidget(QtCore.Qt.RightDockWidgetArea, RHDockWidget)
    RHDockWidget.setFloating(False)  # dock

    RHDockWidget.activateWindow()
    RHDockWidget.raise_()
    if RHDockWidget and cv is not None:
        dw = t.findChildren(QtGui.QDockWidget)

        try:
            t.tabifyDockWidget(cv, RHDockWidget)
            i_say("Tabified done !")

        except:
            i_say('exception raised')
            pass
    if instance_nbr == 0:
        instance_nbr = 1
        dock_right_RH()

##


def dock_left_RH():
    RHmw = Gui.getMainWindow()
    RHmw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, RHDockWidget)
    RHDockWidget.setFloating(False)  # dock

    RHDockWidget.activateWindow()
    RHDockWidget.raise_()

    RHDockWidget.setFloating(False)  # dock

    RHDockWidget.activateWindow()
    RHDockWidget.raise_()
    t = Gui.getMainWindow()
    cv = t.findChild(QtGui.QDockWidget, "Combo View")
    if RHDockWidget and cv:
        dw = t.findChildren(QtGui.QDockWidget)
        try:
            t.tabifyDockWidget(cv, RHDockWidget)
            i_say("Tabified done !")
        except:
            i_say('exception raised')
            pass
##


def RH_centerOnScreen(widg):
    '''centerOnScreen()
    Centers the window on the screen.'''
    resolution = QtGui.QDesktopWidget().screenGeometry()
    # - (KSUWidget.frameSize().width() / 2)
    xp = (resolution.width() / 2) - sizeX/2
    # - (KSUWidget.frameSize().height() / 2))
    yp = (resolution.height() / 2) - sizeY/2

    widg.setGeometry(xp, yp, sizeX, sizeY)
##


def onHelp():
    msg = """<b>Defeaturer Tools</b><br>
    Defeaturer is working with FC >= 0.15<br>
    advance defeaturing functions with OCC >= 7.3<br>
    """
    msg += 'App version: ' + \
        App.Version()[0]+'.'+App.Version()[1]+'.'+App.Version()[2]+'<br>'
    if hasattr(Part, "OCC_VERSION"):
        OCCMV = Part.OCC_VERSION.split('.')[0]
        OCCmV = Part.OCC_VERSION.split('.')[1]
        msg = msg+"""OCC version: """+str(Part.OCC_VERSION)+"""<br>"""
    else:
        msg = msg+"""OCC version &lt; 7.0<br>"""
    msg = msg+"""
    <font color = blue>Defeaturing Tools Version:  
    """+__version__+"""</font>"""

    QtGui.QApplication.restoreOverrideCursor()
    res = ''
    QtGui.QApplication.restoreOverrideCursor()
    res = QtGui.QMessageBox.question(None, "Help", msg, QtGui.QMessageBox.Ok)


doc = App.ActiveDocument
if RH_singleInstance():
    RHDockWidget = QtGui.QDockWidget()
    RHDockWidget.ui = Ui_DockWidget()
    RHDockWidget.ui.setupUi(RHDockWidget)  # setup the ui
    RHDockWidget.setObjectName("DefeaturingTools")
    RHDockWidget.raise_()
    # |QtGui.QDockWidget.DockWidgetClosable )
    RHDockWidget.setFeatures(
        QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)

    def onClickClose():
        RH_visible = RHDockWidget.isVisible()

    RHDockWidget.visibilityChanged.connect(onClickClose)

    # PySide # the active qt window, = the App window since we are inside it
    RHmw = Gui.getMainWindow()
    RHmw.addDockWidget(QtCore.Qt.RightDockWidgetArea, RHDockWidget)
    RHDockWidget.setFloating(True)  # undock
    RH_centerOnScreen(RHDockWidget)
    RHDockWidget.ui.Version.setText(__version__)

    if hasattr(Part, "OCC_VERSION"):
        OCCMV = Part.OCC_VERSION.split('.')[0]
        OCCmV = Part.OCC_VERSION.split('.')[1]
        if (int(OCCMV) >= 7) and (int(OCCmV) >= 3):
            RHDockWidget.ui.PB_PartDefeaturing.setVisible(True)
            RHDockWidget.ui.PB_PartDefeaturing.setEnabled(True)


# raising up
RHDockWidget.activateWindow()
RHDockWidget.raise_()
dock_left_RH()  # Dock the widget to the left
