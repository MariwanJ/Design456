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

# -*- coding: utf-8 -*-
'''
# -------------------------------------------------
# -- methods for drawing on faces
# --
# -- microelly 2017 v 0.3
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------
'''

# \cond
from say import *

import FreeCAD as App
import FreeCADGui as Gui
import Design456Init


from PySide import QtGui
import Part
import Mesh
import Draft
import Points


import os

try:
    import numpy as np
except ImportError:
    print("Please install the required module : numpy")
    
import random

import os
# import scipy
# import scipy.interpolate

# import

import Design456Init

class PartFeature:
    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj

# grundmethoden zum sichern

    def attach(self, vobj):
        self.Object = vobj.Object

    def claimChildren(self):
        return self.Object.Group

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


class ViewProvider:
    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def onChanged(self, fp, prop):
        # print ("onChanged",prop)
        pass


# \endcond

class Nurbs_createShape:
    def __init__(self,obj):
        self.obj=obj
          
    def Activated(self, obj):
        '''create the 2D or 3D mapping Shape for a wire and a base face
        the data are parameters of the obj '''

    #    print ("CreateShape for obj:",obj.Label

        # pointCount=obj.pointcount
        # pointCount=50

        [uv2x, uv2y, xy2u, xy2v] = [self.obj.mapobject.Proxy.uv2x,
                                    self.obj.mapobject.Proxy.uv2y, self.obj.mapobject.Proxy.xy2u, self.obj.mapobject.Proxy.xy2v]

        if xy2v == None:
            print("Kann umkehrung nicht berechnen xy2v nicht vorhanden")
            return

        # diese daten vom mapobjekt lesen #+#

        mpv = 0.5
        mpu = 0.5

        u0 = 0
        v0 = 0

        fy = 1.
        fx = 1.

        # +# facenumer aus obj param holen
        face = self.obj.face.Shape.Face1
        bs = face.Surface
    #    w=obj.wire.Shape.Wires[0]
        wires = obj.wire.Shape.Wires
        if len(wires) == 0:
            wires = obj.wire.Shape.Edges

        ppall = []

        pos = App.Vector(self.obj.mapobject.Placement.Base.x,
                         self.obj.mapobject.Placement.Base.y, 0)

        for i, w in enumerate(wires):
            # print ("Wire ...",i,pointCount)
            App.w = w
            for i, ee in enumerate(w.Edges):
                ct = max(int(round(ee.Length/obj.pointdist)), 2)
                if i == 0:
                    ptsaa = ee.discretize(ct)
                else:
                    pts = ee.discretize(ct)
                    if pts[-1] == ptsaa[-1]:
                        pts = pts[::-1]
                    ptsaa += pts[1:]

            pts = [p-pos for p in ptsaa]

            pts2 = []

            # refpos geht noch nicht
            mpv = 0.
            mpu = 0.

    #        refpos=bs.value(mpu,mpv)
    #        print ("refpos",mpu,mpv)
    #        print refpos

            refpos = App.Vector(0, 0, 0)

            for p in pts:

                y = fx*(p.x-refpos.x)
                x = fy*(p.y-refpos.y)

                # fuer ruled surface !!
                x = fx*p.y
                y = fy*p.x

                u = xy2u(x, y)
                v = xy2v(x, y)

    # su=face.ParameterRange[1]
    # sv=face.ParameterRange[3]

                sua = face.ParameterRange[0]
                sva = face.ParameterRange[2]
                sue = face.ParameterRange[1]
                sve = face.ParameterRange[3]
                sul = sue-sua
                svl = sve-sva

                # sua + svl*
                # sva + svl*

                # try: sweep=obj.face.TypeId=='Part::Sweep'
                # except: sweep=True

                if obj.mapobject.flipuv23:
                    p2 = bs.value(u, v)
                else:
                    p2 = bs.value(sva+u*svl, aua+v*sul)

                pts2.append(p2)

            App.pts2a = pts2
            self.obj.Shape = Part.makePolygon(pts2)



class Isodraw(PartFeature):
    '''a Drawing of a curve onto a Face with the points of a wire'''

    def __init__(self, obj):
        PartFeature.__init__(self, obj)
#        obj.addProperty("App::PropertyVector","Size","Base").Size=App.Vector(300,-100,200)
        obj.addProperty("App::PropertyLink", "face", "Source")
        obj.addProperty("App::PropertyLink", "wire", "Source")
        obj.addProperty("App::PropertyLink", "mapobject",
                        "Details", "configuration objekt for mapping")
        obj.addProperty("App::PropertyBool", "drawFace", "Output",
                        "display subface cut by the wire projection")
        obj.addProperty("App::PropertyBool", "reverseFace",
                        "Output", "display inner or outer subface")
#        obj.addProperty("App::PropertyInteger","pointcount","Details","count of points to discretize source wire")
#
#        obj.pointcount=100

        obj.addProperty("App::PropertyInteger", "pointdist", "Details",)
        obj.pointdist = 1000

        obj.addProperty("App::PropertyLink", "backref", "Workspace")

        ViewProvider(obj.ViewObject)
        obj.ViewObject.LineColor = (1., 0., 1.)

#    def onChanged(self, fp, prop):
#        print ("onChanged",prop)

    def execute(proxy, obj):
        Nurbs_createShape(obj)
        if  obj.backref != None:
            obj.backref.touch()
            obj.backref.Document.recompute()
        face = obj.face.Shape.Face1
        facedraw
        #reload(facedraw)
        try:
            obj.ViewObject.ShapeColor = obj.wire.ViewObject.ShapeColor
        except:
            obj.ViewObject.ShapeColor = (1., 0., 0.)

        facedraw.drawcurve(obj, face)


class Nurbs_createIsodrawFace:
    def Activated(self):
        '''creates a IsoDrawFace object'''
        b = App.ActiveDocument.addObject("Part::FeaturePython", "IsoDrawFace")
        Isodraw(b)
        return b

    def GetResources(self):
        return {
            'Pixmap': Design456Init.NURBS_ICON_PATH + 'drawing.svg',
            'MenuText': 'Nurbs_createIsodrawFace',
            'ToolTip':  'Nurbs_createIsodrawFace'
        }


Gui.addCommand('Nurbs_createIsodrawFace', Nurbs_createIsodrawFace())
Nurbs_createIsodrawFace.__doc__ = """createIsodrawFace: Tobe added later     """

# ------------------------------------------------------


class Brezel(PartFeature):
    '''a Drawing of a curve onto a Face with the points of a wire'''

    def __init__(self, obj):
        PartFeature.__init__(self, obj)
#        obj.addProperty("App::PropertyVector","Size","Base").Size=App.Vector(300,-100,200)
        obj.addProperty("App::PropertyLink", "face", "Source")
        obj.addProperty("App::PropertyLink", "wire1", "Source")
        obj.addProperty("App::PropertyLink", "wire2", "Source")
        obj.addProperty("App::PropertyLink", "wire3", "Source")
        obj.addProperty("App::PropertyLink", "wire4", "Source")
        obj.addProperty("App::PropertyBool", "reverseWire1", "Source")
        obj.addProperty("App::PropertyBool", "reverseWire2", "Source")
        obj.addProperty("App::PropertyBool", "reverseWire3", "Source")
        obj.addProperty("App::PropertyBool", "reverseWire4", "Source")
        # obj.addProperty("App::PropertyLink","mapobject","Details","configuration object for mapping")
        # obj.addProperty("App::PropertyBool","drawFace","Output","display subface cut by the wire projection")
        # obj.addProperty("App::PropertyBool","reverseFace","Output","display inner or outer subface")
        # obj.addProperty("App::PropertyInteger","pointcount","Details","count of points to discretize source wire")
        # obj.pointcount=100
        obj.reverseWire2 = True

        obj.addProperty("App::PropertyLink", "backref", "Workspace")

        ViewProvider(obj.ViewObject)
        obj.ViewObject.LineColor = (1., 0., 1.)

#    def onChanged(self, fp, prop):
#        print ("onChanged",prop)

    def execute(proxy, obj):
        # createShape(obj)
        if obj.backref != None:
            obj.backref.touch()
            obj.backref.Document.recompute()
        # face=obj.face.Shape.Face1

        facedraw
        # #reload(.facedraw)
        try:
            obj.ViewObject.ShapeColor = obj.wire.ViewObject.ShapeColor
        except:
            obj.ViewObject.ShapeColor = (1., 0., 0.)

        # outside edge 
        wire1 = obj.wire1
        # innenrand fuer erstes loch
        wire2 = obj.wire2

        wires = []
        for w in [obj.wire1, obj.wire2, obj.wire3, obj.wire4]:
            if w != None:
                wires += [w]

        # faceobj=App.ActiveDocument.face
        faceobj = obj.face  # .Shape.Face1

#        dirs=[False,True,True]
        dirs = [obj.reverseWire1, obj.reverseWire2,
                obj.reverseWire3, obj.reverseWire4, ]
        facedraw.drawring(
            obj.Label, wires, dirs, faceobj, facepos=App.Vector())


class createBrezel:
    def Activated(self):
        '''creates a IsoDrawFace object'''
        b = App.ActiveDocument.addObject("Part::FeaturePython", "Brezel")
        Brezel(b)
        if 1:
            b.face = App.ActiveDocument.face
            b.wire1 = App.ActiveDocument.IsoDrawFace002
            b.wire2 = App.ActiveDocument.IsoDrawFace003
            b.wire3 = App.ActiveDocument.IsoDrawFace
            b.wire4 = App.ActiveDocument.IsoDrawFace004
        return b

    def GetResources(self):
        return {
            'Pixmap': Design456Init.NURBS_ICON_PATH + 'drawing.svg',
            'MenuText': 'testD',
            'ToolTip':  'testD'
        }


Gui.addCommand('createBrezel', createBrezel())
createBrezel.__doc__ = """createBrezel: Tobe added later     """

# -------------------------------------------------------------


class MapVP(ViewProvider):

    def setupContextMenu(self, obj, menu):
        menu.clear()
        action = menu.addAction("Display 2D Grid")
        action.triggered.connect(lambda: self.display2DGrid(obj.Object))
        action = menu.addAction("Display 3D Grid")
        action.triggered.connect(lambda: self.display3DGrid(obj.Object))

    def display2DGrid(self, obj):
        obj.display2d = not obj.display2d
        obj.Proxy.execute(obj)
        App.ActiveDocument.recompute()

    def display3DGrid(self, obj):
        obj.display3d = not obj.display3d
        obj.Proxy.execute(obj)
        App.ActiveDocument.recompute()


class Map(PartFeature):
    def __init__(self, obj, mode=''):
        PartFeature.__init__(self, obj)
        obj.addProperty("App::PropertyVector", "Size",
                        "Base").Size = App.Vector(300, -100, 200)
# obj.addProperty("App::PropertyLink","face","Base")
        obj.addProperty("App::PropertyLink", "faceObject", "Base")
        obj.addProperty("App::PropertyEnumeration", "mode",
                        "Base").mode = ['', 'curvature']
        obj.addProperty("App::PropertyEnumeration", "modeCurvature",
                        "Base").modeCurvature = ["Gauss", "Min", "Max", "Mean"]
        obj.addProperty("App::PropertyInteger", "factorCurvature",
                        "Base").factorCurvature = 1000000
        # raender
        obj.addProperty("App::PropertyInteger", "border",
                        "UV Interpolation", "border offset in uv space")
        obj.addProperty("App::PropertyInteger", "ub", "UV Interpolation",
                        "minimum u value for interpolation base")
        obj.addProperty("App::PropertyInteger", "ue", "UV Interpolation",
                        "maximum u value for interpolation base")
        obj.addProperty("App::PropertyInteger", "vb", "UV Interpolation",
                        "minimum v value for interpolation base")
        obj.addProperty("App::PropertyInteger", "ve", "UV Interpolation",
                        "minimum v value for interpolation base")
        obj.addProperty("App::PropertyInteger", "uc",
                        "UV Interpolation", "count u segments")
        obj.addProperty("App::PropertyInteger", "vc",
                        "UV Interpolation", "count v segments")
#        obj.addProperty("App::PropertyInteger","uCount","Interpolation","count u segments").uCount=30
#        obj.addProperty("App::PropertyInteger","vCount","Interpolation","count v segments").vCount=30

        obj.addProperty("App::PropertyEnumeration", "modeA",
                        "UV Interpolation", "interpolation mode uv to iso-xy")
        obj.modeA = ['cubic', 'linear']
        obj.addProperty("App::PropertyEnumeration", "modeB",
                        "UV Interpolation", "interpolation mode iso-xy to uv")
        obj.modeB = ['thin_plate', 'cubic', 'linear']

        obj.addProperty("App::PropertyInteger", "pointsPerEdge",
                        "Map", "discretize for 3D to 2D")
        obj.pointsPerEdge = 3

        # mitte
#        obj.addProperty("App::PropertyFloat","vm","Map","v center")
#        obj.addProperty("App::PropertyFloat","um","Map","u center")

#        obj.addProperty("App::PropertyFloat","fx","Map","Scale factor for x").fx=-1.
#        obj.addProperty("App::PropertyFloat","fy","Map","Scale factor for y").fy=-1.


#        obj.vm=0.5
#        obj.um=0.5

        obj.mode = mode
        obj.ve = -1
        obj.ue = -1

        obj.border = 0
        obj.ub = 10
        obj.vb = 10
        obj.ue = 21
        obj.ve = 21

        obj.uc = 30
        obj.vc = 30

        obj.addProperty("App::PropertyLink", "backref", "Base")

        obj.addProperty("App::PropertyInteger", "faceNumber", "Base")

        obj.addProperty("App::PropertyLink", "wire", "Base")

        obj.addProperty("App::PropertyInteger", "uMin", "Base")
        obj.addProperty("App::PropertyInteger", "uMax", "Base")
        obj.addProperty("App::PropertyInteger", "uCenter", "Base")
        obj.addProperty("App::PropertyInteger", "uCount", "Base")

        obj.addProperty("App::PropertyInteger", "vMin", "Base")
        obj.addProperty("App::PropertyInteger", "vMax", "Base")
        obj.addProperty("App::PropertyInteger", "vCenter", "Base")
        obj.addProperty("App::PropertyInteger", "vCount", "Base")

        obj.addProperty("App::PropertyBool", "flipuv", "Base")
        obj.addProperty("App::PropertyBool", "flipxy", "Base")

        obj.addProperty("App::PropertyFloat", "fx", "Base")
        obj.addProperty("App::PropertyFloat", "fy", "Base")

        obj.addProperty("App::PropertyFloat", "vMapCenter", "Map")
        obj.addProperty("App::PropertyFloat", "uMapCenter", "Map")

        obj.addProperty("App::PropertyBool", "display2d", "Map")
        obj.addProperty("App::PropertyBool", "display3d", "Map")
        obj.addProperty("App::PropertyBool", "displayCircles", "Map")
        obj.addProperty("App::PropertyBool", "flipuv23", "Map").flipuv23 = True

        obj.display2d = True
        obj.display3d = True

        obj.fx = 1.
        obj.fy = 1.
        obj.flipxy = True

        obj.uMapCenter = 50
        obj.vMapCenter = 50

        obj.uCount = 30
        obj.vCount = 30

        obj.uMax = 31
        obj.uMin = 1
        obj.vMax = 31
        obj.vMin = 1

        if obj.mode == 'curvature':

            obj.uCount = 100
            obj.vCount = 100

            obj.uMax = 101
            obj.uMin = 1
            obj.vMax = 101
            obj.vMin = 1
            obj.display3d = False

        # test config
        # obj.mode='curvature'
        # obj.flipuv=True
        obj.modeCurvature = "Gauss"

        # ViewProvider(obj.ViewObject)
        MapVP(obj.ViewObject)
        obj.ViewObject.LineColor = (1., 0., 1.)
        obj.ViewObject.LineWidth = 1

    def onBeforeChange(self, fp, prop):
        #        print ("onbeforeChange", fp.Label,prop,getattr(fp,prop))
        if prop == "uCount":
            self.pc = prop
            self.val = getattr(fp, prop)
        if prop == "vCount":
            self.pc = prop
            self.val = getattr(fp, prop)

    def onChanged(self, fp, prop):
        #        print ("onChanged", fp.Label,prop,getattr(fp,prop))
        try:
            z = [fp.uMax, fp.vMax, fp.uMin, fp.vMin]
        except:
            return
        if prop == "uCount":
            vn = getattr(fp, prop)
            vo = self.val
            if vo == 0:
                return
            fp.uMax = fp.uMax*vn/vo
            fp.uMin = fp.uMin*vn/vo
        if prop == "vCount":
            vn = getattr(fp, prop)
            vo = self.val
            if vo == 0:
                return
            fp.vMax = fp.vMax*vn/vo
            fp.vMin = fp.vMin*vn/vo

    def execute(proxy, obj):
        '''get the mapping of the obj.face, create the 2D and 3D grid for the mapping'''

        [uv2x, uv2y, xy2u, xy2v] = getmap(obj, obj.faceObject)
        proxy.uv2x = uv2x
        proxy.uv2y = uv2y
        proxy.xy2u = xy2u
        proxy.xy2v = xy2v

        # obj.faceObject=obj.face
        cps = []
        if obj.display2d:
            cps.append(createGrid(obj))
        if obj.display3d:
            cps.append(createGrid(obj, upmode=True))

        pl = obj.Placement
        obj.Shape = Part.Compound(cps)
        obj.Placement = pl

        if obj.backref != None:
            obj.backref.touch()
            obj.backref.Document.recompute()

    def onDocumentRestored(proxy, obj):

        print("onDocumentRestored(proxy,obj)", proxy, obj, obj.Label)

        [uv2x, uv2y, xy2u, xy2v] = getmap(obj, obj.faceObject)
        proxy.uv2x = uv2x
        proxy.uv2y = uv2y
        proxy.xy2u = xy2u
        proxy.xy2v = xy2v
        print("getmap done")


class createMap:
    def Activated(self, mode=''):
        '''create a Map object'''
        b = App.ActiveDocument.addObject("Part::FeaturePython", "MAP")
        Map(b, mode=mode)

        # hack
        b.display2d = False
        b.displayCircles = True
        b.uMin = 0
        b.vMin = 0

        if 0:
            b.modeCurvature = "Gauss"
            b.uMin = 20
            b.vMin = 0
            b.uMax = 50
            b.vMax = 101
        return b

    def GetResources(self):
        return {
            'Pixmap': Design456Init.NURBS_ICON_PATH + 'drawing.svg',
            'MenuText': 'testD',
            'ToolTip':  'testD'
        }


Gui.addCommand('createMap', createMap())
createMap.__doc__ = """createMap: Tobe added later     """


class createGrid:
    def Activated(mapobj, upmode=False):
        '''create a 2D grid  or 3D grid (if upmode) for the map obj'''

        obj = mapobj

        try:
            face = obj.faceObject.Shape.Faces[obj.faceNumber]
            bs = face.Surface
        except:
            return Part.Shape()

        print("createGrid for special faces")
        print(face)
        import os

        sf = face.Surface

        if sf.__class__.__name__ == 'Cone':

            alpha, beta, hmin, hmax = face.ParameterRange

            r2 = sf.Radius
            r1 = (sf.Apex-sf.Center).Length

            alpha = r2*np.pi/r1

            su = 21
            sv = 21

            pts = np.zeros(su*sv*3).reshape(su, sv, 3)

            comp = []
            for u in range(su):
                for v in range(sv):
                    # print (beta-alpha)*u/2
                    p = App.Vector((r1+hmax*v/sv)*np.cos((alpha)*u/su),
                                   (r1+hmax*v/sv)*np.sin((alpha)*u/su))
                    pts[u, v] = p

            for z in pts:
                comp += [Part.makePolygon([App.Vector(p) for p in z])]

            pts = pts.swapaxes(0, 1)
            for z in pts:
                comp += [Part.makePolygon([App.Vector(p) for p in z])]

            # Part.show(Part.Compound(comp))

            return Part.Compound(comp)


#       face=obj.faceObject.Shape.Face1

#       mpu=obj.uMapCenter/100
#       mpv=obj.vMapCenter/100

        mpv = obj.uMapCenter/100
        mpu = obj.vMapCenter/100

        # skalierung/lage
        fx = obj.fx
        fy = obj.fy

        fz = 1.0

        comps = []

        refpos = bs.value(mpv, mpu)

        # su=bs.UPeriod()
        # sv=bs.VPeriod()

        print("hack DD suu asv")
        su = face.ParameterRange[1]
        sv = face.ParameterRange[3]

        if su > 1000:
            su = face.ParameterRange[1]
        if sv > 1000:
            sv = face.ParameterRange[3]

        # mittelpunkt

#       try: sweep=obj.Faceobject.TypeId=='Part::Sweep'
#       except: sweep=True

        sua = face.ParameterRange[0]
        sva = face.ParameterRange[2]
        sue = face.ParameterRange[1]
        sve = face.ParameterRange[3]
        sul = sue-sua
        svl = sve-sva

        # sua + svl*
        # sva + svl*

        if not obj.flipuv23:

            mpu2 = sva+mpu*svl
            mpv2 = aza+mpv*sul

        else:
            if upmode:
                mpu2 = sua+mpu*sul
                mpv2 = sva+mpv*svl
            else:
                mpu2 = sva+mpu*svl
                mpv2 = sua+mpv*sul

        mpu = mpv2
        mpv = mpu2

        vc = obj.uCount
        uc = obj.vCount

        print("isodraw #ll")
        print(su, sv)
        print(uc, vc)
        print(face.ParameterRange)

        ptsa = []
        ptska = []

        ba = bs.uIso(mpu)
        comps += [ba.toShape()]

        for v in range(vc+1):
            pts = []
            vm = sva+1.0/vc*v*svl

            ky = ba.length(vm, mpv)

            if vm < mpv:
                ky = -ky
            bbc = bs.vIso(vm)

            comps += [bbc.toShape()]

            ptsk = []
            for u in range(uc+1):
                uv = sua+1.0/uc*u*sul

                ba = bs.uIso(uv)

                ky = ba.length(vm, mpv)
                if vm < mpv:
                    ky = -ky

                kx = bbc.length(mpu, uv)
                if uv < mpu:
                    kx = -kx

                # ptsk.append(bs.value(vm,uv))
                ptsk.append(bs.value(uv, vm))

                pts.append([kx, ky, 0])
                # print ("isodraw nknk",uv,vm,bs.value(uv,vm))

            ptsa.append(pts)
            ptska.append(ptsk)

#    -----------------------------------------------

        [uv2x, uv2y, xy2u, xy2v] = getmap(mapobj, obj.faceObject)

        print("hier 3D Methode  ccc..oo..............")
        if obj.mode == 'curvature':
            [uv2x, uv2y, uv2z, xy2u, xy2v] = getmap3(mapobj, obj.faceObject)
        ptsa = []

        for v in range(vc+1):
            pts = []
            z2 = 0
            z = 0
            for u in range(uc+1):

                if mapobj.flipuv:
                    uv = sua+1.0/uc*u*sul
                    vv = sva+1.0/vc*v*svl
                    vv2 = sva+1.0/uc*u*svl
                    uv2 = sua+1.0/vc*v*sul
                else:
                    vv = sua+1.0/uc*u*sul
                    uv = sva+1.0/vc*v*svl
                    uv2 = sva+1.0/uc*u*svl
                    vv2 = sua+1.0/vc*v*sul


#                   try: sweep=face.TypeId=='Part::Sweep'
#                   except: sweep=True
#
#                   sweep=True

                if 1 or (mapobj.flipuv23 and upmode):
                    #                    print ("---------------------------RRRRRRRRRRRRRRRRRRR"
                    #                    x=uv2x(vv,uv)
                    #                    y=uv2y(vv,uv)
                    # uv=sua+1.0/uc*(uc-u)*sul
                    uv = sua+1.0/uc*(u)*sul
#    vv=sva+1.0/vc*(vc-v)*svl
                    vv = sva+1.0/vc*(v)*svl

                    x = uv2x(uv, vv)
                    y = uv2y(uv, vv)
#                       x=uv2x(vv,uv)
#                       y=uv2y(vv,uv)

                else:
                    x = uv2x(uv, vv)
                    y = uv2y(uv, vv)

                if obj.mode == 'curvature':
                    # z=uv2z(uv,vv)
                    # drekt nutzen statt interpolator
                    # z=bs.curvature(vv,uv,"Mean")
                    try:
                        z2 = bs.curvature(uv2, vv2, obj.modeCurvature)
                    except:
                        z2 = 0

                    if z2 != 0:
                        r = round(1.0/z2)
                    else:
                        r = 'planar'
                    if u >= mapobj.vMin-1 and u <= mapobj.vMax+1 and v >= mapobj.uMin-1 and v <= mapobj.uMax+1:
                        print("u,v, curvature,radius ", u, v, round(z2, 6), r)

                        if abs(z2) > 0.001:
                            print("********** HIGH", u, v, z2, r)

                    z = obj.factorCurvature*z2

                else:
                    z = 0
                # print z
#                   print (x,y,z)
                pts.append(App.Vector(x, y, z))

#                   if u==5:
#                       print ("aadfdbbw--",uv,vv,z)
#                       print (x,y)

            ptsa.append(pts)

        if upmode:
            print("Rahmen 3D", obj.uMin, obj.uMax, obj.vMin, obj.vMax)
            print(obj.faceObject.TypeId)

#           try: sweep=obj.faceObject.TypeId=='Part::Sweep'
#           except: sweep=True

#           sweep=True
            if not obj.flipuv23:
                uMin, uMax, vMin, vMax = obj.uMin, obj.uMax, obj.vMin, obj.vMax
            else:
                vMin, vMax, uMin, uMax = obj.uMin, obj.uMax, obj.vMin, obj.vMax

            relpos = obj.Placement.Base*(-1)

            comps = []

            for pts in ptska[uMin:uMax]:

                ll = []
                for p in pts[vMin:vMax]:
                    pmh = obj.Placement.inverse()
                    vh = App.Vector(tuple(p))
                    th = App.Placement()
                    th.Base = vh
                    t2 = pmh.multiply(th)
                    vh2 = t2.Base
                    ll += [vh2]
                try:
                    comps += [Part.makePolygon(ll)]
                except:
                    pass

            '''
            comps=[]

            for pts in ptska[obj.vMin:obj.vMax]:

                ll=[]
                for p in pts[obj.uMin:obj.uMax]:
                    pmh=obj.Placement.inverse()
                    vh=App.Vector(tuple(p))
                    th=App.Placement()
                    th.Base=vh
                    t2=pmh.multiply(th)
                    vh2=t2.Base
                    ll += [vh2]

                comps += [ Part.makePolygon(ll) ]

            '''

            ptska = np.array(ptska).swapaxes(0, 1)

            for pts in ptska[vMin:vMax]:

                ll = []
                for p in pts[uMin:uMax]:
                    pmh = obj.Placement.inverse()
                    vh = App.Vector(tuple(p))
                    th = App.Placement()
                    th.Base = vh
                    t2 = pmh.multiply(th)
                    vh2 = t2.Base
                    ll += [vh2]

                comps += [Part.makePolygon(ll)]

            # markiere zentrum der karte
            z = bs.value(sua+0.5*sul, sva+0.5*svl)
            circ = Part.Circle()
            circ.Radius = 10

            th = App.Placement()
            th.Base = z
            t2 = pmh.multiply(th)
            circ.Location = t2.Base

            th = App.Placement()
            th.Base = bs.normal(sua+0.5*sul, sva+0.5*svl)
            t2 = pmh.multiply(th)

            circ.Axis = t2.Base
            if obj.displayCircles:
                comps += [circ.toShape()]

            # mapcenter

            z = bs.value(mpu, mpv)
            z = bs.value(mpv, mpu)

            circ = Part.Circle()
            circ.Radius = 20

            th = App.Placement()
            th.Base = z
            t2 = pmh.multiply(th)
            circ.Location = t2.Base

            th = App.Placement()
            th.Base = bs.normal(mpv, mpu)
            t2 = th.multiply(pmh)
#           t2=pmh.multiply(th)

            # diese richtung stimmt noch nicht, deaktivert
#    circ.Axis=t2.Base

            if obj.displayCircles:
                comps += [circ.toShape()]
            return Part.Compound(comps)

        else:  # 2d mode
            comps = []

            # markiere zentrum der karte
            uv = sua+0.5*sul
            vm = sva+0.5*svl

            ky = ba.length(vm, mpv)
            if vm < mpv:
                ky = -ky

            kx = bbc.length(mpu, uv)
            if uv < mpu:
                kx = -kx

            if not obj.flipxy:
                z = App.Vector(fy*ky, fx*kx, 0)
            else:
                z = App.Vector(fx*kx, fy*ky, 0)

            circ = Part.Circle()
            circ.Radius = 10
            circ.Location = z
            if obj.displayCircles:
                comps += [circ.toShape()]

            z = App.Vector(0, 0, 0)
            circ = Part.Circle()
            circ.Radius = 20
            circ.Location = z
            if obj.displayCircles:
                comps += [circ.toShape()]

            print("Rahmen 2D", obj.uMin, obj.uMax, obj.vMin, obj.vMax)

            if obj.flipxy:
                if 1:
                    for pts in ptsa[obj.uMin:obj.uMax]:
                        try:
                            comps += [Part.makePolygon([App.Vector(fx*p[1], fy*p[0], fz*p[2])
                                                        for p in pts[obj.vMin:obj.vMax]])]
                        except:
                            pass

                    ptsa = np.array(ptsa).swapaxes(0, 1)
                    for pts in ptsa[obj.vMin:obj.vMax]:
                        try:
                            comps += [Part.makePolygon([App.Vector(fx*p[1], fy*p[0], fz*p[2])
                                                        for p in pts[obj.uMin:obj.uMax]])]
                        except:
                            pass

            else:
                if 1:
                    for pts in ptsa[obj.uMin:obj.uMax]:
                        comps += [Part.makePolygon([App.Vector(fx*p[0], fy*p[1], fz*p[2])
                                                    for p in pts[obj.vMin:obj.vMax]])]

                    ptsa = np.array(ptsa).swapaxes(0, 1)
                    for pts in ptsa[obj.vMin:obj.vMax]:
                        comps += [Part.makePolygon([App.Vector(fx*p[0], fy*p[1], fz*p[2])
                                                    for p in pts[obj.uMin:obj.uMax]])]

                else:
                    for pts in ptsa[obj.vMin:obj.vMax]:
                        comps += [Part.makePolygon([App.Vector(fx*p[0], fy*p[1], fz*p[2])
                                                    for p in pts[obj.vMin:obj.vMax]])]

                    ptsa = np.array(ptsa).swapaxes(0, 1)

                    for pts in ptsa[obj.uMin:obj.uMax]:
                        comps += [Part.makePolygon([App.Vector(fx*p[0], fy*p[1], fz*p[2])
                                                    for p in pts[obj.uMin:obj.uMax]])]
            return Part.Compound(comps)


# ------------

class Drawgrid(PartFeature):
    ''' draw the isomap grid'''

    def __init__(self, obj):
        PartFeature.__init__(self, obj)
        obj.addProperty("App::PropertyVector", "Size",
                        "Base").Size = App.Vector(300, -100, 200)
        obj.addProperty("App::PropertyLink", "faceObject", "Base")
        obj.addProperty("App::PropertyInteger", "faceNumber", "Base")

        obj.addProperty("App::PropertyLink", "wire", "Base")

        obj.addProperty("App::PropertyInteger", "uMin", "Base")
        obj.addProperty("App::PropertyInteger", "uMax", "Base")
        obj.addProperty("App::PropertyInteger", "uCenter", "Base")
        obj.addProperty("App::PropertyInteger", "uCount", "Base")

        obj.addProperty("App::PropertyInteger", "vMin", "Base")
        obj.addProperty("App::PropertyInteger", "vMax", "Base")
        obj.addProperty("App::PropertyInteger", "vCenter", "Base")
        obj.addProperty("App::PropertyInteger", "vCount", "Base")

        obj.addProperty("App::PropertyLink", "backref", "Base")
        obj.addProperty("App::PropertyBool", "flipuv", "Base")
        obj.addProperty("App::PropertyBool", "flipxy", "Base")
        obj.addProperty("App::PropertyFloat", "fx", "Base")
        obj.addProperty("App::PropertyFloat", "fy", "Base")

        obj.addProperty("App::PropertyFloat", "vMapCenter", "Map")
        obj.addProperty("App::PropertyFloat", "uMapCenter", "Map")

        obj.fx = 1.
        obj.fy = 1.
        obj.flipxy = True

        obj.uMapCenter = 50
        obj.vMapCenter = 50

        ViewProvider(obj.ViewObject)
        obj.ViewObject.LineColor = (1., 0., 1.)

        obj.uCount = 30
        obj.vCount = 30

        obj.uMax = 31
        obj.uMin = 0
        obj.vMax = 31
        obj.vMin = 0

    def onChanged(self, obj, prop):
        if obj == None:
            return
        # print ("onChanged",prop,obj)
        if prop in ["uMin", "uMax", "vMin", "vMax", "e2", "e3"]:
            obj.Shape = createGrid(obj)

    def execute(proxy, obj):
        print("exe", obj)
        if obj.faceObject != None:
            obj.Shape = createGrid(obj)
        if obj.backref != None:
            obj.backref.touch()
            obj.backref.Document.recompute()


class Draw3Dgrid(PartFeature):
    ''' draw the grid onto to 3d face obj'''

    def __init__(self, obj):
        PartFeature.__init__(self, obj)
        obj.addProperty("App::PropertyLink", "drawgrid", "Base")
        obj.addProperty("App::PropertyLink", "backref", "Base")

        ViewProvider(obj.ViewObject)
        obj.ViewObject.LineColor = (0., 1., 1.)

    def onChanged(self, obj, prop):
        print("aaaa", prop)
        if prop == "drawgrid":
            obj.Shape = createGrid(obj.drawgrid, True)

    def execute(proxy, obj):
        print("exe", obj)
        if obj.drawgrid != None:
            obj.Shape = createGrid(obj.drawgrid, True)
        if obj.backref != None:
            obj.backref.touch()
            obj.backref.Document.recompute()


class ViewProviderSL(ViewProvider):

    def onChanged(self, obj, prop):
        # print ("onChanged",prop)
        if obj.Visibility:
            ws = WorkSpace(obj.Object.workspace)
            ws.show()
        else:
            ws = WorkSpace(obj.Object.workspace)
            ws.hide()

    def onDelete(self, obj, subelements):
        print("on Delete Sahpelink")
        print("from", obj.Object.workspace, obj.Object.Label, obj.Object.Name)
        ws = WorkSpace(obj.Object.workspace)
        objs = ws.dok.findObjects()
        for jj in objs:
            print(jj.Label, jj.Name)
            s = jj.Name+"@"
            print(s, obj.Object.Name)
            if obj.Object.Label.startswith(s):
                ws.dok.removeObject(jj.Name)
                print("gguutt")
                return True
#        return False
        return(True)


class ShapeLink(PartFeature):

    def __init__(self, obj, sobj, docname):
        print("create shape link")
        PartFeature.__init__(self, obj)
        obj.addProperty("App::PropertyLink", "source", "Base")
        obj.addProperty("App::PropertyBool", "nurbs", "Base")
        obj.addProperty("App::PropertyInteger", "gridcount", "Base")
        obj.addProperty("App::PropertyString", "workspace", "Base")

        obj.source = sobj
        obj.workspace = docname
        obj.gridcount = 20
        obj.gridcount = 3

        ViewProviderSL(obj.ViewObject)

    def execute(proxy, obj):
        if not obj.ViewObject.Visibility:
            return
        objnurbs=None # don't know what this do. added by mariwan
        print("update shape", obj.source.Name, obj.workspace, obj.gridcount)

        tw = WorkSpace(obj.workspace)
        print("!!", tw)
        print(tw.dok)
        target = tw.dok.getObject(obj.source.Name)
        print(target)
        if target == None:
            tw.addObject2(obj.source, obj.gridcount)
        print(target)
        if 1 or objnurbs:
            target.Shape = obj.source.Shape.toNurbs()

            cs = []
            count = obj.gridcount
            f = obj.source.Shape.Face1.toNurbs()
            fs = f.Face1.Surface

            for ui in range(count+1):
                cs.append(fs.uIso(1.0/count*ui).toShape())
            for vi in range(count+1):
                cs.append(fs.vIso(1./count*vi).toShape())
            target.Shape = Part.Compound(cs)
            App.cs = cs
        else:
            target.Shape = obj.source.Shape
        tw.recompute()


class ViewProviderWSL(ViewProvider):

    def onChanged(self, obj, prop):
        print("onChanged", prop)
        if obj.Visibility:
            ws = WorkSpace(obj.Object.workspace)
            ws.show()
        else:
            ws = WorkSpace(obj.Object.workspace)
            ws.hide()

    def onDelete(self, obj, subelements):
        print("on Delete")
        App.closeDocument(obj.Object.workspace)
        # return False
        return(True)


class WSLink(PartFeature):

    def __init__(self, obj, docname):
        PartFeature.__init__(self, obj)
        obj.addProperty("App::PropertyString", "workspace", "Base")
        obj.workspace = docname
        ViewProviderWSL(obj.ViewObject)

    def execute(proxy, obj):
        if obj.ViewObject.Visibility:
            ws = WorkSpace(obj.workspace)
            ws.show()
        else:
            ws = WorkSpace(obj.workspace)
            ws.hide()


class WorkSpace():

    def __init__(self, name):
        try:
            lidok = App.getDocument(name)
        except:
            lidok = App.newDocument(name)
        self.dok = lidok
        self.name = name

    def delete(self):
        App.closeDocument(self.name)

    def addObject2(self, obj, count=10):
        if 0:
            res = self.dok.addObject("Part::FeaturePython", obj.Name)
            ViewProvider(res.ViewObject)
        # return
        res = self.dok.addObject("Part::Spline", obj.Name)
        res.Shape = obj.Shape.toNurbs()
        # return
        f = obj.Shape.Face1.Surface
        cs = []

        for ui in range(count+1):
            cs.append(f.uIso(1.0/count*ui).toShape())
        for vi in range(count+1):
            cs.append(f.vIso(1./count*vi).toShape())
        res.Shape = Part.Compound(cs)

    def recompute(self):
        self.dok.recompute()

    def show(self):
        self.getWidget().show()

    def hide(self):
        self.getWidget().hide()

    def getWidget(self):
        mw = Gui.getMainWindow()
        mdiarea = mw.findChild(QtGui.QMdiArea)

        sws = mdiarea.subWindowList()
        print("windows ...")
        for w2 in sws:
            print(str(w2.windowTitle()))
            s = str(w2.windowTitle())
            if s == self.name + '1 : 1[*]':
                print("gefundne")
                return w2
        print(self.name + '1:1[*]')


def createLink(obj, docname="Linkdok"):
    ad = App.ActiveDocument
    print(ad.Name)

    lidok = WorkSpace(docname)
    link = lidok.addObject2(obj)
    lidok.recompute()

    bares = obj.Document.addObject(
        "Part::FeaturePython", "Base Link "+obj.Label)
    bares.Label = obj.Label+"@"+docname

    ShapeLink(bares, obj, docname)

    return link


def createWsLink(docname = "Linkdok"):
    self.docname=docname
    ad = App.ActiveDocument
    bares = ad.addObject("Part::FeaturePython", "WS "+self.docname + "")
    WSLink(bares, self.docname)
    return bares


def testF():

    link.source = obj

    try:
        obj.backref = link
    except:
        pass

    print(lidok.Name)
    gad = Gui.getDocument(lidok.Name)
    lidok.recompute()
    Gui.SendMsgToActiveView("ViewSelection")
    Gui.SendMsgToActiveView("ViewFit")
    print(ad.Name)
    App.setActiveDocument(ad.Name)
    Gui.ActiveDocument = Gui.getDocument(ad.Name)
    return link


'''

def StrangeSoManyMain():

    for w in [App.ActiveDocument.Sketch]:
        b=App.ActiveDocument.addObject("Part::FeaturePython","MyIsodraw")
        bn=Isodraw(b)
        b.face=App.ActiveDocument.Poles
        b.wire=w
        createShape(b)
        b.ViewObject.Transparency=60
        App.ActiveDocument.recompute()
        createLink(b,"A3D")


def WhyNewMain():

        b=App.ActiveDocument.addObject("Part::FeaturePython","MyDrawGrid")

        Drawgrid(b)
        b.faceObject=App.ActiveDocument.Poles


        b.ViewObject.Transparency=60
        App.ActiveDocument.recompute()
        createLink(b,"A2D")



def OhSomanyMain():

        b=App.ActiveDocument.addObject("Part::FeaturePython","MyGrid")

        Draw3Dgrid(b)
        b.drawgrid=App.ActiveDocument.MyDrawGrid


        b.ViewObject.Transparency=60
        ss=createLink(b,"A3D")








'''


def testA():
    ad = App.ActiveDocument
    App.ActiveDocument = ad

    # bb=App.ActiveDocument.Poles
    # cc=App.ActiveDocument.orig
    cc = App.ActiveDocument.Cylinder

    # lidok= WorkSpace("A3D")
    # try: lidok.delete()
    # except: pass

    wl = createWsLink("Shoe")
    App.ActiveDocument = ad

    a = createLink(cc, "Shoe")


def testB():
    wl = createWsLink("Sole")
    App.ActiveDocument = ad
    ad.recompute()

    wl = createWsLink("Both")
    App.ActiveDocument = ad
    ad.recompute()

    a = createLink(bb, "Shoe")
    a = createLink(cc, "Sole")

    App.ActiveDocument = ad
    a = createLink(bb, "Both")
    a = createLink(cc, "Both")
    App.ActiveDocument = ad

    App.ActiveDocument = ad
    '''
    b=createLink(cc,"DD")
    b2=createLink(bb,"AA")

    a=createLink(bb,"DD")

    WorkSpace("AA").show()
    WorkSpace("DD").hide()
    '''


class map3Dto2D:
    def Activated(self):
        try:
            # 3D edge to 2D edge
            # face=App.ActiveDocument.Poles
            # wire=App.ActiveDocument.UUUU_Drawing_on_Poles__Face1002_Spline

            s0 = Gui.Selection.getSelectionEx()
            base = s0[-1]

            if hasattr(base, "faceObject"):
                face = base.faceObject
                mapobj = base
            else:
                face = base
                mapobj = None

            s = s0[:-1]
            if len(s0) == 1:
                s = s0
                mapobj = base.mapobject
                face = mapobj.faceObject
            print(face.Label)
            print("Run 3D to 2D")

            for wire in s:
                print("Wire ", wire)
                [uv2x, uv2y, xy2u, xy2v] = getmap(mapobj, face)

#                bs=face.Shape.Face1.Surface
                bs = face.Shape.Faces[mapobj.faceNumber].Surface
                pts2 = []
                firstEdge = True
                for e in wire.Shape.Edges:
                    print("Edge", e)

                    # auf 5 millimeter genau
                    if mapobj != None:
                        dd = mapobj.pointsPerEdge
                    else:
                        dd = int(round(e.Length/5))
                        dd = 30
                    ptsa = e.discretize(dd)
                    if not firstEdge:
                        pts = ptsa[1:]
                    else:
                        pts = ptsa
                    firstEdge = False

                    App.ptsaa = pts

#                    su=face.Shape.Face1.ParameterRange[1]
#                    sv=face.Shape.Face1.ParameterRange[3]
#                    print ("su sv",su,sv)
#
#
                    App.ffg = face
                    print(face)
                    print(face.Shape)
                    print(face.Shape.Faces)
                    print(face.Shape.Faces[0])
                    face1 = face.Shape.Faces[0]
                    print(face1)
                    print("!!", face1.ParameterRange)

                    sua = face1.ParameterRange[0]
                    sva = face1.ParameterRange[2]
                    sue = face1.ParameterRange[1]
                    sve = face1.ParameterRange[3]
                    sul = sue-sua
                    svl = sve-sva

                    for p in pts:
                        (u, v) = bs.parameter(p)
                        (v, u) = bs.parameter(p)
                        print(u, v)
                        # calculate back
#                        su=bs.UPeriod()
#                        sv=bs.VPeriod()

#                        print ("hack xx su sv aa bb"
                        # print base.faceobject
                        # print face
#                        su=face.Shape.Face1.ParameterRange[1]
#                        sv=face.Shape.Face1.ParameterRange[3]

#                        if su>10000: su=face.Shape.Face1.ParameterRange[1]
#                        if sv>10000: sv=face.Shape.Face1.ParameterRange[3]

#
#                        try: sweep=face.TypeId=='Part::Sweep'
#                        except: sweep=True

                        if not mapobj.flipuv23:
                            v = (v-sva)/svl
                            u = (u-sua)/sul

                        # hack yy

                        x = uv2x(u, v)
                        y = uv2y(u, v)

                        # hack zylinder schnell xx

                        if bs.__class__.__name__ == 'Cylinder':
                            print("hack for cylinder quickly line 1413 ")
                            bs.Radius
                            # x *= 0.01 *0.2
                            x /= bs.Radius
                            # x *= 100
                            # y *= bs.Radius*0.5
                            y *= 100 * bs.Radius/100
                            x, y = y, x

                        print("Umrechung u,v,x,y", u, v, x, y)
                        if mapobj != None and mapobj.flipxy:
                            p2 = App.Vector(y, x, 0)
                        else:
                            p2 = App.Vector(-y, -x, 0)
                        # hack richgtung beim Schuh
                        p2 = App.Vector(y, x, 0)
#                        p2=App.Vector(y,x,0)
                        print("p2", p2)
                        pts2.append(p2)
                App.ptsa = pts2
                a = Draft.makeWire(pts2, closed=True)
                a.Label = "map2D_for_"+wire.Label
                a.ViewObject.ShapeColor = wire.ViewObject.LineColor
        except Exception as err:
            App.Console.PrintError("'map3Dto2D' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.NURBS_ICON_PATH + 'drawing.svg',
            'MenuText': 'map 3d to 2D',
            'ToolTip':  'Map 3D drawing to 2D'
        }


Gui.addCommand('map3Dto2D', map3Dto2D())
map3Dto2D.__doc__ = """map3Dto2D: Tobe added later     """


class map2Dto3D():

    def Activated(self):
        ''' 2D Kante(Sketch) auf  3D Flaeche Poles '''

        # last selection == face
        # other sels: wires to project

        s0 = Gui.Selection.getSelectionEx()
        moa = s0[-1]
        s = s0[:-1]

        #        moa=createMap()
        #        moa.face=face
        f = None
        for w in s:
            f = createIsodrawFace()
            f.mapobject = moa
            print(moa.Label)
            f.face = moa.faceObject
            f.wire = w
            f.Label = "map3D_for_"+w.Label+"_on_"+f.face.Label + "_by_" + moa.Label
            # color=(random.random(),random.random(),random.random())
            color = w.ViewObject.ShapeColor
            print("color", color)
            print(w.Label)
            w.ViewObject.ShapeColor = color
            w.ViewObject.LineColor = color
            App.ActiveDocument.recompute()
        return f

    def GetResources(self):
        return {
            'Pixmap': Design456Init.NURBS_ICON_PATH + 'drawing.svg',
            'MenuText': 'map 3d to 2D',
            'ToolTip':  'Map 3D drawing to 2D'
        }
Gui.addCommand('map2Dto3D', map2Dto3D())
map2Dto3D.__doc__ = """map2Dto3D: Tobe added later     """


# ------------------------


class map3Dgridto2Dgrid:

    def Activated(self):
        # 3D Edges auf 2D Edges

        s0 = Gui.Selection.getSelectionEx()
        base = s0[-1]

        if hasattr(base, "faceObject"):
            face = base.faceObject
            mapobj = base
        else:
            face = base
            mapobj = None

        s = s0[:-1]
        if len(s0) == 1:
            s = s0

        print(s0)

        polcol = []
        for wire in s:
            print(wire.Label)
            [uv2x, uv2y, xy2u, xy2v] = getmap(mapobj, face)

            # bs=face.Shape.Face1.Surface
            bs = face.Shape.Faces[base.faceNumber].Surface
            pts2 = []
            firstEdge = True
            n = 0
            for e in wire.Shape.Edges:
                # print e
                n += 1
                # if n>6: break
                # auf 5 millimeter genau
                if mapobj != None:
                    dd = mapobj.pointsPerEdge
                else:
                    dd = int(round(e.Length/5))
                    dd = 30
                dd = 3
                ptsa = e.discretize(dd)
                # if not firstEdge:
                #    pts=ptsa[1:]
                # else:
                pts = ptsa
                firstEdge = False

                App.ptsaa = pts

                ptsb = []
                for p in pts:
                    #                (u,v)=bs.parameter(p)
                    (v, u) = bs.parameter(p)

#                    print ("hack A su sv aa bb"
#                    su=face.Shape.Face1.ParameterRange[1]
#                    sv=face.Shape.Face1.ParameterRange[3]
#
#                    if su>1000: su=face.ParameterRange[1]
#                    if sv>1000: sv=face.ParameterRange[3]

                    sua = face.ParameterRange[0]
                    sva = face.ParameterRange[2]
                    sue = face.ParameterRange[1]
                    sve = face.ParameterRange[3]
                    sul = sue-sua
                    svl = sve-sva

                    v = (v-sva)/svl
                    u = (u-sua)/sul

                    x = uv2x(u, v)
                    y = uv2y(u, v)
                    if mapobj != None and mapobj.flipxy:
                        p2 = App.Vector(y, x, 0)
                    else:
                        p2 = App.Vector(-y, -x, 0)
                    # hack richgtung beim Schuh
                    p2 = App.Vector(y, x, 0)

                    ptsb.append(p2)

                if len(ptsb) > 1:
                    try:
                        polcol += [Part.makePolygon(ptsb)]
                    except:
                        print("kann kein polygon bauen")
                        print(ptsb)

            # Draft.makeWire(pts2)
        Part.show(Part.Compound(polcol))

#     def GetResources(self):
#         return {
#             'Pixmap': Design456Init.NURBS_ICON_PATH + 'drawing.svg',
#             'MenuText': 'map3Dgridto2Dgrid',
#             'ToolTip':  'map3Dgridto2Dgrid'
#         }
# Gui.addCommand('map3Dgridto2Dgrid', map3Dgridto2Dgrid())
# map3Dgridto2Dgrid.__doc__ = """map3Dgridto2Dgrid: Tobe added later     """



class getmap:
    def __init__(self,mapobj, obj):
        self.mapobj=mapobj
        self.obj=obj

    def Activated(self):
        '''calculates four interpolators to convert xy (isomap) into uv (nurbs) and back
         mapobj supplies the parameters
         obj is the part with the used face
        '''

        # default values
        mpv = 0.5
        mpu = 0.5
        fx = -1
        fy = -1
        vc = 30
        uc = 30
        modeA = 'cubic'
        modeB = 'thin_plate'

        bs = obj.Shape.Face1.Surface
        face = obj.Shape.Face1

#        su=bs.UPeriod()
#        sv=bs.VPeriod()

        print("hack B-BB su sv aa bb")
        print(face)
        print(obj.Label)
        print("get map parameter Range ", face.ParameterRange)
        print("BS CLASS_______!!_______________", bs.__class__.__name__)
        print("isodraw.py zele  1705")

        if bs.__class__.__name__ == 'Cylinder':
            print("CYLINDER MODE!!")

            def m_uv2x(u, v):
                return bs.Radius*u
                return 100*u

            def m_uv2y(u, v):
                return v*1

            def m_xy2u(x, y):
                return x/bs.Radius
                return (x*1)

            def m_xy2v(x, y):
                return y

            return [m_uv2x, m_uv2y, m_xy2u, m_xy2v]

        if bs.__class__.__name__ == 'Cone':
            print("CONE MODE!!")

            alpha, beta, hmin, hmax = face.ParameterRange

            r2 = bs.Radius
            r1 = (bs.Apex-bs.Center).Length

            alpha = r2*np.pi/r1

            su = 21
            sv = 21

            def m_uv2y(u, v):
                u, v = v, u
                return (r1+hmax*v/sv/1000)*np.cos((alpha)*u/su*np.pi)
                return (r1+hmax*v/sv)*np.cos((alpha)*u/su*np.pi)/1000

            def m_uv2x(u, v):
                u, v = v, u
                return (r1+hmax*v/sv/1000)*np.sin((alpha)*u/su*np.pi)
                return (r1+hmax*v/sv)*np.sin((alpha)*u/su*np.pi)/1000

            def m_xy2u(x, y):
                return np.arctan2(x, y)/alpha*su/np.pi

            def m_xy2v(x, y):
                v = (App.Vector(x, y, 0).Length-r1) / hmax*1000*sv
                return v

            return [m_uv2x, m_uv2y, m_xy2u, m_xy2v]

    #    su=face.ParameterRange[1]
    #    sv=face.ParameterRange[3]
    #
    #    if su>1000: su=face.ParameterRange[1]
    #    if sv>1000: sv=face.ParameterRange[3]

        sua = face.ParameterRange[0]
        sva = face.ParameterRange[2]
        sue = face.ParameterRange[1]
        sve = face.ParameterRange[3]
        sul = sue-sua
        svl = sve-sva

        if mapobj != None:
            if hasattr(mapobj, 'faceObject'):

                mpv = mapobj.uMapCenter/100
                mpu = mapobj.vMapCenter/100

                fx = mapobj.fx
                fy = mapobj.fy
                vc = mapobj.vCount
                uc = mapobj.uCount

            else:

                mpv = mapobj.uMapCenter/100
                mpu = mapobj.vMapCenter/100

                vc = mapobj.vCount
                uc = mapobj.uCount

                fx = mapobj.fx
                fy = mapobj.fy
                modeA = mapobj.modeA
                modeB = mapobj.modeB

                vc = mapobj.vc
                uc = mapobj.uc

        # print ("isomap YYparameter",su,sv,uc,vc)

        refpos = bs.value(mpv, mpu)
        ptsa = []  # abbildung des uv-iso-gitter auf die xy-Ebene

        mpv = svl * mpv + sva
        mpu = sul * mpu + sua

        for v in range(vc+1):
            pts = []
            vaa = sva+1.0/vc*v*svl

            bbc = bs.vIso(vaa)

            for u in range(uc+1):
                uaa = sua+1.0/uc*u*sul
                ba = bs.uIso(uaa)

                ky = ba.length(vaa, mpv)
                if vaa < mpv:
                    ky = -ky

                kx = bbc.length(mpu, uaa)
                if uaa < mpu:
                    kx = -kx

                pts.append([kx, ky, 0])

            ptsa.append(pts)

        ptsa = np.array(ptsa).swapaxes(0, 1)

    #    vs=[1.0/vc*v for v in range(vc+1)]
    #    us=[1.0/uc*u for u in range(uc+1)]

        vs = [sva+1.0/vc*v*svl for v in range(vc+1)]
        us = [sua+1.0/uc*u*sul for u in range(uc+1)]

        uv2x = scipy.interpolate.interp2d(us, vs, ptsa[:, :, 0], kind=modeA)
        uv2y = scipy.interpolate.interp2d(us, vs, ptsa[:, :, 1], kind=modeA)

        # if only 3D to 2D is needed, exit here
        if mapobj == None:
            xy2v = None
            xy2u = None
            return [uv2x, uv2y, xy2u, xy2v]

    # ------------------------------------------------------

        # d=mapobj.border
        d = 0

        kku = []

        for ui in range(d, uc+1-d):
            for vi in range(d, vc+1-d):
                kku.append([ptsa[ui, vi, 0], ptsa[ui, vi, 1], us[ui]])
        kku = np.array(kku)

        kkv = []
        for ui in range(d, uc+1-d):
            for vi in range(d, vc+1-d):
                kkv.append([ptsa[ui, vi, 0], ptsa[ui, vi, 1], vs[vi]])
        kkv = np.array(kkv)

        try:
            dx = mapobj.ue
            dy = mapobj.ve
            sx = mapobj.ub
            sy = mapobj.vb

            # print ("Shape",uc+1,vc+1,(uc+1)*(vc+1),np.array(kku).shape)
            kku2 = np.array(kku).reshape(uc+1, vc+1, 3)
            # print(dx,dy,sx,sy)
            # print ("Shape aa",dx,dy,dx*dy,np.array(kku2[sx:sx+dx,sy:sy+dy]).shape)
            kkua = kku2[sx:sx+dx, sy:sy+dy].reshape((dx)*(dy), 3)

            kkv2 = np.array(kkv).reshape(uc+1, vc+1, 3)
            kkva = kkv2[sx:sx+dx, sy:sy+dy].reshape(dx*dy, 3)

            xy2u = scipy.interpolate.Rbf(
                kkua[:, 0], kkua[:, 1], kkua[:, 2], function=modeB)
            xy2v = scipy.interpolate.Rbf(
                kkva[:, 0], kkva[:, 1], kkva[:, 2], function=modeB)

    #        xy2v = scipy.interpolate.interp2d(kkv[:,0],kkv[:,1],kkv[:,2], kind=mode)
    # ideas for error
    # https://stackoverflow.com/questions/34820612/scipy-interp2d-warning-and-different-result-than-expected

        except Exception as err:
            sayexc()
            print('Handling  error:', err)
            xy2v = None
            xy2u = None
            print("FEHLER BERECHNUNG bUMKEHRfunktionen")

        return [uv2x, uv2y, xy2u, xy2v]

        if 0:  # testrechnung sollte auf gleiche stelle zurueck kommen
            u0 = 0.2
            v0 = 0.6

            y = uv2y(u0, v0)
            x = uv2x(u0, v0)
            u = xy2v(x, y)
            v = xy2u(x, y)

            print(u0, v0, x, y, u, v)

        return [uv2x, uv2y, xy2u, xy2v]

#     def GetResources(self):
#         return {
#             'Pixmap': Design456Init.NURBS_ICON_PATH + 'drawing.svg',
#             'MenuText': 'map 3d to 2D',
#             'ToolTip':  'Map 3D drawing to 2D'
#         }


# Gui.addCommand('getmap', getmap())
# getmap.__doc__ = """getmap: Tobe added later     """


class getmap3:
    def __ini__(self, mapobj, obj, calcZ=None):
        self.mapobj=mapobj
        self.obj=obj
        self.calcZ=calcZ
        
    def Activated(self):
        ''' berechnet einen dritten wert für z'''
        print("berechne curvature gauss")
        print(mapobj.Label)
        print(obj.Label)

    def calcZ(face, u, v):
        bs = face.Surface
        ur = 1.0*(u)/30  # mapobj.uCount
        vr = 1.0*(v)/30  # mapobj.vCount

        # umrechnung auf parametrrangen
        su = face.ParameterRange[1]
        sv = face.ParameterRange[3]

        sua = face.ParameterRange[0]
        sva = face.ParameterRange[2]
        sue = face.ParameterRange[1]
        sve = face.ParameterRange[3]
        sul = sue-sua
        svl = sve-sva

        ur = ur * sul + sua
        vr = vr * svl + sva

        tt = mapobj.modeCurvature
        App.bsa = bs

        try:
            cc = bs.curvature(ur, vr, tt)
            # kewgelhack
            cc = bs.curvature(vr, ur, tt)
        except:
            cc = 0

        if tt == "Gauss":
            z = abs(cc)**0.5 * 1000
            # if z>30: z=30
            if cc < 0:
                z = -z
        else:
            z = cc * 1000
            # beschraenken nach oben
            # if z>30: z=30
            # if z<-30: z=-30
#        if z!=0: print ("!curvature ur,vr,z", round(ur),round(vr),z)

        if tt == "Mean":
            z = 10000*cc

        # bechcraenken der kurvature
        if z > 1000:
            z = 1000
        if z < -1000:
            z = -1000

        return z

        # default values
        mpv = 0.5
        mpu = 0.5
        fx = -1
        fy = -1
        vc = 30
        uc = 30

        modeA = 'cubic'
        modeB = 'thin_plate'

        bs = obj.Shape.Face1.Surface
        face = obj.Shape.Face1

        # su=bs.UPeriod()
        # sv=bs.VPeriod()

        print("hack BB su sv aa bb XX")

        su = face.ParameterRange[1]
        sv = face.ParameterRange[3]

        if su > 1000:
            su = face.ParameterRange[1]
        if sv > 1000:
            sv = face.ParameterRange[3]

        sua = face.ParameterRange[0]
        sva = face.ParameterRange[2]
        sue = face.ParameterRange[1]
        sve = face.ParameterRange[3]
        sul = sue-sua
        svl = sve-sva

        if mapobj != None:
            if hasattr(mapobj, 'faceObject'):

                mpv = mapobj.uMapCenter/100
                mpu = mapobj.vMapCenter/100

                fx = mapobj.fx
                fy = mapobj.fy
                vc = mapobj.vCount
                uc = mapobj.uCount

            else:

                mpv = mapobj.uMapCenter/100
                mpu = mapobj.vMapCenter/100

                vc = mapobj.vCount
                uc = mapobj.uCount

                fx = mapobj.fx
                fy = mapobj.fy
                modeA = mapobj.modeA
                modeB = mapobj.modeB

        vc = mapobj.vc
        uc = mapobj.uc

        refpos = bs.value(mpv, mpu)
        ptsa = []  # abbildung des uv-iso-gitter auf die xy-Ebene

        mpv = svl*mpv + sva
        mpu = sul*mpu + sua

        for v in range(vc+1):
            pts = []
            vaa = sva+1.0/vc*v*svl

            bbc = bs.vIso(vaa)

            for u in range(uc+1):
                uaa = sua+1.0/uc*u*sul
                ba = bs.uIso(uaa)

                ky = ba.length(vaa, mpv)
                if vaa < mpv:
                    ky = -ky

                kx = bbc.length(mpu, uaa)
                if uaa < mpu:
                    kx = -kx

                kz = calcZ(face, u, v)
                pts.append([kx, ky, kz])

            ptsa.append(pts)

        ptsa = np.array(ptsa).swapaxes(0, 1)

        vs = [1.0/vc*v for v in range(vc+1)]
        us = [1.0/uc*u for u in range(uc+1)]

        vs = [sva+1.0/vc*v*svl for v in range(vc+1)]
        us = [sua+1.0/uc*u*sul for u in range(uc+1)]

        uv2x = scipy.interpolate.interp2d(us, vs, ptsa[:, :, 0], kind=modeA)
        uv2y = scipy.interpolate.interp2d(us, vs, ptsa[:, :, 1], kind=modeA)
        uv2z = scipy.interpolate.interp2d(us, vs, ptsa[:, :, 2], kind=modeA)

        # if only 3D to 2D is needed, exit here
        if mapobj == None:
            xy2v = None
            xy2u = None

            return [uv2x, uv2y, uv2z, xy2u, xy2v]

# --    ----------------------------------------------------

        # d=mapobj.border
        d = 0

        kku = []

        for ui in range(d, uc+1-d):
            for vi in range(d, vc+1-d):
                kku.append([ptsa[ui, vi, 0], ptsa[ui, vi, 1], us[ui]])
        kku = np.array(kku)

        kkv = []
        for ui in range(d, uc+1-d):
            for vi in range(d, vc+1-d):
                kkv.append([ptsa[ui, vi, 0], ptsa[ui, vi, 1], vs[vi]])
        kkv = np.array(kkv)

        try:
            dx = mapobj.ue
            dy = mapobj.ve
            sx = mapobj.ub
            sy = mapobj.vb

            # print ("Shape",uc+1,vc+1,(uc+1)*(vc+1),np.array(kku).shape)
            kku2 = np.array(kku).reshape(uc+1, vc+1, 3)
            # print(dx,dy,sx,sy)
            # print ("Shape aa",dx,dy,dx*dy,np.array(kku2[sx:sx+dx,sy:sy+dy]).shape)
            kkua = kku2[sx:sx+dx, sy:sy+dy].reshape((dx)*(dy), 3)

            kkv2 = np.array(kkv).reshape(uc+1, vc+1, 3)
            kkva = kkv2[sx:sx+dx, sy:sy+dy].reshape(dx*dy, 3)

            xy2u = scipy.interpolate.Rbf(
                kkua[:, 0], kkua[:, 1], kkua[:, 2], function=modeB)
            xy2v = scipy.interpolate.Rbf(
                kkva[:, 0], kkva[:, 1], kkva[:, 2], function=modeB)

#            xy2v = scipy.interpolate.interp2d(kkv[:,0],kkv[:,1],kkv[:,2], kind=mode)
# id    eas for error
# ht    tps://stackoverflow.com/questions/34820612/scipy-interp2d-warning-and-different-result-than-expected

        except Exception as err:
            sayexc()
            print('Handling  error:', err)
            xy2v = None
            xy2u = None
            print("FEHLER BERECHNUNG bUMKEHRfunktionen")

        return [uv2x, uv2y, uv2z, xy2u, xy2v]

        if 0:  # testrechnung sollte auf gleiche stelle zurueck kommen
            u0 = 0.2
            v0 = 0.6

            y = uv2y(u0, v0)
            x = uv2x(u0, v0)
            u = xy2v(x, y)
            v = xy2u(x, y)

            print(u0, v0, x, y, u, v)

        return [uv2x, uv2y, xy2u, xy2v]

#     def GetResources(self):
#         return {
#             'Pixmap': Design456Init.NURBS_ICON_PATH + 'drawing.svg',
#             'MenuText': 'map 3d to 2D',
#             'ToolTip':  'Map 3D drawing to 2D'
#         }


# Gui.addCommand('getmap3', getmap3())
# getmap3.__doc__ = """getmap3: Tobe added later     """


# pruefe qualitaet der umrechnung
class testC():
    def Activated(self):
        face = App.ActiveDocument.Poles
        # face=App.ActiveDocument.MySegment
        bs = face.Shape.Face1.Surface
        # wire=App.ActiveDocument.UUUU_Drawing_on_Poles__Face1002_Spline
        wire = App.ActiveDocument.UUUU_Drawing_on_Poles__Face1001_Spline
        # wire=App.ActiveDocument.Shape001
        p = wire.Shape.Vertex1.Point
        p
        print("huu")
        [uv2x, uv2y, xy2u, xy2v] = getmap(face)

        (u, v) = bs.parameter(p)
        (u, v) = bs.parameter(p)
        pt0 = bs.value(u, v)
        print(u, v)
        x = uv2x(u, v)
        y = uv2y(u, v)
        print(x, y)
        u = xy2v(x, y)
        v = xy2u(x, y)
        print(u, v)
        pt = bs.value(u, v)
#        print pt
#        print p
        print(p-pt)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.NURBS_ICON_PATH + 'drawing.svg',
            'MenuText': 'testC',
            'ToolTip':  'testC'
        }
Gui.addCommand('testC', testC())
testC.__doc__ = """testC: Tobe added later     """


class testD():
    def Activated(self):
        #    kku2=np.array(App.kku).reshape(31,31,3)
        #    kku=kku2[10:25,10:20].reshape(150,3)

        ptsu = [App.Vector(tuple(i)) for i in kku]
        Draft.makeWire(ptsu)
        Points.show(Points.Points(ptsu))

        mode = 'thin_plate'
        xy2u = scipy.interpolate.Rbf(
            kku[:, 0], kku[:, 1], kku[:, 2], function=mode)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.NURBS_ICON_PATH + 'drawing.svg',
            'MenuText': 'testD',
            'ToolTip':  'testD'
        }
Gui.addCommand('testD', testD())
testD.__doc__ = """testD: Tobe added later     """


class testE():
    def Activated(Self):
        [uv2x, uv2y, xy2u, xy2v] = getmap(face)
        ptbb = []
        for p in App.ptsaa:
            (u, v) = bs.parameter(p)
            (u, v) = bs.parameter(p)
            pt0 = bs.value(u, v)
#            print (u,v)
            x = uv2x(u, v)
            y = uv2y(u, v)
#            print (x,y)
            u = xy2v(x, y)
            v = xy2u(x, y)
#            print(u,v)
            pt = bs.value(u, v)
        #    print pt
        #    print p
            print(p-pt)
            ptbb.append(pt)

        Draft.makeWire(ptbb)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.NURBS_ICON_PATH + 'drawing.svg',
            'MenuText': 'testE',
            'ToolTip':  'testE'
        }


Gui.addCommand('testE', testE())
testE.__doc__ = """testE: Tobe added later     """
