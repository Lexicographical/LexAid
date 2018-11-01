#!/bin/bash

ocr() {
	tesseract "/home/pi/Desktop/IDEX/tmp/raw.jpg" "/home/pi/Desktop/IDEX/tmp/output"
	value=`cat /home/pi/Desktop/IDEX/tmp/last.txt`
	text=`cat /home/pi/Desktop/IDEX/tmp/output.txt`
	mkdir -p "/home/pi/Desktop/IDEX/output"
	mkdir -p "/home/pi/Desktop/IDEX/output/pictures"
	mkdir -p "/home/pi/Desktop/IDEX/output/text"
	cp "/home/pi/Desktop/IDEX/tmp/img.jpg" "/home/pi/Desktop/IDEX/output/pictures/img_$value.jpg"
	cp "/home/pi/Desktop/IDEX/tmp/output.txt" "/home/pi/Desktop/IDEX/output/text/output_$value.txt"
	echo "$((value + 1))" > "/home/pi/Desktop/IDEX/tmp/last.txt"
}

tts() {
	rm "/home/pi/Desktop/IDEX/tmp/audio.mp3"
	espeak -s 150 -ven+f3 -f "$1" --stdout | ffmpeg -i - -ar 44100 -ac 2 -ab 192k -f mp3 "/home/pi/Desktop/IDEX/tmp/audio.mp3"; cvlc --play-and-exit "/home/pi/Desktop/IDEX/tmp/audio.mp3"
}

convert() {
	ebook-convert "$1" "$2"
}

ttsdirect() {
	espeak "$1" -s 150 -ven+f3 --stdout | ffmpeg -i - -ar 44100 -ac 2 -ab 192k -f mp3 "/home/pi/Desktop/IDEX/tmp/audio.mp3"; cvlc --play-and-exit "/home/pi/Desktop/IDEX/tmp/audio.mp3"
}

if [ "$1" == "ocr" ]
then
	ocr
elif [ "$1" == "tts" ]
then
	tts "$2"
elif [ "$1" == "convert" ]
then
	convert "$2" "$3"
elif [ "$1" == "ttsdirect" ]
then
	ttsdirect "$2"
else
	echo "Invalid parameter"
fi