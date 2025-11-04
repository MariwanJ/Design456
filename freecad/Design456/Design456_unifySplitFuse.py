# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2021 Mario ( mario52a )
# SPDX-FileContributor: Mariwan Jalal ( mariwan.jalal@gmail.com )
# SPDX-FileNotice: Part of the Design456 addon.

#
#   Read more:
#   https://forum.freecadweb.org/viewtopic.php?f=3&t=56185&p=483304&hilit=slice#p483304
#

from __future__ import unicode_literals

import os
import sys
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft as _draft
import Part as _part
import Design456Init
from pivy import coin
import FACE_D as faced
import math as _math
from draftutils.translate import translate   #for translate
from PySide.QtCore import QT_TRANSLATE_NOOP
from draftobjects.base import DraftObject
#

__updated__ = '2022-05-19 22:44:02'

class Design456_LoftBetweenFaces:
    
    def Activated(self):
        try: 
            App.ActiveDocument.openTransaction(translate("Design456","LoftBetweenFaces"))
            selectedObj  = Gui.Selection.getSelectionEx()
            Both3DObject=[False,False]
            FACE1=FACE2=None
            
            if (len(selectedObj) != 2):
                # Two object must be selected
                if (len(selectedObj[0].SubObjects)!=2):
                    errMessage = "Select two Faces of to use the Tool"
                    faced.errorDialog(errMessage)
                    return
                else:
                    FACE1=selectedObj[0].SubObjects[0]
                    FACE2=selectedObj[0].SubObjects[1]

                    Both3DObject[0]=True
                    Both3DObject[1]=True
            else:
                FACE1=selectedObj[0].SubObjects[0]
                FACE2=selectedObj[1].SubObjects[0]
                for i in range(0,2):
                    if faced.isFaceOf3DObj(selectedObj[i]) is True:
                        Both3DObject[i]=True
                    else:
                        Both3DObject[i]=False

            newObj1=newObj2=None
            newObj1= App.ActiveDocument.addObject('Part::Feature','Face1')
            newObj1.Shape = FACE1.copy()
            newObj2=App.ActiveDocument.addObject('Part::Feature','Face2')
            newObj2.Shape = FACE2.copy()
            App.ActiveDocument.recompute()
            
            ### Part_Loft
            attached = App.ActiveDocument.addObject('Part::Loft','Fuse')
            attached.Sections = [newObj1,newObj2 ]
            attached.Solid=True
            attached.Ruled=False
            attached.Closed=False
            ### End command Part_Loft
            App.ActiveDocument.recompute()

            ###Part_Fuse
            if (Both3DObject[0] ==True and Both3DObject[1]==True ):
                fusion = App.ActiveDocument.addObject("Part::MultiFuse","multiFusion")
                allObjects= []
                for o in selectedObj:
                    allObjects.append(o.Object)
                allObjects.append(attached)
                fusion.Shapes = allObjects
                App.ActiveDocument.recompute()
    
                #simplify object
                resultObj= App.ActiveDocument.addObject('Part::Feature','JoinedObjects')
                resultObj.Shape=fusion.Shape.copy()
                App.ActiveDocument.recompute()
                
                # ##### remove Objects 
                for obj in selectedObj:
                    App.ActiveDocument.removeObject(obj.Object.Name)
                App.ActiveDocument.removeObject(attached.Name)
                App.ActiveDocument.removeObject(fusion.Name)
                App.ActiveDocument.removeObject(newObj1.Name)
                App.ActiveDocument.removeObject(newObj2.Name)
            else:
                resultObj= App.ActiveDocument.addObject('Part::Feature','JoinedObjects')
                resultObj.Shape = attached.Shape.copy()
                App.ActiveDocument.recompute()
                for obj in selectedObj:
                    App.ActiveDocument.removeObject(obj.Object.Name)
                App.ActiveDocument.removeObject(attached.Name)
                App.ActiveDocument.removeObject(newObj1.Name)
                App.ActiveDocument.removeObject(newObj2.Name)
                App.ActiveDocument.recompute()

            App.ActiveDocument.commitTransaction() #undo reg.

        except Exception as err:
            App.Console.PrintError("'LoftBetweenFaces' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
            return{
            'Pixmap':    Design456Init.ICON_PATH + 'LoftBetweenFaces.svg',
            'MenuText': 'Loft Between Faces',
            'ToolTip':  'Loft Between 2D/3D Faces'
        }
            
Gui.addCommand('Design456_LoftBetweenFaces', Design456_LoftBetweenFaces())



class Design456_unifySplitFuse2:
    def Activated(self):
        try:
            sel = Gui.Selection.getSelection()
            if (len(sel) != 2):
                # Two object must be selected
                errMessage = "Select two objects to use the Tool"
                faced.errorDialog(errMessage)
                return
            reply = self.askQuestion()
            App.ActiveDocument.openTransaction(translate("Design456","LoftBetweenFaces"))
            Gui.ActiveDocument.getObject(sel[0].Name).Visibility=False
            Gui.ActiveDocument.getObject(sel[1].Name).Visibility=False

            #### Config Begin ####

            switchRemoveConstructionObject = self.askQuestion()    # if 0 (NO) not removed creation objects 1= (YES) remove objects
            colorCommon = (0.9373, 0.1608, 0.1608)
            colorCut1   = (0.4471, 0.6235, 0.8118)
            colorCut2   = (0.0235, 0.6902, 0.6902)
            colorFuse   = (1.0000, 0.6667, 0.0000)
            #### Config End ####

            ##### Begin command _part_Common
            #### create copy
            shapeCommon = _part.getShape(App.ActiveDocument.getObject(sel[0].Name),'',needSubElement=False,refine=False)
            App.ActiveDocument.addObject('Part::Feature','Common1').Shape = shapeCommon
            newObjectCut_A1 = App.ActiveDocument.ActiveObject
            shapeCommon = _part.getShape(App.ActiveDocument.getObject(sel[1].Name),'',needSubElement=False,refine=False)
            App.ActiveDocument.addObject('Part::Feature','Common2').Shape = shapeCommon
            newObjectCut_A2 = App.ActiveDocument.ActiveObject
            ####
            commonObject     = App.ActiveDocument.addObject("Part::MultiCommon","Common")
            commonObjectMake = App.ActiveDocument.getObject(commonObject.Name)
            commonObjectMake.Shapes = [App.ActiveDocument.getObject(newObjectCut_A1.Name), App.ActiveDocument.getObject(newObjectCut_A2.Name),]
            shapeCommonMake  = App.ActiveDocument.ActiveObject
            App.ActiveDocument.recompute()
            Gui.ActiveDocument.activeObject().ShapeColor = colorCommon
            ####
            shapeCommon = _part.getShape(App.ActiveDocument.getObject(shapeCommonMake.Name),'',needSubElement=False,refine=False)
            App.ActiveDocument.addObject('Part::Feature','shapeCommon').Shape = shapeCommon
            Gui.ActiveDocument.activeObject().ShapeColor = colorCommon
            if switchRemoveConstructionObject == 1:
                App.ActiveDocument.removeObject(shapeCommonMake.Name)
                App.ActiveDocument.removeObject(newObjectCut_A1.Name)
                App.ActiveDocument.removeObject(newObjectCut_A2.Name)
            #### End command Part_Common

            #### Begin command Part_Cut First
            #### create copy
            shapeCut1 = _part.getShape(App.ActiveDocument.getObject(sel[0].Name),'',needSubElement=False,refine=False)
            App.ActiveDocument.addObject('Part::Feature','Cut01').Shape = shapeCut1
            newObjectCut_A1 = App.ActiveDocument.ActiveObject
            shapeCut1 = _part.getShape(App.ActiveDocument.getObject(sel[1].Name),'',needSubElement=False,refine=False)
            App.ActiveDocument.addObject('Part::Feature','Cut02').Shape = shapeCut1
            newObjectCut_A2 = App.ActiveDocument.ActiveObject
            ####
            App.ActiveDocument.addObject("Part::Cut","Cut_01")
            App.ActiveDocument.Cut_01.Base = App.ActiveDocument.getObject(newObjectCut_A1.Name)
            App.ActiveDocument.Cut_01.Tool = App.ActiveDocument.getObject(newObjectCut_A2.Name)
            shapeCutMake  = App.ActiveDocument.ActiveObject
            App.ActiveDocument.recompute()
            Gui.ActiveDocument.activeObject().ShapeColor = colorCut1
            ####
            shapeCut01 = _part.getShape(App.ActiveDocument.getObject(shapeCutMake.Name),'',needSubElement=False,refine=False)
            App.ActiveDocument.addObject('Part::Feature','shapeCut01').Shape = shapeCut01
            Gui.ActiveDocument.activeObject().ShapeColor = colorCut1
            if switchRemoveConstructionObject == 1:
                App.ActiveDocument.removeObject(shapeCutMake.Name)
                App.ActiveDocument.removeObject(newObjectCut_A1.Name)
                App.ActiveDocument.removeObject(newObjectCut_A2.Name)
            #### End command Part_Cut First

            #### Begin command Part_Cut Second
            #### create copy
            shapeCut2 = _part.getShape(App.ActiveDocument.getObject(sel[1].Name),'',needSubElement=False,refine=False)
            App.ActiveDocument.addObject('Part::Feature','Cut01').Shape = shapeCut2
            newObjectCut_A1 = App.ActiveDocument.ActiveObject
            shapeCut2 = _part.getShape(App.ActiveDocument.getObject(sel[0].Name),'',needSubElement=False,refine=False)
            App.ActiveDocument.addObject('Part::Feature','Cut02').Shape = shapeCut2
            newObjectCut_A2 = App.ActiveDocument.ActiveObject
            ####
            App.ActiveDocument.addObject("Part::Cut","Cut_02")
            App.ActiveDocument.Cut_02.Base = App.ActiveDocument.getObject(newObjectCut_A1.Name)
            App.ActiveDocument.Cut_02.Tool = App.ActiveDocument.getObject(newObjectCut_A2.Name)
            shapeCutMake  = App.ActiveDocument.ActiveObject
            App.ActiveDocument.recompute()
            Gui.ActiveDocument.activeObject().ShapeColor = colorCut2
            ####
            shapeCut02 = _part.getShape(App.ActiveDocument.getObject(shapeCutMake.Name),'',needSubElement=False,refine=False)
            App.ActiveDocument.addObject('Part::Feature','shapeCut02').Shape = shapeCut02
            Gui.ActiveDocument.activeObject().ShapeColor = colorCut2
            if switchRemoveConstructionObject == 1:
                App.ActiveDocument.removeObject(shapeCutMake.Name)
                App.ActiveDocument.removeObject(newObjectCut_A1.Name)
                App.ActiveDocument.removeObject(newObjectCut_A2.Name)
            #### End command Part_Cut Second

            #### Begin command Part_Fuse
            #### create copy
            shapeFuse1 = _part.getShape(App.ActiveDocument.getObject(sel[1].Name),'',needSubElement=False,refine=False)
            App.ActiveDocument.addObject('Part::Feature','Fuse01').Shape = shapeFuse1
            newObjectFuse1 = App.ActiveDocument.ActiveObject
            shapeFuse2 = _part.getShape(App.ActiveDocument.getObject(sel[0].Name),'',needSubElement=False,refine=False)
            App.ActiveDocument.addObject('Part::Feature','Fuse02').Shape = shapeFuse2
            newObjectFuse2 = App.ActiveDocument.ActiveObject
            ####
            App.ActiveDocument.addObject("Part::MultiFuse","Fusion")
            App.ActiveDocument.Fusion.Shapes = [App.ActiveDocument.getObject(newObjectFuse1.Name),App.ActiveDocument.getObject(newObjectFuse2.Name),]
            shapeCutFusion  = App.ActiveDocument.ActiveObject
            App.ActiveDocument.recompute()
            Gui.ActiveDocument.activeObject().ShapeColor = colorFuse
            ####
            shapeFusion = _part.getShape(App.ActiveDocument.getObject(shapeCutFusion.Name),'',needSubElement=False,refine=False)
            App.ActiveDocument.addObject('Part::Feature','shapeFusion').Shape = shapeFusion
            Gui.ActiveDocument.activeObject().ShapeColor = colorFuse
            if switchRemoveConstructionObject == 1:
                App.ActiveDocument.removeObject(shapeCutFusion.Name)
                App.ActiveDocument.removeObject(newObjectFuse1.Name)
                App.ActiveDocument.removeObject(newObjectFuse2.Name)
            #### End command Part_Fuse
            App.ActiveDocument.commitTransaction() #undo reg.
        except Exception as err:
            App.Console.PrintError("'Design456_unifySplitFuse2' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    def askQuestion(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setStandardButtons(QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
        msgBox.setInformativeText("Remove old objects?")
        t= msgBox.exec_()
        if t== QtGui.QMessageBox.Yes:
            return 1
        else: 
            return 0
    def GetResources(self):
            return{
            'Pixmap':    Design456Init.ICON_PATH + 'UnifySplitFuse2.svg',
            'MenuText': 'unify-Split & Fuse 2',
            'ToolTip':  'unify Split and Fuse2'
        }
Gui.addCommand('Design456_unifySplitFuse2', Design456_unifySplitFuse2())