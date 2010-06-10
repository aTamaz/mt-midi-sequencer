'''
Created on 09.06.2010

@author: Bao
'''


'''
TCP Status Messages:

for communication bezween core.audio.OutputAdapter and core.audio.server.MidiServer

message format:
<tick-start><DELIMITER><event-start><DELIMITER><instrument><DELIMITER><channel><DELIMITER><note><DELIMITER><velocity><DELIMITER><status><DELIMITER><event-end><DELIMITER><event-start>...<event-end>...<DELIMITER><tick-end><DELIMITER>
'''
TCP_tick_start     = '<tick-start>'
TCP_tick_end     = '<tick-end'
TCP_event_start    = '<event-start>'
TCP_event_end    = '<event-end>'
TCP_delimiter     = '<*>'