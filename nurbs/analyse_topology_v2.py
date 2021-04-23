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
# -------------------------------------------------
# -- analyse topology of parts
# --
# -- microelly 2017 v 0.3
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------


# \cond

import FreeCAD as App
import FreeCADGui as Gui
import random
import os, sys
import NURBSinit
import Part
import Points
import time

try:
    import networkx as nx
except ImportError:
    print("Please install the required library networkx")
    
try:
    import numpy as np
except ImportError:
    print("Please install the required module : numpy")
    

# modul variables
g=nx.Graph()
points={}


def ptokey(v):
    ''' simplify vectors'''
    return (round(v.x, 2), round(v.y, 2), round(v.z, 2))


def rf(v):
    ''' vector modification hook'''
    return v
    ff = 0.001
    return v + App.Vector(ff*random.random(), ff*random.random(), ff*random.random())


def createFaceMidPointmodel(a):
    '''create an extended model with facepoints'''

    fs = a.Shape.Faces

    pts = []
    col = []
    col = a.Shape.Edges

    for f in fs:
        c = f.CenterOfMass
        pts.append(c)
        for v in f.Vertexes:
            p = v.Point
            pts.append(p)
            col.append(Part.makeLine(rf(c), rf(p)))

    # Points.show(Points.Points(pts))

    Part.show(Part.Compound(col))
    App.ActiveDocument.ActiveObject.ViewObject.hide()
    App.ActiveDocument.ActiveObject.ViewObject.PointSize = 6.
    App.ActiveDocument.ActiveObject.ViewObject.LineWidth = 1.
    App.ActiveDocument.ActiveObject.Label = "Face Extend for " + a.Label

    return App.ActiveDocument.ActiveObject


# def displayMatplot():
#    # display in matplotlib
#    pos=nx.get_node_attributes(g,'pos')
#    nx.draw(g,pos)
#    #p-l-t.show()
#    # p-l-t.savefig("/tmp/path.png")

#TODO: This function is defined twice. Which one is correct. 
# def getkey(n):
#     import networkx as nx
#     g = nx.Graph()
#     l = g.node[n]['vs'].Length
#     if l < 1:
#         l = 100000

#     return (g.node[n]['ec'], round(g.node[n]['sl']/l, 4), round(g.node[n]['vds']/l, 4))
#     # return (g.node[n]['ec'],round(g.node[n]['sl']/l,16),round(g.node[n]['vds']/l,14))


def getkey(n):
    import networkx as nx
    v2es = App.Vector()
    for v in g.node[n]['edirs']:
        v2 = App.Vector(v).normalize()
        v2es += v2

#    print ("huhu ", len( g.node[n]['fdirs'])
    v2fs = App.Vector()
    for v in g.node[n]['fdirs']:
        #        print v
        v2 = App.Vector(v)
        v2.normalize()
        v2fs += v2

#    return (#g.node[n]['ec'],
#        0,
#        App.Vector(ptokey(v2fs)).Length,
#        App.Vector(ptokey(v2es)).Length
#        )


#    print v2fs
#    print v2es
#    print ("fdirs",len(g.node[n]['fdirs'])
#    print ("edirs",len(g.node[n]['edirs'])

#    print ("getkey",(
#        g.node[n]['ec'],
#        0,
#        App.Vector(v2fs).Length,
#        App.Vector(v2es).Length
#        )

# ----------------
    return (
        # g.node[n]['ec'],
        # 0,
        len(g.node[n]['fdirs'])+100*len(g.node[n]['edirs']),
        round(App.Vector(ptokey(v2fs)).Length, 2),
        round(App.Vector(ptokey(v2es)).Length, 2)
    )

# -----------------------------------------------------------------------------------


def getkeyg(g, n):
    v2es = App.Vector()
    for v in g.node[n]['edirs']:
        v2 = App.Vector(v).normalize()
        v2es += v2

    if len(g.node[n]['edirs']) == 4 and round(App.Vector(ptokey(v2es)).Length, 2) == 0.0:
        v0 = App.Vector(g.node[n]['edirs'][0]).normalize()
        v1 = App.Vector(g.node[n]['edirs'][1]).normalize()
        v2 = App.Vector(g.node[n]['edirs'][2]).normalize()
        v2es = v0.cross(v1)
        if v2es == App.Vector():
            v2es = v0.cross(v2)

    v2fs = App.Vector()
    for v in g.node[n]['fdirs']:
        v2 = App.Vector(v)
        v2.normalize()
        v2fs += v2

    return (
        len(g.node[n]['fdirs'])+100*len(g.node[n]['edirs']),
        round(App.Vector(ptokey(v2fs)).Length, 2),
        round(App.Vector(ptokey(v2es)).Length, 2)
    )
# ---------------------------------------------------------------------------------


def createKeys():
    import networkx as nx
    kp = {}

    for n in g.nodes():
        #            print n
        #            print g.node[n]
        try:
            g.node[n]['fdirs']
        except:
            g.node[n]['fdirs'] = []
        key = getkey(n)
        g.node[n]['keys'] = [key]
        g.node[n]['key'] = key
        try:
            kp[key] += 1
        except:
            kp[key] = 1

    anz = 0
    print("Keys, count occur")
    for k in kp:
        print(k, kp[k])
        if kp[k] == 1:
            anz += 1

    print("number of top level marker points:", len(g.nodes()), anz)
    return kp


def setQuality(nodes, kp):
    for n in nodes:
        key = g.node[n]['key']
        if kp[key] == 1:
            g.node[n]['quality'] = 1


def getNeighborEdges(n):
    import networkx as nx
    ''' freecad edges from a point n '''
    col = []
    nbs = g.neighbors(n)
    for nb in nbs:
        col += [g.edge[n][nb]['fcedge']]
    return col

# ----------------------------------------------------

class MainAnalysisMethodRunAna:
    def __init__(self, model=None, silent=False):
        self.model=model
        self.silent=silent
        
    def Activated(self):
        self.runCompare()

    def runAna(self, model, silent=False):
        '''main analysis method'''

        print("NodesA", g.nodes())
        mp = createFaceMidPointmodel(model)
        print("NodesB", g.nodes())
        self.loadModel(mp)

        print("Model ", mp.Label)
        print("NodesC", g.nodes())

        # link labels and geometry from freecad to networkx
        bm = model
        sp = bm.Shape

        for i, v in enumerate(sp.Vertexes):
            pp = (round(v.Point.x, 2), round(
                v.Point.y, 2), round(v.Point.z, 2))
            try:
                #            print (pp,i)
                #            print ("found ",points[pp])
                gi = points[pp]

                g.node[gi]["label"] = bm.Label+":Vertex"+str(i+1)
                g.node[gi]["Vertex"] = v
    #            print (g.node[gi])
            except:
                print("NOT FOUND")
                pass

        for i, f in enumerate(sp.Faces):
            print("Face ", i, len(f.Vertexes))
            for v in f.Vertexes:
                #            print (v,ptokey(v.Point),points[ptokey(v.Point)])
                pix = points[ptokey(v.Point)]
    #            print (g.node[pix])

                # flaechennormale anfuegen
                (u, v) = f.Surface.parameter(v.Point)
    #            print( pix,"Addiere Flaechennoirmalw",(u,v),f.normalAt(u,v))
                try:
                    g.node[pix]['fdirs'].append(f.normalAt(u, v))
                except:
                    g.node[pix]['fdirs'] = [(f.normalAt(u, v))]
                print("len fdirs", len(g.node[pix]['fdirs']))

            c = f.CenterOfMass
            pp = (round(c.x, 2), round(c.y, 2), round(c.z, 2))
            try:
                #            print (pp,i)
                #            print ("found ",points[pp])
                gi = points[pp]

                g.node[gi]["label"] = bm.Label+":Face"+str(i+1)
                g.node[gi]["Face"] = f
    #            print (g.node[gi])
            except:
                print("NOT FOUND")
                pass

        kp = createKeys()
        print(g.nodes())

        setQuality(g.nodes(), kp)

        # hack
        # return

        # calculate and display top quality nodes
        if 1:
            ns = []
            for n in g.nodes():
                if g.node[n]['quality'] == 1:
                    ns.append(n)
            # print ns
            if not silent:
                self.displayNB(ns)
                App.ActiveDocument.ActiveObject.Label = "Top Quality"
                App.ActiveDocument.ActiveObject.ViewObject.LineColor = (
                    random.random(), random.random(), random.random())

        # calculate all levels
        for i in range(1, 10):
            self.berechneKeyLevel(i)
            rc = self.valuesFromLevel (i)
            if rc == 0:
                break

        last = i
        # zeige alle indentifizierten Punkte im Verbund
        if not silent:
            for i in range(1, last):
                self.zeigeQ(i)

        # hold the data for postprocessing in a global variable
        App.g = g
        App.a = model

    #    print  (len(sp.Vertexes)
        self.addToVertexStore()


    def TopologicalAnalyse(self):
        """
         TopologicalAnalyse
        """
        import networkx as nx
        try:
            App.PT
        except:
            App.PT = {}

        try:
            '''run analysis for one selected object'''
            s = Gui.Selection.getSelectionEx()
            self.runAna(s[0])

        except Exception as err:
            App.Console.PrintError("'TopologicalAnalyse' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def valuesFromLevel (self,i=1):
        ''' which points have unique keys at level i'''

        # count the key occurrences
        kp = {}
        for n in g.nodes():
            if g.node[n]['quality'] == 0:
                key = g.node[n]['keys'][i]
                try:
                    kp[key] += 1
                except:
                    kp[key] = 1

        # which points have unique keys
        anz = 0
        anzg = 0

        # count the unique points
        for k in kp:
            if kp[k] == 1:
                anz += 1

        # set the quality of the unique points
        for n in g.nodes():
            if g.node[n]['quality'] == 0:
                key = g.node[n]['keys'][i]
                if kp[key] == 1:
                    g.node[n]['quality'] = i+1
                    anzg += 1
            else:
                anzg += 1

        print("level", i, "found", anz, "found overall", anzg,
              "not identified till now", len(g.nodes())-anzg)
        return anz

    def displayNB(self,nodes):
        ''' diasplay neighbor edges as Part'''
        col = []
        for n in nodes:
            col += getNeighborEdges(n)
        Part.show(Part.Compound(col))

    def zeigeQ(self,i):
        ''' display the identification quality level as Sub Grid '''

        ns = []
        for n in g.nodes():
            if g.node[n]['quality'] == i:
                ns.append(n)

        # print ns
        self.displayNB(ns)
        App.ActiveDocument.ActiveObject.Label = "Quality" + str(i)
        App.ActiveDocument.ActiveObject.ViewObject.LineColor = (
            random.random(), random.random(), random.random())

    def berechneKeyLevel(self,i=1):
        '''key for level i is the i-th neighbor sum of the keys'''

        for n in g.nodes():
            nbs = g.neighbors(n)
            kka = {}
            aas = 0
            bbs = 0
            ccs = 0
            for nb in nbs:
                (a, b, c) = g.node[nb]['keys'][i-1]
                aas += a
                bbs += b
                ccs += c

            try:
                g.node[n]['keys'][i] = (aas, bbs, ccs)
            except:
                g.node[n]['keys'].append((aas, bbs, ccs))

    def loadModel(self,s):
        ''' map the Part <s> to a networx graph <g> with points set <points>'''

        sp = s.Shape

        for i, v in enumerate(sp.Vertexes):

            pp = (round(v.Point.x, 2), round(
                v.Point.y, 2), round(v.Point.z, 2))

            try:
                points[pp]
            except:
                points[pp] = i
                g.add_node(i, pos=(v.Point.x, v.Point.y), keys=[],
                           quality=0, vector=ptokey(v.Point))

        for e in sp.Edges:

            p1 = e.Vertexes[0].Point
            i1 = ptokey(p1)

            p2 = e.Vertexes[1].Point
            i2 = ptokey(p2)

            print("addedge", points[i1], points[i2])
            ge = g.add_edge(points[i1], points[i2],
                            weight=round(e.Length, 2),
                            vector=p2-p1,
                            fcedge=e  # the real edge
                            )

        # calculate some topological/metrical information for the vertexes

        for n in g.nodes():
            es = g.edge[n]
            sl = 0  # sum of vector length
            vs = App.Vector()  # sum of vectors
            vds = 0
            edirs = []

            if len(es) > 0:
                esl = []
                for i, e in enumerate(es):
                    esl.append(e)
                    sl += g.edge[n][e]['vector'].Length
                    vs += g.edge[n][e]['vector']
                    edirs += [g.edge[n][e]['vector']]

                vsn = App.Vector(vs)

                # some trouble ist the sum of all vectors is zero
                if 0:  # still look for a better solution
                    if vsn.Length < 1:
                        vsn = g.edge[n][esl[0]]['vector'].cross(
                            g.edge[n][esl[2]]['vector'])

                    if vsn.Length < 1:
                        vsn = g.edge[n][esl[0]]['vector'].cross(
                            g.edge[n][esl[1]]['vector'])

                if vsn.Length > 1:
                    vsn.normalize()
                else:
                    vsn = 0

                for e in es:
                    v = App.Vector(g.edge[n][e]['vector'])
                    v.normalize()
                    vd = v.dot(vs)
                    vds += vd

            g.node[n]['ec'] = len(es)
            g.node[n]['vs'] = vs
            g.node[n]['sl'] = sl
            g.node[n]['vds'] = vds
            g.node[n]['vs'] = vs
            g.node[n]['edirs'] = edirs
            # g.node[n]['fdirs']=[]

    def addToVertexStore(self):
            '''add the keys to the global vertex store'''
            try:
                App.PT
            except:
                App.PT = {}

            print("add to Vertex-Store")
            g = App.g
            a = App.a
            for v in g.nodes():
    
                try:
                    g.node[v]['label']
                except:
                    g.node[v]['label'] = '----'
    
                print("kkkk")
                print(g.node[v]['label'])
                print(g.node[v]['quality']-1)
                print(g.node[v]['keys'])
    #            print g.node[v]['keys'][g.node[v]['quality']-1]
                print("ha")
    
        #        key=(a.Label,g.node[v]['label'],v,g.node[v]['keys'][g.node[v]['quality']-1],"!>",
        #            g.node[v]['quality'],"<!",g.node[v]['keys'])
    
                key = (a.Label, g.node[v]['label'], v, g.node[v]['keys'][0], "!>",
                       g.node[v]['quality'], "<!", g.node[v]['keys'])
    
                try:
                    if key not in App.PT[g.node[v]['vector']]:
                        App.PT[g.node[v]['vector']] += [key]
                        # print ("added"
                except:
                    # App.PT[g.node[v]['vector']] =[(a.Label,g.node[v]['label'],v,g.node[v]['keys'][g.node[v]['quality']-1],g.node[v]['quality'])]
                    App.PT[g.node[v]['vector']] = [key]

    # TopologicalCompare'
    def TopologicalCompare(self):
        """ 
        TopologicalCompare
        """
        import networkx as nx



        try:
            self.runCompare()
        except Exception as err:
            App.Console.PrintError("'Magnet' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def runCompare(self):
        '''run analysis for more parts and display the results'''
        resetVertexStore()
        s = Gui.Selection.getSelectionEx()
        for model in s:
            #        g=nx.Graph()
            #        App.g=g
            print("Startrnstand")
            for v in g.nodes():
                print(g.node[v]['fdirs'])
                print(g.node[v]['edirs'])
                g.node[v]['fdirs'] = []
                g.node[v]['edirs'] = []
            print("--------------")
            print("NodesA", g.nodes())
            runAna(model, silent=True)
        self.displayVertexStore()

    def displayVertexStore(self):
        '''print the vertex store'''
        print("The vertex Store compare")
        found = 0
        count = 0
        keys = {}
        keyd = {}

        for j in App.PT:
            # print
            # print j
            vs = App.PT[j]
            for v in vs:
                if str(v[1]) == '----':
                    continue
                k = v[3]
                count += 1
                try:
                    keys[k] += 1
                    keyd[k] += [(j, v[:-2])]
                    # print v
                except:
                    keys[k] = 1
                    keyd[k] = [(j, v[:-2])]
        pts = []
        for k in keys:
            if keys[k] > 1:
                found += 1
                # print k,keys[k]
                # print keyd[k]
                pts.append(keyd[k][0][0])
                pts.append(keyd[k][1][0])
                # moeglich sortieren auf koerper einzeln
                # print keyd[k][0][1]
                # print keyd[k][1][1]

    #    if pts!=[]:
    #        #print pts
    #        Points.show(Points.Points(pts))
    #        App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(
    #            random.random(),random.random(),random.random())
    #        App.ActiveDocument.ActiveObject.ViewObject.PointSize= 10
    #
    #        App.ActiveDocument.ActiveObject.Label="Common Points "

    #    print ("no found -----------------------------"
        pts = []
        for k in keys:
            if keys[k] == 1:
                #            print k,keys[k]
                #            print keyd[k]
                #            print ("!!",keyd[k][0][0]
                pts.append(keyd[k][0][0])

        print
        print("after keys issued")
        for k in keys:
            if k[0] % 100 != 0:  # ignore reine flaechen
                print
                print(k)
                for p in keyd[k]:
                    print(p[1])

        anz = 0
        gps = []
        print
        print("after keys issued only pairs -------------------------------")
        for k in keys:
            first = True
            if k[0] % 100 != 0:  # ignore reine flaechen
                if len(keyd[k]) == 2:
                    [p, q] = keyd[k]
                    if p[1][0] != q[1][0]:
                        if p[1][1].startswith(p[1][0]):
                            if first:
                                print
                                print(k)
                                first = False
                            print(p[1])
    #                        print p
                            print(q[1])
                            anz += 1
                            gps += [App.Vector(p[0]), App.Vector(q[0])]

        print("found pairs  ")
        print(anz)

        if gps != []:
            Points.show(Points.Points(gps))
            App.ActiveDocument.ActiveObject.ViewObject.ShapeColor = (
                random.random(), random.random(), random.random())
            App.ActiveDocument.ActiveObject.ViewObject.PointSize = 10

            App.ActiveDocument.ActiveObject.Label = "Gefundene unique keys -- bestes ergebnis"

    #    if pts!=[]:
    #        #print pts
    #        Points.show(Points.Points(pts))
    #        App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(
    #            random.random(),random.random(),random.random())
    #        App.ActiveDocument.ActiveObject.ViewObject.PointSize= 10
    #
    #        App.ActiveDocument.ActiveObject.Label="No common Points "
    #
    #    print ("common found:",found
    #    print count

    def displayQualityPoints(self):
        """ 
        displayQualityPoints TOPO 8
        """
        import networkx as nx

        def Activated(self):
            try:
                self.displayQualityPoints()
            except Exception as err:
                App.Console.PrintError("'Magnet' Failed. "
                                       "{err}\n".format(err=str(err)))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

        def displayQualityPoints(self):
            '''display the quality points as point clouds'''
            g = App.g
            for q in range(1, 7):
                pts = []
                for v in g.nodes():
                    # print g.node[v]['quality']
                    if g.node[v]['quality'] == q:
                        pts.append(g.node[v]['vector'])
        #        print pts
                if pts != []:
                    Points.show(Points.Points(pts))
                    App.ActiveDocument.ActiveObject.ViewObject.ShapeColor = (
                        random.random(), random.random(), random.random())
                    App.ActiveDocument.ActiveObject.ViewObject.PointSize = 10
                    App.ActiveDocument.ActiveObject.Label = "Points Quality " + str(q)

# printGraphData TOPO 5

    def printGraphData(self):
        """ 
        printGraphData
        """
        import networkx as nx

        def Activated(self):
            try:
                self.printData()

            except Exception as err:
                App.Console.PrintError("'Magnet' Failed. "
                                       "{err}\n".format(err=str(err)))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

        def printData(self):
            '''print some diagnostic data'''
            g = App.g
            for v in g.nodes():
                print(v)
                print(g.node[v]['quality'])
                print(g.node[v]['keys'])
                print(g.node[v]['vector'])
                print(g.node[v]['keys'][g.node[v]['quality']-1])

        def GetResources(self):
            return {
                'Pixmap': NURBSinit.ICONS_PATH + '.svg',
                'MenuText': '',
                            'ToolTip':  ''
            }

    def GetResources(self):
        return {
            'Pixmap': NURBSinit.ICONS_PATH+'nurbs.svg',
            'MenuText': 'MainAnalysisMethodRunAna',
                        'ToolTip':  'MainAnalysisMethodRunAna'
        }
Gui.addCommand('MainAnalysisMethodRunAna', MainAnalysisMethodRunAna())
#TODO : FIX ME .. YOU CANNOT HAVE IT LIKE THAT SEPARATE THEM. Mariwan
#Gui.addCommand('displayVertexStoreCommonPoints',               TopologicalCompare.displayVertexStore(TopologicalCompare()))



# resetVertexStore
class resetVertexStore:
    """ 
    resetVertexStore
    """

    def Activated(self):
        try:
            self.resetVertexStore()
        except Exception as err:
            App.Console.PrintError("'Magnet' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def resetVertexStore(self):
        '''clear the vertex store for next analysis'''
        App.PT = {}
        print(App.PT)

    def GetResources(self):
        return {
            'Pixmap': NURBSinit.ICONS_PATH + 'Nurbs.svg',
            'MenuText': '',
                        'ToolTip':  ''
        }
Gui.addCommand('resetVertexStore', resetVertexStore())


# print vertextstore
class printVertexStore:
    """ 
    printVertexStoreDump'
    """

    def Activated(self):
        try:
            self.printVertexStore()
        except Exception as err:
            App.Console.PrintError("'Magnet' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def printVertexStore():
        '''print the vertex store'''
        print("The vertex Store")
        for j in App.PT:
            print
            print(j)
            vs = App.PT[j]
            for v in vs:
                if str(v[1]) != '----':
                    print(v[1:-1])
#                print ("    ",v[-1]

    def GetResources(self):
        return {
            'Pixmap': NURBSinit.ICONS_PATH + 'Nurbs.svg',
            'MenuText': 'printVertexStoreDump',
                        'ToolTip':  'printVertexStoreDump'
        }


Gui.addCommand('printVertexStore', printVertexStore())

class Nurbs_AnalyseLoadTest1:
    def Activate(self):
        self.loadTest1()
    def loadTest1():
        print(__file__)
        # hier relativen pfad reintun
        App.open(NURBSinit.DATA_PATH+"zwei_gleiche_fenster.fcstd")
        App.setActiveDocument("zwei_gleiche_fenster")
        App.ActiveDocument = App.getDocument("zwei_gleiche_fenster")
        Gui.ActiveDocument = Gui.getDocument("zwei_gleiche_fenster")

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_AnalyseLoadTest1")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_AnalyseLoadTest1"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_AnalyseLoadTest1", Nurbs_AnalyseLoadTest1())


class Nurbs_AnalyseLoadTest2:
    def Activated(self):
        self.loadTest2()
    def loadTest2():
    
        App.open(NURBSinit.DATA_PATH+"zwei_gleiche_fenster.fcstd")
        App.setActiveDocument("zwei_gleiche_fenster")
        App.ActiveDocument = App.getDocument("zwei_gleiche_fenster")
        Gui.ActiveDocument = Gui.getDocument("zwei_gleiche_fenster")

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_AnalyseLoadTest2")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_AnalyseLoadTest2"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_AnalyseLoadTest2", Nurbs_AnalyseLoadTest2())




def getkeytab(g, nodes):
    keys = {}
    for n in nodes:
        #        print n
        #        print g.node[n]
        k = getkeyg(g, n)
        try:
            keys[k] += [n]
        except:
            keys[k] = [n]
    return keys


def getUniques(keys):
    us = []
    for k in keys:
        if len(keys[k]) == 1:
            us += keys[k]
    return us

class Nurbs_AnalyseTest4:
    def Activated(self):
        self.Test4()
        
    def Test4(self):
        import networkx as nx
        g = App.g
        print("Test 4")
    #    print g.nodes()

        keys = getkeytab(g, g.nodes())

        print("keytab all results ...")
        for k in keys:
            print(k, keys[k])

        uniqs = getUniques(keys)
        print("uniques start ")
        print(uniqs)

        for n in uniqs:
            g.node[n]['upath'] = [n]

        found = True
        for i in range(8):
            if not found:
                break

            found = False
            print("loop i= ")
            print(i)
            for n in uniqs:
                nbs = g.neighbors(n)
                nbs2 = []
                for na in nbs:
                    if na not in uniqs:
                        nbs2.append(na)

                keys = getkeytab(g, nbs2)

    #            print
    #            print ("node ",n,getkeyg(g,n),nbs2)
    #            print nbs

                for k in keys:
                    print(k, keys[k])

                uniqs2 = getUniques(keys)
                if uniqs2 != []:
                    print("----------------------------------uniques2: ")
                    print(uniqs2)
                    for u in uniqs2:
                        if u not in uniqs:
                            #                print ("-add--------------------",u
                            found = True
                            uniqs += [u]
                            g.node[u]['upath'] = g.node[n]['upath']+[u]

        print("all uniqs ")
        print(uniqs)

        for n in uniqs:
            print(k, n, g.node[n]['label'], g.node[n]['upath'])

        ups = []
        for n in uniqs:
            ups.append(App.Vector(g.node[n]['vector']))

        Points.show(Points.Points(ups))
        App.ActiveDocument.ActiveObject.ViewObject.ShapeColor = (
            random.random(), random.random(), random.random())
        App.ActiveDocument.ActiveObject.ViewObject.PointSize = 10

        App.ActiveDocument.ActiveObject.Label = "Eindeutige Punkte"

        print
        print("nicht zuordenbar ...")
        noups = []
        for n in g.nodes():
            if n not in uniqs:
                k = getkeyg(g, n)
                print(k, n, g.node[n]['label'], g.node[n]['vector'])
    #            print (n,g.node[n]['label'])
    #            print g.node[n]['edirs']
    #            print g.node[n]['fdirs']
                noups.append(App.Vector(g.node[n]['vector']))

        Points.show(Points.Points(noups))
        App.ActiveDocument.ActiveObject.ViewObject.ShapeColor = (
            random.random(), random.random(), random.random())
        App.ActiveDocument.ActiveObject.ViewObject.PointSize = 10

        App.ActiveDocument.ActiveObject.Label = "Nich eindeutige Punkte"

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_AnalyseTest4")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_AnalyseTest4"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_AnalyseTest4", Nurbs_AnalyseTest4())



class Nurbs_AnalyseTest3:
    def Activate(self):
        self.Test3()
    def Test3(self):
        import fem_edgelength_mesh
        for i in range(1):
            #reload(fem_edgelength_mesh)
            fem_edgelength_mesh.run()
            Gui.updateGui()
            print("i ")
            print(i)
            time.sleep(0.01)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_AnalyseTest3")
        return {'Pixmap': NURBSinit.ICONS_PATH+'draw.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_AnalyseTest3"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 ", _tooltip)}

Gui.addCommand("Nurbs_AnalyseTest3", Nurbs_AnalyseTest3())

