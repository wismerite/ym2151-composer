import re
import itertools
from lib import sequencer as seq
from lib import instrument as i

def flatten(input_list):

    flat_list = []
    for item in input_list:
        if isinstance(item, list):
            for item2 in item:
                flat_list.append(item2)
        else:
            flat_list.append(item)

    return flat_list

def split_string(string):
    number = float(string.split(" ")[0])
    return int(number)

def loop_it(pattern, desired_length, remainder="trim"):
    # remainder possible values:
    # trim - use silence to fill the last few steps if they are not evenly divisible into your desired length
    # keep_start - fill all steps up to your desired length even if the pattern is not easily divided into it
    # keep_end - fill all steps up to your desired length even if the pattern is not easily divided into it
    # distribute - distributes the blank steps through the new pattern 
    #
    # example:
    #
    # pattern 15 steps log with desired length 64 = 4 remaining steps after pattern multiplication
    #
    # trim: 15 X 4 steps + 4 blank steps = 64 steps
    # keep_start: 15 x 4 steps + the first 4 steps of the pattern = 64 steps
    # keep_end: 15 x 4 steps + the last 4 steps of the the pattern = 64 steps
    # distribute: (15  steps + 1 blank step) x 4 = 64 steps

    pattern_dict = pattern.to_d()
    pattern_length = pattern_dict["header"]["length"]
    times_to_loop = desired_length // pattern_length
    extra_steps = desired_length % pattern_length

    #print(f"times to loop: {times_to_loop}")
  
    steps = pattern_dict['steps'] 

    looped_steps = []

    for step in steps:
        burp = step.to_d()
        old_position = burp["position"]
        for i in range(0, times_to_loop):
            new_position = old_position + ( pattern_length * i)
            looped_steps.append(copy_step(step, new_position))
  
    return looped_steps

    #pattern_dict["steps"] = looped_steps
    #pattern_dict["header"]["length"] = desired_length

    #mypat = pat_from_dict(pattern_dict)

    #return mypat 

def copy_step(step, new_position=0):
   
    step = step.to_d()
    
    new_step = seq.Step(new_position, step["note_length"], step["pitch"], step["channel"], step["cmd"])

    return new_step

def pat_from_dict(mydict):

    mypat = seq.Pattern(mydict["steps"], mydict["header"]["length"], mydict["header"]["division"])

    return mypat

    


def randomized(scale="chromatic", octave="4"):
    return

def chorder():
    return
## converts OPM files to sp instruments
def load_dmp(dmp_file, chan):

    ints = []
    dmp_ins = i.Instrument(chan)
    
    with open(dmp_file, "rb") as dmp:
        byte = dmp.read(1)
    
        while byte:
            #print(byte)
            ints.append(int.from_bytes(byte, byteorder='big'))
            byte = dmp.read(1)

        dmp.close()
    
    
    header = ints[0:3]
    chanlfo = ints[3:7]
    m1 = ints[7:18]
    c1 = ints[18:29]
    m2 = ints[29:40]
    c2 = ints[40:51]
    
    # all 0's cause apparently you can't set the lfo or noise generator in deflemask
    lfo = [0, 0, 0, 0, 0]
    chan = [64, chanlfo[1], chanlfo[2], chanlfo[3], chanlfo[0], 127, 0]
    #     AR     D1R    D2R    RR    D1L   TL     KS  MUL DT1 DT2 AMS-EN
    m1 = [m1[2], m1[3], m1[9], m1[5], m1[4], m1[1], 0, m1[0], 0, 0, m1[6]] 
    c1 = [c1[2], c1[3], c1[9], c1[5], c1[4], c1[1], 0, c1[0], 0, 0, c1[6]] 
    m2 = [m2[2], m2[3], m2[9], m2[5], m2[4], m2[1], 0, m2[0], 0, 0, m2[6]] 
    c2 = [c2[2], c2[3], c2[9], c2[5], c2[4], c2[1], 0, c2[0], 0, 0, c2[6]] 
    
    dmp_ins.set_CHANNEL_LFO(lfo, chan)
    dmp_ins.set_M1(m1)
    dmp_ins.set_C1(c1)
    dmp_ins.set_M2(m2)
    dmp_ins.set_C2(c2)
    
    return dmp_ins 


def load_opm(opm_file, chan_in_file, chan):

    opm = open(opm_file, 'r')
    
    data = []
    instruments = {}
    
    for line in opm:
    
        line = line.rstrip()
        line = re.sub(' +', ' ', line)

        if "//" in line:
            next
        elif line == '':
            next
        elif "#" in line:
            next
        elif "@" in line:
            channel = int(line.split(":")[1].split(" ")[0])
            instruments[channel] = {}
            instruments[channel]["data"] = []
        else:
            instruments[channel]["data"].append(line.split(' ')[1:])
    
    #print(instruments[chan_in_file])

    data = instruments[chan_in_file]["data"]
    
    instruments[chan_in_file]["ins"] = i.Instrument(chan)
    
    instruments[chan_in_file]["ins"].set_CHANNEL_LFO(data[0], data[1])
    instruments[chan_in_file]["ins"].set_M1(data[2])
    instruments[chan_in_file]["ins"].set_C1(data[3])
    instruments[chan_in_file]["ins"].set_M2(data[4])
    instruments[chan_in_file]["ins"].set_C2(data[5])

    return instruments[chan_in_file]["ins"]

def zip_it(steps, notes, note_lengths, channels):
    zipped = list(zip(steps, note_lengths, notes, channels))

    steps = []

    for i in range(0,len(zipped)):
        if zipped[i][0] == 1:
            steps.append(seq.Step(i, zipped[i][1], zipped[i][2], zipped[i][3], zipped[i][4]))

    print(steps)
    return steps