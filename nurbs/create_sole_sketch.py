# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import curves
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

'''shoe sole object'''

from say import *
import Sketcher
import Design456Init

import Design456Init
def createsole(sk):
    '''create the basic geometry sketch for a sole with 12 segments'''
    LL = sk.LL

    lls = []
    for p in range(11):
        ll = sk.addGeometry(Part.LineSegment(App.Vector(
            10*p, 0, 0), App.Vector(10*p+10, 0, 0)), False)
        sk.toggleConstruction(ll)
        sk.addConstraint(Sketcher.Constraint('Horizontal', ll))
        print(ll)
        if ll > 0:
            sk.addConstraint(Sketcher.Constraint('Coincident', ll-1, 2, ll, 1))
            sk.addConstraint(Sketcher.Constraint('Equal', 0, ll))
        llast = ll
    sk.addConstraint(Sketcher.Constraint('Coincident', 0, 1, -1, 1))

    # for p in range(1,12):
    for p in range(0, 11):
        ll = sk.addGeometry(Part.LineSegment(App.Vector(
            10*p, 0, 0), App.Vector(10*p, 20, 0)), False)
        sk.toggleConstruction(ll)
        sk.addConstraint(Sketcher.Constraint('Vertical', ll))
        sk.addConstraint(Sketcher.Constraint('Coincident', p, 1, ll, 1))

    p = 11
    ll = sk.addGeometry(Part.LineSegment(App.Vector(
        10*p, 0, 0), App.Vector(10*p, 20, 0)), False)
#    sk.toggleConstruction(ll)
    sk.addConstraint(Sketcher.Constraint('Vertical', ll))
    sk.addConstraint(Sketcher.Constraint('Coincident', llast, 2, ll, 1))

    # for p in range(1,12):
    for p in range(0, 11):
        ll = sk.addGeometry(Part.LineSegment(App.Vector(
            10*p, 0, 0), App.Vector(10*p, -20, 0)), False)
        sk.toggleConstruction(ll)
        sk.addConstraint(Sketcher.Constraint('Vertical', ll))
        sk.addConstraint(Sketcher.Constraint('Coincident', p, 1, ll, 1))

    p = 11
    ll = sk.addGeometry(Part.LineSegment(App.Vector(
        10*p, 0, 0), App.Vector(10*p, -20, 0)), False)
#    sk.toggleConstruction(ll)
    sk.addConstraint(Sketcher.Constraint('Vertical', ll))
    sk.addConstraint(Sketcher.Constraint('Coincident', llast, 2, ll, 1))

    cLL = sk.addConstraint(Sketcher.Constraint('DistanceX', 10, 2, LL))
    # App.ActiveDocument.sohle.renameConstraint(cLL, u'LL')

    for p in range(11):
        print(p)
        p = 10-p
        #    if p!=12:
        # ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,-40.,0),App.Vector(10*p+10,-40.,0)),False)
        ll = sk.addGeometry(Part.LineSegment(App.Vector(
            10*p+10, -40., 0), App.Vector(10*p+0, -40., 0)), False)
        sk.addConstraint(Sketcher.Constraint('Coincident', 23+p, 2, ll, 1))
        sk.addConstraint(Sketcher.Constraint('Coincident', 24+p, 2, ll, 2))
#            else:
#                ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,-50.,0),App.Vector(10*p+10,-50.,0)),False)
#                sk.addConstraint(Sketcher.Constraint('Coincident',23+p,2,ll,1))
#                sk.addConstraint(Sketcher.Constraint('Coincident',11,2,ll,2))

    for p in range(11):
        print(p)
        ll = sk.addGeometry(Part.LineSegment(App.Vector(
            10*p, 40., 0), App.Vector(10*p+10, 40., 0)), False)
        sk.addConstraint(Sketcher.Constraint('Coincident', 11+p, 2, ll, 1))
        sk.addConstraint(Sketcher.Constraint('Coincident', 12+p, 2, ll, 2))

#            else:
#                ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,50.,0),App.Vector(10*p+10,50.,0)),False)
#                sk.addConstraint(Sketcher.Constraint('Coincident',12+p,2,ll,1))
#                sk.addConstraint(Sketcher.Constraint('Coincident',11,2,ll,2))

    if 0:

        if 1:
            ll = sk.addGeometry(Part.LineSegment(App.Vector(
                10*p, -50., 0), App.Vector(10*p+10, -50., 0)), False)
            sk.addConstraint(Sketcher.Constraint('Coincident', 0, 1, ll, 1))
            sk.addConstraint(Sketcher.Constraint('Coincident', 23, 2, ll, 2))

            ll = sk.addGeometry(Part.LineSegment(App.Vector(
                10*p, -50., 0), App.Vector(10*p+10, -50., 0)), False)
            sk.addConstraint(Sketcher.Constraint('Coincident', 0, 1, ll, 1))
            sk.addConstraint(Sketcher.Constraint('Coincident', 12, 2, ll, 2))

    App.ActiveDocument.recompute()


# Reload imported module
#import importlib
# importlib.#reload(curves)


class Sole(curves.OffsetSpline):
    '''Shoe sole as Sketch Object with Python'''

    # \cond
    def __init__(self, obj, icon=Design456Init.NURBS_ICON_PATH+'icons/draw.svg'):
        curves.OffsetSpline.__init__(
            self, obj, icon=Design456Init.NURBS_ICON_PATH+'icons/draw.svg')
        obj.Proxy = self
        self.Type = self.__class__.__name__
        self.obj2 = obj
        self.aa = None
    # \endcond

    def onChanged(proxy, obj, prop):
        '''change on lastlength, inner and outer offset'''
        if prop == 'LL':
            obj.setDatum(79, obj.LL)              # This is causing a problem .. I don't know what is index 79 Mariwan
        if prop not in ["ofin", "ofout"]:
            return
        curves.OffsetSpline.myExecute(obj)


#
#
#
#

class runSole():
    def __init__(self, LL=260,name="mySole"):
        self.LL=LL
        self.name=name
        
    '''create a default sole object'''
    def Activated(self):
        try:
            obj = App.ActiveDocument.addObject(
                "Sketcher::SketchObjectPython", self.name)
            obj.addProperty("App::PropertyInteger", "ofin",
                            "Base", "end").ofin = 10
            obj.addProperty("App::PropertyInteger", "ofout",
                            "Base", "end").ofout = 10
            obj.addProperty("App::PropertyInteger", "LL", "Base", "end").LL = self.LL

            Sole(obj)
            createsole(obj)
            obj.ViewObject.hide()
            App.activeDocument().recompute()

            import Draft
            img = Draft.makeRectangle(
                length=265., height=265., face=True, support=None)
            img.ViewObject.TextureImage = Design456Init.NURBS_ICON_PATH+"Foot_bg.png"
            img.Placement = App.Placement(
                App.Vector(-6, 133, 0), App.Rotation(App.Vector(0, 0, -1), 90))
            img.ViewObject.Selectable = False
        except Exception as err:
            App.Console.PrintError("'Design456_Nurbs RunSole' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    # return obj

    def GetResources(self):
        return {
            'Pixmap': Design456Init.NURBS_ICON_PATH + 'shoe.svg',
            'MenuText': 'shoe sole object',
                        'ToolTip':  'Nurbs shoe sole object'
        }

Gui.addCommand('runSole', runSole())
runSole.__doc__ = """To be added later
                            """
