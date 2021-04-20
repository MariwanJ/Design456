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
# -------------------------------------------------
# -- nurbs editor -
# --
# -- microelly 2016
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------
from pivy import coin
from say import *
import os

import NURBSinit
try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
__version__ = '0.3'

# idea from  FreeCAD TemplatePyMod module by (c) 2013 Werner Mayer LGPL

# http://de.wikipedia.org/wiki/Non-Uniform_Rational_B-Spline
# http://www.opencascade.com/doc/occt-6.9.0/refman/html/class_geom___b_spline_surface.html


if 0:  # change render to show triangulations

    view = Gui.ActiveDocument.ActiveView
    viewer = view.getViewer()
    render = viewer.getSoRenderManager()

    glAction = coin.SoGLRenderAction(render.getViewportRegion())
    render.setGLRenderAction(glAction)
    render.setRenderMode(render.WIREFRAME_OVERLAY)


def setNice(flag=True):
    ''' make smooth skins '''
    p = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Part")
    w = p.GetFloat("MeshDeviation")
    if flag:
        p.SetFloat("MeshDeviation", 0.05)
    else:
        p.SetFloat("MeshDeviation", 0.5)


setNice()


class PartFeature:
    def __init__(self, obj):
        obj.Proxy = self
        self.obj2 = obj

# grundmethoden zum sichern

    def attach(self, vobj):
        self.Object = vobj.Object

    def claimChildren(self):
        return self.Object.Group

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


class Nurbs(PartFeature):
    def __init__(self, obj, uc=5, vc=5):
        PartFeature.__init__(self, obj)

        self.TypeId = "Nurbs"
        obj.addProperty("App::PropertyInteger", "polnumber",
                        "XYZ", "Length of the Nurbs").polnumber = 0

        obj.addProperty("App::PropertyInteger", "degree_u",
                        "Nurbs", "").degree_u = 2
        obj.addProperty("App::PropertyInteger", "degree_v",
                        "Nurbs", "").degree_v = 2
        obj.addProperty("App::PropertyInteger", "nNodes_u",
                        "Generator", "").nNodes_u = uc
        obj.addProperty("App::PropertyInteger", "nNodes_v",
                        "Generator", "").nNodes_v = vc
        obj.addProperty("App::PropertyFloatList", "knot_u", "Nurbs", "").knot_u = [
            0, 0, 0, 0.33, 0.67, 1, 1, 1]
        obj.addProperty("App::PropertyFloatList", "knot_v", "Nurbs", "").knot_v = [
            0, 0, 0, 0.33, 0.67, 1, 1, 1]
        obj.addProperty("App::PropertyFloatList", "weights",
                        "Nurbs", "").weights = [1]*(uc*vc)

        obj.addProperty("App::PropertyEnumeration", "model", "Base", "").model = [
            "NurbsSuface", "NurbsCylinder", "NurbsSphere", "NurbsTorus"]

        obj.addProperty("App::PropertyFloat", "Height", "XYZ",
                        "Height of the Nurbs").Height = 1.0
        obj.addProperty("App::PropertyStringList", "poles", "Nurbs", "")

        # the poles and surface helper object link
        obj.addProperty("App::PropertyLink", "polobj", "XYZ", "")
        obj.addProperty("App::PropertyLink", "gridobj", "XYZ", "")
        obj.addProperty("App::PropertyLink", "polselection", "XYZ", "")
        obj.addProperty("App::PropertyLink", "polgrid", "XYZ", "")
        obj.addProperty("App::PropertyBool", "grid", "Helper",
                        "create a grid object in 3D").grid = True
        obj.addProperty("App::PropertyInteger", "gridCount",
                        "Helper", "").gridCount = 6
        obj.addProperty("App::PropertyBool", "solid", "Shape",
                        "close the surface by a bottom plane").solid = True
        obj.addProperty("App::PropertyBool", "base", "Shape",
                        "create a base cuboid under the surface").base = True
        obj.addProperty("App::PropertyBool", "polpoints", "Helper",
                        "display Poles as separate Points").polpoints = False
        obj.addProperty("App::PropertyFloat", "baseHeight",
                        "Shape", "height of the base cuboid").baseHeight = 100
        obj.addProperty("App::PropertyFloat", "stepU", "Generator",
                        "size of cell in u direction").stepU = 100
        obj.addProperty("App::PropertyFloat", "stepV", "Generator",
                        "size of cell in u direction").stepV = 100
        obj.addProperty("App::PropertyBool", "generatePoles", "Generator",
                        "generate Poles from model").generatePoles = True
        obj.addProperty("App::PropertyBool", "expertMode", "XYZ",
                        "generate Poles from model").expertMode = False

        obj.degree_u = 3
        obj.degree_v = 3

        if not obj.expertMode:
            # not gui editable
            for a in ['degree_u', 'degree_v', 'poles', 'knot_u', 'knot_v', 'nNodes_u', 'nNodes_v', 'weights', 'solid']:
                obj.setEditorMode(a, 2)

        for a in ['polnumber', 'Height', 'polselection', 'gridobj', 'polgrid', 'polobj']:
            obj.setEditorMode(a, 2)

        if obj.generatePoles:
            for a in ['nNodes_u', 'nNodes_v']:
                obj.setEditorMode(a, 0)

    def attach(self, vobj):
        print("attach -------------------------------------")
        self.Object = vobj.Object
        self.obj2 = vobj.Object

    def onChanged(self, fp, prop):
        # print ("changed ",prop

        if prop == 'nNodes_u' and fp.nNodes_u <= fp.degree_u:
            fp.nNodes_u = fp.degree_u + 1
        if prop == 'nNodes_v' and fp.nNodes_v <= fp.degree_v:
            fp.nNodes_v = fp.degree_v + 1

        if prop == "expertMode":
            if not fp.expertMode:
                v = 2
            else:
                v = 0
            for a in ['degree_u', 'degree_v', 'poles', 'knot_u', 'knot_v', 'nNodes_u', 'nNodes_v', 'weights']:
                try:
                    fp.setEditorMode(a, v)
                except:
                    pass

        if prop == "generatePoles":
            if fp.generatePoles:
                v = 0
            else:
                v = 2
            for a in ['nNodes_u', 'nNodes_v', 'stepU', 'stepV']:
                try:
                    fp.setEditorMode(a, v)
                except:
                    pass

        if prop == 'stepU' or prop == 'stepV' or prop == 'nNodes_u' or prop == 'nNodes_v':

            a = App.ActiveDocument.Nurbs
            a.Proxy.obj2 = a
            try:
                ps = a.Proxy.getPoints()
                a.Proxy.togrid(ps)
    #            a.Proxy.elevateVline(2,100)

                a.Proxy.updatePoles()
                a.Proxy.showGriduv()
                a.Proxy.update(fp)
            except:
                pass

        return

    def update(self, fp):
        if hasattr(fp, "polobj"):
            if fp.polobj != None:
                App.ActiveDocument.removeObject(
                    fp.polobj.Name)
            fp.polobj = self.createSurface(fp, fp.poles)
            if fp.polobj != None:
                fp.polobj.ViewObject.PointSize = 4
                fp.polobj.ViewObject.PointColor = (1.0, 0.0, 0.0)

    def execute(self, fp):
        pass

    def onDocumentRestored(self, fp):
        say(["onDocumentRestored", str(fp.Label) +
             ": "+str(fp.Proxy.__class__.__name__)])
        a = App.ActiveDocument.Nurbs
        a.Proxy.obj2 = a

        ps = a.Proxy.getPoints()
        a.Proxy.togrid(ps)
        a.Proxy.updatePoles()
        a.Proxy.showGriduv()
        a.Proxy.update(fp)

        if not fp.expertMode:
            v = 2
        else:
            v = 0

        for a in ['degree_u', 'degree_v', 'poles', 'knot_u', 'knot_v', 'nNodes_u', 'nNodes_v', 'weights']:
            fp.setEditorMode(a, v)

        if fp.generatePoles:
            v = 0
        else:
            v = 2

        for a in ['nNodes_u', 'nNodes_v', 'stepU', 'stepV']:
            fp.setEditorMode(a, v)

        for a in ['polnumber', 'Height', 'polselection', 'gridobj', 'polgrid', 'polobj']:
            fp.setEditorMode(a, 2)

    def create_grid_shape(self, ct=20):
        ''' create a grid of BSplineSurface bs with ct lines and rows '''

        ct = ct
        bs = self.bs
        sss = []

        st = 1.0/ct
        for iu in range(ct+1):
            pps = []
            for iv in range(ct+1):
                p = bs.value(st*iu, st*iv)
                pps.append(p)
            tt = Part.BSplineCurve()
            tt.interpolate(pps)
            ss = tt.toShape()
            sss.append(ss)

        for iv in range(1, ct+1):
            pps = []
            for iu in range(0, ct+1):

                p = bs.value(st*iu, st*iv)
                # print (iv,iu,st*iu,st*iv)
                pps.append(p)
            tt = Part.BSplineCurve()
            tt.interpolate(pps)
            ss = tt.toShape()

            # Hack
            ss = Part.makePolygon(pps)
            sss.append(ss)

        comp = Part.Compound(sss)
        return comp

    def create_grid(self, bs, ct=20):

        comp = self.create_grid_shape(ct)
        Part.show(comp)
        return App.ActiveDocument.ActiveObject

    def create_uv_grid_shape(self):
        ''' create a grid of the poles '''

        bs = self.bs
        sss = []

        nNodes_u = self.obj2.nNodes_u
        nNodes_v = self.obj2.nNodes_v

        print("poles and knots")
        print(nNodes_u, nNodes_v)
        print(bs.NbUPoles, bs.NbVPoles)
        nNodes_u = bs.NbUPoles
        nNodes_v = bs.NbVPoles

        for iu in range(nNodes_u):
            # meridiane
            pps = []
            p = bs.getPole(1+iu, 1)
            pps = [p.add(App.Vector(0, -20, 0))]

            for iv in range(nNodes_v):
                p = bs.getPole(1+iu, 1+iv)
                pps.append(p)

            p = bs.getPole(1+iu, nNodes_v)
            pps.append(p.add(App.Vector(0, 20, 0)))

            ss = Part.makePolygon(pps)

            # fuer geschlossenes
            ss = Part.makePolygon(pps[1:-1])
            # if iu==nNodes_u-1:
            sss.append(ss)

        for iv in range(nNodes_v):
            # breitengrade
            p = bs.getPole(1, 1+iv)
            pps = [p.add(App.Vector(-20, 0, 0))]
            for iu in range(nNodes_u):
                p = bs.getPole(1+iu, 1+iv)
                pps.append(p)

            p = bs.getPole(nNodes_u, 1+iv)
            pps.append(p.add(App.Vector(20, 0, 0)))

            ss = Part.makePolygon(pps)

            # fuer geschlossenes
            pps2 = pps[1:-1]
            pps2.append(pps[1])
            try:
                ss = Part.makePolygon(pps2)
                # horizontale
                # if iv!=1:
                sss.append(ss)
            except:
                print("kein polygon fuer", pps2)

        comp = Part.Compound(sss)
        return comp

    def create_uv_grid(self):

        comp = self.create_uv_grid_shape()
        Part.show(comp)
        App.ActiveDocument.ActiveObject.ViewObject.LineColor = (1.0, 0.0, 1.0)
        App.ActiveDocument.ActiveObject.ViewObject.LineWidth = 1
        return App.ActiveDocument.ActiveObject

    def create_solid(self, bs):
        ''' create a solid part with the surface as top'''

        poles = np.array(bs.getPoles())
        ka, kb, tt = poles.shape

        weights = np.array(bs.getWeights())
        multies = bs.getVMultiplicities()

        cs = []

        for n in 0, ka-1:
            pts = [App.Vector(tuple(p)) for p in poles[n]]
            bc = Part.BSplineCurve()
            bc.buildFromPolesMultsKnots(
                pts, multies, bs.getVKnots(), False, 2, weights[n])
            cs.append(bc.toShape())

        poles = poles.swapaxes(0, 1)
        weights = weights.swapaxes(0, 1)
        multies = bs.getUMultiplicities()

        for n in 0, kb-1:
            pts = [App.Vector(tuple(p)) for p in poles[n]]
            bc = Part.BSplineCurve()
            bc.buildFromPolesMultsKnots(
                pts, multies, bs.getUKnots(), False, 2, weights[n])
            cs.append(bc.toShape())

        comp = Part.Compound(cs)
        Part.show(comp)

        # create wire and face
        Draft.upgrade(App.ActiveDocument.ActiveObject, delete=True)
        App.ActiveDocument.recompute()

        Draft.upgrade(App.ActiveDocument.ActiveObject, delete=True)
        App.ActiveDocument.recompute()

        # bottom face ...
        cur = App.ActiveDocument.ActiveObject
        s1 = cur.Shape
        App.ActiveDocument.removeObject(cur.Name)

        # solid ...
        sh = Part.makeShell([s1, bs.toShape()])
        return Part.makeSolid(sh)

    def CylinderCoords(self, obj, coor):
        ''' calculate coord for cylinder '''

        coor = np.array(coor)
        print(coor)
        l, d = coor.shape
        xs = coor[:, 0]
        ys = coor[:, 1]
        zs = coor[:, 2]

        xs -= xs.min()
        xs /= xs.max()
        xs *= (2*3.14)
        print(xs)

        ys -= ys.min()
        ys /= ys.max()

        zs -= zs.min()
        zs /= zs.max()

        print(ys)
        coor = []
        h = 2000
        for i in range(l):
            r = 400+200*zs[i]
            coor.append([r*np.cos(xs[i]), r*np.sin(xs[i]), h*ys[i]])

        return (coor)

    def SphereCoords(self, obj, coor):
        ''' calculate coord for cylinder '''

        coor = np.array(coor)
#        print coor
        l, d = coor.shape
        xs = coor[:, 0]
        ys = coor[:, 1]
        zs = coor[:, 2]

        xs -= xs.min()
        xs /= xs.max()
        xs *= (2*3.1)
#        print xs

        ys -= ys.min()
        ys /= ys.max()
        ys -= 0.5
        ys *= 3.14

        zs -= zs.min()
        zs /= zs.max()

#        print ys
        coor = []
        r = 400
        h = 4000
        for i in range(l):
            r = 400+400*zs[i]
            r = 400-60*zs[i]
            coor.append([r*np.cos(xs[i])*np.cos(ys[i]),
                         r*np.sin(xs[i])*np.cos(ys[i]),
                         r*np.sin(ys[i])])

        return coor

    def createSurface(self, obj, poles=None):
        ''' create the nurbs surface and aux parts '''

        starttime = time.time()
        degree_u = obj.degree_u
        degree_v = obj.degree_v
        nNodes_u = obj.nNodes_u
        nNodes_v = obj.nNodes_v

        uc = nNodes_u
        vc = nNodes_v

        l = [1.0/(uc-2)*i for i in range(uc-1)]
        obj.knot_u = [0, 0] + l + [1, 1]

        l = [1.0/(vc-2)*i for i in range(vc-1)]
        obj.knot_v = [0, 0] + l + [1, 1]

        if obj.degree_u == 3:
            l = [1.0/(uc-3)*i for i in range(uc-2)]
            obj.knot_u = [0, 0, 0] + l + [1, 1, 1]

        if obj.degree_v == 3:
            l = [1.0/(vc-3)*i for i in range(vc-2)]
            obj.knot_v = [0, 0, 0] + l + [1, 1, 1]

        if obj.degree_u == 1:
            l = [1.0/(uc-1)*i for i in range(uc)]
            obj.knot_u = [0] + l + [1]

        if obj.degree_v == 1:
            l = [1.0/(vc-1)*i for i in range(vc)]
            obj.knot_v = [0] + l + [1]

        try:
            weights = np.array(obj.weights)
            weights = weights.reshape(vc, uc)
        except:
            weights = np.ones(vc*uc)
            weights = weights.reshape(vc, uc)

        obj.weights = list(np.ravel(weights))

        knot_u = obj.knot_u
        knot_v = obj.knot_v

        coor = [[0, 0, 1], [1, 0, 1], [2, 0, 1], [3, 0, 1], [4, 0, 1],
                [0, 1, 1], [1, 1, 0], [2, 1, 0], [3, 1, 0], [4, 1, 1],
                [0, 2, 1], [1, 2, 0], [2, 2, 3], [3, 2, 0], [4, 2, 1],
                [0, 3, 1], [1, 3, 0], [2, 3, 1], [3, 3, -3], [4, 3, 1],
                [0, 4, 1], [1, 4, 1], [2, 4, 1], [3, 4, 1], [4, 4, 1]]

        if poles != None:
            cc = ""
            for l in poles:
                cc += str(l)
            coor = eval(cc)

        if obj.model == "NurbsCylinder":

            coor = self.CylinderCoords(obj, coor)

        if obj.model == "NurbsSphere":

            coor = self.SphereCoords(obj, coor)

            if obj.degree_u == 399999:
                l = [1.0/(uc-3)*i for i in range(uc-2)]
                obj.knot_u = [0, 0, 0, 0] + l + [1, 1, 1, 1]

            if obj.degree_v == 3:
                l = [1.0/(vc-3)*i for i in range(vc-2)]
                obj.knot_v = [0, 0, 0, 0] + l + [1, 1, 1, 1]


# ----------------------------------------------------------------------------------
        print("len A coor ", len(coor))

#        knot_u=[0,0,0.2,0.4,0.6,0.8,1,1]
#        knot_u=[0,0,0.2, 0.4,0.4, 0.6,0.8,1,1]

#        knot_v=[0,0.5,1]
#        knot_v=[0,0,0.5,1,1]

        obj.poles = str(coor)

        bs = Part.BSplineSurface()

        # bs.setUPeriodic()
        self.bs = bs

        bs.increaseDegree(degree_u, degree_v)

        if obj.model == "NurbsCylinder":
            # cylinder - experimental  play with periodic nurbs
            pass
            bs.setUPeriodic()

        if obj.model == "NurbsSphere":
            pass
            bs.setUPeriodic()


#        bs.setVPeriodic()
#        bs.setUPeriodic()

        print("poles u count", bs.NbUKnots)
        print("poles v count", bs.NbVKnots)

        # +#+ todo split knot vectors in single values vector and multiplicity vector
        for i in range(0, len(knot_u)):
            # if knot_u[i+1] > knot_u[i]:
            bs.insertUKnot(knot_u[i], 1, 0.0000001)

        for i in range(0, len(knot_v)):
            # if knot_v[i+1] > knot_v[i]:
            bs.insertVKnot(knot_v[i], 1, 0.0000001)

        print("dim nodes", nNodes_v, nNodes_u)
        print("len coor ", len(coor))
#        print ("knot_u",knot_u)
#        print ("knot_v",knot_v)
        print("poles u count", bs.NbUPoles)
        print("poles v count", bs.NbVPoles)
#        print bs.getUKnots()
#        print bs.getVKnots()
#        print bs.getUMultiplicities()
#        print bs.getVMultiplicities()

        t = bs.getPoles()
        print("shape poles", len(t), len(t[0]))
        # return

        # nNodes_v,nNodes_u=nNodes_u,nNodes_v

        if obj.model == "NurbsSuface":
            print("Nurbs surface !!!")
            poles2 = np.array(coor).reshape(nNodes_v, nNodes_u, 3)
            print(poles2.shape)

            vc = nNodes_v
            kv = [1.0/(nNodes_v-1)*i for i in range(nNodes_v)]
            ku = [1.0/(nNodes_u-1)*i for i in range(nNodes_u)]

            print(ku)
            print(kv)
            print((len(ku)))
            print((len(kv)))
            print(nNodes_u)
            print(nNodes_v)

            bs.buildFromPolesMultsKnots(poles2, [3] + [1]*(nNodes_v-2) + [3], [3]+[1]*(nNodes_u-2)+[3],
                                        kv,
                                        ku,
                                        False, False, 3, 3, 10.0*np.ones(nNodes_v*(nNodes_u-1)))

        if obj.model == "NurbsSphere" or obj.model == "NurbsCylinder":
            poles2 = np.array(coor).reshape(nNodes_v, nNodes_u, 3)
            print(poles2.shape)

            vc = nNodes_v
            kv = [1.0/(nNodes_v-1)*i for i in range(nNodes_v)]
            ku = [1.0/(nNodes_u-1)*i for i in range(nNodes_u)]

            bs.buildFromPolesMultsKnots(poles2, [3] + [1]*(nNodes_v-2) + [3], [2]+[1]*(nNodes_u-2)+[2],
                                        kv,
                                        ku,
                                        False, True, 3, 3, 1.0*np.ones(nNodes_v*(nNodes_u-1)))

        # irgendwas vertauscht beim torus
        if obj.model == "NurbsTorus":

            coor = [
                [20.0, 0, -40], [60, 0, -40], [30, 0, 50], [0, 0, -40],
                [20, 10, -40], [40, 10, -40], [40, 10, 55], [0, 10, -40],
                [20, 15, -40], [65, 15, -40], [60, 15, 75], [35, 15, -40],
                [0, 20, 10], [0, 40, 20], [0, 45, 65], [0, 20, 20],
                [-20, 0, 0], [-40, 0, 20], [-70, 0, 75], [-20, 0, 40],
                [-30, -10, 5], [-40, -10, 20], [-40, -10, 55], [-20, -20, 40],
                [5, -20, 5], [0, -40, 30], [0, -45, 65], [5, -20, 10],
            ]
            tt = 10*np.array(coor)
            poles2 = tt.reshape(7, 4, 3)
            bs.buildFromPolesMultsKnots(poles2, [2, 1, 1, 1, 1, 1, 2], [2, 1, 1, 2], [
                                        0, 0.2, 0.4, 0.5, 0.7, 0.8, 1], [0, 0.4, 0.6, 1], True, True, 3, 3, 1.0*np.ones(28))

        '''
        else:
            i=0
            for jj in range(0,nNodes_v):
                for ii in range(0,nNodes_u):

                    try:
                        # print("getpole",bs.getPole(jj+1,ii+1))
                        bs.setPole(jj+1,ii+1,App.Vector((coor[i][0],coor[i][1],coor[i][2])),weights[jj,ii])
                        bs.setWeight(jj+1,ii+1,4)
                        # print i,App.Vector((coor[i][0],coor[i][1],coor[i][2]))
                        print([ii+1,jj+1,App.Vector((coor[i][0],coor[i][1],coor[i][2])),weights[jj,ii]])
                    except:
                            print([ii+1,jj+1,App.Vector((coor[i][0],coor[i][1],coor[i][2])),weights[jj,ii]])

                            sayexc("error setPols ii,jj:"+str([ii+1,jj+1]))
                            print("getpole exc reverse --",
                                  bs.getPole(jj+1,ii+1))
                            print("getpole exc --",bs.getPole(ii+1,jj+1))
                    i=i+1;
        '''

        # create aux parts
        if obj.solid:
            obj.Shape = self.create_solid(bs)
        else:
            if App.ParamGet('User parameter:Plugins/nurbs').GetBool("createNurbsShape", True):
                obj.Shape = bs.toShape()

        vis = False
        vis = True
        if obj.grid:
            if obj.gridobj != None:
                vis = obj.gridobj.ViewObject.Visibility
                App.ActiveDocument.removeObject(obj.gridobj.Name)
            obj.gridobj = self.create_grid(bs, obj.gridCount)
            obj.gridobj.Label = "Nurbs Grid"
            obj.gridobj.ViewObject.Visibility = vis

        if 0 and obj.base:
            # create the socket box
            mx = np.array(coor).reshape(nNodes_v, nNodes_u, 3)
            print("create box")

            print(mx.shape)
            a0 = tuple(mx[0, 0])
            b0 = tuple(mx[0, -1])
            c0 = tuple(mx[-1, -1])
            d0 = tuple(mx[-1, 0])
            bh = obj.baseHeight

            a = tuple(mx[0, 0]+[0, 0, -bh])
            b = tuple(mx[0, -1]+[0, 0, -bh])
            c = tuple(mx[-1, -1]+[0, 0, -bh])
            d = tuple(mx[-1, 0]+[0, 0, -bh])
            print(a, b, c, d)

            lls = [Part.makeLine(a0, b0), Part.makeLine(
                b0, b), Part.makeLine(b, a), Part.makeLine(a, a0)]
            fab = Part.makeFilledFace(lls)
            lls = [Part.makeLine(b0, c0), Part.makeLine(
                c0, c), Part.makeLine(c, b), Part.makeLine(b, b0)]
            fbc = Part.makeFilledFace(lls)
            lls = [Part.makeLine(c0, d0), Part.makeLine(
                d0, d), Part.makeLine(d, c), Part.makeLine(c, c0)]
            fcd = Part.makeFilledFace(lls)
            lls = [Part.makeLine(d0, a0), Part.makeLine(
                a0, a), Part.makeLine(a, d), Part.makeLine(d, d0)]
            fda = Part.makeFilledFace(lls)
            lls = [Part.makeLine(a, b), Part.makeLine(
                b, c), Part.makeLine(c, d), Part.makeLine(d, a)]
            ff = Part.makeFilledFace(lls)

            surf = bs.toShape()
            fs = [fab, fbc, fcd, fda, ff, surf]
            comp = Part.makeCompound(fs)
            Part.show(comp)
            App.ActiveDocument.ActiveObject.Label = "Nurbs with Base"

            App.ActiveDocument.recompute()
            App.ActiveDocument.recompute()

            # bottom face ...
            cur = App.ActiveDocument.ActiveObject
            s1 = cur.Shape
            App.ActiveDocument.removeObject(cur.Name)

            # solid ...
            s = Part.makeShell([s1, bs.toShape()])

            s = Part.makeShell(fs)

            sol = Part.makeSolid(s)
#            Part.show(sol)
            obj.Shape = sol

        # create a pole grid with spines

        # --- hack
        # print ("cancellation Zeile 661"
        # return None
        # ---

        vis = True
        vis = False
        try:
            vis = obj.polgrid.ViewObject.Visibility
            App.ActiveDocument.removeObject(obj.polgrid.Name)
        except:
            pass
        obj.polgrid = self.create_uv_grid()
        obj.polgrid.Label = "Pole Grid"
        obj.polgrid.ViewObject.Visibility = vis

        nurbstime = time.time()

        print("XB")

        polesobj = None
        comptime = time.time()

        if obj.polpoints:
            # create the poles for visualization
            # the pole point cloud
            pts = [App.Vector(tuple(c)) for c in coor]
            vts = [Part.Vertex(pp) for pp in pts]

            # and the surface

            # vts.append(obj.Shape)
            comp = Part.makeCompound(vts)
            comptime = time.time()
            try:
                yy = App.ActiveDocument.Poles
            except:
                yy = App.ActiveDocument.addObject("Part::Feature", "Poles")

            yy.Shape = comp
            polesobj = App.ActiveDocument.ActiveObject

        endtime = time.time()

        print("create nurbs components, surface time ",
              round(nurbstime-starttime, 2),
              round(comptime-nurbstime, 2),
              round(endtime-comptime, 2))

        return polesobj

    def getBS(self):
        try:
            rc = self.bs
        except:
            sayexc("BSpline nicht mehr vorhanden, muss neu berechnet werden ....")
            uc = self.obj2.nNodes_v
            vc = self.obj2.nNodes_u
            self.createSurface(self.obj2, self.obj2.poles)
            rc = self.bs
        return rc

    def getPoints(self):
        ''' generic point set for grid'''
        if self.obj2.generatePoles:
            ps = []
            vc = self.obj2.nNodes_v
            uc = self.obj2.nNodes_u
            for v in range(vc):
                for u in range(uc):
                    ps.append(App.Vector(
                        u*self.obj2.stepU, v*self.obj2.stepV, 0))
            return ps
        else:
            t = eval(str(self.obj2.poles))
            return eval(t[0])

    def togrid(self, ps):
        ''' points to 2D grid'''
        self.grid = None
        self.g = np.array(ps).reshape(
            self.obj2.nNodes_v, self.obj2.nNodes_u, 3)
        return self.g

    def showGriduv(self):
        '''recompute and show the Pole grid '''

        starttime = time.time()
        gg = self.g

        try:
            if not self.calculatePoleGrid:
                return
        except:
            return

        ls = []
        uc = self.obj2.nNodes_v
        vc = self.obj2.nNodes_u

        # straight line grid
        for u in range(uc):
            for v in range(vc):
                if u < uc-1:
                    ls.append(Part.makeLine(
                        tuple(gg[u][v]), tuple(gg[u+1][v])))
                if v < vc-1:
                    ls.append(Part.makeLine(
                        tuple(gg[u][v]), tuple(gg[u][v+1])))

        comp = Part.makeCompound(ls)
        if self.grid != None:
            self.grid.Shape = comp
        else:
            Part.show(comp)
            App.ActiveDocument.ActiveObject.ViewObject.hide()
            self.grid = App.ActiveDocument.ActiveObject
            self.grid.Label = "Pole Grid"

        App.ActiveDocument.recompute()
        Gui.updateGui()
        endtime = time.time()
        print("create PoleGrid time", endtime-starttime)

    def setpointZ(self, u, v, h=0, w=20):
        ''' set height and weight of a pole point '''

        u, v = v, u
        # self.g[v][u][2]=h
        self.g[v][u][2] = 100*np.tan(0.5*np.pi*h/101)
        try:
            wl = self.obj2.weights
            wl[v*self.obj2.nNodes_u+u] = w
            self.obj2.weights = wl
        except:
            sayexc()

    def setpointRelativeZ(self, u, v, h=0, w=0, update=False):
        ''' set relative height and weight of a pole point '''

        u, v = v, u
        # self.g[v][u][2] = self.gBase[v][u][2] + h
        # unrestricted
        self.g[v][u][2] = self.gBase[v][u][2] + 100 * np.tan(0.5*np.pi*h/101)
        sayW(("set  rel h, height", h, self.g[v][u][2]))

        if update:
            self.gBase = self.g.copy()

        try:
            wl = self.obj2.weights
            wl[v*self.obj2.nNodes_u+u] = w
            self.obj2.weights = wl
        except:
            sayexc()

    def movePoint(self, u, v, dx, dy, dz):
        ''' relative move ofa pole point '''

        App.ActiveDocument.openTransaction(
            "move Point " + str((u, v, dx, dy, dz)))

        self.g[v][u][0] += dx
        self.g[v][u][1] += dy
        self.g[v][u][2] += dz

        self.updatePoles()
        self.showGriduv()
        App.ActiveDocument.commitTransaction()

    def elevateUline(self, vp, height=40):
        ''' change the height of all poles with the same u value'''

        App.ActiveDocument.openTransaction("elevate ULine" + str([vp, height]))

        uc = self.obj2.nNodes_u
        vc = self.obj2.nNodes_v

        for i in range(1, uc-1):
            self.g[vp][i][2] = height

        self.updatePoles()
        self.showGriduv()
        App.ActiveDocument.commitTransaction()

    def elevateVline(self, vp, height=40):

        # App.ActiveDocument.openTransaction("elevate VLine" + str([vp,height]))

        uc = self.obj2.nNodes_u
        vc = self.obj2.nNodes_v

        for i in range(1, vc-1):
            self.g[i][vp][2] = height

        # self.updatePoles()
        # self.showGriduv()
        # App.ActiveDocument.commitTransaction()

    def elevateRectangle(self, v, u, dv, du, height=50):
        ''' change the height of all poles inside a rectangle of the pole grid'''

        App.ActiveDocument.openTransaction(
            "elevate rectangle " + str((u, v, dv, du, height)))

        uc = self.obj2.nNodes_u
        vc = self.obj2.nNodes_v

        for iv in range(v, v+dv+1):
            for iu in range(u, u+du+1):
                try:
                    self.g[iu][iv][2] = height
                except:
                    pass

        self.updatePoles()
        self.showGriduv()
        App.ActiveDocument.commitTransaction()

    def elevateCircle(self, u=20, v=30, radius=10, height=60):
        ''' change the height for poles around a cenral pole '''

        App.ActiveDocument.openTransaction(
            "elevate Circle " + str((u, v, radius, height)))

        uc = self.obj2.nNodes_u
        vc = self.obj2.nNodes_v

        g = self.g
        for iv in range(vc):
            for iu in range(uc):
                try:
                    if (g[iu][iv][0]-g[u][v][0])**2 + (g[iu][iv][1]-g[u][v][1])**2 <= radius**2:
                        g[iu][iv][2] = height
                except:
                    pass
        self.g = g

        self.updatePoles()
        self.showGriduv()
        App.ActiveDocument.commitTransaction()

    def elevateCircle2(self, u=20, v=30, radius=10, height=60):
        ''' change the height for poles around a cenral pole '''

        App.ActiveDocument.openTransaction(
            "elevate Circle " + str((u, v, radius, height)))

        uc = self.obj2.nNodes_u
        vc = self.obj2.nNodes_v

        g = self.g
        for iv in range(v-radius, v+radius+1):
            for iu in range(u-radius, u+radius+1):
                try:
                    g[iu][iv][2] = height
                except:
                    pass
        self.g = g

        self.updatePoles()
        self.showGriduv()
        App.ActiveDocument.commitTransaction()

    def createWaves(self, height=10, depth=-5):
        '''wave pattern over all'''

        App.ActiveDocument.openTransaction(
            "create waves " + str((height, depth)))

        uc = self.obj2.nNodes_u
        vc = self.obj2.nNodes_v

        for iv in range(1, vc-1):
            for iu in range(1, uc-1):

                if (iv+iu) % 2 == 0:
                    self.g[iu][iv][2] = height
                else:
                    self.g[iu][iv][2] = depth

        self.updatePoles()
        self.showGriduv()
        App.ActiveDocument.commitTransaction()

    def addUline(self, vp, pos=0.5):
        ''' insert a line of poles after vp, pos is relative to the next Uline'''

        App.ActiveDocument.openTransaction("add ULine " + str((vp, pos)))

        uc = self.obj2.nNodes_u
        vc = self.obj2.nNodes_v

        if pos <= 0:
            pos = 0.00001
        if pos >= 1:
            pos = 1-0.00001
        pos = 1-pos

        g = self.g

        vline = []
        for i in range(uc):
            # (g[vp-1][i][2]+g[vp][i][2])/2
            vline.append([(g[vp-1][i][0]+g[vp][i][0])/2,
                          (g[vp-1][i][1]+g[vp][i][1])/2, 0])

        vline = []
        for i in range(uc):
            vline.append([(pos*g[vp-1][i][0]+(1-pos)*g[vp][i][0]), (pos*g[vp-1]
                                                                    [i][1]+(1-pos)*g[vp][i][1]), 0])  # (g[vp-1][i][2]+g[vp][i][2])/2

        vline = np.array(vline)

        gg = np.concatenate((g[:vp], [vline], g[vp:]))
        self.g = gg

        self.obj2.nNodes_v += 1

        self.updatePoles()
        self.showGriduv()
        App.ActiveDocument.commitTransaction()

    def addVline(self, vp, pos=0.5):

        # App.ActiveDocument.openTransaction("add Vline " + str((vp,pos)))

        uc = self.obj2.nNodes_u
        vc = self.obj2.nNodes_v

        if pos <= 0:
            pos = 0.00001
        if pos >= 1:
            pos = 1-0.00001
        pos = 1-pos

        g = self.g
        g = g.swapaxes(0, 1)

        vline = []
        for i in range(vc):
            vline.append([(pos*g[vp-1][i][0]+(1-pos)*g[vp][i][0]), (pos*g[vp-1]
                                                                    [i][1]+(1-pos)*g[vp][i][1]), 0])  # (g[vp-1][i][2]+g[vp][i][2])/2

        vline = np.array(vline)

        gg = np.concatenate((g[:vp], [vline], g[vp:]))
        gg = gg.swapaxes(0, 1)
        self.g = gg

        self.obj2.nNodes_u += 1

        self.updatePoles()
        self.showGriduv()
        # App.ActiveDocument.commitTransaction()

    def addS(self, vp):
        ''' harte kante links, weicher uebergang, harte kante rechts '''

        App.ActiveDocument.openTransaction("add vertical S " + str(vp))

        uc = self.obj2.nNodes_u
        vc = self.obj2.nNodes_v

        g = self.g
        g = g.swapaxes(0, 1)

        vline = []
        for i in range(vc):
            pos = 0.5
            if i < 0.3*vc:
                pos = 0.0001
            if i > 0.6*vc:
                pos = 0.9999

            vline.append([(pos*g[vp-1][i][0]+(1-pos)*g[vp][i][0]), (pos*g[vp-1][i]
                                                                    [1]+(1-pos)*g[vp][i][1]), (pos*g[vp-1][i][2]+(1-pos)*g[vp][i][2])])

        vline = np.array(vline)

        gg = np.concatenate((g[:vp], [vline], g[vp:]))

        self.g = gg.swapaxes(0, 1)
        self.obj2.nNodes_u += 1

        self.updatePoles()
        self.showGriduv()
        App.ActiveDocument.commitTransaction()

    def updatePoles(self):
        '''recompute polestring and recompute surface'''

        uc = self.obj2.nNodes_u
        vc = self.obj2.nNodes_v

        ll = ""
        gf = self.g.reshape(uc*vc, 3)
        for i in gf:
            ll += str(list(i)) + ","
        ll = "[" + ll + "]"

        self.obj2.poles = ll
        # self.onChanged(self.obj2,"Height")
        self.update(self.obj2)

    def showSelection(self, pole1, pole2):
        ''' show the pole grid '''
        try:
            print("delete ", self.obj2.polselection.Name)
            App.ActiveDocument.removeObject(self.obj2.polselection.Name)
        except:
            pass
        print(pole1, pole2)
        [u1, v1] = pole1
        [u2, v2] = pole2
        if u1 > u2:
            u1, u2 = u2, u1
        if v1 > v2:
            v1, v2 = v2, v1
        pts = []
        for u in range(u1, u2+1):
            for v in range(v1, v2+1):
                # print (u,v, self.bs.getPole(u+1,v+1))
                pts.append(Part.Vertex(self.bs.getPole(u+1, v+1)))
        com = Part.Compound(pts)
        Part.show(com)
        pols = App.ActiveDocument.ActiveObject
        pols.Label = "Poles Selection"
        pols.ViewObject.PointSize = 8
        pols.ViewObject.PointColor = (1.0, 1.0, 0.0)
        self.obj2.polselection = pols


class ViewProviderNurbs:
    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj

    def attach(self, obj):
        ''' Setup the scene sub-graph of the view provider, this method is mandatory '''
        obj.Proxy = self
        self.Object = obj
        return

    def updateData(self, fp, prop):
        ''' If a property of the handled feature has changed we have the chance to handle this here '''
        return

    def getDisplayModes(self, obj):
        modes = []
        return modes

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Shaded"

    def setDisplayMode(self, mode):
        ''' Map the display mode defined in attach with those defined in getDisplayModes.
        Since they have the same names nothing needs to be done. This method is optional.
        '''
        return mode

    def onChanged(self, vp, prop):
        pass

    def showVersion(self):
        cl = self.Object.Proxy.__class__.__name__
        PySide.QtGui.QMessageBox.information(
            None, "About ", "Nurbs" + "\nVersion " + __version__)

    def setupContextMenu(self, obj, menu):
        cl = self.Object.Proxy.__class__.__name__
        action = menu.addAction("About " + cl)
        action.triggered.connect(self.showVersion)

        action = menu.addAction("Edit ...")
        action.triggered.connect(self.edit)

#        for m in self.cmenu + self.anims():
#            action = menu.addAction(m[0])
#            action.triggered.connect(m[1])

    def getIcon(self):

        return """
            /* XPM */
            static const char * ViewProviderNurbs_xpm[] = {
            "16 16 6 1",
            "     c None",
            ".    c #141010",
            "+    c #615BD2",
            "@    c #C39D55",
            "#    c #000000",
            "$    c #57C355",
            "        ........",
            "   ......++..+..",
            "   .@@@@.++..++.",
            "   .@@@@.++..++.",
            "   .@@  .++++++.",
            "  ..@@  .++..++.",
            "###@@@@ .++..++.",
            "##$.@@$#.++++++.",
            "#$#$.$$$........",
            "#$$#######      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            " #$#$$$$$#      ",
            "  ##$$$$$#      ",
            "   #######      "};
            """

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def edit(self):
        import nurbs_dialog
        #reload(nurbs_dialog)
        App.tt = self
        self.Object.Object.generatePoles = False
        self.Object.Object.Label = "Nurbs individual"
        self.miki = nurbs_dialog.mydialog(self.Object)

    def setEdit(self, vobj, mode=0):
        self.edit()
        return True

    def unsetEdit(self, vobj, mode=0):
        return True

    def doubleClicked(self, vobj):
        return False


def makeNurbs(uc=5, vc=7):

    a = App.ActiveDocument.addObject("Part::FeaturePython", "Nurbs")
    a.Label = "Nurbs generated"
    Nurbs(a, uc, vc)
    ViewProviderNurbs(a.ViewObject)
    a.ViewObject.ShapeColor = (0.00, 1.00, 1.00)
    a.ViewObject.Transparency = 50
    return a


def createnurbs():

    a = makeNurbs(6, 10)
    a.solid = False
    a.base = False
    # a.grid=False

    polestring = '''[
    [0.0, 0.0, 0.0], [40.0, 0.0, 0.0], [80.0, 0.0, 0.0], [
        120.0, 0.0, 0.0], [160.0, 0.0, 0.0], [200.0, 0.0, 0.0],
    [0.0, 30.0, 0.0], [40.0, 30.0, 0.0], [80.0, 30.0, 0.0], [
        120.0, 30.0, 0.0], [160.0, 30.0, -60.0], [200.0, 30.0, 0.0],
    [0.0, 60.0, 0.0], [40.0, 60.0, 0.0], [80.0, 60.0, 0.0], [
        120.0, 60.0, -60.0], [160.0, 60.0, -60.0], [200.0, 60.0, 0.0],
    [0.0, 90.0, 0.0], [40.0, 90.0, 0.0], [80.0, 90.0, 0.0], [
        120.0, 90.0, 0.0], [160.0, 90.0, 0.0], [200.0, 90.0, 0.0],
    [0.0, 120.0, 0.0], [40.0, 120.0, 0.0], [80.0, 120.0, 0.0], [
        120.0, 120.0, 0.0], [160.0, 120.0, 0.0], [200.0, 120.0, 0.0],
    [0.0, 150.0, 0.0], [40.0, 150.0, 0.0], [80.0, 150.0, 100.0], [
        120.0, 150.0, 100.0], [160.0, 150.0, 80.0], [200.0, 150.0, 0.0],
    [0.0, 180.0, 0.0], [40.0, 180.0, 0.0], [80.0, 180.0, 0.0], [120.0, 180.0, 100.0], [160.0, 180.0, 80.0], [200.0, 180.0, 0.0], [
    0.0, 210.0, 0.0], [40.0, 210.0, 100.0], [80.0, 210.0, 0.0], [120.0, 210.0, 0.0], [160.0, 210.0, 0.0], [200.0, 210.0, 0.0],
    [0.0, 240.0, 0.0], [40.0, 240.0,0.0], [80.0, 240.0, 0.0], [
        120.0, 240.0, 0.0], [160.0, 240.0, 0.0], [200.0, 240.0, 0.0],
    [0.0, 270.0, 0.0], [40.0, 270.0, 0.0], [80.0, 270.0, 0.0], [120.0, 270.0, 0.0], [160.0, 270.0, 0.0], [200.0, 270.0, 0.0]]'''

    polarr = eval(polestring)
    ps = [App.Vector(tuple(v)) for v in polarr]

    a.poles = polestring
    # ps=a.Proxy.getPoints()

    a.Proxy.togrid(ps)
    a.Proxy.updatePoles()
    a.Proxy.showGriduv()

    App.ActiveDocument.recompute()
    Gui.updateGui()

    Gui.activeDocument().activeView().viewAxonometric()
    Gui.SendMsgToActiveView("ViewFit")
    a.ViewObject.startEditing()
    a.ViewObject.finishEditing()
    a.polselection.ViewObject.hide()


def testRandomB():

    nd = App.newDocument("Unnamed")
    App.setActiveDocument(nd.Name)
    App.ActiveDocument = App.getDocument(nd.Name)
    Gui.ActiveDocument = Gui.getDocument(nd.Name)

    na = 20
    b = 10

    a = makeNurbs(b, na)

    a.solid = False
    a.base = False
    # a.grid=False
    a.gridCount = 6

    ps = a.Proxy.getPoints()

    if 0:
        print("random ..")
        ps = np.array(App.ps).swapaxes(0, 1)
        temp, ct = ps.shape
        ps[2] += 100*np.random.random(ct)
        ps = ps.swapaxes(0, 1)
    #    ps[0:3]

    ps = np.array(ps)
    ps.resize(na, b, 3)

    for k0 in range(10):
        k = random.randint(0, na-6)
        l = random.randint(1, b-1)
        for j in range(3):
            ps[k+j][l][2] += 60
        rj = random.randint(0, 2)
        print(k, rj)
        for j in range(rj):
            ps[k+3+j][l][2] += 60

    for k0 in range(10):
        k = random.randint(0, na-5)
        l = random.randint(1, b-1)

        for j in range(2):
            ps[k+j][l][2] += 30
        rj = random.randint(0, 2)
        print(k, rj)
        for j in range(rj):
            ps[k+2+j][l][2] += 30

    ps.resize(na*b, 3)

    a.Proxy.togrid(ps)
    a.Proxy.elevateVline(2, 0)

    a.Proxy.updatePoles()
    a.Proxy.showGriduv()

    App.a = a
    App.ps = ps

    Gui.activeDocument().activeView().viewAxonometric()
    Gui.SendMsgToActiveView("ViewFit")


def testRandomCylinder():

    nd = App.newDocument("Unnamed")
    App.setActiveDocument(nd.Name)
    App.ActiveDocument = App.getDocument(nd.Name)
    Gui.ActiveDocument = Gui.getDocument(nd.Name)

    na = 30
    b = 30

    a = makeNurbs(b, na)
    a.model = "NurbsCylinder"

    a.solid = False
    a.base = False
    # a.grid=False
    a.gridCount = 20

    ps = a.Proxy.getPoints()
    print("points ps", len(ps))

    if 0:
        print("random ..")
        ps = np.array(App.ps).swapaxes(0, 1)
        temp, ct = ps.shape
        ps[2] += 100*np.random.random(ct)
        ps = ps.swapaxes(0, 1)
    #    ps[0:3]

    ps = np.array(ps)
    ps.resize(na, b, 3)

    for k0 in range(25):
        k = random.randint(0, na-3)
        l = random.randint(1, b-1)
        for j in range(1):
            ps[k+j][l][2] += 100*random.random()
        rj = random.randint(0, 1)
        print(k, rj)
        for j in range(rj):
            ps[k+j][l][2] += 100*random.random()

    for k0 in range(10):
        k = random.randint(0, na-3)
        l = random.randint(1, b-1)

        for j in range(1):
            ps[k+j][l][2] += 200*random.random()
        rj = random.randint(0, 1)
        print(k, rj)
        for j in range(rj):
            ps[k+j][l][2] += 200*random.random()

    ps.resize(na*b, 3)

    a.Proxy.togrid(ps)
#    a.Proxy.elevateVline(2,0)

    a.Proxy.updatePoles()
    a.Proxy.showGriduv()

    App.a = a
    App.ps = ps

    Gui.activeDocument().activeView().viewAxonometric()
    Gui.SendMsgToActiveView("ViewFit")


def testRandomSphere():

    nd = App.newDocument("Unnamed")
    App.setActiveDocument(nd.Name)
    App.ActiveDocument = App.getDocument(nd.Name)
    Gui.ActiveDocument = Gui.getDocument(nd.Name)

    na = 17
    b = 15

    pass1 = 15
    pass2 = 10
#    App.ParamGet('User parameter:Plugins/nurbs').SetBool("createNurbsShape",True)

    # for larger tests
    # App.ParamGet('User parameter:Plugins/nurbs').SetBool("createNurbsShape",False)


#    App.ParamGet('User parameter:Plugins/nurbs/randomSphere').SetInt("countLatitude",30)
#    App.ParamGet('User parameter:Plugins/nurbs/randomSphere').SetInt("countLongitude",120)
#    App.ParamGet('User parameter:Plugins/nurbs/randomSphere').SetInt("countRandom1",200)
#    App.ParamGet('User parameter:Plugins/nurbs/randomSphere').SetInt("countRandom2",100)

    na = App.ParamGet(
        'User parameter:Plugins/nurbs/randomSphere').GetInt("countLatitude", 100)
    b = App.ParamGet(
        'User parameter:Plugins/nurbs/randomSphere').GetInt("countLongitude", 100)
    pass1 = App.ParamGet(
        'User parameter:Plugins/nurbs/randomSphere').GetInt("countRandom1", 100)
    pass2 = App.ParamGet(
        'User parameter:Plugins/nurbs/randomSphere').GetInt("countRandom2", 100)

    if 0:
        na = 500
        b = 500
        pass1 = 5000
        pass2 = 5000

    if 0:
        na = 1000
        b = 1500
        pass1 = 500000
        pass2 = 250000

    if 0:
        na = 100
        b = 300
        pass1 = 500
        pass2 = 500

    a = makeNurbs(b, na)
    a.model = "NurbsSphere"

    a.solid = False
    a.base = False
    # a.grid=False

    # a.gridCount=1000

    ps = a.Proxy.getPoints()
    print("points ps", len(ps))

    if 0:
        print("random ..")
        ps = np.array(App.ps).swapaxes(0, 1)
        temp, ct = ps.shape
        ps[2] += 100*np.random.random(ct)
        ps = ps.swapaxes(0, 1)
    #    ps[0:3]

    ps = np.array(ps)
    ps.resize(na, b, 3)

    for k0 in range(pass1):
        k = random.randint(2, na-3)
        l = random.randint(1, b-1)
        for j in range(1):
            ps[k+j][l][2] += 1*random.random()
        rj = random.randint(0, 1)
#        print (k,rj)
        for j in range(rj):
            ps[k+j][l][2] += 1*random.random()
        if k0 % 1000 == 0:
            print(k0)
            Gui.updateGui()

    for k0 in range(pass2):
        k = random.randint(2, na-3)
        l = random.randint(1, b-1)

        for j in range(1):
            ps[k+j][l][2] += 2*random.random()
        rj = random.randint(0, 1)
#        print (k,rj)
        for j in range(rj):
            ps[k+j][l][2] += 2*random.random()
        if k0 % 1000 == 0:
            print(k0)
            Gui.updateGui()

    ps.resize(na*b, 3)
    print("A")
    print(time.time())
    Gui.updateGui()

    a.Proxy.togrid(ps)
    print("B")
    print(time.time())
    Gui.updateGui()

#    a.Proxy.elevateVline(2,0)

    a.Proxy.updatePoles()

    print("c")
    print(time.time())
    Gui.updateGui()
    a.Proxy.showGriduv()
    print("d")
    print(time.time())
    Gui.updateGui()

    App.ActiveDocument.recompute()
    App.ActiveDocument.recompute()

    App.a = a
    App.ps = ps

    Gui.activeDocument().activeView().viewAxonometric()
    Gui.SendMsgToActiveView("ViewFit")

class Nurbs_NurbsRandomTours:
    def Activated(self):
        self.testRandomTorus()
        
    def testRandomTorus(self):

        na = 7
        b = 4

        nd = App.newDocument("Unnamed")
        App.setActiveDocument(nd.Name)
        App.ActiveDocument = App.getDocument(nd.Name)
        Gui.ActiveDocument = Gui.getDocument(nd.Name)

        a = makeNurbs(b, na)
        a.model = "NurbsTorus"

        a.solid = False
        a.base = False
        # a.grid=False
        a.gridCount = 20

        ps = a.Proxy.getPoints()
        print("points ps", len(ps))

        ps = a.Proxy.getPoints()
        print("A")
        a.Proxy.togrid(ps)
        print("B")
        a.Proxy.updatePoles()
        print("C")
        a.Proxy.showGriduv()

        '''
        if 0:
            print ("random .."
            ps=np.array(App.ps).swapaxes(0,1)
            temp,ct=ps.shape
            ps[2] += 100*np.random.random(ct)
            ps=ps.swapaxes(0,1)
        #    ps[0:3]

        ps=np.array(ps)
        ps.resize(na,b,3)


        for k0 in range(15):
            k=random.randint(2,na-3)
            l=random.randint(1,b-1)
            for j in range(1):
                ps[k+j][l][2] += 100*random.random()
            rj=random.randint(0,1)
            print (k,rj)
            for j in range(rj):
                ps[k+j][l][2] += 100*random.random()

        for k0 in range(10):
            k=random.randint(2,na-3)
            l=random.randint(1,b-1)

            for j in range(1):
                ps[k+j][l][2] += 200*random.random()
            rj=random.randint(0,1)
            print (k,rj)
            for j in range(rj):
                ps[k+j][l][2] += 200*random.random()


        ps.resize(na*b,3)


        a.Proxy.togrid(ps)
    #    a.Proxy.elevateVline(2,0)

        '''

        App.a = a
        App.ps = ps

        Gui.activeDocument().activeView().viewAxonometric()
        Gui.SendMsgToActiveView("ViewFit")

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_NurbsRandomTours")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_NurbsRandomTours"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_NurbsRandomTours", Nurbs_NurbsRandomTours())



class Nurbs_NurbsTest:
    def Activated(self):
        self.runtest() 
    def runtest(self):
        global createnurbs
        try:
            App.closeDocument("Unnamed")
        except:
            pass

        if App.ActiveDocument == None:
            App.newDocument("Unnamed")
            App.setActiveDocument("Unnamed")
            App.ActiveDocument = App.getDocument("Unnamed")
            Gui.ActiveDocument = Gui.getDocument("Unnamed")

    #    createnurbs()

        na = 10
        b = 10

        a = makeNurbs(b, na)

        a.solid = False
        a.base = False
        ps = a.Proxy.getPoints()
        a.Proxy.togrid(ps)
        a.Proxy.updatePoles()
        a.Proxy.showGriduv()

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_NurbsTest")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_NurbsTest"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_NurbsTest", Nurbs_NurbsTest())



class Nurbs_NurbsTest2:
    def Activated(self):
        self.runtest2()    
    def runtest2(self):
        # testRandomB()
        testRandomCylinder()
        # testRandomSphere()
        # testRandomTorus()

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_NurbsTest2")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_NurbsTest2"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_NurbsTest2", Nurbs_NurbsTest2())



'''

nurbs

nurbs.testRandomB()
nurbs.testRandomCylinder()
nurbs.testRandomSphere()
nurbs.testRandomTorus()


'''
