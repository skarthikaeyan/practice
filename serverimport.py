#!/usr/bin/python3
"""Imported server Module"""
import time
import sys
import server as s
CS = s.ChatServer()  # creating object for chat server
try:
    CS.startserver()  # starting the server

except KeyboardInterrupt:

    CS.endserver()  # closing the server connection
    time.sleep(1)
    sys.exit()
