from lib import tools
import json

class Instrument:
    def __init__(self, chan):

        chan = int(chan)

        self.CHANNEL_LFO = {
                                # LFRQ 
                                int('0x18', 16)        : 0,
                                # AMD / PMD
                                int('0x19', 16)        : 0,
                                # WF
                                int('0x1B', 16)        : 0,
                                # NFRQ / NE
                                int('0x0F', 16)        : 0,
                                # PAN / FL / CON
                                int('0x20', 16) + chan : 215,
                                # AMS / PMS
                                int('0x38', 16) + chan : 0
                            }

        self.M1 =           {
                                ## M1 
                                # AR / KS
                                int('0x80', 16) + chan : 24,
                                # D1R / AMS-EN
                                int('0xA0', 16) + chan : 0,
                                # D2R / DT2
                                int('0xC0', 16) + chan : 0,
                                # RR
                                int('0xE0', 16) + chan : 5,
                                # TL
                                int('0x60', 16) + chan : 7,
                                # MUL / DT1
                                int('0x40', 16) + chan : 0
                            }    

        self.C1 =          {
                            
                                ## C1
                                # AR / KS
                                int('0x88', 16) + chan : 0,
                                # D1R / AMS-EN
                                int('0xA8', 16) + chan : 0,
                                # D2R / DT2
                                int('0xC8', 16) + chan : 0,
                                # RR
                                int('0xE8', 16) + chan : 0,
                                # TL
                                int('0x68', 16) + chan : 0,
                                # MUL / DT1
                                int('0x48', 16) + chan : 0
                            }

        self.M2 =          {
                                ## M2
                                # AR / KS
                                int('0x90', 16) + chan : 0,
                                # D1R / AMS-EN
                                int('0xB0', 16) + chan : 0,
                                # D2R / DT2
                                int('0xD0', 16) + chan : 0,
                                # RR
                                int('0xF0', 16) + chan : 0,
                                # TL
                                int('0x70', 16) + chan : 0,
                                # MUL / DT1
                                int('0x50', 16) + chan : 0
                            }

        self.C2 =          {
                                ## C2
                                # AR / KS
                                int('0x98', 16) + chan : 0,
                                # D1R / AMS-EN
                                int('0xB8', 16) + chan : 0,
                                # D2R / DT2
                                int('0xD8', 16) + chan : 0,
                                # RR
                                int('0xF8', 16) + chan : 0,
                                # TL
                                int('0x78', 16) + chan : 0,
                                # MUL / DT1
                                int('0x58', 16) + chan : 0
                                
                            }    
            
    ## private functions
    def __format_cl(self, row):
        # formats channel_lfo

        data = []

        # massage the data
        # LFRQ
        data.append(row[0])
        # AMD / PMD
        #data.append([row[1], (int(row[2]) + (1 << 7))])
        data.append([row[1], (int(row[2]) + (1 << 7))])
        # WF
        data.append(row[3])
        # NFRQ / NE 
        data.append(int(row[4]) + self.__shift_it(row[11], 7))
        # PAN / FL / CON
        # set PAN hard 11
        data.append((1 << 7) + (1 << 6) + self.__shift_it(row[6], 3) + int(row[7]))
        # AMS / PMS
        data.append([int(row[8]), self.__shift_it(row[9], 4)])

        return data

    def __format_mc(self, row):

        data = []

        # AR / KS
        data.append(int(row[0]) + self.__shift_it(row[6], 6))
        # D1R / AME
        data.append(int(row[1]) + self.__shift_it(row[10], 7))
        # D2R / DT2
        data.append(int(row[2]) + self.__shift_it(row[9], 6))
        # RR / D1L
        data.append(int(row[3]) + self.__shift_it(row[4], 4))
        # TL
        data.append(row[5])
        # MUL / DT1
        data.append(int(row[7]) + self.__shift_it(row[8], 4))

        return data


    def __shift_it(self, num, bits):
        return int(int(num) << bits)

    # setters
    def set_CHANNEL_LFO(self, lfo, channel):
        
        row = []
        row.append(lfo)
        row.append(channel)
        row = tools.flatten(row)

        data = self.__format_cl(row) 
        registers = self.CHANNEL_LFO.keys()
        
        self.CHANNEL_LFO = dict(zip(registers, data))
    
        #print(f"{self.CHANNEL_LFO}")

        return 0

    def set_M1(self, row):
        data = self.__format_mc(row)
        registers = self.M1.keys()

        self.M1 = dict(zip(registers, data))

        #print(f"{self.M1}")

        return 0
    
    def set_C1(self, row):
        data = self.__format_mc(row)
        registers = self.C1.keys()

        self.C1 = dict(zip(registers, data))

        #print(f"{self.C1}")

        return 0

    def set_M2(self, row):
        data = self.__format_mc(row)
        registers = self.M2.keys()

        self.M2 = dict(zip(registers, data))

        #print(f"{self.M2}")

        return 0 

    def set_C2(self, row):
        data = self.__format_mc(row)
        registers = self.C2.keys()

        self.C2 = dict(zip(registers, data))

        #print(f"{self.C2}")

        return 0

    ## getters
    def get_CHANNEL_LFO(self):
        return self.CHANNEL_LFO
    
    def get_M1(self):
        return self.M1

    def get_C1(self):
        return self.C1

    def get_M2(self):
        return self.M2

    def get_C2(self):
        return self.C2

    ## other functions
    def convert_to_spt(self):
        # set number of commands to follow
        
        aggregate_data = {}

        aggregate_data.update(self.CHANNEL_LFO)
        aggregate_data.update(self.M1)
        aggregate_data.update(self.C1)
        aggregate_data.update(self.M2)
        aggregate_data.update(self.C2)

        num_lists = 0
        data = []

        for reg, value in aggregate_data.items():
            if isinstance(value, list):
                for i in range(0,len(value)):
                    data.append([reg, value[i]])
                num_lists += 1
            else:
                data.append([reg, value])

        strings = []

        # convert everything to string
        for item in data:
            for i in range(0, len(item)):
                item[i] = str(item[i])
            
            strings.append(",".join(item))
            
        # num commands
        strings.insert(0, str(len(aggregate_data) + num_lists))
        # skip a frame to avoid max of 127 commands per frame
        strings.append('1')

        joined = "\n".join(strings)
        joined += "\n" 
        return joined
     #   joined = [str(len(self.instrument))]

     #   registers = list(self.instrument.keys())
     #   data = list(self.instrument.values())
     #   
     #   mapped = zip(registers, data)

     #   for pair in mapped:
     #       pair = list(pair)
     #       pair[1] = str(pair[1])
     #       pair[0] = str(pair[0])
     #       joined.append(','.join(pair))
     #   
     #   joined.append('1\n')
     #   return joined
