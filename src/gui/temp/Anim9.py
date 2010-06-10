'''
Created on 7 Jun 2010

@author: ELLA
'''
'''
Created on 6 Jun 2010

@author: ELLA
'''
import os
from pymt import *
from OpenGL.GL import *
import math

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
    font-size: 40;
    font-weight: bold;
    font-color: rgb(139,0,139);
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
objlist = []

def action_close_menu(menu, w, args, *largs):
    menu.parent.remove_widget(menu)
    del menu

class MTPhoto(MTKineticItem):
    def __init__(self, **kwargs):
        super(MTPhoto, self).__init__(**kwargs)
        
        self.filename = kwargs.get('filename')
        self.image    = pymt.Image(self.filename)
        #self.size     = self.image.size
        self.scale = 0.8
       


    def draw(self):
        # background
        #if self.selected:
            #set_color(0, 0.1, 0)
        #else:
            #set_color(0, 0, 0)
        #without this the images won;t be shown why???????
        self.image.pos  = self.pos
        # print self.pos
        self.image.scale= self.scale
        self.image.draw()
        


class Showinstruments(MTKineticList):
    def __init__(self, **kwargs):
        kwargs.setdefault('title', None)
        kwargs.setdefault('searchable', False)
        kwargs.setdefault('deletable', False)
        #kwargs.setdefault('padding_x', 1)
        #kwargs.setdefault('padding_y', 0)
        super(Showinstruments, self).__init__(**kwargs)
        self.padding_x = 1
        self.padding_y = 1
        self.size = (120, 300)
        #self.pos = (10,100)
        w = MTKineticItem(label='Close Menu', size=(100, 32),
                          style={'font-size': 12, 'bg-color': (.2, .2, .2, .9)})
        w.push_handlers(on_press=curry(action_close_menu, self, w, []))
        self.add_widget(w)         

        for p in range(12):
            imgName = os.path.join(current_dir, 'instruments', 'pic%d.jpg' % (p+1))
            #print imgName
            item = MTPhoto(filename = imgName )
            item.connect('on_press', curry(self.on_item_press, item))
            self.add_widget(item)
       
       
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
        self.anim1 = Animation(duration=0.3, x=120)
        self.do(self.anim1)  

       
        self.current = None
        
    def on_update(self):
        w = self.get_parent_window()

        
    def on_item_press(self, item, *largs):
        if self.current is not None:
            self.current.selected = False
        self.current = item
        self.current.selected = True
        
    def draw(self):
        with DO(gx_matrix, gx_blending):
            if self.highlight:
                self.highlightalpha = self.alpha * 1.25
                if(self.highlightalpha > 1):
                   self.highlightalpha = 1
                glColor4f(self.highlightred, self.highlightgreen, self.highlightblue, self.highlightalpha)
            glColor4f(self.red,self.green,self.blue,self.alpha)
            drawRoundedRectangle(pos=(self.x-5, self.y-5),size = (self.width + 5, self.height + 10))
        super(Showinstruments, self).draw()
    def ListFade(self,dt):
        self.do(self.fadeout)
       
class Showslider(MTSlider):
    def __init__(self, **kwargs):
        super(Showslider, self).__init__(**kwargs)
        
        self.size = (20, 230)
        #self.pos = (10,100)
       
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
        self.anim1 = Animation(duration=0.3, x=120)
        self.do(self.anim1)  

       
        self.current = None
        
    def on_update(self):
        w = self.get_parent_window()

        
    def on_item_press(self, item, *largs):
        if self.current is not None:
            self.current.selected = False
        self.current = item
        self.current.selected = True
        
    def draw(self):
        with DO(gx_matrix, gx_blending):
            if self.highlight:
                self.highlightalpha = self.alpha * 1.25
                if(self.highlightalpha > 1):
                   self.highlightalpha = 1
                glColor4f(self.highlightred, self.highlightgreen, self.highlightblue, self.highlightalpha)
            glColor4f(self.red,self.green,self.blue,self.alpha)
            drawRoundedRectangle(pos=(self.x, self.y),size = (self.width, self.height))
        super(Showslider, self).draw()
    def ListFade(self,dt):
        self.do(self.fadeout)
              
class MTbut(MTButton):
    def __init__(self, **kwargs):
        super(MTbut, self).__init__(**kwargs)
        self.downcolor = (0.1, .1, .4, .8)
    def resetColor(self, color):
        self.buttoncolor = color
        self.draw()

    def setDownColor(self, downcolor):
        self.downcolor = downcolor
        self.draw()
  
   
        
        
W = MTWindow(style={'bg-color':(0,0,0)})
       
b0 = MTButton(label='Arpegiator', size = (100,60), cls=('simple', 'colored'))
b1 = MTButton(label='BMP', size = (100,60), cls=('simple', 'colored'))
b2 = MTButton(label='Delay', size = (100,60), cls=('simple', 'colored'))
b3 = MTButton(label='Volume', size = (100,60), cls=('simple', 'colored'))
b4 = MTbut(label='Instruments', size = (100,60), cls=('simple', 'colored'))
m = MTBoxLayout(orientation='vertical',padding = 10, spacing = 3, pos = (5, W.height-350))
m.add_widget(b0)
m.add_widget(b1)
m.add_widget(b2)
m.add_widget(b3)
m.add_widget(b4)


   
            
        



    
    
  

l1 = MTBoxLayout(orientation='vertical',padding = 10, spacing = 3)
l2 = MTBoxLayout(orientation='vertical',padding = 10, spacing = 3)

@b4.event
def on_press(*largs):
    b4.setDownColor((0.1, .1, .4, .8))
    list = Showinstruments()
    l1.add_widget(list)
    l1.x = 0
    l1.y = W.height-360
    
@b3.event
def on_press(*largs):
    m = Showslider(cls=('simple', 'colored'), orientation='vertical', value=50)
    l2.add_widget(m)
    l2.x = 0
    l2.y = W.height-360

   
    
    

##W.add_widget(v2)
#W.add_widget(b)
music = MTButton(label="Music",height=50,bg_color=(.3,1,.6,.2),pos=(500,170))

    
W.add_widget(l1) 
  
W.add_widget(l2)  
W.add_widget(music )
W.add_widget(m)

runTouchApp()

#start the application (inits and shows all windows)
if __name__ == '__main__':
    #runTouchApp()
    pass
   


