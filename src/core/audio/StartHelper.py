import threading

import helloworld

class StartHelper(threading.Thread): # EventWorker runs in its own Thread

    ''' Parameters
        ticktime is the time in seconds between two ticks. default = 1
    '''
    def __init__(self, **kwargs):
        # mandatory for threading
        threading.Thread.__init__(self)

    def run(self):
        print 'SADASDASDASDASDASDASDASDASDAS'
        helloworld.go()


StartHelper().start()
#helloworld.go()