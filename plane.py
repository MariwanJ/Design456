import os
import sys
import FreeCAD
import FreeCADGui as Gui
import pivy.coin as coin
import init
import Draft as _draft


def dim_dash(p1, p2,color,LineWidth):
    dash = coin.SoSeparator()
    v = coin.SoVertexProperty()
    v.vertex.set1Value(0, p1)
    v.vertex.set1Value(1, p2)
    line = coin.SoLineSet()
    line.vertexProperty = v
    style = coin.SoDrawStyle()
    style.lineWidth = LineWidth
    # sg.addChild(style)
    dash.addChild(style)
    dash.addChild(color)
    dash.addChild(line)
    return dash


class Grid:
    collectGarbage=[]
    def __init__(self, view):
        self.view = view
        self.sg =None
        self.collectGarbage=[]  #Keep the nodes for removing
        self.sg=None
        
    def removeAllAxis(self):
        self.removeGarbage()
    
    def Activated(self):
        try:
            self.sg = Gui.ActiveDocument.ActiveView.getSceneGraph()
            # Draw xy plane
            self.drawXYPlane()
            # Draw Z plane
            self.drawZAxis()
            #Draw Axis 
            self.draw_XandYandZZeroAxis()

        except Exception as err:
            FreeCAD.Console.PrintError("'Plane' Failed. "
                                       "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
       
    def drawZAxis(self):
        col= coin.SoBaseColor()
        col.rgb= (237, 225, 0) # Yellow 
        LengthOfGrid = 500  # mm
        bothSideLength = LengthOfGrid/2
        GridSize = 5
        counter = LengthOfGrid
        try:
            line = []
            for i in range(0, counter, GridSize):
                #X direction
                P1x=-2
                P1y=0 
                P2x=+2
                P1y=0
                line.append(dim_dash((P1x,P1y,-bothSideLength+i ),(P2x,P1y , -bothSideLength+i ),col,1))  # x                
            for i in line:
                self.sg.addChild(i)
                self.collectGarbage.append(i)
                
        except Exception as err:
            FreeCAD.Console.PrintError("'Plane' Failed. "
                                       "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno) 
                            
    def draw_XandYandZZeroAxis(self):
        from constant import stndColor
        col1= coin.SoBaseColor()
        col2= coin.SoBaseColor()
        col3= coin.SoBaseColor()
        col1.rgb= stndColor.get_red()      # RED
        col2.rgb= stndColor.get_green()    # GREEN
        col3.rgb= stndColor.get_blue() # BLUE
        
        LengthOfGrid = 1000  # mm
        counter = LengthOfGrid
        try:
            line = []
            line.append(dim_dash((-LengthOfGrid,0.0,0.0),(+LengthOfGrid,0.0 , 0.0),col1,5))  # x
            line.append(dim_dash((0.0, -LengthOfGrid,0.0),(0.0, +LengthOfGrid, 0.0),col2,5))  # y
            line.append(dim_dash((0.0, 0.0,-LengthOfGrid),(0.0, 0.0, LengthOfGrid),col3,5))  # y
            
            for i in range(0, 3):
                self.sg.addChild(line[i])
                self.collectGarbage.append(line[i])

        except Exception as err:
            FreeCAD.Console.PrintError("'Plane' Failed. "
                                       "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno) 

        except Exception as err:
            FreeCAD.Console.PrintError("'Plane' Failed. "
                                       "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        
    def removeGarbage(self):
        for i in (self.collectGarbage):
                self.sg.removeChild(i)
            
        self.collectGarbage.clear()
        
    def drawXYPlane(self):
        from constant import stndColor
        col= coin.SoBaseColor()
        col.rgb=stndColor.get_blue4()  
        LengthOfGrid = 1000  # mm
        bothSideLength = LengthOfGrid/2
        GridSize = 5
        counter = LengthOfGrid
        try:
            line = []
            count5Cells=0
            lineSize=1
            for i in range(0, counter, GridSize):
                #X direction
                P1x=-bothSideLength
                P1y=-bothSideLength+i 

                #y direction
                P3x=-bothSideLength+i 
                P3y=-bothSideLength

                if count5Cells ==0:
                    lineSize=4
                else:
                    lineSize=1
                #don't draw the line on 0,±y and ±x,0
                #TODO: Draw x, y in the correct color 
                if  P1y != 0:    
                    line.append(dim_dash((P1x,P1y,0.0),(-P1x,P1y , 0.0),col,lineSize))  # x
                
                if P3x !=0 :
                    line.append(dim_dash((P3x, P3y,0.0),(P3x, -P3y, 0.0),col,lineSize))  # y
                
                count5Cells=count5Cells+1
                if count5Cells==5 : 
                    count5Cells=0
            for i in line:
                self.sg.addChild(i)
                self.collectGarbage.append(i)

        except Exception as err:
            FreeCAD.Console.PrintError("'Plane' Failed. "
                                       "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno) 

        except Exception as err:
            FreeCAD.Console.PrintError("'Plane' Failed. "
                                       "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
