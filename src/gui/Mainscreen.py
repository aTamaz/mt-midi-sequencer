'''
Created on 9 Jun 2010

@author: ELLA
'''
import os
from pymt import *
from OpenGL.GL import *
import math
from random import randint, random
import random, time
import core.audio.EventManager as EventManager
import myButtonMatrix as ButtonMatrix
import core.Constants as Constants

IS_PYMT_PLUGIN = True
PLUGIN_TITLE = 'Menu Music'
PLUGIN_AUTHOR = 'Ella Kadas'
PLUGIN_DESCRIPTION = 'menu Music stuff'
additional_css = '''
.simple {
    draw-alpha-background: 1;
    draw-border: 1;
    draw-slider-alpha-background: 1;
    draw-slider-border: 1;
    draw-text-shadow: 2;
}

.colored {
    bg-color:  rgb(102,205,170);
    border-radius: 20;
    border-radius-precision: .3;
    font-size: 5;
    font-weight: bold;
    font-color: rgb(104,34,139);
    slider-border-radius-precision: .3;
    slider-border-radius: 20;
}
.pcolored{
    bg-color: rgb(255,165,0);
    border-radius: 20;
    border-radius-precision: .3;
    font-size: 5;
    font-weight: bold;
    font-color: rgb(104,34,139);
    slider-border-radius-precision: .3;
    slider-border-radius: 20;
    


}

boundaryslider.colored,
xyslider.colored,
slider.colored {
    bg-color: rgba(75, 0, 130, 150);
}
'''

css_add_sheet(additional_css)



current_dir = os.path.dirname(__file__)
bubblelist = []

def action_close_menu(menu, w, args, *largs):
    menu.parent.remove_widget(menu)
    del menu

def bubble_activate(image,*largs):
        print "i pushed it"
        s=largs[0]
        
        s.replace("pic","buh")
        S=s[0:46]
        a=s[49]
        print a
        if a=="3":
           print "it is 3"
           S+"pic33.png"
           print S
        img = Loader.image(largs[0])
        x=image.x
        y=image.y
        b = MTScatterImage(image=img, pos=(200,200))
        w= MTWindow()
        w.add_widget(b)
        #falls du eine Idee hast welche ist das Unterschied zwischen diese beide Kode zeilen
        #Variante1:
        #S = 'xxxxSPAMxxxxSPAMxxxx'
        #print S.replace("SPAM", "EGGS", 1)
        #S + 'buhuhuhu'
        #print S
        #Variante2:
        #word = 'Help' 
        #print word
        #print '<' + word*5 + '>'

class MTPhoto(MTKineticItem):
    def __init__(self, **kwargs):
        super(MTPhoto, self).__init__(**kwargs)
        
        self.filename = kwargs.get('filename')
        self.image    = pymt.Image(self.filename)
        self.scale = 1   
    
    def draw(self):
        self.image.pos  = self.pos
        self.image.scale= self.scale
        self.image.draw()
        



class MusicBubble(MTScatterImage):
    def __init__(self, **kwargs):
        kwargs.setdefault('instrument', 0)
        self.filename = kwargs.get('filename')
        img = Loader.image(self.filename)
        
        x = int(random.uniform(300, 600))
        y = int(random.uniform(100, 500))
        
        # make sequence for this instrument
        self.seq = EventManager.getInstance().createSequence()
        ''' TODO auswahl des instruments muss hier noch rein '''
        self.seq.setInstrument(kwargs.get('instrument'))
        
        self.volume = Constants.SEQUENCE_START_VOLUME
        
        # this is used to ensure that the on_touch_up handler just
        # executes one time. see on_touch_up event handler
        self.touch_up_oneTime = 0.0
        
        super(MusicBubble, self).__init__(image=img, pos=(x,y), scale=0.8, **kwargs)
        self.register_event_type('on_tap')
    
    def on_tap(self, touch):
        #matrix = ButtonMatrix.createButtonMatrix()
        matrix = ButtonMatrix.NotesMatrix(sequence=self.seq)
    
    def on_touch_down(self, touch):
        # check if the touch is inside the widget
        if not self.collide_point(*touch.pos):
            return super(MusicBubble, self).on_touch_down(touch)
        
        # remember time to tell if it is a tap or move    
        touch.userdata['tap_widget'] = self
        touch.userdata['start_time'] = time.time()        
        
        #return same as super event handler to get normal manipulations
        return super(MusicBubble, self).on_touch_down(touch)
    
    def on_transform(self, angle, scale, trans, point):
        if (self.volume < 20):
            self.volume = 20
            
        self.volume = int(self.volume * scale)
        
        if (self.volume > 127):
            self.volume = 127
            
        if (self.volume < 0):
            self.volume = 0
            
        self.seq.setVolume(self.volume)
    
    def on_touch_up(self, touch):
        '''
        EventSystem dispatches this event some times twice per
        on_touch_down it's result is: on_tap event will be fired
        2 time although I just tapped one time.
        
        This ensures that only one dispatch will be served.
        '''
        if ((time.time()-self.touch_up_oneTime)<0.2):
            return super(MusicBubble, self).on_touch_up(touch)
        else:
            self.touch_up_oneTime = time.time()
        
        # is it my touch?
        if not touch.userdata.get('tap_widget') == self:
            return super(MusicBubble, self).on_touch_up(touch)
        
        #if the touch was tapped, it has start time set,
        #so check if it was short enough to dispatch event
        start_time = touch.userdata['start_time']
        stop_time = time.time()
        if (stop_time - start_time) < 0.2:
            start_time=0
            self.dispatch_event('on_tap', touch)
            
        # check, if we've dropped into the trash
        ''' TODO verbessern mit self.collide(muelleimer) '''
        if touch.x>700 and touch.y<100:
            self.__destructor()
            
        # check, if we've dropped into the "arpeggio-zone":
        if touch.x < 150 and touch.y < 100:
            if not self.seq.arpeggiated:
                self.image_backup = self.image
                imgPath = os.path.join(current_dir, 'instruments', 'arp.png')
                #imgPath = self.filename[:len(self.filename) - 4] + "_arp.png"
                self.image = Loader.image(imgPath)
                self.seq.arpeggiated = True
                self.seq.transformRawDataToPlayData()
        else:
            if self.seq.arpeggiated:
                self.seq.arpeggiated = False
                self.seq.transformRawDataToPlayData()
                ''' TODO Mute all notes '''
                if self.image_backup != None:
                    self.image = self.image_backup

        #return same as super event handler to get normal manipulations
        return super(MusicBubble, self).on_touch_up(touch)
        
    def on_touch_move(self, touch):
        ''' TODO check, if we're leaving the allowed area (e.g. we drag on the menu). '''
        return super(MusicBubble, self).on_touch_move(touch)
    
    ''' use this to delete this biubble '''
    def __destructor(self):
        # remove bubble from window
        getWindow().remove_widget(self)
        # delete sequence
        self.seq.delete()
        # destroy self
        del self
        

class Showinstruments(MTWidget):
    def __init__(self, **kwargs):
        super(Showinstruments, self).__init__(**kwargs)
        self.list = MTKineticList(size=(300, 300),
                        deletable=False, searchable=False,
                        title= None, padding_y = 1,
                        padding_x=1, friction=1)
        self.list.size = (115, 304)
        self.list.pos = (163,270)
        self.add_widget(self.list)
        self.bubbles = []
        
        
        for p in range(8):
            imgName = os.path.join(current_dir, 'instruments', 'pic%d.png' % (p+1))
            item = MTPhoto(filename = imgName )
            item.connect('on_press', curry(self.on_item_press, item))
            self.list.add_widget(item)
        
        
        # states
        self.current = None
        self.animation = None
        self.alpha = 0.00
        self.red = 0.7
        self.green = 0.4
        self.blue = 0.9
        self.radius = 60
        self.highlightred = self.red * 1.25
        if(self.highlightred > 1):
            self.highlightred = 1
        
        self.highlightblue = self.blue * 1.25
        if(self.highlightblue > 1):
            self.highlightblue = 1
        
        self.highlightgreen = self.green * 1.25
        if(self.highlightgreen > 1):
            self.highlightgreen = 1
        
        getClock().schedule_once(self.ListFade, 1.0)
        self.fadein = Animation(d=0.3, alpha=0.7)
        self.fadeout = Animation(d=0.7, alpha=0)
        
        self.do(self.fadein)
        self.showing = True
        self.highlight = True
        self.current = None    
    
    
    def on_item_press(self, item, *largs):
        if self.current is not None:
            self.current.selected = False
        self.current = item
        self.current.selected = True
        a = self.current.filename
        
        # get instrument no. from filename
        instrument = int(a[len(a)-5])
        # transfer this number to general midi instrument numbers
        instrDict = {1:117, 2:66, 3:59, 4:1, 5:41, 6:26, 7:28, 8:47} 
        
        self.m = MusicBubble(filename = a, instrument=instrDict[instrument])
        
        '''
        to read
        
        Ella hat die MusicBubble in ShowInstruments gepackt. Das macht keinen
        Sinn! Das muss in das Window eingehaengt werden. Andernfalls kommen die 
        on_press handler nicht durch weil an der falschen stelle haengt. 
        '''
        getWindow().add_widget(self.m)
        #self.add_widget(self.m) 
        
        
        self.bubbles.append(self.m)
        
        '''
        to read
        
        ich weiss nicht wofuer hier ein window erzeugt werden sollte, aber das ist
        nicht gut neue sachen in neue windows zu stecken. jedes window ist ein
        input consumer. gibt es viele windows, gibts auch viele komplikationen
        
        wenn was ins hauptfenster soll, dann wie oben per getWindow() einhaengen.
        '''
        #W = MTWindow() 
    
    
    def on_draw(self):
        super(Showinstruments, self).on_draw()
    
    def draw(self):
        with DO(gx_matrix, gx_blending):
            if self.highlight:
                self.highlightalpha = self.alpha * 1.25
                if(self.highlightalpha > 1):
                    self.highlightalpha = 1
                glColor4f(self.highlightred, self.highlightgreen, self.highlightblue, self.highlightalpha)
            glColor4f(self.red,self.green,self.blue,self.alpha)
            drawRoundedRectangle(pos=(self.list.x, self.list.y),size = (self.list.width, self.list.height))
        super(Showinstruments, self).draw()
    def ListFade(self,dt):
        self.do(self.fadeout)
    
    
class Showslider(MTSlider):
    def __init__(self, **kwargs):
        super(Showslider, self).__init__(**kwargs)
        
        self.size = (50, 300)
        self.pos = (180,263)
        
        self.min = 20
        self.max = 220
        
        self.alpha = 0.00
        self.red = 0.7
        self.green = 0.4
        self.blue = 0.9
        self.radius = 60
        self.highlightred = self.red * 1.25
        if(self.highlightred > 1):
            self.highlightred = 1
        
        self.highlightblue = self.blue * 1.25
        if(self.highlightblue > 1):
            self.highlightblue = 1
        
        self.highlightgreen = self.green * 1.25
        if(self.highlightgreen > 1):
            self.highlightgreen = 1
        
        getClock().schedule_once(self.ListFade, 1.0)
        self.fadein = Animation(d=0.3, alpha=0.7)
        self.fadeout = Animation(d=0.7, alpha=0)
        
        self.do(self.fadein)
        self.showing = True
        self.highlight = True      
        self.current = None       
    
    def draw(self):
        with DO(gx_matrix, gx_blending):
            if self.highlight:
                self.highlightalpha = self.alpha * 1.25
                if(self.highlightalpha > 1):
                   self.highlightalpha = 1
                glColor4f(self.highlightred, self.highlightgreen, self.highlightblue, self.highlightalpha)
            glColor4f(self.red,self.green,self.blue,self.alpha)
            drawRoundedRectangle(pos=(self.x+4, self.y+4),size = (self.width-7, self.height-10))
        super(Showslider, self).draw()
    def ListFade(self,dt):
        self.do(self.fadeout)
    

class Menubut(MTWidget):
    def __init__(self, **kwargs):
        super(Menubut, self).__init__(**kwargs)
        W = MTWindow()
        print W.height
        imgName = os.path.join(current_dir, 'instruments', 'menu1.png')
        self.object = MTContainer(Image(imgName), pos =(0,100))
        self.add_widget(self.object)
        imgName = os.path.join(current_dir,'instruments','trashcan.png')
        self.object = MTContainer(Image(imgName),pos = (720,0))
        self.add_widget(self.object)
        self.btn0 = MTButton(label='Arpeggiator', size = (100,60), cls=('simple', 'colored'))
        self.btn0.push_handlers(on_press=self.arpegiator)
        self.btn1 = MTButton(label='Bpm', size = (100,60), cls=('simple', 'colored'))
        self.btn1.push_handlers(on_press=self.bpm)
        self.btn2 = MTButton(label='Delay', size = (100,60), cls=('simple', 'colored'))
        self.btn2.push_handlers(on_press=self.delay)
        self.btn3 = MTButton(label='Volume', size = (100,60), cls=('simple', 'colored'))
        self.btn3.push_handlers(on_press=self.volume)
        self.btn4 = MTButton(label='Instruments', size = (100,60), cls=('simple', 'colored'))
        self.btn4.push_handlers(on_press=self.instruments)
        self.buttons = MTBoxLayout(orientation='vertical',padding = 10, spacing = 3, pos = (30, W.height-450))
        self.buttons.add_widget(self.btn0)
        self.buttons.add_widget(self.btn1)
        self.buttons.add_widget(self.btn2)
        self.buttons.add_widget(self.btn3)
        self.buttons.add_widget(self.btn4)
        self.add_widget(self.buttons)
    
    
    def clear(self, *largs):
        self.children.clear()
        W=MTWindow()
        imgName = os.path.join(current_dir, 'instruments', 'menu1.png')
        self.object = MTContainer(Image(imgName), pos =(0,100))
        self.add_widget(self.object)
        imgName = os.path.join(current_dir,'instruments','trashcan.png')
        self.object = MTContainer(Image(imgName),pos = (720,0))
        self.add_widget(self.object)
        self.btn0 = MTButton(label='Arpeggiator', size = (100,60), cls=('simple', 'colored'))
        self.btn0.push_handlers(on_press=self.arpegiator)
        self.btn1 = MTButton(label='Bpm', size = (100,60), cls=('simple', 'colored'))
        self.btn1.push_handlers(on_press=self.bpm)
        self.btn2 = MTButton(label='Delay', size = (100,60), cls=('simple', 'colored'))
        self.btn2.push_handlers(on_press=self.delay)
        self.btn3 = MTButton(label='Volume', size = (100,60), cls=('simple', 'colored'))
        self.btn3.push_handlers(on_press=self.volume)
        self.btn4 = MTButton(label='Instruments', size = (100,60), cls=('simple', 'colored'))
        self.btn4.push_handlers(on_press=self.instruments)
        self.buttons = MTBoxLayout(orientation='vertical',padding = 10, spacing = 3, pos = (30, W.height-450))
        self.buttons.add_widget(self.btn0)
        self.buttons.add_widget(self.btn1)
        self.buttons.add_widget(self.btn2)
        self.buttons.add_widget(self.btn3)
        self.buttons.add_widget(self.btn4)
        self.add_widget(self.buttons)
    
    
    def arpegiator(self, *largs):
        self.clear()
        c = self.btn0
        x = c.x
        y = c.y
        self.remove_widget(c)
        btn = MTButton(label='Arpeggiator', size = (100,60),pos = (x,y), cls=('simple','pcolored'))
        btn.push_handlers(on_press=self.clear)
        self.add_widget(btn)
    
    
    def bpm(self, *largs):
        self.clear()
        c = self.btn1
        x = c.x
        y = c.y
        self.remove_widget(c)
        btn = MTButton(label='Bpm', size = (100,60),pos = (x,y), cls=('simple','pcolored'))
        btn.push_handlers(on_press=self.clear)
        self.add_widget(btn)
        l1 = MTBoxLayout(orientation='vertical',padding = 10, spacing = 3, pos= (180,263))
        m = Showslider(cls=('simple', 'colored'), orientation='vertical', value=EventManager.getInstance().getBPM())
        m.connect('on_value_change',self.bpmSlider_value_change)
        l1.add_widget(m)
        self.add_widget(l1)
         
    ''' event handler for BPM slider's on_value_change '''                                 
    def bpmSlider_value_change(self,value):
        try:
            EventManager.getInstance().setBPM(value)
        except: 
            pass
    
    def volume(self, *largs):
        self.clear()
        c = self.btn3
        x = c.x
        y = c.y
        self.remove_widget(c)
        btn = MTButton(label='Volume', size = (100,60),pos = (x,y), cls=('simple','pcolored'))
        btn.push_handlers(on_press=self.clear)
        self.add_widget(btn)
        l2 = MTBoxLayout(orientation='vertical',padding = 10, spacing = 3, pos= (180,263))
        m = Showslider(cls=('simple', 'colored'), orientation='vertical', value=EventManager.getInstance().getVolume())
        m.min = 0
        m.max = 100
        m.connect('on_value_change',self.volumeSlider_value_change)
        l2.add_widget(m)
        self.add_widget(l2)
    
    ''' event handler for volume slider's on_value_change '''
    def volumeSlider_value_change(self,value):
        try:
            EventManager.getInstance().setVolume(value)
        except: 
            pass
        
    def delay(self, *largs):
        self.clear()
        c = self.btn2 
        x = c.x
        y = c.y
        self.remove_widget(c)
        btn = MTButton(label='Delay', size = (100,60),pos = (x,y), cls=('simple','pcolored'))
        btn.push_handlers(on_press=self.clear)
        self.add_widget(btn)
        l3 = MTBoxLayout(orientation='vertical',padding = 10, spacing = 3, pos= (180,263))
        m = Showslider(cls=('simple', 'colored'), orientation='vertical', value=50)
        l3.add_widget(m)
        self.add_widget(l3)
                        
    def instruments(self, *largs):
        self.clear()
        c = self.btn4
        x = c.x
        y = c.y
        self.remove_widget(c)
        btn = MTButton(label='Instruments', size = (100,60),pos = (x,y), cls=('simple','pcolored'))
        btn.push_handlers(on_press=self.clear)
        self.add_widget(btn)
        l4 = MTBoxLayout(orientation='vertical',padding = 10, spacing = 3)
        list = Showinstruments()
        l4.add_widget(list)
        self.add_widget(l4)
        
    

def createMainscreen():
    fl = Menubut()
    w = getWindow()
    w.add_widget(fl)



 
