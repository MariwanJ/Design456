#***************************************************************************
#*																		   *
#*	Open source - FreeCAD												   *
#*	Design456 Workbench													   *
#*	Auth : Mariwan Jalal and others										   *
#***************************************************************************

class Design456_Workbench (Workbench):
	"Design456 Workbench object"
	def __init__(self):
		import Design456Init
		self.__class__.Icon = Design456Init.ICON_PATH + '/WorkbenchIcon.svg'
		self.__class__.MenuText = "Design456"
		self.__class__.ToolTip = "A workbench easy designing objects"

	def Initialize(self):
		"This function is executed when FreeCAD starts"
		import	Design456_Extrude  # import all	 needed files
		import	Design456_Extract  
		import	Design456_ExtrudeFace
		import	Design456_SplitObject
		import	Design456_Move
		self.list = [ "Design456_Extrude" , 
					   "Design456_Extract", 
					   "Design456_ExtrudeFace" ,
					   "Design456_SplitObject",
					   "Design456_Move"
					]
		self.appendToolbar("Design456", self.list)
		self.appendMenu("Design456 Menu", self.list) #TODO : Might be wrong or it is wrong :(
	
	def Activated(self):
		if not(FreeCAD.ActiveDocument):
			FreeCAD.newDocument()

		FreeCAD.Console.PrintMessage('Design456 workbench loaded\n')
		return

	def Deactivated(self):
		"workbench deactivated"
		return

	def ContextMenu(self, recipient):
		"right-clicks on screen"
		self.appendContextMenu("Design456 commands", self.list)

	def GetClassName(self): 
		return "Gui::PythonWorkbench"
	   
Gui.addWorkbench(Design456_Workbench())
