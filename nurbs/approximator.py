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
#approximate  a point cloud by a bezier curve
# -------------------------------------------------
# --
# --
# -- microelly 2018  0.2
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------


import Draft
import Points
import Part
import Sketcher
import os,sys
import random
import time
import FreeCAD as App
import FreeCADGui as Gui
import NURBSinit
import inspect
from  pyob import FeaturePython, ViewProvider
from  scipy import misc
from  scipy import signal
from  scipy.optimize import minimize
from  miki_g import createMikiGui2, MikiApp
import Design456Init

try:
    import numpy as np 
except ImportError:
    print ("Please install the required module : numpy")
    
try:
    import imageio
except ImportError:
    print ("Please install the required module :imageio")
import say

#reload(say)

#reload(miki_g)


def getPart(name="hugo"):
    '''objekt bereitstellen bzw. anlegen'''

    obj = App.ActiveDocument.getObject(name)
    if obj == None:
        obj = App.ActiveDocument.addObject("Part::Feature", name)
    return obj


# diagramm fuer filter nur einmal am anfang zeigen
diagram = False


def runfilt(t, xn, degree=2, lowfilt=0.005):
    '''signale-filter fuer PointCloudApprox'''

    global diagram

    if 0:
        mymin = -5
        mymax = 5
        xn2 = []
        for x in xn:
            if x < mymin: xn2 += [mymin]
            elif x > mymax: xn2 += [mymax]
            else: xn2 += [x]
        xn = xn2

    b, a = signal.butter(degree, lowfilt)

    zi = signal.lfilter_zi(b, a)
    z, _ = signal.lfilter(b, a, xn, zi=zi*xn[0])
    z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])
    y = signal.filtfilt(b, a, xn)

    if 1 or not diagram:
        if 0:  # in midi-bereich
            import Plot
            Plot.figure("Smooth Filter for Points")
        else:  # eigenes fenster
            import Plot2 as Plot
            Plot.figureWindow("Smooth Filter for Points")

        Plot.plot(t, xn, 'points')
        Plot.plot(t, y, 'filter')
        Plot.legend(True)
        Plot.grid(True)
        diagram = True

    return (t, y)

# ----------------------------------------


# Approximation einer Punktwolke durche ine Kurve
#
#


class PointCloudApprox(FeaturePython):
    def __init__(self, obj, label=None, points=None, start=None):
        FeaturePython.__init__(self, obj)

        obj.addProperty("App::PropertyInteger", "count").count = 10
        obj.addProperty("App::PropertyInteger", "degree").degree = 10
        obj.addProperty("App::PropertyFloat", "lowfilter").lowfilter = 2
        obj.addProperty("App::PropertyFloat", "threshold").threshold = 5

        obj.addProperty("App::PropertyLink", "Points")
        obj.addProperty("App::PropertyLink", "Start")
#        obj.addProperty("App::PropertyBool","createBSpline","smooth")
#        obj.addProperty("App::PropertyBool","closeBSpline","smooth")
#        obj.addProperty("App::PropertyInteger","discretizeCount").discretizeCount=30
        obj.addProperty("App::PropertyBool", "active", "smooth")
        obj.addProperty("App::PropertyBool", "closed", "smooth")
        obj.Points = points
        obj.Start = start

    def runPountCloudApprox(self, obj, bo=None):

        dd = obj.count
        name = obj.Name
        ao = obj.Start
        a = ao.Shape
        w = obj.Points.Points.Points

        pts = []
        ptsu = []
        comps = []
        for i, bbb in enumerate(w):
            b = Part.Point(bbb).toShape()
            rc = a.distToShape(b)
            if rc[0] > 0:
                (pa, pb) = rc[1][0]
                comps += [Part.makePolygon([pb, pa])]

                c = a.Edge1.Curve
                try:
                    p = c.parameter(pb)
                    n = c.normal(p)
                    if abs((pb-pa).dot(n)) < obj.threshold:
                        pts += [App.Vector(p, (pb-pa).dot(n))]

                except:
                    print("ignore", i)

        hop = getPart(name+"_helper")
        hop.Shape = Part.Compound(comps)
        hop.ViewObject.hide()

        # sortieren
        pts2 = sorted(pts, key=lambda x: x[0])
        pts3 = pts2

        for l in [0]:  # anzahl der durchlaeufe

            pts2 = pts3
            ll = len(pts2)

            pts3 = [pts2[0]]
            x = []
            y = []
            for i in range(ll):
                x += [pts2[i].x]
                y += [pts2[i].y]

            if obj.closed:  # zyklisch -enden anpassen
                sx = x[0]
                ex = x[-1]
                xx = [v+(ex-sx) for v in x]
                x0 = [v-(ex-sx) for v in x]
                ll = len(x)

                (x2, y2) = runfilt(x0+x+xx, y+y+y, obj.degree, 0.001*obj.lowfilter)
                pts3 = [App.Vector(x, y)
                                   for (x, y) in zip(x2[ll:2*ll], y2[ll:2*ll])]

            else:
                (x2, y2) = runfilt(x, y, obj.degree, 0.001*obj.lowfilter)
                pts3 = [App.Vector(x, y) for (x, y) in zip(x2, y2)]

            pts4 = []
            pts5 = []
            for p in pts3:
                pts4 += [c.value(p.x)+c.normal(p.x)*p.y]
                pts5 += [c.value(p.x), c.value(p.x) +
                                 c.normal(p.x)*p.y, c.value(p.x)]

            hop = getPart(name+"_Wire")
            hop.Shape = Part.makePolygon(pts4)

            import smooth
            #reload(smooth)
            smooth = App.ActiveDocument.getObject("smooth"+"_"+name)
            if smooth == None:
                smooth.smoothWire(hop, "smooth"+"_"+name)
            else:
                print("setze smooth count ", dd)
                smooth.Wire = hop
                smooth.discretizeCount = dd

    def onChanged(self, obj, prop):
        if not hasattr(obj, "active"): return
        if prop in ['count', 'degree', 'lowfilter', 'threshold']:
            self.runPountCloudApprox(obj)


# a BSpline approximation is calculated for a point cloud and a start curve
# the interferences are removed with scipy.signal.filtfilt
# the deviation from the suggested curve is used as the amplitude

def createPointCloudApprox():
    '''methode wird vom Dialog smoothPointcloud aufgerufen'''

    [points, start] = Gui.Selection.getSelection()
    name = points.Name+"_from_"+start.Name

    a = App.ActiveDocument.addObject("Part::FeaturePython", name)
    PointCloudApprox(a, name, points, start)
    ViewProvider(a.ViewObject)
    return a

class Nurbs_smoothPointcloudGUI:
    def Activated(self):
        self._smoothPointcloudGUI()
    
    def _smoothPointcloudGUI(self):
        '''smooth the point cloud to a bspline curve'''
        mikigui = createMikiGui2(layout, myApp)
        mikigui.part = createPointCloudApprox()
        mikigui.run()
        return mikigui

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_smoothPointcloudGUI")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_smoothPointcloudGUI"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_smoothPointcloudGUI", Nurbs_smoothPointcloudGUI())


def _smoothPointcloudGUI():
	'''smooth the point cloud to a bspline curve'''

##\cond
	layout = '''
	MainWindow:
		QtGui.QLabel:
			setText:"***   D E M O 1  ***"

		HorizontalGroup:
			setTitle: "Mode"
			QtGui.QComboBox:
				id: 'mode'
				addItem: "all"
				#addItem: "none"
				addItem: "vertical"
				addItem: "horizontal"

		HorizontalGroup:
			setTitle: "Tangent Force v"

			QtGui.QDial:
				id: 'tbb'
				setFocusPolicy: QtCore.Qt.StrongFocus
				valueChanged.connect: app.run
				setMinimum: 5
				setValue: 10
				setMaximum: 50

		QtGui.QPushButton:
			setText: "Run Action"
			clicked.connect: app.run

		QtGui.QPushButton:
			setText: "change Image"
			clicked.connect: app.changeImage

		QtGui.QPushButton:
			setText: "close"
			clicked.connect: app.myclose

		setSpacer:
		# temp image widget prototype
		PicWidget:
			id: 'image'
			sizeX: 400
			sizeY: 200
			run_display: "/home/thomas/Bilder/bp_841.png"
		'''


class myApp(MikiApp):
    # temp. testdaten fuer den image widget
    index = 0
    images = [NURBSinit.ICONS_PATH+"bp_842.png",
    NURBSinit.ICONS_PATH+"bp_843.png",
    NURBSinit.ICONS_PATH+"bp_844.png"
    ]
    def myclose(self):
        self.close()
    def changeImage(self):
        '''test method for image widget '''
        self.root.ids['image'].run_display(self.images[self.index])
        self.index += 1
        if self.index >= len(self.images): self.index = 0
    def run(self):
        modus = self.root.ids['mode'].currentText()
        try:
            print("part is ..", self.part)
        except:
            print("no object assigned yet")
            return
        try:
            tb = self.root.ids['tbb'].value()
            self.part.count = int(round(tb))
        except:
            return

# \ endcond

# load the points from an image - the image must
# to be reworked with methods of the reconstruction wb


class ImagePoints(FeaturePython):

    def __init__(self, obj):
        FeaturePython.__init__(self, obj)
        obj.addProperty("App::PropertyFile", "image")
        obj.addProperty("App::PropertyInteger", "min").min = 150
        obj.addProperty("App::PropertyInteger", "max").max = 1000
        obj.addProperty("App::PropertyIntegerList",
                        "params").params = [1, 1, 1, 1]

    def execute(self, obj):
        import imageio
        face = imageio.imread(obj.image)#misc.imread(obj.image)

        face2 = obj.params[0]*face[:, :, 0]+obj.params[1] * \
            face[:, :, 1]+obj.params[2]*face[:, :, 2]
        (uc, vc) = face2.shape

        pts = []
        for u in range(uc):
            for v in range(vc):
                if face2[u, v] > obj.min and face2[u, v] < obj.max:
                    pts += [App.Vector(v, u, face2[u, v]*obj.params[3])]

        obj.Points = Points.Points(pts)

class Nurbs_loadPointcloudfromImageGUI:
    def Activated(self):
        self._loadPointcloudfromImageGUI()
        
    def _loadPointcloudfromImageGUI(self):
        ''' Load image file'''

        fn = '/home/thomas/Downloads/Profil-Punktewolke3D.png'
        yy = App.ActiveDocument.addObject("Points::FeaturePython", "ImagePoints")
        ImagePoints(yy)
        yy.image = fn
        ViewProvider(yy.ViewObject)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_loadPointcloudfromImageGUI")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_loadPointcloudfromImageGUI"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_loadPointcloudfromImageGUI", Nurbs_loadPointcloudfromImageGUI())



# ------------------------ Show image on nurbs

class ImagePoints2(FeaturePython):

    def __init__(self, obj, mode='generic'):
        FeaturePython.__init__(self, obj)
        obj.addProperty("App::PropertyFile", "image")
        obj.addProperty("App::PropertyFloat", "R").R = 100
        obj.addProperty("App::PropertyFloat", "h").h = 0.01
        obj.addProperty("App::PropertyFloat", "factor").factor = 100.
        obj.addProperty("App::PropertyFloatList", "params").params = [
                        1., 1., 1., 1., 0.]
        obj.addProperty("App::PropertyEnumeration", "mode")

        obj.addProperty("App::PropertyInteger", "degree").degree = 3
        obj.mode = ['generic', 'cylinder', 'face']
        obj.mode = mode
        obj.setEditorMode("mode", 2)
        if mode == 'face':
            obj.addProperty("App::PropertyLink", "source")
            obj.addProperty("App::PropertyInteger", "faceNumber")

    def execute(self, obj):
        face=None
        if obj.image != '':
            img = imageio.imread(obj.image)
            im_arr = np.fromstring(img.tobytes(), dtype=np.uint8)
            zd = im_arr.shape[0]/img.shape[0]/img.shape[1]
            print(zd)
            im_arr = im_arr.reshape(img.shape[1], img.shape[0], int(zd))
            face = im_arr
        else:
            face = np.ones(20*20*3).reshape(20, 20, 3)

        (uc, vc, _) = face.shape
        print(face.shape)

        # face=face[10:,-10:]
        (uc, vc, _) = face.shape
        print("Image-size", face.shape)

        if obj.mode == 'generic':
            poles = []
            for u in range(uc):
                pts = []
                for v in range(vc):
                        pts += [App.Vector(v, u, 0.01*sum(face[u, v]))]
                poles += [pts]

        if obj.mode == 'cylinder':
            R = 100
            h = 0.01
            poles = []
            for u in range(uc):
                pts = []
                for v in range(vc):
                        ss = sum(face[u, v])
                        ss = face[u, v, 0]*obj.params[0]+face[u, v, 1] * \
                            obj.params[1]+face[u, v, 2]*obj.params[2]
                        pts += [App.Vector((R+h*ss)*np.cos(v*np.pi*0.5/vc),
                                -(R+h*ss)*np.sin(v*np.pi*0.5/vc), -R*u/uc*np.pi*0.4)]
                poles += [pts]

        if obj.mode == 'face':  # bump auf freiform-flaeche

            ff = obj.source.Shape.Faces[obj.faceNumber].toNurbs()
            bs = ff.Face1.Surface.copy()
            bs.increaseDegree(3, 3)
            print("upuesl", bs.getUKnots())
            print("vpuesl", bs.getVKnots())
#            print bs
            # mit rand

            mitrand = 1

            if mitrand:
                scu = uc
                scv = vc
            else:
                # phne rand
                scu = uc
                scv = vc

            print("basic figure start")
            poles = np.array(bs.getPoles())
            print(poles.shape)

            c = bs.uIso(0)
            c = bs.vIso(0)

            l = int(round(c.length()/10)-1)
            l = c.length()

            if mitrand:
                ups = [0]
                for i in range(1, scu):
                    p = c.parameterAtDistance(l/scu*i)

                    try:
                        bs.insertUKnot(p, 1, 0)
                        ups += [p]
                    except:
                        print("fehler", i, p)
                        pass
                ups += [c.parameterAtDistance(l)]
            else:
                ups = []
                for i in range(scu):
                    p = c.parameterAtDistance(l/scu*i)
                    print("parameter uu", i, p)
                    try:
                        bs.insertUKnot(p, 1, 0)
                        ups += [p]
                    except:
                        pass


#            print ("ups",ups)
            print("---------------")
            print("len bs knots", len(bs.getUKnots()))
            print
            yinterp = np.interp(bs.getUKnots(), ups, range(len(ups)))
#            print yinterp
            print

            c = bs.vIso(0)
            c = bs.uIso(0)

            l = int(round(c.length()/10)-1)
            l = c.length()
            # print c.getKnots(),"------------"
            mm = c.getKnots()[-1]

            if mitrand:
                vps = [0]
    #            print bs.getVKnots()

                for i in range(1, scv):
                    p = c.parameterAtDistance(l/scv*i)
                    try:
                        bs.insertVKnot(p, 1, 0)
                        vps += [p]
                    except:
                        pass

                vps += [c.parameterAtDistance(l)]

            else:
                vps = []
                for i in range(scv):
                    p = c.parameterAtDistance(l/scv*i)

                    try:
                        bs.insertVKnot(p, 1, 0)
                        vps += [p]
                    except:
                        pass
                    if vps[-1] != p:

                        vps += [p]

            poles = np.array(bs.getPoles())

            # -------------------------------------
            print("Figur shape", poles.shape)
            print("upuesl", bs.getUKnots())
            print("vpuesl", bs.getVKnots())

            poles2 = poles.copy()

            # Part.show(bs.toShape())

            uc, vc, _ = poles.shape

            uc2, vc2 = scu, scv
            print("Basic figure", poles2.shape)

            print("uc2,vc2", uc2, vc2)
            print(len(vps))

#            print vps
#            for u in range(2,uc2-2):
#                for v in range(2,vc2-2):
#                    [ui,vi]=bs.parameter(App.Vector(poles[u,v]))
#                    n=bs.normal(ui,vi)
#                    ss=face[u,v,0]*obj.params[0]+face[u,v,1]*obj.params[1]+face[u,v,2]*obj.params[2]
#                    poles2[u,v] +=  0.001*obj.factor*ss*n
#
#            print (len(ups),len(vps))
#            adds=np.zeros(len(ups)*len(vps)*3)
#            adds=adds.reshape(len(ups),len(vps),3)

            if mitrand:
                ssab = []
                print("!##", face.shape, uc2, vc2)
                for u in range(uc2-1):
                    ssa = [0]
                    for v in range(vc2-1):
                        ssa += [(face[u, v, 0]*obj.params[0]+face[u, v, 1]*obj.params[1] +
                                 face[u, v, 2]*obj.params[2])*obj.params[3]+obj.params[4]]
                    ssa += [0]
                    print(len(ups[:-1]))
                    print(len(ups))
                    print(len(ssa))
                    print("huhu")
                    yinterp = np.interp(bs.getUKnots(), ups, ssa)
    #                print u
    #                print yinterp
                    ssab += [yinterp]
    #            print ("erstes shape"
    #            print np.array(ssab).shape
    #            print  (len(bs.getUKnots())
    #            print bs.getUKnots()
    #            print  (len(bs.getVKnots())
    #            print bs.getVKnots()

                ssab = np.array(ssab).swapaxes(0, 1)
                print("ssab.shape ", ssab.shape)
                print("--------------")
                ssba = [[0]*len(bs.getVKnots())]
                # vps += [0]

                for ui, u in enumerate(bs.getUKnots()):
                    ssa = [0]
                    print("-------------")
                    print(len(vps[:-1]))
                    print(len(ssab[ui]))
                    yinterp = np.interp(bs.getVKnots(), vps[:-2], ssab[ui])
    #                print u
    #                print yinterp
                    ssba += [yinterp]

                ssba += [[0]*len(bs.getVKnots())]
                print("zweites shape")
                print(np.array(ssba).shape)
    #            print ("u ",len(bs.getUKnots())
    #            print ("v ", len(bs.getVKnots())

                ssba = np.array(ssba)

                print("Zielarray poles2 shape ", poles2.shape)
                print("belegugn", len(bs.getUKnots()), len(bs.getVKnots()))

                for u in range(len(bs.getUKnots())):
                    for v in range(len(bs.getVKnots())):
                        [ui, vi] = bs.parameter(App.Vector(poles[u+1, v+1]))
                        n = bs.normal(ui, vi)
                        poles2[u+1, v+1] += 0.001*obj.factor*(ssba[u, v])*n

            else:

                ssab = []
                print("!##", face.shape, uc2, vc2)
                for u in range(uc2):
                    ssa = []
                    for v in range(vc2):
                        ssa += [(face[u, v, 0]*obj.params[0]+face[u, v, 1]*obj.params[1] +
                                 face[u, v, 2]*obj.params[2])*obj.params[3]+obj.params[4]]
                    # ssa +=[0]
    #                print  (len(ups)
    #                print  (len(ssa)
#                    print
#                    print bs.getUKnots()
#                    print
#                    print ups
#                    print
#                    print ssa
#                    if u==4: return
                    yinterp = np.interp(bs.getUKnots(), ups, ssa)
    #                print u
    #                print yinterp
                    ssab += [yinterp]
                print("erstes shape")
    #            print np.array(ssab).shape
                print(len(bs.getUKnots()))
    #            print bs.getUKnots()
                print(len(bs.getVKnots()))
    #            print bs.getVKnots()

                ssab = np.array(ssab).swapaxes(0, 1)
                print("ssab.shape ", ssab.shape)
    #            print ("--------------"
                ssba = []
                # vps += [0]

                for ui, u in enumerate(bs.getUKnots()):
                    ssa = [0]
#                    print ("-------gg------",ui,u)
#                    print (len(vps),len(ups))
#                    print  (len(ssab[ui])
#                    print bs.getVKnots()
#                    print vps
#                    print ssab[ui]
#                    if ui==1: return
                    yinterp = np.interp(bs.getVKnots(), vps, ssab[ui])
    #                print u
    #                print yinterp
                    ssba += [yinterp]

#                ssba += [[0]*len(bs.getVKnots())]
                print("zweites shape")
                print(np.array(ssba).shape)
    #            print ("u ",len(bs.getUKnots())
    #            print ("v ", len(bs.getVKnots())

                ssba = np.array(ssba)

                print("Zielarray poles2 shape ", poles2.shape)
                print("belegugn", len(bs.getUKnots()), len(bs.getVKnots()))

                for u in range(len(bs.getUKnots())):
                    for v in range(len(bs.getVKnots())):
                        [ui, vi] = bs.parameter(App.Vector(poles[u+1, v+1]))
                        n = bs.normal(ui, vi)
                        poles2[u, v] += 100
                        # poles2[u,v] +=  0.001*obj.factor*(ssba[u,v])*n

            # return
            um = bs.getUMultiplicities()
            vm = bs.getVMultiplicities()
            bs.buildFromPolesMultsKnots(poles2,
                                um, vm, range(len(um)), range(len(vm)), False, False, bs.UDegree, bs.VDegree)
#            Part.show(bs.toShape())
            poles = poles2
#            return

        degree = obj.degree

        if degree == 0:
            comps = []
            for pols in [poles, poles.swapaxes(0, 1)]:
                for ps in pols:
                    comps += [Part.makePolygon([App.Vector(p) for p in ps])]
            obj.Shape = Part.Compound(comps)

        else:
            bc = Part.BSplineSurface()
            ya = [degree+1]+[1]*(uc-degree-1)+[degree+1]
            yb = [degree+1]+[1]*(vc-degree-1)+[degree+1]

            bc.buildFromPolesMultsKnots(poles,
                ya, yb, range(len(ya)), range(len(yb)),
                False, False, degree, degree)

            obj.Shape = bc.toShape()

#Attach an image to a cylinder 
class Nurbs_LoadCylinderfacefromImageGUI:
    def Activated(self):
        self._loadCylinderfacefromImageGUI()
    
    def _loadCylinderfacefromImageGUI(self):
        yy = App.ActiveDocument.addObject("Part::FeaturePython", "ImageSurface")
        ImagePoints2(yy)
        yy.mode = 'cylinder'
        fn = Design456Init.NURBS_IMAGES_PATH+'2364.png'
        yy.image = fn
        ViewProvider(yy.ViewObject)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_LoadCylinderfacefromImageGUI")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_LoadCylinderfacefromImageGUI"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_LoadCylinderfacefromImageGUI", Nurbs_LoadCylinderfacefromImageGUI())



class Nurbs_BumpFacefromImageGUI:
    def Activated(self):
        self._BumpFacefromImageGUI()
        
    def _BumpFacefromImageGUI(self):

        fn = Design456Init.NURBS_IMAGES_PATH+"profil_for_bump.png"

        yy = App.ActiveDocument.addObject("Part::FeaturePython", "ImageSurface")
        ImagePoints2(yy, mode='face')
        yy.source = Gui.Selection.getSelection()[0]
        yy.image = fn
        ViewProvider(yy.ViewObject)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_BumpFacefromImageGUI")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_BumpFacefromImageGUI"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_BumpFacefromImageGUI", Nurbs_BumpFacefromImageGUI())




# -----------------------------------------


class MinLengthBezier(FeaturePython):
    ''' gegeben 7 Punkte Spline, finde optimale Kurve durch Mittelpunkt, durch Endpunkt und Endtangenten'''

    def __init__(self, obj, mode='minimal Lenght', method='Default'):
        FeaturePython.__init__(self, obj)
        obj.addProperty("App::PropertyLink", "path", "source")
        obj.addProperty("App::PropertyFloat", "factor", "config")  # .factor=30
        obj.addProperty("App::PropertyFloat", "alphaStart",
                        "config")  # .alphaStart=-18
        obj.addProperty("App::PropertyFloat", "alphaEnd", "config")
        obj.addProperty("App::PropertyFloat", "betaStart",
                        "config")  # .alphaStart=-18
        obj.addProperty("App::PropertyFloat", "betaEnd", "config")
        obj.addProperty("App::PropertyBool", "betaOff", "config")

        obj.addProperty("App::PropertyBool", "reuseAlphas")

        obj.addProperty("App::PropertyFloat", "tol", "approx").tol = 0.1
        obj.addProperty("App::PropertyBool", "closed").closed = True
        obj.addProperty("App::PropertyBool", "useStart",
                        "config").useStart = True
        obj.addProperty("App::PropertyBool", "useEnd", "config").useEnd = True
        obj.addProperty("App::PropertyEnumeration", "method", "approx")
        obj.addProperty("App::PropertyEnumeration", "tangentModel", "approx")
        obj.addProperty("App::PropertyFloatList",
                        "factorList").factorList = [100.]*20
        obj.addProperty("App::PropertyFloatList", "alphaList", "result")
        obj.addProperty("App::PropertyFloatList", "extraKnots")
        obj.addProperty("App::PropertyInteger", "start", "source").start = 0
        obj.addProperty("App::PropertyInteger", "end", "source").end = 0
        obj.addProperty("App::PropertyInteger", "Wire", "source").Wire = -1

        obj.addProperty("App::PropertyEnumeration", "mode", "approx")
        obj.mode = ['minimal Lenght', 'Length',
            'curvature', 'myMinA', 'myMinSoft']

        obj.addProperty("App::PropertyFloat", "length", "result")

        obj.addProperty("App::PropertyFloat", "_a")._a = 10
#        obj.addProperty("App::PropertyFloat","_b")._b=10
#        obj.addProperty("App::PropertyFloat","_c")._c=10
#        obj.addProperty("App::PropertyFloat","_d")._d=3

        obj.tangentModel = ['all equal', '1/3 distance', 'circle']
        # obj.tangentModel='1/3 distance'

        obj.method = ['Default',
            'simple',
            'Nelder-Mead',
            'Powell',
            'CG',
            'BFGS',
# *            'Newton-CG',
            'L-BFGS-B',
            'TNC',
            'COBYLA',
            'SLSQP',
#            'trust-constr',
# *            'dogleg',
#            'trust-ncg',
#            'trust-exact',
#            'trust-krylov',
        ]

        obj.method = 'Nelder-Mead'
        obj.method = 'simple'
        obj.closed = False
        # obj.factor=10
        obj.alphaStart = 0
        obj.alphaEnd = 0
        obj.tangentModel = '1/3 distance'
        obj._debug = True

        obj.mode = mode
        obj.method = method

        self.restored = False
        self.executed = False

    def runMinLength(self, fp, ptsa, f=0.5):

        if fp.start != 0 or fp.end != 0:
            ptsa = ptsa[fp.start:fp.end]

        if fp.closed:
            ptsa += [ptsa[0]]

        pts = ptsa
        alphas = [1]*(len(ptsa))*2
        alphasKK = [1]*(len(ptsa))*2

        for i in range(1, len(ptsa)-1):
            v = ptsa[i+1]-ptsa[i-1]
            alphas[i] = np.arctan2(v.y, v.x)

#            print i
#            print ptsa[i+1]
#            print ptsa[i-1]
#            print v
#            print (i,alphas[i]*180/np.pi)
            # alphas[i]=np.pi*0.5
            alphasKK[i] = np.arctan2(v.y, v.x)

        fp.Proxy.loops = 0
        fp.Proxy.time = time.time()

#        # diagramm
#        if 1: # in midi-bereich
#            import Plot
#            Plot.figure("directions of tangents")
#        else: # eigenes fenster
#            import Plot2 as Plot
#            Plot.figureWindow("Smooth Filter for Points")

#        t=range(len(ptsa)*2)
#        Plot.plot(t, alphas ,'points')
#        Plot.plot( t, alphas, 'filter2')
#        Plot.legend(True)
#        Plot.grid(True)

        def lengthMin(alpha, show=True):
            '''function to minimize'''

            la = len(ptsa)
            alphas = [0]*(la)*2

            if fp.betaOff:
                alphas[0:la] = alpha[0:la]
            else:
                alphas[0:2*la] = alpha[0:2*la]

            alpha = alphas

            fp.Proxy.loops += 1

            if alpha != None:

                if fp.Proxy.loops == 1:
                    if fp.useStart:
                        alpha[0] = fp.alphaStart*np.pi/18.0
                        alpha[la] = fp.betaStart*np.pi/18.0

                    if fp.useEnd:
                        alpha[la-1] = fp.alphaEnd*np.pi/18.0
                        alpha[2*la-1] = fp.betaEnd*np.pi/18.0

                if fp.closed:
                    alpha[la-1] = alpha[0]
                    alpha[2*la-1] = alpha[la]

                if fp.tangentModel == '1/3 distance':

                    pts = []
                    kk = 0.33  # 1/3 distance
                    k = fp.factorList[0]*0.01*fp.factor
                    k1 = min((ptsa[-1]-ptsa[0]).Length*kk, k)

                    for i in range(0, len(ptsa)):
                        k = fp.factorList[i]*0.01*fp.factor
                        k2 = k1
                        if i == len(ptsa)-1:
                            k1 = min((ptsa[0]-ptsa[i]).Length*kk, k)
                        else:
                            k1 = min((ptsa[i+1]-ptsa[i]).Length*kk, k)

                        if i != 0:
                            pts += [ptsa[i]-App.Vector(np.cos(alpha[la+i])*np.cos(alpha[i])*k2,
                                np.cos(alpha[la+i])*np.sin(alpha[i])*k2, np.sin(alpha[la+i])*k2)]

                        pts += [ptsa[i]]
                        if i != len(ptsa)-1:
                            pts += [ptsa[i]+App.Vector(np.cos(alpha[la+i])*np.cos(alpha[i])*k1,
                                np.cos(alpha[la+i])*np.sin(alpha[i])*k1, np.sin(alpha[la+i])*k1)]

                else:

                    pts = []
                    for i in range(0, len(ptsa)):
                        k = fp.factorList[i]*0.01*fp.factor
                        # k=30
                        if i != 0:
                            pts += [ptsa[i]-App.Vector(np.cos(alpha[la+i])*np.cos(alpha[i])*k,
                                    np.cos(alpha[la+i])*np.sin(alpha[i])*k, np.sin(alpha[la+i])*k)]
                        pts += [ptsa[i]]
                        if i != len(ptsa)-1:
                            pts += [ptsa[i]+App.Vector(np.cos(alpha[la+i])*np.cos(alpha[i])*k,
                                    np.cos(alpha[la+i])*np.sin(alpha[i])*k, np.sin(alpha[la+i])*k)]

#            print alpha
            bc = Part.BSplineCurve()
            n = la-2
            ms = [4]+[3]*n+[4]

            bc.buildFromPolesMultsKnots(pts, ms, range(len(ms)), False, 3)
            if show:
                fp.Shape = bc.toShape()
                if fp._showaux:
                    fp.Shape = Part.Compound(
                        [bc.toShape(), Part.makePolygon(pts)])
                if fp._debug:
                    Gui.updateGui()

            err = sum([abs(a+b) for a, b in zip(alphas, alphasKK)])

#            if fp.Proxy.loops %100 ==0 :
#                Plot.removeSerie(1)
#                Plot.plot(range(la*2), alpha ,'results')

            return bc.length()

        # main method

        if fp.method == 'Default':
            rc = minimize(lengthMin, alphas, tol=1.)
        elif fp.method == 'simple':
            print("simple structure - no optimize")
            _ = lengthMin(alphas)

            return
        else:
            rc = minimize(lengthMin, alphas, method=fp.method, tol=fp.tol)

        print(fp.method, rc.success, rc.message, fp.Proxy.loops)
        print("Length ", round(fp.Shape.Edge1.Length, 1))
        fp.length = fp.Shape.Edge1.Length
        fp.alphaList = list(rc.x)
        e = fp.Shape.Edge1
        bc = fp.Shape.Edge1.Curve

        size = bc.NbKnots+1
        anz = 1000
        cc = np.array([bc.curvature(size*u/anz)**2 for u in range(anz+1)])

        print("Curvature mean ", round(cc.mean()*10**6, 1))
        print("Curvature max ", round(cc.max()*10**6, 1))

        print("Radius", round(1/cc.mean(), 1),
              round(1/cc.max(), 1), round(1/cc.min(), 1))

# ----------------------------

    def runMyMinSoft_SIMPLE(self, fp, ptsa, f=0.5):

        # Tangenten
        ta = ptsa[1]-ptsa[0]
        tb = ptsa[4]-ptsa[3]
        tc = ptsa[5]-ptsa[6]
        alphas = [1., -1., 0., 1., 1.]

        fp.Proxy.loops = 0
        fp.Proxy.time = time.time()

#        # diagramm
#        if 1: # in midi-bereich
#            import Plot
#            Plot.figure("directions of tangents")
#        else: # eigenes fenster
#            import Plot2 as Plot
#            Plot.figureWindow("Smooth Filter for Points")

#        t=range(len(ptsa)*2)
#        Plot.plot(t, alphas ,'points')
#        Plot.plot( t, alphas, 'filter2')
#        Plot.legend(True)
#        Plot.grid(True)

        def minSoft(alpha, show=True):
            '''function to minimize'''

            if fp._a == 0:
                alpha[0] = 1
            if fp._a == 1:
                alpha[4] = 1
            if fp._a == 2:
                alpha[0] = 0.8
                alpha[4] = 0.8
            if fp._a == 3:
                alpha[0] = 1.
                alpha[4] = 1.

            ptsb = [ptsa[0],
                ptsa[0]+ta*alpha[0],
                ptsa[3]+tb*alpha[1],
                ptsa[3]+tb*alpha[2],
                ptsa[3]+tb*alpha[3],
                ptsa[6]+tc*alpha[4],
                ptsa[6]
            ]

            nn = 30
            fp.Proxy.loops += 1
            a = len(ptsa)
            af = Part.BSplineCurve()
            ya = [4]+[1]*3 + [4]
            af.buildFromPolesMultsKnots(ptsb, ya, range(len(ya)), False, 3)
            pp = af.discretize(nn)

            # vorgabe
            bc = Part.BSplineCurve()
            ms = [4]+[3]+[4]
            bc.buildFromPolesMultsKnots(ptsa, ms, range(len(ms)), False, 3)
            pp2 = bc.discretize(nn)

            dd = sum([(p-p2).Length**2 for p, p2 in zip(pp, pp2)])
            fp.Shape = af.toShape()

            if fp.Proxy.loops % 20 == 0: Gui.updateGui()
#            print ("ergebnis", dd,fp.Proxy.loops)
            return dd

        # main method

        rc = minimize(minSoft, alphas, method=fp.method, tol=fp.tol)
        print(fp.method, rc.success, rc.message, fp.Proxy.loops)
        print(rc.fun)
        fp.alphaList = list(rc.x)

    def runMyMinSoft(self, fp, ptsa, f=0.5):

        # Tangenten
        # print ("ptsa",ptsa
        zz = (len(ptsa)-4)/3
        # assert(zz==2)
        tangs = [ptsa[1]-ptsa[0]]
        for z in range(zz):
            tangs += [ptsa[3*z+2]-ptsa[3*z+3]]
        tangs += [ptsa[-2]-ptsa[-1]]
        alphas = [1.]
        for z in range(zz):
            alphas += [1, 0, -1]
        alphas += [1.]

        fp.Proxy.loops = 0
        fp.Proxy.time = time.time()

#        # diagramm
#        if 1: # in midi-bereich
#            import Plot
#            Plot.figure("directions of tangents")
#        else: # eigenes fenster
#            import Plot2 as Plot
#            Plot.figureWindow("Smooth Filter for Points")

#        t=range(len(ptsa)*2)
#        Plot.plot(t, alphas ,'points')
#        Plot.plot( t, alphas, 'filter2')
#        Plot.legend(True)
#        Plot.grid(True)

        def minSoft(alpha, show=True):
            '''function to minimize'''

            ptsb = [ptsa[0],
                ptsa[0]+tangs[0]*alpha[0],
                ]
            for z in range(zz):
                ptsb += [
                ptsa[3*z+3]+tangs[z+1]*alpha[3*z+1],
                ptsa[3*z+3]+tangs[z+1]*alpha[3*z+2],
                ptsa[3*z+3]+tangs[z+1]*alpha[3*z+3],
                ]

            ptsb += [
                ptsa[-1]+tangs[-1]*alpha[-1],
                ptsa[-1]
            ]

            nn = 30
            fp.Proxy.loops += 1
            a = len(ptsa)
            af = Part.BSplineCurve()
            ya = [4]+[1]*3*zz + [4]
            af.buildFromPolesMultsKnots(ptsb, ya, range(len(ya)), False, 3)
            pp = af.discretize(nn)

            # vorgabe
            # print ("MyMin Soft",zz)
            bc = Part.BSplineCurve()
            ms = [4]+[3]*zz+[4]
            bc.buildFromPolesMultsKnots(ptsa, ms, range(len(ms)), False, 3)
            pp2 = bc.discretize(nn)

            dd = sum([(p-p2).Length**2 for p, p2 in zip(pp, pp2)])
            fp.Shape = af.toShape()

#            kk=1000
#            dd2=0
#            for z in range(zz):
#                dd += (bc.value(bc.parameter(ptsa[3*z]))-ptsa[3*z]).Length**2*kk
#                dd2 += (bc.value(bc.parameter(ptsa[3*z]))-ptsa[3*z]).Length**2*kk

            if fp.Proxy.loops % 20 == 0:
                Gui.updateGui()
#                print ("ergebnis", dd2,fp.Proxy.loops)
            return (dd/nn)**0.5

        # main method

        rc = minimize(minSoft, alphas, method=fp.method, tol=fp.tol)
        print(fp.method, rc.success, rc.message, fp.Proxy.loops)
        print(rc.fun)
        fp.alphaList = list(rc.x)
        minSoft(rc.x)


# --------ende run min soft----------------------


    def addExtraKnots(self, fp):

        xtras = []
        bc = fp.Shape.Edge1.Curve
        for i in fp.extraKnots:
                print("extra knot ", i)
                bc.insertKnot(i, 3)
                pt = bc.value(i)
                xtras += [Part.makeSphere(1, pt)]

        af = Part.BSplineCurve()
        poles = bc.getPoles()
        ya = bc.getMultiplicities()
        af.buildFromPolesMultsKnots(poles, ya, range(len(ya)), False, 3)
        fp.Shape = Part.Compound([af.toShape()]+xtras)

    def onChanged(self, fp, prop):

        try: self.restored
        except: return
        if fp._noExecute: return
        oldpm = fp.Placement

        if prop in ["factor", 'method', 'alphaStart', 'alphaEnd', 'betaEnd', 'betaStart', 'factorList', 'tangentModel'] or prop.startswith('_'):

            if fp.Shape == None or fp.path == None:
                return
            try:
                pts = fp.path.Points
            except:
                pts = [v.Point for v in fp.path.Shape.Vertexes]

            # wenn Kurve, dann nehme Poles
            try:  # wenn es eine kurve ist
                pts = fp.path.Shape.Edge1.Curve.getPoles()
            except:
                pass

            if fp.Wire > -1:
                pts = [v.Point for v in fp.path.Shape.Wires[fp.Wire].Vertexes]

            if fp.factor == 0:
                try:
                    fp.factor = fp.path.Shape.BoundBox.DiagonalLength / \
                        len(pts)/4
                except:
                    fp.factor = 100

            if fp.mode == 'myMinA':
                runMyMinA(fp, pts)
            elif fp.mode == 'myMinSoft':
                if prop == "factor":
                    return
                else:
                    self.runMyMinSoft(fp, pts)
            else:
                self.runMinLength(fp, pts, fp.factor)

            self.addExtraKnots(fp)
            self.executed = True
            fp.Placement = oldpm

    def execute(self, fp):
        try:
            if self.executed:
                self.executed = False
                return
        except:
            pass
        if fp._noExecute: return
        self.onChanged(fp, 'method')
        self.executed = False


class Nurbs_minimumLengthBezier:
    def Activated(self):
        self._minimumLengthBezier()
    def _minimumLengthBezierGUI(self):
        ''' optimale kurve mit zwei Segmenten durch einen Punkt finden'''

        for s in Gui.Selection.getSelection():
            yy = App.ActiveDocument.addObject(
                "Part::FeaturePython", "MinLenBezier")
            MinLengthBezier(yy, mode='minimal Lenght')
            ViewProvider(yy.ViewObject)

            yy.path = s
            # yy._noExecute=True
            yy._debug = False
            yy.alphaStart = 15
            yy.alphaEnd = 14
            yy.factor = 50

            yy.ViewObject.LineColor = (.3, 1., 0.0)
            yy.ViewObject.ShapeColor = (1., 0., 0.)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_minimumLengthBezier")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_minimumLengthBezier"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_minimumLengthBezier", Nurbs_minimumLengthBezier())



class Nurbs_CreateMyMinAGUI:
    def Activated(self):
        self._createMyMinAGUI()
    def _createMyMinAGUI(self):
        ''' myMinA-Object erzeugen'''

        ss = Gui.Selection.getSelection()
        if len(ss) == 0:
            s = App.ActiveDocument.addObject(
                'Sketcher::SketchObject', 'Sketch_forMyMinA')
            s.addGeometry(Part.LineSegment(
                App.Vector(-20, 0, 0), App.Vector(-10, 10, 0)), False)
            s.addGeometry(Part.LineSegment(
                App.Vector(-10, 10, 0), App.Vector(10, 10, 0)), False)
            s.addConstraint(Sketcher.Constraint('Coincident', 0, 2, 1, 1))
            s.addGeometry(Part.LineSegment(App.Vector(
                10, 10, 0), App.Vector(20, -10, 0)), False)
            s.addConstraint(Sketcher.Constraint('Coincident', 1, 2, 2, 1))
            App.ActiveDocument.recompute()
            ss = [s]

        for s in ss:
            yy = App.ActiveDocument.addObject("Part::FeaturePython", "MyMinA")
            MinLengthBezier(yy, mode='myMinA', method='Nelder-Mead')
            ViewProvider(yy.ViewObject)
            yy.path = s
            yy.ViewObject.LineColor = (.3, 1., 0.0)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_CreateMyMinAGUI")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_CreateMyMinAGUI"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_CreateMyMinAGUI", Nurbs_CreateMyMinAGUI())


class Nurbs_createMyMinSoftGUI:
    def Activated(self):
        self._createMyMinSoftGUI()
    def _createMyMinSoftGUI(self):
        ''' myMinSoft-Object erzeugen'''

        for s in Gui.Selection.getSelection():
            yy = App.ActiveDocument.addObject("Part::FeaturePython", "MyMinSoft")
            MinLengthBezier(yy, mode='myMinSoft', method='Nelder-Mead')
            ViewProvider(yy.ViewObject)
            yy.path = s
            yy.ViewObject.LineColor = (.3, 1., 0.0)

        '''
        if 1:
            pts=[App.Vector(0,0,0),
                    App.Vector(300,0,0),
                    App.Vector(500,200,300),
                    App.Vector(500,400,500),
                    App.Vector(500,400,800),
                    ]
            import Draft
            Draft.makeWire(pts)
        '''

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_createMyMinSoftGUI")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_createMyMinSoftGUI"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_createMyMinSoftGUI", Nurbs_createMyMinSoftGUI())



class ConstantCurvatureBezier(FeaturePython):

    def __init__(self, obj):
        FeaturePython.__init__(self, obj)
        obj.addProperty("App::PropertyLink", "path")
#        obj.addProperty("App::PropertyInteger","factor").factor=30
#        obj.addProperty("App::PropertyFloat","alphaStart").alphaStart=-18
#        obj.addProperty("App::PropertyFloat","alphaEnd")
        obj.addProperty("App::PropertyFloat", "tol").tol = 0.1
#        obj.addProperty("App::PropertyBool","closed").closed=True
#        obj.addProperty("App::PropertyBool","useStart").useStart=True
#        obj.addProperty("App::PropertyBool","useEnd").useEnd=True
        obj.addProperty("App::PropertyEnumeration", "method")
#        obj.addProperty("App::PropertyEnumeration","tangentModel")
#        obj.addProperty("App::PropertyFloatList","factorList").factorList=[100.]*20
        obj.addProperty("App::PropertyFloatList", "alphaList", "~calculated")
        obj.addProperty("App::PropertyInteger", "start").start = 0
        obj.addProperty("App::PropertyInteger", "end").end = 0

#        obj.addProperty("App::PropertyEnumeration","mode")
#        obj.mode=['minimal Lenght','Length','curvature']
        obj.addProperty("App::PropertyFloat", "length", "~calculated")

#        obj.addProperty("App::PropertyFloat","_a")._a=10
#        obj.addProperty("App::PropertyFloat","_b")._b=10
#        obj.addProperty("App::PropertyFloat","_c")._c=10
#        obj.addProperty("App::PropertyFloat","_d")._d=3

#        obj.addProperty("App::PropertyInteger","segment")segment=0
#        obj.tangentModel=['all equal','1/3 distance','circle']
        # obj.tangentModel='1/3 distance'
        obj.method = ['Default',
            'Nelder-Mead',
            'Powell',
            'CG',
            'BFGS',
# *            'Newton-CG',
            'L-BFGS-B',
            'TNC',
            'COBYLA',
            'SLSQP',
#            'trust-constr',
# *            'dogleg',
#            'trust-ncg',
#            'trust-exact',
#            'trust-krylov',
        ]
        obj.method = 'Nelder-Mead'
        obj._debug = True
        self.restored = False

    def runMinCurv(self, fp, ptsv):

        ptsa = ptsv
        fp.Proxy.loops = 0
        fp.Proxy.time = time.time()

        def curvatureMinMax(alpha, show=True):

            a = alpha[0]
            b = alpha[1]
            pts = [ptsa[0],
                    ptsa[0]+(ptsa[1]-ptsa[0]).normalize()*(0.0001+abs(a)),
                    ptsa[3]+(ptsa[2]-ptsa[3]).normalize()*(0.0001+abs(b)),
                    ptsa[3]
                ]
            fp.Proxy.loops += 1

            bc = Part.BSplineCurve()
            ms = [4]+[4]

            bc.buildFromPolesMultsKnots(pts, ms, range(len(ms)), False, 3)
            if show:
                fp.Shape = bc.toShape()

            if fp._debug:
                Gui.updateGui()

            size = 1.0
            anz = 1000
            cc2 = np.array([bc.curvature(size*u/anz) for u in range(anz+1)])
            fp.Proxy.cc2 = cc2

            fp.alphaList = list(alpha)
#            print ("!"
#            print (cc2.max(),cc2.min())
#            print (abs(cc2.max()-cc2.min()),cc2.mean())
#            print bc.length()
#
#
#
#            rc=abs(cc2.max()-cc2.min())*(1+cc2.mean())**np.pi#*bc.length()
#            print (rc)

            rc = abs(cc2.max()-cc2.min())*(1+cc2.mean())**np.pi*bc.length()

#            print (rc)
#            if fp.Proxy.loops>3000:
#                print ("loops ende"
#                return 0

            return rc * 10**4

        # main method

        alphas = [0, 0]
        if fp.method == 'Default':
            rc = minimize(curvatureMinMax, alphas, tol=fp.tol)
        else:
            rc = minimize(curvatureMinMax, alphas,
                          method=fp.method, tol=fp.tol)

        print(fp.method, fp.Proxy.loops, rc.success, rc.message)
        print(fp.Proxy.cc2.max(), fp.Proxy.cc2.min())

        curvatureMinMax(fp.alphaList)
        return fp.Shape

    def onChanged(self, fp, prop):
        try: self.restored
        except: return
        if fp._noExecute: return
        oldpm = fp.Placement

        if prop in ["_execute", "factor", 'method', 'alphaStart', 'alphaEnd', 'factorList', 'tangentModel', 'segment'] or prop.startswith('_'):
            if fp.Shape == None or fp.path == None:
                return

            try:  # Draft Wire oder Draft BSpline
                pts = fp.path.Points
            except:
                pts = [v.Point for v in fp.path.Shape.Vertexes]

            try:  # wenn es eine kurve ist
                pts = fp.path.Shape.Edge1.Curve.getPoles()
            except:
                pass

            if fp.start != 0 or fp.end != 0:
                pts = pts[3*fp.start:3*fp.end+1]

            ll = len(pts)/3
            shapes = []
            lenn = 0.0
            for li in range(ll):
                ptsa = pts[li*3:li*3+4]
                rc = self.runMinCurv(fp, ptsa)
                print("runArc", li, rc)
                shapes += [rc]
                lenn += rc.Length

            poles = []
            for i, s in enumerate(shapes):
                if i == 0:
                    poles = s.Edge1.Curve.getPoles()
                else:
                    poles += s.Edge1.Curve.getPoles()[1:4]

#            fp.Shape=Part.makePolygon(poles)

            abc = Part.BSplineCurve()
            ms = [4]+[3]*i+[4]

            abc.buildFromPolesMultsKnots(poles, ms, range(len(ms)), False, 3)
            fp.Shape = abc.toShape()
            fp.Placement = oldpm

            fp.length = lenn

    def execute(self, fp):
        try:
            if self.executed:
                self.executed = False
                return
        except:
            pass

        if fp._noExecute: return
        self.onChanged(fp, "_execute")

class Nurbs_nearconstantCurvatureBezier:
    def Activated(self):
        self._nearconstantCurvatureBezier()
    def _nearconstantCurvatureBezierGUI(self):
        ''' optimale kurve mit minimaler kruemmungs aenderung'''

        for s in Gui.Selection.getSelection():
            yy = App.ActiveDocument.addObject(
                "Part::FeaturePython", "nearConstantCurvatureBezier")
            ConstantCurvatureBezier(yy)
            ViewProvider(yy.ViewObject)
            yy
        #    yy.start=3
        #    yy.end=4
            yy._debug = False
            yy.path = s
            yy.ViewObject.LineColor = (1.0, 0.3, 1.0)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_nearconstantCurvatureBezier")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_nearconstantCurvatureBezier"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_nearconstantCurvatureBezier", Nurbs_nearconstantCurvatureBezier())





def deactivateExecution():
    ''' the execute method for the selection is deactivated'''
    for s in Gui.Selection.getSelection():
        try:
            s._noExecute = True
        except:
            pass


def activateExecution():
    ''' the execute method for the selection is activated'''
    for s in Gui.Selection.getSelection():
        try:
            s._noExecute = False
        except:
            pass

# ------------------


def myMinA(pts):
    '''meine midimal-Methdoe A'''
#    a=App.Vector(0,0,0)
#    b=App.Vector(50,100,0)
#    c=App.Vector(200,0,0)

    [a, b, c] = pts
    # Part.show(Part.makePolygon([a,b,c]))

    ptr = []
    n = 10
    ta = range(0, n+1)
    tb = range(0, n+1)
    for ia in ta:
        for ib in tb:
            iar = 1.0*ia/(n+1)
            ibr = 1.0*ib/(n+1)
            a1 = a*iar+b*(1-iar)
            b1 = c*ibr+b*(1-ibr)
            pts = [a, a1, b1, c]
            cu = Part.BSplineCurve()
            cu.buildFromPolesMultsKnots(pts, [4, 4], [0, 1], False, 3)
            # print cu.length()
            s = []
            for i in range(n+1):
                s += [cu.curvature(1.0*i/(n+1))]
            ss = (np.max(s)-np.min(s))/np.mean(s)**1.0
            ptr += [App.Vector(iar, ibr, ss)]

    # Points.show(Points.Points(ptr))

    ptra = np.array(ptr)
    mm = np.min(ptra[:, 2])
    mins = np.where(ptra[:, 2] <= mm + 0.0)
#    print mins

    # for (ix,iy) in zip(mins[0],mins[1]):
    #    if iy==2:
    #        print (ix,iy,ptra[ix])

#    for ix in mins[0]:
#            print (ix,ptra[ix])

    ix = mins[0][0]

    iar, ibr, _ = ptra[ix]
#    print ("!",iar,ibr)
    a1 = a*iar+b*(1-iar)
    b1 = c*ibr+b*(1-ibr)
    pts = [a, a1, b1, c]
    cu = Part.BSplineCurve()
    cu.buildFromPolesMultsKnots(pts, [4, 4], [0, 1], False, 3)
    # Part.show(cu.toShape())

    return pts


def runMyMinA(fp, pts):


#    for s in Gui.Selection.getSelection():
#        pts=[v.Point for v in s.Shape.Wires[0].Vertexes]
        s = fp

        if fp.start != 0 or fp.end != 0:
            pts = pts[fp.start:fp.end]

        if fp.closed:
            pts += [pts[0]]

        label = s.Label+"_curve"

        debug = 0

        def schnittpunkt(pts):

            a = np.array(((pts[0].x-pts[1].x, pts[3].x-pts[2].x),
                                (pts[0].y-pts[1].y, pts[3].y-pts[2].y)))

            b = np.array((pts[3].x-pts[1].x, pts[3].y-pts[1].y))
            t, s = np.linalg.solve(a, b)
        #    print pts
        #    print (t,s)
        #    print pts[0]*t+pts[1]*(1-t)
        #    print pts[2]*s+pts[3]*(1-s)
            return pts[0]*t+pts[1]*(1-t)

        def makeSimpleCurve(pts):

            print("makeSimpleCurve")
#            print pts

            pr = []
            # print  (len(pts)
            if len(pts) <= 3:
                pr = pts
                # Draft.makeWire(pr)
                return []
            for i in range(len(pts)-3):
        #        print i
                try:
                    sp = schnittpunkt([pts[i+1], pts[i+1]+pts[i]-pts[i+2],
                                    pts[i+2], pts[i+2]+pts[i+3]-pts[i+1]])
                except:
                    print("Problem Schnittpuinkt", i)
                    for pui in [pts[i+1], pts[i+1]+pts[i]-pts[i+2], pts[i+2], pts[i+2]+pts[i+3]-pts[i+1]]:
                        print(pui)
                    sp = pts[i+1]
                k = 0.9
                k = 0.5
                pr += myMinA([pts[i+1], sp, pts[i+2]])[0:3]
    #            pr += pts[i+1],k*sp+(1-k)*pts[i+1],k*sp+(1-k)*pts[i+2]

            pr += [pts[i+2]]

            a = len(pr)
            af = Part.BSplineCurve()
            ya = [4]+[3]*((a-4)/3)+[4]
            af.buildFromPolesMultsKnots(pr, ya, range(len(ya)), False, 3)
            if debug:
                Part.show(af.toShape())
            # Draft.makeWire(pr)
            return pr

        def makeLineCurve(pts, mode='', fp=None):

#            print ("Make Line",mode)
#            print pts

            ff = 0.2
            if mode == 'start':
                k = (pts[1]-pts[0]).Length * ff
                pr = [pts[0], pts[0]+(pts[1]-pts[0]).normalize()*k,
                                    pts[1]+(pts[0]-pts[2]).normalize()*k, pts[1]]

                # tangente fix

                if fp.useStart:
                    ast = fp.alphaStart*np.pi/18.0
                    bs = fp.betaStart*np.pi/18.0
                    tg = -App.Vector(np.cos(bs)*np.cos(ast),
                                   np.cos(bs)*np.sin(ast), np.sin(bs))
                    pr = [pts[0], pts[0]+tg*k, pts[1] +
                        (pts[0]-pts[2]).normalize()*k, pts[1]]

                if fp.useEnd:
                    ae = fp.alphaEnd*np.pi/18.0
                    be = fp.betaEnd*np.pi/18.0

            elif mode == 'end':
                k = (pts[1]-pts[2]).Length * ff
                pr = [pts[1], pts[1]+(pts[2]-pts[0]).normalize()*k, pts[2]+(pts[1]-pts[2]).normalize()*k,
                pts[2]]

                if fp.useEnd:
                    ast = fp.alphaEnd*np.pi/18.0
                    bs = fp.betaEnd*np.pi/18.0
                    tg = App.Vector(np.cos(bs)*np.cos(ast),
                                  np.cos(bs)*np.sin(ast), np.sin(bs))
                    pr = [pts[1], pts[1]+(pts[2]-pts[0]).normalize()
                                        * k, pts[2]+tg*k, pts[2]]

            else:
                k = (pts[2]-pts[1]).Length * ff
                pr = [pts[1], pts[1]+(pts[2]-pts[0]).normalize()*k,
                                    pts[2]+(pts[1]-pts[3]).normalize()*k, pts[2]]

            a = len(pr)
            af = Part.BSplineCurve()
            ya = [4]+[3]*((a-4)/3)+[4]
            af.buildFromPolesMultsKnots(pr, ya, range(len(ya)), False, 3)
            if debug:
                Part.show(af.toShape())
            return pr

        print("Loop---------------------------")
        ll = len(pts)
        if ll < 3:
            print("brauche wenigstens 3 punkte")
            print("cancellation")
            return

        j = 0
        d = pts[j+1]-pts[j]
        direct = np.arctan2(d.x, d.y)
        d2 = pts[j+2]-pts[j+1]
        direct2 = np.arctan2(d2.x, d2.y)

        start = -1 if direct-direct2 > 0 else 1
        anfang = 0

        pr = []
        rc = makeLineCurve(pts[0:3], mode='start', fp=fp)
        pr += rc

        j = 1
        while j < ll-2:
            d = pts[j+1]-pts[j]
            direct = np.arctan2(d.x, d.y)
            d2 = pts[j+2]-pts[j+1]
            direct2 = np.arctan2(d2.x, d2.y)
            dd = direct-direct2
#            print ("Richtung Punkt           ",pts[j+1])
#            print ("start ",start
            if direct > 0:
                if direct2 < direct and direct2 > direct-np.pi:
                    dd = -1
#                    print ("A",j,direct,direct2,dd)
                else:
                    dd = 1
#                    print ("B",j,direct,direct2,dd)
            else:
                if (direct2 > direct and direct2 < np.pi+direct):
                    dd = 1
#                    print ("C",j,direct,direct2,dd)
                else:
                    dd = -1
#                    print ("D",j,direct,direct2,dd)

            if dd*start < 0:
                print("Ende", j)
                start = dd
                rc = makeSimpleCurve(pts[anfang:j+2])
                pr += rc[1:]
                anfang = j
                rc = makeLineCurve(pts[j-1:j+3])
                pr += rc[1:]
            else:
                j += 1
                # start=direct

        rc = makeSimpleCurve(pts[anfang:j+2])
        pr += rc[1:]
        rc = makeLineCurve(pts[-3:], mode='end', fp=fp)
        pr += rc[1:]

        a = len(pr)
        af = Part.BSplineCurve()
        ya = [4]+[3]*((a-4)/3)+[4]
        af.buildFromPolesMultsKnots(pr, ya, range(len(ya)), False, 3)
        fp.Shape = af.toShape()
        # App.ActiveDocument.ActiveObject.Label=label


class PolesFrame(FeaturePython):

    def __init__(self, obj):
        FeaturePython.__init__(self, obj)
        obj.addProperty("App::PropertyLinkList", "ribs")
        obj.ribs = []

    def onChanged(self, fp, prop):

        if prop != 'ribs': return
#        try: self.restored
#        except: return

#        try: fp.Shape
#        except: return
        fp.Shape = Part.Shape()

        if fp._noExecute: return

        ss = fp.ribs

        ptsa = []
        lmin = 10**3

        for rc, s in enumerate(ss):

            pols = s.Shape.Edge1.Curve.getPoles()
            lmin = min(len(pols), lmin)
            print("Rippe", rc, s.Label, len(pols))
            ptsa += [pols]

        cols = []
        for i in range(lmin):
            if i % 3 == 0:
                pts = []
                for pols in ptsa:
                    pts += [pols[i]]
                cols += [Part.makePolygon(pts)]

        fp.Shape = Part.Compound(cols)

    def execute(self, obj):
        print("execute")
        self.onChanged(obj, "ribs")
        pass

class Nurbs_createBezierPolesFramefromribsGUI:
    #_createBezierPolesFramefromribsGUI
    def Activated(self):
        '''create a poles grid for a list of bezier curves'''
        yy = App.ActiveDocument.addObject("Part::FeaturePython", "PolesFrame")
        ViewProvider(yy.ViewObject)
        PolesFrame(yy)
        yy.ribs = Gui.Selection.getSelection()

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_createBezierPolesFramefromribsGUI")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_createBezierPolesFramefromribsGUI"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_createBezierPolesFramefromribsGUI", Nurbs_createBezierPolesFramefromribsGUI())


# ---------------------

def swapCurves(sel=None, mode='polygons', extraknots=None):
    ''' polefeld in andrere richtung aufziehen'''

    if sel == None:
        sel = Gui.Selection.getSelection()
    polar = []
    xtras = []
    print("Control points ...")
    eps = 0
    for isx, s in enumerate(sel):
        if extraknots == None:
            pols = s.Shape.Edge1.Curve.getPoles()
            xtras += [s.Shape.Edge1]
        else:
            cc = s.Shape.Edge1.Curve
            xtras += [s.Shape.Edge1]
            for i in extraknots[isx]:
#                print ("!extra knot ",i
                cc.insertKnot(i, 3)
                pt = cc.value(i)
                xtras += [Part.makeSphere(1, pt)]
            pols = cc.getPoles()

        print(isx, str(s.Label), (len(pols)-4)/3+2,
              (len(pols)-4)/3+2-len(extraknots[isx]))
        polar += [pols]

    polar = np.array(polar).swapaxes(0, 1)
    if mode == 'polar':
        return polar, xtras
    for pts in polar:
        ptsa = [App.Vector(p[0], p[1], p[2]) for p in pts]
        Part.show(Part.makePolygon(ptsa))


def curvestoFace(polsarr=None, mode="Bezier Face"):
    '''flaeche aus polefeld selbst berechenn'''

    if polsarr == None:
        polsarr = []
        cc = Gui.Selection.getSelection()[0]
        try:
            for l in cc.Links:
                pols = l.Shape.Edge1.Curve.getPoles()
                polsarr += [pols]
        except:
            for l in Gui.Selection.getSelection():
                pols = l.Shape.Edge1.Curve.getPoles()
                polsarr += [pols]

    poles = np.array(polsarr)
    print("curves to shape ", poles.shape)
    try:
        b, a, _ = poles.shape
    except:
        print("Probleme mit Punktematrix- Segemente nicht leich lang -- cancellation")
        return
    print("huhuhu")
#    a,b=b,a
    af = Part.BSplineSurface()

    # bezier
    if mode == "Bezier Face" or mode == "Both":
        ya = [4]+[3]*((a-4)/3)+[4]
        yb = [4]+[3]*((b-4)/3)+[4]
    else:
        ya = [4]+[1]*((a-4))+[4]
        yb = [4]+[1]*((b-4))+[4]

    db = 3
#    print (a,ya)
#    print (b,yb)
    af.buildFromPolesMultsKnots(poles,
                yb, ya,
                range(len(yb)), range(len(ya)),
                False, False, db, 3)
    # Part.show(af.toShape())
    print(af)
    return af


def A():
    berings
    #reload(berings)
    rc = berings.createBering()
    for obj in rc:
        obj.stripmode = True

class Nurbs_DontKnowWhatThisDo_B:
    def Activated(self):
        self.B()
    def B(self):
        for l in Gui.Selection.getSelection():
        #    pols=l.Shape.Edge1.Curve.getPoles()
            pols = [v.Point for v in l.Shape.Wires[0].Vertexes]

            polsn = [pols[0]]
            kf = 30
            for i, p in enumerate(pols[1:-1]):
                t = (pols[i+2]-pols[i]).normalize()*kf
                if i == 0:
                    polsn += [p-t]
                polsn += [p-t, p, p+t]

            polsn += [p+t, pols[-1]]
    #        Part.show(Part.makePolygon(polsn))
    #        print polsn

            bc = Part.BSplineCurve()
            n = (len(polsn)-4)/3
            ms = [4]+[3]*n+[4]

            bc.buildFromPolesMultsKnots(polsn, ms, range(len(ms)), False, 3)
            Part.show(bc.toShape())

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_DontKnowWhatThisDo_B")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_DontKnowWhatThisDo_B"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_DontKnowWhatThisDo_B", Nurbs_DontKnowWhatThisDo_B())



#
# wenn knoten fehlen, wo sollen sie hinkommen
# experimentell #+#
#

def extraKnots():
    ''' zurodnung extra knoten '''

    # -----zuordnung
    i1 = [0, 1, 2, 4, 5]
    i2 = [0, 1, 2, 3, 4]
    # ---------

    c1 = App.ActiveDocument.MyMinA.Shape.Edge1.Curve
    k1sa = np.array(c1.getKnots())
    l1sa = np.array([c1.length(0, k) for k in k1s])
    k1m = k1sa.max()
    k1s = k1sa / k1m
    l1s = l1sa/l1sa.max()

    c2 = App.ActiveDocument.MyMinA001.Shape.Edge1.Curve
    k2sa = np.array(c2.getKnots())
    l2sa = np.array([c2.length(0, k) for k in k2s])
    k2m = k2sa.max()
    k2s = k2sa/k2m
    l2s = l2sa/l2sa.max()

    if 0:
        if 0:  # in midi-bereich
            import Plot
            Plot.figure("Smooth Filter for Points")
        else:  # eigenes fenster
            import Plot2 as Plot
            Plot.figureWindow("Smooth Filter for Points")

        Plot.plot(k1s, l1s, 'A')
        Plot.plot(k2s, l2s, 'B')
        # Plot.plot( t, y, 'filter')
        Plot.legend(True)
        Plot.grid(True)
        diagram = True

    x1 = [l1s[i] for i in i1]
    x2 = [l2s[i] for i in i2]

    rc1 = np.interp(l1s, x1, x2)
    rck1 = np.interp(rc1, l2s, k2s)

    # Knoten auf kurve 2
    kkk = rck1*k2m

    for k in kkk:
        if k not in k2sa:
            print (k)


class Ribface(FeaturePython):

    def __init__(self, obj):
        FeaturePython.__init__(self, obj)
        obj.addProperty("App::PropertyLinkList", "ribs")
        obj.addProperty("App::PropertyStringList", "extraKnots")
        obj.extraKnots = ["1.2 1.6 1.8", "1.5 2.5",
            "1.4 1.8", "1.4 1.8", "", "", "", ""]
        obj.addProperty("App::PropertyEnumeration", "shapeMode").shapeMode = [
                        "PolesFrame", "Bezier Face", "BSpline", "Both"]
        obj.addProperty("App::PropertyFloat", "factor").factor = 10

    def execute(self, obj):
        ss = obj.ribs
        extraknots = []
        for kk in obj.extraKnots:
            extraknots += [[float(k) for k in kk.split()]]

        if len(ss) > len(extraknots):
            extraknots += []*(len(ss)-len(extraknots))

        # print ("extraknots", extraknots)
        
        # swap
        polars, xtras = swapCurves(ss, mode='polar', extraknots=extraknots)
    #    print pols
    #    print pols[0][0]
    #    print App.Vector(pols[0][0])
        polesarrN = []
        for polsA in polars:
        #    for pts in polar:
        #        ptsa=[App.Vector(p[0],p[1],p[2])  for p in pts]
            pols = [App.Vector(p) for p in polsA]

            polsn = [pols[0]]
            kf = obj.factor
            for i, p in enumerate(pols[1:-1]):
                l1 = (pols[i+1]-pols[i]).Length
                l2 = (pols[i+1]-pols[i+2]).Length
                t = (pols[i+2]-pols[i]).normalize()*kf
                t1 = (pols[i+2]-pols[i]).normalize()*kf*0.01*l1
                t2 = (pols[i+2]-pols[i]).normalize()*kf*0.01*l2
                if i == 0:
                    polsn += [p-t1]
                polsn += [p-t1, p, p+t2]

            polsn += [p+t, pols[-1]]

            bc = Part.BSplineCurve()
            n = (len(polsn)-4)/3
            ms = [4]+[3]*n+[4]
            bc.buildFromPolesMultsKnots(polsn, ms, range(len(ms)), False, 3)
        #    Part.show(bc.toShape())

            polesarrN += [polsn]

        af = curvestoFace(polsarr=polesarrN, mode=obj.shapeMode)
        obj.Shape = af.toShape()

        if obj.shapeMode == "Both":
            cols = [af.toShape()]
        else:
            cols = []

        cols += xtras
        for i, pts in enumerate(polesarrN):
            if i % 3 == 0:
                cols += [Part.makePolygon(pts)]

        if obj.shapeMode == "PolesFrame" or obj.shapeMode == "Both":
            obj.Shape = Part.Compound(cols)

class Nurbs_RibstoFace:
    def Activated(self):
        self.RibstoFace()
    def RibstoFace(self):
        ''' swap, umformen in bezier,m flaeche machen'''

        yy = App.ActiveDocument.addObject("Part::FeaturePython", "RibFace")
        Ribface(yy)
        yy.ribs = Gui.Selection.getSelection()
        ViewProvider(yy.ViewObject)
        yy.ViewObject.ShapeColor = (.6, .6, 1.)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_RibstoFace")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_RibstoFace"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_RibstoFace", Nurbs_RibstoFace())



#
#  tools fuer verfeinern von flaechen ...
#

def findrib():
    # finde punkt auf kurve mit gegebenem x und mache dorhin einen pol
    a = App.ActiveDocument.BeringSketch.Shape.Edge1.Curve

    x = 3
    v = App.Vector(x, 0)

    for i in range(50):
        m = a.parameter(v)
        pp = a.value(m)
        v = App.Vector(x, pp.y)
        print(i, v, (pp-v).Length)
        if (pp-v).Length < 0.001:
            break

    a.insertKnot(m, 3)
    Part.show(Part.Point(pp).toShape())
    Part.show(a.toShape())


#################################################################
def usage(msg=""):
    if msg != "": msg = "\n"+msg+"\n"
    errorDialog("Fehler in " + inspect.stack()[1][1].split('/')[-1]+" line:"+str(inspect.stack()[1][2]) +
        "\n"+eval(inspect.stack()[1][3]+".__doc__") + msg)
    App.Console.PrintError("Error"+str(inspect.stack()[1][1:4])+msg)
#################################################################


def AA():
    '''Erzeuge zu drei hart kodierten Laengen und Winkeln
eine Abwicklung. Idee ist eine Flaeche zu erzeugen, die
man auf eine Freiformfläche aufkleben ann.
    '''

    doc = App.newDocument("Unnamed")
    App.ActiveDocument = doc
    Gui.ActiveDocument = doc
#    try: App.ActiveDocument.Cone
#    except:
#        usage("geht nur, wenn ein Kegel da ist")

    grp = App.ActiveDocument.addObject("App::DocumentObjectGroup", "Defaut")
    oba = App.ActiveDocument.addObject("Part::Feature", "A")
    obb = App.ActiveDocument.addObject("Part::Feature", "B")
    obc = App.ActiveDocument.addObject("Part::Feature", "C")

    VX = App.Vector(1, 0, 0)
    VZ = App.Vector(0, 0, 1)

    if 0:
        lens = App.lens
        arcs = App.arcs
    else:
        print("verwende fest kodierte werte")
        arcs = [90, 90, 90]
        lens = [100., 100., 100.]

    arcs = [arcs[2], arcs[1], arcs[0]]

    [a, c, b] = lens
    jj = (-c**2+a**2+b**2)/(2*a*b)
    alpha = np.arccos(jj)
    y = b*np.sin(alpha)
    x = b*np.cos(alpha)
    pts = [App.Vector(), App.Vector(lens[0], 0), App.Vector(x, y)]
    Draft.makeWire(pts, closed=True)

    tts = [170, -40, pts[1].x, pts[1].y]
    tts = [170, -40, pts[1].x, pts[1].y, pts[2].x, pts[2].y]

    def minFun(tts):
            tf = 100
            tf = min(lens)/3

            minf = 0

            p0 = pts[0]
            p1 = p0+VX*tf
            p3 = App.Vector(tts[2], tts[3])
            p2 = p3+App.Rotation(VZ, tts[0]).multVec(VX)*tf
            bc = Part.BSplineCurve()
            bc.buildFromPolesMultsKnots(
                [p0, p1, p2, p3], [4, 4], [0, 1], False, 3)
            minf += (bc.length()-lens[0])**2
            oba.Shape = bc.toShape()

            p4 = p3+App.Rotation(VZ, tts[0]-arcs[0]).multVec(VX)*tf
            p6 = App.Vector(tts[4], tts[5])
            p5 = p6+App.Rotation(VZ, tts[1]).multVec(VX)*tf
            bc.buildFromPolesMultsKnots(
                [p3, p4, p5, p6], [4, 4], [0, 1], False, 3)
            minf += (bc.length()-lens[1])**2
            obb.Shape = bc.toShape()

            p7 = p6+App.Rotation(VZ, tts[1]-arcs[2]).multVec(VX)*tf
            p8 = p0+App.Rotation(VZ, arcs[1]).multVec(VX)*tf
            bc.buildFromPolesMultsKnots(
                [p6, p7, p8, p0], [4, 4], [0, 1], False, 3)
            minf += (bc.length()-lens[2])**2
            obc.Shape = bc.toShape()

            Gui.updateGui()
            return minf

    methods = [
        'Nelder-Mead',
        'Powell',
        'CG',
        'BFGS',
        'L-BFGS-B',
        'TNC',
        'COBYLA',
        'SLSQP',
    ]

    rc = minimize(minFun, tts, tol=3)
    for ob in [oba, obb, obc]: grp.addObject(ob)
    _ = Part.makeFilledFace(Part.__sortEdges__(
        [oba.Shape.Edge1, obb.Shape.Edge1, obc.Shape.Edge1, ]))
    try:
        _.check()
        f = App.ActiveDocument.addObject('Part::Feature', 'Face')
        f.Shape = _
        grp.addObject(f)
        if rc.success:
            print(round(rc.fun), round(f.Shape.Area), np.round(rc.x, 1))
    except:
            for ob in [oba, obb, obc]: App.ActiveDocument.removeObject(ob.Name)
            App.ActiveDocument.removeObject(grp.Name)

    for m in methods:
        grp = App.ActiveDocument.addObject("App::DocumentObjectGroup", m)
        oba = App.ActiveDocument.addObject("Part::Feature", "A"+m)
        obb = App.ActiveDocument.addObject("Part::Feature", "B"+m)
        obc = App.ActiveDocument.addObject("Part::Feature", "C"+m)
        for ob in [oba, obb, obc]: grp.addObject(ob)
        rc = minimize(minFun, tts, method=m, tol=10.0)

        try:
            _ = Part.makeFilledFace(Part.__sortEdges__(
                [oba.Shape.Edge1, obb.Shape.Edge1, obc.Shape.Edge1, ]))
            _.check()
            f = App.ActiveDocument.addObject('Part::Feature', 'Face')
            f.Shape = _
            grp.addObject(f)
            if rc.success:
                print(round(rc.fun), round(f.Shape.Area), m, np.round(rc.x, 1))
            print("diff lens", [round(e.Length-l, 1)
                  for e, l in zip(f.Shape.Edges, lens)])
        except:
            for ob in [oba, obb, obc]: App.ActiveDocument.removeObject(ob.Name)
            App.ActiveDocument.removeObject(grp.Name)

        # break
    print("finished")


def AAA():
    '''find cones by points '''

    pts = [v.Point for v in App.ActiveDocument.Wedge001.Shape.Vertexes]
    params = [0.]*6
    params = [5, 21, 5, np.pi/2, 0, 0.1]
    # params=[5,20,5,-1,0,0.3]
    paramsA = [21, 0.1]

    def minFun(paramsB, show=False):

        if 0:
        #    print ("paramsb",paramsB
            # params[0]=5
            params[1] = paramsB[0]
            # params[1]=25
            # params[2]=5

            params[3] = np.pi/2
            params[4] = 0

        params = paramsB

        # params[5]=0.4
        S = App.Vector(params[0:3])
        R = App.Vector(
            np.cos(params[3])*np.cos(params[4]),
            np.sin(params[3])*np.cos(params[4]),
            np.sin(params[4]))
        # alpha=params[5]
        alpha = paramsB[1]

#        print ("S",S)
#        print ("R",R)
        fval = 0.
        ptsa = []
        # fval += (S-App.Vector(5,20,5)).Length**2*100
        lx = [0, 1, 4, 5]
        lx = [2, 3, 6, 7]
        # lx=range(8)
        # lx=[0]
        # lx=[0,1,2]
        for pi in lx:
        # for pi in :
            p = pts[pi]
#            print ("!",pi,p)
            a = (p-S).dot(R)
            n = (p-S).cross(R)
            n2 = n.cross(R).normalize()
            r2a = n2*np.sin(alpha)
            r2 = R*np.cos(alpha)+r2a
#            print ("r2 ",r2
            if 10:
                # print ("r2",r2
                # print("lens",alpha, (p-S).dot(r2),(p-S).Length)
                # print (abs((p-S).dot(r2))-(p-S).Length)**2
#                print("l-",alpha, (p-S).dot(r2))

                ptsa += [S, p, S+(p-S).dot(r2)*r2, p, S]
            # fval += (abs((p-S).dot(r2))-(p-S).Length)**2

            a = r2*(p-S).dot(r2)-(p-S)
            b = r2*(p-S).dot(r2)+(p-S)
            ab = a if a.Length < b.Length else b

#            if pi==0:
#                print ab.Length
#                print r2*(p-S).dot(r2)
#                print p-S
            fval += ((ab.Length) ** 2) * 10**5

#        print ("fval",fval,"alp",alpha,"S:",S)
#        print (fval,paramsB)

        #    v2=n2*np.tan(alpha)*a+R*a
        #    if show: print a
            # fval +=((S+R*a-p).Length - a*np.tan(alpha))**2
            # fval += ((S+R*a-p).Length - v2.Length)**2
            # fval +=(p-S-v2).Length**2
        if show:
                # print (a,(S+R*a-p).Length,a*np.tan(alpha))
#                print (S+R*a-p).Length #- a*np.tan(alpha)
                pass

#        if show:
#            print ("fval", fval
#            Draft.makeWire(ptsa)

        # print (fval," ",paramsB)
        return fval

    methods = [
        'Nelder-Mead',
        'Powell',
        'CG',
        'BFGS',
        'L-BFGS-B',
        'TNC',
        'COBYLA',
        'SLSQP',
    ]

    for alpha in range(275, 276):
        break
        params[5] = 0.001*alpha
        minFun(params, True)
#    return

    # bounds fuer 4,5,7
    methods = [methods[i] for i in [5]]

    print("auswertung------------")
    for m in methods:
        minv=10**10
        for a in range(10, 30):
            # print()
            for b in [0.271, 0.274, 0.275, 0.276, 0.278, 0.279]:
                paramsA=[a, b]
                params[1]=a
                params[5]=b
                # print ("!!",a,b, paramsA)
                # rc=minimize(minFun,params,method=m,tol=.1,bounds=[(5,5),(24,30),(5,5),(0,2),(0,2),(0,2)])
                # rc=minimize(minFun,paramsA,method=m,tol=.01,bounds=[(20,30),(0.1,0.3)])
                # rc=minimize(minFun,paramsA,method=m,tol=.0001)
                rc=minimize(minFun, params, method=m, tol=.0001, bounds=[
                            (0, 10), (20, 30), (0, 15), (0, 2), (0, 2), (0, 2)])
                if rc.success:
#                    print ("-----------",round(rc.fun,8),rc.x,a,b)
                    if minv > rc.fun:
                        print("*")
                        minv=rc.fun
                        result=rc.x
#                else:
#                    print (m,rc.success,rc.message)

        # print ("minv ",minv, result)

        if 1:

            params2=params
            params2[1]=result[0]
            params2[5]=result[1]

            params2=result

            S=App.Vector(params2[0:3])
            R=App.Vector(
                    np.cos(params2[3])*np.cos(params2[4]),
                    np.sin(params2[3])*np.cos(params2[4]),
                    np.sin(params2[4]))

            R *= -1
            t=S.cross(R).normalize()
            t2=t.cross(R).normalize()
            k=40
            T=S+R*k+t*k*np.tan(params[5])
            T2=S+R*k+t2*k*np.tan(params[5])
            T3=S+R*k-t*k*np.tan(params[5])
            T4=S+R*k-t2*k*np.tan(params[5])
            TT=S+R*2*k

            w=Draft.makeWire([S, T, S, T2, S, T3, S, T4, S, TT])
            print("minv ", minv, result, str(w.Label))


            # minFun(rc.x,True)

#
# version 2
#

def AA():
    '''find cones by points'''
    pts=[v.Point for v in App.ActiveDocument.Wedge001.Shape.Vertexes]
    params=[0.]*6
    params=[5, 25, 5, np.pi/2, 0]
    params=[5, 25, 5, np.pi/2, 0]
    # params=[5,20,5,-1,0,0.3]
    paramsA=[21, 0.1]
    bb=[0., 0.]

    def minFun(paramsB, show=False):

        if 0:
        #    print ("paramsb",paramsB
            params[0]=5
#            params[1]=paramsB[0]
            params[1]=25
            params[2]=5

#            params[3]=np.pi/2
#            params[4]=0
            pass

        params[3:5]=paramsB

        # params[5]=0.4
        S=App.Vector(params[0:3])
        R=App.Vector(
            np.cos(params[3])*np.cos(params[4]),
            np.sin(params[3])*np.cos(params[4]),
            np.sin(params[4]))

#        print ("S",S)
#        print ("R",R)
        fval=0.
        ptsa=[]

        lx=[0, 1, 4, 5]
        # lx=[2,3,6,7]
        lx=range(8)
        # lx=[0]
        # lx=[0,1,2]

        aas=[]
        for pi in lx:
            p=pts[pi]
#            print ("!",pi,p)
            a=abs((p-S).normalize().dot(R))
            aas += [a]


        fval=np.std(aas)*10**5
        bb[0]=np.mean(aas)
        # print bb
        # fval += ((ab.Length) **2) * 10**5

        # print aas;
#        print ("fval",fval,[round(d,4) for d in paramsB])#,S,R)
        return fval




    methods=[
        'Nelder-Mead',
        'Powell',
        'CG',
        'BFGS',
        'L-BFGS-B',
        'TNC',
        'COBYLA',
        'SLSQP',
    ]



    for alpha in range(275, 276):
        break
        minFun(params, True)
#    return

    # bounds fuer 4,5,7
    methods=[methods[i] for i in [1]]

    print("auswertung------------")

    for m in methods:
        minv=10**10
        for x in range(3, 8):
            for z in range(3, 8):
                for p in range(0, 10):
                    params[1]=20+p
                    params[0]=x
                    params[2]=z
                    for a in [4]:
            #            print
                        for b in [7]:
                            paramsA=[(a-10)*0.1*np.pi/2, 0.1*(b-10)]
                            # params[1]=25
                            # params[0]=b


                            # rc=minimize(minFun,paramsA,method=m,tol=.0001,bounds=[(5,5),(25,25),(5,5),(-2,2),(-2,2)])
                            rc=minimize(minFun, paramsA, method=m, tol=.1)
                            if rc.success:
            #                    print ("-----------",round(rc.fun,8),rc.x,a,b)
                                if minv > rc.fun:
                                    print("*")
                                    minv=rc.fun
                                    result=rc.x
                                    pos=[x, z, p]
                                    print("!minv ", round(minv*10**5, 2),
                                          [round(r, 3) for r in result], a, b, p)
                                    print("pos ", pos)
                            else:
                                print(m, rc.success, rc.message)
                        if minv < 0.1:
                            print("!minv ", minv, [round(r, 3)
                                  for r in result], a, b, p)
                            print(bb, round(minv*10**5, 2), x, z, p)
                            print("pos ", pos)


                            params2=params
                            params2[3:5]=result

                            S=App.Vector(params2[0:3])
                            R=App.Vector(
                                    np.cos(params2[3])*np.cos(params2[4]),
                                    np.sin(params2[3])*np.cos(params2[4]),
                                    np.sin(params2[4]))

                            R *= -1
                            t=S.cross(R).normalize()
                            t2=t.cross(R).normalize()
                            k=30
                            alpha=np.arccos(bb[0])
                            T=S+R*k+t*k*np.tan(alpha)
                            T2=S+R*k+t2*k*np.tan(alpha)
                            T3=S+R*k-t*k*np.tan(alpha)
                            T4=S+R*k-t2*k*np.tan(alpha)
                            TT=S+R*2*k

            #                print S
            #                print R
                            w=Draft.makeWire([S, TT])
                            w=Draft.makeWire(
                                [S, T, S, T2, S, T3, S, T4, S, TT])
            #                print ("minv ",minv, result, str(w.Label))
                            return


        return

def huhu():

    if 0:
        minv=10**10
        for a in range(10, 30):
#            print
            for b in [0.271, 0.274, 0.275, 0.276, 0.278, 0.279]:
                paramsA=[a, b]
                params[1]=a
                params[5]=b
                # print ("!!",a,b, paramsA)
                # rc=minimize(minFun,params,method=m,tol=.1,bounds=[(5,5),(24,30),(5,5),(0,2),(0,2),(0,2)])
                # rc=minimize(minFun,paramsA,method=m,tol=.01,bounds=[(20,30),(0.1,0.3)])
                # rc=minimize(minFun,paramsA,method=m,tol=.0001)
                rc=minimize(minFun, params, method=m, tol=.0001, bounds=[
                            (0, 10), (20, 30), (0, 15), (0, 2), (0, 2), (0, 2)])
                if rc.success:
#                    print ("-----------",round(rc.fun,8),rc.x,a,b)
                    if minv > rc.fun:
                        print("*")
                        minv=rc.fun
                        result=rc.x
#                else:
#                    print (m,rc.success,rc.message)

        # print ("minv ",minv, result)

        if 1:

            params2=params
            params2[1]=result[0]
            params2[5]=result[1]

            params2=result

            S=App.Vector(params2[0:3])
            R=App.Vector(
                    np.cos(params2[3])*np.cos(params2[4]),
                    np.sin(params2[3])*np.cos(params2[4]),
                    np.sin(params2[4]))

            R *= -1
            t=S.cross(R).normalize()
            t2=t.cross(R).normalize()
            k=40
            T=S+R*k+t*k*np.tan(params[5])
            T2=S+R*k+t2*k*np.tan(params[5])
            T3=S+R*k-t*k*np.tan(params[5])
            T4=S+R*k-t2*k*np.tan(params[5])
            TT=S+R*2*k

            w=Draft.makeWire([S, T, S, T2, S, T3, S, T4, S, TT])
            print("minv ", minv, result, str(w.Label))
            print

            # minFun(rc.x,True)
