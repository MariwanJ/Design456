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
# * Modified and adapted to Desing456 by:                                  *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- miki - my kivy like creation tools
#--
#-- microelly 2016
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

from say import *
 
def getMainWindow():
   "returns the main window"
   toplevel = QtGui.qApp.topLevelWidgets()
   for i in toplevel:
       if i.metaObject().className() == "Gui::MainWindow":
           return i
   raise Exception("No main window found")

def getComboView(mw):
   dw=mw.findChildren(QtGui.QDockWidget)
   for i in dw:
       if str(i.objectName()) == "Combo View":
           return i.findChild(QtGui.QTabWidget)
       elif str(i.objectName()) == "Python Console":
           return i.findChild(QtGui.QTabWidget)
   raise Exception ("No tab widget found")

def ComboViewShowWidget(widget,tabMode=False):

    # stop to default
    if not tabMode:
        widget.show()
        return

    mw = getMainWindow()
    tab = getComboView(getMainWindow())
    c=tab.count()

    # clear the combo  window
    for i in range(c-1,1,-1):
        tab.removeTab(i)

    # start the requested tab
    tab.addTab(widget,"Nurbs WB")
    tab.setCurrentIndex(2)

    print ("ComboViewShowWidget done")


def creatorFunction(name):

#    print ("creator Function :", name
    if name.startswith('Part.'):
        [a,c]=name.split('.')
        return "App.activeDocument().addObject('Part::"+c+"','test')"

    if name.startswith('So'):
        return "coin."+name+'()'

    if name.startswith('QtGui'):
        return name+"()"

    if name.startswith('MyQtGui'):
        return name+"()"

    if name.startswith('Animation'):
        [a,c]=name.split('.')
        return 'Animation.create' +c + '()'


    if name in ['Plugger','Manager']:
        return 'Animation.create'+name+'()'

    #default method
    return name+'()'

import re
import pivy
from pivy import coin

# a test method
# YourSpecialCreator=Animation.createManager

def  fv2(name="vertical",title=''):
    ''' create as a dock widget '''

    t=QtGui.QLabel("my widget")
#    w=MyDockWidget(t,"Reconstruction WB")
    w=MyWidget(t,"Reconstruction WB")

    if title !='': w.setWindowTitle(title)


    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    ComboViewShowWidget(w,True)

    # store it to FC.w5
    try: App.w5.append(w)
    except: App.w5=[w]

    return w


def  fv(name="vertical",title=''):

    # w=QtGui.QWidget()
    t=QtGui.QLabel("my widget")
    w=MyDockWidget(t,"Nurbs WB")
    
###    w.setStyleSheet("QWidget { font: bold 18px;color:brown;border-style: outset;border-width: 3px;border-radius: 10px;border-color: blue;}")

    if title !='': w.setWindowTitle(title)
    
    layout = QtGui.QVBoxLayout()
    layout.setAlignment(QtCore.Qt.AlignTop)
    #w.layout=layout
    #w.setLayout(layout)

    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    w.show()
    # ComboViewShowWidget(w,True)
    try:
        App.w5.append(w)
    except:
        App.w5=[w]

    return w

def  fv3(name="vertical",title=''):
    ''' vertical  layout but not a dock widget'''

    w=QtGui.QWidget()
#    w.setStyleSheet("QWidget { font: bold 18px;color:brown;border-style: outset;border-width: 3px;border-radius: 10px;border-color: blue;}")

    if title !='': w.setWindowTitle(title)

    layout = QtGui.QVBoxLayout()
    layout.setAlignment(QtCore.Qt.AlignTop)
    #w.layout=layout
    #w.setLayout(layout)

#    w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
#    w.show()

    try: App.w5.append(w)
    except: App.w5=[w]
    return w



def  fh(name="horizontal",title=''):
    w=QtGui.QWidget()
    #w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    
###    w.setStyleSheet("QWidget { font: bold 18px;color:blue;border-style: outset;border-width: 3px;border-radius: 10px;border-color: blue;}")
    layout = QtGui.QHBoxLayout()
    layout.setAlignment(QtCore.Qt.AlignLeft)
    w.setLayout(layout)
    # Gruppenname setzen:
    #pB= QtGui.QLabel("name")
    #pB.setStyleSheet("QWidget { font: bold 18px;color:red;border-style: outset;border-width: 3px;border-radius: 10px;border-color: blue;}")
    #layout.addWidget(pB)

    if title !='': w.setWindowTitle(title)
    #w.show()
    #ComboViewShowWidget(w,False)
    w.layout=layout
    return w

    
def  fh2(name="vertik horizontal",title=''):
    w=QtGui.QWidget()
    #w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    
###    w.setStyleSheet("QWidget { font: bold 18px;color:blue;border-style: outset;border-width: 3px;border-radius: 10px;border-color: blue;}")
    layout = QtGui.QVBoxLayout()
    layout.setAlignment(QtCore.Qt.AlignLeft)
    w.setLayout(layout)
    #pB= QtGui.QLabel("name")
    #pB.setStyleSheet("QWidget { font: bold 18px;color:red;border-style: outset;border-width: 3px;border-radius: 10px;border-color: blue;}")
    #layout.addWidget(pB)
    if title !='': w.setWindowTitle(title)
    #w.show()
    #ComboViewShowWidget(w,False)
    w.layout=layout
    return w
    

def  ftab2(name="horizontal"):
    w=QtGui.QWidget()
###    w.setStyleSheet("QWidget { font: bold 18px;color:blue;border-style: outset;border-width: 3px;border-radius: 10px;border-color: blue;}")
    layout = QtGui.QHBoxLayout()
    layout.setAlignment(QtCore.Qt.AlignLeft)
    w.setLayout(layout)
    pB= QtGui.QLabel(name)
    pB.setStyleSheet("QWidget { font: bold 18px;color:red;border-style: outset;border-width: 3px;border-radius: 10px;border-color: blue;}")
    layout.addWidget(pB)
    # w.show()
    ComboViewShowWidget(w,False)

    w1=QtGui.QWidget()
###    w.setStyleSheet("QWidget { font: bold 18px;color:blue;border-style: outset;border-width: 3px;border-radius: 10px;border-color: blue;}")
    layout1 = QtGui.QVBoxLayout()
    layout1.setAlignment(QtCore.Qt.AlignLeft)

    w1.setLayout(layout1)

    pB1= QtGui.QLabel("name1")
    layout1.addWidget(pB1)
    pB1= QtGui.QLabel("name1")
    layout1.addWidget(pB1)

    layout.addWidget(w1)

    w2=QtGui.QWidget()
###    w.setStyleSheet("QWidget { font: bold 18px;color:blue;border-style: outset;border-width: 3px;border-radius: 10px;border-color: blue;}")
    layout2 = QtGui.QVBoxLayout()
    layout2.setAlignment(QtCore.Qt.AlignLeft)

    w2.setLayout(layout2)

    pB2= QtGui.QLabel("name2")
    layout2.addWidget(pB2)
    pB1= QtGui.QLabel("name1")
    layout2.addWidget(pB1)

    layout.addWidget(w2)
    



    w.layout=layout
    return w


# name mappings from layout string to methods

VerticalLayout=fh2
VerticalLayoutTab=fv2

#VerticalLayout=fv
MainWindow=fv

HorizontalLayout=fh

#***************


class Miki():
    def __init__(self):
        self.objects=[]
        self.anchors={}
        self.indents=[]
        self.olistref=[]
        self.indpos=-1
        self.app=None
        self.ids={}
        self.classes={}
        getdockwindowMgr()



    def parse2(self,s):

        ls=s.splitlines()

        app=self.app
        line=0
        depth=0
        d=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ln=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        refs={}
        rs=[]
        r=None
        r=[-1,0,0,'']
        for l in ls:
            ltxt=l
#            print l
#            print  ln

            if r: 
                rs.append(r)
                r=[-1,0,0,'']
            line += 1
#            print l
            if l.startswith('#:'):
                res=re.search("#:\s*(\S.*)",l)
                r=[l,line,-1,'cmd',res.group(1)]
                continue

            if l.startswith('#'):
                continue
                
            res=re.search("\<(\S.*)\>:",l)
            if res:
                    parent=0
                    ln[0]=line
                    depth=0
                    r=[l,line,parent,"local class",res.group(1)]
                    self.classes[res.group(1)]=line
                    continue

            res=re.search("(\s*)(\S.*)",l)
            if res:
                l=len(res.group(1))
                
                if l==0:
                    depth=0
                if d[depth]<l:
                    depth += 1
                elif d[depth]>l:
                    depth -= 1
#                print d
#                print depth
                try:
                    d[depth]=l
                except:
                    print ("error ")
                    print ([l, ltxt])
                    pass
                #ln[depth]=line
                #parent=ln[depth-1]
                parent=ln[l-1]
                ln[l]=line
#                print ["einzug",l,"depth",depth,"parent",parent,ln]
#                print 
                r=[l,line,parent,res.group(2)]
                r=[l,line,parent,res.group(2),depth,ln]
                st=res.group(2)
                
                res=re.search("(\S+):\s*\*(\S+)",st)
                if res:
                    r=[l,line,parent,'link',res.group(1),res.group(2),refs[res.group(2)]]
    #                print refs[res.group(2)]
                    continue

                res=re.search("(\S+):\s*&(\S+)\s+(\S.*)",st)
                if res:
                    r=[l,line,parent,"anchor attr",res.group(1),res.group(2),res.group(3)]
                    refs[res.group(2)]=line
                    continue

                res=re.search("(\S+):\s*&(\S+)",st)
                if res:
                    r=[l,line,parent,"anchor",res.group(1),res.group(2)]
                    refs[res.group(2)]=line
                    continue

                res=re.search("(\S+[^:]):\s*([^:]\S.*)",st)
                if res:
#                    print app
                    r=[l,line,parent,"att val",res.group(1),eval(res.group(2))]
                    if res.group(1) =='Name':
#                        print ("setze Namen von parent"
#                        print parent
#                        print rs[parent]
                        rs[parent].append(res.group(2))
#                        print rs[parent]
                    continue

                res=re.search("\s*(\S):\s*([^:]\S.*)",st)
                if res:
                    print (app)
                    r=[l,line,parent,"att val",res.group(1),eval(res.group(2))]
                    if res.group(1) =='Name':
#                        print ("setze Namen von parent"
#                        print parent
#                        print rs[parent]
                        rs[parent].append(res.group(2))
#                        print rs[parent]
                    continue
                else:
#                    print ("tttt"
#                    print st
                    res=re.search("(\S+):",st)
                    if res:    
                        r=[l,line,parent,"obj", res.group(1),'no anchor']

        self.anchors=refs
        self.lines=rs



        debug = 0
        if debug:
            print
            print ("lines parsed ...")
            for r in rs:
                    print (r)
            if  len(self.anchors.keys()) >0:
                print 
                print ("Anchors ....")
                print
                print (self.anchors)
                print


    def build(self):

        for l in self.lines:

            if l[3]=='cmd':
                try: 
                    exec(l[4])
                except:
                    sayexc(str(["Error exec:",l[4]]))
                continue
            if l[3]=='obj' or  l[3]=='anchor' or  l[3]=='local class':
                    name=l[4]
#                    print name
                    try: 
#                        print ("class check ..."
#                        print (self.classes
                        self.classes[name]
                        f=name+"()"
                        f2=name
                    except:
                        f=creatorFunction(l[4])

                    if len(l)<7: # no name for object
                        l.append('')
#                    print ("**", f



                    if l[3]=='local class':
                        exec("class "+name+"(object):pass")
                        h=eval(f2)
                    else:
                        h=eval(f)
#                    print h
                    if len(l)<7:
                        l.append(None)
                    l.append(h)
                    self.objects.append(h)
            if  l[2] != 0:
                if l[4]=='Name': continue
                if l[3]=='obj' or  l[3]=='anchor':
                    parent=self.lines[l[2]][7]
#                    print parent
#                    print l
#                    print l[7]
                    self.addChild(parent,l[7])
#                    print l
                if l[3]=='link':
                    parent=self.lines[l[2]][7]
                    try:
                        child=self.lines[l[6]][7]
                        self.addChild(parent,child)
                    except:
                        # link eines attribs
                #----------------------------------
                        method=l[4]
                        v=self.lines[l[6]][6]
#                        print ("check atts"
                        kk=eval("parent."+l[4])
                        cnkk=kk.__class__.__name__
#                        print ["vor function ", cnkk]
                        
                        if cnkk.startswith('So'):
#                            print ("So ..."
#                            print v
#                            print v.__class__
                            ex="parent."+method+".setValue(" +str(v) + ")"
                            exec(ex)
                            continue
                        if cnkk =='builtin_function_or_method':
                            # qt 2...
#                            print ("mche was"
#                            print v
#                            print ("parent."+l[4]
                            kk(v)
#                            print ("okay"
                            continue
                        cn=v.__class__.__name__
#                        print [v,cn]
                        if cn=='int' or  cn=='float':
                            ex="parent."+l[4]+"="+str(v)
                        elif cn=='str':
                            ex="parent."+l[4]+"='"+v+"'"
                        else:
                            print ("nicht implementierter typ")
                            ex=''
#                        print ("!!! *!!** "+ex
                        exec(ex)
#                        print parent
                        
                #-----------------------------------
            if l[3]=='att val' or  l[3]=='anchor attr':
#                    print l
#                    print (self.lines[l[2]]
                    

                    method=l[4]
                    parent=self.lines[l[2]][7]

                    if l[3]=='att val':
                        v=l[5]
                    else:
#                        print ("anchor val"
                        v=l[6]
                    if method=='id':
                        self.ids[v]=parent
                        continue
                    try:
                        kk=eval("parent."+l[4])
                    except:
                        
                        cn=v.__class__.__name__
#                        print [v,cn]
                        if cn=='int' or  cn=='float':
                            ex="parent."+l[4]+"="+str(v)
                        elif cn=='str':
                            ex="parent."+l[4]+"='"+v+"'"
                        else:
                            print ("nicht implementierter typ")
                            ex=''
#                        ex="parent."+l[4]+"="+str(v)
#                        print ("*** "+ex
                        exec(ex)
                        continue


                    kk=eval("parent."+l[4])
                    cnkk=kk.__class__.__name__
#                    print ("vor function ", cnkk
                    if cnkk.startswith('So'):
#                        print ("So ..."
#                        print v
#                        print v.__class__
                        ex="parent."+method+".setValue(" +str(v) + ")"
                        exec(ex)
                        continue
                    
                    if cnkk =='builtin_function_or_method':
                            # qt 3...
#                            print ("mche was"
#                            print v
#                            print ("parent."+l[4]
                            kk(v)
#                            print ("okay"
                            continue

                    cn=v.__class__.__name__
#                    print [v,cn]
                    if cn=='int' or  cn=='float':
                        ex="parent."+l[4]+"="+str(v)
                    elif cn=='str':
                        ex="parent."+l[4]+"='"+v+"'"
                    else:
                        print ("nicht implementierter typ")
                        ex=''
#                    print ("//*** "+ex
                    exec(ex)
#                    print parent
        print ("Ende build")


    def showSo(self):
        for l in self.lines:
            if  l[2] == 0 and l[0] !=-1:
#                    print l
                    if len(l)<7:
                        continue
                    r=l[7]
#                    print r
                    if r.__class__.__name__.startswith('So'):
#                        print r
                        sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
                        sg.addChild(r)



    def showSo2(self,dokname):
        for l in self.lines:
            if  l[2] == 0 and l[0] !=-1:
#                    print l
                    r=l[7]
#                    print r
                    if r.__class__.__name__.startswith('So'):
#                        print r
                        dok = FreeCADGui.getDocument(dokname)
                        sg=dok.ActiveView.getSceneGraph()
                        sg.addChild(r)



    def addChild(self,p,c):
        cc=c.__class__.__name__
#        print p
#        print p.__class__
#        print 
#        print c
#        print c.__class__
#        print cc
#        

        if str(c.__class__).startswith("<type 'PySide.QtGui."):
#            print ("pyside"
#            print p
#            dir(p)
#            print p.layout
            p.layout.addWidget(c)
            return
        
        if cc.startswith('So'):
            p.addChild(c)
            return

        if p.__class__.__name__=='object' or str(p.__class__).startswith("<class 'geodat.miki."):
#            print ("Add children to object"
            try:
                p.children.append(c)
            except:
                p.children=[c]
            return
        print (p)
        try:
            if str(p.TypeId)=='Part::MultiFuse':
                z=p.Shapes
                z.append(c)
                p.Shapes=z
            elif str(p.TypeId)=='Part::Compound':
                z=p.Links
                z.append(c)
                p.Links=z
            else:
                try: 
                    p.addObject(c)
                except: 
                    App.Console.PrintError("\naddObject funktioniert nicht")
                    App.Console.PrintError([p,c])
        except:
                try: 
                    p.addObject(c)
                except: 
                    App.Console.PrintError("\naddObject funktioniert nicht")
                    App.Console.PrintError([p,c])
        

    def run(self,string,cmd=None):
        debug=False
        if debug: print ("parse2 ....")
        self.parse2(string)
        if debug: print ("build ...#")
        self.build()

        if debug:  print ("showSo ...")
        self.showSo()
        if cmd!=None:
            print ("CMD ...")
            print (cmd )
            cmd()


    def roots(self):
        rl=[]
        for l in self.lines:
            if l[0]==0:
                rl.append(l)
        return rl

    def report(results=[]):
        print ("Results ...")
        for r in results:
            print (r)
            if r.__class__.__name__.startswith('So'):
                sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
                sg.addChild(r)

        print ("Data ...")
        for ob in self.objects:
            print (ob)

        print (self.anchors)

        for r in self.roots():
            print (r)

################

from PySide import QtGui, QtCore

class MyWidget(QtGui.QWidget):

    def __init__(self, title_widget,objectname):

        QtGui.QWidget.__init__(self)
        self.title_widget = title_widget
        self.setWindowTitle(objectname)
        self.setObjectName(objectname)
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        self.layout=layout

class MyDockWidget(QtGui.QDockWidget):

    def __init__(self, title_widget,objectname):

        QtGui.QDockWidget.__init__(self)

        self.title_widget = title_widget
        self.setWindowTitle(objectname)
        self.setObjectName(objectname)
        
#        self.toggle_title_widget(False)
#        self.toggle_title_widget(True)
#        self.topLevelChanged.connect(self.toggle_title_widget)
        self.setTitleBarWidget(None)
        
        self.setMinimumSize(200, 185)
        
        self.centralWidget = QtGui.QWidget(self)
        self.setWidget(self.centralWidget)        
        #self.centralWidget.setMaximumHeight(800)
        
        
        layout = QtGui.QVBoxLayout()
        self.ll=layout
        self.centralWidget.setLayout(layout)
        self.scroll=QtGui.QScrollArea()

        self.liste=QtGui.QWidget()
        self.lilayout=QtGui.QVBoxLayout()
        self.liste.setLayout(self.lilayout)
        
        mygroupbox = QtGui.QGroupBox()
        mygroupbox.setStyleSheet("QWidget { background-color: lightblue;margin:0px;padding:0px;}\
        QPushButton { margin-right:0px;margin-left:0px;margin:0 px;padding:0px;;\
        background-color: lightblue;text-align:left;;padding:6px;padding-left:4px;color:brown; }")
        self.mygroupbox=mygroupbox

        myform = QtGui.QFormLayout()
        self.myform=myform
        self.myform.setSpacing(0)
        mygroupbox.setLayout(myform)

        scroll = QtGui.QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        self.lilayout.addWidget(scroll)

        # optionaler Top button
        if 0:
            self.pushButton00 = QtGui.QPushButton(QtGui.QIcon('icons:App.svg'),objectname)
            layout.addWidget(self.pushButton00)

        self.pushButton01 = QtGui.QPushButton(
            QtGui.QIcon(App.ConfigGet('UserAppData')+'/Mod/mylib/icons/mars.png'),"Mars" )
        #self.pushButton01.clicked.connect(self.start)

#        layout.addWidget(self.liste)
#        layout.addWidget(self.pushButton01)

        dw=QtGui.QWidget()
        dwl = QtGui.QHBoxLayout()
        dw.setLayout(dwl)
        self.dwl=dwl


        if False: # Top level Icon leiste optional sichtbar machen
            layout.addWidget(dw)
        #self.setTitleBarWidget(dw)
        
        l=QtGui.QLabel('Label')
        #dwl.addWidget(l)
        self.add_top(l)

        b=QtGui.QPushButton('Butto')
        #dwl.addWidget(b)
        self.add_top(b)
        
        b=QtGui.QPushButton(QtGui.QIcon('icons:App.svg'),'Icon+Button')
        #dwl.addWidget(b)
        self.add_top(b)

        b=QtGui.QPushButton(QtGui.QIcon('icons:view-refresh.svg'),'')
        self.add_top(b)

        b=QtGui.QPushButton(QtGui.QIcon('/home/thomas/.FreeCAD/Mod/reconstruction/icons/std_viewscreenshot.svg'),'Foto Image')
        self.add_top(b)

        b=QtGui.QPushButton(QtGui.QIcon('/home/thomas/.FreeCAD/Mod/reconstruction/icons/web-home.svg'),'Foto 3D')
        self.add_top(b)



        layout.setSpacing(0)
        self.layout=layout


    def add_top(self,widget):
        self.dwl.addWidget(widget)


    def toggle_title_widget(self, off):
        if off:
            self.setTitleBarWidget(None)
        else:
            self.setTitleBarWidget(self.title_widget)

def getMainWindowByName(name):
    toplevel2 = QtGui.qApp.topLevelWidgets()
    for i in toplevel2:
        if name == i.windowTitle():
            i.show()
            return i
        
    r=QtGui.QMainWindow()
    
    App.r=r
    r.setWindowTitle(name)
    r.show()
    return r

def getdockwindowMgr():
    pass

def getdockwindowMgr2():
    if 1:
        w = getMainWindowByName("name")
        t = QtGui.QLabel('Title 1')
        d = MyDockWidget(t,"huhu")
        w.addDockWidget(QtCore.Qt.LeftDockWidgetArea, d)
        t = QtGui.QLabel('Title 2')
        d2 = MyDockWidget(t,"haha")
        w.addDockWidget(QtCore.Qt.LeftDockWidgetArea, d2)
        w.tabifyDockWidget(d2, d);
        w.show()
        App.dockwindowMgr=w
        return w



################



class Miki2(Miki):
    def __init__(self,App,layoutstring,obj):
        Miki.__init__(self)
        self.app=App()
        self.app.root=self
        self.app.obj=obj
        obj.ViewObject.Proxy.cmenu.append(["Dialog",lambda:self.run(layoutstring)])
        obj.ViewObject.Proxy.edit= lambda:self.run(layoutstring)



def testme():

    layout='''
    VerticalLayoutTab:
    #    id:'main'
        QtGui.QLabel:
            setText:"***   N U R B S     E D I T O R   ***"
        VerticalLayout:
            HorizontalLayout:
                QtGui.QLabel:
                    setText: "huhuwas 1 3"
                QtGui.QLabel:
                    setText: "huhuwas 2 3"
                QtGui.QLabel:
                    setText: "huhuwas 3 3"
            HorizontalLayout:
                QtGui.QLabel:
                    setText:"Action "
                QtGui.QPushButton:
                    setText: "Run Action"
                VerticalLayout:
                    QtGui.QLineEdit:
                        setText:"edit Axample"
                    QtGui.QLineEdit:
                        setText:"edit B"
                QtGui.QLineEdit:
                    setText:"horizel "
        HorizontalLayout:
            QtGui.QLineEdit:
                setText:"AA"
            QtGui.QLineEdit:
                setText:"BB"

    '''


    miki=Miki()
    app.root=miki

    miki.parse2(layout)
    miki.run(layout)
