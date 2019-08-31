#!/usr/bin/env python3

from serial import Serial
import time

import threading

start=time.time()

# ~ def arduinoReader():
    # ~ """thread worker function"""
    # ~ print('Worker')


# ~ threads = []
# ~ for i in range(5):
    # ~ t = threading.Thread(target=worker)
    # ~ threads.append(t)
    # ~ t.start()

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

def isButtonPressed():
    with Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
        time.sleep(1)
        
        while True:
            time.sleep(0.1)

            cmd='l'
            ser.write(cmd.encode())
        
            if ser.in_waiting:
                x = ser.read()          # read one byte
                line = ser.readline()   # read a '\n' terminated line
                break
        
        return line.decode()

def isDummyButtonPressed():
    global start
    
    # ~ print("hello at:", time.time()- start)
    
    # ~ return "hello!"
    if time.time() - start > 1:
        start=time.time()
        return 1
    
    else: 
        return 0
        
            
class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client
        print(self.address, 'message handler')
        cmd=str(isDummyButtonPressed())
        print("cmd sent: ", cmd)
        self.sendMessage(cmd)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', 1337, SimpleEcho)
server.serveforever()
