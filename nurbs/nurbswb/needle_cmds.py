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


import sys
import numpy as np


from PySide import QtGui

import FreeCAD as App
import FreeCADGui as Gui

needle
needle_models
reload(nurbswb.needle_models)


def getdata(index):
    ri = index.row()-2
    c = index.column()
    ci = 0

    if c == 0:  # command fuer curve
        sel = "ccmd"
        return sel, ci, ri, index.data()

    if c == 5:  # command fuer curve
        sel = "bcmd"
        return sel, ci, ri, index.data()

    if c in range(1, 4):
        sel = "rib"
        ci = c-1
    elif c in range(6, 9):
        sel = "bb"
        ci = c-6
    else:
        sel = None
        ci = -1

    return sel, ci, ri, index.data()


def initmodel():
    App.activeDocument().MyNeedle.Proxy.lock = False
    App.activeDocument().MyNeedle.Proxy.getExampleModel(nurbswb.needle_models.modelS)
    # App.activeDocument().MyNeedle.Proxy.getExampleModel(nurbswb.needle_models.modelBanana)
    # App.activeDocument().MyNeedle.Proxy.getExampleModel(nurbswb.needle_models.modelEd4)


def addRib(dialog):
    # read
    (curve, bb, scaler, twister) = App.activeDocument().MyNeedle.Proxy.Model()

    # modifications
    i = dialog.pos
    if i == 0:
        print("kann keine ripee vroschieben")
        return

    t = (bb[i-1]+bb[i])*0.5
    b = np.concatenate([bb[0:i], [t], bb[i:]])
    bb = b
    t = (scaler[i-1]+scaler[i])*0.5
    b = np.concatenate([scaler[0:i], [t], scaler[i:]])
    scaler = b
    t = (twister[i-1]+twister[i])*0.5
    b = np.concatenate([twister[0:i], [t], twister[i:]])
    twister = b

    # write back
    App.activeDocument().MyNeedle.Proxy.lock = False
    App.activeDocument().MyNeedle.Proxy.setModel(curve, bb, scaler, twister)
    dialog.obj.Proxy.showRib(i)
    dialog.close()


def CaddRib(obj, i):
    # read
    (curve, bb, scaler, twister) = obj.Proxy.Model()

    t = (bb[i]+bb[i+1])*0.5
    b = np.concatenate([bb[0:i+1], [t], bb[i+1:]])
    bb = b
    t = (scaler[i]+scaler[i+1])*0.5
    b = np.concatenate([scaler[0:i+1], [t], scaler[i+1:]])
    scaler = b
    t = (twister[i]+twister[i+1])*0.5
    b = np.concatenate([twister[0:i+1], [t], twister[i+1:]])
    twister = b

    # write back
    obj.Proxy.lock = False
    obj.Proxy.setModel(curve, bb, scaler, twister)
    obj.Proxy.showRib(i)


def addMeridian(dialog):
    # read
    (curve, bb, scaler, twister) = App.activeDocument().MyNeedle.Proxy.Model()

    # modifications
    i = dialog.pos
    t = (curve[i-1]+curve[i])*0.5
    c = np.concatenate([curve[0:i], [t], curve[i:]])
    curve = c

    # write back
    App.activeDocument().MyNeedle.Proxy.lock = False
    App.activeDocument().MyNeedle.Proxy.setModel(curve, bb, scaler, twister)
    dialog.obj.Proxy.showMeridian(i)
    dialog.close()


def CaddMeridian(obj, i):
    (curve, bb, scaler, twister) = obj.Proxy.Model()
    t = (curve[i]+curve[i+1])*0.5
    c = np.concatenate([curve[0:i+1], [t], curve[i+1:]])
    curve = c
    obj.Proxy.lock = False
    obj.Proxy.setModel(curve, bb, scaler, twister)
    obj.Proxy.showMeridian(i)


def addStrongMeridianEdge(dialog):
    obj = dialog.obj
    i = dialog.pos
    CaddStrongMeridianEdge(obj, i+1)
    dialog.close()


def addNeighborMeridians(dialog):
    obj = dialog.obj
    i = dialog.pos
    CaddNeighborMeridians(obj, i+1)
    dialog.close()


def CaddNeighborRibs(obj, i):
    (curve, bb, scaler, twister) = obj.Proxy.Model()
    st = 0.98
    i = i-1
    if curve.shape[0] == i:
        i = 0
    if curve.shape[0] == i+1:
        j = 0
    else:
        j = i+1

    t1 = bb[i]+(bb[i]-bb[j])*0.02
    t2 = bb[i]+(bb[i]-bb[i-1])*0.02
    b = np.concatenate([bb[0:i], [t1, bb[i], t2], bb[i+1:]])
    bb = b

    t2 = scaler[i]+(scaler[j]-scaler[i])*0.02
    t1 = scaler[i]+(scaler[i-1]-scaler[i])*0.02
    b = np.concatenate([scaler[0:i], [t1, scaler[i], t2], scaler[i+1:]])
    scaler = b

    t2 = twister[i]+(twister[j]-twister[i])*0.02
    t1 = twister[i]+(twister[i-1]-twister[i])*0.02
    b = np.concatenate([twister[0:i], [t1, twister[i], t2], twister[i+1:]])
    twister = b

    obj.Proxy.lock = False
    obj.Proxy.setModel(curve, bb, scaler, twister)
    obj.Proxy.showRib(i+1)


def CaddStrongRibEdge(obj, i):
    (curve, bb, scaler, twister) = obj.Proxy.Model()
    st = 0.98

    if bb.shape[0] == i:
        print("Keine verlaengerung uebers einde hinaus moegliche")
        return

    t = bb[i-1]*st+bb[i]*(1-st)
    b = np.concatenate([bb[0:i], [t], bb[i:]])
    bb = b
    t = scaler[i-1]*st+scaler[i]*(1-st)
    b = np.concatenate([scaler[0:i], [t], scaler[i:]])
    scaler = b
    t = twister[i-1]*st+twister[i]*(1-st)
    b = np.concatenate([twister[0:i], [t], twister[i:]])
    twister = b

    obj.Proxy.lock = False
    obj.Proxy.setModel(curve, bb, scaler, twister)
    obj.Proxy.showRib(i)


# sharp and round edge -- strong edge p -> 2p oder p ->git commit - 3p

def addStrongRibEdge(dialog):
    CaddStrongRibEdge(dialog.obj, dialog.pos+1)
    dialog.close()


def addNeighborRibs(dialog):
    obj = dialog.obj
    i = dialog.pos
    CaddNeighborRibs(obj, i+1)
    dialog.close()


def CaddStrongMeridianEdge(obj, i):
    (curve, bb, scaler, twister) = obj.Proxy.Model()
    st = 0.98
    if curve.shape[0] == i:
        i = 0
    t = curve[i-1]*st + curve[i]*(1-st)
    c = np.concatenate([curve[0:i], [t], curve[i:]])
    obj.Proxy.lock = False
    obj.Proxy.setModel(c, bb, scaler, twister)
    obj.Proxy.showMeridian(i)


def CaddNeighborMeridians(obj, i):
    (curve, bb, scaler, twister) = obj.Proxy.Model()
    st = 0.98
    i = i-1
    if curve.shape[0] == i:
        i = 0
    if curve.shape[0] == i+1:
        j = 0
    else:
        j = i+1
    t1 = curve[i]+(curve[i]-curve[j])*0.02
    t2 = curve[i]+(curve[i]-curve[i-1])*0.02
    c = np.concatenate([curve[0:i], [t1, curve[i], t2], curve[i+1:]])
    obj.Proxy.lock = False
    obj.Proxy.setModel(c, bb, scaler, twister)
    obj.Proxy.showMeridian(i+1)


def delMeridian(dialog):
    # read
    (curve, bb, scaler, twister) = App.activeDocument().MyNeedle.Proxy.Model()

    if curve.shape[0] < 5:
        print("zu wenig Punkte "())
        return

    # modifications
    i = dialog.pos
    c = np.concatenate([curve[0:i], curve[i+1:]])
    curve = c

    # write back
    App.activeDocument().MyNeedle.Proxy.lock = False
    App.activeDocument().MyNeedle.Proxy.setModel(curve, bb, scaler, twister)
    dialog.obj.Proxy.showMeridian(i)
    dialog.close()


def CdelMeridian(obj, i):
    # read
    (curve, bb, scaler, twister) = obj.Proxy.Model()

    if curve.shape[0] < 5:
        print("zu wenig Punkte ")
        return

    # modifications
    c = np.concatenate([curve[0:i], curve[i+1:]])
    curve = c

    # write back
    obj.Proxy.lock = False
    obj.Proxy.setModel(curve, bb, scaler, twister)
    obj.Proxy.showMeridian(i-2)


def CdelRib(obj, i):
    # read
    (curve, bb, scaler, twister) = obj.Proxy.Model()

    i = i

    if bb.shape[0] < 5:
        print("zu wenig Punkte ")
        return

    # modifications
    b = np.concatenate([bb[0:i], bb[i+1:]])
    bb = b

    s = np.concatenate([scaler[0:i], scaler[i+1:]])
    scaler = s

    t = np.concatenate([twister[0:i], twister[i+1:]])
    twister = t

    # write back
    obj.Proxy.lock = False
    obj.Proxy.setModel(curve, bb, scaler, twister)
    obj.Proxy.showRib(i-2)


class RibEditor(QtGui.QWidget):

    def __init__(self, obj, title="undefined", pos=-1):

        super(RibEditor, self).__init__()
        self.title = title
        self.pos = pos
        self.obj = obj
        print(self.obj.Spreadsheet.Label)
        self.initUI()

    def initUI(self):

        self.btn = QtGui.QPushButton('Init A Model', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(initmodel)

#        self.btn = QtGui.QPushButton('Add Point', self)
#        self.btn.move(20, 50)
#        self.btn.clicked.connect(self.showDialog)

        self.btn = QtGui.QPushButton('Delete Rib', self)
        self.btn.move(20, 50)
        def f(): return delRib(self)
        self.btn.clicked.connect(f)

        self.btn = QtGui.QPushButton('Add Rib', self)
        self.btn.move(20, 80)
        def f(): return addRib(self)

        self.btn.clicked.connect(f)

        self.btn2 = QtGui.QPushButton('End', self)
        self.btn2.move(20, 110)
        self.btn2.clicked.connect(self.close)

        self.btn = QtGui.QPushButton('Add strong rib', self)
        self.btn.move(20, 140)
        def f(): return addStrongRibEdge(self)
        self.btn.clicked.connect(f)

        self.btn = QtGui.QPushButton('Add 2 neighbor ribs', self)
        self.btn.move(20, 140)
        def f(): return addNeighborRibs(self)
        self.btn.clicked.connect(f)

        self.le = QtGui.QLineEdit(self)
        self.le.setText("pos " + str(self.pos))
        self.le.move(150, 22)

        self.setGeometry(50, 30, 390, 250)
        self.setWindowTitle(self.title)
        self.show()
        try:
            self.obj.Proxy.dialog.hide()
        except:
            pass
        self.obj.Proxy.dialog = self

    def showDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
                                              'Enter your name:')

        if ok:
            self.le.setText(str(text))


class BackboneEditor(QtGui.QWidget):

    def __init__(self, obj, title="undefined", pos=-1):

        super(BackboneEditor, self).__init__()
        self.title = title
        self.pos = pos
        self.obj = obj
        print(self.obj.Spreadsheet.Label)
        self.initUI()

    def initUI(self):

        self.btn = QtGui.QPushButton('Init Model', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(initmodel)

#        self.btn = QtGui.QPushButton('Add Point', self)
#        self.btn.move(20, 50)
#        self.btn.clicked.connect(self.showDialog)

        self.btn = QtGui.QPushButton('Delete Meridian', self)
        self.btn.move(20, 50)
        self.btn.clicked.connect(lambda: delMeridian(self))

        self.btn = QtGui.QPushButton('Add Meridian', self)
        self.btn.move(20, 80)
        self.btn.clicked.connect(lambda: addMeridian(self))

        self.btn2 = QtGui.QPushButton('End', self)
        self.btn2.move(20, 110)
        self.btn2.clicked.connect(self.close)

        self.btn = QtGui.QPushButton('Add strong meridian', self)
        self.btn.move(20, 140)
        def f(): return addStrongMeridianEdge(self)
        self.btn.clicked.connect(f)

        self.btn = QtGui.QPushButton('Add 2 neighbor meridians', self)
        self.btn.move(20, 140)
        def f(): return addNeighborMeridians(self)
        self.btn.clicked.connect(f)

        self.le = QtGui.QLineEdit(self)
        self.le.setText("pos " + str(self.pos))
        self.le.move(150, 22)

        self.setGeometry(50, 30, 390, 250)
        self.setWindowTitle(self.title)
        self.show()
        try:
            self.obj.Proxy.dialog.hide()
        except:
            pass
        self.obj.Proxy.dialog = self

    def showDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
                                              'Enter your name:')

        if ok:
            self.le.setText(str(text))


def pressed(index, obj):
    sel, ci, ri, data = getdata(index)
    if sel == "bcmd":
        App.t = RibEditor(obj, "Rib Editor", ri)
    elif sel == "ccmd":
        App.t = BackboneEditor(obj, "Backbone Editor", ri)
    else:
        pass


def cmdAdd():
    ''' add some curves to selections '''

    s = FreeCADGui.Selection.getSelectionEx()[0]

    s.Object.Label
    print(s.Object.Name)
    print(s.SubElementNames)

    needle = s.Object.InList[0]
    needle.Label

    for sen in s.SubElementNames:
        print(sen[4:])
        if s.Object.Name[0:4] == 'Ribs':
            print("ribs ...")
            CaddRib(needle, int(sen[4:]))
        if s.Object.Name[0:9] == 'Meridians':
            print("meridians ...")
            CaddMeridian(needle, int(sen[4:]))


def cmdDel():
    ''' add some curves to selections '''

    s = FreeCADGui.Selection.getSelectionEx()[0]

    s.Object.Label
    print(s.Object.Name)
    print(s.SubElementNames)

    needle = s.Object.InList[0]
    needle.Label

    for sen in s.SubElementNames:
        print(sen[4:])
        if s.Object.Name[0:4] == 'Ribs':
            print("ribs ...")
            CdelRib(needle, int(sen[4:]))
        if s.Object.Name[0:9] == 'Meridians':
            print("meridians ...")
            CdelMeridian(needle, int(sen[4:]))
