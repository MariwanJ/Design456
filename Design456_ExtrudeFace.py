# -*- coding: utf-8 -*-
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import FACE_D as Face
import Design456_Extract as face_extract

class Design456_ExtrudeFace:
	def __init__(self):
		return
	
	def Activated(self):
		s = Gui.Selection.getSelectionEx()
		objName = s[0].ObjectName
		sh = s[0].Object.Shape.copy()
		if hasattr(s[0].Object, "getGlobalPlacement"):
			gpl = s[0].Object.getGlobalPlacement()
			sh.Placement = gpl
		name =s[0].SubElementNames[0]
		fullname = objName+"_"+name            #Name of the face extracted
		newobj = s[0].Document.addObject("Part::Feature",fullname)
		newobj.Shape = sh.getElement(name)
		selection =newobj                      #The face extraced
		activeSel=Gui.Selection.getSelection(App.ActiveDocument.Name)
		Gui.Selection.removeSelection(activeSel[0])
		Gui.Selection.addSelection(selection)           #Select the face extracted before
		App.ActiveDocument.recompute()
		m = App.activeDocument().getObject(fullname)
		f = App.activeDocument().addObject('Part::Extrusion','ExtrudeFace')   # Add extrusion
		f.Base = newobj             # App.activeDocument().getObject(fullname)
		f.DirMode = "Normal" 
		f.DirLink = None	
#		if(m.Placement.Rotation.Axis.x==1):
#			f.Base.MapMode='ObjectYZ'
#		elif (m.Placement.Rotation.Axis.y==1):
#			f.Base.MapMode='ObjectXZ'
#		elif (m.Placement.Rotation.Axis.z==1):
#			f.Base.MapMode='ObjectXY'
		
		f.LengthFwd = QtGui.QInputDialog.getDouble(None,"Get value","Input:")[0]
		f.LengthRev = 0.0
		f.Solid = True
		f.Reversed = False
		f.Symmetric = False
		f.TaperAngle = 0.0
		f.TaperAngleRev = 0.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.addObject('Part::Feature',f.Name+'N').Shape=Part.getShape(f,'',needSubElement=False,refine=False)        
		App.ActiveDocument.removeObject(f.Name)
		App.ActiveDocument.removeObject(m.Name)
		App.ActiveDocument.recompute()
		return

	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/ExtrudeFace.svg',
				'MenuText': 'ExtrudeFace',
				'ToolTip':  'ExtrudeFace'
				}

Gui.addCommand('Design456_ExtrudeFace', Design456_ExtrudeFace())
