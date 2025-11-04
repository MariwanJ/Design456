# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2017 Maurice ( easyw@katamail.com )
# SPDX-FileContributor: Mariwan Jalal ( mariwan.jalal@gmail.com )
# SPDX-FileNotice: Part of the Defeaturing addon. Included in the Design456 addon.

from __future__ import unicode_literals

import  os
import OpenSCADUtils, FreeCAD, FreeCADGui, Part, os
import  Design456Init
import FreeCAD as App
global defeat_icon, use_cm
defeat_icon=os.path.join(Design456Init.DefeaturingWB_icons_path,'DefeaturingParametric.svg')
use_cm = True

'''
This Script includes python Features to represent Defeaturing Operations
'''
class ViewProviderTree:
    "A generic View Provider for Elements with Children"
        
    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj.Object
        
    def attach(self, obj):
        self.Object = obj.Object
        return

    def getIcon(self):
        global defeat_icon
        if isinstance(self.Object.Proxy,oDefeatShape):
            return(defeat_icon)

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self,obj):
        modes=[]
        return modes

    def setDisplayMode(self,mode):
        return mode

    def onChanged(self, vp, prop):
        return

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        if state is not None:
            import FreeCAD
            doc = App.ActiveDocument #crap
            self.Object = doc.getObject(state['ObjectName'])

    def claimChildren(self):
        objs = []
        if hasattr(self.Object.Proxy,"Base"):
            objs.append(self.Object.Proxy.Base)
        if hasattr(self.Object,"Base"):
            objs.append(self.Object.Base)
        if hasattr(self.Object,"Objects"):
            objs.extend(self.Object.Objects)
        if hasattr(self.Object,"Components"):
            objs.extend(self.Object.Components)
        if hasattr(self.Object,"Children"):
            objs.extend(self.Object.Children)
        return objs
   

##
class oDefeatShape:
    '''return a refined shape'''
    def __init__(self, fc, obj, child=None):
        
        global use_cm
        doc = App.ActiveDocument
        obj.addProperty("App::PropertyLink","Base","Base",
                        "The base object that must be defeatured")
        obj.Proxy = self
        obj.Base = child
        obj.addProperty("App::PropertyStringList","Faces","dFaces",
                        "List of Faces to be defeatured")
        obj.Faces = fc
        if use_cm:
            obj.addProperty("App::PropertyStringList","CM","dFaces",
                            "Center of Mass")
            cm = []
            for f in fc:    
                oname = obj.Base.Name #f.split('.')[0]
                o = doc.getObject(oname)
                fnbr = int(f.split('.')[1].strip('Face'))-1
                mf = o.Shape.Faces[fnbr]
                cm.append('x='+"{0:.3f}".format(mf.CenterOfMass.x)+' y='+"{0:.3f}".format(mf.CenterOfMass.y)+' z='+"{0:.3f}".format(mf.CenterOfMass.z))
            obj.CM = cm
            obj.addProperty("App::PropertyBool","useFaceNbr","dFaces",
                            "use Face Number")
        
    def onChanged(self, fp, prop):
        "Do something when a property has changed"
        doc = App.ActiveDocument
        d_faces=[]

        if (prop == 'useFaceNbr' or prop == 'Shape') and len (fp.Base.Shape.Faces) > 0:

            if fp.useFaceNbr: #not use_cm:
                cm_list=[]
                for fn in fp.Faces:
                    oname = fp.Base.Name #fp.Faces[0].split('.')[0]
                    fnbr = int(fn.split('.')[1].strip('Face'))-1
                    o = doc.getObject(oname)
                    for i, f in enumerate (o.Shape.Faces):
                        if i == fnbr:

                            d_faces.append(f)
                            c='x='+"{0:.3f}".format(f.CenterOfMass.x)+' y='+"{0:.3f}".format(f.CenterOfMass.y)+' z='+"{0:.3f}".format(f.CenterOfMass.z)
                            cm_list.append(c)

                    fp.CM = cm_list        
            else:

                if len (fp.Base.Shape.Faces) > 0:
                    fc = []
                    for i, c in enumerate(fp.CM):
                        for j, f in enumerate (fp.Base.Shape.Faces):
                                if c ==('x='+"{0:.3f}".format(f.CenterOfMass.x)+' y='+"{0:.3f}".format(f.CenterOfMass.y)+' z='+"{0:.3f}".format(f.CenterOfMass.z)):
                                    d_faces.append(f)
                                    fc.append(str(fp.Base.Name)+'.'+'Face'+str(j+1))
                    fp.Faces = fc
                else:
                    print('loading first time')
        pass

    def execute(self, fp):
        global defeat_icon, use_cm
        doc = App.ActiveDocument
        docG = Gui.ActiveDocument
        if len (fp.Faces) > 0:
            if fp.Base and fp.Base.Shape.isValid():
                d_faces=[]
                if fp.useFaceNbr: #not use_cm:
                    cm_list=[]
                    for fn in fp.Faces:
                        oname = fp.Base.Name #fp.Faces[0].split('.')[0]
                        fnbr = int(fn.split('.')[1].strip('Face'))-1
                        o = doc.getObject(oname)
                        for i, f in enumerate (o.Shape.Faces):
                            if i == fnbr:
                                d_faces.append(f)
                                c='x='+"{0:.3f}".format(f.CenterOfMass.x)+' y='+"{0:.3f}".format(f.CenterOfMass.y)+' z='+"{0:.3f}".format(f.CenterOfMass.z)
                                cm_list.append(c)

                        fp.CM = cm_list
                else:
                    oname = fp.Base.Name #fp.Faces[0].split('.')[0]
                    o = doc.getObject(oname)
                    fc = []
                    for i, c in enumerate(fp.CM):
                        for j, f in enumerate (fp.Base.Shape.Faces):
                                if c ==('x='+"{0:.3f}".format(f.CenterOfMass.x)+' y='+"{0:.3f}".format(f.CenterOfMass.y)+' z='+"{0:.3f}".format(f.CenterOfMass.z)):
                                    d_faces.append(f)
                                    fc.append(str(o.Name)+'.'+'Face'+str(j+1))
                check_faces = True
                if not fp.useFaceNbr: #use_cm:
                    if len (d_faces) != len (fp.CM):
                        check_faces = False
                elif len (d_faces) == 0:
                    check_faces = False
                if check_faces:
                    sh = fp.Base.Shape.defeaturing(d_faces)
                    if fp.Base.Shape.isPartner(sh):
                        App.Console.PrintError('Defeaturing failed 1\n')
                        defeat_icon=os.path.join(Design456Init.DefeaturingWB_icons_path,'error.svg')
                        docG.getObject(fp.Name).ShapeColor  =  (1.00,0.00,0.00)
                        raise NameError('Defeaturing FAILED!')
                    else:
                        fp.Shape=OpenSCADUtils.applyPlacement(sh)
                        if fp.Label.find('_ERR') != -1:
                            fp.Label=fp.Label[:fp.Label.rfind('_ERR')]
                        defeat_icon=os.path.join(Design456Init.DefeaturingWB_icons_path,'DefeaturingParametric.svg')
                        docG.getObject(fp.Name).ShapeColor  =  docG.getObject(fp.Base.Name).ShapeColor
                        docG.getObject(fp.Name).LineColor   =  docG.getObject(fp.Base.Name).LineColor
                        docG.getObject(fp.Name).PointColor  =  docG.getObject(fp.Base.Name).PointColor
                        docG.getObject(fp.Name).DiffuseColor=  docG.getObject(fp.Base.Name).DiffuseColor
                        docG.getObject(fp.Name).Transparency=  docG.getObject(fp.Base.Name).Transparency
                else:
                    defeat_icon=os.path.join(Design456Init.DefeaturingWB_icons_path,'error.svg')

                    App.Console.PrintError('Defeaturing failed 2\n')
                    sh = fp.Base.Shape
                    fp.Shape=OpenSCADUtils.applyPlacement(sh)
                    if fp.Label.find('_ERR') == -1:
                        fp.Label='%s_ERR' % fp.Label
                    docG.getObject(fp.Name).ShapeColor  =  (1.00,0.00,0.00)
                    raise Exception('Defeaturing FAILED!')

        else:
            print('first executing')
