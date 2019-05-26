# GenMusic

Script that allows creation of random melodies and progression.


## Requirements

* [librosa](https://librosa.github.io/librosa/)
* [numpy](https://www.numpy.org/)

## Methods


midi2freq(self, n:int)

Converts midi note to frequency in Hz.

Parameters:
n (int): Midi note

Returns:
float: Frequency in Hz.


midi2note(self, n:int):

Converts midi note to the note representation in a string.

freq2midi(self, freq:float):

Converts the frequency in Hz to the midi note.


delay(self, time:float, attenuation:float):

Put delay in a sound.

time: miliseconds

attenuation: [0,1]


to_wav(sound, file_name:str, sf=44100):

Writes a vector to a .wav file.
