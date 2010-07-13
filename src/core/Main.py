'''
Created on 9 Jun 2010

@author: ELLA
'''
import core.audio.EventManager as EventManager
import core.Constants as Constants

from pymt import *

import pygame
import pygame.midi

import gui.Mainscreen as Mainscreen
import gui.myButtonMatrix as myButtonMatrix


if __name__ == '__main__':
    
    print '============================================================'
    print '=================== START =================================='
    print '============================================================'

    pygame.init()
    pygame.midi.init()

    port = pygame.midi.get_default_output_id()
    myOutput = pygame.midi.Output(port, buffer_size=8, latency=1)

    manager = EventManager.EventManager(logging=Constants.LOGGING_eventSystem, midi_out=myOutput)
    
    #seq1=manager.createSequence()
    
    ''' start ella's main screen '''
    Mainscreen.createMainscreen()
    
    ''' button matrix beispiel '''
    #myButtonMatrix.NotesMatrix()
    
    runTouchApp()