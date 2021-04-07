# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- skletcher structures, regulkar grid ...
#--
#-- microelly 2017 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


# from say import *
# import nurbswb.pyob
#------------------------------
import FreeCAD as App
import FreeCADGui as Gui
,Sketcher,Part

App = FreeCAD
Gui = FreeCADGui

import numpy as np
import time


class FeaturePython:
	''' basic defs'''

	def __init__(self, obj):
		obj.Proxy = self
		self.Object = obj

	def attach(self, vobj):
		self.Object = vobj.Object

	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self, state):
		return None


class ViewProvider:
	''' basic defs '''

	def __init__(self, obj):
		obj.Proxy = self
		self.Object = obj

	def __getstate__(self):
		return None

	def __setstate__(self, state):
		return None

#-------------------------------



def creategrid(uc=3,vc=5,sk=None):
	if sk==None:
		sk=App.activeDocument().addObject('Sketcher::SketchObject','Sketch')

# sketche grid generator

	print ("create grid ..."
	gct=sk.GeometryCount
	for i in range(gct):
		sk.delGeometry(gct-i-1)


	for u in range(uc+1):
		for v in range(vc):
			_=sk.addGeometry(Part.LineSegment(App.Vector(v*10,u*10,0),App.Vector((v+1)*10,u*10,0)),False)
			

	for v in range(vc+1):
		for u in range(uc):
			_=sk.addGeometry(Part.LineSegment(App.Vector(v*10,u*10,0),App.Vector(v*10,(u+1)*10,0)),False)



#	App.activeDocument().recompute()


	def getedges(a,b):
		return [(b-1)*vc+(a-1),b*vc+(a-1),vc*(uc+1)+(b-1)+ uc*(a-1),vc*(uc+1)+(b-1)+ uc*a]


	def zz(a,b,uc,vc):
		les=getedges(a,b)
	#	for e in les: 
	#		sk.setConstruction(e,True)

		l=les
		#print l
		_=sk.addConstraint(Sketcher.Constraint('Coincident',l[0],1,l[2],1)) 
		if a!=vc:
			_=sk.addConstraint(Sketcher.Constraint('Coincident',l[0],2,l[0]+1,1)) 
		if b!=uc:
			_=sk.addConstraint(Sketcher.Constraint('Coincident',l[2],2,l[2]+1,1)) 
		if a == vc:
			_=sk.addConstraint(Sketcher.Constraint('Coincident',l[0],2,l[3],1))
			if b!= uc:
				_=sk.addConstraint(Sketcher.Constraint('Coincident',l[3],2,l[3]+1,1)) 
		if b == uc:
			_=sk.addConstraint(Sketcher.Constraint('Coincident',l[2],2,l[1],1)) 
			_=sk.addConstraint(Sketcher.Constraint('Coincident',l[3],2,l[1],2)) 

		#App.activeDocument().recompute()



	for a in range(1,vc+1):
		for b in range(1,uc+1):
			zz(a,b,uc,vc)
	
	sk.solve()





class GridSketch(FeaturePython):
	'''Sketch Object with Python''' 

	##\cond
	def __init__(self, obj, icon='/home/thomas/.FreeCAD/Mod/freecad-nurbs/icons/draw.svg'):
		obj.Proxy = self
		self.Type = self.__class__.__name__
		self.obj2 = obj
		obj.addProperty("App::PropertyBool",'stopExecute', 'Base',"")
		obj.addProperty("App::PropertyInteger",'columns', 'Base',"")
		obj.addProperty("App::PropertyInteger",'rows', 'Base',"")
		obj.rows=3
		obj.columns=5
		ViewProvider(obj.ViewObject)
	##\endcond

#	def onChanged(proxy,obj,prop):
#		'''run myExecute for property prop: relativePosition and vertexNumber'''
#		print ("changed",prop)
#		if prop in ["parent"]: 
#			proxy.myExecute(obj)



	def execute(self,obj):

#		if obj.error:
#				obj.error=False
#				raise Exception("Obj -- Error")


		obj.recompute() 
		try: self.Lock
		except: self.Lock=False
		if not self.Lock:
			self.Lock=True
			try:
				#print ("run myexecute"
				self.myExecute(obj)
				#print ("myexecute done"
			except Exception as ex:
				print(ex)
				print('myExecute error')
#				sayexc("myExecute Error")
				self.Lock=False
				raise Exception("myExecute Error AA")
			self.Lock=False


##\cond
	def myExecute(self, obj):
		if not obj.stopExecute:
			creategrid(obj.columns,obj.rows,obj)
			obj.recompute() 
##\endcond




def createGridSketch(name="MyGridSketch"):
	obj = App.ActiveDocument.addObject("Sketcher::SketchObjectPython",name)
	GridSketch(obj)
	App.ActiveDocument.recompute()
	return obj


# createGridSketch()



