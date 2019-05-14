def to_midi(messages):
    import time
    import mido
    import rtmidi
    from rtmidi.midiconstants import NOTE_OFF, NOTE_ON

    '''
    a[x][0] = note
    a[x][1] = velocity
    a[x][2] = duration
    '''
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()

    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("My virtual output")

    for i in messages:
        note_on = [NOTE_ON, messages[i][0], messages[i][1]]
        note_off = [NOTE_OFF, messages[i][0], 1]

        midiout.send_message(note_on)
        time.sleep(messages[i][2])
        midiout.send_message(note_off)

    del midiout

