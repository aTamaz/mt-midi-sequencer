import Sequence
import EventManager
import gui.temp.helloworld
import gui.myButtonMatrix


# cmd /K "cd C:\Users\Bao\Desktop\Studium\6. Sem SoSe 10\Multitouch Sequencer\repository\tim\midisequencer\MidiOutput+Event && python Main.py"


''' main program for test purposes '''
if __name__ == '__main__':
	print '============================================================'
	print '=================== START =================================='
	print '============================================================'

	# Options:
	amount_sequences = 1
	bpm=128
	#bpm=200

	# Logging On/Off
	logging_sequences=0
	logging_eventSystem=0

	######################################################################
	# edit options above.

	# start manager
	manager=EventManager.EventManager(logging=logging_eventSystem)
	manager.start()
	manager.setBPM(bpm)

	# create sequences and register at manager
	seq1=Sequence.Sequence(id=1, logging=logging_sequences)
	manager.register(seq1, seq1.getMidiData)

	for i in range(2, amount_sequences+1):
		seq=Sequence.Sequence(id=i, logging=logging_sequences)
		manager.register(seq, seq.getMidiData)

	
	# test unregistering a sequence
	seq42=Sequence.Sequence(id=42, logging=logging_sequences)
	manager.register(seq42, seq42.getMidiData)
	manager.unregister(seq42)
	
	
		
	''' hello world beispiel -> slider verstellt bpm '''
	#import gui.temp.helloworld
	#gui.temp.helloworld.setBpmHandler(manager.setBPM)
	#gui.temp.helloworld.go()
	
	''' button matrix beispiel -> 3 toene schmeissen arpeggiator an '''
	gui.myButtonMatrix.go(seq1)
	
	''' testweise gui implementierung von Ella '''
	#import gui.temp.Anim9
	
	#StartHelper().start()

	# if this terminates, program will terminate
	while 1:
		a=1