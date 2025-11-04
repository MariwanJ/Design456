# SPDX-FileContributor: Mariwan Jalal ( mariwan.jalal@gmail.com )
# SPDX-FileNotice: Included in the Design456 addon.
# SPDX-FileNotice: Part of the Defeaturing addon.

from __future__ import unicode_literals

#****************************************************************************
#*                                                                          *
#*  Kicad STEPUP (TM) (3D kicad board and models to STEP) for FreeCAD       *
#*  3D exporter for FreeCAD                                                 *
#*  Kicad STEPUP TOOLS (TM) (3D kicad board and models to STEP) for FreeCAD *
#*  Copyright (c) 2015                                                      *
#*  Maurice easyw@katamail.com                                              *
#*                                                                          *
#*  Kicad STEPUP (TM) is a TradeMark and cannot be freely usable            *
#*                                                                          *
import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import Part
import imp, os, sys, tempfile
from PySide import QtGui, QtCore
from Design456Init import *

try:
    from PathScripts.PathUtils import horizontalEdgeLoop
    from PathScripts.PathUtils import horizontalFaceLoop
    from PathScripts.PathUtils import loopdetect
except:
    App.Console.PrintError('Path WB not found\n')

#reload_Gui=False#True

def oreload_lib(lib):
    if (sys.version_info > (3, 0)):
        import importlib
        importlib.reload(lib)
    else:
        reload (lib)

class oDefeatShapeFeature:
    def IsActive(self):

        if hasattr(Part, "OCC_VERSION"):
            OCCMV = Part.OCC_VERSION.split('.')[0]
            OCCmV = Part.OCC_VERSION.split('.')[1]
            if (int(OCCMV)>= 7) and (int(OCCmV)>= 3):
                sel = Gui.Selection.getSelectionEx()
                for sub in sel:
                    if 'Face' in str(sub.SubElementNames):
                        return True
        else:
            return False

    def Activated(self):
        import Part, DefeaturingFeature
        selection=Gui.Selection.getSelectionEx()
        rh_faces = [];rh_faces_names=[]
        selEx=Gui.Selection.getSelectionEx()
        if len (selEx) > 0:
            for selFace in selEx:
                for i,f in enumerate(selFace.SubObjects):
                    if 'Face' in selFace.SubElementNames[i]:
                        rh_faces.append(f)
                        rh_faces_names.append(selFace.ObjectName+'.'+selFace.SubElementNames[i])
                        print(selFace.ObjectName+'.'+selFace.SubElementNames[i])

            for selobj in selection:
                newobj=selobj.Document.addObject("Part::FeaturePython",'defeat')
                DefeaturingFeature.oDefeatShape(rh_faces_names,newobj,selobj.Object)
                DefeaturingFeature.ViewProviderTree(newobj.ViewObject)
                newobj.Label='defeat_%s' % selobj.Object.Label
                selobj.Object.ViewObject.hide()
            App.ActiveDocument.recompute()
    def GetResources(self):
        return {'Pixmap'  : os.path.join(DefeaturingWB_icons_path,'DefeaturingParametric.svg'), 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('DefeatShapeFeature',\
                'Defeat Shape Feature'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('DefeatShapeFeature',\
                'Create Defeat Shape Parametric Feature')}
Gui.addCommand('oDefeatShapeFeature',oDefeatShapeFeature())


class oDF_SelectLoop:
    "the Path command to complete loop selection definition"
    def __init__(self):
        self.obj = None
        self.sub = []
        self.active = False
        
    def Activated(self):
        sel = Gui.Selection.getSelectionEx()[0]
        obj = sel.Object
        edge1 = sel.SubObjects[0]
        if 'Face' in sel.SubElementNames[0]:
            loop = horizontalFaceLoop(sel.Object, sel.SubObjects[0], sel.SubElementNames)
            if loop:
                Gui.Selection.clearSelection()
                Gui.Selection.addSelection(sel.Object, loop)
            loopwire = []
        elif len(sel.SubObjects) == 1:
            loopwire = horizontalEdgeLoop(obj, edge1)
        else:
            edge2 = sel.SubObjects[1]
            loopwire = loopdetect(obj, edge1, edge2)

        if loopwire:
            Gui.Selection.clearSelection()
            elist = obj.Shape.Edges
            for e in elist:
                for i in loopwire.Edges:
                    if e.hashCode() == i.hashCode():
                        Gui.Selection.addSelection(obj, "Edge"+str(elist.index(e)+1))

    def formsPartOfALoop(self, obj, sub, names):
        if names[0][0:4] != 'Edge':
            if names[0][0:4] == 'Face' and horizontalFaceLoop(obj, sub, names):
                return True
            return False
        if len(names) == 1 and horizontalEdgeLoop(obj, sub):
            return True
        if len(names) == 1 or names[1][0:4] != 'Edge':
            return False
        return True

    def GetResources(self):
        return {'Pixmap'  : os.path.join( DefeaturingWB_icons_path , 'Path-SelectLoop.svg') ,
                'MenuText': "Defeaturing_SelectLoop",
                'ToolTip': "Defeaturing SelectLoop"} 
                
if App.GuiUp:
    Gui.addCommand('oDF_SelectLoop', oDF_SelectLoop())

class orefineFeatureTool:
    "refine Feature Parametric"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( DefeaturingWB_icons_path , 'RefineShapeFeature.svg') , # the name of a svg file available in the resources
                     'MenuText': "refine Feature" ,
                     'ToolTip' : "refine Feature Parametric"}
 
    def IsActive(self):
        if len(Gui.Selection.getSelection()) > 0:
            return True
 
    def Activated(self):
        import OpenSCADFeatures
        doc=App.ActiveDocument
        docG = Gui.ActiveDocument
        sel=Gui.Selection.getSelectionEx()
        if len (sel) > 0:
            for selobj in sel:
                if hasattr(selobj.Object,"Shape"):        
                    newobj=selobj.Document.addObject("Part::FeaturePython",'refined')
                    OpenSCADFeatures.RefineShape(newobj,selobj.Object)
                    OpenSCADFeatures.ViewProviderTree(newobj.ViewObject)
                    ## to do: see if it is possible to conserve colors in refining
                    docG.ActiveObject.ShapeColor=docG.getObject(selobj.Object.Name).ShapeColor
                    docG.ActiveObject.LineColor=docG.getObject(selobj.Object.Name).LineColor
                    docG.ActiveObject.PointColor=docG.getObject(selobj.Object.Name).PointColor
                    docG.ActiveObject.DiffuseColor=docG.getObject(selobj.Object.Name).DiffuseColor
                    docG.ActiveObject.Transparency=docG.getObject(selobj.Object.Name).Transparency

                    newobj.Label=selobj.Object.Label
                    selobj.Object.ViewObject.hide()
            doc.recompute()
Gui.addCommand('orefineFeatureTool',orefineFeatureTool())


class oFuzzyCut:
    "Fuzzy boolean Cut"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( DefeaturingWB_icons_path , 'FuzzyCut.svg') , # the name of a svg file available in the resources
                     'MenuText': "Fuzzy boolean Cut" ,
                     'ToolTip' : "Fuzzy boolean Cut"}
 
    def IsActive(self):
        doc = App.ActiveDocument
        if hasattr(Part, "OCC_VERSION"):
            OCCMV = Part.OCC_VERSION.split('.')[0]
            OCCmV = Part.OCC_VERSION.split('.')[1]
            if (int(OCCMV)>= 7) and (int(OCCmV)>= 1):
                #return True
                if len(Gui.Selection.getSelection()) == 2:
                    return True
        else:
            return False
 
    def Activated(self):
        # do something here...
        import DefeaturingWB.oFuzzyTools 
        oreload_lib(DefeaturingWB.oFuzzyTools)
        DefeaturingWB.oFuzzyTools.ofuzzyCut()

 
Gui.addCommand('oFuzzyCut',oFuzzyCut())


class oFuzzyUnion:
    "Fuzzy boolean Union"
    def GetResources(self):
        return {'Pixmap'  : os.path.join( DefeaturingWB_icons_path , 'FuzzyUnion.svg') , # the name of a svg file available in the resources
                     'MenuText': "Fuzzy boolean Union" ,
                     'ToolTip' : "Fuzzy boolean Union"}
 
    def IsActive(self):
        doc = App.ActiveDocument
        if hasattr(Part, "OCC_VERSION"):
            OCCMV = Part.OCC_VERSION.split('.')[0]
            OCCmV = Part.OCC_VERSION.split('.')[1]
            if (int(OCCMV)>= 7) and (int(OCCmV)>= 1):
                #return True
                if len(Gui.Selection.getSelection()) > 1:
                    return True
        else:
            return False

    def Activated(self):
        # do something here...
        import DefeaturingWB.oFuzzyTools
        oreload_lib(DefeaturingWB.oFuzzyTools)
        DefeaturingWB.oFuzzyTools.ofuzzyUnion()
 
Gui.addCommand('oFuzzyUnion',oFuzzyUnion())

class oFuzzyCommon:
    "Fuzzy boolean Common"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( DefeaturingWB_icons_path , 'FuzzyCommon.svg') , # the name of a svg file available in the resources
                     'MenuText': "Fuzzy boolean Common" ,
                     'ToolTip' : "Fuzzy boolean Common"}
 
    def IsActive(self):
        doc = App.ActiveDocument
        if hasattr(Part, "OCC_VERSION"):
            OCCMV = Part.OCC_VERSION.split('.')[0]
            OCCmV = Part.OCC_VERSION.split('.')[1]
            if (int(OCCMV)>= 7) and (int(OCCmV)>= 1):
                #return True
                if len(Gui.Selection.getSelection()) > 1:
                    return True
        else:
            return False

    def Activated(self):
        # do something here...
        import DefeaturingWB.oFuzzyTools
        oreload_lib(DefeaturingWB.oFuzzyTools)
        DefeaturingWB.oFuzzyTools.ofuzzyCommon()

 
Gui.addCommand('oFuzzyCommon',oFuzzyCommon())
