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
    root = MTWidget()
    keyboard = MTKeyboard()
    scat = MTScatterWidget(size = (605,468), pos = (5,5))
    note = MTNote()

    rawNoteDataArray = []
    for i in xrange(32):
        rawNoteDataArray.append([])
        for j in xrange(12):
            rawNoteDataArray[i].append([])

    # Set Button
    btnSet = MTButton(label='Set', pos=(650,50))
    @btnSet.event
    def on_press(*largs):
        print keyboard.getRawNoteData(rawNoteDataArray)
    
    root.add_widget(btnSet)

    @keyboard.event
    def on_press(*largs):
        '''
        largs[0][0] -> x-axis, goes from 0 to 31 (starting in the left low corner)
        largs[0][1] -> y-axis, goes from 0 to 11
        largs[0][2] -> 0 / 1, toggles on/off
        '''
        if largs[0][2] == 1:
            seq.setNote(largs[0][1] + 60)
#            rawNoteDataArray[largs[0][0]][largs[0][1]] = note.length()
#        else:
#            rawNoteDataArray[largs[0][0]][largs[0][1]] = []

    @keyboard.event
    def on_touch_down(touch):
        if not keyboard.collide_point(*touch.pos):
            return
        touch.grab(keyboard)
        return True

    scat.add_widget(keyboard)
    root.add_widget(scat)

    runTouchApp(root)
