import time
import numpy as np
import pyaudio
import struct

CHUNK = 1024*2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


def stream(state):
    stream = pyaudio.PyAudio().open(
        format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK
    )

    if state == False:
        stream.stop_stream()
        stream.close()
        pyaudio.PyAudio().terminate()

    data = stream.read(CHUNK)
    dataInt = struct.unpack(str(CHUNK) + 'h', data)
    #print(dataInt)
    return dataInt
    
