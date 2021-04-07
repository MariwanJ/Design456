# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- create a needle
#--
#-- microelly 2016 v 0.4
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


import FreeCAD as App
import FreeCADGui as Gui



from PySide import QtGui
import Part,Mesh,Draft

import numpy as np

def Myarray2NurbsD3(arr,label="MyWall",degree=3,obj=None):

	cylinder=True

	pst=np.array(arr)
	NbVPoles,NbUPoles,_t1 =pst.shape

	#degree=3
	#degree=1
	
	udegree=degree
	vdegree=degree
	
	if degree == 1: cylinder = False
	
	ps=[[App.Vector(pst[v,u,0],pst[v,u,1],pst[v,u,2]) for u in range(NbUPoles)] for v in range(NbVPoles)]

	kv=[1.0/(NbVPoles-3)*i for i in range(NbVPoles-2)]
	mv=[4] +[1]*(NbVPoles-4) +[4]

	if degree == 1:
		kv=[1.0/(NbVPoles-1)*i for i in range(NbVPoles)]
		mv=[2] +[1]*(NbVPoles-2) +[2]

	if  NbVPoles == 2:
		print ("KKKK"
		kv=[0,1]
		mv=[2,2]
		vdegree=1


	if cylinder:
		ku=[1.0/(NbUPoles-1)*i for i in range(NbUPoles)]
		mu=[2]+[1]*(NbUPoles-2)+[2]

		# bug 
		ku=[1.0/(NbUPoles)*i for i in range(NbUPoles+1)]
		mu=[1]*(NbUPoles+1)
		print len(ps)
		print sum(mu)



		if degree == 1:
			ku=[1.0/(NbUPoles-1)*i for i in range(NbUPoles)]
			mu=[1]*(NbUPoles)

	else:
		ku=[1.0/(NbUPoles-3)*i for i in range(NbUPoles-2)]
		mu=[4]+[1]*(NbUPoles-4)+[4]
		if degree == 1:
			ku=[1.0/(NbUPoles-1)*i for i in range(NbUPoles)]
			mu=[2] +[1]*(NbUPoles-2) +[2]




	bs=Part.BSplineSurface()
	bs.buildFromPolesMultsKnots(ps, mv, mu, kv, ku, False,cylinder ,vdegree,udegree)

	sh=bs.toShape()

	if 1:
		vcp=True
		try:
			sp=App.getDocument("Needle").Poles
			vcp=sp.ViewObject.ControlPoints
		except: sp=App.ActiveDocument.addObject("Part::Spline","Poles")
		sp.Shape=sh
		sp.ViewObject.ControlPoints=vcp
		sp.ViewObject.hide()

	if obj.makeSolid:
		try:
			fa=bs.uIso(0)
			sha1 = Part.Wire(fa.toShape())
			sha = Part.Face(sha1)

			fb=bs.uIso(1)
			shb1 = Part.Wire(fb.toShape())
			shb = Part.Face(shb1)

			sol=Part.Solid(Part.Shell([sha.Face1,shb.Face1,sh.Face1]))
		except:
			try:
				sha=Part.makeFilledFace(Part.__sortEdges__([App.ActiveDocument.Poles.Shape.Edge3, ]))
				shb=Part.makeFilledFace(Part.__sortEdges__([App.ActiveDocument.Poles.Shape.Edge1, ]))
				sol=Part.Solid(Part.Shell([sha.Face1,shb.Face1,sh.Face1]))
			except:
				sol=sh
	else:
		sol=sh

	return (sol,bs)


def toUVMesh(bs, uf=5, vf=5):
		uc=uf*bs.NbUPoles
		vc=vf*bs.NbVPoles
		ss=[]
		for x in range(uc+1): 
			for y in range(vc+1): 
				ss.append(bs.value(1.0/uc*x,1.0/vc*y))

		mm=np.array(ss)[:,2].max()
		#add closing points
		ss.append(App.Vector(0,0,0))
		ss.append(App.Vector(0,0,mm))

		topfaces=[]
		x=0
		for y in range(vc): 
			topfaces.append(((vc+1)*x+y,(vc+1)*x+y+1,len(ss)-2))
		x=uc
		for y in range(vc): 
			topfaces.append(((vc+1)*x+y,(vc+1)*x+y+1,len(ss)-1))

#		t=Mesh.Mesh((ss,topfaces))
#		Mesh.show(t)
#		App.activeDocument().ActiveObject.ViewObject.Lighting="Two side"



		faces=[]
		for x in range(uc): 
			for y in range(vc): 
				#if max((vc+1)*x+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y+1,(vc+1)*(x+1)+y)<50000: 
				#if len(faces)<100000:
					faces.append(((vc+1)*x+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y))
					faces.append(((vc+1)*x+y+1,(vc+1)*(x+1)+y+1,(vc+1)*(x+1)+y))

		# print ss
		# print faces
		if 0:
			App.Console.PrintMessage(str(("size of the mesh:",uc,vc))+"\n")
			App.Console.PrintMessage(str(("number of points" ,len(ss)))+"\n")
			App.Console.PrintMessage(str(("faces:",len(faces)))+"\n")



		if len(faces)<100000:
			t=Mesh.Mesh((ss,faces))
			Mesh.show(t)
			App.activeDocument().ActiveObject.ViewObject.Lighting="Two side"
			App.activeDocument().ActiveObject.ViewObject.DisplayMode = u"Wireframe"
			App.activeDocument().ActiveObject.ViewObject.LineColor = (.70,.00,0.00)
			#App.Console.PrintMessage(str(t))
			return App.activeDocument().ActiveObject
		else:
			raise Exception("big mesh not implemented")

			ks=len(faces)//100000
			for i in range(ks+1):
				t=Mesh.Mesh((ss,faces[i*100000:(i+1)*100000]))
				Mesh.show(t)
				App.activeDocument().ActiveObject.ViewObject.Lighting="Two side"
				App.activeDocument().ActiveObject.ViewObject.DisplayMode = u"Wireframe"
				App.activeDocument().ActiveObject.ViewObject.LineColor = (.70,.00,0.00)
				App.Console.PrintMessage(str(t))

		return t




def scale(profile,scaler=None):
	c=np.array(profile)
	if scaler == None: scaler= [1]*10
	poles=np.array([c*[scaler[i,0],scaler[i,0],scaler[i,1]] for i in  range(len(scaler))])
	return poles


def extrude(profile,path=None):
	c=np.array(profile)
	vc,uc,_t=c.shape
	for v in range(vc):
		c[v] += path[v]
	return c

def myrot(v,twister):
	v=App.Vector(v)
	xa=0
	ya=0
	za=10
	[xa,ya,za]=twister
	p2=App.Placement()
	p2.Rotation=App.Rotation(App.Vector(0,0,1),za).multiply(App.Rotation(App.Vector(0,1,0),ya).multiply(App.Rotation(App.Vector(1,0,0),xa)))
#	print ("Rotation Euler",p2.Rotation.toEuler())

	p=App.Placement()
	p.Base=v
	rc=p2.multiply(p)
#	print v
#	print rc.Base
	return rc.Base


def twist(profile,twister):
#	print ("twister"
	c=np.array(profile)
	vc,uc,_t=c.shape
	rc=[]
	for v in range(vc):
		cv=[]
#		print twister[v]
		for u in range(uc):
			sp=c[v,u]
			tpp=myrot(sp,twister[v])
			cv.append(tpp)
		c[v]=cv
	return c




#---------------------
# daten aus sheet







def cellname(col,row):
	#limit to 26
	if col>90-64:
		raise Exception("not implement")
	char=chr(col+64)
	cn=char+str(row)
	return cn



def npa2ssa(arr,spreadsheet,c1,r1,color=None):
	''' write 2s array into spreadsheet '''
	ss=spreadsheet
	arr=np.array(arr)
	try:
		rla,cla=arr.shape
	except:
		rla=arr.shape[0]
		cla=0
	c2=c1+cla
	r2=r1+rla
	if cla==0:
		for r in range(r1,r2):
			cn=cellname(c1,r)
			ss.set(cn,str(arr[r-r1]))
			if color!=None: ss.setBackground(cn,color)
	else:
		for r in range(r1,r2):
			for c in range(c1,c2):
				cn=cellname(c,r)
	#			print (cn,c,r,)
				ss.set(cn,str(arr[r-r1,c-c1]))
				if color!=None: ss.setBackground(cn,color)

def gendata(ss):
	print ("gendata",ss.Label)

	# Form der Nadel als Parameter 

	# profil blatt
	curve=[[0,0,0],[5,-5,10],[30,-10,-0],[20,-5,-10],[0,10,0],[-20,-5,-0],[-30,-10,0],[-5,-5,0]]

	curve=[
			[0,0,0],
			[0,29,0],[0,30,0],[0,31,0],
			[100,30,25],
			[100,180,25],
			[-20,180,-5],
			[-20,-30,-5],
			[-100,-30,-25],[-99,-30,-25],
			[-100,-129,-25],[-100,-130,-25],[-99,-130,-25],
			[0,-40,-0]
		]

	# backbone
	bb= [[0,0,0],[0,0,100],[0,-5,40],[5,-10,170],[-3,20,300]]
	bb= [[0,0,0],[0,0,50],[0,0,100],[0,0,200],[0,0,400],[0,0,500],[0,0,600]]





	#scaling
	sc=[[1,0],[1.5,1],[1,-5],[0.7,1],[3.05,0]]
	sc=[[1,0],[1,0],[1,0],[1,0],[3,0]]
	sc=[[1,0],[1,2],[2,0],[1,-2],[4,0]]

	sc=[[1,0],[1,0],[1,0],[1,0],[1,0],[1.3,0],[1.,0]]


	#twist along the z-axis
	twister=[[0,0,0],[0,0,90],[30,0,-70],[0,30,-90],[0,0,0]]
	twister=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

	twister=[[0,0,0],[0,0,90],[0,0,20],[0,0,-20],[0,0,30],[0,0,0],[0,0,-50]]
	twister=[[0,0,0],[0,0,0],[35,0,0],[00,0,0],[-35,0,0],[-35,0,0],[0,0,0]]
	twister=[[0,0,0],[0,45,0],[0,0,0],[00,0,0],[0,45,0],[0,-45,0],[0,0,0]]


	# halbscharfe kante
	bb= [[0,0,0],[0,0,50],[0,0,100],[0,0,200],[0,0,400],[0,0,499],[0,0,500],[0,0,600]]
	twister=[[0,0,0],[0,-25,0],[0,0,0],[00,0,0],[0,-25,0],[0,25,0],[0,25,0],[0,0,0]]
	sc=[[1,0],[1,0],[1,0],[1,0],[1,0],[1.3,0],[1.3,0],[1.,0]]



	bb= [[0,0,0],[0,0,50],[0,0,100],[0,0,200],[0,0,400],[0,0,499],[0,0,500],[0,0,501],[0,0,800]]
	twister=[[0,0,0],[0,-25,0],[0,0,0],[00,0,0],[0,-25,0],[0,25,0],[0,25,0],[0,25,0],[20,30,40]]
	sc=[[1,0],[1,0],[1,0],[1,0],[1,0],[1.3,0],[1.3,0],[1.3,0],[1.5,0]]




	npa2ssa(curve,ss,2,3,(1.0,1.0,0.5))
	npa2ssa(bb,ss,7,3,(1.0,.5,1.0))
	npa2ssa(sc,ss,10,3,(0.5,1.0,1.0))
	npa2ssa(twister,ss,13,3,(1.0,.5,0.5))
	ss.set('B1',str(len(curve)))
	ss.set('G1',str(len(bb)))
	ss.set('G2','Backbone x')
	ss.set('H2','y')
	ss.set('I2','z')
	ss.set('J2','Scale xy')
	ss.set('K2','z')
	ss.set('M2','Rotation x')
	ss.set('N2','y')
	ss.set('O2','z')
	ss.set('B2','Rib x')
	ss.set('C2','y')
	ss.set('D2','z')
	App.activeDocument()().recompute()


def ssa2npa(spreadsheet,c1,r1,c2,r2,default=None):
	''' create array from table'''

	c2 +=1
	r2 +=1

	ss=spreadsheet
	z=[]
	for r in range(r1,r2):
		for c in range(c1,c2):
			cn=cellname(c,r)
			# print cn
			try:
				v=ss.get(cn)
				z.append(ss.get(cn))
			except:
				z.append(default)


	z=np.array(z)
#	print z
	ps=np.array(z).reshape(r2-r1,c2-c1)
	return ps


if 0 and __name__=='__main__':

	App.ActiveDocument=None
	Gui.ActiveDocument=None
	App.open(u"/home/thomas/Schreibtisch/nadel_daten.fcstd")
	App.setactiveDocument()("nadel_daten")
	App.ActiveDocument=App.getDocument("nadel_daten")
	Gui.ActiveDocument=Gui.getDocument("nadel_daten")





class PartFeature:
	def __init__(self, obj):
		obj.Proxy = self
		self.Object=obj

# grundmethoden zum sichern

	def attach(self,vobj):
		self.Object = vobj.Object

	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


class ViewProvider:
	def __init__(self, obj):
		obj.Proxy = self
		self.Object=obj

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None



class Needle(PartFeature):
	def __init__(self, obj,uc=5,vc=5):
		PartFeature.__init__(self, obj)

		self.Type="Needle"
		self.TypeId="Needle"

		for l in ['Mesh','Backbone','Profile','RibCage','RibTemplate','Spreadsheet']:
			obj.addProperty("App::PropertyLink",l,l)
			obj.addProperty("App::PropertyBool","use" + l ,l)
			setattr(obj,"use"+l,False)

		obj.addProperty("App::PropertyBool","noExecute" ,"Base")
		obj.addProperty("App::PropertyInteger","Degree","Base").Degree=3
		obj.addProperty("App::PropertyLink","Meridians","RibCage")
		obj.addProperty("App::PropertyInteger","RibCount","RibCage").RibCount=10
		obj.addProperty("App::PropertyInteger","MeshUCount","Mesh").MeshUCount=5
		obj.addProperty("App::PropertyInteger","MeshVCount","Mesh").MeshVCount=5

		obj.addProperty("App::PropertyInteger","startSegment","Segment").startSegment=0
		obj.addProperty("App::PropertyInteger","endSegment","Segment").endSegment=-1
		
		obj.addProperty("App::PropertyBool","makeSolid" ,"Base").makeSolid=True

		# obj.ViewObject.LineColor=(1.0,0.0,1.0)
		#obj.ViewObject.DisplayMode = "Shaded"
		obj.ViewObject.Transparency = 30
		obj.addProperty("App::PropertyLink","ribtemplateSource","Spreadsheet")
		obj.addProperty("App::PropertyLink","backboneSource","Spreadsheet")
		obj.addProperty("App::PropertyBool","externSourcesOff" ,"Spreadsheet")
		ViewProvider(obj.ViewObject)

	def onDocumentRestored(self, fp):
		print ("onDocumentRestored "
		print fp.Label
		self.Object=fp


	def onChanged(self, fp, prop):
		
		if prop == 'useSpreadsheet':
			if fp.useSpreadsheet:
				if fp.Spreadsheet == None:
					fp.Spreadsheet = App.activeDocument().addObject('Spreadsheet::Sheet','Spreadsheet')
					##gendata(fp.Spreadsheet)
			return
		if prop in ["Shape", 'Spreadsheet']: return
#		print ("onChanged",prop)


	def execute(proxy,obj):
#		print("execute ")
		if obj.noExecute: return
		try: 
			if proxy.lock: return
		except:
			print("except proxy lock")
		proxy.lock=True
#		print("myexecute")
		proxy.myexecute(obj)
		proxy.lock=False

	def myexecute(proxy,obj):

		ss=obj.Spreadsheet


		if obj.ribtemplateSource != None and not obj.externSourcesOff:
			cs=obj.ribtemplateSource.Shape.Edge1.Curve
			curve=cs.getPoles()
			cl=len(curve)
			npa2ssa(curve,ss,2,3)
			print ("update curve",curve
		else:
			cl=int(ss.get('B1'))
			curve=ssa2npa(ss,2,3,4,3+cl-1)
			if obj.Degree == 1:
				curve=list(curve)
				curve.append(curve[1])


		if obj.backboneSource != None and not obj.externSourcesOff:
			cs=obj.backboneSource.Shape.Edge1.Curve
			bb=cs.getPoles()
			bl=len(bb)
			npa2ssa(bb,ss,7,3)
			print ("update backbone",bb

		else:
			bl=int(ss.get('G1'))
			bb=ssa2npa(ss,7,3,9,3+bl-1)


		scaler=ssa2npa(ss,10,3,11,3+bl-1,default=1.0)
		twister=ssa2npa(ss,13,3,15,3+bl-1,default=0.0)


#----------------------------
		#'''
		# backbone machen
		bbc=Part.BSplineCurve()
		bbc.buildFromPoles(bb)

		pa=bbc.LastParameter
		ps=bbc.FirstParameter

		print ("-----------------------------------------------"
		for n in range(len(bb)):
			v=ps +(pa-ps)*n/(len(bb)-1)
			print ("!!",n,v)
			print bbc.tangent(v)
			t=bbc.tangent(v)[0]
			p=bbc.value(v)
			
			print t
			zarc=np.arctan2(t.y,t.x)
			zarc *=180.0/np.pi
			zarc=0

			harc=np.arcsin(t.z)
			harc *=180.0/np.pi

			print twister[n]
			# twister[n]=[0,0,harc]
			
			print twister[n]
		print ("---------------------------------------ccccccccc--------"
		print len(twister)
		print twister
		print ("huhu"
		#'''


#-----------------------------




		poles= scale(curve,scaler)
		poles= twist(poles,twister)
		poles= extrude(poles,bb)

		(nn,bs)=Myarray2NurbsD3(poles,"Nadelhuelle",degree=obj.Degree,obj=obj)
		obj.Shape=nn

		if obj.useBackbone: proxy.createBackbone(obj,bb)
		if obj.useRibTemplate: proxy.createRibTemplate(obj,curve)
		if obj.useRibCage: proxy.createRibCage(obj,bs)
		if obj.useMesh: proxy.createMesh(obj,bs)

	def createBackbone(proxy,obj,bb):
		if obj.Backbone == None:
			obj.Backbone=App.activeDocument().addObject('Part::Feature','Backbone')
		
		#obj.Backbone.Shape=Part.makePolygon([App.Vector(b) for b in bb])
		bs=Part.BSplineCurve()
		bs.buildFromPoles(bb)
		obj.Backbone.Shape=bs.toShape()

		vob=obj.Backbone.ViewObject
		vob.LineColor=(0.,1.,1.)
		vob.LineWidth = 5.00

	def createRibTemplate(proxy,obj,curve):
		if obj.RibTemplate == None:
			obj.RibTemplate=App.activeDocument().addObject('Part::Feature','Rib template')
		#obj.RibTemplate.Shape=Part.makePolygon([App.Vector(c) for c in curve])

		bs=Part.BSplineCurve()
		c=curve
		ms=[2] +[1]*(len(c)-2) +[2]
		ks=[1.0/(len(c)-1)*i for i in range(len(c))]
		bs.buildFromPolesMultsKnots(c,ms,ks,True,3)
		obj.RibTemplate.Shape=bs.toShape()

		vob=obj.RibTemplate.ViewObject
		vob.LineColor=(1.,0.6,.0)
		vob.LineWidth = 5.00

	def createMesh(proxy,obj,bs):
			vb=True
			if obj.Mesh != None:
				vb=obj.Mesh.ViewObject.Visibility
				App.activeDocument().removeObject(obj.Mesh.Name)
			obj.Mesh=toUVMesh(bs,obj.MeshUCount,obj.MeshVCount)
			obj.Mesh.ViewObject.Visibility=vb

	def createRibCage(proxy,obj,bs):
		rc=obj.RibCount


		if rc>0:
			ribs=[]
			for i in range(rc+1):
				f=bs.uIso(1.0/rc*i)
				ribs.append(f.toShape())
		else:
			ribs=[]
			for i,j in enumerate(bs.getUKnots()):
				f=bs.uIso(j)
				ribs.append(f.toShape())


		comp=Part.Compound(ribs)
		if obj.RibCage == None:
			obj.RibCage=App.activeDocument().addObject('Part::Feature','Ribs')
		obj.RibCage.Shape=comp
		vob=App.getDocument("Needle").ActiveObject.ViewObject
		vob.LineColor=(1.,1.,0.)
		vob.LineWidth = 5.00

		mers=[]
		for i,j in enumerate(bs.getVKnots()):
			f=bs.vIso(j)
			mers.append(f.toShape())
		comp=Part.Compound(mers)
		if obj.Meridians == None:
			obj.Meridians=App.getDocument("Needle").addObject('Part::Feature','Meridians')
		obj.Meridians.Shape=comp
		vob=App.getDocument("Needle").ActiveObject.ViewObject
		vob.LineColor=(1.,0.,0.4)
		vob.LineWidth = 5.00


	def updateSS(self,curve,bb,sc,twister):

			ss=self.Object.Spreadsheet
			ss.clearAll()
			npa2ssa(curve,ss,2,3,(1.0,1.0,0.5))
			npa2ssa(bb,ss,7,3,(1.0,.5,1.0))
			npa2ssa(sc,ss,10,3,(0.5,1.0,1.0))
			npa2ssa(twister,ss,13,3,(1.0,.5,0.5))
			ss.set('B1',str(len(curve)))
			ss.set('G1',str(len(bb)))
			ss.set('G2','Backbone x')
			ss.set('H2','y')
			ss.set('I2','z')
			ss.set('J2','Scale xy')
			ss.set('K2','z')
			ss.set('M2','Rotation x')
			ss.set('N2','y')
			ss.set('O2','z')
			ss.set('B2','Rib x')
			ss.set('C2','y')
			ss.set('D2','z')
			try:
				App.activeDocument()().recompute()
			except:
				print ("recompute jack "
				dokname=App.ParamGet('User parameter:Plugins/nurbs').GetString("Document","Needle")
				App.getDocument(dokname).recompute()
				pass

	def getExampleModel(self,model):
		print ("getExampleModel"
		print model
		m=model()
		print model().curve
		self.updateSS(m.curve,m.bb,m.sc,m.twister)

	def Model(self):
		ss=self.Object.Spreadsheet
		cl=int(ss.get('B1'))
		curve=ssa2npa(ss,2,3,4,3+cl-1)
		bl=int(ss.get('G1'))
		bb=ssa2npa(ss,7,3,9,3+bl-1)
		scaler=ssa2npa(ss,10,3,11,3+bl-1,default=1.0)
		twister=ssa2npa(ss,13,3,15,3+bl-1,default=0.0)
		return(curve,bb,scaler,twister)

	def setModel(self,curve,bb,scaler,twister):
		self.updateSS(curve,bb,scaler,twister)

	def startssevents(self):
#		global table

		mw=FreeCADGui.getMainWindow()
		mdiarea=mw.findChild(QtGui.QMdiArea)


		App.activeDocument().Spreadsheet.ViewObject.startEditing(0)
		subw=mdiarea.subWindowList()
	#	print len(subw)
		for i in subw:
	#		print i.widget().metaObject().className()
			if i.widget().metaObject().className() == "SpreadsheetGui::SheetView":
				sheet = i.widget()
				table=sheet.findChild(QtGui.QTableView)

		table.clicked.connect(self.clicked)
	#	table.entered.connect(entered)
		table.pressed.connect(self.pressed)
		self.table=table

	def clicked(self,index):
		print ("Clicked",index
		self.dumpix(index)
		print (getdata(index))

	def entered(self,index):
		print ("Entered"
		self.dumpix(index)

	def pressed(self,index):
		import nurbswb.needle_cmds
		reload(nurbswb.needle_cmds)
		nurbswb.needle_cmds.pressed(index,App.activeDocument().MyNeedle)
		print ("Pressed"

	def changed(self,index):
		print ("Changed"
		self.dumpix(index)

	def dumpix(self,index): 
		print ("dumpix", index.row(),index.column(),(getdata(index)))
		self.show(getdata(index))


	def showRib(self,ri):
		Gui.Selection.clearSelection()
		dokname=App.ParamGet('User parameter:Plugins/nurbs').GetString("Document","Needle")
		d=App.getDocument(dokname)
		Gui.Selection.addSelection(d.getObject('Ribs'),"Edge" +str(ri))

	def showMeridian(self,ri):
		Gui.Selection.clearSelection()
		dokname=App.ParamGet('User parameter:Plugins/nurbs').GetString("Document","Needle")
		d=App.getDocument(dokname)
		Gui.Selection.addSelection(d.getObject('Meridians'),"Edge" +str(ri))


	def show(self,dat):
		sel,ci,ri,data=dat
		print ("show",dat)
		if sel=="bb" or sel=="bcmd": self.showRib(ri)
		elif sel=="rib" or sel=="ccmd": self.showMeridian(ri)
		else: Gui.Selection.clearSelection()





def importCurves(obj):
	ss=obj.Spreadsheet
	print ss.Label
	if obj.ribtemplateSource != None and not obj.externSourcesOff:
		cs=obj.ribtemplateSource.Shape.Edge1.Curve
		curve=cs.getPoles()
		cl=len(curve)
		npa2ssa(curve,ss,2,3)
		print ("update curve",curve


	if obj.backboneSource != None and not obj.externSourcesOff:
		cs=obj.backboneSource.Shape.Edge1.Curve
		bb=cs.getPoles()
		bl=len(bb)
		npa2ssa(bb,ss,7,3)
		print ("update backbone",bb

def createNeedle(label="MyNeedle"):
	a=App.activeDocument().addObject("Part::FeaturePython",label)
	n=Needle(a)
	a.useSpreadsheet=True
	# gendata(a.Spreadsheet)
	a.ViewObject.DisplayMode="Shaded"
	return a



'''
table.clicked.disconnect(clicked)
table.entered.disconnect(entered)
'''


#global globdat
#globdat=None

def commitData(editor):
#	print ("commit data",editor)

	import nurbswb.needle_cmds
	reload(nurbswb.needle_cmds)
	global globdat
#	print globdat
	if globdat[0]=='ccmd':
		cn=cellname(int(globdat[1])+1,int(globdat[2])+3)
		old=globdat[3]
		nurbswb.needle_cmds.runCmd(old,cn,globdat[2],App.activeDocument().Spreadsheet)


def startssevents2():
	global table

	mw=FreeCADGui.getMainWindow()
	mdiarea=mw.findChild(QtGui.QMdiArea)

	App.activeDocument().Spreadsheet.ViewObject.startEditing(0)
	subw=mdiarea.subWindowList()
#	print len(subw)
	for i in subw:
#		print i.widget().metaObject().className()
		if i.widget().metaObject().className() == "SpreadsheetGui::SheetView":
			sheet = i.widget()
			table=sheet.findChild(QtGui.QTableView)

	table.clicked.connect(clicked)
#	table.entered.connect(entered)
	table.pressed.connect(pressed)




#	table.itemDelegate().commitData.connect(commitData)


'''
	from PySide import QtCore
	class SheetFilter(QtCore.QObject):
		def eventFilter(self,obj,event):
			print type(event)
			return False

	filter=SheetFilter()
	table.installEventFilter(filter)
	# table.removeEventFilter(filter)
 
'''




def getdata(index):
	r=index.row()
	c=index.column()

	if c == 0: # command fuer curve
		sel="ccmd"
		ri=r-2
		ci=0
		return sel,ci,ri,index.data()

	if c == 5: # command fuer curve
		sel="bcmd"
		ri=r-2
		ci=0
		return sel,ci,ri,index.data()


	if c in range(1,4):
		sel="rib"
		ci=c-1
	elif c in range(6,9):
		sel="bb"
		ci=c-6
	else:
		sel=None
		ci=-1

	ri=r-2

	return sel,ci,ri,index.data()


def run():
#			import nurbswb.nurbs
#		import nurbswb.needle as needle
#		reload( nurbswb.needle)

		dokname=App.ParamGet('User parameter:Plugins/nurbs').GetString("Document","Needle")
		try: App.closeDocument(dokname)
		except: pass

		App.newDocument(dokname)
		App.setActiveDocument(dokname)
		App.ActiveDocument=App.getDocument(dokname)
		Gui.ActiveDocument=Gui.getDocument(dokname)

		a=createNeedle()


		a.useBackbone=True
		a.useRibTemplate=True
		a.useRibCage=True
		#a.useMesh=True
		a.RibCount=0
		import nurbswb.needle_models
		reload (nurbswb.needle_models)
		# a.Proxy.getExampleModel(nurbswb.needle_models.modelBanana)
		model=App.ParamGet('User parameter:Plugins/nurbs').GetString("NeedleModel","modelSimple")

		print ("a.Proxy.getExampleModel(nurbswb.needle_models."+ model+")")
		eval("a.Proxy.getExampleModel(nurbswb.needle_models."+ model+")")


#		import Draft
#		points=[App.Vector(192.694291746,-129.634476444,0.0),App.Vector(130.429397583,-0.657173752785,40.0),App.Vector(-52.807308197,-112.73400116,0.0),App.Vector(-127.525184631,-71.8170700073,0.0),App.Vector(-205.801071167,-274.622741699,0.0),App.Vector(28.1370697021,-262.169769287,0.0),App.Vector(125.981895447,-187.451873779,0.0)]
#		# Draft BSpline
#		Draft.makeBSpline(points,closed=True,face=True,support=None)
#		import Part
#		bs=Part.BSplineCurve()
#		bs.interpolate(points)
#		bs.setPeriodic()
#		mybsc=App.ActiveDocument.addObject('Part::Feature','MyBSC')
#		mybsc.Shape=bs.toShape()

		App.activeDocument().recompute()
		Gui.SendMsgToActiveView("ViewFit")
		App.activeDocument().recompute()


		a.Proxy.startssevents()
		a.ViewObject.Selectable=False




#-----------------------------------------
# TEST CASE
#-----------------------------------------

if  __name__=='__main__':

	# test aus parametern
	import Draft
	import nurbswb
	import nurbswb.needle as needle
	reload( nurbswb.needle)

	dokname=App.ParamGet('User parameter:Plugins/nurbs').GetString("Document","Needle")
	try: App.closeDocument(dokname)
	except: pass

	App.newDocument(dokname)
	App.setactiveDocument()(dokname)
	App.ActiveDocument=App.getDocument(dokname)
	Gui.ActiveDocument=Gui.getDocument(dokname)

	if 0:
		points=[App.Vector(192.694291746,-129.634476444,0.0),App.Vector(130.429397583,-0.657173752785,0.0),App.Vector(-52.807308197,-112.73400116,0.0),App.Vector(-127.525184631,-71.8170700073,0.0),App.Vector(-205.801071167,-274.622741699,0.0),App.Vector(28.1370697021,-262.169769287,0.0),App.Vector(125.981895447,-187.451873779,0.0)]
		Draft.makeBSpline(points,closed=True,face=True,support=None)
		# BSpline

		points=[App.Vector(-37.2293014526,1.68375661825e-08,0.28248746792),App.Vector(132.959136963,6.57217134591e-06,110.262731687),App.Vector(149.817367554,1.45151301104e-05,243.523458616),App.Vector(-69.3403015137,2.18838984602e-05,367.150869505),App.Vector(-182.531646729,2.7960740423e-05,469.103353635),App.Vector(-256.549041748,5.67015768864e-05,951.294546262)]
		Draft.makeBSpline(points,closed=False,face=True,support=None)
		# Bspline001


		points=[App.Vector(-73.5499812578,-192.458589192,0.0),App.Vector(-35.2118430692,-245.401746512,0.0),App.Vector(-148.400562353,-232.622317741,0.0),App.Vector(-115.539281652,-172.376687886,0.0)]
		Draft.makeBSpline(points,closed=True,face=True,support=App.activeDocument().getObject("BSpline"))
		# Bspline002

		points=[App.Vector(-37.2293014526,1.68375661825e-08,-10),App.Vector(132.959136963,6.57217134591e-06,110.262731687),App.Vector(149.817367554,1.45151301104e-05,243.523458616),App.Vector(-69.3403015137,2.18838984602e-05,367.150869505),App.Vector(-182.531646729,2.7960740423e-05,469.103353635),App.Vector(-256.549041748,5.67015768864e-05,1200)]
		Draft.makeBSpline(points,closed=False,face=True,support=None)
		# Bspline003


	import nurbswb
	import nurbswb.needle as needle

	a=needle.createNeedle()

	#a.useBackbone=True
	#a.useRibTemplate=True
	a.useRibCage=True
	a.useMesh=True



#	a.ribtemplateSource=App.activeDocument().BSpline
#	a.backboneSource=App.activeDocument().BSpline001

	App.activeDocument()().recompute()

#	vp=needle.ViewProvider(a.ViewObject)
	App.activeDocument()().recompute()

	if 0:

		# zweiter koerper

		b=App.activeDocument().addObject("Part::FeaturePython","MyNeedle")
		bn=needle.Needle(b)


		'''
		b.useBackbone=True
		b.useRibTemplate=True
		b.useRibCage=True
		b.useMesh=True
		'''
		b.useSpreadsheet=True


		# b.Spreeadsheet=App.activeDocument()().addObject('Spreadsheet::Sheet','huhu')
		bss=b.Spreadsheet
		needle.gendata(bss)

		b.ribtemplateSource=App.activeDocument().BSpline002
		b.backboneSource=App.activeDocument().BSpline003
		App.activeDocument()().recompute()


		vp=needle.ViewProvider(b.ViewObject)


		Gui.SendMsgToActiveView("ViewFit")
		print ("fertig"
		 


		needle.importCurves(a)
		needle.importCurves(b)
		
	App.activeDocument()().recompute()
	App.activeDocument()().recompute()
	Gui.SendMsgToActiveView("ViewFit")

