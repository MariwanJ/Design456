'''shoe configuration data'''
# version 0.92
# (c) microelly
#

print ("shoedata version 0.92"

## shoeAdam ist das erste Schuh-Modell
#
# es benutzt eine Erweiterung der Methoden der Needle-Klasse
# bei den einzelnen Rippen handelt es sich um parametrische Varianten einer Sketcher-BSpline
#
# Backbone, Twister und Scaler werden wie bei Needle verwendet.
#
  

class shoeAdam():
    ''' the first shoe model a
    use shoeAdam.bbps, shoeAdam.boxes, shoeAdam.twister, shoeAdam.sc '''

##\cond

    # backbone (red line)
    bbps=[ 
            [280,0,11+9], #  not used
            [260,0,11+3], #  outside

            [250,0,11], # top
            [218,0,4], # st 

            [168,0,0], # joint j
            [132,0,6], # girth
            [110,0,10], # waist
            [68,0,14], # instep ik

            [60,0,16], #  leg
            [45,0,17], #  leg
            [35,0,18], #  leg
            [20,0,19], #  leg

            [5,0,20], #  inner back end 
            [0,0,20], #  back end heel
        ]


    # 3D Boxes for the ribs  - feinarbeit

    boxes=[
            [8,0,-24,10], # not used
            [10,0,-16,12], # vorspitze
            [22,0,-25+10,14],# spizte fuss
            [29,0,-20,16],
            [40,0,-40,22], # sp == einschnitt, zehengelenk? 
            [42,0,-48,42], # joint J3
            [35,0,-43,58], # waist
            [32,0,-38,67], # girth
            [30,0,-35,97], # instep I
            [30,0,-34,103],# oeffnung short heel
            [30,0,-32,100],# knoechel 1
            [28,0,-30,94],# knoechel 2
            [26,0,-26,94],# knoechel 3
            [24,0,-10,94],# vorbereitung abschluss hinten
            [1,0,-1,94], # abschluss hinten
        ]


    # rotations and scaling
    #twister= [[0,0,0]]*4 + [[0,30,0]]*4 + [[0,25,0]] + [[0,20,0]]+ [[0,10,0]]*4

    # drehwinkel der rippen gedrehter joint
    twister= [[0,0,0]]*4 + [[0,30,-10]]+[[0,30,0]]*3 + [[0,25,0]] + [[0,20,0]]+ [[0,10,0]]*4

    sc= [[1,1]]*14 



# control of output

# show loft of the profiles
showlofts=False

# show scaled models 
showscales=False
scaleIn=0.98
scaleOut=1.02


##\endcond
