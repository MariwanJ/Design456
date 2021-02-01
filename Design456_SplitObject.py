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
import BOPTools.SplitFeatures as SPLIT
from FreeCAD import Base
from time import time as _time, sleep as _sleep

class Design456_SplitObject:
	"""Devide object in to two parts"""
	def Activated(self):
		try:
		#Save object name that will be divided.
			selection = Gui.Selection.getSelectionEx()
			shape=selection[0].Object.Shape
			bb=shape.BoundBox
			length=max(bb.XLength,bb.YLength,bb.ZLength)
	
			nameOfselectedObject=selection[0].ObjectName
			totalName=nameOfselectedObject+'_cs'
			
			""" slow function . . you need to use wait before getting 
				the answer as the execution is continuing down """
			Gui.runCommand('Part_CrossSections',0) 
			gcompund=App.ActiveDocument.addObject("Part::Compound","Compound")
			
			App.ActiveDocument.recompute()
			
			#get object name 
			#We need this delay to let user choose the split form. And	
			getExtrude_cs=None	#Dummy variable used to wait for the Extrude_cs be made
			while (getExtrude_cs==None):
				getExtrude_cs=App.ActiveDocument.getObject(totalName)
				_sleep(.1)
				Gui.updateGui() 
			### Begin command Part_Compound
			gcompund.Links = [getExtrude_cs,]		
					
			### Begin command Part_BooleanFragments
			j = SPLIT.makeBooleanFragments(name='BooleanFragments')
			j.Objects = [gcompund,App.ActiveDocument.getObject(nameOfselectedObject)]
			j.Mode = 'Standard'
			j.Proxy.execute(j)
			j.purgeTouched()
			App.ActiveDocument.recompute()
			
			#Make a simple copy
			newShape=Part.getShape(j,'',needSubElement=False,refine=False)
			NewJ=App.ActiveDocument.addObject('Part::Feature','SplitedObject').Shape=newShape
			
			#Remove Old objects
			for obj in j.Objects:
				App.ActiveDocument.removeObject(obj.Name)
			App.ActiveDocument.removeObject(totalName)
			App.ActiveDocument.removeObject(j.Name)
			
			App.ActiveDocument.recompute()
		except ImportError as err:
			App.Console.PrintError("'SplitObject' Failed. "
								   "{err}\n".format(err=str(err)))
			
	def GetResources(self):
		return{
			'Pixmap' :	Design456Init.ICON_PATH +  '/SplitObject.svg',
			'MenuText': 'Split Object',
			'ToolTip': 'Divide object in to two parts'
		}
Gui.addCommand('Design456_SplitObject', Design456_SplitObject()) 

