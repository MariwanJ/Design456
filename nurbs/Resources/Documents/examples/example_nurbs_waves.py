import nurbs



if  App.ActiveDocument==None:
    App.newDocument("Unnamed")
    App.setActiveDocument("Unnamed")
    App.ActiveDocument=App.getDocument("Unnamed")
    Gui.ActiveDocument=Gui.getDocument("Unnamed")





#
#  example  for the use of the  nurbs node of the reconstructiuon workbench
#

def createWater():

    a=nurbswb.nurbs.makeNurbs()
    App.ActiveDocument.Nurbs.ViewObject.ShapeColor=(0.00,0.30,1.00)
    App.ActiveDocument.Nurbs.ViewObject.Transparency = 70

    # a  20 x 20  grid for the waves
    a.nNodes_u=20
    a.nNodes_v=20

    # generic data generator
    ps=a.Proxy.getPoints()
    g=a.Proxy.togrid(ps)

    #---------- apply Nurbs Tool  createWaves
    a.Proxy.createWaves()

    a.Label="Water"

    Gui.activeDocument().activeView().viewAxonometric()
    Gui.SendMsgToActiveView("ViewFit")



createWater()
