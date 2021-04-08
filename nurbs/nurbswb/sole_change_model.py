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
# * Modified and adapter to Desing456 by:                                  *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

from PySide import QtGui, QtCore
import FreeCAD as App
import FreeCADGui as Gui

import numpy as np


def srun(w):
    print(w.m.currentIndex())
    a = w.target
    model = 'modelS'
    import nurbswb.sole_models
    reload(nurbswb.sole_models)
    lm = nurbswb.sole_models.listModels(silent=True)
    print(lm[w.m.currentIndex()])
    model = lm[w.m.currentIndex()][0]

    reload(nurbswb.sole)
    cmd = "nurbswb.sole.runA(model=nurbswb.sole_models." + model + "())"
    print(cmd)
    eval(cmd)
    # w.hide()


def MyDialog(target=None):

    import nurbswb.sole_models
    reload(nurbswb.sole_models)
    lm = nurbswb.sole_models.listModels()

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


def run():
    # [target]=FreeCADGui.Selection.getSelection()
    target = None
    return MyDialog(target)


if __name__ == '__main__':
    run()
