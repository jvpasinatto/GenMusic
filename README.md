# :musical_note: GenMusic 

Script that allows creation of random melodies and progressions.


## Requirements

* [librosa](https://librosa.github.io/librosa/)
* [numpy](https://www.numpy.org/)

## Usage

```python
from GenMusic import GMusic as gm

#Converts midi note to frequency in Hz.
gm.midi2freq(self, n:int)

#Converts midi note to the note representation in a string.
gm.midi2note(self, n:int)

#Converts the frequency in Hz to the midi note.
gm.freq2midi(self, freq:float)

#Put delay in a sound.
gm.delay(self, time:float, attenuation:float):

#Writes a vector to a .wav file.
gm.to_wav(sound:numpy.array, file_name:str, sf=44100):

```
