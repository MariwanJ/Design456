#***************************************************************************
#*																		   *
#*	Open source - FreeCAD												   *
#*	Design456 Workbench													   *
#*	Auth : Mariwan Jalal and others										   *
#***************************************************************************
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import Part
import BOPTools.SplitFeatures as SPLIT
from FreeCAD import Base

class Design456_SplitObject:
	"""Devide object in to two parts"""
	def Activated(self):
		
		Gui.runCommand('Part_CrossSections',0)
		wires=list()
		selection = Gui.Selection.getSelectionEx()
		shape=selection[0].Object.Shape
		
		bb=shape.BoundBox
		length=max(bb.XLength,bb.YLength,bb.ZLength)
		
		for i in shape.slice(Base.Vector(0,0,1),length):
			wires.append(i)

		comp=Part.Compound(wires)
		#get object name 
		slice=App.activeDocument().getObject(selection[0].ObjectName+'_cs')
		
		### Begin command Part_Compound
		gcompund=App.activeDocument().addObject("Part::Compound","Compound")
		gcompund.Links = slice                             #TODO : Doesn't work here but in the GUI works? why? 
		gcompund.touch()
		App.ActiveDocument.recompute()
		
		
		### Begin command Part_BooleanFragments
		j = SPLIT.makeBooleanFragments(name='BooleanFragments')
		j.Objects = [App.ActiveDocument.Compound, selection[0].Object]
		j.Mode = 'Standard'
		j.Proxy.execute(j)
		j.purgeTouched()
		for obj in j.ViewObject.Proxy.claimChildren():
			obj.ViewObject.hide()
		App.ActiveDocument.recompute()
		
		
	def GetResources(self):
		return{
			'Pixmap' :	Design456Init.ICON_PATH +  '/SplitObject.svg',
			'MenuText': 'Split Object',
			'ToolTip': 'Devide object in to two parts'
		}
Gui.addCommand('Design456_SplitObject', Design456_SplitObject()) 

