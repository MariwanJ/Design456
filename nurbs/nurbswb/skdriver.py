'''create a driversketch for a sketch'''

from say import *
import nurbswb.pyob
import Sketcher



def setSketchDatum(sk,name,wert):
	'''set the value of a constraint by constraint name'''

	for i,c in enumerate(sk.Constraints):
		#print (i,c.Name)
		if c.Name==name:
			sk.setDatum(i,wert)
			return
	raise Exception("Constraint " + name + " nicht gefunden")



class _ViewProvider(nurbswb.pyob.ViewProvider):
	''' base class view provider '''

	def __init__(self, vobj):
		self.Object = vobj.Object
		vobj.Proxy = self

	def getIcon(self):
		return '/home/thomas/.FreeCAD/Mod/freecad-nurbs/icons/sketchdriver.svg'


class Driver(nurbswb.pyob.FeaturePython):
	'''Sketch Object with Python''' 

	##\cond
	def __init__(self, obj):
		obj.Proxy = self
		self.Type = self.__class__.__name__
		self.obj2 = obj
		_ViewProvider(obj.ViewObject) 
	##\endcond

	def onBeforeChange(proxy,obj,prop):
		'''create a backup of the point coordinates'''
		if prop <> "Geometry": return

#		print ("onBeforeChange",prop)
		proxy.podump=[]
		proxy.oldpos={}
		gs=obj.Geometry
		for i,g in enumerate(gs):
#			print (i,g.__class__.__name__)
			for j in range(4):
				try: 
#					print ("## ",j,obj.getPoint(i,j))
					proxy.podump.append([i,j,obj.getPoint(i,j)])
					proxy.oldpos[(i,j)]=obj.getPoint(i,j)
				except: break

	def rollback(proxy,obj):
		for (i,j,pos) in proxy.podump:
			obj.movePoint(i,j,pos)
			obj.solve()
			print ("back",i,j)

	def onChanged(proxy,obj,prop):
		'''run myExecute for some properties'''

		if prop in ["radiusA","radiusB"]:
			print ("onchanged",prop)
			if obj.base <>None:
				obj.base.setDatum(5,obj.radiusA)
				obj.base.setDatum(6,obj.radiusB)
			proxy.myExecute(obj)


	def myExecute(proxy,obj):
		''' position to parent'''

		if obj.off:
			print obj.Label + " is deactivated (off)"
			return
#		print "start"
#		print obj.relation

		for its in range(2):

			try:
				ts=time.time()
				bsk=obj.base

				rel=np.array(obj.relation).reshape(len(obj.relation)/5,5)

				tomove=[]
				for i,(a,b,c,d,e) in enumerate(rel):
					try:
						if a==1:
							tomove.append(False)
						else:
							pos=obj.getPoint(b,c)
		#					print pos
							posa=bsk.getPoint(d,e)
		#					print posa
		#					print
							tomove.append((pos-posa).Length>0.001)
					except:
						print i,"###"
						print (a,b,c,d,e)
						sayexc()
						tomove.append(False)
						FreeCAD.obj=obj
						return

				for i,(a,b,c,d,e) in enumerate(rel):
					try:
						if a==0 : 
							FreeCAD.obj=obj
							pos=obj.getPoint(b,c)
							#if (proxy.oldpos[(b,c)]-pos).Length>0.1:
							if tomove[i]:
								bsk.movePoint(d,e,pos)
							rc=bsk.solve()
							if rc <>0: print ("solve 0 rc=",rc)
	#					else:
	#						pos=bsk.getPoint(b,c)
	#						obj.movePoint(d,e,pos)
	#						rc=obj.solve()
	#						if rc <>0: print ("solve 1 rc=",rc)
					except:
						sayexc("movepoint"+str(i))


				for i,(a,b,c,d,e) in enumerate(rel):
					try:
						if a==0:
							pos=bsk.getPoint(d,e)
							obj.movePoint(b,c,pos)
							rc=obj.solve()
							if rc <>0: print ("solve 1 rc=",rc)
					except:
						sayexc("movepoint"+str(i))



				obj.recompute()
				bsk.recompute()
			except:
				sayexc()
				proxy.rollback(obj)

		# rollback im testmode
		if obj.rollback:
			proxy.rollback(obj)

		print ("myExecute time",round(time.time()-ts,2))



##\cond
	def execute(self, obj):
		''' recompute sketch and than run postprocess: myExecute'''
		obj.recompute() 
		self.myExecute(obj)
##\endcond



def runDriver(name="MyDriver"):
	''' an example driver for a special test sketch'''


	obj = FreeCAD.ActiveDocument.addObject("Sketcher::SketchObjectPython",name)
	obj.addProperty("App::PropertyLink", "base", "Base",)

	obj.addProperty("App::PropertyBool", "off", "Base",)
	obj.addProperty("App::PropertyBool", "rollback", "Base",)

	obj.addProperty("App::PropertyIntegerList", "relation", "Base",)

	# weitere parameter
	obj.addProperty("App::PropertyFloat", "radiusA", "Base",).radiusA=80
	obj.addProperty("App::PropertyFloat", "radiusB", "Base",).radiusB=100

	# initial geometry
	obj.addGeometry(Part.LineSegment(App.Vector(0,3,0),App.Vector(2,0.000000,0)),False)
	obj.addGeometry(Part.LineSegment(App.Vector(0,3,0),App.Vector(2,0.000000,0)),False)

	Driver(obj)

	obj.ViewObject.DrawStyle = u"Dashdot"
	obj.ViewObject.LineColor= (1.000,0.000,0.498)
	obj.ViewObject.LineWidth = 4

	return obj



def runtest():
	''' the testcase for runDriver'''

	obj=runDriver()
	obj.base=App.ActiveDocument.Sketch

	# erste spalte: 0 von obj, 1 von bsk holen
	obj.relation=[
			0,	0,1,	1,3,
			0,	0,2,	2,3,
			1,	1,3,	0,1,
			1,	2,3,	0,2,
			1,	3,1,	1,1,
			1,	3,2,	1,2,
		]



def create_rib_driver(nr):
	'''create the rib driver for rib nr and put it into the group of the rib'''

	rib=App.ActiveDocument.getObject('rib_'+str(nr))
	print ("create driver for rib",rib.Label)

	for i in range(76,96):
		rib.setDriving(i,False) 

	name="ribdriver_" +str(nr)

	runrib(rib,name,nr)




def runribtest():
	'''creates the driver for the single default rib'''

	try:App.closeDocument("Unnamed")
	except: pass
	App.newDocument("Unnamed")
	App.setActiveDocument("Unnamed")
	App.ActiveDocument=App.getDocument("Unnamed")
	Gui.ActiveDocument=Gui.getDocument("Unnamed")

	import nurbswb
	import nurbswb.createshoerib
	reload(nurbswb.createshoerib)
	nurbswb.createshoerib.run()
	rib=App.ActiveDocument.ribbow
	rib.ViewObject.LineColor = (1.000,0.667,0.000)

	for i in range(76,96):
		# rib.toggleDriving(i) 
		rib.setDriving(i,False) 

	name="ribdriver"
	runrib(rib,name)

def runrib(rib,name,nr=None):

	obj = FreeCAD.ActiveDocument.addObject("Sketcher::SketchObjectPython",name)
	obj.addProperty("App::PropertyLink", "base", "Base",)

	obj.addProperty("App::PropertyBool", "off", "Base",)
	obj.addProperty("App::PropertyBool", "rollback", "Base",)

	obj.addProperty("App::PropertyIntegerList", "relation", "Base",)

	# weitere parameter
	obj.addProperty("App::PropertyFloat", "radiusA", "Base",).radiusA=80
	obj.addProperty("App::PropertyFloat", "radiusB", "Base",).radiusB=100

	# initial geometry

	obj.base=rib


	for i in [17,19,21,23,26,28]:
		g=rib.Geometry[i].copy()
		obj.addGeometry(g)
		# print g
		obj.solve()
		obj.recompute


	obj.ViewObject.DrawStyle = u"Dashdot"
	obj.ViewObject.LineColor= (1.000,0.000,0.498)
	obj.ViewObject.LineWidth = 6


	obj.relation=[
				0,	0,1,	15,3,
				0,	0,2,	1,3,

				0,	1,1,	2,3,
				0,	1,2,	3,3,

				0,	2,1,	5,3,
				0,	2,2,	6,3,

				0,	3,1,	7,3,
				0,	3,2,	9,3,

				0,	4,1,	10,3,
				0,	4,2,	11,3,

				0,	5,1,	13,3,
				0,	5,2,	14,3,
			]


	bsk=obj.base
	rel=np.array(obj.relation).reshape(len(obj.relation)/5,5)
	
	for i,(a,b,c,d,e) in enumerate(rel):
				try:
					if a==0:
						pos=bsk.getPoint(d,e)
						obj.movePoint(b,c,pos)
						rc=obj.solve()
						if rc <>0: print ("solve 1 rc=",rc)
				except:
					sayexc("movepoint"+str(i))




	Driver(obj)


	App.activeDocument().recompute()
	Gui.activeDocument().activeView().viewTop()
	Gui.SendMsgToActiveView("ViewFit")
	Gui.activeDocument().activeView().viewTop()

	if nr<> None:
		grp=App.ActiveDocument.getObject('GRP_'+str(nr))
		grp.addObject(obj)
		obj.ViewObject.hide()



def create_rib_driverALT(nr):
	'''create the rib driver for rib nr and put it into the group of the rib'''

	rib=App.ActiveDocument.getObject('rib_'+str(nr))
	print ("create driver for rib",rib.Label)

	for i in range(76,96):
		rib.toggleDriving(i) 

	name="ribdriver_" +str(nr)

	obj = FreeCAD.ActiveDocument.addObject("Sketcher::SketchObjectPython",name)
	obj.addProperty("App::PropertyLink", "base", "Base",)

	obj.addProperty("App::PropertyBool", "off", "Base",)
	obj.addProperty("App::PropertyBool", "rollback", "Base",)

	obj.addProperty("App::PropertyIntegerList", "relation", "Base",)

	# weitere parameter
	obj.addProperty("App::PropertyFloat", "radiusA", "Base",).radiusA=80
	obj.addProperty("App::PropertyFloat", "radiusB", "Base",).radiusB=100

	# initial geometry

	obj.base=rib

	for i in range(8):
		g=rib.Geometry[17+2*i].copy()
		obj.addGeometry(g)
		#print g
		obj.solve()
		obj.recompute



	obj.ViewObject.DrawStyle = u"Dashdot"
	obj.ViewObject.LineColor= (1.000,0.000,0.498)
	obj.ViewObject.LineWidth = 6


	obj.relation=[
				0,	0,1,	0,3,
				0,	0,2,	1,3,
				0,	1,1,	2,3,
				0,	1,2,	3,3,

				0,	2,1,	4,3,
				0,	2,2,	5,3,

				0,	3,1,	6,3,
				0,	3,2,	7,3,

				0,	4,1,	8,3,
				0,	4,2,	9,3,

				0,	5,1,	10,3,
				0,	5,2,	11,3,

				0,	6,1,	12,3,
				0,	6,2,	13,3,

				0,	7,1,	14,3,
				0,	7,2,	15,3,



				1,	0,3,	0,1,
				1,	1,3,	0,2,
				1,	2,3,	1,1,
				1,	3,3,	1,2,

				1,	4,3,	2,1,
				1,	5,3,	2,2,


				1,	6,3,	3,1,
				1,	7,3,	3,2,

## ab hier fehler 
#				1,	8,3,	4,1,
#				1,	9,3,	4,2,
#
#				1,	10,3,	5,1,
#				1,	11,3,	5,2,
#
#				1,	12,3,	6,1,
#				1,	13,3,	6,2,
#
#				1,	14,3,	7,1,
#				1,	15,3,	7,2,




			]

	Driver(obj)


	App.activeDocument().recompute()
	Gui.activeDocument().activeView().viewTop()
	Gui.SendMsgToActiveView("ViewFit")
	Gui.activeDocument().activeView().viewTop()
	grp=App.ActiveDocument.getObject('GRP_'+str(nr))
	grp.addObject(obj)
	obj.ViewObject.hide()



def runribtest2():
	'''create ribdrivers for all shoe ribs'''
	for i in  range(2,15):
	#for i in [10]:
		try:
			create_rib_driver(i)
		except:
			sayexc()



def recomputeAll():
	'''to recompute the shoe all ribs must be touched'''
	for i in range(2,15):
		obj=App.ActiveDocument.getObject('rib_'+str(i))
		dob=App.ActiveDocument.getObject('ribdriver_'+str(i))
		if obj <> None:
			obj.touch()
		# deactivate the driver feedback to speed up
		if dob<>None:
			dob.off=True

	App.activeDocument().recompute()

	for i in range(2,15):
		dob=App.ActiveDocument.getObject('ribdriver_'+str(i))
		if dob<>None:
			dob.off=False

