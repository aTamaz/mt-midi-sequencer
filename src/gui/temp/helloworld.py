from pymt import *
import core.audio.EventManager as EventManager


class MTScatterLabel(MTScatterWidget):
    '''Zeigt label in sich selbst an und ist zoombar, rotierbar, verschiebbar
    @param:    label_text gibt den Text an der im Label ist. default='hello world'
    '''
    def __init__(self, **kwargs):
        kwargs.setdefault('label_text', 'hello world')
        super(MTScatterLabel, self).__init__(**kwargs)
        self.label = MTLabel(label=kwargs.get('label_text'), font_size=20, autowidth=True, autoheight=True, pos=(0, 0))
        self.add_widget(self.label)
        self.pos=(200,200)
        self._fitScatterSize()
        win = getWindow()
        win.add_widget(self)

    def _fitScatterSize(self):
        print self.label.width
        self.width = self.label.width
        self.height = self.label.height

    def getHandle(self):
        return self.label

    def setText(self, text):
        self.label.label=text
        self.label.draw()
        self._fitScatterSize()

    def setSize(self, size):
        self.label.font_size=size
        self.label.draw()
        self._fitScatterSize()


################################################################################

bpmHandler = None

def setBpmHandler(method):
    global bpmHandler
    bpmHandler = method

def go():
    # root widget
    root = MTWidget()

    # Label befindet sich in nem MTScatterWidget
    scatterLabel = MTScatterLabel(label_text='Hello World')

    # Layout, das Buttons enthaelt
    btnLayout = MTBoxLayout(orientation='horizontal')

    # Ugh Button
    btnUgh = MTButton(label='Ugh Agh')
    @btnUgh.event
    def on_press(*largs):
        scatterLabel.setText('Ugh Agh!')

    # Hello World Button
    btnHello = MTButton(label='Hello World')
    @btnHello.event
    def on_press(*largs):
        scatterLabel.setText('Hello World')

    # buttons in layout packen und das layout aufs root widget
    btnLayout.add_widget(btnUgh)
    btnLayout.add_widget(btnHello)
    root.add_widget(btnLayout)

    # SLider einbauen fuer Schriftgroesse
    slider = MTSlider(min=10, max=400, value=128, pos=(600,50))
    @slider.event
    def on_value_change(*largs):
        scatterLabel.setSize(slider.value)
        scatterLabel.setText(slider.value)
        try:
            #bpmHandler(slider.value)
            EventManager.getInstance().setBPM(slider.value)
        except:
            pass
        

    root.add_widget(slider)

    runTouchApp(root)