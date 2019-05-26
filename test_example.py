'''
Usage example 1.
Creating a random melody and progression in the G Major scale.
Putting the result into a stereo .wav file.
'''

from GenMusic import GMusic, Melody, Progression
import numpy as np


a = Melody()
a.random_melody(60000,30,"G","Major")
b = Progression()
b.random_progression(60000,10,"G","Major")

melodia = a.melody
chord = b.prog

print(len(melodia))
print(len(chord))

if len(melodia) > len(chord):
    n = len(melodia) - len(chord)
    chord = np.append(chord, np.zeros(n))
else:
    n = len(chord) - len(melodia)
    melodia = np.append(melodia, np.zeros(n))


x = np.vstack((melodia,chord))
GMusic.to_wav(x, 'test.wav')
