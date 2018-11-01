import os

# cmd = "cd /home/pi/Desktop/IDEX/voices; espeak -s 150 -ven+{0} \"The quick brown fox jumps over the lazy dog.\" --stdout | ffmpeg -i - -ar 44100 -ac 2 -ab 192k -f mp3 {0}.mp3"
cmd = "cd /home/pi/Desktop/IDEX/voices; cvlc --play-and-exit {0}.mp3"

for gen in ("m", "f"):
    for i in range(1, 6):
        os.system(cmd.format(gen + str(i)))
