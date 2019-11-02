from itertools import cycle, count
from midiutil import MIDIFile
from notes import *
import music_gen

key = music_gen.gen_key()

chords = music_gen.gen_chords(key)

bass = music_gen.gen_bass(key, chords)

melody = music_gen.gen_melody(key)

CHORD_TRACK = 0
DRUM_TRACK = 1
BASS_TRACK = 2
ATMOS_TRACK = 3
MELODY_TRACK = 4
AAAAA_TRACK = 5
CHORD_CHANNEL  = 0
BASS_CHANNEL = 1
ATMOS_CHANNEL = 2
MELODY_CHANNEL = 3
AAAAA_CHANNEL = 4
DRUM_CHANNEL = 9

CHORD_INSTR = 1
KICK_INSTR = 35
SNARE_INSTR = 38
BASS_INSTR = 33
ATMOS_INSTR = 99
MELODY_INSTR = 24
AAAAA_INSTR = 88

KICK_START = 8
SNARE_START = 16
BASS_START = 24
MELODY_START = 32
AAAAA_START = 40
END = 64

time     = 0    # In beats
duration = 1    # In beats
tempo    = 60   # In BPM
volume   = 100  # 0-127, as per the MIDI standard

myMIDI = MIDIFile(6)
myMIDI.addTempo(CHORD_TRACK, time, tempo)

# chords
print("Generating chords")
myMIDI.addProgramChange(CHORD_TRACK, CHORD_CHANNEL, 0, CHORD_INSTR)
for i, chord in enumerate(cycle(chords)):
    time = i * 2
    if time == END:
        break
    for note in chord:
        myMIDI.addNote(CHORD_TRACK, CHORD_CHANNEL, note, time, 2, volume - 20)

# drums
print("Generating drums")
for i in range(KICK_START, END):
    myMIDI.addNote(DRUM_TRACK, DRUM_CHANNEL, KICK_INSTR, i, 1, volume - 20)

for i in range(SNARE_START, END):
    myMIDI.addNote(DRUM_TRACK, DRUM_CHANNEL, SNARE_INSTR, i+0.5, 1, volume - 20)


# bass
print("Generating bass")
myMIDI.addProgramChange(BASS_TRACK, BASS_CHANNEL, 0, BASS_INSTR)
for i, note in enumerate(cycle(bass)):
    time = BASS_START + i * 2
    if time == END:
        break
    myMIDI.addNote(BASS_TRACK, BASS_CHANNEL, note - 12, time, 2, volume)

# atmosphere
print("Generating atmosphere")
myMIDI.addProgramChange(ATMOS_TRACK, ATMOS_CHANNEL, 0, ATMOS_INSTR)
myMIDI.addNote(ATMOS_TRACK, ATMOS_CHANNEL, key, 0, END, volume)

# melody
print("Generating melody")
myMIDI.addProgramChange(MELODY_TRACK, MELODY_CHANNEL, 0, MELODY_INSTR)
for i in count():
    if MELODY_START + i*2 >= END: break
    for note, t, duration in melody:
        time = MELODY_START + i*2 + t
        myMIDI.addNote(MELODY_TRACK, MELODY_CHANNEL, note, time, duration, volume)

# aaaaa
print("Generating aaaaa")
myMIDI.addProgramChange(AAAAA_TRACK, AAAAA_CHANNEL, 0, AAAAA_INSTR)
myMIDI.addNote(AAAAA_TRACK, AAAAA_CHANNEL, key - 7, AAAAA_START, END, volume)


with open("thing.mid", "wb") as output_file:
    myMIDI.writeFile(output_file)