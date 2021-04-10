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
# -- simualtion force by edge length
# --
# -- microelly 2017 v 0.2
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------


import FreeCAD as App
import FreeCADGui as Gui

import Part
import Points

import networkx as nx
import random
import os
#import nurbswb


if 0:
    # load a testfile
    try:
        App.open(u"/home/thomas/Schreibtisch/netz_test_data.fcstd")
        App.setActiveDocument("netz_test_data")
        App.ActiveDocument = App.getDocument("netz_test_data")
        Gui.ActiveDocument = Gui.getDocument("netz_test_data")
    except:
        pass


def copySketch(source, target):
    '''Sketch uebernehmen'''
    for g in source.Geometry:
        target.addGeometry(g)
    for eg in source.ExternalGeometry:
        #        print (eg,    eg[0],eg[1])
        for g in eg[1]:
            target.addExternal(eg[0].Name, g)
    for i, c in enumerate(source.Constraints):
        #        print i,c
        target.addConstraint(c)


def getForceSketch():
    '''open and reset the force visualization sketch'''
    ska = App.ActiveDocument.getObject("Force")
    if ska == None:
        ska = App.ActiveDocument.addObject('Sketcher::SketchObject', 'Force')
        ska.ViewObject.LineColor = (1.0, .0, .0)
        ska.ViewObject.LineWidth = 4

    gct = ska.GeometryCount
    for i in range(gct):
        ska.delGeometry(gct-i-1)

    ska.solve()
    return ska


def getBaseSketch():
    sks = Gui.Selection.getSelection()[0]
    sk = App.ActiveDocument.addObject(
        'Sketcher::SketchObject', "CopySim_" + sks.Name)
    sk.Label = 'Copy of ' + sks.Label
    copySketch(sks, sk)
    return sk


def get_sval(s):
    '''parse the content substring of a geometry '''
    (a, b) = s.split("=")
    return int(eval(b))


def findnode(conix, n):
    for k in conix:
        if n in conix[k]:
            return k
    print("findnode fehler bei ", n)
    print()
    return -1


def getGraph(sk):
    '''sketch to graph'''

    # modul variables
    g = nx.Graph()
    points = {}

    for i, geo in enumerate(sk.Geometry):
        #        print geo.__class__.__name__
        if geo.__class__.__name__ != 'LineSegment':
            continue
#        print (i,geo.StartPoint,geo.EndPoint)
        g.add_node((i, 1))
        g.add_node((i, 2))

    for c in sk.Constraints:
        #    print c.Content
        tt = c.Content.split(' ')
        if tt[2] != 'Type="1"':
            continue

        First = get_sval(tt[4])
        FirstPos = get_sval(tt[5])
        Second = get_sval(tt[6])
        SecondPos = get_sval(tt[7])

        if First == '-1' or Second == '-1':
            continue

        g.add_edge(
            (int(First), int(FirstPos)),
            (int(Second), int(SecondPos))
        )

    # umwandeln in echten topologischen graphen
    conix = {}
    g2 = nx.Graph()

    for i, cons in enumerate(nx.connected_components(g)):
        conix[i] = cons
        g2.add_node(i)

    for i in conix:
        print(i, conix[i])

        for i, geo in enumerate(sk.Geometry):

            # circle radius as 2D height
            if geo.__class__.__name__ == 'Circle':
                n1 = findnode(conix, (i, 3))
                g2.node[n1]['vector'] = sk.getPoint(i, 3)
                g2.node[n1]['radius'] = 1.0*geo.Radius
                print("circle found", geo.Radius, n1)
                continue

            # process only lines
            if geo.__class__.__name__ != 'LineSegment':
                continue

            n1 = findnode(conix, (i, 1))
            g2.node[n1]['vector'] = sk.getPoint(i, 1)
            n2 = findnode(conix, (i, 2))
            g2.node[n2]['vector'] = sk.getPoint(i, 2)
            g2.add_edge(n1, n2)

        rc = sk.solve()
        rc = App.activeDocument().recompute()

    return conix, g2


def add_zdim(g2):
    ''' add the 3D dimension to sketcher 2D data'''
    for n2 in g2.nodes():
        try:
            z = g2.node[n2]['radius']
        except:
            g2.node[n2]['radius'] = 0
            z = 0

        if g2.node[n2]['radius'] == 0:
            # gravitation
            z = -1

        g2.node[n2]['vector'].z = z


def calculateForce(g2, n):
    '''calculate force and new position for node n'''

    f = 0.003

    nbs = g2.neighbors(n)
    v0 = g2.node[n]['vector']
    r = App.Vector()

    for nb in nbs:

        # model A
        if 1:
            mk = 2
            tf = g2.node[nb]['vector'] - v0
            if tf.Length > mk:
                fac = 1.0*(tf.Length-mk)/mk
                tf = tf * fac
            else:
                tf = App.Vector()

        # model B
        if 0:
            tf = g2.node[nb]['vector'] - v0

        r += tf

    force = r*f
    newpos = v0+force
    return (newpos, force)


def run(animate=True, itercount=101):

    ska = getForceSketch()
    sk = getBaseSketch()

    conix, g2 = getGraph(sk)
    add_zdim(g2)

    for lp in range(itercount):

        # cleasr the force sketch
        gct = ska.GeometryCount
        for i in range(gct):
            ska.delGeometry(gct-i-1)
        ska.solve()

        sumforces = 0

        for n in g2.nodes():
            # calculate the force in node n
            (newpos, force) = calculateForce(g2, n)

            # apply the force
            sumforces += force.Length
            g2.node[n]['vector2'] = newpos

            (a, b) = list(conix[n])[0]
            rc = sk.movePoint(a, b, newpos, 0)

            rc = sk.solve()
            v1 = sk.getPoint(a, b)

            g2.node[n]['vector2'] = v1
            if newpos.z > 0:
                g2.node[n]['vector2'].z = newpos.z

            # if a height is given by a circle preserve this value
            if g2.node[n]['radius'] != 0:
                g2.node[n]['vector2'].z = g2.node[n]['radius']

            if force.Length > 0.1:
                ska.addGeometry(Part.Circle(
                    v1, App.Vector(0, 0, 1), force.Length), False)
                ska.addGeometry(Part.LineSegment(v1, v1+force), False)

        # create the 3D model
        col = []
        for (a, b) in g2.edges():
            h = App.Vector(0, 0, random.random()*20)
            col += [Part.LineSegment(g2.node[a]['vector2'],
                                     g2.node[b]['vector2']).toShape()]

        color = (random.random(), random.random(), random.random())

        if animate:  # update grid
            n3 = App.ActiveDocument.getObject("grid")
            if n3 == None:
                n3 = App.ActiveDocument.addObject("Part::Feature", "grid")
        else:  # create new grif each time
            n3 = App.ActiveDocument.addObject("Part::Feature", "grid")
            n3.ViewObject.Transparency = 70
        n3.ViewObject.LineColor = color
        n3.Shape = Part.Compound(col)

        rc = App.activeDocument().recompute()
        print("SUM FORCES", lp, sumforces)
        Gui.updateGui()

        for n in g2.nodes():
            g2.node[n]['vector'] = g2.node[n]['vector2']

    # erzuegen einer flaeche
    if 0:
        import numpy as np

        pts = []

        for b in range(4):
            for a in range(5):
                n = findnode(conix, (a+b*5, 1))
                pts.append(g2.node[n]['vector2'])
            n = findnode(conix, (a+b*5, 2))
            pts.append(g2.node[n]['vector2'])

        pts = np.array(pts).reshape(4, 6, 3)
        bs = Part.BSplineSurface()
        bs.interpolate(pts)

        n3 = App.ActiveDocument.addObject("Part::Spline", "face")
        n3.Shape = bs.toShape()
        n3.ViewObject.Transparency = 70
        n3.ViewObject.ShapeColor = color

    rc = App.activeDocument().recompute()


if __name__ == '__main__':
    run()
