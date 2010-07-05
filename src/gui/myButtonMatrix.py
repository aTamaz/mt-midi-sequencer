from pymt import *
import core.audio.Sequence

class MTKeyboard(MTButtonMatrix):
    def __init__(self, **kwargs):
        super(MTKeyboard, self).__init__(**kwargs)
        self.pos = (15,15)
        self.buttoncolor = (.2,.9,0,.5)
        self.matrix_size = (32,12)
        self.size = (600,455)
        self.downcolor = (0, .5, 1, 1)

    def getRawNoteData(self, rawNoteDataArray):
        return rawNoteDataArray

class MTNote:
    def length(self):
        return 1

#################################################################################################

def go(seq):
    w = MTWindow()
    
    keyboard = MTKeyboard()
    note = MTNote()
    # Set Button
    btnSet = MTButton(label='Set', pos=(650,50))
    
    # initialize
    rawNoteDataArray = []
    for i in xrange(32):
        rawNoteDataArray.append([])
        for j in xrange(12):
            rawNoteDataArray[i].append([])

    ''' Event Handlers '''
    @btnSet.event
    def on_press(*largs):
        print keyboard.getRawNoteData(rawNoteDataArray)





    ''' adding zone '''
    innerwin = MTInnerWindow(size=(605,468), pos=(50,50))
    innerwin.add_widget(keyboard)

    w.add_widget(innerwin)
    w.add_widget(btnSet)
    

    runTouchApp()
