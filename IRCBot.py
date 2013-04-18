# IRCBot
# http://github.com/justindmartin1/irc-bot
#
# Copyright 2013 Justin Martin
# Released under the MIT license
# http://github.com/justindmartin1/irc-bot/blob/master/LICENSE.md

import commands       #IRCBot Custom Commands
import configuration  #IRCBot Configuration
from os import system
import select
import socket
from sys import exit
from time import sleep

class IRCBot():
    sock = None

    def __init__(self):
        system("clear")
        self.connect(configuration.server, configuration.port)
        self.identify(configuration.server, configuration.identity, configuration.realname, configuration.nick)
        self.joinChannel(configuration.channel)
        self.live()

    def connect(self, server, port):
        self.sock = socket.socket()
        try:
            self.sock.connect((server, port))
            print "Connected to " + server
        except:
            print "Failed to connect to " + server + "!\n"
            exit()

    def die(self):
        self.sock.send("QUIT \r\n")
        exit()

    def identify(self, server, identity, realname, nick):
        self.sock.send("NICK " + nick + "\r\n")
        self.sock.send("USER " + identity + " " + server + " bla :" + realname + "\r\n")

    def joinChannel(self, channelName):
        self.channelName = channelName
        self.sock.send("JOIN " + channelName + "\r\n")
        print "Joined " + channelName

    def leaveChannel(self):
        self.sock.send("PART " + self.channelName + "\r\n")
        print "Left " + self.channelName
        self.channelName = None

    def live(self):
        while True:
            readableSocket, wlist, xlist = select.select([self.sock], [], [], 1)
            for c in readableSocket:
                if isinstance(c, socket.socket):
                    msg = self.sock.recv(4096)
                    if " PRIVMSG " in msg:
                        if "STOP BOT" in msg:
                            self.say("Goodbye!")
                            self.leaveChannel()
                            self.die()
                        elif any(greeting in msg.lower() for greeting in ("hello bot", "hi bot", "hey bot", "hola bot", "greetings bot")):
                            self.say("Greetings Human!")
                        else:
                            text = msg.rstrip().rsplit(':', 1)[-1].split(" ")
                            command = text[0]
                            parameters = text[1:]
                            try:
                                print "Running command \"" + command + "\"..."
                                output = getattr(commands, command)(parameters).split("\n")
                                for line in output:
                                    self.say(line)
                                    #stagger output so that we don't get kicked for flooding
                                    sleep(0.5)
                            except:
                                self.say("That command does not exist. Try again.")

                    elif "PING" in msg:
                        self.pong()

    def pong(self):
        self.sock.send("PONG : Pong\r\n")

    def say(self, message):
        messages = message.splitlines()
        for message in messages:
            self.sock.send("PRIVMSG " + self.channelName + " : " + message + "\r\n")