## converts OPM files to sp instruments
import sys
import re
from lib import instrument 

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("takes two arguments, the name of the dmp file to convert and the channel you want it on")
    exit(1)

spi = open(sys.argv[1].split('.')[0] + '.spi', 'w')
channel = sys.argv[2]

ints = []

with open(sys.argv[1], "rb") as dmp:
    byte = dmp.read(1)

    while byte:
        #print(byte)
        ints.append(int.from_bytes(byte, byteorder='big'))
        byte = dmp.read(1)

print(ints)

dmp = instrument.Instrument(channel)

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

dmp.set_CHANNEL_LFO(lfo, chan)
dmp.set_M1(m1)
dmp.set_C1(c1)
dmp.set_M2(m2)
dmp.set_C2(c2)

spi.write(dmp.convert_to_spt())
print(dmp.convert_to_spt(), end = '')

#    print(f"CHANNEL_LFO {instruments[channel]['ins'].get_CHANNEL_LFO()}")
#    print(f"M1 {instruments[channel]['ins'].get_M1()}") 
#    print(f"C1 {instruments[channel]['ins'].get_C1()}")
#    print(f"M2 {instruments[channel]['ins'].get_M2()}")
#    print(f"C2 {instruments[channel]['ins'].get_C2()}")
#
##print(instruments)
#
##for instrument in dict_of_ins.values():
##    #print(instrument)
##    instrument = instrument.get_all()
##    spt.write('\n'.join(instrument))
##    #print('\n'.join(instrument))
###print(chunks)
###print(list_of_ins)
spi.close()
