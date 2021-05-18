from typing import Optional
from numpy.lib.twodim_base import _diag_dispatcher
import soundcard as sc
import numpy as np
from scipy.io.wavfile import read


def signaltonoise(a, axis=0, ddof=0):
    # Zwraca w dB SNR
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return abs(20*np.log10(abs(np.where(sd == 0, 0, m/sd))))

class Player:


    def __init__(self, device=None, samplerate : Optional[int]=48000, channels : Optional[list] = [0,1]) -> None:
        """
        device : głośnik z biblioteki soundcard (domyślnie, domyślny)\n
        samplerate : częstotliwość próbkowania\n
        channels : lista kanałów na których ma być odtwarzany dźwięk (dotyczy tylko playData())
        """
        self.device = device if device != None else sc.default_speaker()

        self.samplerate = samplerate
        self.channels = channels

    def playData(self, data : np.ndarray):
        """
        data - numpy.ndarray
        zwraca -> SNR
        """
        # odtwarzanie dzięku 
        self.device.play(data, self.samplerate, self.channels)
        return signaltonoise(data)

    def playWav(self, src : str):
        """
        src : ścieżka do pliku wav
        zwraca -> SNR
        """

        # zapisanie do zmiennej wartości z czytanego pliku
        data = read(src)
        samplerate = data[0]
        # konwersja intów na floaty
        data = np.float64(data[1]/np.max(abs(data[1])))
        channels = []

        for i in range(len(data[0])):
            channels.append(i)
        # odtwarzanie dzwięku
        self.device.play(data, samplerate, channels)

        return signaltonoise(data)