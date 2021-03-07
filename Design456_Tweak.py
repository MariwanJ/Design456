# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
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
# * Author :carlopav                                                        *
# *This is pulled to the main github at the link bellow                     *
# *github.com/MariwanJ/Design456/commits/5911dd3817aba28df6f5b215d39ef8851b974d5f
# *  See the forum :                                                       *
# *Modified by     Mariwan Jalal     mariwan.jalal@gmail.com               *
# **************************************************************************
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft
import Part

from draftguitools import gui_move
from draftutils.messages import _msg, _err
from draftutils.translate import translate


# This part is higly experimental and used for moveSubElements function
# it's and experiment by carlopav initially aimed at Draft WB, but not completed.
# We need to make this work better, for specific usage. More works must be done-Mariwan

def moveSubElements(obj, sub_objects_names, vector):
    """moveSubElements(obj, sub_objects_names, vector)

    Move the given object sub_objects according to a vector or crates an new one
    if the object is not a Part::Feature.
    Parameters
    ----------
    obj : the given object
    sub_objects_names : list of subelement names
        A list of subelement names to identify the subelements to move.
    vector : Base.Vector
        Delta Vector to move subobjects from the original position. 
    Return
    ----------
    shape : Part.Shape
        Return the new Shape or None.
    """
    if not isinstance(sub_objects_names, list):
        sub_objects_names = [sub_objects_names]

    shape = obj.Shape
    new_shape = None
    if not shape.isValid():
        return

    selected_subelements = []
    for sub_objects_name in sub_objects_names:
        sub_object = obj.Shape.getElement(sub_objects_name)
        selected_subelements.append(sub_object)
        selected_subelements.extend(sub_object.Faces)
        selected_subelements.extend(sub_object.Edges)
        selected_subelements.extend(sub_object.Vertexes)

    new_shape, touched = parse_shape(shape, selected_subelements, vector)

    if not new_shape.isValid():
        should_fix = move_subelements_msgbox()
        if should_fix:
            new_shape.fix(0.001, 0.001, 0.001)

    if new_shape:
        if hasattr(obj, 'TypeId') and obj.TypeId == 'Part::Feature':
            obj.Shape = new_shape
        else:
            new_obj = App.ActiveDocument.addObject("Part::Feature", "Feature")
            new_obj.Shape = new_shape
        del selected_subelements[:]
        return new_shape
        


def parse_shape(shape, selected_subelements, vector):
    """ Parse the given shape and rebuild it according to its
    original topological structure
    """
    print('Parsing ' + shape.ShapeType + '\n')

    if shape.ShapeType in ("Compound", "CompSolid", "Solid", "Shell", "Wire"):
        # No geometry involved
        new_sub_shapes, touched_subshapes = parse_sub_shapes(
            shape, selected_subelements, vector)

        if shape.ShapeType == "Compound":
            new_shape = Part.Compound(new_sub_shapes)

        elif shape.ShapeType == "CompSolid":
            new_shape = Part.CompSolid(new_sub_shapes)

        elif shape.ShapeType == "Solid":
            if isinstance(new_sub_shapes, list) and len(new_sub_shapes) == 1:
                # check if shell object is given inside a list
                new_sub_shapes = new_sub_shapes[0]
            new_shape = Part.Solid(new_sub_shapes)

        elif shape.ShapeType == "Shell":
            new_shape = Part.Shell(new_sub_shapes)

        elif shape.ShapeType == "Wire":
            new_sub_shapes = Part.__sortEdges__(new_sub_shapes)
            new_shape = Part.Wire(new_sub_shapes)

        print(shape.ShapeType + " re-created.")
        touched = True

    elif shape.ShapeType == "Face":
        new_sub_shapes, touched_subshapes = parse_sub_shapes(
            shape, selected_subelements, vector)
        if touched_subshapes == 1 or touched_subshapes == 2:
            print("some subshapes touched " + shape.ShapeType + " recreated.")
            if shape.Surface.TypeId == 'Part::GeomPlane':
                new_sub_shapes = sort_wires(new_sub_shapes)
                new_shape = Part.Face(new_sub_shapes)
                touched = True
                # TODO: handle the usecase when the Face is not planar anymore after modification
            else:
                print("Face geometry not supported")
        elif touched_subshapes == 0:
            print("subshapes not touched " + shape.ShapeType + " not touched.")
            new_shape = shape
            touched = False

    elif shape.ShapeType == "Edge":
        # TODO: Add geometry check
        new_sub_shapes, touched_subshapes = parse_sub_shapes(
            shape, selected_subelements, vector)
        if touched_subshapes == 2:
            print("all subshapes touched. " + shape.ShapeType + " translated.")
            # all subshapes touched
            new_shape = shape.translate(vector)
            touched = True
        elif touched_subshapes == 1:
            # some subshapes touched: recreate the edge as a straight vector: TODO Add geometry check
            print("some subshapes touched " + shape.ShapeType + " recreated.")
            new_shape = Part.makeLine(
                new_sub_shapes[0].Point, new_sub_shapes[1].Point)
            touched = True
        elif touched_subshapes == 0:
            # subshapes not touched
            print("subshapes not touched " + shape.ShapeType + " not touched.")
            new_shape = shape
            touched = False

    elif shape.ShapeType == "Vertex":
        # TODO: Add geometry check
        touched = False
        for s in selected_subelements:
            if shape.isSame(s):
                touched = True
        if touched:
            print(shape.ShapeType + " translated.")
            new_shape = shape.translate(vector)
        else:
            print(shape.ShapeType + " not touched.")
            new_shape = shape

    return new_shape, touched


def sort_wires(wires):
    if not isinstance(wires, list):
        return wires
    if len(wires) == 1:
        return wires
    outer_wire = wires[0]

    for w in wires:
        if outer_wire.BoundBox.DiagonalLength < w.BoundBox.DiagonalLength:
            outer_wire = w

    new_wires = [outer_wire]
    for w in wires:
        if w != outer_wire:
            new_wires.append(w)

    return new_wires


def parse_sub_shapes(shape, selected_subelements, vector):
    """ Parse the subshapes of the given shape in order to
    find modified shapes and substitute them to the originals.
    """
    sub_shapes = []
    touched_subshapes = []
    if shape.SubShapes:
        for sub_shape in shape.SubShapes:
            new_sub_shape, touched_subshape = parse_shape(
                sub_shape, selected_subelements, vector)
            sub_shapes.append(new_sub_shape)

            if touched_subshape:
                touched_subshapes.append(2)
            else:
                touched_subshapes.append(0)

    if 0 in touched_subshapes and 2 in touched_subshapes:
        # only some subshapes touched
        touched = 1
    elif 2 in touched_subshapes:
        # all subshapes touched
        touched = 2
    elif 0 in touched_subshapes:
        # no subshapes touched
        touched = 0
    return sub_shapes, touched


def move_subelements_msgbox():
    if not App.GuiUp:
        return False
    msgBox = QtGui.QMessageBox()
    msgBox.setText("Shape has become invalid after editing.")
    msgBox.setInformativeText("Do you want to try to fix it?\n")
    msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
    msgBox.setDefaultButton(QtGui.QMessageBox.Yes)
    ret = msgBox.exec_()

    if ret == QtGui.QMessageBox.Yes:
        return True
    elif ret == QtGui.QMessageBox.No:
        return False


class Design456_Tweak(gui_move.Move):
    def __init__(self):
        super(Design456_Tweak, self).__init__()

    def Activated(self):
        super(Design456_Tweak, self).Activated()
        return


    def proceed(self):
        super(Design456_Tweak, self).proceed()
        state = QtCore.Qt.CheckState()
        self.ui.isSubelementMode.setCheckState(state.Checked)

    def move_subelements(self):
        """Move the subelements."""
        try:
            if self.ui.isCopy.isChecked():
                self.commit(translate("draft", "Copy"),
                            self.build_copy_subelements_command())
            else:
                self.commit(translate("draft", "Move"),
                            self.build_move_subelements_command())
        except Exception:
            _err(translate("draft", "Some subelements could not be moved."))
        import Draft
        # try:
        if self.ui.isCopy.isChecked():
            self.commit(translate("draft", "Copy"),
                        self.build_copy_subelements_command())
        else:
            # self.commit(translate("draft", "Move"), # Moult implementation start
            #            self.build_move_subelements_command()) # Moult implementation end

            objects = {}

            # create a dictionary with {'obj.Name' : 'list of selected SubObjects'}
            for sel in self.selected_subelements:
                if not sel.Object.Name in objects:
                    objects[sel.Object.Name] = []
                if sel.SubObjects:
                    objects[sel.Object.Name].extend(sel.SubElementNames)

            App.ActiveDocument.openTransaction(
                translate("Draft", "Move subelements"))

            for name in objects:  # for each object
                # get the object and its shape
                # Gui.addModule("Draft")
                # Gui.doCommand('Draft.moveSubElements(' +
                #                'FreeCAD.ActiveDocument.' + name + ', ' +
                #                str(objects[name]) + ', ' +
                #                DraftVecUtils.toString(self.vector) +
                #                ')')
                moveSubElements(App.ActiveDocument.getObject(
                    name), objects[name], self.vector)
            App.ActiveDocument.commitTransaction()

        # except Exception:
        #    _err(translate("draft", "Some subelements could not be moved."))

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Design456_Tweak.svg',
            'MenuText': 'Tweak',
            'ToolTip':  'Tweak Object'
        }

Gui.addCommand('Design456_Tweak', Design456_Tweak())
