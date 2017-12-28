"""Importing client Package"""
import time
import sys
import multiclient as mc

try:

    NAME = input('Your Name:')
    RCVRNAME = input("Enter Name(case sensitive) of Friend to chat:")
    time.sleep(2)
    # creating object for ChatClient Module
    CLIENTOBJECT = mc.ChatClient(NAME, RCVRNAME)
    CLIENTOBJECT.startclient()

except KeyboardInterrupt as k:
    print("\nDisconnected", )
    CLIENTOBJECT.endchat()  # closing chat
    time.sleep(1)
    sys.exit()
