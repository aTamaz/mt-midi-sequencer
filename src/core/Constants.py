'''
Created on 09.06.2010

@author: Bao
'''


''' Logging '''
LOGGING_sequences=1
LOGGING_eventSystem=1

''' Audio System '''
DEFAULT_bpm=128

'''
TCP Status Messages:

for communication bezween core.audio.OutputAdapter and core.audio.server.MidiServer

message format:
<tick-start><DELIMITER><event-start><DELIMITER><instrument><DELIMITER><channel><DELIMITER><note><DELIMITER><velocity><DELIMITER><status><DELIMITER><event-end><DELIMITER><event-start>...<event-end>...<DELIMITER><tick-end><DELIMITER>
'''
TCP_tick_start      = '<tick-start>'
TCP_tick_end        = '<tick-end'
TCP_event_start     = '<event-start>'
TCP_event_end       = '<event-end>'
TCP_delimiter       = '<*>'
TCP_setBPM          = '<setBPM>'

''' connection setup '''
TCP_ip = '127.0.0.1'
TCP_port = 5005
TCP_buffer_size = 5120


EventManager_playDataQueue_maxsize = 2
MidiServer_playDataQueue_maxsize = 2
