'''shoe sole object'''

from say import *
import Sketcher


def createsole(sk):
	'''create the basic geometry sketch for a sole with 12 segments'''
	LL=sk.LL

	lls=[]
	for p in range(11):
		ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,0,0),App.Vector(10*p+10,0,0)),False)
		sk.toggleConstruction(ll) 
		sk.addConstraint(Sketcher.Constraint('Horizontal',ll)) 
		print ll
		if ll>0:
			sk.addConstraint(Sketcher.Constraint('Coincident',ll-1,2,ll,1)) 
			sk.addConstraint(Sketcher.Constraint('Equal',0,ll)) 
		llast=ll
	sk.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1)) 

	#for p in range(1,12):
	for p in range(0,11):
		ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,0,0),App.Vector(10*p,20,0)),False)
		sk.toggleConstruction(ll) 
		sk.addConstraint(Sketcher.Constraint('Vertical',ll)) 
		sk.addConstraint(Sketcher.Constraint('Coincident',p,1,ll,1)) 

	p=11
	ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,0,0),App.Vector(10*p,20,0)),False)
#	sk.toggleConstruction(ll) 
	sk.addConstraint(Sketcher.Constraint('Vertical',ll)) 
	sk.addConstraint(Sketcher.Constraint('Coincident',llast,2,ll,1)) 


	#for p in range(1,12):
	for p in range(0,11):
		ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,0,0),App.Vector(10*p,-20,0)),False)
		sk.toggleConstruction(ll) 
		sk.addConstraint(Sketcher.Constraint('Vertical',ll)) 
		sk.addConstraint(Sketcher.Constraint('Coincident',p,1,ll,1)) 

	p=11
	ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,0,0),App.Vector(10*p,-20,0)),False)
#	sk.toggleConstruction(ll) 
	sk.addConstraint(Sketcher.Constraint('Vertical',ll)) 
	sk.addConstraint(Sketcher.Constraint('Coincident',llast,2,ll,1)) 


	cLL=sk.addConstraint(Sketcher.Constraint('DistanceX',10,2,LL)) 
	# App.ActiveDocument.sohle.renameConstraint(cLL, u'LL')

	for p in range(11):
		print p
		p=10-p
		#	if p<>12:
		#ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,-40.,0),App.Vector(10*p+10,-40.,0)),False)
		ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p+10,-40.,0),App.Vector(10*p+0,-40.,0)),False)
		sk.addConstraint(Sketcher.Constraint('Coincident',23+p,2,ll,1)) 
		sk.addConstraint(Sketcher.Constraint('Coincident',24+p,2,ll,2)) 
#			else:
#				ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,-50.,0),App.Vector(10*p+10,-50.,0)),False)
#				sk.addConstraint(Sketcher.Constraint('Coincident',23+p,2,ll,1)) 
#				sk.addConstraint(Sketcher.Constraint('Coincident',11,2,ll,2)) 



	for p in range(11):
			print p
			ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,40.,0),App.Vector(10*p+10,40.,0)),False)
			sk.addConstraint(Sketcher.Constraint('Coincident',11+p,2,ll,1)) 
			sk.addConstraint(Sketcher.Constraint('Coincident',12+p,2,ll,2)) 

#			else:
#				ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,50.,0),App.Vector(10*p+10,50.,0)),False)
#				sk.addConstraint(Sketcher.Constraint('Coincident',12+p,2,ll,1)) 
#				sk.addConstraint(Sketcher.Constraint('Coincident',11,2,ll,2)) 

	if 0:


		if 1:
				ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,-50.,0),App.Vector(10*p+10,-50.,0)),False)
				sk.addConstraint(Sketcher.Constraint('Coincident',0,1,ll,1)) 
				sk.addConstraint(Sketcher.Constraint('Coincident',23,2,ll,2)) 

				ll=sk.addGeometry(Part.LineSegment(App.Vector(10*p,-50.,0),App.Vector(10*p+10,-50.,0)),False)
				sk.addConstraint(Sketcher.Constraint('Coincident',0,1,ll,1)) 
				sk.addConstraint(Sketcher.Constraint('Coincident',12,2,ll,2)) 

	App.ActiveDocument.recompute()


import nurbswb.curves
reload(nurbswb.curves)



class Sole(nurbswb.curves.OffsetSpline):
	'''Shoe sole as Sketch Object with Python''' 

	##\cond
	def __init__(self, obj, icon='/home/thomas/.FreeCAD/Mod/freecad-nurbs/icons/draw.svg'):
		nurbswb.curves.OffsetSpline.__init__(self, obj, icon='/home/thomas/.FreeCAD/Mod/freecad-nurbs/icons/draw.svg')
		obj.Proxy = self
		self.Type = self.__class__.__name__
		self.obj2 = obj
		self.aa = None
	##\endcond

	def onChanged(proxy,obj,prop):
		'''change on lastlength, inner and outer offset'''  
		if prop == 'LL':
			obj.setDatum(79,obj.LL)
		if prop not in ["ofin","ofout"]: return 
		nurbswb.curves.OffsetSpline.myExecute(obj)


#
#
#
#

def runSole(name="meineSohle",LL=260):
	'''create a default sole object'''
	obj = FreeCAD.ActiveDocument.addObject("Sketcher::SketchObjectPython",name)
	obj.addProperty("App::PropertyInteger", "ofin", "Base", "end").ofin=10
	obj.addProperty("App::PropertyInteger", "ofout", "Base", "end").ofout=10
	obj.addProperty("App::PropertyInteger", "LL", "Base", "end").LL=LL

	Sole(obj)


	createsole(obj)
	obj.ViewObject.hide()
	App.activeDocument().recompute()
	
	import Draft
	img=Draft.makeRectangle(length=265.,height=265.,face=True,support=None)
	img.ViewObject.TextureImage = "/home/thomas/Dokumente/freecad_buch/b235_shoe/Foot_bg.png"
	img.Placement = App.Placement(App.Vector(-6,133,0),App.Rotation(App.Vector(0,0,-1),90))
	img.ViewObject.Selectable = False

	return obj


if __name__== '__main__':
	obj=runSole("Schuhsohle")
