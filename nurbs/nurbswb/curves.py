'''OffsetSpline and Star'''

'''
SketcherObjectPython example oo
for Offset curve generation
<A HREF="http://www.freecadbuch.de/doku.php?id=blog">FreeCAD Buch</A>

''' 


# <A HREF="http://www.freecadbuch.de/doku.php?id=blog">FreeCAD Buch 2</A> 
# Author  microelly
# Warning huhuwas
# weiter


#http://free-cad.sourceforge.net/SrcDocu/dc/d77/classSketcher_1_1SketchObjectPy.html
#https://forum.freecadweb.org/viewtopic.php?t=6121
#https://forum.freecadweb.org/viewtopic.php?t=12829



#pylint: disable=W0312,W0232,R0903

from say import *
import nurbswb.pyob

##\cond


class _ViewProvider(nurbswb.pyob.ViewProvider):
	''' base class view provider '''

	def __init__(self, vobj, icon='/icons/mover.png'):
		self.Object = vobj.Object
		self.iconpath =  icon
		vobj.Proxy = self

	def getIcon(self):
		return '/home/thomas/.FreeCAD/Mod/freecad-nurbs/icons/draw.svg'

##\endcond

## Two Offset curves for a Bspline defined by a Sketcher interpolation polygon

class OffsetSpline(nurbswb.pyob.FeaturePython):
	'''Sketch Object with Python''' 

	##\cond
	def __init__(self, obj, icon='/home/thomas/.FreeCAD/Mod/freecad-nurbs/icons/draw.svg'):
		obj.Proxy = self
		self.Type = self.__class__.__name__
		self.obj2 = obj
		self.aa = None
		_ViewProvider(obj.ViewObject, icon) 

	##\endcond

	def onChanged(proxy,obj,prop):
		'''run myExecute for property prop: "ofin" and "ofout"'''
		if prop not in ["ofin","ofout"]: return 
		proxy.myExecute(obj)





	def myExecute(proxy,obj):
		''' creates a closed BSpline that interpolates the vertexes chain of the sketch
		and two offset curves in- and outside'''
		vs=obj.Shape.Vertexes
		if len(vs)==0: return

		pts=[p.Point for p in vs]
		pts.append(pts[0])

		bc=Part.BSplineCurve()
		bc.interpolate(pts)
		bc.setPeriodic()
		
		name=obj.Name

		fa=App.ActiveDocument.getObject(name+"_spline")
		if fa==None:
			fa=App.ActiveDocument.addObject('Part::Spline',name+"_spline")
		
		fa.Shape=bc.toShape()
		fa.ViewObject.LineColor=(.0,1.0,.0)

		if obj.ofout!=0:
			ofs=App.ActiveDocument.getObject(name+"_offOut")
			if ofs==None: ofs=App.ActiveDocument.addObject("Part::Offset2D",name+"_offOut")
			ofs.Source = fa
			ofs.ViewObject.LineColor=(.0,0.0,1.0)
			ofs.Value = obj.ofout
			ofs.recompute()

		if obj.ofin!=0:
			ofsi=App.ActiveDocument.getObject(name+"_offIn")
			if ofsi==None: ofsi=App.ActiveDocument.addObject("Part::Offset2D",name+"_offIn")
			ofsi.Source = fa
			ofsi.ViewObject.LineColor=(1.0,0.0,.0)
			ofsi.Value = -obj.ofin
			ofsi.recompute()


##\cond
	def execute(self, obj):
		''' recompute sketch and than run postprocess: myExecute'''
		obj.recompute()
		self.myExecute(obj)
##\endcond


#---------------------
class Ufo(nurbswb.pyob.FeaturePython):
	'''a mirgrationtest class''' 

	##\cond
	def __init__(self, obj, icon='/home/thomas/.FreeCAD/Mod/freecad-nurbs/icons/draw.svg'):
		obj.Proxy = self
		self.Type = self.__class__.__name__
		self.obj2 = obj
		self.aa = None
		_ViewProvider(obj.ViewObject, icon) 

	##\endcond

	def onChanged(proxy,obj,prop):
		print ("ufo changed")
		return
#		'''run myExecute for property prop: "ofin" and "ofout"'''
#		if prop not in ["ofin","ofout"]: return
#		proxy.myExecute(obj)


	def myExecute(proxy,obj):
		print ("ufo my execute "
		return
		#	ofsi.recompute()


##\cond
	def execute(self, obj):
		''' recompute sketch and than run postprocess: myExecute'''
		obj.recompute()
		self.myExecute(obj)
##\endcond





#----------------------


def runOffsetSpline(name="MyOffSp"):
	'''run(name="Sole with borders"): a demo skript
		the demo script creates an empty  Sketch Python Object and sets
		the border distances for the offset curves to 10
		@ Author anton
	'''



	obj = App.ActiveDocument.addObject("Sketcher::SketchObjectPython",name)
	obj.addProperty("App::PropertyInteger", "ofin", "Base", "end").ofin=10
	obj.addProperty("App::PropertyInteger", "ofout", "Base", "end").ofout=10

	OffsetSpline(obj)

	obj.ofin=10
	obj.ofout=10

	App.activeDocument().recompute()
	return obj


#
#
# 
#


import numpy as np

# finde Kanten


def dirs(obj,vn):
	'''find directions of the edges in a shape obj.Shape
	at vertex number vn
	'''

	print ("dirs",obj.Label)
	p=obj.Shape.Vertexes[vn].Point
	rc=[]
	for e in obj.Shape.Edges:
		if e.Vertexes[0].Point == p:
			t=e.tangentAt(0)
			dire=np.arctan2(t.y,t.x)
			print ("startpoint", dire *180.0/np.pi)
			rc.append(np.pi+dire)
		if len(e.Vertexes)>1 and  e.Vertexes[1].Point == p:
			t=e.tangentAt(1)
			dire=np.arctan2(t.y,t.x)
			print ("endpoint", dire *180.0/np.pi)
			rc.append(dire)

	return rc

#obj=App.ActiveDocument.MyStar
#rc=dirs(obj,2)

#print rc
import time

## A (topological) 2D tree with special connecting methods to combine trees to larger tree

class Star(nurbswb.pyob.FeaturePython):
	'''Sketch Object with Python''' 

	##\cond
	def __init__(self, obj, icon='/home/thomas/.FreeCAD/Mod/freecad-nurbs/icons/draw.svg'):
		obj.Proxy = self
		self.Type = self.__class__.__name__
		self.obj2 = obj
		self.aa = None
		_ViewProvider(obj.ViewObject, icon) 

	##\endcond

	def onChanged(proxy,obj,prop):
		'''run myExecute for property prop: relativePosition and vertexNumber'''

		if prop in ["parent","relativePosition","VertexNumber","tangentCond","tangentInverse","tangentCond"]: 
			proxy.myExecute(obj)


	def myExecute(proxy,obj):
		''' position to parent'''

		print ("myExecute",time.time())

		if obj.parent == None: return

		relpos=App.Placement(obj.relativePosition)
		
		if obj.tangentCond !=0 and obj.VertexNumber != 0:
			rc=dirs(obj.parent,obj.VertexNumber-1)
			
			if obj.tangentCond > len(rc): obj.tangentCond =len(rc)
			if obj.tangentCond < 0: obj.tangentCond = 0

			print ("genutzer Winkel ", rc[obj.tangentCond-1] *180/np.pi
			if obj.tangentInverse:
				relpos.Rotation.Angle += np.pi + rc[obj.tangentCond-1]
			else:
				relpos.Rotation.Angle += rc[obj.tangentCond-1]


		if obj.VertexNumber==0:
			pos=obj.parent.Placement
		else:
			pos=App.Placement(obj.parent.Shape.Vertexes[obj.VertexNumber-1].Point,App.Rotation())

		obj.Placement=pos.multiply(relpos)


##\cond
	def execute(self, obj):
		''' recompute sketch and than run postprocess: myExecute'''
		obj.recompute()
		self.myExecute(obj)
##\endcond


import Sketcher

def runStar(name="MyStar"):
	'''runStar(name="Sole with borders"): 
		creates a Star/Tree with 5 lines (3 leafs)
	'''


	obj = App.ActiveDocument.addObject("Sketcher::SketchObjectPython",name)
	obj.addProperty("App::PropertyInteger", "VertexNumber", "Parent", ).VertexNumber=0
	obj.addProperty("App::PropertyInteger", "tangentCond", "Parent", )
	obj.addProperty("App::PropertyBool", "tangentInverse", "Parent", )
	obj.addProperty("App::PropertyLink", "parent", "Parent", )
	obj.addProperty("App::PropertyPlacement", "relativePosition", "Parent", )

	# add some data
	obj.addGeometry(Part.LineSegment(App.Vector(0.000000,0.000000,0),App.Vector(100.,0.,0)),False)
	obj.addConstraint(Sketcher.Constraint('Coincident',-1,1,0,1)) 
	App.ActiveDocument.recompute()
	App.ActiveDocument.recompute()

	obj.addGeometry(Part.LineSegment(App.Vector(100.,0,0),App.Vector(200.,100.,0)),False)
	obj.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
	App.ActiveDocument.recompute()
	App.ActiveDocument.recompute()

	obj.addGeometry(Part.LineSegment(App.Vector(200.,100.,0),App.Vector(200.,200.,0)),False)
	obj.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
	App.ActiveDocument.recompute()
	App.ActiveDocument.recompute()


	obj.addGeometry(Part.LineSegment(App.Vector(100.,0,0),App.Vector(200.,-200.,0)),False)
	obj.addConstraint(Sketcher.Constraint('Coincident',0,2,3,1)) 
	App.ActiveDocument.recompute()
	App.ActiveDocument.recompute()

	obj.addGeometry(Part.LineSegment(App.Vector(200.,-200.,0),App.Vector(40.,-300.,0)),False)
	obj.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
	App.ActiveDocument.recompute()
	App.ActiveDocument.recompute()

	Star(obj)
	obj.ViewObject.LineColor=(0.5*random.random(),0.5*random.random(),0.5*random.random())
	obj.ViewObject.PointColor=(1.0,0.,0.)
	obj.ViewObject.PointSize=8
	obj.ViewObject.LineWidth=4
	
	obj.addGeometry(Part.Circle(App.Vector(0.0,0.00,0),App.Vector(0,0,1),20),False)
	obj.addConstraint(Sketcher.Constraint('Coincident',5,3,-1,1)) 
	App.ActiveDocument.recompute()
	App.ActiveDocument.recompute()
	App.activeDocument().recompute()
	
	obj.VertexNumber=3
	#obj.parent=App.ActiveDocument.getObject('MyStar')

	return obj


## \cond
if __name__=='__main__':
	star=runStar()
	star2=runStar()
	star2.parent=star
	star2.VertexNumber=2
	star2.relativePosition.Rotation.Angle=-1.2
	App.activeDocument().recompute()


#\endcond
