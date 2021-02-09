#***************************************************************************
#*                                                                         *
#*  This file is part of the Open Source Design456 Workbench - FreeCAD.    *
#*                                                                         *
#*  Copyright (C) 2021                                                     *
#*																		   *
#*                                                                         *
#*  This library is free software; you can redistribute it and/or          *
#*  modify it under the terms of the GNU Lesser General Public             *
#*  License as published by the Free Software Foundation; either           *
#*  version 2 of the License, or (at your option) any later version.       *
#*                                                                         *
#*  This library is distributed in the hope that it will be useful,        *
#*  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
#*  Lesser General Public License for more details.                        *
#*                                                                         *
#*  You should have received a copy of the GNU Lesser General Public       *
#*  License along with this library; if not, If not, see                   *
#*  <http://www.gnu.org/licenses/>.                                        *
#*                                                                         *
#*  Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
#***************************************************************************
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import Design456Init 


from PySide import QtCore, QtGui

class Design456_Part_Tools:
	list= [ "Design456_Part_Merge" ,
			"Design456_Part_Subtract",
			"Design456_Part_Intersect",
			"Design456_Part_Group"
 
			] 
			   
	"""Design456 Part Tools Toolbar"""
	def GetResources(self):
		return{
				'Pixmap' :	 Design456Init.ICON_PATH +	'/Part_Tools.svg',
				'MenuText': 'Tools',
				'ToolTip':	'Tools'
			}
	
	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True
	
	"""Message box (error) """
	def errorDialog(self,msg):
		# Create a simple dialog QMessageBox
		# The first argument indicates the icon used: one of QtGui.QMessageBox.{NoIcon, Information, Warning, Critical, Question} 
		diag = QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Tools ', self.msg)
		diag.setWindowModality(QtCore.Qt.ApplicationModal)
		diag.exec_()
	 
	def Activated(self):
		self.appendToolbar("Design456_Part_Tools", self.list)
		


# Merge
class Design456_Part_Merge:
		
	def Activated(self):
		try:
			s = Gui.Selection.getSelectionEx()
			temp=None
			if (len(s)<2) :
				#Two object must be selected
				errMessage= "Select two or more objects to Merge"
				self.errorDialog(errMessage)
				return
			allObjects=[]
			for o in s:
				allObjects.append(App.ActiveDocument.getObject(o.ObjectName))
				
			newObj=App.activeDocument().addObject("Part::MultiFuse","MergedTemp")
			newObj.Shapes = allObjects 
			App.ActiveDocument.recompute()
			newObj.Refine=True
			App.ActiveDocument.recompute()
			#Make a simple copy
			newShape=Part.getShape(newObj,'',needSubElement=False,refine=False)
			NewJ=App.ActiveDocument.addObject('Part::Feature','Merged').Shape=newShape
			App.ActiveDocument.recompute()

			#Remove Old objects
			for obj in allObjects:
				App.ActiveDocument.removeObject(obj.Name)
			App.ActiveDocument.removeObject(newObj.Name)
			App.ActiveDocument.recompute()
		except ImportError as err:
			App.Console.PrintError("'Part::Merge' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Merge.svg',
				'MenuText': 'Part_Merge',
				'ToolTip':	'Part Merge'
				}
Gui.addCommand('Design456_Part_Merge', Design456_Part_Merge())						


# Subtract
class Design456_Part_Subtract:
		
	def Activated(self):
		try:
			s = Gui.Selection.getSelectionEx()
			temp=None
			if (len(s)<2) :
				#Two object must be selected
				errMessage= "Select two or more objects to Subtract"
				self.errorDialog(errMessage)
				return
			newObj=App.activeDocument().addObject("Part::Cut","Subtract")
			newObj.Base =App.ActiveDocument.getObject(s[0].ObjectName) # Target
			newObj.Tool =App.ActiveDocument.getObject(s[1].ObjectName) # Subtracted shape/object
			App.ActiveDocument.recompute()
			newObj.Refine=True
			App.ActiveDocument.recompute()
						#Make a simple copy
			newShape=Part.getShape(newObj,'',needSubElement=False,refine=False)
			NewJ=App.ActiveDocument.addObject('Part::Feature','Subtract').Shape=newShape
			App.ActiveDocument.recompute()
			#Remove Old objects
			allObjects=[]
			for o in s:
				allObjects.append(App.ActiveDocument.getObject(o.ObjectName))
			for obj in allObjects:
				App.ActiveDocument.removeObject(obj.Name)
			App.ActiveDocument.removeObject(newObj.Name)
			App.ActiveDocument.recompute()
		except ImportError as err:
			App.Console.PrintError("'Part::Subtract' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Subtract.svg',
				'MenuText': 'Part_Subtract',
				'ToolTip':	'Part Subtract'
				}
Gui.addCommand('Design456_Part_Subtract', Design456_Part_Subtract())						


# Intersect
class Design456_Part_Intersect:
		
	def Activated(self):
		try:
			s = Gui.Selection.getSelectionEx()
			temp=None
			if (len(s)<2) :
				#Two object must be selected
				errMessage= "Select two or more objects to Intersect"
				self.errorDialog(errMessage)
				return
			newObj=App.activeDocument().addObject("Part::MultiCommon","tempIntersect")
			newObj.Shapes=[App.ActiveDocument.getObject(s[0].ObjectName),App.ActiveDocument.getObject(s[1].ObjectName)]
			App.ActiveDocument.recompute()
						#Make a simple copy
			newShape=Part.getShape(newObj,'',needSubElement=False,refine=False)
			NewJ=App.ActiveDocument.addObject('Part::Feature','Intersect').Shape=newShape
			App.ActiveDocument.recompute()
			#Remove Old objects
			allObjects=[]
			for o in s:
				allObjects.append(App.ActiveDocument.getObject(o.ObjectName))
			for obj in allObjects:
				App.ActiveDocument.removeObject(obj.Name)
			App.ActiveDocument.removeObject(newObj.Name)
			App.ActiveDocument.recompute()
		except ImportError as err:
			App.Console.PrintError("'Part::Intersect' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Intersect.svg',
				'MenuText': 'Part_Intersect',
				'ToolTip':	'Part Intersect'
				}
Gui.addCommand('Design456_Part_Intersect', Design456_Part_Intersect())						
# Group
class Design456_Part_Group:
		
	def Activated(self):
		try:
			s = Gui.Selection.getSelectionEx()
			temp=None
			if (len(s)<2) :
				#Two object must be selected
				errMessage= "Select two or more objects to create a group"
				self.errorDialog(errMessage)
				return

			newObj= App.activeDocument().Tip = App.activeDocument().addObject('App::Part','Group')
			newObj.Label = 'Group'
			for obj_ in s:
				obj= App.ActiveDocument.getObject(obj_.ObjectName)
				newObj.addObject(obj)

			App.ActiveDocument.recompute()
		except ImportError as err:
			App.Console.PrintError("'Part::Part' Failed. "
								   "{err}\n".format(err=str(err)))
	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Part_Group.svg',
				'MenuText': 'Part_Group',
				'ToolTip':	'Part Group'
				}
Gui.addCommand('Design456_Part_Group', Design456_Part_Group())						
