## convert.py
# converts midi data to binary format for use with ym2151 soundchip
# written to make music composition easier for Commander X16 project
#
# NOTES
# each ym2151 instrument is tied to a midi channel, so having, say,
# all of your drums on midi channel 4 will not work here since that's
# 4 voices on a single, monophonic channel on the ym215.
#
# make sure you are controlling volume on your midi instruments with
# velocity rather than volume knobs on the devices themselves since
# this script uses velocity to set volume
#
# TODO
# CC = effects such as arpeggiator, vibrato, etc.
# pitch bend?
# find out where to set volume on the chip
#
# RESOURCES
# registers: https://w.atwiki.jp/mxdrv/pages/24.html
# commander x16 emulator: https://x16.io
# ym2151 manual: http://map.grauw.nl/resources/sound/yamaha_ym2151_synthesis.pdf
# vgm file format: http://www.smspower.org/Music/VGMFileFormat 

import re
import itertools
import sys

if len(sys.argv) < 2 or len(sys.argv) > 2:
    print("takes one argument, the name of the text file to convert")
    exit(1)

midi_file = open(sys.argv[1])

# keyed on midi channel
instruments = {
        "0" : 0,
        "1" : 1,
        "2" : 2,
        "3" : 3,
        "11": 4,
        "12": 5,
        "13": 6,
        "14": 7,
        "10": 0,
        "4" : 4,
        "5" : 5,
        "6" : 6,
        "7" : 7
        }


midi = {}
count = 0
frame = 0
commands = 0
old_frame = 0 
scratch_pad = []
actual_pad = []
scratch_pad = []
num_commands = 0
on = 1
off = "off"
# 60 frames, so 16.6667 ms per frame
#interval = 66.66666666 
#interval = 33.333333 
interval = 16.666666666666667
#interval = 8.3333333
# populate our ordered midi dict
## using a dict because files can only be read once 

#instrument_init = """32 ; 32 commands to initalize all 8 instruments
#32, 215 ; # chan 0, enable, FL, CON
#96, 7   ; write $07 to reg $60
#128,24  ; write $18 to reg $80
#224,5   ; write $05 to reg $E0
#33, 215 ; # chan 1, enable, FL, CON
#97, 7
#129,24
#225,5
#34, 215 ; # chan 2, enable, FL, CON
#98, 7
#130,24
#226,5
#35, 215 ; # chan 3, enable, FL, CON
#99, 7
#131,24
#227,5
#36, 215 ; # chan 4, enable, FL, CON
#100,    7   ; write $07 to reg $60
#132,24  ; write $18 to reg $80
#226,5   ; write $05 to reg $E0
#37, 215 ; # chan 5, enable, FL, CON
#101,    7
#133,24
#229,5
#38, 215 ; # chan 6, enable, FL, CON
#102,    7
#134,24
#230,5
#39, 215 ; # chan 7, enable, FL, CON
#103,    7
#135,24
#231,5
#10"""
#actual_pad.append(instrument_init)
#####
# Changin this: Off 0 0 0
# To this:
# <COM> <NUMBER OF COMMANDS TO RUN>
# <REG> Off
# <REG> <DATA>
# <REG> 0
# <REG> 0
# <REG> <CC>
# <SKIP> <NUMBER OF FRAMES TO SKIP

for row in midi_file:
    #print(row)
    row = row.rstrip()
    row = re.sub(' +', ' ', row)
    row_split = row.split(" ")
    #print(row_split)


    timestamp = 0
    cmd = ""
    ins = 0
    pitch = 0
    cc = 0
    vol = 0
    skip = 0
    reg =  {
            # KON
            "on"  : "8",
            "off" : "8",
            
            # KC
            "note_chan_0" : "40", 
            "note_chan_1" : "41",
            "note_chan_2" : "42", 
            "note_chan_3" : "43", 
            "note_chan_4" : "44", 
            "note_chan_5" : "45", 
            "note_chan_6" : "46", 
            "note_chan_7" : "47" 
        
            }

    for i in range(0, len(row_split)):
        # frame
        if i == 0:
            timestamp = float(row_split[i])
            #print(f"timestamp: {timestamp}")
            #frame = round(int(timestamp, 16) / interval)
            frame = round(timestamp / interval)
            print(f"frame: {frame}")
        if i == 1:
            command = row_split[i]
            cmd = command.lower()
            #print(f"cmd: {cmd}")
        # instrument
        if i == 2:
            chan = row_split[i].split("=")[1]
            ins = instruments[chan]
        # note/cc
        if i == 3:
            if "n" in row_split[i]:
              pitch = int(row_split[i].split("=")[1])
            elif "c" in row_split[i]:
              cc = row_split[i].split("=")[1]
        # volume
        if i == 4:
            vel = row_split[i].split("=")[1]
            vol = int(vel)
    
    # store our data
    if cmd == "off":
        # note off
        scratch_pad.append(f"{reg['off']}, {ins}; Off {ins} (midi {chan})") 
        off = "off"
        #continue
    if cmd == "on":
        key = f"note_chan_{ins}"
        # octave and note data
        #if off == "off":
        scratch_pad.append(f"{reg[key]}, {pitch}; note {ins} (midi {chan})")
        scratch_pad.append(f"{reg['on']}, {120 + ins}; On {ins} (midi {chan})")
        off = "on"
    if cmd == "par":
        print("yay")

    #print(f"Frame: {frame}")
    #print(f"Old_frame: {old_frame}")

    if frame != old_frame:
        diff = frame - old_frame
        print(f"diff: {diff}")
        commands = len(scratch_pad)
        #if diff != 1:
        actual_pad.append(f"{str(commands)} ; {commands} commands")
        actual_pad.append(scratch_pad)
        actual_pad.append(f"{str(diff)} ; skip {diff} frames") 
        commands = 0
        scratch_pad = []

    old_frame = frame

#print(scratch_pad)
#actual_pad = list(itertools.chain(actual_pad))
flat_list = []
for item in actual_pad:
    if isinstance(item, list):
        for item2 in item:
            flat_list.append(item2)
    else:
        flat_list.append(item)
flat_list.append("00")

#print(flat_list)
#print(flat_list)
#print(len(flat_list))
#print(actual_pad)
#flat_commands = list(itertools.chain(scratch_pad))
#flat_commands.append("00")
#print(flat_commands)
flat_string = "\n".join(flat_list)
file = open(sys.argv[1].split('.')[0] + '.spt', 'w')
#bytes_file = open('test.sp', 'w')
print(flat_string)
file.write(flat_string)
file.close()
#print(string_commands)
#print(flat_string)
#print(commands)
