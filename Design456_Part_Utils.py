# ***************************************************************************
# *                                                                         *
# *  This file is part of the Open Source Design456 Workbench - FreeCAD.    *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *																		   *
# *                                                                         *
# *  This library is free software; you can redistribute it and/or          *
# *  modify it under the terms of the GNU Lesser General Public             *
# *  License as published by the Free Software Foundation; either           *
# *  version 2 of the License, or (at your option) any later version.       *
# *                                                                         *
# *  This library is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# *  Lesser General Public License for more details.                        *
# *                                                                         *
# *  You should have received a copy of the GNU Lesser General Public       *
# *  License along with this library; if not, If not, see                   *
# *  <http://www.gnu.org/licenses/>.                                        *
# *                                                                         *
# *  Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# ***************************************************************************
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import Design456Init


from PySide import QtCore, QtGui
"""
class Design456_Part_Template:
	list= [ "Design456_Part_Merge" و
			] 
			   
	"""Design456 Part Template Toolbar"""
	def GetResources(self):
		return{
				'Pixmap' :	 Design456Init.ICON_PATH +	'/Part_Template.svg',
				'MenuText': 'Template',
				'ToolTip':	'Template'
			}
	
	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True
			
	"""Message box(error) """
	def errorDialog(self,msg):
		# Create a simple dialog QMessageBox
		# The first argument indicates the icon used: one of QtGui.QMessageBox.{NoIcon, Information, Warning, Critical, Question} 
		diag = QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Template ', self.msg)
		diag.setWindowModality(QtCore.Qt.ApplicationModal)
		diag.exec_()
	 
	def Activated(self):
		self.appendToolbar("Design456_Part_Template", self.list)
		


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
						#Make a simple copy
			newShape=Part.getShape(newObj,'',needSubElement=False,refine=False)
			NewJ=App.ActiveDocument.addObject('Part::Feature','Merged').Shape=newShape
			
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
"""
