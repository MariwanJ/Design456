
#print ("nurbs configuration file loaded")


# meta data for the actions
modes={}

import FreeCAD as App

from PySide import QtGui



class MyWidget(QtGui.QLineEdit):

	def __init__(self, text, path):

		QtGui.QLineEdit.__init__(self)
		self.setText(text)
		self.path=path
		self.path="BaseApp/Preferences/Mod/nurbswb/editor"
		self.name="MyTestparam"
		self.textChanged.connect(self.ttChanged)

	def ttChanged(self,arg):
		print ("!!", self)
		print (self.path)
		print ("testprocessor")
		print (arg)
		print (self.text())
		
	def loadA(self):
		group = App.ParamGet("User parameter:"+self.path)
		rc=group.GetString(self.name)
		self.setText(rc)

	def save(self):
		group = App.ParamGet("User parameter:"+self.path)
		group.SetString(self.name, self.text())

if 0:
	w=MyWidget("AAA","BBB")
	w.show()
	w.setText("TT")
	w.save()
	w.setText("huhu")
	w.loadA()


path="BaseApp/Preferences/Mod/nurbswb/editor"

def setcf(name,value):
	group = App.ParamGet("User parameter:"+path)
	group.SetFloat(name, value)

def getcf(name):
	group = App.ParamGet("User parameter:"+path)
	return group.GetFloat(name)

def setcs(name,value):
	group = App.ParamGet("User parameter:"+path)
	group.SetString(name, value)

def getcs(name):
	group = App.ParamGet("User parameter:"+path)
	return group.GetString(name)
	

def setcb(name,value):
	group = App.ParamGet("User parameter:"+path)
	group.SetBool(name, value)

def getcb(name):
	group = App.ParamGet("User parameter:"+path)
	return group.GetBool(name)


def initialize():
	pass

setcb("mikidebug",False)



