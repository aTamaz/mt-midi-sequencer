'''
Created on 9 Jun 2010

@author: ELLA
'''
import core.audio.EventManager as EventManager
import core.Constants as Constants

import pygame
import pygame.midi
from gui import myButtonMatrix



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
    #import gui.Severalbuttons7
    
    ''' button matrix beispiel -> 3 toene schmeissen arpeggiator an '''
    import gui.myButtonMatrix
    myButtonMatrix.go(manager.createSequence())
    
    ''' hello world beispiel -> slider verstellt bpm '''
    #import gui.temp.helloworld
    #manager.createSequence()
    #gui.temp.helloworld.go()