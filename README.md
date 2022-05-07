# VGM_MUSIC
### An attempt at writing a music composition tool for the YM2151 in python

Hello!  As you look through this, please keep in mind that it was one of, if not the, first code I wrote that wasn't a one-file shell or python script.

## What is this?

In early 2019, a friend was writing a game engine for the [Commander X16](https://www.commanderx16.com/forum/index.php?/home/).  He was developing a small game alongside it as part of the engine development and asked me if I wanted to compose music and sound effects for it.  I said "yes", but there was one catch: at the time, the Commander X16 used only the [YM2151](https://en.wikipedia.org/wiki/Yamaha_YM2151) and I had never programmed for a microcontroller before.  Still, it seemed fun so I hopped in and began writing this code.  Development stopped in mid-late 2019.

## What does it do?

It has several utilities:
* `sequencer.py`contains the following classes:
    * *Step* (represents one subdivision of a measure)
    * *Pattern* (a virtually unlimited length sequence of steps)
    * *Sequence* (a virtually unlimited length sequence of patterns)
* `instrument.py` contains the following class:
    * *Instrument* (instrument definitions for the [YM2151](https://en.wikipedia.org/wiki/Yamaha_YM2151))
* `convert_mid.py` is used to convert midi files generated by midi-ox into commands for the YM2151
* `convert_dmp.py` is used to convert .dmp instruments to .spi
* `convert_opm.py` is used to convert .opm instruments to .spi

## Glossary

**sp**: file extension for binary files to be fed to YM2151
    * Stands for "Star Path", an old music alias of mine
        * Yes, yes, it's not a useful name\
    * none of this code directly deals with .sp files, see [x16-music-player](https://github.com/jjbliss/x16-music-player) instead
**spt**: file extenstion for "SP Textfile"
    * Is output from 
    * Each line *must* have:
        * An integer representing the YM2151 command followed by a comma
        * An integer representing the value for the command
    * Each line *can* have:
        * A comment, delimited by a semicolon after any commands or data
**spi**: file extenstion for "SP Instrument"
    * An instrument is really just a series of commands send to the YM2151 which configures its operators and modulators.
    * Each line *must* have:
        * An integer representing the YM2151 command followed by a comma
        * An integer representing the value for the command
    * Each line *can* have:
        * A comment, delimited by a semicolon after any commands or data

## Data examples

#### spt file with comments

``` 

```

#### midi file from midi-ox 

```
schema: timestamp, on/off, channel, note, velocity

0 On   ch=1 n=48 v=91
0 On   ch=11 n=41 v=123
0 On   ch=12 n=48 v=101
0 On   ch=13 n=81 v=125
1 On   ch=14 n=57 v=97
14 Off  ch=12 n=48 v=101
15 Off  ch=14 n=57 v=97
28 Off  ch=1 n=48 v=91
30 On   ch=12 n=52 v=110
30 On   ch=14 n=60 v=31
```

## References and Resources

* YM2151 original manual: http://map.grauw.nl/resources/sound/yamaha_ym2151_synthesis.pdf
* YM2151 Registers: https://w.atwiki.jp/mxdrv/pages/24.html
* Commander X16 programmer's guide: https://github.com/commanderx16/x16-docs/blob/master/Commander%20X16%20Programmer's%20Reference%20Guide.md
* VGM file format: http://www.smspower.org/Music/VGMFileFormat 


### External tools

* Music player for Commander X16: https://github.com/jjbliss/x16-music-player
    * has utilities
* Commander X16 emulator in a browser: https://x16.io
* Commander X16 emulator binaries: https://www.commanderx16.com/forum/files/
* Commander X16 on github: https://github.com/commanderx16


2.93 KB
[9:29 PM] Phalset: the script convert.sh contains the command to run the python script that will convert the text file music.spt to MUSIC.SP
[9:30 PM] Phalset: and to run this in the emulator you need run the command 
/location/of/emulator/x16emu -prg PLAYER.PRG -run
[9:31 PM] sunbunbird: 👍
[9:31 PM] sunbunbird: what's the "t" in spt stand for? text?
9:33 PM] sunbunbird: okay, so if i can generate a text file in the spt format, your script can convert it to binary for use with the game?


python3 spconvert.py -i music.spt -o MUSIC.SP -mode dec
that will read music.spt and expect decimal values


[10:17 PM] Phalset: could you send me an example of a file that you're converting from?
[10:17 PM] sunbunbird: sure
[10:18 PM] sunbunbird:
0 On   ch=1 n=48 v=91
0 On   ch=11 n=41 v=123
0 On   ch=12 n=48 v=101
0 On   ch=13 n=81 v=125
1 On   ch=14 n=57 v=97
14 Off  ch=12 n=48 v=101
15 Off  ch=14 n=57 v=97
28 Off  ch=1 n=48 v=91
30 On   ch=12 n=52 v=110
30 On   ch=14 n=60 v=31
[10:18 PM] Phalset: So is the number on the left a frame number?
[10:19 PM] sunbunbird: more or less, it's ms in hex which gets converted to a frame number
[10:21 PM] Phalset: I'd say keep track of the previous frame number, and then when it is different, you make a new Frame object and write the difference in frame numbers to the Frame object as the delay.
