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

	
# Cone
class Design456_Part_Torus:
		
	def Activated(self):
		try:
			App.ActiveDocument.addObject("Part::Torus","Torus")
			App.ActiveDocument.ActiveObject.Label = "Torus"
			App.ActiveDocument.recompute()
			#Gui.SendMsgToActiveView("ViewFit")
		except ImportError as err:
			App.Console.PrintError("'Part::Torus' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Torus.svg',
				'MenuText': 'Part_Torus',
				'ToolTip':	'Part Torus'
				}
Gui.addCommand('Design456_Part_Torus', Design456_Part_Torus())

# Wedge
class Design456_Part_Wedge:
		
	def Activated(self):
		try:
			App.ActiveDocument.addObject("Part::Wedge","Wedge")
			App.ActiveDocument.ActiveObject.Label = "Wedge"
			App.ActiveDocument.recompute()
			#Gui.SendMsgToActiveView("ViewFit")
		except ImportError as err:
			App.Console.PrintError("'Part::Wedge' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Wedge.svg',
				'MenuText': 'Part_Wedge',
				'ToolTip':	'Part Wedge'
				}
Gui.addCommand('Design456_Part_Wedge', Design456_Part_Wedge())


# Prism
class Design456_Part_Prism:
		
	def Activated(self):
		try:
			App.ActiveDocument.addObject("Part::Prism","Prism")
			App.ActiveDocument.ActiveObject.Label = "Prism"
			App.ActiveDocument.recompute()
			#Gui.SendMsgToActiveView("ViewFit")
		except ImportError as err:
			App.Console.PrintError("'Part::Prism' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Prism.svg',
				'MenuText': 'Part_Prism',
				'ToolTip':	'Part Prism'
				}
Gui.addCommand('Design456_Part_Prism', Design456_Part_Prism())


# Pyramid
class Design456_Part_Pyramid:
		
	def Activated(self):
		try:
			App.ActiveDocument.addObject("Part::Pyramid","Pyramid")
			App.ActiveDocument.ActiveObject.Label = "Pyramid"
			App.ActiveDocument.recompute()
			#Gui.SendMsgToActiveView("ViewFit")
		except ImportError as err:
			App.Console.PrintError("'Part::Pyramid' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Pyramid.svg',
				'MenuText': 'Part_Pyramid',
				'ToolTip':	'Part Pyramid'
				}
Gui.addCommand('Design456_Part_Pyramid', Design456_Part_Pyramid())


# Hemisphere
class Design456_Part_Hemisphere:
		
	def Activated(self):
		try:
			App.ActiveDocument.addObject("Part::Hemisphere","Hemisphere")
			App.ActiveDocument.ActiveObject.Label = "Hemisphere"
			App.ActiveDocument.recompute()
			#Gui.SendMsgToActiveView("ViewFit")
		except ImportError as err:
			App.Console.PrintError("'Part::Hemisphere' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Hemisphere.svg',
				'MenuText': 'Part_Hemisphere',
				'ToolTip':	'Part Hemisphere'
				}
Gui.addCommand('Design456_Part_Hemisphere', Design456_Part_Hemisphere())

# Ellipsoid
class Design456_Part_Ellipsoid:
		
	def Activated(self):
		try:
			App.ActiveDocument.addObject("Part::Ellipsoid","Ellipsoid")
			App.ActiveDocument.ActiveObject.Label = "Ellipsoid"
			App.ActiveDocument.recompute()
			#Gui.SendMsgToActiveView("ViewFit")
		except ImportError as err:
			App.Console.PrintError("'Part::Ellipsoid' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Ellipsoid.svg',
				'MenuText': 'Part_Ellipsoid',
				'ToolTip':	'Part Ellipsoid'
				}
Gui.addCommand('Design456_Part_Ellipsoid', Design456_Part_Ellipsoid())