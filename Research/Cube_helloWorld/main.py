import pygame as pg
import moderngl as mgl
import sys
from Research.Cube_helloWorld.model import *
from Research.Cube_helloWorld.camera import *
from Research.Cube_helloWorld.light import Light


class GraphicsEngine:
    def __init__(self,win_size=(1000,700)):
        # init pygame module
        pg.init()
        # window size 
        self.WIN_SIZE=win_size
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION,3)  #MAJOR OPENGL 
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION,3) #INOR OPENGL 
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,pg.GL_CONTEXT_PROFILE_CORE) # Depricated functionality will not be used
        # create OpenGL context
        pg.display.set_mode(self.WIN_SIZE,flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()
        #self.ctx.front_face= 'cw'  #to show internal faces
        self.ctx.front_face= 'ccw'  #to show external faces
        
        pg.event.set_grab(True)
        pg.mouse.set_visible(False) # hide mouse pointer
        
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE) # CULL_FACE disallow non visible faces to be rendered 
        # detect an object to help track time
        self.clock=pg.time.Clock()   #frame rate
        self.time=0
        self.delta_time=0.0
        # camera 
        self.camera= Camera(self)
        self.light=Light()
        # scene 
        self.scene = Cube(self )
        
    def check_events(self):
        #events to check windows
        for event in pg.event.get():
            if event.type == pg.QUIT or(event.type== pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit(0)

    def render(self):
        # clear framebuffer
        self.ctx.clear(color=(0.08,0.16,0.18))
        # render scene
        self.scene.render()
        # swap buffers
        pg.display.flip()
        
    def get_time(self):
        self.time = pg.time.get_ticks()*0.001
        
    def run(self):
        while True:           
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time=self.clock.tick(60) #frame buffer

if __name__ == '__main__':
    app=GraphicsEngine()
    app.run()