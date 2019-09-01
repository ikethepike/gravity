#!/usr/bin/env python3

from serial import Serial
import time

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


start = time.time()

SERIALPORT = "/dev/ttyUSB0"
# ~ SERIALPORT="/dev/ttyACM0"

DUMMY = False
DUMMY_INTERVAL = 1


def isDummyButtonPressed():
    global start

    if time.time() - start > DUMMY_INTERVAL:
        start = time.time()
        return 1

    else:
        return 0


lastPressed = time.time()
previous = "not pressed"


def simpleRead():
    global lastPressed, previous

    pressed = "0"
    with Serial(SERIALPORT, 9600, timeout=1) as ser:
        cmd = "l"
        ser.write(cmd.encode())
        time.sleep(0.1)
        state = ""
        bytesToRead = (
            ser.inWaiting()
        )  # get the amount of bytes available at the input queue
        if bytesToRead:
            line = ser.read(
                bytesToRead
            ).decode()  # read the bytes            # ~ self.output_queue.put(line)
            state = line.splitlines()
            if int(state[0]) == 1:

                pressed = "0"
                previous = "not pressed"
            else:
                if time.time() - lastPressed > 0.1 and previous == "not pressed":
                    pressed = "1"
                    lastPressed = time.time()
                    previous = "pressed"

                else:
                    pressed = "0"

    return pressed


class SimpleEcho(WebSocket):
    def handleMessage(self):
        # echo message back to client
        print(self.address, "message handler")

        if DUMMY:
            cmd = str(isDummyButtonPressed())
        else:
            cmd = str(simpleRead())
        print("cmd sent: ", cmd)
        self.sendMessage(cmd)

    def handleConnected(self):
        global arduino

        print(self.address, "connected")

    def handleClose(self):
        print(self.address, "closed")


server = SimpleWebSocketServer("", 1337, SimpleEcho)
server.serveforever()
