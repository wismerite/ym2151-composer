from lib import sequencer as seq
from lib import tools as t

def four_to_the_floor():
    # returns a pattern object
    steps = []

    length = 64

    # bass on the upbeats
    for i in range(0, length, 2):
        if i >= 0 and i < 16:
            steps.append(seq.Step(i, "e", 30, 2))
        elif i >= 16 and i < 32:
            steps.append(seq.Step(i, "e", 37, 2))
        elif i >= 32 and i < 48:
            steps.append(seq.Step(i, "e", 39, 2))
        elif i >= 48 and i < 64:
            steps.append(seq.Step(i, "e", 30, 2))

    for step in t.loop_it(kick_snare(), 64):
        steps.append(step)

    for step in t.loop_it(hat(), length):
        steps.append(step)

    mypat = seq.Pattern(steps, length,  "s")

    return mypat

def kick_snare():
    steps = []

    length = 16

    ## kick on the downbeat
    for i in range(0, length, 4):
        steps.append(seq.Step(i, "s", 36, 0))

    ## snare on 2 and 4
    for i in range(4, length, 8):
        steps.append(seq.Step(i, "s", 65, 1))

    mypat = seq.Pattern(steps, length,  "s")

    return mypat

def hat():
    steps = []
    length = 16
    
    for i in range(0, length):
        steps.append(seq.Step(i, "s", 80, 3))

    mypat = seq.Pattern(steps, length, "s")

    return mypat

#print(t.loop_it(kick_snare(), 64))

patterns = {}

patterns[1] = four_to_the_floor()

myseq = seq.Sequencer(patterns, 180, "4/4") 
myseq.generate_sequence()
myseq.convert_to_spt("instruments", "output_file")

#myseq.convert_to_txt("test.txt")
