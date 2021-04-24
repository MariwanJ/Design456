# -*- coding: utf-8 -*-
# -------------------------------------------------
# -- extra workspace
# --
# -- microelly 2017 v 0.1
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------


import FreeCAD as App
import FreeCADGui as Gui
import os, sys

import NURBSinit


from PySide import QtGui
import Part
import Mesh
import Draft
import Points



try:
    import numpy as np
except ImportError:
    print("Please install the required module : numpy")

import random
import nurbs


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

    def _haha(self):
        pass


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
        print("onChanged", prop)


class Nurbs_ViewProviderSL(ViewProvider):

    def onChanged(self, obj, prop):
        print("onChanged X", prop)
        if obj.Visibility:
            ws = WorkSpace(obj.Object.workspace)
            print(ws)
            jj = ws.dok.getObject(obj.Object.source.Name)
            print(jj)
            print(jj.Name)
            jj.ViewObject.show()

        else:
            ws = WorkSpace(obj.Object.workspace)
            print(ws)
            jj = ws.dok.getObject(obj.Object.source.Name)
            print(jj)
            jj.ViewObject.hide()
        print("done")

    def onDelete(self, obj, subelements):
        print("on Delete Sahpelink")
        print("from", obj.Object.workspace, obj.Object.Label, obj.Object.Name)
        try:
            _ = App.getDocument(obj.Object.workspace)
        except:
            return True
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


class Nurbs_ShapeLink(PartFeature):

    def __init__(self, obj, sobj, docname):
        print("create shape link")
        PartFeature.__init__(self, obj)
        obj.addProperty("App::PropertyLink", "source", "Base")
        obj.addProperty("App::PropertyBool", "nurbs", "Base")
        obj.addProperty("App::PropertyInteger", "gridcount", "Base")
        obj.addProperty("App::PropertyFloat", "umax", "Base")
        obj.addProperty("App::PropertyFloat", "vmax", "Base")
        obj.addProperty("App::PropertyString", "workspace", "Base")

        obj.umax = 1.0
        obj.vmax = 1.0
        obj.source = sobj
        obj.workspace = docname
        obj.gridcount = 20

        ViewProviderSL(obj.ViewObject)

    def execute(proxy, obj):
        if not obj.ViewObject.Visibility:
            return
        objnurbs = None  # Added by mariwan .. dont know what this do
        print("update shape", obj.source.Name, obj.workspace, obj.gridcount)

        tw = WorkSpace(obj.workspace)
        print("!!")
        print(tw)
        print(tw.dok)
        target = tw.dok.getObject(obj.source.Name)
        print(target)
        if target == None:
            tw.addObject2(obj.source, obj.gridcount)
        print(target)
        if objnurbs:
            print("nurbs surface")
            target.Shape = obj.source.Shape.toNurbs()

            cs = []
            count = obj.gridcount
            # f=obj.source.Shape.Face1.toNurbs()
            # f=f.Face1.Surface

            for ff in obj.source.Shape.Faces:
                print("Face")
                print(ff)
                f2 = ff.toNurbs()
                cs.append(f2)
                f = f2.Face1.Surface

                for ui in range(count+1):
                    cs.append(f.uIso(obj.umax/count*ui).toShape())
                for vi in range(count+1):
                    cs.append(f.vIso(obj.vmax/count*vi).toShape())
            target.Shape = Part.Compound(cs)
            App.cs = cs
        else:
            print("no nurbs")
            target.Shape = obj.source.Shape
        tw.recompute()
        print("act dok ")
        print(App.ActiveDocument.Label)


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


class Nurbs_initGUI():

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
                print("found")
                return w2
        print(self.name + '1:1[*]')

    def _haha(self):
        pass


class Nurbs_createLink:
    """ 
    create link 
    TODO: When do you use this? Write comments Mariwan
    """

    def Activated(self, obj, docname="Linkdoc"):
        ad = App.ActiveDocument
        print(ad.Name)

        lidok = WorkSpace(docname)
        link = lidok.addObject2(obj)
        lidok.recompute()

        bares = obj.Document.addObject(
            "Part::FeaturePython", "Base Link "+obj.Label)
        bares.Label = obj.Label+"@"+docname

        ShapeLink(bares, obj, docname)
        bares.Proxy.execute(bares)

        return bares


class Nurbs_CreateWSLink:
    """ 
    create new workspace
    TODO: When do you use this? Write comments Mariwan
    """

    def Activated(self, docname="Linkdoc"):
        ad = App.ActiveDocument
        bares = ad.addObject("Part::FeaturePython", "WS "+docname+"")
        WSLink(bares, docname)
        return bares

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap': NURBSinit.ICONS_PATH+'workspacelink.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "NurbsCreateWSLink"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 Nurbs CreateWSLink", _tooltip)}


Gui.addCommand("Nurbs_CreateWSLink", Nurbs_CreateWSLink())


class Nurbs_CreateWorkspace:
    """ 
    create new workspace
    TODO: When do you use this? Write comments Mariwan
    """

    def Activated(self):
        '''called from the menu '''
        adname = App.ActiveDocument.Name

        ad = App.ActiveDocument
        bares = ad.addObject("Part::FeaturePython", "WS "+adname+"")
        WSLink(bares, "TestMeWorkspace")
        App.setActiveDocument(adname)
        App.ActiveDocument = App.getDocument(adname)
        Gui.ActiveDocument = Gui.getDocument(adname)
        App.ActiveDocument.recompute()

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap': NURBSinit.ICONS_PATH+'workspace.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "NurbsCreateWorkspace"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 Nurbs CreateWorkspace", _tooltip)}


Gui.addCommand("Nurbs_CreateWorkspace", Nurbs_CreateWorkspace())


def createlink():
    '''called from the menu '''
    ad = App.ActiveDocument.Name
    cc = Gui.Selection.getSelection()[0]
    ws = Gui.Selection.getSelection()[-1]
    createLink(cc, ws.workspace)
    App.setActiveDocument(ad)
    App.ActiveDocument = App.getDocument(ad)
    Gui.ActiveDocument = Gui.getDocument(ad)
    App.ActiveDocument.recompute()


# ---------------------------------
'''

import workspace
#reload(workspace)

def testme():
    ad=App.ActiveDocument.Name
    cc=Gui.Selection.getSelection()[0]
    workspace.createWsLink("TestMeWorkspace")
    workspace.createLink(cc,"TestMeWorkspace")
    App.setActiveDocument(ad)
    App.ActiveDocument=App.getDocument(ad)
    Gui.ActiveDocument=Gui.getDocument(ad)
    App.ActiveDocument.recompute()


Gui.Selection.addSelection(App.ActiveDocument.Box)
testme()

'''
# ---------------------------------


def huhu():
    pass


def __haha():
    pass

# TODO : FIXME .. WHAT SHOULD THIS CLASS NAME BE? MARIWAN


class Nurbs_main:
    def Activated(self):
        if App.ActiveDocument == None:
            App.newDocument("Unnamed")
            App.setActiveDocument("Unnamed")
            App.ActiveDocument = App.getDocument("Unnamed")
            Gui.ActiveDocument = Gui.getDocument("Unnamed")

        ad = App.ActiveDocument

        aa = App.ActiveDocument.addObject("Part::Box", "Box")
        bb = App.ActiveDocument.addObject("Part::Torus", "Torus")
        cc = App.ActiveDocument.addObject("Part::Cylinder", "Cylinder")

        App.ActiveDocument.recompute()

        wl = createWsLink("Shoe")
        App.ActiveDocument = ad

        c = createLink(cc, "Shoe")
        b = createLink(bb, "Shoe")
        a = createLink(aa, "Shoe")

        b.umax = 6
        b.vmax = 6

        c.umax = 6
        c.vmax = 6

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_main")
        return {'Pixmap': NURBSinit.ICONS_PATH+'drawing.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_main"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456  Nurbs_main", _tooltip)}


Gui.addCommand("Nurbs_main", Nurbs_main())
