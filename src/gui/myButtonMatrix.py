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
#        rawNoteDataArray = []
#        for i in xrange(32):
#            rawNoteDataArray.append([])
#            for j in xrange(12):
#                rawNoteDataArray[i].append([])

    def getRawNoteData(self, rawNoteDataArray):
        rawNoteDataArray[largs[0][0]][largs[0][1]] = lengthArray[0]
        return rawNoteDataArray

    def on_press(self, *largs):
        print largs[0]
#    if largs[0][2] == 1:
#        seq.setNote(largs[0][1] + 60)
#            rawNoteDataArray[largs[0][0]][largs[0][1]] = note.length()
#        else:
#            rawNoteDataArray[largs[0][0]][largs[0][1]] = []

    def setPlaydata(self, playdata):
        pass

class MTNote:
    def length(self):
        return 1

#################################################################################################

<<<<<<< HEAD
def createButtonMatrix():
    w = getWindow()
    
    keyboard = MTKeyboard()
    note = MTNote()
    # Set Button
    btnSet = MTButton(label='Set', pos=(650,50))
    
    ''' Event Handlers '''
    @btnSet.event
    def on_press(*largs):
        if largs[0][2] == 1:
            lengthArray[0] = note.length()
#            rawNoteDataArray[largs[0][0]][largs[0][1]] = note.length()
        else:
            lengthArray[0] = []
#            rawNoteDataArray[largs[0][0]][largs[0][1]] = []
        print lengthArray
#        print keyboard.getRawNoteData(rawNoteDataArray)
    
    
    ''' adding zone '''
    innerwin = MTInnerWindow(size=(605,468), pos=(50,50))
    innerwin.add_widget(keyboard)
    
    w.add_widget(innerwin)
    w.add_widget(btnSet)
=======
class NotesMatrix():
    def __init__(self, **kwargs):
        self.keyboard = MTKeyboard()
        self.note = MTNote()
        
        # insert sequence playdata info into NotesMatrix
        self.sequence = kwargs.get('sequence')
        if not self.sequence == None:
            self.setPlaydata(self.sequence.getPlaydata())
        
        
        
        # initialize
        rawNoteDataArray = []
        for i in xrange(32):
            rawNoteDataArray.append([])
            for j in xrange(12):
                rawNoteDataArray[i].append([])
        
        ''' adding zone '''
        self.innerwin = MTInnerWindow(size=(605,468), pos=(50,50))
        self.innerwin.add_widget(self.keyboard)
        
        w = getWindow()
        w.add_widget(self.innerwin)
        
    def setPlaydata(self, playdata):
        offset = 60
        # get matrix which represents the button's state (pressed or not)in 
        # the matrix
        guiMatrix = self.keyboard.matrix
        
        ''' TODO das muss ueberarbeitet werden. der offset scheint falsch zu sein,
            auf jeden fall mit tamaz arpeggiator, arbeite erstmal mit modulo um was
            brauchbares zu bekommen
        '''
        for tick in range(0,len(playdata)/2): # iterates ticks in playdata
            for packet in playdata[tick]: # iterate Midi Event Packages
                note = packet[2]
                status = packet[4]
                
                if (status==1):
                    guiMatrix[tick][(note-offset)%12]=True
                    
>>>>>>> 7224a1a8449a5d2e405ebef130231362c71e7fa0

