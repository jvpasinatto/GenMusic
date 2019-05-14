import numpy as np

class GMusic(object):
    
    def __init__(self):
        self.sf = 44100.
        self.info = {}
        self.info['sample_frequency'] = self.sf

    def __sel_scale(self, d_scale):
        """
        Select the desired scale, all MIDI scales referenced on C4 = 60.
        """
        if d_scale == "Major":
            return [60, 62, 64, 65, 67, 69, 71, 72]
        elif d_scale == "Minor":
            return [60, 62, 63, 65, 67, 68, 70, 72] 
        elif d_scale == "Chromatic":
            return [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72]
        elif d_scale == "MajorPentatonic":
            return [60, 62, 64, 67, 69, 72]
        elif d_scale == "MinorPentatonic":
            return [60, 63, 65, 67, 70, 72]
        else:
            print("Error!, scale not found.")
            exit()


    def __selChord(self, d_chord):
        """
        Select the desired chord, all MIDI chords referenced on C4 = 60
        """
        if d_chord == "Major":
            n_chord = [60, 64, 67]
        elif d_chord == "Minor":
            n_chord = [60, 63, 67]
        elif d_chord == "Major7":
            n_chord = [60, 64, 67, 71]
        elif d_chord == "Minor7":
            n_chord = [60, 63, 67, 70]
        elif d_chord == "HDim":
            n_chord = [60, 63, 66, 70]
        elif d_chord == "Dim":
            n_chord = [60, 63, 66, 69]
        elif d_chord == "Dom":
            n_chord = [60, 64, 67, 70]
        elif d_chord == "Sus2":
            n_chord = [60, 62, 67]
        elif d_chord == "Sus4":
            n_chord = [60, 65, 67]
        elif d_chord == "Aug":
            n_chord = [60, 65, 68]
        else:
            print("Error!, Chord not found.")
            exit()
        return n_chord


    def __transpose(self, key, w):
        """
        Transpose the scale or chord to the desired key.
        """
        n = 0
        if len(key) == 2:
            if key[1] == "#":
                n = 1
            elif key[1] == "b":
                n = -1
            else:
                print("Error!, only # for sharp and b for flat.")
                exit()
            key = key[0]
        
        if key == "C":
            pass
        elif key == "D":
            n = n + 2
        elif key == "E":
            n = n + 4
        elif key == "F":
            n = n + 5
        elif key == "G":
            n = n + 7
        elif key == "A":
            n = n + 9
        elif key == "B":
            n = n + 11

        sch = [x+n for x in w]
        return sch


    def __lenght_vector(self, n_notes, totalLenght):

        '''
        Creates a list of random durations of each note that do not exceed the total lenght of the melody.
        '''
        minimum_duration = 100

        if n_notes > totalLenght / minimum_duration:
            print("Error, Number of Notes <= TotalLenght*10)")
            exit()
        else:
            v = minimum_duration * np.ones(n_notes)
            while sum(v) < totalLenght:
                i = np.random.randint(0, n_notes)
                v[i] = v[i] + 100
        return v


    def __harmonic_field(self, key, field):
        if field == "Major":
            major_harmonic = ["Major", "Minor", "Minor", "Major", "Major", "Minor", "HDim"]
            scale = self.__sel_scale("Major")
            scale = self.__transpose(key, scale)
            list_chord = []
            for i, k in list(zip(major_harmonic, scale)):
                y = self.midi2note(k)
                chord = self.__selChord(i)
                chord = self.__transpose(y, chord)
                list_chord.append(chord)
            return list_chord
        elif field == "Minor":
            minor_harmonic = ["Minor", "Major7", "HDim", "Major7", "Minor7", "Minor7", "Major7", "Dim"]
            scale = self.__sel_scale("Minor")
            list_chord = []
            for i, k in list(zip(minor_harmonic, scale)):
                y = self.midi2note(k)
                chord = self.__selChord(i)
                chord = self.__transpose(y, chord)
                list_chord.append(chord)
            return list_chord
        else:
            print("Error!")
            exit()


    def __generate_chord(self, T, chord):
        T = T/1000
        t = np.array(range(int(int(self.sf) * T))) / self.sf     #Time vector
        chord_freqs = [self.midi2freq(n) for n in chord]         #Convert to Hz
        waves = [np.cos(2 * np.pi * f * t) for f in chord_freqs] #List of cossines that form the chord
        complete_chord = sum(waves)
        return complete_chord


    def midi2freq(self, n:int):
        """
        Converts midi note to frequency in Hz.
        """
        return 440*2**((n-69)/12)


    def midi2note(self, n:int):
        """
        Converts midi note to the note representation in a string.
        """
        n = n%12
        if n == 0:
            return 'C'
        elif n == 1:
            return 'C#'
        elif n == 2:
            return 'D'
        elif n == 3:
            return 'D#'
        elif n == 4:
            return 'E'
        elif n == 5:
            return 'F'
        elif n == 6:
            return 'F#'
        elif n == 7:
            return 'G'
        elif n == 8:
            return 'G#'
        elif n == 9:
            return 'A'
        elif n == 10:
            return 'A#'
        elif n == 11:
            return 'B'
        else:
            print('Error')
            exit()


    def freq2midi(self, freq:float):
        """
        Converts the frequency in Hz to the midi note.
        """
        freq = round(freq)
        n = 69 + 12*np.log2(freq/440)
        return round(n)
  

    def midi2notelist(self, midi_list):
        note_list = []
        for i in midi_list:
            note = self.midi2note(n=i)
            note_list.append(note)
        return note_list


    def delay(self, time:float, attenuation:float):
        """
        Put delay in a sound.

        ---------------------
        time: miliseconds

        attenuation: [0,1]
        """

        xx =  attenuation * self.sound
        z = np.zeros(int(self.sf/1000 * time))
        x = np.concatenate((z, xx), axis=0)
        y = np.concatenate((self.sound, z), axis=0)
        self.delayed = np.sum([x, y], axis=0)
        self.info['delay_time'] = time
        self.info['delay_attenuation'] = attenuation
    

    def to_wav(sound, file_name:str, sf=44100):
        """
        Writes a vector to a .wav file.
        """
        import librosa

        x = sound*0.6 #Atenuate to not clip
        librosa.output.write_wav(file_name, sound, sr=44100, norm=True)


    def beat2sample(bpm:int):
        one_beat = (44100* 60)/bpm
        return int(one_beat)

    def behaved_lenght(bpm:int, totalLenght:int):
        beat = GMusic.beat2sample(bpm)
        beats = round((totalLenght * 44100)/beat)
        lenghts_list = [round(beat/44100, 3) for i in range(beats)]
        return lenghts_list
    


class Melody(GMusic):
    
    def __init__(self):
        GMusic.__init__(self)

    def __sel_scale(self, d_scale):
        return self._GMusic__sel_scale(d_scale)

    def __transpose(self, key, s_scale):
        return self._GMusic__transpose(key, s_scale)

    def __lenght_vector(self, n_chords, totalLenght):
        return self._GMusic__lenght_vector(n_chords, totalLenght)
    
    def random_melody(self,  totalLenght:int,  n_notes:int, key:str, d_scale:str):
        """
        Creates a random melody.
        """

        s_scale = self.__sel_scale(d_scale)
        scale = self.__transpose(key, s_scale)
        lenghts_list = self.__lenght_vector(n_notes, totalLenght)
        x = []
        midi_list = []

        for i in range(len(lenghts_list)):
            T = lenghts_list[i]                        #Duration of the note
            T = T/1000
            pos = np.random.randint(0, len(scale))     #Random position of the note in the scale
            n = scale[pos]                             #MIDI note.
            midi_list.append(n)                        #Add MIDI not to MIDI list
            f = self.midi2freq(n)                      #Converting MIDI to Frequency
            t = np.array(range(int(int(self.sf) * T))) / self.sf #Time vector
            xx = np.cos(2 * np.pi * f * t)             #Generate wave
            x = np.concatenate((x, xx), axis=0)        #Concatenate waves

        self.melody = x
        self.info['lenghts_list'] = lenghts_list
        self.info['melody_list'] = midi_list
        self.info['note_list'] = self.midi2notelist(midi_list)

        lenghts_listm = [i for i in lenghts_list]
        messages = [[i,k] for i,k in zip(midi_list, lenghts_listm)]
        self.messages = messages

class Progression(GMusic):

    def __init__(self):
        GMusic.__init__(self)

    def __harmonic_field(self, key, harmonic):
        return self._GMusic__harmonic_field(key, harmonic)
    
    def __lenght_vector(self, n_chords, totalLenght):
        return self._GMusic__lenght_vector(n_chords, totalLenght)

    def __generate_chord(self, i, c):
        return self._GMusic__generate_chord(i, c)

    def random_progression(self, totalLenght:int, n_chords:int, key:str, harmonic:str):
        """
        Creates a random progression of chords.
        """

        chord_list1 = self.__harmonic_field(key, harmonic)
        lenghts_list = self.__lenght_vector(n_chords, totalLenght)

        x = []
        chord_list = []
        cnt = 0

        for i in range(len(lenghts_list)):
            pos = np.random.randint(0, len(chord_list1))      #Random position of the chord in list
            c = chord_list1[pos]
            chord_list.append(c)
            xx = self.__generate_chord(lenghts_list[i], c)
            x = np.concatenate((x, xx), axis=0)                
            cnt = cnt + 1

        self.prog = x
        self.info['lenghts_list'] = lenghts_list
        self.info['chord_list'] = chord_list


def midi2notelist(midi_list):
    note_list = []
    for i in midi_list:
        note_list.append(midi2note(i))
    return note_list



