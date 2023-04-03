# LinuxGSM Discord Bot

## Description
This is a simple Discord bot that allows you to control your LinuxGSM Servers via Discord. I originally made this to learn Python and for my community in order for them to manage our Gameservers without having to give them access to my server.

This is in a working state but I am looking to expand upon it in the future.

## Features

Currently its able to start, stop, restart and update LinuxGSM Servers that are configured in a JSON file.

## Installation / Usage

### Dependencies

- Python3
- Pycord
- NodeJS
- Pm2

### Installation

1. Create a Bot and get the Token: [Guide](https://guide.pycord.dev/getting-started/creating-your-first-bot)
2. Create a Directory for the Bot on your Server ```mkdir LinuxGSM-Discord```
3. Install git using ```sudo apt-get install git```
4. Clone the Repository to your desired directory using ```git clone https://github.com/osnium/LinuxGSM-Discord-Bot.git``` inside it [^1]
5. Install NodeJS and NPM using ```sudo apt install nodejs``` & ```sudo apt install npm```
6. Install Pm2 using ```npm install pm2 -g```
7. Edit the ```gameservers.json``` and add your server names, Paths and file names
8. Put your Bot Token inside ```bot.run("token")``` at the bottom of the main.py

### Usage

- Start your Bot using ```pm2 start main.py ---name=BotName ---interpreter=python3``` inside the main.py directory
- Now you can start / stop / restart the bot using ```pm 2 <command> BotName```
- Refrain from messing with the servers outside of Discord to not have the bot mix up things
- Feel free to change bot commands permission using Discords inbuild integration feature

## Todo

- [ ] Add easier way to add / remove servers from the configuration
- [ ] Allow a specified amount of servers to be hosted at the same time
- [ ] Find a better way to get server statuses

Incase you have any questions or issues regarding this bot feel free to reach out to me via Discord: O S N I U M#2375 
I will try my best to help you but I don't really know what I am doing either.



[^1]: From now on you can update it with ```git pull``` when inside the directory.
