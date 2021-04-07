def test1():

# test aus parametern
	import Draft
	import nurbswb
	import nurbswb.needle as needle
	reload( nurbswb.needle)

	try: App.closeDocument("Unnamed")
	except: pass

	App.newDocument("Unnamed")
	App.setActiveDocument("Unnamed")
	App.ActiveDocument=App.getDocument("Unnamed")
	Gui.ActiveDocument=Gui.getDocument("Unnamed")

	points=[App.Vector(192.694291746,-129.634476444,0.0),App.Vector(130.429397583,-0.657173752785,0.0),App.Vector(-52.807308197,-112.73400116,0.0),App.Vector(-127.525184631,-71.8170700073,0.0),App.Vector(-205.801071167,-274.622741699,0.0),App.Vector(28.1370697021,-262.169769287,0.0),App.Vector(125.981895447,-187.451873779,0.0)]
	Draft.makeBSpline(points,closed=True,face=True,support=None)
	# BSpline

	points=[App.Vector(-37.2293014526,1.68375661825e-08,0.28248746792),App.Vector(132.959136963,6.57217134591e-06,110.262731687),App.Vector(149.817367554,1.45151301104e-05,243.523458616),App.Vector(-69.3403015137,2.18838984602e-05,367.150869505),App.Vector(-182.531646729,2.7960740423e-05,469.103353635),App.Vector(-256.549041748,5.67015768864e-05,951.294546262)]
	Draft.makeBSpline(points,closed=False,face=True,support=None)
	# Bspline001


	points=[App.Vector(-73.5499812578,-192.458589192,0.0),App.Vector(-35.2118430692,-245.401746512,0.0),App.Vector(-148.400562353,-232.622317741,0.0),App.Vector(-115.539281652,-172.376687886,0.0)]
	Draft.makeBSpline(points,closed=True,face=True,support=App.ActiveDocument.getObject("BSpline"))
	# Bspline002

	points=[App.Vector(-37.2293014526,1.68375661825e-08,-10),App.Vector(132.959136963,6.57217134591e-06,110.262731687),App.Vector(149.817367554,1.45151301104e-05,243.523458616),App.Vector(-69.3403015137,2.18838984602e-05,367.150869505),App.Vector(-182.531646729,2.7960740423e-05,469.103353635),App.Vector(-256.549041748,5.67015768864e-05,1200)]
	Draft.makeBSpline(points,closed=False,face=True,support=None)
	# Bspline003

	a=App.ActiveDocument.addObject("Part::FeaturePython","MyNeedle")
	n=needle.Needle(a)

	'''
	a.useBackbone=True
	a.useRibTemplate=True
	a.useRibCage=True
	a.useMesh=True
	'''
	a.useSpreadsheet=True


	ss=a.Spreadsheet
	needle.gendata(ss)

	a.ribtemplateSource=App.ActiveDocument.BSpline
	a.backboneSource=App.ActiveDocument.BSpline001

	App.activeDocument().recompute()

	vp=needle.ViewProvider(a.ViewObject)
	App.activeDocument().recompute()



	# zweiter koerper

	b=App.ActiveDocument.addObject("Part::FeaturePython","MyNeedle")
	bn=needle.Needle(b)


	'''
	b.useBackbone=True
	b.useRibTemplate=True
	b.useRibCage=True
	b.useMesh=True
	'''
	b.useSpreadsheet=True


	# b.Spreeadsheet=App.activeDocument().addObject('Spreadsheet::Sheet','huhu')
	bss=b.Spreadsheet
	needle.gendata(bss)

	b.ribtemplateSource=App.ActiveDocument.BSpline002
	b.backboneSource=App.ActiveDocument.BSpline003
	App.activeDocument().recompute()


	vp=needle.ViewProvider(b.ViewObject)


	Gui.SendMsgToActiveView("ViewFit")
	print ("fertig"
	 


	needle.importCurves(a)
	needle.importCurves(b)

	App.activeDocument().recompute()
	App.activeDocument().recompute()




if 1:

	import Draft
	import nurbswb
	import nurbswb.needle as needle
	reload( nurbswb.needle)

	try: App.closeDocument("Unnamed")
	except: pass

	App.newDocument("Unnamed")
	App.setActiveDocument("Unnamed")
	App.ActiveDocument=App.getDocument("Unnamed")
	Gui.ActiveDocument=Gui.getDocument("Unnamed")

	a=needle.createNeedle()

	a.useBackbone=True
	a.useRibTemplate=True
	a.useRibCage=True
	a.useMesh=True

	App.activeDocument().recompute()
	Gui.SendMsgToActiveView("ViewFit")



