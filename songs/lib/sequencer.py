# sequencer
from lib import tools as t

class Sequencer:
    def __init__(self, patterns, bpm, signature):

        # dict of pattern objects, can be unordered
        self.patterns = patterns
        
        # float
        self.bpm = bpm

        # int
        self.sequence_length = len(patterns)

        self.beats_in_bar = int(signature.split("/")[0])
        self.beat = int(signature.split("/")[1])

        # float
        # use 60 here cause 60 fps
        fps = 60
        # use 1000 here cause we want seconds per frame
        self.ms_per_frame = 1000  / fps
        # use 60 here cause beats per minute >> beats per second
        # use 16.6666667 because that's the number of ms per frame
        self.ms_per_beat = (fps / (self.bpm / 60)) * 16.66666666667
        self.ms_per_bar = self.ms_per_beat * self.beats_in_bar

        self.steps_timestamped = []

        self.note_lengths = {}
        self.note_lengths["w"] = self.ms_per_beat * self.beat
        self.note_lengths["h"] = self.ms_per_beat * (self.beat / 2)
        self.note_lengths["q"] = self.ms_per_beat * (self.beat / 4 )
        self.note_lengths["e"] = self.ms_per_beat * (self.beat / 8 )
        self.note_lengths["s"] = self.ms_per_beat * (self.beat / 16 )
        self.note_lengths["t"] = self.ms_per_beat * (self.beat / 32 )

        self.note_divisions = {}
        # sixteenth notes
        self.note_divisions["s"] = self.ms_per_beat / 4
        # thirty-second notes
        self.note_divisions["t"] = self.ms_per_beat / 8

    def get_sequence(self):
        return self.steps_timestamped

    def generate_sequence(self):
        clock = 0

        # use "sorted" here to ensure the patterns are in order
        for key in sorted(self.patterns.keys()):
            # for each pattern, in order
            # get a sorted list of steps
            # apply timestamps to those steps in intervals of self.clock_beat

            pattern = self.patterns[key].to_d()

            num_steps = pattern["header"]["length"]
            division  = pattern["header"]["division"]
            steps     = pattern["steps"]

            ms_per_step = self.note_divisions[division]

            steps_dicts = []

            for step in steps:
                steps_dicts.append(step.to_d())

            for step in steps_dicts:
                timestamp = (ms_per_step * int(step["position"])) + clock
              
                step["timestamp"] = timestamp
                self.steps_timestamped.append(step)

                if step["cmd"] == "on":

                    off = {
                                "cmd": "off",
                                "timestamp": self.note_lengths[step["note_length"]] + timestamp,
                                "channel": step["channel"]

                          }

                    self.steps_timestamped.append(off)

            clock += ((num_steps) * ms_per_step)

        #return self.steps_timestamped


    def convert_to_txt(self, output_file):
        output = open(output_file, 'a+')
        
        master_list = []

        for step in self.steps_timestamped:
            if step["cmd"] == "on":
                master_list.append(f"{step['timestamp']} {step['cmd']} ch={step['channel']} n={step['pitch']}\n")
            elif step["cmd"] == "off":
                master_list.append(f"{step['timestamp']} {step['cmd']} ch={step['channel']}\n")

        master_list.sort(key=t.split_string)

        #print(master_list)
   
        for step in master_list:
            output.write(step)

        output.close()
        return

    def convert_to_spt(self, instruments, output_file, print_to_screen=True):
        
        steps = self.steps_timestamped
        
        master_dict = {}
    
        for step in steps:
           #print(step) 
            # step is a dict
            timestamp = step['timestamp']
            if timestamp not in master_dict:
                master_dict[timestamp] = []
            if step["cmd"] == "on":
                print(step)
                master_dict[step['timestamp']].append([step['cmd'], step['channel']])
                master_dict[step['timestamp']].append([step['pitch'], step['channel']])
            elif step["cmd"] == "off":
                print(step)
                master_dict[step['timestamp']].append([step['cmd'], step['channel']])
    
        master_spt_list = []
        # registers for commands and channels in decimal
        reg = {
                # KON
                "on" : "8",
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
    
        for key in sorted(master_dict.keys()):
            timestamp = key
            steps = master_dict[key]
    
            for step in steps:
                # steps is a list of lists
                # step is a list
                # print(step)
                master_spt_list.append([timestamp, step])
    
        #print(master_spt_list)
        
        # tmp list for use later on
        tmp = []
        master = []
        # ms per frame
        interval = 16.666666667 
        old_frame = -1 

        for step in master_spt_list:
            print(f"step: {step}")
            timestamp = step[0]
            cmd = step[1][0]
            data = step[1][1]
    
            frame = round(timestamp / interval) 
    
            # store our data
            if cmd == "off":
                # note off
                tmp.append(f"{reg['off']}, {data}; Off {data}") 
                off = "off"
                #continue
            if cmd == "on":
                key = f"note_chan_{data}"
                # octave and note data
                #if off == "off":
                tmp.append(f"{reg[key]}, {data}; note {data})")
                tmp.append(f"{reg['on']}, {120 + data}; On {data})")
                off = "on"
            if cmd == "par":
                print("yay")
    
            #print(f"Frame: {frame}")
            #print(f"Old_frame: {old_frame}")
    
            if frame != old_frame:
                diff = frame - old_frame
                print(f"frame: {frame}")
                print(f"old_frame: {old_frame}")
                print(f"diff: {diff}")
                commands = len(tmp)
                #if diff != 1:
                master.append(f"{str(commands)} ; {commands} commands")
                master.append(tmp)
                master.append(f"{str(diff)} ; skip {diff} frames") 
                commands = 0
                tmp = []
    
            old_frame = frame
     
                
    
            #print(key)
            #print(master_dict[key]) 
# pattern
class Pattern:
    def __init__(self, steps, pattern_length, note_division):
        
        # a list of step objects
        self.steps = steps

        # an int describing how long the pattern is, starting with 1 
        self.pattern_length = pattern_length

        # one of the following strings
        # s(ixteenth)
        # t(hirty-second)
        self.note_division = note_division

    def to_d(self):
        mydict = {
                    
                    "header": {

                                    "length": self.pattern_length,
                                    "division": self.note_division
                              },

                    "steps": self.steps
                
                 }

        return mydict

    def get_length(self):
        return self.pattern_length

# step
class Step:
    def __init__(self, position, note_length, pitch, channel, cmd="on"):
        # position: an int describing which step of the pattern the note should fall on (starting with 0)
        self.position = position
        # note_length: one of the following letters
        # w(hole)
        # h(alf)
        # q(uarter)
        # e(ighth)
        # s(ixteenth)
        # t(hirty-second)
        self.note_length = note_length
        # pitch: an int between 0 and 127 (inclusive)
        self.pitch = pitch
        # channel: an int between 0 and 7 (inclusive)
        self.channel = channel
        self.cmd = cmd
        # if octave:
        #     self.octave = octave
        # else:
        #     self.octave = ""
        # self.pitch_shifted = (octave << 4) + pitch

    def to_s(self):
        joined = str(self.position) + " " + str(self.note_length) + " " + str(self.pitch) + " " + str(self.channel) + " " + str(self.cmd)
        return joined
    
    def to_l(self):
        mylist = [self.position, self.note_length, self.pitch, self.channel, self.cmd]
        return mylist

    def to_d(self):
        
        mydict = {
                    "position": self.position,
                    "note_length": self.note_length,
                    "pitch": self.pitch,
                    "channel": self.channel,
                    "cmd": self.cmd
                }

        return mydict

