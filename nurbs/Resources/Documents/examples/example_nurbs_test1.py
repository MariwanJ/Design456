
import nurbs

if  App.ActiveDocument==None:
    App.newDocument("Unnamed")
    App.setActiveDocument("Unnamed")
    App.ActiveDocument=App.getDocument("Unnamed")
    Gui.ActiveDocument=Gui.getDocument("Unnamed")

def createNurbs():


    uc=6
    vc=10

    a=nurbswb.nurbs.makeNurbs()

    App.ActiveDocument.Nurbs.ViewObject.ShapeColor=(0.00,1.00,1.00)
    App.ActiveDocument.Nurbs.ViewObject.Transparency = 70

    a.nNodes_u=uc
    a.nNodes_v=vc


    # punkte holen
    ps=a.Proxy.getPoints()

    # daten in gitter
    g=a.Proxy.togrid(ps)
    g.shape


    # horizontale Linien einfgen

    if 0:
        g=addUline(g,4)
        g=addUline(g,7)
        g=addUline(g,1)

        g=addVline(g,6)
        g=addVline(g,9)
        g=addVline(g,10)

        movePoint(g,2,7,0,0,30)
        movePoint(g,3,8,5,-3,15)
        movePoint(g,1,1,5,-3,15)
        movePoint(g,3,4,0,0,-30)

        movePoint(g,6,12,0,0,-30)
        movePoint(g,4,15,5,5,30)

        movePoint(g,9,15,5,5,30)


    # punkte holen
    ps=a.Proxy.getPoints()

    # daten in gitter
    g=a.Proxy.togrid(ps)


    a.Proxy.movePoint(1,1,0,0,40)
    a.Proxy.movePoint(4,6,0,0,60)
    a.Proxy.movePoint(2,5,0,0,60)

    print ("add Uline")
    a.Proxy.addUline(8)
    a.Proxy.addUline(8)
    a.Proxy.addUline(8)

    a.Proxy.addUline(4)

    a.Proxy.addUline(3,0.4)
    a.Proxy.addUline(3,0.7)

    a.Proxy.addUline(2,0.1)
    a.Proxy.addUline(2,0.1)


    a.Proxy.addVline(4,0)
    a.Proxy.addVline(4,0)

    a.Proxy.addVline(3,1)
    a.Proxy.addVline(3,1)
    

    a.Proxy.addVline(2,0.33)
    a.Proxy.addVline(1,0.67)


    a.Proxy.elevateUline(4)
    a.Proxy.elevateUline(6,-30)

    a.Proxy.elevateVline(3)
    a.Proxy.elevateUline(2,-30)





createNurbs()
