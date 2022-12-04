import numpy as np
import Design456Init
class Triangle:
    def __init__(self,app):
        self.app = app
        self.ctx = app.ctx
        self.vbo=self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao= self.get_vao()
        
    def render(self):
        self.vao.render()
        
    def destroy(self):
        #Garbage collector / Destructor 
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
        
    def get_vao(self): 
        #each buffer consist of 3 float with an attr of 'in_position' 
        vao=self.ctx.vertex_array(self.shader_program,[(self.vbo, '3f', 'in_position')])  #buffer format = 3 float and attribute = in_position
        return vao 
    
    def get_vertext_data(self):
        vertex_data=[(-0.6,-0.8,0.0), (0.6,-0.8,0.0), (0.0,0.8,0.0)]
        vertex_data=np.array(vertex_data, dtype='f4')
        return vertex_data
    
    def get_vbo(self):
        vertex_data=self.get_vertext_data()
        vbo=self.ctx.buffer(vertex_data)
        return vbo
    def get_shader_program(self,shader_name):
        with open(Design456Init.RESEARCH_PATH2+f'\\shaders\\{shader_name}.vert') as file:
            vertex_shader =  file.read()
        
        with open(Design456Init.RESEARCH_PATH2+f'\\shaders\\{shader_name}.frag') as file:
            fragment_shader = file.read()
        
        program = self.ctx.program(vertex_shader=vertex_shader,fragment_shader=fragment_shader)
        return program
    
        