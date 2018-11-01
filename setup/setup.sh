#!/bin/bash

sudo apt-get update
sudo apt-get install -y pi-bluetooth blueman python-picamera python3-picamera tesseract-ocr espeak pulseaudio pavucontrol pulseaudio-module-bluetooth -y
sudo apt-get install xserver-xorg-video-fbdev cmake ffmpeg calibre -y
sudo apt-get install libjpeg zlib libpng libboost libxrender imagemagick python-opencv -y
yes | sudo pip3 install tensorflow imutils keras h5py numpy

cd ~
cd Desktop
git clone https://github.com/tasanakorn/rpi-fbcp
cd rpi-fbcp/
mkdir build
cd build/
cmake ..
make
sudo install fbcp /usr/local/bin/fbcp

cd ~
cd Desktop
mkdir scantailor
cd scantailor
git clone https://github.com/scantailor/scantailor.git
mkdir build
cd build
cmake ..
sudo make install