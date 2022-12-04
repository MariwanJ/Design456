import pygame as pg
import moderngl as mgl
import sys

from Research.Triangle_helloWorld.module import *

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
        # detect an object to help track time
        self.clock=pg.time.Clock()   #frame rate
        # scene 
        self.scene = Triangle(self )
        
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
    def run(self):
        while True:
            self.check_events()
            self.render()
            self.clock.tick(60) #frame buffer
            
if __name__ == '__main__':
    app=GraphicsEngine()
    app.run()