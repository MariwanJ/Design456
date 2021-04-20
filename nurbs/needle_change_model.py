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
# * Modified and adapted to Desing456 by:                                  *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

from PySide import QtGui, QtCore
import FreeCAD as App
import FreeCADGui as Gui 

import NURBSinit

import os,sys

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    


def srun(w):
    print(w.m.currentIndex())
    a = w.target
    model = 'modelS'
    needle_models
    #reload(.needle_models)
    lm = needle_models.listModels(silent=True)
    print(lm[w.m.currentIndex()])
    model = lm[w.m.currentIndex()][0]

    print("a.Proxy.getExampleModel(.needle_models." + model+")")
    eval("a.Proxy.getExampleModel(.needle_models." + model+")")
    w.hide()


def MyDialog(target):

    needle_models
    #reload(.needle_models)
    lm = needle_models.listModels()

    w = QtGui.QWidget()
    w.target = target

    box = QtGui.QVBoxLayout()
    w.setLayout(box)
    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    l = QtGui.QLabel("Select the model")
    box.addWidget(l)

    combo = QtGui.QComboBox()

    for item in lm:
        combo.addItem(str(item))

    w.m = combo
    combo.activated.connect(lambda: srun(w))

    box.addWidget(combo)

    w.show()
    return w

class Nurbs_NeedleChangeModel:
    def Activated(self):
        self.runNeedleChangeModel()
    def runNeedleChangeModel(self):
        [target] = Gui.Selection.getSelection()
        MyDialog(target)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_NeedleChangeModel")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_NeedleChangeModel"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_NeedleChangeModel", Nurbs_NeedleChangeModel())

