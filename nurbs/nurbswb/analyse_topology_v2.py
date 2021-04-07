# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- analyse topology of parts
#--
#-- microelly 2017 v 0.3
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


#\cond
import FreeCAD,FreeCADGui
App=FreeCAD
Gui=FreeCADGui

import Part,Points

import networkx as nx
import random
import os 
import nurbswb

# modul variables
g=nx.Graph()
points={}



def ptokey(v):
	''' simplify vectors'''
	return (round(v.x,2),round(v.y,2),round(v.z,2))

def rf(v):
	''' vector modification hook'''
	return v
	ff=0.001
	return v+ FreeCAD.Vector(ff*random.random(),ff*random.random(),ff*random.random())


def createFaceMidPointmodel(a):
	'''create an extended model with facepoints'''

	fs=a.Shape.Faces

	pts=[]
	col=[]
	col=a.Shape.Edges

	for f in fs:
		c=f.CenterOfMass
		pts.append(c)
		for v in f.Vertexes: 
			p=v.Point
			pts.append(p)
			col.append(Part.makeLine(rf(c),rf(p)))

	# Points.show(Points.Points(pts))

	Part.show(Part.Compound(col))
	App.ActiveDocument.ActiveObject.ViewObject.hide()
	App.ActiveDocument.ActiveObject.ViewObject.PointSize=6.
	App.ActiveDocument.ActiveObject.ViewObject.LineWidth=1.
	App.ActiveDocument.ActiveObject.Label="Face Extend for " + a.Label

	return App.ActiveDocument.ActiveObject




def loadModel(s):
	''' map the Part <s> to a networx graph <g> with points set <points>'''

	sp=s.Shape

	for i,v in enumerate(sp.Vertexes):

		pp=(round(v.Point.x,2),round(v.Point.y,2),round(v.Point.z,2))

		try: points[pp]
		except: 
			points[pp]=i
			g.add_node(i,pos=(v.Point.x,v.Point.y),keys=[],quality=0,vector=ptokey(v.Point))

	for e in sp.Edges:

		p1=e.Vertexes[0].Point
		i1=ptokey(p1)

		p2=e.Vertexes[1].Point
		i2=ptokey(p2)

		print ("addedge",points[i1],points[i2])
		ge=g.add_edge(points[i1],points[i2],
			weight=round(e.Length,2),
			vector=p2-p1,
			fcedge=e # the real edge
			)

	# calculate some topological/metrical information for the vertexes

	for n in g.nodes():
		es=g.edge[n]
		sl=0 # sum of vector length
		vs=FreeCAD.Vector() # sum of vectors
		vds=0
		edirs=[]

		if len(es)>0:
			esl=[]
			for i,e in enumerate(es):
				esl.append(e)
				sl += g.edge[n][e]['vector'].Length
				vs += g.edge[n][e]['vector']
				edirs += [g.edge[n][e]['vector']] 

			vsn=FreeCAD.Vector(vs)

			# some trouble ist the sum of all vectors is zero
			if 0: # still look for a better solution
				if vsn.Length < 1: 
					vsn= g.edge[n][esl[0]]['vector'].cross(g.edge[n][esl[2]]['vector'])

				if vsn.Length < 1: 
					vsn= g.edge[n][esl[0]]['vector'].cross(g.edge[n][esl[1]]['vector'])


			if vsn.Length > 1: 
				vsn.normalize()
			else: vsn=0 

			for e in es:
				v = FreeCAD.Vector(g.edge[n][e]['vector'])
				v.normalize()
				vd=v.dot(vs)
				vds +=vd

		g.node[n]['ec']=len(es)
		g.node[n]['vs']=vs
		g.node[n]['sl']=sl
		g.node[n]['vds']=vds
		g.node[n]['vs']=vs
		g.node[n]['edirs']=edirs
		#g.node[n]['fdirs']=[]


#def displayMatplot():
#	# display in matplotlib
#	pos=nx.get_node_attributes(g,'pos')
#	nx.draw(g,pos)
#	#p-l-t.show()
#	# p-l-t.savefig("/tmp/path.png")


def getkey(n):
	l=g.node[n]['vs'].Length
	if l < 1: l= 100000

	return (g.node[n]['ec'],round(g.node[n]['sl']/l,4),round(g.node[n]['vds']/l,4))
	#return (g.node[n]['ec'],round(g.node[n]['sl']/l,16),round(g.node[n]['vds']/l,14))

def getkey(n):
	v2es=FreeCAD.Vector()
	for v in g.node[n]['edirs']:
		v2=FreeCAD.Vector(v).normalize()
		v2es += v2

#	print "huhu ", len( g.node[n]['fdirs'])
	v2fs=FreeCAD.Vector()
	for v in g.node[n]['fdirs']:
#		print v
		v2=FreeCAD.Vector(v)
		v2.normalize()
		v2fs += v2

#	return (#g.node[n]['ec'],
#		0,
#		FreeCAD.Vector(ptokey(v2fs)).Length,
#		FreeCAD.Vector(ptokey(v2es)).Length
#		)


#	print v2fs
#	print v2es
#	print "fdirs",len(g.node[n]['fdirs'])
#	print "edirs",len(g.node[n]['edirs'])

#	print "getkey",(
#		g.node[n]['ec'],
#		0,
#		FreeCAD.Vector(v2fs).Length,
#		FreeCAD.Vector(v2es).Length
#		)

#----------------
	return (
		#g.node[n]['ec'],
		#0,
		len(g.node[n]['fdirs'])+100*len(g.node[n]['edirs']),
		round(FreeCAD.Vector(ptokey(v2fs)).Length,2),
		round(FreeCAD.Vector(ptokey(v2es)).Length,2)
		)

#-----------------------------------------------------------------------------------
def getkeyg(g,n):
	v2es=FreeCAD.Vector()
	for v in g.node[n]['edirs']:
		v2=FreeCAD.Vector(v).normalize()
		v2es += v2

	if len(g.node[n]['edirs'])==4 and round(FreeCAD.Vector(ptokey(v2es)).Length,2) == 0.0:
		v0=FreeCAD.Vector(g.node[n]['edirs'][0]).normalize()
		v1=FreeCAD.Vector(g.node[n]['edirs'][1]).normalize()
		v2=FreeCAD.Vector(g.node[n]['edirs'][2]).normalize()
		v2es=v0.cross(v1)
		if v2es==FreeCAD.Vector():
			v2es=v0.cross(v2)

	v2fs=FreeCAD.Vector()
	for v in g.node[n]['fdirs']:
		v2=FreeCAD.Vector(v)
		v2.normalize()
		v2fs += v2


	return (
		len(g.node[n]['fdirs'])+100*len(g.node[n]['edirs']),
		round(FreeCAD.Vector(ptokey(v2fs)).Length,2),
		round(FreeCAD.Vector(ptokey(v2es)).Length,2)
		)
#---------------------------------------------------------------------------------

def createKeys():

	kp={}

	for n in g.nodes():
#			print n
#			print g.node[n]
			try: g.node[n]['fdirs']
			except: g.node[n]['fdirs']=[]
			key=getkey(n)
			g.node[n]['keys']= [key]
			g.node[n]['key']= key
			try: kp[key] += 1
			except: kp[key] = 1

	anz=0
	print "Keys, count occur"
	for k in kp:
		print (k,kp[k])
		if kp[k]==1: anz += 1

	print ("number of top level marker points:", len(g.nodes()),anz)
	return kp

def setQuality(nodes,kp):
	for n in nodes:
		key=g.node[n]['key']
		if kp[key]==1:
			g.node[n]['quality']=1



def getNeighborEdges(n):
	''' freecad edges from a point n '''
	col=[]
	nbs=g.neighbors(n)
	for nb in nbs:
		col +=  [g.edge[n][nb]['fcedge']]
	return col

#----------------------------------------------------

def displayNB(nodes):
	''' diasplay neighbor edges as Part'''
	col=[]
	for n in nodes:
		col +=getNeighborEdges(n)
	Part.show(Part.Compound(col))



def berechneKeyLevel(i=1):
	'''key for level i is the i-th neighbor sum of the keys'''

	for n in g.nodes():
		nbs=g.neighbors(n)
		kka={}
		aas=0
		bbs=0
		ccs=0
		for nb in nbs:
			(a,b,c)=g.node[nb]['keys'][i-1]
			aas += a
			bbs += b
			ccs += c

		try: g.node[n]['keys'][i]=(aas,bbs,ccs)
		except: g.node[n]['keys'].append((aas,bbs,ccs))


def werteausLevel(i=1):
	''' which points have unique keys at level i'''

	# count the key occurrences
	kp={}
	for n in g.nodes():
		if g.node[n]['quality']==0:
			key=g.node[n]['keys'][i]
			try: kp[key] += 1
			except: kp[key] = 1

	# which points have unique keys
	anz=0
	anzg=0

	#count the unique points
	for k in kp:
		if kp[k]==1: anz += 1

	#set the quality of the unique points 
	for n in g.nodes():
		if g.node[n]['quality']==0:
			key=g.node[n]['keys'][i]
			if kp[key]==1:
				g.node[n]['quality']=i+1
				anzg += 1
		else:
			anzg +=1

	print ("level",i,"found",anz,"found overall",anzg, "not identified till now",len(g.nodes())-anzg)
	return anz

def zeigeQ(i):
	''' display the indetification quality level as Sub Grid '''

	ns=[]
	for n in g.nodes():
		if g.node[n]['quality']==i:
			ns.append(n)

	# print ns
	displayNB(ns)
	App.ActiveDocument.ActiveObject.Label="Quality" +str(i)
	App.ActiveDocument.ActiveObject.ViewObject.LineColor=(
			random.random(),random.random(),random.random())



def run():
	'''run analysis for one selected object'''
	s=Gui.Selection.getSelection()
	model=s[0]
	runAna(model)


def runAna(model,silent=False):
	'''main analysis method'''

	print "NodesA",g.nodes()
	mp=createFaceMidPointmodel(model)
	print "NodesB",g.nodes()
	loadModel(mp)

	print "Model ",mp.Label
	print "NodesC",g.nodes()


	# link labels and geometry from freecad to networkx
	bm=model
	sp=bm.Shape

	for i,v in enumerate(sp.Vertexes):
		pp=(round(v.Point.x,2),round(v.Point.y,2),round(v.Point.z,2))
		try:
#			print (pp,i) 
#			print ("found ",points[pp])
			gi=points[pp]

			g.node[gi]["label"]=bm.Label+":Vertex"+str(i+1)
			g.node[gi]["Vertex"]=v
#			print g.node[gi]
		except: 
			print "NOT FOUND"
			pass


	for i,f in enumerate(sp.Faces):
		print ("Face ",i,len(f.Vertexes))
		for v in f.Vertexes:
#			print (v,ptokey(v.Point),points[ptokey(v.Point)])
			pix=points[ptokey(v.Point)]
#			print g.node[pix]
			
			#flaechennormale anfuegen
			(u,v)=f.Surface.parameter(v.Point)
#			print( pix,"Addiere Flaechennoirmalw",(u,v),f.normalAt(u,v))
			try:
				g.node[pix]['fdirs'].append(f.normalAt(u,v))
			except:
				g.node[pix]['fdirs'] = [(f.normalAt(u,v))]
			print "len fdirs",len(g.node[pix]['fdirs'] )


		c=f.CenterOfMass
		pp=(round(c.x,2),round(c.y,2),round(c.z,2))
		try:
#			print (pp,i) 
#			print ("found ",points[pp])
			gi=points[pp]

			g.node[gi]["label"]=bm.Label+":Face"+str(i+1)
			g.node[gi]["Face"]=f
#			print g.node[gi]
		except: 
			print "NOT FOUND"
			pass



	kp=createKeys()
	print g.nodes()
	
	setQuality(g.nodes(),kp)
	
	#hack
	#return

	#calculate and display top quality nodes
	if 1:
		ns=[]
		for n in g.nodes():
			if g.node[n]['quality']==1:
				ns.append(n)
		# print ns
		if not silent:
			displayNB(ns)
			App.ActiveDocument.ActiveObject.Label="Top Quality"
			App.ActiveDocument.ActiveObject.ViewObject.LineColor=(
					random.random(),random.random(),random.random())

	# calculate all levels
	for i in range(1,10):
		berechneKeyLevel(i=i)
		rc=werteausLevel(i=i)
		if rc==0:break

	last=i
	# zeige alle indentifizierten Punkte im Verbund
	if not silent:
		for i in range(1,last):
			zeigeQ(i)




	# hold the data for postprocessing in a global variable
	FreeCAD.g=g
	FreeCAD.a=model

#	print len(sp.Vertexes)
	addToVertexStore()


def runCompare():
	'''run analysis for more parts and display the results'''
	resetVertexStore()
	s=Gui.Selection.getSelection()
	for model in s:
#		g=nx.Graph()
#		FreeCAD.g=g
		print "Startrnstand"
		for v in g.nodes():
			print g.node[v]['fdirs']
			print g.node[v]['edirs']
			g.node[v]['fdirs']=[]
			g.node[v]['edirs']=[]
		print "--------------"
		print "NodesA",g.nodes()
		runAna(model,silent=True)
	displayVertexStore()




def displayQualityPoints():
	'''display the quality points as point clouds'''
	g=FreeCAD.g
	for q in range(1,7):
		pts=[]
		for v in g.nodes():
			#print g.node[v]['quality']
			if  g.node[v]['quality']==q: pts.append(g.node[v]['vector'])

#		print pts
		if pts<>[]:
			Points.show(Points.Points(pts))
			App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(
				random.random(),random.random(),random.random())
			App.ActiveDocument.ActiveObject.ViewObject.PointSize= 10

			App.ActiveDocument.ActiveObject.Label="Points Quality " +str(q)


def printData():
	'''print some diagnostic data'''
	g=FreeCAD.g
	for v in g.nodes():
		print v
		print g.node[v]['quality']
		print g.node[v]['keys']
		print g.node[v]['vector']
		print g.node[v]['keys'][g.node[v]['quality']-1]


def addToVertexStore():
	'''add the keys to the global vertex store'''

	try: FreeCAD.PT
	except: FreeCAD.PT={}

	print "addtoVertexStore"
	g=FreeCAD.g
	a=FreeCAD.a
	for v in g.nodes():
		
		try: g.node[v]['label']
		except: g.node[v]['label']='----'

		print "kkkk"
		print g.node[v]['label']
		print g.node[v]['quality']-1
		print g.node[v]['keys']
#		print g.node[v]['keys'][g.node[v]['quality']-1]
		print "ha"

#		key=(a.Label,g.node[v]['label'],v,g.node[v]['keys'][g.node[v]['quality']-1],"!>",
#			g.node[v]['quality'],"<!",g.node[v]['keys'])

		key=(a.Label,g.node[v]['label'],v,g.node[v]['keys'][0],"!>",
			g.node[v]['quality'],"<!",g.node[v]['keys'])

		try:
			if key not in FreeCAD.PT[g.node[v]['vector']]:
				FreeCAD.PT[g.node[v]['vector']] += [key]
				# print "added"
		except:
			#FreeCAD.PT[g.node[v]['vector']] =[(a.Label,g.node[v]['label'],v,g.node[v]['keys'][g.node[v]['quality']-1],g.node[v]['quality'])]
			FreeCAD.PT[g.node[v]['vector']] = [key]


def resetVertexStore():
	'''clear the vertex store for next analysis'''
	FreeCAD.PT={}
	print FreeCAD.PT


def printVertexStore(): 
	'''print the vertex store'''
	print "The vertex Store"
	for j in FreeCAD.PT:
		print
		print j
		vs=FreeCAD.PT[j]
		for v in vs:
			if str(v[1])<>'----':
				print v[1:-1]
#				print "	",v[-1]





def displayVertexStore(): 
	'''print the vertex store'''
	print "The vertex Store compare"
	found=0
	count=0
	keys={}
	keyd={}

	for j in FreeCAD.PT:
		#print
		#print j
		vs=FreeCAD.PT[j]
		for v in vs:
				if str(v[1]) =='----': continue
				k=v[3]
				count +=1
				try: 
					keys[k] += 1
					keyd[k] += [(j,v[:-2])]
					# print v
				except: 
					keys[k]=1 
					keyd[k] = [(j,v[:-2])]
	pts=[]
	for k in keys:
		if keys[k]>1:
			found += 1
			#print k,keys[k]
			#print keyd[k]
			pts.append(keyd[k][0][0])
			pts.append(keyd[k][1][0])
			# moeglich sortieren auf koerper einzeln
			#print keyd[k][0][1]
			# print keyd[k][1][1]

#	if pts<>[]:
#		#print pts
#		Points.show(Points.Points(pts))
#		App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(
#			random.random(),random.random(),random.random())
#		App.ActiveDocument.ActiveObject.ViewObject.PointSize= 10
#
#		App.ActiveDocument.ActiveObject.Label="Common Points "


#	print "no found -----------------------------"
	pts=[]
	for k in keys:
		if keys[k]==1:
#			print k,keys[k]
#			print keyd[k]
#			print "!!",keyd[k][0][0]
			pts.append(keyd[k][0][0])

	print
	print "nach keys ausgegeben"
	for k in keys:
		if k[0] %100 <>0: #ignore reine flaechen
			print
			print k
			for p in keyd[k]:
				print p[1]

	anz=0
	gps=[]
	print
	print "nach keys ausgegeben nur noch paare-------------------------------"
	for k in keys:
		first=True
		if k[0] %100 <>0: #ignore reine flaechen
			if len(keyd[k])==2:
				[p,q] = keyd[k]
				if p[1][0] <> q[1][0]:
					if p[1][1].startswith( p[1][0]):
						if first:
							print
							print k
							first=False
						print p[1]
#						print p
						print q[1]
						anz +=1
						gps += [FreeCAD.Vector(p[0]),FreeCAD.Vector(q[0])]

	print "gefundene paare ",anz

	if gps<>[]:
		Points.show(Points.Points(gps))
		App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(
			random.random(),random.random(),random.random())
		App.ActiveDocument.ActiveObject.ViewObject.PointSize= 10

		App.ActiveDocument.ActiveObject.Label="Gefundene unique keys -- bestes ergebnis"



#	if pts<>[]:
#		#print pts
#		Points.show(Points.Points(pts))
#		App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(
#			random.random(),random.random(),random.random())
#		App.ActiveDocument.ActiveObject.ViewObject.PointSize= 10
#
#		App.ActiveDocument.ActiveObject.Label="No common Points "
#
#	print "common found:",found
#	print count


def loadTest1():
	print __file__
	# hier relativen pfad reintun
	FreeCAD.open(u"/home/thomas/Schreibtisch/zwei_gleiche_fenster.fcstd")
	App.setActiveDocument("zwei_gleiche_fenster")
	App.ActiveDocument=App.getDocument("zwei_gleiche_fenster")
	Gui.ActiveDocument=Gui.getDocument("zwei_gleiche_fenster")



def loadTest2():
	__dir__ = os.path.dirname(nurbswb.__file__)

	FreeCAD.open(__dir__+"/../testdata/zwei_gleiche_fenster.fcstd")
	App.setActiveDocument("zwei_gleiche_fenster")
	App.ActiveDocument=App.getDocument("zwei_gleiche_fenster")
	Gui.ActiveDocument=Gui.getDocument("zwei_gleiche_fenster")

def getkeytab(g,nodes):
	keys={}
	for n in nodes:
#		print n
#		print g.node[n]
		k=getkeyg(g,n)
		try: keys[k] += [n]
		except: keys[k] = [n]
	return keys

def getUniques(keys):
	us=[]
	for k in keys:
		if len(keys[k])==1:
			us += keys[k]
	return us

	
def Test4():
	g=FreeCAD.g
	print "Test 4"
#	print g.nodes()

	keys=getkeytab(g,g.nodes())

	print "keytab all results ..."
	for k in keys:
		print (k,keys[k])
		
	uniqs=getUniques(keys)
	print "uniques start "
	print uniqs

	for n in uniqs:
		g.node[n]['upath']=[n]


	found=True
	for i in range(8):
		if not found: break
		
		found=False
		print "loop i= ",i
		for n in uniqs:
			nbs=g.neighbors(n)
			nbs2=[]
			for na in nbs:
				if na not in uniqs:
					nbs2.append(na)

			keys=getkeytab(g,nbs2)
			
#			print
#			print ("node ",n,getkeyg(g,n),nbs2)
#			print nbs
			
			for k in keys:
				print (k,keys[k])

			uniqs2=getUniques(keys)
			if uniqs2<>[]:
				print "----------------------------------uniques2: ",uniqs2
				for u in uniqs2:
					if u not in uniqs: 
		#				print "-add--------------------",u
						found=True
						uniqs += [u]
						g.node[u]['upath']= g.node[n]['upath']+[u]

	print
	print ("all uniqs ",uniqs)

	for n in uniqs:
		print (k,n,g.node[n]['label'],g.node[n]['upath'])

	ups=[]
	for n in uniqs:
			ups.append(FreeCAD.Vector(g.node[n]['vector']))

	Points.show(Points.Points(ups))
	App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(
		random.random(),random.random(),random.random())
	App.ActiveDocument.ActiveObject.ViewObject.PointSize= 10

	App.ActiveDocument.ActiveObject.Label="Eindeutige Punkte"

	print
	print "nicht zuordenbar ..."
	noups=[]
	for n in g.nodes():
		if n not in uniqs:
			k=getkeyg(g,n)
			print (k,n,g.node[n]['label'],g.node[n]['vector'])
#			print (n,g.node[n]['label'])
#			print g.node[n]['edirs']
#			print g.node[n]['fdirs']
			noups.append(FreeCAD.Vector(g.node[n]['vector']))

	Points.show(Points.Points(noups))
	App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(
		random.random(),random.random(),random.random())
	App.ActiveDocument.ActiveObject.ViewObject.PointSize= 10

	App.ActiveDocument.ActiveObject.Label="Nich eindeutige Punkte"

import time
def Test3():
	import nurbswb.fem_edgelength_mesh
	for i in range(1):
		reload (nurbswb.fem_edgelength_mesh)
		nurbswb.fem_edgelength_mesh.run()
		Gui.updateGui()
		print "i ",i
		time.sleep(0.01)
	

'''

s=Gui.Selection.getSelection()
len(s[0].Shape.Vertexes)

'''
