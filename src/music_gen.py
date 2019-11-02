import random

SECOND = 2
MIN_THIRD = 3
MAJ_THIRD = 4
FOURTH = 5
FIFTH = 7
SIXTH = 9

def gen_key():
    return random.randint(55, 76)

def gen_chords(key):
    # iv I I V
    chords = random.choice([
        [
            [key + SIXTH, key + SIXTH + MIN_THIRD, key + SIXTH + FIFTH - 12],
            [key, key + MAJ_THIRD, key + FIFTH],
            [key, key + MAJ_THIRD, key + FIFTH],
            [key + FIFTH, key + FIFTH + MAJ_THIRD, key + FIFTH + FIFTH - 12]
        ],
        [
            [key + FOURTH, key + FOURTH + MAJ_THIRD, key + FOURTH + FIFTH - 12],
            [key, key + MAJ_THIRD, key + FIFTH],
            [key + SIXTH, key + SIXTH + MIN_THIRD, key + SIXTH + FIFTH - 12],
            [key + FIFTH, key + FIFTH + MAJ_THIRD, key + FIFTH + FIFTH - 12]
        ]
    ])
    print(chords)
    for chord in chords:
        for i in range(len(chord)):
            if random.random() < 0.5:
                chord[i] -= 12
    random.shuffle(chords)
    print(chords)
    return chords

def gen_bass(key, chords):
    bass = [random.choice(chord) for chord in chords]
    for i in range(len(bass)):
        if random.random() < 0.5:
            bass[i] -= 24
        else:
            bass[i] -= 12
    return bass

def gen_melody(key):
    return random.choice([
        [
            (key + SECOND, 0, 4/8),
            (key + MAJ_THIRD, 4/8, 2/8),
            (key + FIFTH, 6/8, 4/8),
            (key + MAJ_THIRD, 10/8, 2/8),
            (key + SECOND, 12/8, 1/8),
            (key + MAJ_THIRD, 13/8, 1/8),
            (key + SECOND, 14/8, 4/8)
        ],
        [
            (key, 0, 1/2),
            (key, 1/2, 2/2),
            (key, 2/2, 3/2),
            (key, 3/2, 4/2),
        ],
        [
            (key, 0, 1/2),
            (key + SECOND, 1/2, 2/2),
            (key, 2/2, 3/2),
            (key + SECOND, 3/2, 4/2),
        ],
        [
            (key, 0, 1/2),
            (key - 1, 1/2, 2/2),
            (key, 2/2, 3/2),
            (key - 1, 3/2, 4/2),
        ],
        [
            (key + 12 + FOURTH, 0, 1/2),
            (key + 12 + MAJ_THIRD, 1/2, 2/2),
            (key + 12 + SECOND, 2/2, 3/2),
            (key + 12, 3/2, 4/2),
        ]
    ])
