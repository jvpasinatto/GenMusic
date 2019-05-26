def print_mid(filename):
    from mido import MidiFile
    import sys
    midi_file = MidiFile(filename)
    for i, track in enumerate(midi_file.tracks):
        sys.stdout.write('=== Track {}\n'.format(i))
        for message in track:
            sys.stdout.write('  {!r}\n'.format(message))