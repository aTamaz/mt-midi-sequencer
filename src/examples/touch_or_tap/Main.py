'''
Created on 07.07.2010

@author: Bao
'''
from pymt import *
import time, random

class MusicBubble(MTScatterImage):
   def __init__(self, **kwargs):
       super(MusicBubble, self).__init__(scale=0.2, **kwargs)
       self.register_event_type('on_tap')

   def on_tap(self, touch):
       print "default on_tap handler called", self.id

   def on_touch_down(self, touch):
       # if touch is on teh widget remeber the time
       if self.collide_point(*touch.pos):
           touch.userdata['tap_widget'] = self
           touch.userdata['start_time'] = time.time()

       #return same as super event handler to get normal manipulations
       return super(MusicBubble, self).on_touch_down(touch)

   def on_touch_up(self, touch):
       #if teh touch was tapped, it has start time set,
       #so check if it was short enough to dispatch event
       if touch.userdata.get('tap_widget') == self:
           start_time = touch.userdata['start_time']
           stop_time = time.time()
           if (stop_time - start_time) < 0.1:
               self.dispatch_event('on_tap', touch)

       #return same as super event handler to get normal manipulations
       return super(MusicBubble, self).on_touch_up(touch)



#create a root widget and add a label which well set the text on
# when teh user taps a music bubble
root = MTWidget()
root.add_widget(MTLabel(id="message_label", label='action: none yet...'))

#add some randomly positioned MusicBubbles
for i in range(5):
   x = int(random.uniform(300, 600))
   y = int(random.uniform(100, 500))
   r = random.uniform(0,360)
   bubble = MusicBubble(id='bubble #'+str(i), pos=(x,y), rotation=r,
filename="tree.png")
   root.add_widget(bubble)

   #attach another event handler to set the message_label
   def set_label(touch):
       getWidgetById("message_label").label = "TAP! caller: "+touch.userdata['tap_widget'].id
   bubble.connect('on_tap', set_label)

runTouchApp(root)