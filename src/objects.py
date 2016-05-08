import numpy as np
import pygame as pg

class Particle:
    
    def __init__(self, pos, size, color, fill):
        assert len(pos)==2, "Argument pos is not twodimensional."
        self.x = int(pos[0])
        self.y = int(pos[1])
        self.v = 0
        self.dt = 0.5
        self.size = int(size)
        self.colour = color
        self.thickness = 12
        self.blurred = False
        if fill:
            self.thickness = 0
            
    def blur(self, screen, std):
        if std > 0.0:
            self.blurred = True
            self.randx = np.random.normal(self.x, std, 25)
            for pos in self.randx:
                pg.draw.circle(screen, self.colour, (int(pos), self.y), int(0.5*self.size), self.thickness)
        
    def deblur(self):
        self.blurred = False
    
    def display(self, screen):
        if not self.blurred:
            pg.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)
        else:
            for pos in self.randx:
                pg.draw.circle(screen, self.colour, (int(pos), self.y), int(0.5*self.size), self.thickness)
           
    
    def fall(self, gacc):
        T = 0
        if gacc>0:
            while T<1:
                self.v = self.v + self.dt * gacc
                self.y = int( self.y + self.dt * self.v )
                T += self.dt
        else:
            self.y = int( self.y + self.dt * 5 )
    
    def move(self, vel):
        assert len(vel)==2, "Argument vel is not twodimensional."
        self.x = self.x + int(vel[0])
        self.y = self.y + int(vel[1])
    
    def moveto(self, pos):
        assert len(pos)==2, "Argument pos is not twodimensional."
        self.x = int(pos[0])
        self.y = int(pos[1])
        
    def reset(self, pos):
        assert len(pos)==2, "Argument pos is not twodimensional."
        self.v = 0
        self.moveto(pos)
        
    def stop(self):
        self.v = 0
        
        
class Occluder(pg.Rect):
    
    def __init__(self, pos, size, color):
        assert len(pos)==2, "Argument pos is not twodimensional."
        assert len(size)==2, "Argument size is not twodimensional."
        self.centerx = int(pos[0])
        self.centery = int(pos[1])
        self.width = int(size[0])
        self.height = int(size[1])
        self.colour = color
        
    def display(self, screen):
        pg.draw.rect(screen, self.colour, self)
        
class Cursor(Particle):
    
    def __init__(self, pos, size, color, fill):
        Particle.__init__(self, pos, size, color, fill)
        self.stop = False
        
    def update(self, screen, mouse):
        assert len(mouse)==2, "Argument pos is not twodimensional."
        width = screen.get_width()
        if (self.x - self.size) < self.size:
            pg.mouse.set_pos([self.size+50,mouse[1]])
        if (self.x + self.size) > width-self.size:
            pg.mouse.set_pos([width-self.size-50,mouse[0]])
        if not self.stop:
            self.x = mouse[0]
        self.display(screen)