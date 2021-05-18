from typing import Optional
import soundcard as sc
import numpy as np
from scipy.io.wavfile import write

class Recorder:

    def __init__(self, device = None, samplerate : Optional[int] = 48000, channels : Optional[list] = [0,1]) -> None:
        """
        device : mikrofon z biblioteki soundcard (domyślnie, domyślny)\n
        samplerate : częstotliwość próbkowania\n
        channels : lista kanałów na których ma być nagrywany dźwięk
        """

        self.device = device if device!=None else sc.default_microphone()
        
        self.samplerate = samplerate
        
        self.channels = channels

        self.audiosave = None

    
    def record(self, seconds : int) -> None:
        """
        seconds - ile sekund nagrać
        """

        # jeżeli self.audiosave jest puste to przypisz do niego nagranie
        if type(self.audiosave) != np.ndarray:
            self.audiosave = self.device.record(seconds * self.samplerate, self.samplerate, self.channels)
        # jeżeli self.audiosave nie jest puste dopisz do niego nagranie
        else:
            test = self.device.record(seconds * self.samplerate, self.samplerate, self.channels)
            self.audiosave = np.concatenate((self.audiosave, test), axis=None)


    def getAudio(self) -> np.ndarray:
        return self.audiosave

    def saveToFile(self, fname : str, bps : Optional[int] = 16) -> None:
        '''
        fname - nazwa pliku bez rozszerzenia
        bps - poziom kwantowanaia [8, 16, 32] (domyslnie 16)
        '''
        
        if not bps in [8, 16, 32]:
            raise Exception("bps can be represented only by 8, 16 or 32 bits")

        data = self.audiosave

        # poziom kwantyzacji
        if bps == 8:
            data = np.int8(data/np.max(abs(data)) * np.iinfo("int8").max)
        if bps == 16:
            data = np.int16(data/np.max(abs(data)) * np.iinfo("int16").max)
        if bps == 32:
            data = np.int32(data/np.max(abs(data)) * np.iinfo("int32").max)

        # zapis do pliku przy użyciu biblioteki scipy
        write("{}.wav".format(fname), self.samplerate, data)
