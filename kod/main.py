from ac import Recorder
from ca import Player
import keyboard as kb

try:
    samplerate = abs(int(input("Podaj częstotliwość próbkowania [48000]: ")))
except:
    samplerate = 48000


try:
    quantization = int(input("Wybierz poziom kwantyzacji (8, [16], 32): "))
except:
    quantization = 16
if quantization not in [8, 16, 32]:
    exit("Czytac nie umiesz?")


REC = Recorder(samplerate=samplerate)

print("""
    Trzymaj 'r' aby nagrywać
    Wciśnij 's' aby zapisać nagranie
    Wciśnij 'p' aby odtworzyć nagranie
    Wciśnij 'q' aby zakończyć program
""")

PLAY = Player(samplerate=samplerate)
last_filename = ""

while not kb.is_pressed('q'):
    if kb.is_pressed('r'):
        REC.record(1)
    if kb.is_pressed('s'):
        last_filename = input("Nazwij plik (nie podawaj rozszerzenia): ")
        REC.saveToFile(last_filename, quantization)
    if kb.is_pressed('p'):
        print("Odtwarzam oryginalne nagranie...")
        SNR = PLAY.playData(REC.getAudio())
        print("SNR oryginalnego nagrania to: {}dB".format(SNR))
        if last_filename != "":
            print("Odtwarzam zapisane nagranie...")
            SNR = PLAY.playWav("{}.wav".format(last_filename))
            print("SNR zapisanego nagrania to: {}dB".format(SNR))


