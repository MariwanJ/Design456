# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- spreadsheet lib testcase
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


from spreadsheet_lib import *
#import nurbswb
reload (spreadsheet_lib)


ss1=createSpreadsheet(label='MySpreadsheet')
gendata(ss1)
table2Nurbs(ss1,"simpe gen data")


ss1=getSpreadsheet('MySpreadsheet')
ss1.set("E15","-4000")
App.activeDocument().recompute()
table2Nurbs(ss1,"E15")


#--------------------------------------------


pps=table2array(ss1)
pps.shape
array2Nurbs(pps,1,9,1,11)

array2Nurbs(pps,3,9,2,11)

array2Nurbs(pps,1,11,3,11)

pps[6,8,2]=2000
array2Nurbs(pps,1,11,3,11)

pps[4,6,2]=2000
array2Nurbs(pps,1,11,3,11)

pps[3,6,2]=-2000
array2Nurbs(pps,0,11,3,11)




xs=tabletop(ss1)
xs

ys=tableleft(ss1)
ys




# example from numpy 
x = np.arange(-5.00, 5.00, 0.5)
y = np.arange(-5.00, 5.00, 0.5)
xx, yy = np.meshgrid(x, y)
z = np.sin(xx**2+yy**2)

setSpreadsheet(ss1,x,y,z)
table2Nurbs(ss1,"initial")


z[4:7,4:7]=5
setSpreadsheet(ss1,x,y,z)
table2Nurbs(ss1,"mountain 5")


z[5:10,12:20]=3
setSpreadsheet(ss1,x,y,z)

table2Nurbs(ss1,"mountain 3")

z = (xx-3)*(xx+4)*xx+yy**2
z *= 0.1
setSpreadsheet(ss1,x,y,z)
table2Nurbs(ss1,"sum of cubic x and square y")

z=np.sin(2*xx)+yy**2*0.1
setSpreadsheet(ss1,x,y,z)
table2Nurbs(ss1,"sum of sin and square")



