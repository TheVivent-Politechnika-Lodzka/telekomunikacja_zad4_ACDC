from ac import Recorder
from ca import Player


test = Recorder()
test.record(3)
test.saveToFile("test", 32)

testAudio = Player()
print(testAudio.playData(test.getAudio()))
print(testAudio.playWav("test.wav"))