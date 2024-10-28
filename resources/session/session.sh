#!/usr/bin/env bash
# Jarvis - UserBot

clear
echo -e "\e[1m"
echo "       _                  _     "
echo "      | |                (_)    "
echo "      | | __ _ _ ____   ___ ___ "
echo "  _   | |/ _` | '__\ \ / / / __|"
echo " | |__| | (_| | |   \ V /| \__ \"
echo "  \____/ \__,_|_|    \_/ |_|___/"
echo -e "\e[0m"
sec=5
spinner=(⣻ ⢿ ⡿ ⣟ ⣯ ⣷)
while [ $sec -gt 0 ]; do
    echo -ne "\e[33m ${spinner[sec]} Starting dependency installation in $sec seconds...\r"
    sleep 1
    sec=$(($sec - 1))
done
echo -e "\e[1;32mInstalling Dependencies ---------------------------\e[0m\n" # Don't Remove Dashes / Fix it
apt-get update
apt-get upgrade -y
pkg upgrade -y
pkg install python wget -y
wget https://raw.githubusercontent.com/btworeo/jarvis/main/resources/session/ssgen.py
pip uninstall telethon -y && install telethon
clear
python3 ssgen.py
