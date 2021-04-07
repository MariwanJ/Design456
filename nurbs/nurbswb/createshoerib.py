'''create a shoe rib for shoeAdam'''
# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- (c) microelly 2017 v 0.1
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

from say import * 
import Sketcher
import nurbswb.pyob

'''
multiplizitaet erhoehen
App.ActiveDocument.Sketch.modifyBSplineKnotMultiplicity(7,3,1) 
App.ActiveDocument.Sketch.exposeInternalGeometry(6)
App.ActiveDocument.Sketch.modifyBSplineKnotMultiplicity(6,3,-1) 
'''

class _ViewProvider(nurbswb.pyob.ViewProvider):
	''' base class view provider '''

	def __init__(self, vobj):
		self.Object = vobj.Object
		vobj.Proxy = self

	def getIcon(self):
		return '/home/thomas/.FreeCAD/Mod/freecad-nurbs/icons/sketchrib.svg'


## create a special ful constrainted Sketcher Bspline
#
# @param name of the rib
# @param moves post creation movement of the points inside the sketch(deactivated) 
# @param box 4 parameters for the bounding box
# @param zoff offset of the sketch in z-direction 
#
#.


def run(name='ribbow',moves=[],box=[40,0,-40,30],zoff=0):
	'''creates a shoe rib '''

	debug=True
	debug=False
	
	print "----createshoerib------------------"
	print name
	print moves
	print box
	print "-------------------------"

	label=name
	try: body=App.activeDocument().Body
	except:	body=App.activeDocument().addObject('PartDesign::Body','Body')

	#sk=App.activeDocument().addObject('Sketcher::SketchObject',name)
	sk = FreeCAD.ActiveDocument.addObject("Sketcher::SketchObjectPython",name)
	_ViewProvider(sk.ViewObject) 


	sk.Placement.Base.z=zoff
	sk.Label=label
#	sk.MapMode = 'FlatFace'

	App.activeDocument().recompute()

	#create a regular naz-gon
	anz=16
	r=50
	pts= [FreeCAD.Vector(r*np.sin(2*np.pi/anz*i),r*np.cos(2*np.pi/anz*i)+50,0) for i in range(anz)]

	#create the helper circles for the bspline curve
	for i,p in enumerate(pts):
		sk.addGeometry(Part.Circle(App.Vector(int(round(p.x)),int(round(p.y)),0),App.Vector(0,0,1),10),True)
		radius=2.0
		sk.addConstraint(Sketcher.Constraint('Radius',i,radius)) 
		sk.renameConstraint(i, 'Weight ' +str(i+1))

	k=i+1
	l=[App.Vector(int(round(p.x)),int(round(p.y))) for p in pts]

	#create the spline
	if 0: # open spline
		ll=sk.addGeometry(Part.BSplineCurve(l,None,None,False,3,None,False),False)
	else: # periodic spline
		ll=sk.addGeometry(Part.BSplineCurve(l,None,None,True,3,None,False),False)


	#connect the poles to the spline
	conList = []
	for i,p in enumerate(pts):
		conList.append(Sketcher.Constraint('InternalAlignment:Sketcher::BSplineControlPoint',i,3,k,i))
	sk.addConstraint(conList)
	App.activeDocument().recompute()

	# connect the points for easier access in edit mode drag/drop for lines
	for p in range (0,anz):
		if 1:
			ll=sk.addGeometry(Part.LineSegment(App.Vector(100+10*p,100+10*p,0),App.Vector(-100,-100,0)),False)
		else:
			# nur als hilfslinien
			ll=sk.addGeometry(Part.LineSegment(App.Vector(100+10*p,100+10*p,0),App.Vector(-100,-100,0)),True)

		sk.addConstraint(Sketcher.Constraint('Coincident',p,3,ll,1)) 
		App.ActiveDocument.recompute()

		if p==anz-1: p=-1

		sk.addConstraint(Sketcher.Constraint('Coincident',p+1,3,ll,2)) 
		App.ActiveDocument.recompute()

	d=sk.addConstraint(Sketcher.Constraint('Parallel',32,17)) 
	sk.renameConstraint(d,'Parallel_32_17')
	d=sk.addConstraint(Sketcher.Constraint('Parallel',20,21)) 
	sk.renameConstraint(d,'Parallel_20_21')
	d=sk.addConstraint(Sketcher.Constraint('Parallel',23,24)) 
	sk.renameConstraint(d,'Parallel_23_24')
	d=sk.addConstraint(Sketcher.Constraint('Parallel',24,25)) 
	sk.renameConstraint(d,'Parallel_24_25')
	d=sk.addConstraint(Sketcher.Constraint('Parallel',25,26)) 
	sk.renameConstraint(d,'Parallel_25_26')

	d=sk.addConstraint(Sketcher.Constraint('Parallel',28,29)) 
	sk.renameConstraint(d,'Parallel_28_29')

	#rahmen rechteck
	if 0:
		sk.addConstraint(Sketcher.Constraint('Horizontal',17)) 
		sk.addConstraint(Sketcher.Constraint('Horizontal',23)) 

		sk.addConstraint(Sketcher.Constraint('Vertical',20)) 
		sk.addConstraint(Sketcher.Constraint('Vertical',28)) 

	else:
		d=sk.addConstraint(Sketcher.Constraint('Angle',23,1,-1,1,np.pi)) 
		sk.renameConstraint(d, u'angleBottom')
		d=sk.addConstraint(Sketcher.Constraint('Angle',-1,1,17,1,0)) 
		sk.renameConstraint(d, u'angleTop')
		d=sk.addConstraint(Sketcher.Constraint('Angle',-1,2,20,1,np.pi/2)) 
		sk.renameConstraint(d, u'angleRight')
		d=sk.addConstraint(Sketcher.Constraint('Angle',29,2,-1,1,np.pi/2)) 
		sk.renameConstraint(d, u'angleLeft')

	# symmetrische Ecken
	d=sk.addConstraint(Sketcher.Constraint('Symmetric',5,3,3,3,4,3))
	sk.renameConstraint(d, u'symmetryRight')
	d=sk.addConstraint(Sketcher.Constraint('Symmetric',11,3,13,3,12,3))
	sk.renameConstraint(d, u'symmetryLeft')
	App.activeDocument().recompute()


	dd=5
	[r,b,l,t]=box

	if min(r,-l)<dd:
		dd=min(r,-l)*0.4

	if r== 10: dd=1 #hack for the first rib

	dtb=dd # tangent Bottom

	d=sk.addConstraint(Sketcher.Constraint('DistanceY',4,3,3,3,dd)) 
	sk.renameConstraint(d, u'tangentRight')
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',7,3,6,3,dtb)) 
	sk.renameConstraint(d, u'tangentBottom')
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',10,3,9,3,dtb)) 
	sk.renameConstraint(d, u'tangentBottomB')
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',8,3,7,3,dd)) 
	sk.renameConstraint(d, u'WidthBottomA')
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',9,3,8,3,dd)) 
	sk.renameConstraint(d, u'WidthBottomB')
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',11,3,12,3,dd)) 
	sk.renameConstraint(d, u'tangentLeft')
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',0,3,1,3,dd)) 
	sk.renameConstraint(d, u'tangentTop')
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',15,3,0,3,dd)) 
	sk.renameConstraint(d, u'tangentTopB')

	if r+l<-10:
		print "verletzung --------------createshoerib zeile 152---- r+l",r+l
		print r+l


	#move the main points to the right position
	sk.movePoint(0,0,App.Vector(0,t,0),0)

	d=sk.addConstraint(Sketcher.Constraint('DistanceX',0,3,0)) 
	sk.renameConstraint(d, u'p0X')
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',0,3,t)) 
	sk.renameConstraint(d, u'p0Y')
	App.activeDocument().recompute()

	sk.movePoint(2,0,App.Vector(r,t,0),0)
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',2,3,r)) 
	sk.renameConstraint(d, u'p2X')
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',2,3,t)) 
	sk.renameConstraint(d, u'p2Y')
	App.activeDocument().recompute()

	sk.movePoint(14,0,App.Vector(l,t,0),0)
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',14,3,l)) 
	sk.renameConstraint(d, u'p14X')
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',14,3,t)) 
	sk.renameConstraint(d, u'p14Y')
	App.activeDocument().recompute()

	sk.movePoint(4,0,App.Vector(r,b+dd,0),0)
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',4,3,r)) 
	sk.renameConstraint(d, u'p4X')
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',4,3,b+dd)) 
	sk.renameConstraint(d, u'p4Y')
	App.activeDocument().recompute()

	sk.movePoint(12,0,App.Vector(l,b+dd,0),0)
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',12,3,l)) 
	sk.renameConstraint(d, u'p12X')
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',12,3,b+dd)) 
	sk.renameConstraint(d, u'p12Y')
	App.activeDocument().recompute()

	sk.movePoint(8,0,App.Vector(0,b,0),0)
	d=sk.addConstraint(Sketcher.Constraint('DistanceX',8,3,0)) 
	sk.renameConstraint(d, u'p8X')
	d=sk.addConstraint(Sketcher.Constraint('DistanceY',8,3,b)) 
	sk.renameConstraint(d, u'p8Y')
	App.activeDocument().recompute()

	# kein verschieben
	return sk

#	print (name,"moves ...")
# wird nicht ausgefuehrt, weil die constraints das bereits verhindern #!#
	for [k,x,y] in moves:
		print (k,x,y)
		sk.movePoint(k,3,App.Vector(x,y,0),0)
		App.activeDocument().recompute()

	return sk



def test():
	'''creat some ribs'''

	sk1=run("rib1",[[8,0,0],[0,0,120],[4,120,-10],[12,-130,0]])
	sk2=run("rib2",[[8,0,0],[0,0,150],[4,70,10],[12,-90,100]])
	target=run("rib3",[],[40,-10,-40,30])



if  __name__ == '__main__':
	test()
