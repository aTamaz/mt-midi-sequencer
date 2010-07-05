from pymt import *
#import core.audio.Sequence

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

    def setSize(self, size):
        self.size = size
        self.draw()

#class MTScatterFrame(MTScatterWidget):
#    def __init__(self, **kwargs):
#        super(MTScatterFrame, self).__init__(**kwargs)
#        self.pos = (55,55)
#        self.size = (605,470)

#    def on_touch_down(self, touch):
#       if scat.collide_point(touch.x, touch.y) and not keyboard.collide_point(touch.x, touch.y):
#            super(MTKeyboard, keyboard).on_press(touch.x, touch.y)
#            print 'hi'
#	else:
#		print 'hihi'

class MTNote:
    def length(self):
        return 1

#################################################################################################

def go(seq):
    root = MTWidget()
    keyboard = MTKeyboard()
    #scat = MTScatterFrame()
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

    @scat.event
    def on_touch_down(touch):
        if scat.collide_point(touch.x, touch.y) and not keyboard.collide_point(touch.x, touch.y):
#           super(MTScatterWidget, scat).keyboard(touch.x, touch.y)
            print 'hi'
            return

    scat.add_widget(keyboard)
    root.add_widget(scat)

    runTouchApp(root)
