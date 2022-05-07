## converts OPM files to sp instruments
import sys
import re
import os
from lib import instrument 
from lib import tools

if len(sys.argv) < 2 or len(sys.argv) > 2:
    print("takes one argument, the name of the opm file to convert")
    exit(1)

opm = open(sys.argv[1], 'r')
path = sys.argv[1].split('.')[0].split("/")[-2]
name = sys.argv[1].split('.')[0].split("/")[-1] 
print(path)
os.mkdir(path)
#opm = open('test.opm', 'r')
#spt = open('output.spt', 'w')

data = []
instruments = {}
chunks = {}

for line in opm:

    line = line.rstrip()

    if "//" in line:
        next
    elif line == '':
        next
    elif "#" in line:
        next
    elif "@" in line:
#        print("channel")
        chan = line.split(":")[1].split(" ")[0]
        instruments[chan] = {}
        instruments[chan]["data"] = []
#        print(chan)
    else:
#        print("data")
        line = re.sub(' +', ' ', line)
#        print(line)
        instruments[chan]["data"].append(line.split(' ')[1:])

for channel in instruments.keys():
    data = instruments[channel]["data"]

    instruments[channel]["ins"] = instrument.Instrument(channel)
    
    instruments[channel]["ins"].set_CHANNEL_LFO(data[0], data[1])
    instruments[channel]["ins"].set_M1(data[2])
    instruments[channel]["ins"].set_C1(data[3])
    instruments[channel]["ins"].set_M2(data[4])
    instruments[channel]["ins"].set_C2(data[5])


    spi = open(f"{path}/{name}.{channel}.spi", 'w')
    spi.write(instruments[channel]["ins"].to_spi())
    spi.close()

#    print(f"CHANNEL_LFO {instruments[channel]['ins'].get_CHANNEL_LFO()}")
#    print(f"M1 {instruments[channel]['ins'].get_M1()}") 
#    print(f"C1 {instruments[channel]['ins'].get_C1()}")
#    print(f"M2 {instruments[channel]['ins'].get_M2()}")
#    print(f"C2 {instruments[channel]['ins'].get_C2()}")
#
#print(instruments)

#for instrument in dict_of_ins.values():
#    #print(instrument)
#    instrument = instrument.get_all()
#    spt.write('\n'.join(instrument))
#    #print('\n'.join(instrument))
##print(chunks)
##print(list_of_ins)
opm.close()
spi.close()
