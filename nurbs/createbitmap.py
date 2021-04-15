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

'''create_degree1_surface.py'''

from PySide import QtGui, QtCore
import PySide
import time
import Design456Init
import os

try:
    import numpy as np
except ImportError:
    print("Please install the required module : numpy")

import FreeCAD as App
import FreeCADGui as Gui
import Part


class Nurbs_CreateBtimap:
    def Activated(self):
        rc = self.dialog()

    def dialog(self):

        w = QtGui.QWidget()

        box = QtGui.QVBoxLayout()
        w.setLayout(box)
        w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        l = QtGui.QLabel("String")
        box.addWidget(l)
        w.anz = QtGui.QLineEdit()
        w.anz.setText('OK')
        box.addWidget(w.anz)

        l = QtGui.QLabel("Degree")
        box.addWidget(l)
        w.degree = QtGui.QLineEdit()
        w.degree.setText('0')
        box.addWidget(w.degree)

        w.r = QtGui.QPushButton("run")
        box.addWidget(w.r)
        w.r.pressed.connect(lambda: self._run(w))
        w.progressbar = QtGui.QProgressBar()
        box.addWidget(w.progressbar)

        w.show()
        return w

    def _run(self,window):
        self.qrcodeFace(message=window.anz.text(), degree=int(
            window.degree.text()), showPoints=False, window=window)
        App.ActiveDocument.recompute()

    def qrcodeFace(self,message='qr', degree=2, showPoints=False, window=None):
        # bitmuster as string

        ts = time.time()

        import pyqrcode
        #number = pyqrcode.create('http://www.freecadweb.org')

        number = pyqrcode.create(message)
        print(number.text())

        s = number.text()
        lns = s.splitlines()
        l = len(lns)

        pts = []
        for x in range(l):
            for y in range(l):
                pts.append(App.Vector(x, y, float(str(lns[x][y]))))

        if 0:  # idee zweite bild ueberlagern
            number2 = pyqrcode.create('abbceraaaYaaawqwqwwr')
            s2 = number2.text()
            lns2 = s2.splitlines()
            l2 = len(lns2)
            assert l2 == l

            pts = []
            for x in range(l):
                for y in range(l):
                    pts.append(App.Vector(x, y, float(
                        str(lns[x][y]))+float(str(lns2[x][y]))))

        du = degree
        if du == 0:
            du = 1
        dv = du

        if degree == 1 or degree == 0:
            cu = int(len(pts)**0.5)
            print(cu)

            pts = np.array(pts)
            pts1 = pts.reshape(cu, cu, 3)

            ptsa = []
            for r in pts1:
                r2 = r.copy()
                r2[:, 0] += 0.5
                ptsa += [r, r2]

            ptsa = np.array(ptsa)
            pts1 = ptsa.swapaxes(0, 1)

            ptsa = []
            for r in pts1:
                r2 = r.copy()
                r2[:, 1] += 0.5
                ptsa += [r, r2]

            pts2 = np.array(ptsa)

        if du == 2 or du == 3:
            cu = int(len(pts)**0.5)
            print(cu)

            pts = np.array(pts)
            pts1 = pts.reshape(cu, cu, 3)

            ptsa = []
            for r in pts1:
                r2 = r.copy()
                r2[:, 0] += 0.33
                r3 = r.copy()
                r3[:, 0] += 0.67

                ptsa += [r, r2, r3]

            ptsa = np.array(ptsa)
            pts1 = ptsa.swapaxes(0, 1)

            ptsa = []
            for r in pts1:
                r2 = r.copy()
                r2[:, 1] += 0.33
                r3 = r.copy()
                r3[:, 1] += 0.67

                ptsa += [r, r2, r3]

            pts2 = np.array(ptsa)

        (cu, cv, _t) = pts2.shape

        kvs = [1.0/(cv-dv)*i for i in range(cv-dv+1)]
        kus = [1.0/(cu-du)*i for i in range(cu-du+1)]

        mv = [dv+1]+[1]*(cv-dv-1)+[dv+1]
        mu = [du+1]+[1]*(cu-du-1)+[du+1]

        bs = Part.BSplineSurface()

        bs.buildFromPolesMultsKnots(pts2, mv, mu, kvs, kus,
                                    False, False,
                                    dv, du,
                                    )

        if degree > 0:
            obname = 'MyBitmap_'+str(degree)
            fa = App.ActiveDocument.getObject(obname)
            if fa == None:
                fa = App.ActiveDocument.addObject('Part::Spline', obname)
            fa.Label = obname+": "+message
            fa.ViewObject.DisplayMode = u"Shaded"
            fa.ViewObject.hide()

        try:
            fg = App.ActiveDocument.MyBitmap_Grid
        except:
            fg = App.ActiveDocument.addObject('Part::Spline', 'MyBitmap_Grid')

        d = 5
        bv = len(kvs)
        bu = len(kus)

        if window != None:
            window.progressbar.setValue(0)

        if 1:
            sps = []
            for a in range(0, bv):
                sps.append(bs.uIso(kvs[a]).toShape())

                App.ActiveDocument.recompute()
                Gui.updateGui()
                fg.Shape = Part.Compound(sps)

                if window != None:
                    window.progressbar.setValue(10*a/bv)

            for b in range(0, bu):
                sps.append(bs.vIso(kus[b]).toShape())

                App.ActiveDocument.recompute()
                Gui.updateGui()
                fg.Shape = Part.Compound(sps)

                if window != None:
                    window.progressbar.setValue(10+10*b/bu)

        if degree > 0:
            sps = []
            for a in range(0, bv/d+1):
                if window != None:
                    window.progressbar.setValue(100*a/(bv/d))
                App.Console.PrintMessage(" "+str(a))
                for b in range(0, bu/d+1):
                    d = 5
                    bs2 = bs.copy()
    #                print (d*a+d,d*b+d)
                    if d*a+d >= len(kvs):
                        kv = len(kvs)-1
                    else:
                        kv = d*a+d
                    if d*b+d >= len(kus):
                        ku = len(kus)-1
                    else:
                        ku = d*b+d

                    try:
                        bs2segment(kvs[d*a], kvs[kv], kus[d*b], kus[ku])
                        sh = bs2.toShape()
                        sps.append(sh)
                    except:
                        pass
                    App.ActiveDocument.recompute()
                    Gui.updateGui()
                    fa.Shape = Part.Compound(sps)

            fa.ViewObject.show()

        if 0:  # laufzeittest
            a = 0
            b = 0
            for d in range(3, 3):
                tss = time.time()
                bs2 = bs.copy()
                bs2segment(kvs[d*a], kvs[d*a+d], kus[d*b], kvs[d*b+d])
                Part.show(bs2.toShape())
                print(d, len(kvs)**2*(time.time()-tss)/d**2)

        print("Runtime:", time.time()-ts)
        print("Message size:", len(message))

        if showPoints:

            import Points
            ptsa = [App.Vector(p) for p in pts2.reshape(cu*cu, 3)]
            Points.show(Points.Points(ptsa))
            App.ActiveDocument.ActiveObject.ViewObject.ShapeColor = (
                1., 0., 0.)
            App.ActiveDocument.ActiveObject.ViewObject.PointSize = 4

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'Nurbs2.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "NurbsTools"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Nurbs_CreateBtimap", Nurbs_CreateBtimap())
