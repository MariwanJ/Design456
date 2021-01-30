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
from PySide import QtGui, QtCore 
import Draft
import Part
import FACE_D as Face


class Design456_Extrude:
	def __init__(self):
		return
	def Activated(self):
		Gui.activeDocument().activeView().viewIsometric()
		App.ActiveDocument.recompute()
		selection = Gui.Selection.getSelectionEx()
		m = App.activeDocument().getObject(selection[0].Object.Name)
		f = App.activeDocument().addObject('Part::Extrusion','Extrude')
		f.Base = App.activeDocument().getObject(m.Name)
		f.DirMode = "Normal" 
		f.DirLink = None
		#TODO: This if might not work always ? 
		if(m.Placement.Rotation.Axis.x==1):
			f.Base.MapMode='ObjectYZ'
		elif (m.Placement.Rotation.Axis.y==1):
			f.Base.MapMode='ObjectXZ'
		elif (m.Placement.Rotation.Axis.z==1):
			f.Base.MapMode='ObjectXY'
		
		f.LengthFwd = QtGui.QInputDialog.getDouble(None,"Get length","Input:")[0]
		f.LengthRev = 0.0
		f.Solid = True
		f.Reversed = False
		f.Symmetric = False
		f.TaperAngle = 0.0
		f.TaperAngleRev = 0.0
		#this part is not working .. don't know why
#		newShape=Part.getShape(f,'',needSubElement=False,refine=False)
#		newObj=App.ActiveDocument.addObject('Part::Feature','Extrude').Shape=newShape
#		App.ActiveDocument.recompute()
#		App.ActiveDocument.ActiveObject.Label=f.Label
#		App.ActiveDocument.recompute()
#		import time
#		import sleep
#		sleep(0.5)
#		App.ActiveDocument.removeObject(f.Name)
#		App.ActiveDocument.removeObject(m.Name)
		App.ActiveDocument.recompute()
		return

	def GuiViewFit(self):
		Gui.SendMsgToActiveView("ViewFit")
		self.timer.stop()

	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Extrude.svg',
				'MenuText': 'Extrude',
				'ToolTip':	'Extrude'
				}


class ActivateGrid():
	def Activated(self):
		my_grid = DraftTrackers.gridTracker()
		my_grid.set()
		my_grid.on()
		return
		
Gui.addCommand('Design456_Extrude', Design456_Extrude())
