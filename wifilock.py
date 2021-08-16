from subprocess import *
import RPi.GPIO as io
import time

io.setmode(io.BCM)
io.setwarnings(False)

UNLK = 16
LOCK = 12
PLIGHTS = 6
#HORN = 21

io.setup(UNLK, io.OUT)
io.setup(LOCK, io.OUT)
io.setup(PLIGHTS, io.OUT)
#io.setup(HORN, io.OUT)
io.output(UNLK, 1)
io.output(LOCK, 1)
io.output(PLIGHTS, 1)
#io.output(HORN, 1)

def getWifi():
    shell_cmd = 'iwconfig {} | grep Link'.format('wlan0')
    proc = Popen(shell_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    output, err = proc.communicate()
    msg = output.decode('utf-8').strip()
    try:
        wifi = int(msg[13] + msg[14])
        return wifi
    except:
        return False

def getLocked():
    with open("/home/pi/lockstat.txt", "r") as LOCKED:
        if '1' in LOCKED.read():
            return True

while True:

    if getLocked():
        if getWifi() >= 10:
            io.output(UNLK, 0)
            io.output(PLIGHTS, 0)
            time.sleep(.1)
            io.output(UNLK, 1)
            time.sleep(.6)
            io.output(PLIGHTS, 1)
            time.sleep(.7)
            io.output(PLIGHTS, 0)
            time.sleep(.7)
            io.output(PLIGHTS, 1)
            with open("/home/pi/lockstat.txt", "w") as LOCKED:
                LOCKED.write('LOCKED = 0')
    else:
        if getWifi() < 10:
            io.output(LOCK, 0)
            io.output(PLIGHTS, 0)
            time.sleep(.1)
            io.output(LOCK, 1)
#           io.output(HORN, 0)
            time.sleep(.1)
#           io.output(HORN, 1)
            time.sleep(.5)
            io.output(PLIGHTS, 1)
            with open("/home/pi/lockstat.txt", "w") as LOCKED:
                LOCKED.write('LOCKED = 1')
    time.sleep(1)
