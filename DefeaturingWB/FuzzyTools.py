# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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


#****************************************************************************
#*                                                                          *
#*  Copyright (c) 2017                                                      *
#*  Maurice easyw@katamail.com                                              *
#*                                                                          *
#                                                                           *
#   Repair Defeaturing Macro                                 *
#                                                                           *
#  (C) Maurice easyw-fc 2018                                               *
#    This program is free software; you can redistribute it and/or modify   *
#    it under the terms of the GNU Library General Public License (LGPL)    *
#    as published by the Free Software Foundation; either version 2 of      *
#    the License, or (at your option) any later version.                    *
#    for detail see the LICENCE text file.                                  *
#****************************************************************************


import FreeCAD as App 
import FreeCADGui as Gui 
import Draft, Part
import re, os, sys
from PySide import QtCore, QtGui

__version__ = "v1.0.2"

def f_say(msg):
    App.Console.PrintMessage(msg)
    App.Console.PrintMessage('\n')

def f_sayw(msg):
    App.Console.PrintWarning(msg)
    App.Console.PrintWarning('\n')
    
def f_sayerr(msg):
    App.Console.PrintError(msg)
    App.Console.PrintWarning('\n')

##
def fuzzyCut():
    global fuzzyTolerance
    from PySide import QtCore, QtGui
    
    fuzzyTolerance = 0.01
    reply = QtGui.QInputDialog.getText(None, "Tolerance","Fuzzy Tolerance",QtGui.QLineEdit.Normal,str(fuzzyTolerance))
    if reply[1]:
            # user clicked OK
            replyText = reply[0]
            fuzzyTolerance = float (replyText)
    else:
        # user clicked Cancel
        replyText = reply[0] # which will be "" if they clicked Cancel
    doc = App.ActiveDocument
    docG = Gui.ActiveDocument
    sel = Gui.Selection.getSelection()
    if len(sel)==2:
        if 0:
            doc.addObject("Part::Cut","Cut")
            added = doc.ActiveObject
            added.Base = sel[0]
            added.Tool = sel[1]
        else:
            shapeBase = sel[0].Shape
            shapeTool = sel[1].Shape      
            result_shape = shapeBase.cut(shapeTool, fuzzyTolerance)
            Part.show(result_shape)
            added = doc.ActiveObject
        docG.getObject(sel[0].Name).Visibility=False
        docG.getObject(sel[1].Name).Visibility=False
        docG.getObject(added.Name).ShapeColor=docG.getObject(sel[0].Name).ShapeColor
        docG.getObject(added.Name).Transparency=docG.getObject(sel[0].Name).Transparency
        docG.getObject(added.Name).DisplayMode=docG.getObject(sel[0].Name).DisplayMode
        added.Label = 'CutFuzzy'
        doc.recompute()
##
def fuzzyUnion():
    global fuzzyTolerance
    
    fuzzyTolerance = 0.01
    reply = QtGui.QInputDialog.getText(None, "Tolerance","Fuzzy Tolerance",QtGui.QLineEdit.Normal,str(fuzzyTolerance))
    if reply[1]:
            # user clicked OK
            replyText = reply[0]
            fuzzyTolerance = float (replyText)
    else:
        # user clicked Cancel
        replyText = reply[0] # which will be "" if they clicked Cancel
    doc = App.ActiveDocument
    docG = Gui.ActiveDocument
    sel = Gui.Selection.getSelection()
    shapes = []
    for s in sel[1:]:
        shapes.append(s.Shape)
    c = sel[0].Shape.multiFuse(shapes, fuzzyTolerance)
    Part.show(c)
    added = doc.ActiveObject
    for s in sel:
        docG.getObject(s.Name).Visibility=False
    docG.getObject(added.Name).ShapeColor=docG.getObject(sel[0].Name).ShapeColor
    docG.getObject(added.Name).Transparency=docG.getObject(sel[0].Name).Transparency
    docG.getObject(added.Name).DisplayMode=docG.getObject(sel[0].Name).DisplayMode
    added.Label = 'UnionFuzzy'
    doc.recompute()
##
def fuzzyCommon():
    global fuzzyTolerance
    
    fuzzyTolerance = 0.01
    reply = QtGui.QInputDialog.getText(None, "Tolerance","Fuzzy Tolerance",QtGui.QLineEdit.Normal,str(fuzzyTolerance))
    if reply[1]:
            # user clicked OK
            replyText = reply[0]
            fuzzyTolerance = float (replyText)
    else:
        # user clicked Cancel
        replyText = reply[0] # which will be "" if they clicked Cancel
    doc = App.ActiveDocument
    docG = Gui.ActiveDocument
    sel = Gui.Selection.getSelection()
    shapes = []
    for s in sel[1:]:
        shapes.append(s.Shape)
    c = sel[0].Shape.common(shapes, fuzzyTolerance)
    Part.show(c)
    added = doc.ActiveObject
    for s in sel:
        docG.getObject(s.Name).Visibility=False
    docG.getObject(added.Name).ShapeColor=docG.getObject(sel[0].Name).ShapeColor
    docG.getObject(added.Name).Transparency=docG.getObject(sel[0].Name).Transparency
    docG.getObject(added.Name).DisplayMode=docG.getObject(sel[0].Name).DisplayMode
    added.Label = 'CommonFuzzy'
    doc.recompute()
##