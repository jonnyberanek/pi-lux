import threading
import time
import strip

WARM_TICK_TIME = 0.015 # Is slightly higher than 60 "frames" per second
COLD_TICK_TIME = 1.0
WARM_TIMEOUT = 10    

class EventLoopThread(threading.Thread):

  def __init__(self, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.daemon = True
    self.lastInputIngest = 0.0
    self._nextCommand = None
    self._strip = strip.Strip() 

  def setNextCommand(self, cmd):
    self._nextCommand = cmd

  def executeLoop(self):
    logMsg = "\n[{}]: ".format(time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime()))
    if (self._nextCommand):
      logMsg += "Current command: {}".format(self._nextCommand)
      self.runCommand(self._nextCommand)
      self._nextCommand = None
      self.lastInputIngest = time.time()
      
      
    else:
      logMsg += 'No current command.'
    print(logMsg)
    
  def runCommand(self, cmd):
    self._strip.fill(cmd.get("color"))

  def keepWarm(self):
    return self.lastInputIngest > time.time() - WARM_TIMEOUT

  def run(self):
    while True:
      self.executeLoop()
      if self.keepWarm():
        time.sleep(WARM_TICK_TIME)
      else:
        time.sleep(COLD_TICK_TIME)