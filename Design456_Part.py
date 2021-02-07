#***************************************************************************
#*																		   *
#*	Open source - FreeCAD												   *
#*	Design456 Part													   *
#*	Auth : Mariwan Jalal and others										   *
#***************************************************************************
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import Design456Init 
#from Part import CommandShapes  #Tube   not working


class Design456_Part_ToolBar:
	list= [ "Design456_Part_Box" ,
			"Design456_Part_Cylinder" ,
			"Design456_Part_Tube" ,
			"Design456_Part_Sphere" ,	
			"Design456_Part_Cone" ,	
			"Design456_Part_Torus" ,	
			"Design456_Part_Wedge" ,	
			"Design456_Part_Prism" ,	
			"Design456_Part_Pyramid" ,	
			"Design456_Part_Hemisphere" ,
			"Design456_Part_Ellipsoid" 
			] 
			   
	"""Design456 Part Toolbar"""
	def GetResources(self):
		return{
				'Pixmap' :	Design456Init.ICON_PATH +  '/Part_Box.svg',
				'MenuText': 'Box',
				'ToolTip': 'Box'
			}
	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True
    
	def Activated(self):
		self.appendToolbar("Design456_Part_ToolBar", self.list)
		


# BOX
class Design456_Part_Box:
		
	def Activated(self):
		try:
			App.ActiveDocument.addObject("Part::Box","Box")
			App.ActiveDocument.ActiveObject.Label = "Cube"
			App.ActiveDocument.recompute()
			#Gui.SendMsgToActiveView("ViewFit")
		except ImportError as err:
			App.Console.PrintError("'Part::Box' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Box.svg',
				'MenuText': 'Part_Box',
				'ToolTip':	'Part Box'
				}
Gui.addCommand('Design456_Part_Box', Design456_Part_Box())						

#Cylinder
class Design456_Part_Cylinder:
		
	def Activated(self):
		try:
			App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
			App.ActiveDocument.ActiveObject.Label = "Cylinder"
			App.ActiveDocument.recompute()
			#Gui.SendMsgToActiveView("ViewFit")
		except ImportError as err:
			App.Console.PrintError("'Part::Cylinder' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Cylinder.svg',
				'MenuText': 'Part_Cylinder',
				'ToolTip':	'Part Cylinder'
				}
Gui.addCommand('Design456_Part_Cylinder', Design456_Part_Cylinder())


#Tube
class Design456_Part_Tube:
		
	def Activated(self):
		try:
			
			Gui.runCommand('Part_Tube',0)
			App.ActiveDocument.recompute()
			#Gui.SendMsgToActiveView("ViewFit")
		except ImportError as err:
			App.Console.PrintError("'Part::Tube' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Tube.svg',
				'MenuText': 'Part_Tube',
				'ToolTip':	'Part Tube'
				}
Gui.addCommand('Design456_Part_Tube', Design456_Part_Tube())


# Shpere
class Design456_Part_Sphere:
		
	def Activated(self):
		try:
			App.ActiveDocument.addObject("Part::Sphere","Sphere")
			App.ActiveDocument.ActiveObject.Label = "Sphere"
			App.ActiveDocument.recompute()
			#Gui.SendMsgToActiveView("ViewFit")
		except ImportError as err:
			App.Console.PrintError("'Part::Sphere' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Sphere.svg',
				'MenuText': 'Part_Sphere',
				'ToolTip':	'Part Sphere'
				}
Gui.addCommand('Design456_Part_Sphere', Design456_Part_Sphere())
# Cone
class Design456_Part_Cone:
		
	def Activated(self):
		try:
			App.ActiveDocument.addObject("Part::Cone","Cone")
			App.ActiveDocument.ActiveObject.Label = "Cone"
			App.ActiveDocument.recompute()
			#Gui.SendMsgToActiveView("ViewFit")
		except ImportError as err:
			App.Console.PrintError("'Part::Cone' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Cone.svg',
				'MenuText': 'Part_Cone',
				'ToolTip':	'Part Cone'
				}
Gui.addCommand('Design456_Part_Cone', Design456_Part_Cone())