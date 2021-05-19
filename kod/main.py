from ac import Recorder
from ca import Player
import keyboard as kb

test = Recorder()

while not kb.is_pressed("q"):
    if kb.is_pressed("r"):
        test.record(1)



test.saveToFile("test8", 8)
test.saveToFile("test16", 16)
test.saveToFile("test32", 32)

testAudio = Player()
testAudio.playData(test.getAudio())