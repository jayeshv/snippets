#!/usr/bin/zsh

# My Sway startup script
swaymsg workspace 2
alacritty --title="   emacsclient" -e emacsclient -t &
sleep 0.2

swaymsg workspace 3
alacritty &
sleep 0.1

swaymsg workspace 9
alacritty --title="   calendar" -e calcurse &
sleep 0.1

swaymsg workspace 4
firefox &
sleep 0.5

swaymsg workspace 1
google-chrome &
