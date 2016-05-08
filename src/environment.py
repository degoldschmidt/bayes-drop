import pygame as pg
import numpy as np
from src.objects import Particle
from src.objects import Occluder
from src.objects import Cursor
from src.defs import Colors

class Setup:
    
    def __init__(self, size):
        assert len(size)==2, "Argument size is not twodimensional."
        self.width,self.height = size
        ### Environment defs
        self.ccenter = self.width/2
        self.gacc = 0.1
        pg.mouse.set_pos([self.ccenter, 0])

        ### Cursor defs
        cursor_height = self.height-50
        self.cursor = Cursor((self.ccenter, cursor_height), 30, Colors.goal)

        ### StartArea defs
        startA   = 50
        self.startPos = (self.ccenter, startA)
        self.start    = Particle(self.startPos, startA, Colors.start, False)

        ### Droplet defs
        dropSize = 5
        self.droplet  = Particle(self.startPos, dropSize, Colors.white, True)

        ### Occluder defs
        self.occ = []
        self.occ.append(Occluder((0,0), (self.width,5*self.height/12), Colors.occgray))
        self.occ.append(Occluder((0,0), (self.width,4*self.height/12), Colors.occgray))
        self.occ[0].top = self.height/2+dropSize
        self.occ[1].bottom = self.height/2-dropSize
        
        ### Trial state and variables
        self.shifted = False
        self.dropit = False
        self.stop_trial = False
        self.shift = 0.0
        self.error = 0.0
        
    def randshift(self, mean, std):
        ### GAUSSIAN SHIFT
        mu = -self.width/4
        sigma = self.width/8
        if self.droplet.y > self.occ[1].centery and not self.shifted:
            self.shift = np.random.normal(mu, sigma)
            print("Random shift drawn from N(", mu, ",", sigma, ") ->", self.shift)
            self.droplet.move((self.shift,0))
            self.shifted = True
        
    def reset(self):
        self.droplet.stop()
        self.cursor.stop = True
        self.error = (self.droplet.x-self.cursor.x)
        print("drop , cursor =", self.droplet.x, self.cursor.x)
        print("Error =", self.error)
        keypress = True
        while keypress:
            for event in pg.event.get():
                if event.type != pg.MOUSEBUTTONDOWN:
                    keypress = False
    
    def update(self, screen, click):
        if click:
            self.dropit = True
        ### Cursor
        self.cursor.update(screen, pg.mouse.get_pos())
        ### Starter
        self.start.display(screen)
        ### Droplet
        self.droplet.display(screen)
        ### Fall
        if self.dropit:
            self.droplet.fall(self.gacc)
        ### Shift
        self.randshift(0,0)
        ### STOP CONDITION    
        if self.droplet.y > self.cursor.y:
            self.stop_trial = True
            
        ### Occluder
        for obj in self.occ:
            obj.display(screen)
        
        