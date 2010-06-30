'''
Created on 9 Jun 2010

@author: ELLA
'''
import os
from pymt import *
from OpenGL.GL import *
import math
from random import randint, random
import random
import core.audio.EventManager as EventManager

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
    font-size: 50;
    font-weight: bold;
    font-color: rgb(139,0,139);
    slider-border-radius-precision: .3;
    slider-border-radius: 20;
}
.pcolored{
    bg-color: rgb(104,34,139);
    border-radius: 20;
    border-radius-precision: .3;
    font-size: 40;
    font-weight: bold;
    font-color: rgb(255,125,64);
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
image_fn = os.path.join(os.path.dirname(__file__), 'icons', 'greeny.png')


current_dir = os.path.dirname(__file__)
objlist = []

def action_close_menu(menu, w, args, *largs):
    menu.parent.remove_widget(menu)
    del menu

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
        
class MusicArea(MTWidget):
    def __init__(self, **kwargs):
        super(MusicArea, self).__init__(**kwargs)
        self.pos = (250, 0)
        self.size = (640, 480)
        self.bgcolor = (0,0,0,1)
        self.color = (0,1,0,1.0)
        self.touch_positions = {}
        self.filename = kwargs.get('filename')
        #print self.filename
        self.button = MTImageButton(filename=self.filename, cls = ('simple'))
        self.button.touched = False
        #self.button.connect('on_touch_down', curry(self.music_activate, self.button))
        #self.button.push_handler(on_touch_down=self.music_activate)
        self.add_widget(self.button)
        self.scale = 0.8
        w = MTWindow()
        x = self.width-int(random.uniform(100, w.width-100))
        y = self.height-int(random.uniform(100, w.height-100))
        self.button.pos= (x,y) 
        print self.button 
        W = MTWindow()    
        self.clear = MTButton(label='Clear', pos = (W.width-50,W.height-50),size = (40,40),cls=('simple'))
        self.clear.push_handlers(on_press=self.music_clear)       
        self.add_widget(self.clear)
          
        
        self.selected = None
        self.radius= 60
        self.red = 0.3
        self.green = 0.9
        self.blue = 0.7
        self.alpha = 1
       
    def draw_circle(self):
        
        
        with DO(gx_matrix, gx_blending): 
            glColor4f(self.red,self.green,self.blue,self.alpha)    
            drawCircle(pos=(self.x + self.width/2-15,self.y + self.height/2-10),radius=self.radius, linewidth = 7)
        
      


    def music_clear(self, *largs):
       #print len(self.bubbles)
       #print self.parent
       print len(self.parent.bubbles)
       for a in self.parent.bubbles:
           #print a
           b = self.parent.bubbles.pop()
           print b
           print b.button
           self.remove_widget(b.button)
    
#    def music_activate(self, *largs):
#        print "music activated"
#        self.draw_circle()
    def music_activate(self, touch, *largs):
        print "music activated"
        if not self.collide_point(touch.x, touch.y):
            #print "it colides"
            if self.button.touched == False:
                #print self.button
                self.Abubbles.append(self.button)
                self.touched = True
            else:
                self.button.touched = False
        for a in self.Abubbles:
            print self.Abubbles.pop()  


        
#class MTMusic(MTWidget):
#    def __init__(self, **kwargs):
#        super(MTMusic, self).__init__(**kwargs)
#        
#        self.filename = kwargs.get('filename')
#        #print self.filename
#        self.image    = pymt.Image(self.filename)
#        self.scale = 0.8
#        W = self.get_parent_window()
#        print W
#        w = MTWindow()
#        x = W.width-int(random.uniform(100, w.width-100))
#        y = W.height-int(random.uniform(100, w.height-100))
#        self.pos = (x,y)
#        self.selected = None
#        self.radius= 60
#        self.red = 0.3
#        self.green = 0.9
#        self.blue = 0.7
#        self.alpha = 1
#       
#
#    def on_draw(self):
#        
#        self.image.pos  = self.pos
#        self.image.scale= self.scale 
#        with DO(gx_matrix, gx_blending): 
#            glColor4f(self.red,self.green,self.blue,self.alpha)    
#            drawCircle(pos=(self.x + self.width/2-15,self.y + self.height/2-10),radius=self.radius, linewidth = 7)
#        self.image.draw()
#    def draw(self):
#         #background
#        if self.selected:
#            set_color(0, 0.1, 0)
#        else:
#            set_color(0, 0, 0)
#       


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
        self.Abubbles = []

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
        #print self.current.filename
        a = self.current.filename
        self.m = MusicArea(filename = a)
        #w = self.get_parent_window()
        #w.add_widget(self.object)
        self.add_widget(self.m)
        self.bubbles.append(self.m)
        print self.m
        
        # make sequence for this instrument
        EventManager.getInstance().createSequence()
       
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
        self.btn0 = MTButton(label='Arpegiator', size = (100,60), cls=('simple', 'colored'))
        self.btn0.push_handlers(on_press=self.arpegiator)
        self.btn1 = MTButton(label='BPM', size = (100,60), cls=('simple', 'colored'))
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
        self.btn0 = MTButton(label='Arpegiator', size = (100,60), cls=('simple', 'colored'))
        self.btn0.push_handlers(on_press=self.arpegiator)
        self.btn1 = MTButton(label='BPM', size = (100,60), cls=('simple', 'colored'))
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
#        
   
        
    def arpegiator(self, *largs):
        m = MTButton(label='buhuh', pos = (400,140))
        self.add_widget(m)
        for b in self.children:
            if b == self.buttons:
                a = b.children
                for c in a:
                    if c.label == 'Arpegiator':
                        x = c.x
                        y = c.y
                        self.remove_widget(c)
                        btn = MTButton(label='Arpegiator', size = (100,60),pos = (x,y), cls=('simple','pcolored'))
                        btn.push_handlers(on_press=self.clear)
                        self.add_widget(btn)
                        
        
                       
    def bpm(self, *largs):
          for b in self.children:
            if b == self.buttons:
                a = b.children
                for c in a:
                    if c.label == 'BPM':
                        x = c.x
                        y = c.y
                        self.remove_widget(c)
                        btn = MTButton(label='BPM', size = (100,60),pos = (x,y), cls=('simple','pcolored'))
                        btn.push_handlers(on_press=self.clear)
                        self.add_widget(btn)
                        l1 = MTBoxLayout(orientation='vertical',padding = 10, spacing = 3, pos= (180,263))
                        m = Showslider(cls=('simple', 'colored'), orientation='vertical', value=120)
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
          for b in self.children:
            if b == self.buttons:
                a = b.children
                for c in a:
                    if c.label == 'Volume':
                        x = c.x
                        y = c.y
                        self.remove_widget(c)
                        btn = MTButton(label='Volume', size = (100,60),pos = (x,y), cls=('simple','pcolored'))
                        btn.push_handlers(on_press=self.clear)
                        self.add_widget(btn)
                        l2 = MTBoxLayout(orientation='vertical',padding = 10, spacing = 3, pos= (180,263))
                        m = Showslider(cls=('simple', 'colored'), orientation='vertical', value=50)
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
          for b in self.children:
            if b == self.buttons:
                a = b.children
                for c in a:
                    if c.label == 'Delay':
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
          for b in self.children:
            if b == self.buttons:
                a = b.children
                for c in a:
                    if c.label == 'Instruments':
                        x = c.x
                        y = c.y
                        self.remove_widget(c)
                        btn = MTButton(label='Instruments', size = (100,60),pos = (x,y), cls=('simple','pcolored'))
                        btn.push_handlers(on_press=self.clear)
                        self.add_widget(btn)
                        l4 = MTBoxLayout(orientation='vertical',padding = 10, spacing = 3)
                        list = Showinstruments()
                        l4.add_widget(list)
                        W = MTWindow()
                        self.add_widget(l4)
                       
                
    
#
#    def randomize(self, *largs):
#        w = self.get_parent_window()
#        for letter in self.children:
#            if letter == self.buttons:
#                continue
#            letter.do(Animation(pos=map(lambda x: x * random(), w.size),
#                                f='ease_out_cubic', duration=.5))

    
fl = Menubut()
w = MTWindow()
w.add_widget(fl)
runTouchApp()

if __name__ == '__main__':
    #manager = EventManager.getInstance()
    #seq1=manager.createSequence()
    runTouchApp()
 
