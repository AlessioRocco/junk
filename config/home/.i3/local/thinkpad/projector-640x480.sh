#!/bin/sh

xrandr --output LVDS1 --mode 1366x768 --primary --output HDMI2 --off --output HDMI3 --off --output VGA1 --off
xrandr --output LVDS1 --mode 1366x768 --primary --output HDMI2 --off --output HDMI3 --off --output VGA1 --mode 640x480 --right-of LVDS1
feh --bg-fill ~/desktop.jpg
xcalib -c
