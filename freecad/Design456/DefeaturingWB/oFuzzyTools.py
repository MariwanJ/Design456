# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2017 Maurice ( easyw@katamail.com )
# SPDX-FileContributor: Mariwan Jalal ( mariwan.jalal@gmail.com )
# SPDX-FileNotice: Part of the Defeaturing addon. Included in the Design456 addon.

from __future__ import unicode_literals


import FreeCAD as App 
import FreeCADGui as Gui 
import Draft, Part
import re, os, sys
from PySide import QtCore, QtGui

__version__ = "v1.0.2"

def of_say(msg):
    App.Console.PrintMessage(msg)
    App.Console.PrintMessage('\n')

def of_sayw(msg):
    App.Console.PrintWarning(msg)
    App.Console.PrintWarning('\n')
    
def of_sayerr(msg):
    App.Console.PrintError(msg)
    App.Console.PrintWarning('\n')

##
def ofuzzyCut():
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
def ofuzzyUnion():
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
def ofuzzyCommon():
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