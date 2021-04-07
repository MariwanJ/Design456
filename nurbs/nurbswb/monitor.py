# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- a basic monitor object
#--
#-- microelly 2017 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------





import FreeCAD as App
import FreeCADGui as Gui



import numpy as np




import PySide
from PySide import  QtGui,QtCore

def run(window):

    anz=int(window.anz.text())
    print anz

    print window.r.isChecked()

    window.r.hide()
    window.hide()


def dialog():

    w=QtGui.QWidget()

    box = QtGui.QVBoxLayout()
    w.setLayout(box)
    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    l=QtGui.QLabel("Anzahl" )
    w.l=l
    box.addWidget(l)

    w.mina = QtGui.QLabel("Anzahl" )
    w.mina.setText('3')
    box.addWidget(w.mina)

    w.anz = QtGui.QLabel("Anzahl" )
    w.anz.setText('13')
    box.addWidget(w.anz)

    w.maxa = QtGui.QLabel("Anzahl" )
    w.maxa.setText('3')
    box.addWidget(w.maxa)

def dialogForce():

    w=QtGui.QWidget()

    box = QtGui.QVBoxLayout()
    w.setLayout(box)
    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    l=QtGui.QLabel("Anzahl" )
    w.l=l
    box.addWidget(l)

    w.mina = QtGui.QLabel("Anzahl" )
    w.mina.setText('3')
    box.addWidget(w.mina)

#    w.anz = QtGui.QLabel("Anzahl" )
#    w.anz.setText('13')
#    box.addWidget(w.anz)

    w.maxa = QtGui.QLabel("Anzahl" )
    w.maxa.setText('3')
    box.addWidget(w.maxa)



#    w.random=QtGui.QCheckBox("Zufall")
#    box.addWidget(w.random)

#    w.r=QtGui.QPushButton("run")
#    box.addWidget(w.r)
#    w.r.pressed.connect(lambda :run(w))

    w.show()
    return w


class PartFeature:
    def __init__(self, obj):
        obj.Proxy = self
        self.Object=obj


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



class Monitor(PartFeature):
    def __init__(self, obj):
        PartFeature.__init__(self, obj)

        obj.addProperty("App::PropertyLink","source","")
        # for a indirect dependency a 2nd source to trigger
        obj.addProperty("App::PropertyLink","source2","")
        obj.addProperty("App::PropertyFloat","val","")
        obj.addProperty("App::PropertyFloat","minVal","")
        obj.addProperty("App::PropertyFloat","maxVal","")
        obj.addProperty("App::PropertyBool","noExecute" ,"Base")
        obj.addProperty("App::PropertyEnumeration","mode" ,"Base")
        obj.mode=['lenght','force']
        
        ViewProvider(obj.ViewObject)

    def onDocumentRestored(self, fp):
        print ("onDocumentRestored "
        print fp.Label


    def onChanged(self, fp, prop):
        if prop in ["Shape", 'Spreadsheet']: return
        print ("onChanged",prop)


    def execute(proxy,obj):
        if obj.noExecute: return
        try: 
            if proxy.lock: return
        except:
            print("except proxy lock")
        proxy.lock=True
        if obj.mode=='force':
            proxy.monitorforce(obj)
        else:
            proxy.myexecute(obj)
        proxy.lock=False

    def monitorforce(proxy,obj):
        ss=obj.source.Shape
        pts=[v.Point for v in ss.Vertexes]

        lp=len(pts)
        su=0
        for i in range(1,lp-1):
            ll =((pts[i]-pts[i-1]).normalize().cross((pts[i+1]-pts[i]).normalize())).Length
            ls =((pts[i]-pts[i-1]).normalize().dot((pts[i+1]-pts[i]).normalize()))
#            print (pts[i]-pts[i-1]).normalize().cross((pts[i+1]-pts[i]).normalize())
#            print (pts[i]-pts[i-1]).normalize().dot((pts[i+1]-pts[i]).normalize())
#            print ll
#            
            print ("!! ",np.arctan2(ll,ls)*180./np.pi
            su += np.arctan2(ll,ls)*180./np.pi


        ss2=obj.source2.Shape

        pls=ss2.Curve.getPoles()
        basel=0
        ll=(len(pls)-1)/3
        for i in range(ll):
            basel += (pls[3*i]-pls[3*i+3]).Length

        print ("Bend force",su)
        print ("Base length",basel)
        print ("Stretch force:",ss2.Curve.length()-basel)

        sk=round(ss2.Curve.length()-basel,2)
        su=round(su,2)

        try: proxy.dialog
        except: 
            proxy.dialog=dialogForce()
        try:
            proxy.dialog.l.setText("Forces for " + str(obj.source.Label))
        except:
            pass
        proxy.dialog.mina.setText("BendArc: {:>10.1f} ".format(su))
        proxy.dialog.maxa.setText("Stretch: {:>10.1f}%".format(sk/basel*100))
        proxy.dialog.show()





    def myexecute(proxy,obj):
        try: proxy.dialog
        except: 
            proxy.dialog=dialog()
        try:
            proxy.dialog.l.setText("Curve length for " + str(obj.source.Label))
        except:
            pass
        proxy.dialog.mina.setText("MIN: " +str(obj.minVal))
        proxy.dialog.maxa.setText("MAX: " +str(obj.maxVal))
        proxy.dialog.show()
        mm=20
        if obj.source != None:
#            try:
                print obj.source.Label
                print ("Value and interval:", round(obj.source.Shape.Edge1.Length,1),obj.minVal,obj.maxVal)
                obj.source.ViewObject.LineColor=(1.0,1.0,1.0)
                if obj.source.Shape.Edge1.Length<obj.minVal:
                    obj.source.ViewObject.LineColor=(0.0,.0,1.0)
                elif obj.source.Shape.Edge1.Length>obj.minVal and obj.source.Shape.Edge1.Length<obj.minVal+mm:
                    j=1-(obj.minVal+mm-obj.source.Shape.Edge1.Length)/mm
                    print j
                    j=j*0.5
                    obj.source.ViewObject.LineColor=(0.,1.0,.0)
                elif obj.source.Shape.Edge1.Length<obj.maxVal and obj.source.Shape.Edge1.Length>obj.maxVal-mm:
                    j=(obj.maxVal-obj.source.Shape.Edge1.Length)/mm
                    print j
                    j=j*0.5
                    obj.source.ViewObject.LineColor=(.0,1.0,0.)
                elif obj.source.Shape.Edge1.Length>obj.maxVal:
                    obj.source.ViewObject.LineColor=(1.0,0.0,.0)
                obj.val=obj.source.Shape.Edge1.Length
                print ("huhu"
                proxy.dialog.anz.setText("VALUE: " + str(obj.val))
#            except:
                print ("kann nichts machen"


def run():
    a=App.activeDocument().addObject("Part::FeaturePython","MyMonitor")

    m=Monitor(a)
    a.source=Gui.Selection.getSelection()[0]
    a.source2=Gui.Selection.getSelection()[1]


#--------------------------
# monitor forces
def runforce():
    a=App.activeDocument().addObject("Part::FeaturePython","MyMonitor")
    m=Monitor(a)
    a.mode='force'
    a.source=Gui.Selection.getSelection()[0]
    a.source2=Gui.Selection.getSelection()[1]




if __name__ == '__main__':


    import Draft

    points = [
        App.Vector(41.6618804932,-29.8381633759,0.0),App.Vector(42.888874054,27.8303642273,0.0),
        App.Vector(-20.4684200287,39.654083252,0.0),App.Vector(-18.1259880066,-19.6876106262,0.0),
        App.Vector(-230.109481812,-79.8339004517,0.0),App.Vector(-201.932830811,105.248153687,0.0),
        App.Vector(77.6240005493,163.258956909,0.0),App.Vector(-91.4360580444,60.4969787598,0.0),
        App.Vector(63.25938797,88.1211624146,0.0),App.Vector(220.717285156,27.9004211426,0.0),
        App.Vector(203.590301514,-89.7786178589,0.0),App.Vector(153.866744995,14.088344574,0.0),
        App.Vector(112.982902527,-46.1323928833,0.0)
    ]

    spline = Draft.makeBSpline(points,closed=False,face=True,support=None)


    a=App.activeDocument().addObject("Part::FeaturePython","MyMonitor")
    m=Monitor(a)

    try:
        import nurbswb
        import nurbswb.createsketchspline
        reload(nurbswb.createsketchspline)
        nurbswb.createsketchspline.run()
        spline=App.ActiveDocument.ActiveObject
    except:
        spline = Draft.makeBSpline(points,closed=False,face=True,support=None)

    spline.ViewObject.LineWidth = 9.00

    a.source=spline
    a.minVal= spline.Shape.Length*0.95
    a.maxVal= spline.Shape.Length*1.05



