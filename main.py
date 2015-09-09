from livespec import LiveSpectrogram
import alsaaudio, time, audioop
import signal
import sys

SAMP_FREQ = 44100
DOWN_SAMPLE_FACTOR = 1
FREQ_RES = SAMP_FREQ/1500.
TIME_RES = 1/10.

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NORMAL)
inp.setchannels(1)
inp.setrate(SAMP_FREQ)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(160)


spectrogram = LiveSpectrogram(SAMP_FREQ/DOWN_SAMPLE_FACTOR, FREQ_RES, TIME_RES, maxscale=1e8)

def signal_handler(signal, frame):
    spectrogram.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

count = 0
while True:
    # Read data from device
    if not spectrogram.is_alive():
        spectrogram.close()
        sys.exit(0)
    l,data = inp.read()
    for i in range(l):
        if count >= DOWN_SAMPLE_FACTOR:
            spectrogram.new_sample(audioop.getsample(data,2,i))
            count = 0
        count+=1
