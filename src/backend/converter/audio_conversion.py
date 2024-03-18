import os
import librosa
import io
import numpy as np

def convert(audio) :
    #audio.seek(0)
    b = io.BytesIO(audio.read())
    a = np.frombuffer(b.getvalue())
    S = np.abs(librosa.stft(a))
    print(S)
    print(S.shape)
    return audio