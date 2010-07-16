from pymt import *
import core.audio.Note as Note
import core.Constants as Constants

class MTKeyboard(MTButtonMatrix):
    def __init__(self, **kwargs):
        super(MTKeyboard, self).__init__(**kwargs)
        self.pos = (15,15)
        self.buttoncolor = (.2,.9,0,.5)
        self.matrix_size = (32,12)
        self.size = (600,455)
        self.downcolor = (0, .5, 1, 1)
        self.__rawNoteData = kwargs.get('rawNoteData')
        self.__notesMatrix = kwargs.get('notesMatrix')
        self.displayRawNoteData()
        
    ''' fill buttonmatrix with rawNoteData's informations '''
    def displayRawNoteData(self):
        offset = Constants.NOTE_BEGIN
        # get matrix which represents the button's state (pressed or not)in 
        # the matrix
        guiMatrix = self.matrix
        
        for tick in xrange(32):
            for pitch in xrange(12):
                if (self.__rawNoteData[tick][pitch] != None):
                    guiMatrix[tick][pitch]=True 
       
    
    def getRawNoteData(self):
        return self.__rawNoteData

    '''
    In largs are tuples of tuples:
    ((x,y,True/False),....)
    
    The inner tuple describes x position, y position and wether the button
    located at x,y is pressed or not
    '''
    def on_press(self, *largs):
        print largs[0]
        
        if (largs[0][2] == 1):
            self.__rawNoteData[largs[0][0]][largs[0][1]] = Note.Note()
        else:
            self.__rawNoteData[largs[0][0]][largs[0][1]] = None

        self.__notesMatrix.update_rawNoteData_in_sequence()


#################################################################################################

''' this class displays a Matrix where you can edit your sequence

    must be initiated with an sequence
'''
class NotesMatrix():
    def __init__(self, **kwargs):
        self.sequence = kwargs.get('sequence')
        self.keyboard = MTKeyboard(rawNoteData=self.sequence.getRawNoteData(),notesMatrix=self)
             
        ''' put matrix into a frame '''
        self.innerwin = myMTInnerWindow(notesMatrix=self, size=(605,468), pos=(50,50))
        self.innerwin.add_widget(self.keyboard)
        
        w = getWindow()
        w.add_widget(self.innerwin)
        
    ''' get raw notes from matrix to sequence in order to update it '''
    def update_rawNoteData_in_sequence(self):
        self.sequence.setRawNoteData(self.keyboard.getRawNoteData())
        


    
''' this is for catching the close event for updating rawNoteData from matrix
    to sequence
'''
class myMTInnerWindow(MTInnerWindow):
    def __init__(self, **kwargs):
        super(myMTInnerWindow, self).__init__(**kwargs)
        self.__notesMatrix = kwargs.get('notesMatrix')
    
    def close(self, touch):
        self.__notesMatrix.update_rawNoteData_in_sequence()
        super(myMTInnerWindow, self).close(touch)