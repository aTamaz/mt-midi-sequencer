from pymt import *
import core.audio.Sequence

class MTKeyboard(MTButtonMatrix):
    def __init__(self, **kwargs):
        super(MTKeyboard, self).__init__(**kwargs)
        self.pos = (0,0)
        self.buttoncolor = (.1,.5,.1,.5)
        self.matrix_size = (32,12)
        self.size = (620,455)
        self.downcolor = (.5,.15,.5,.5)

    def getRawNoteData(self, rawNoteDataArray):
        return rawNoteDataArray        

class MTNote:
    def length(self):
        return 1

################################################################################
def go(seq):
    root = MTWidget()
    keyboard = MTKeyboard()
    note = MTNote()
    
    rawNoteDataArray = []
    for i in xrange(32):
        rawNoteDataArray.append([])
        for j in xrange(12):
            rawNoteDataArray[i].append([])
    
    @keyboard.event
    def on_press(*largs):
        '''
        largs[0][0] -> x-axis, goes from 0 to 31 (starting in the left low corner)
        largs[0][1] -> y-axis, goes from 0 to 11
        largs[0][2] -> 0 / 1, toggles on/off
        '''

        if largs[0][2] == 1:
            seq.setNote(largs[0][1] + 60)
            # rawNoteDataArray[largs[0][0]][largs[0][1]] = note.length()
        # else:
            # rawNoteDataArray[largs[0][0]][largs[0][1]] = []
        # print rawNoteDataArray
        # print largs[0][2]
        # print largs[0][0]
    
    root.add_widget(keyboard)
    
    runTouchApp(root)
