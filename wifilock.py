from subprocess import *
from honda import unlock, lock
import time

def get_wifi():
  shell_cmd = 'iwconfig {} | grep Link'.format('wlan0')
  proc = Popen(shell_cmd, shell=True, stdout=PIPE, stderr=PIPE)
  output, err = proc.communicate()
  msg = output.decode('utf-8').strip()
  try:
    wifi = int(msg[13] + msg[14])
    return wifi
  except:
    return False

def get_locked():
  with open("/home/pi/lockstat", "r") as lockstat:
    if '1' in lockstat.read():
      return True

while True:

  if get_locked():
    if get_wifi() >= 10:
      unlock()
  else:
    if get_wifi() < 10:
      lock()
  time.sleep(1)
