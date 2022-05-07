shepards = open('shepards.txt', 'w')
shepards.write("")
shepards.close()

shepards = open('shepards.txt', 'a+')
unit = 1000
time_scale = 5
cmd = "on"

new = False

def tones(chan, cmd):
    for i in range(0, 128):
        if cmd == "on":
            shepards.write(f"{int((i * unit) / time_scale)} On ch={chan} n={i}\n")
            cmd = "off"
        elif cmd == "off":
            shepards.write(f"{int((i * unit) / time_scale)} Off ch={chan}\n")
            cmd = "on"
tones(11, cmd)

shepards.close()
