import FreeCAD as App
import Points
import Part
import Draft
import numpy as np
import random
import scipy as sp
from scipy import signal

from PySide import QtGui
import sys
import traceback
import random

import FreeCADGui as Gui
import numpy as np
import Draft

if 0:
    pass

    # Hilfswire machen
    [a] = Gui.Selection.getSelection()
    bc = a.Shape.Edge1.Curve
    pts = a.Shape.Edge1.Curve.getPoles()
    # print  (len(pts)
    # Draft.makeWire(pts)
    #App.ActiveDocument.ActiveObject.Label="Poles "+a.Label

    pts = [bc.value(k) for k in bc.getKnots()]
    print(len(pts))
    Draft.makeWire(pts)
    App.ActiveDocument.ActiveObject.Label = "Knotes "+a.Label
    App.ActiveDocument.ActiveObject.ViewObject.PointSize = 10
    App.ActiveDocument.ActiveObject.ViewObject.PointColor = (1., 0., 0.)


def run():

    [a] = Gui.Selection.getSelectionEx()
    bc0 = a.Object.Shape.Edge1.Curve
    kc = len(bc0.getKnots())

    for pos in range(1, kc):
        print(pos)
        # for t in (30000,40000,10000,5000,2000,1000,500,200,100,50,20,10,5,3,2,1):
        # 1.5 und 1 gehen nicht
        for t in (20, 16, 14, 12, 6, 2, 1.5, 1):
            bc = bc0.copy()
            print("huhu")
            rc = bc.removeKnot(pos, 0, t)
            print(t, rc)
            if rc:
                sp = App.ActiveDocument.addObject(
                    "Part::Spline", "approx Spline")
                sp.Shape = bc.toShape()
                App.ActiveDocument.ActiveObject.Label = "BC-" + \
                    str(pos)+" "+str(t)+" " + a.Object.Label

            #    pts=bc.getPoles()
            #    print  (len(pts)
            #    Draft.makeWire(pts)
            #    App.ActiveDocument.ActiveObject.Label="W-"+str(pos)+" "+a.Object.Label
                if 0:
                    pts = [bc.value(k) for k in bc.getKnots()]
            #        print  (len(pts)
                    Draft.makeWire(pts)
                    App.ActiveDocument.ActiveObject.Label = "Kn " + \
                        str(t)+a.Object.Label
                    App.ActiveDocument.ActiveObject.ViewObject.PointSize = 12
                    App.ActiveDocument.ActiveObject.ViewObject.PointColor = (
                        0., 1., 0.)
