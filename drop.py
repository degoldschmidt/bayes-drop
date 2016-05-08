import pygame as pg
import numpy as np
from src.environment import Setup
from src.defs import Colors
import sys

###### Game defs
pg.init()
size = width, height = pg.display.Info().current_w, pg.display.Info().current_h
print(width, height)
screen = pg.display.set_mode(size, pg.FULLSCREEN)
pg.mouse.set_visible(False)

##### ENVIRONMENT
env = Setup(size)


##### EXPERIMENT
Numtrials = 10
errordata = np.zeros((Numtrials,3))


### Trial states
done = False
dropit = False
Trialnum = 1
while not done:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE: done = True
        elif event.type == pg.MOUSEBUTTONDOWN: dropit = True
        elif event.type == pg.QUIT:
            done = True
    
    if env.stop_trial:
        env.reset()
        errordata[Trialnum-1,0] = Trialnum
        errordata[Trialnum-1,1] = env.shift
        errordata[Trialnum-1,2] = env.error
        env = Setup(size)
        dropit = False
        Trialnum += 1
        
    if Trialnum>Numtrials:
        done = True
    
    #### FROM HERE ON IS DRAWN ON SCREEN
    screen.fill(Colors.black)
    env.update(screen, dropit)
        
    pg.display.flip()

#outfile = "./data/config.log"
#np.savetxt(outfile, params, fmt='%u %u %.2f', delimiter=' ', newline='\n', header='#N #T [ms] #dt [ms]')
outfile = "./data/errors.dat"
np.savetxt(outfile, errordata, fmt='%u %u %u', delimiter=' ', newline='\n', header='#Trial #Shift [px] #Error [px]')