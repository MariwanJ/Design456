# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2021                                                     *
# *                                                                        *
# *                                                                        *
# * This library is free software; you can redistribute it and/or          *
# * modify it under the terms of the GNU Lesser General Public             *
# * License as published by the Free Software Foundation; either           *
# * version 2 of the License, or (at your option) any later version.       *
# *                                                                        *
# * This library is distributed in the hope that it will be useful,        *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# * Lesser General Public License for more details.                        *
# *                                                                        *
# * You should have received a copy of the GNU Lesser General Public       *
# * License along with this library; if not, If not, see                   *
# * <http://www.gnu.org/licenses/>.                                        *
# * Modified and adapter to Desing456 by:                                  *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************


# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- nurbs editor -
#--
#-- microelly 2016 v 0.2
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

from say import *

layout='''
VerticalLayoutTab:
#VerticalLayout:
    id:'main'

    VerticalLayout:

#        QtGui.QLabel:
#            setText:"***   N U R B S     E D I T O R   ***"


        HorizontalLayout:

            QtGui.QCheckBox:
                id: 'polegrid'
                setText: 'calculate PoleGrid'
                stateChanged.connect: app.calculatePoleGrid
                visibility: False

            QtGui.QCheckBox:
                id: 'setmode'
                setText: 'Pole only'
                setVisible: False

            QtGui.QCheckBox:
                id: 'relativemode'
                setText: 'Height relative'
                stateChanged.connect: app.relativeMode
                setChecked: True

            QtGui.QComboBox:
                id: 'focusmode'
    #            addItem: "single Pole"
    #            addItem: "VLine"
    #            addItem: "ULine"
    #            addItem: "UV Cross"
                addItem: "Rectangle"
                currentIndexChanged.connect: app.setFocusMode

    VerticalLayout:



        QtGui.QLabel:
            setText: "    A C T I O N "

        HorizontalLayout:


            QtGui.QLabel:
                setText:"Select Action:"

            QtGui.QComboBox:
                id: 'actionmode'
                addItem: "change Height relative"
                addItem: "set absolute Height and Weight"
                addItem: "Add VLine"
                addItem: "Add ULine"
#                addItem: "Elevate VLine"
#                addItem: "Elevate ULine"
#                addItem: "Elevate Rectangle"
#                addItem: "Elevate Circle"
                currentIndexChanged.connect: app.setActionMode


    VerticalLayout:

        QtGui.QLabel:
            setText: "    S E L E C T I O N"

        HorizontalLayout:

            QtGui.QLabel:
                id: 'pole1'
                setText: " pole1: "
            QtGui.QLabel:
                id: 'pole2'
                setText: " pole2: "


        HorizontalLayout:
            addSpacing: 0

            QtGui.QLabel:
                setText: "u"


            QtGui.QLineEdit:
                setText: "1"
                setMaxLength: 3
                editingFinished: app.getInfo
                id: 'u'

            QtGui.QComboBox:
                id: 'ucombo'
                currentIndexChanged.connect: app.processUcombo


            QtGui.QDial:
                setValue: 2
                id: 'ud'
                setMinimum: 1
                setMaximum: 7
                setTickInterval: 1
                valueChanged.connect: app.getDataFromNurbs
#            QtGui.QSpacerItem:
#                is:'spacer'


            QtGui.QLabel:
                setText:"v "

            QtGui.QLineEdit:
                setText:"1"
                id: 'v'
                returnPressed.connect: app.vFinished


            QtGui.QComboBox:
                id: 'vcombo'
                currentIndexChanged.connect: app.processVcombo


            QtGui.QDial:
                setValue: 2
                id: 'vd'
                setMinimum: 1
                setMaximum: 5
                setTickInterval: 1
                valueChanged.connect: app.getDataFromNurbs


#        HorizontalLayout:
#            QtGui.QPushButton:
#                setText: "u++"
#                clicked.connect: app.upp

#            QtGui.QPushButton:
#                setText: "u --"
#                clicked.connect: app.umm

#            QtGui.QPushButton:
#                setText: "v++"
#                clicked.connect: app.vpp


#            QtGui.QPushButton:
#                setText: "v --"
#                clicked.connect: app.vmm
#                clicked.connect: app.vmm

#        HorizontalLayout:
#            QtGui.QPushButton:
#                setText: "edit selected pole"
#                clicked.connect: app.getselection

#            QtGui.QPushButton:
#                setText: "set pole 1"
#                clicked.connect: app.setPole1

#            QtGui.QPushButton:
#                setText: "set pole 2"
#                clicked.connect: app.setPole2

        QtGui.QCheckBox:
            id: 'pole1active'
            setText: 'Pole 1 in change'
#            stateChanged.connect: app.relativeMode
            setChecked: True

        QtGui.QCheckBox:
            id: 'singlepole'
            setText: 'Single Pole mode'
#            stateChanged.connect: app.relativeMode
            setChecked: True


    VerticalLayout:

        QtGui.QLabel:
            setText: "    C O N F I G U R E"

        HorizontalLayout:
            addSpacing: 0

            QtGui.QLabel:
                setText: "height"

            QtGui.QLineEdit:
                setText: "10"
                id: 'h'

            QtGui.QComboBox:
                id: 'hcombo'
                currentIndexChanged.connect: app.processHcombo


            QtGui.QDial:
                setValue: -100
                setMinimum: -100
                setMaximum: 100
                id: 'hd'
                valueChanged.connect: app.modHeight
            QtGui.QLabel:
            QtGui.QLabel:

        HorizontalLayout:

            QtGui.QLabel:
                setText:"weight "

            QtGui.QLineEdit:
                setText:"10"
                id: 'w'

            QtGui.QComboBox:
                id: 'wcombo'
                currentIndexChanged.connect: app.processWcombo

            QtGui.QDial:
                setValue: 1
                setMinimum: 1
                setMaximum: 20
                id: 'wd'
                valueChanged.connect: app.modWeight
            QtGui.QLabel:
            QtGui.QLabel:


        HorizontalLayout:
            QtGui.QPushButton:
                id: "runbutton"
                setText: "Execute"
                clicked.connect: app.run

            QtGui.QPushButton:
                setText: "Recompute"
                clicked.connect: app.recompute


            QtGui.QPushButton:
                setText: "Close"
                clicked.connect: app.resetEdit


#        QtGui.QPushButton:
#            setText: "Commit relative values"
#            id: 'updateRelative'
#            clicked.connect: app.updateRelative


'''


class MyApp(object):

    def __init__(self):
        self.pole1=[1,5]
        self.pole2=[3,1]
        self.lock=False


    def resetEdit(self):
        Gui.ActiveDocument.resetEdit()
#        self.root.ids['main'].hide()
        import nurbswb.miki as miki
        reload(miki)
        mw=miki.getMainWindow()
        miki.getComboView(mw).removeTab(2)
        miki.getComboView(mw).setCurrentIndex(0)


    def updateDialog(self):
        self.root.ids['ud'].setMaximum(self.obj.Object.nNodes_u-2)
        self.root.ids['vd'].setMaximum(self.obj.Object.nNodes_v-2)

    def setFocusMode(self):
        rc=self.root.ids['focusmode'].currentText()
        print ("set Focus Mode is ", rc)


    def setPole1(self):
        u=self.root.ids['ud'].value()
        v=self.root.ids['vd'].value()
        self.root.ids['pole1'].setText("Pole 1:" + str([u+1,v+1]))
        self.pole1=[u,v]
        if self.root.ids['singlepole'].isChecked():
            self.pole2=[u,v]
            self.root.ids['pole2'].setText("Pole 2:" + str([u+1,v+1]))
        self.obj.Object.Proxy.showSelection(self.pole1,self.pole2)

    def setPole2(self):
        u=self.root.ids['ud'].value()
        v=self.root.ids['vd'].value()
        self.root.ids['pole2'].setText("Pole 2:" + str([u+1,v+1]))
        self.pole2=[u,v]
        if self.root.ids['singlepole'].isChecked():
            self.pole1=[u,v]
            self.root.ids['pole1'].setText("Pole 1:" + str([u+1,v+1]))
        self.obj.Object.Proxy.showSelection(self.pole1,self.pole2)

    def setActionMode(self):
        print ("set Action Mode")
        rc=self.root.ids['actionmode'].currentText()
        print (rc)
        if rc=="change Height relative":
            if not self.root.ids['relativemode'].isChecked():
                self.root.ids['relativemode'].click()
                self.getDataFromNurbs()
            self.root.ids['runbutton'].hide()
            return
        if rc=="set absolute Height and Weight":
            if self.root.ids['relativemode'].isChecked():
                self.root.ids['relativemode'].click()
                self.getDataFromNurbs()
            self.root.ids['runbutton'].hide()
            return
        self.root.ids['runbutton'].show()

    def recompute(self):
            self.updateDialog()
            self.setDataToNurbs()



    def run(self):
        rc=self.root.ids['actionmode'].currentText()
        print (rc)
        if rc=='Add ULine':
            v=self.root.ids['vd'].value()
            self.obj.Object.Proxy.addUline(v,0.5)
            self.updateDialog()
            self.setDataToNurbs()
            print ("done")
            return
        if rc=='Add VLine':
            u=self.root.ids['ud'].value()
            self.obj.Object.Proxy.addVline(u,0.5)
            # self.root.ids['ud'].setValue(self.root.ids['ud'].value()-1)
            self.updateDialog()
            self.setDataToNurbs()
            print ("done")
            return
        if rc=="change Height relative":
            if not self.root.ids['relativemode'].isChecked():
                self.root.ids['relativemode'].click()
            self.updateRelative()
            return
        if rc=="set absolute Height and Weight":
            if self.root.ids['relativemode'].isChecked():
                self.root.ids['relativemode'].click()
            self.update()
            return
        if rc== "Elevate VLine":
            u=self.root.ids['ud'].value()
            h=int(round(self.root.ids['hd'].value()))
            self.obj.Object.Proxy.elevateVline(u,h)
            self.updateDialog()
            self.setDataToNurbs()

            return
        if rc== "Elevate ULine":
            v=self.root.ids['vd'].value()
            h=int(round(self.root.ids['hd'].value()))
            self.obj.Object.Proxy.elevateUline(v,h)
            self.updateDialog()
            self.setDataToNurbs()
            return

        if rc== "Elevate Rectangle":
            v=self.root.ids['vd'].value()
            u=self.root.ids['ud'].value()
            h=int(round(self.root.ids['hd'].value()))
            dv=2
            du=1
            self.obj.Object.Proxy.elevateRectangle(v,u,dv,du,h)
            self.updateDialog()
            self.setDataToNurbs()
            return

        if rc== "Elevate Circle":
            v=self.root.ids['vd'].value()
            u=self.root.ids['ud'].value()
            h=int(round(self.root.ids['hd'].value()))
            r=2
            self.obj.Object.Proxy.elevateCircle2(v,u,r,h)
            self.updateDialog()
            self.setDataToNurbs()

            return


        print ("not implemented")




    def getselectionPoint(self):
        ''' get pole from gui pole number selection '''
        s=Gui.Selection.getSelection()
        print (s[0].Label)
        se=Gui.Selection.getSelectionEx()
        ss=se[0]

        sn=ss.SubElementNames
        # ('Vertex32',)
        polnr=int(sn[0][6:])
        print ("pole number ", polnr)

        uc=self.obj.Object.nNodes_v
        vc=self.obj.Object.nNodes_u

        u=(polnr-1) % vc
        v=(polnr-1) / vc
        self.root.ids['vd'].setValue(v)
        self.root.ids['ud'].setValue(u)
        self.setDataToNurbs()

    def getselection(self):
        ''' get pole from gui pole grid selection '''
        s=Gui.Selection.getSelection()
        print (s[0].Label)
        se=Gui.Selection.getSelectionEx()
        ss=se[0]

        sn=ss.SubElementNames
        # ('Edge32',)
        polnr=int(sn[0][4:])
        print ("edge number ", polnr)

        uc=self.obj.Object.nNodes_u
        vc=self.obj.Object.nNodes_v

        if polnr>uc:
            v=polnr-uc-1
        else:
            u=polnr-1

        polnr=int(sn[1][4:])
        print ("edge number ", polnr)

        if polnr>uc:
            v=polnr-uc-1
        else:
            u=polnr-1


        print("u,v",u,v)

        self.root.ids['vd'].setValue(v)
        self.root.ids['ud'].setValue(u)
#        self.setDataToNurbs()
        # write dialer data to the input fields
        self.root.ids['u'].setText(str(u+1))
        self.root.ids['v'].setText(str(v+1))
        if  self.root.ids['pole1active'].isChecked():
            self.setPole1()
        else:
            self.setPole2()
        print ("okay")
        try:
            polnr=int(sn[2][4:])
            print ("edge number 3 ", polnr)

            if polnr>uc:
                v=polnr-uc-1
            else:
                u=polnr-1

            polnr=int(sn[3][4:])
            print ("edge number 4 ", polnr)

            if polnr>uc:
                v=polnr-uc-1
            else:
                u=polnr-1


            print("u,v",u,v)

            self.root.ids['vd'].setValue(v)
            self.root.ids['ud'].setValue(u)

            self.root.ids['u'].setText(str(u+1))
            self.root.ids['v'].setText(str(v+1))
            if  self.root.ids['pole1active'].isChecked():
                self.setPole2()
            else:
                self.setPole1()
        except:
            pass
            # sayexc()





    def relativeMode(self):
        print("RELATVE MODE")
        print (self.root.ids['relativemode'].isChecked())
        if self.root.ids['relativemode'].isChecked():
            self.obj.Object.Proxy.gBase =  self.obj.Object.Proxy.g.copy()
#            try: self.root.ids['updateRelative'].show()
#            except: pass
#        else:
#            self.root.ids['updateRelative'].hide()
        print (self.obj.Object.Proxy.gBase.shape)
        print ("set  relative")

    def calculatePoleGrid(self):
        self.obj.Object.Proxy.calculatePoleGrid=self.root.ids['polegrid'].isChecked()


    def upp(self):
        ''' move pole selection u-axis up '''
        u=int(self.root.ids['ud'].value())
        u += 1
        uc=self.obj.Object.nNodes_u
        vc=self.obj.Object.nNodes_v

        if u >=uc : u=0
        self.root.ids['u'].setText(str(u+1))
        self.root.ids['ud'].setValue(u)
        self.setDataToNurbs()

    def vpp(self):
        v=int(self.root.ids['vd'].value())
        v += 1
        uc=self.obj.Object.nNodes_u
        vc=self.obj.Object.nNodes_v
        if v >=vc: v=0
        self.root.ids['v'].setText(str(v+1))
        self.root.ids['vd'].setValue(v)
        self.setDataToNurbs()

    def umm(self):
        u=int(self.root.ids['ud'].value())
        u -= 1
        if u <0: u=self.obj.Object.nNodes_u-1
        self.root.ids['u'].setText(str(u+1))
        self.root.ids['ud'].setValue(u)
        self.setDataToNurbs()

    def vmm(self):
        v=int(self.root.ids['vd'].value())
        v -= 1
        if v < 0: v= self.obj.Object.nNodes_v - 1
        self.root.ids['v'].setText(str(v+1))
        self.root.ids['vd'].setValue(v)
        self.setDataToNurbs()


    def update(self,force=False):
        ''' setDataToNurbs for update '''
        if not force:
            try:
                # don't setDataToNurbs during a locked transaction
                if self.lock: return
            except: pass
        print ("setDataToNurbs2")
        if not self.root.ids['setmode'].isChecked():
            print ("setze setmode")
            self.root.ids['setmode'].click()
            self.setDataToNurbs()
            self.obj.Object.Proxy.showSelection(self.pole1,self.pole2)



    def updateRelative(self):
        ''' setDataToNurbs for update '''
        try:
            # don't setDataToNurbs during a locked transaction
            if self.lock: return
        except: pass
        print ("setDataToNurbs2")
        if not self.root.ids['setmode'].isChecked():
            print ("setze setmode")
            self.root.ids['setmode'].click()
            self.setDataToNurbs(True)

            self.obj.Object.Proxy.showSelection(self.pole1,self.pole2)

#            id: 'updateRelative'
#            clicked.connect: app.updateRelative



    def setDataToNurbs(self,updateRelative=False):
        ''' setDataToNurbs a change in the dialog for the nurbs '''



        g=self.obj.Object.Proxy.g

        # data from the input fields
#        u=int(self.root.ids['u'].text())
#        v=int(self.root.ids['v'].text())
#        h=int(round(float(self.root.ids['h'].text())))

        # data from the dialers
        u=int(self.root.ids['ud'].value())
        v=int(self.root.ids['vd'].value())
        h=int(round(self.root.ids['hd'].value()))
        w=int(round(self.root.ids['wd'].value()))

        # write dialer data to the input fields
        self.root.ids['u'].setText(str(u+1))
        self.root.ids['v'].setText(str(v+1))
        self.root.ids['h'].setText(str(h))
        self.root.ids['w'].setText(str(w))


        rc=self.root.ids['focusmode'].currentText()
        if rc == 'single Pole':
            u1=u;u2=u
            v1=v;v2=v

        else:
            [u1,v1]=self.pole1
            [u2,v2]=self.pole2
            if u1>u2: u1,u2=u2,u1
            if v1>v2: v1,v2=v2,v1

        pts=[]
        for u in range(u1,u2+1):
            for v in range(v1,v2+1):

                if  self.root.ids['setmode'].isChecked():
                    print ("AKTUALISIERE",u,v)
                    if  self.root.ids['relativemode'].isChecked():
                        print ("!! set relative values ...")
                        self.obj.Object.Proxy.setpointRelativeZ(u,v,h,w)
                        if updateRelative:
                            self.obj.Object.Proxy.setpointRelativeZ(u,v,h,w,updateRelative)
                            h=0
                            self.root.ids['h'].setText(str(0))
                            self.root.ids['hd'].setValue(0)
                        #else:
                        #    self.obj.Object.Proxy.setpointRelativeZ(u,v,h,w)

                    else:
                        print ("set absolute ")
                        self.obj.Object.Proxy.setpointZ(u,v,h,w)
                else:
                    self.getInfo()
                    h=g[v][u][2]
                    print ("u,v,h",u,v,h)
                    uc=self.obj.Object.nNodes_u
                    vc=self.obj.Object.nNodes_v

                    self.root.ids['hd'].setValue(h)

                    self.root.ids['h'].setText(str(h))
                    print ("hole weight von ",((v)*uc+u,"uc,vc",uc,vc))
        #            print (self.obj.Object.weights
                    w=self.obj.Object.weights[(v)*uc+u]
                    self.root.ids['wd'].setValue(w)
        #            self.root.ids['w'].setText(str(h))
                    print ("hole  werte u,v ", u,v,"h,w",h,w)

        self.obj.Object.Proxy.updatePoles()
        self.obj.Object.Proxy.showGriduv()
#

        self.root.ids['setmode'].setChecked(False)


    def getDataFromNurbs(self):
        print ("start getDataFromNurbs")
        self.lock=True

        g=self.obj.Object.Proxy.g

        u=int(self.root.ids['ud'].value())
        v=int(self.root.ids['vd'].value())

        self.root.ids['u'].setText(str(u+1))
        self.root.ids['v'].setText(str(v+1))
        start=2
        self.root.ids['vcombo'].setCurrentIndex(int(v)-1)
        self.root.ids['ucombo'].setCurrentIndex(int(u)-1)

        # wenn nicht rechteckmode setze pole
        rc=self.root.ids['focusmode'].currentText()
#        if rc != 'Rectangle':
        if  self.root.ids['pole1active'].isChecked():
                self.setPole1()
        else:
                self.setPole2()

        h=g[v][u][2]

        uc=self.obj.Object.nNodes_u
        vc=self.obj.Object.nNodes_v
        if  self.root.ids['relativemode'].isChecked():
            self.root.ids['hd'].setValue(0)
            self.root.ids['h'].setText(str(0))
        else:
            self.root.ids['hd'].setValue(h)
            self.root.ids['h'].setText(str(h))

#        print ("hole weight von ",((v)*uc+u)
#        print ("hole weight von ",((v)*uc+u,"uc,vc",uc,vc)
#        print (self.obj.Object.weights





        w=self.obj.Object.weights[(v)*uc+u]

        self.root.ids['wd'].setValue(w)
        self.root.ids['w'].setText(str(w))

        print ("hole  werte u,v ", u,v,"h,w",h,w)

        try:
            ss=App.ActiveDocument.Shape
            ss.ViewObject.Transparency=90
        except:
            pass

        self.root.ids['setmode'].setChecked(False)
        self.lock=False
        print ("getDataFromNurbs fertig")


    def modHeight(self):
        ''' dialog has changed -> modify object '''
        u=int(self.root.ids['ud'].value())
        v=int(self.root.ids['vd'].value())
        h=int(round(self.root.ids['hd'].value()))
        self.root.ids['hcombo'].setCurrentIndex(100+int(h))
        self.update()


    def modWeight(self):
        ''' dialog has changed -> modify object '''
        u=int(self.root.ids['ud'].value())
        v=int(self.root.ids['vd'].value())
        w=int(round(self.root.ids['wd'].value()))
        self.root.ids['wcombo'].setCurrentIndex(int(w)-1)
        self.update()

    def getInfo(self):
        return

        print ("get obj")
        print (self.root)
        print (self.obj)
        print (self.obj.Object.Label)

        print ("shape ..")
        print (self.obj.Object.Proxy.g.shape)


    def vFinished(self):
        self.lock=False
        print ("vFinished")

    def processVcombo(self):
        if self.lock: return
        self.lock=True
        vc=self.root.ids['vcombo']
        rc=self.root.ids['vcombo'].currentText()
        print ("set vcombo Mode is ", rc)
        vc.clear()
        start=2
        ende=self.obj.Object.nNodes_v
        items=[str(n) for n in range(start,ende)]
        vc.addItems(items)
        vc.setCurrentIndex(int(rc)-start)
        self.root.ids['v'].setText(rc)
        self.root.ids['vd'].setValue(int(rc)-1)
        self.lock=False

    def processUcombo(self):
        if self.lock: return
        self.lock=True
        uc=self.root.ids['ucombo']
        rc=self.root.ids['ucombo'].currentText()
        print ("set ucombo Mode is ", rc)
        uc.clear()
        start=2
        ende=self.obj.Object.nNodes_u
        items=[str(n) for n in range(start,ende)]
        uc.addItems(items)
        uc.setCurrentIndex(int(rc)-start)
        self.root.ids['u'].setText(rc)
        self.root.ids['ud'].setValue(int(rc)-1)
        self.lock=False

    def processHcombo(self):
        if self.lock: return
        self.lock=True
        uc=self.root.ids['hcombo']
        rc=self.root.ids['hcombo'].currentText()
        if rc=='': rc='0'
        print ("set hcombo Mode is ", rc)
        uc.clear()
        start=2
        ende=self.obj.Object.nNodes_u
        start=-100
        ende=100
        items=[str(n) for n in range(start,ende)]
        uc.addItems(items)
        uc.setCurrentIndex(int(rc)-start)
        self.root.ids['h'].setText(rc)
        self.root.ids['hd'].setValue(int(rc))
        print ("rufe modHeight")
        self.modHeight()
        self.update(True)
        print ("done")
        self.lock=False


    def processWcombo(self):
        if self.lock: return
        self.lock=True
        uc=self.root.ids['wcombo']
        rc=self.root.ids['wcombo'].currentText()
        print ("set wcombo Mode is ", rc)
        uc.clear()
        start=1
        ende=20+1
        items=[str(n) for n in range(start,ende)]
        uc.addItems(items)
        uc.setCurrentIndex(int(rc)-1)
        self.root.ids['w'].setText(rc)
        self.root.ids['wd'].setValue(int(rc))
        self.lock=False


def mydialog(obj):

    import nurbswb.miki as miki
    reload(miki)

    app=MyApp()
    miki=miki.Miki()

    miki.app=app
    app.root=miki
    app.obj=obj

    miki.parse2(layout)
    miki.run(layout)

    miki.ids['ud'].setMaximum(obj.Object.nNodes_u-2)
    miki.ids['vd'].setMaximum(obj.Object.nNodes_v-2)
    for k in ['u','v','h','w']:
        miki.ids[k].setMaximumSize(50,40)

    start=2
    ende=obj.Object.nNodes_v
    items=[str(n) for n in range(start,ende)]
    miki.ids['vcombo'].addItems(items)

    start=2
    ende=obj.Object.nNodes_u
    items=[str(n) for n in range(start,ende)]
    miki.ids['ucombo'].addItems(items)

    miki.ids['hcombo'].addItems([str(n) for n in range(100,-100,-1)])
    miki.ids['hcombo'].setCurrentIndex(100)
    miki.ids['wcombo'].addItems([str(n) for n in range(1,21)])
    app.getDataFromNurbs()

    miki.ids['polegrid'].hide()
    miki.ids['focusmode'].hide()
    miki.ids['relativemode'].hide()
    miki.ids['w'].hide()
    miki.ids['wd'].hide()
    miki.ids['h'].hide()
    miki.ids['u'].hide()
    miki.ids['v'].hide()


    return miki

# mydialog(miki)
