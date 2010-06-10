import sys
import os
import time
import threading

#import pygame
#import pygame.midi
#from pygame.locals import *



ugh = None

def abc(a):
	global ugh
	ugh = a
	
abc(2)
print ugh