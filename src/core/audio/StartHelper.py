import threading



class StartHelper(threading.Thread): # EventWorker runs in its own Thread

    ''' Parameters
        ticktime is the time in seconds between two ticks. default = 1
    '''
    def __init__(self, **kwargs):
        # mandatory for threading
        threading.Thread.__init__(self)

    def run(self):
        import gui.temp.Anim9


StartHelper().start()
#helloworld.go()