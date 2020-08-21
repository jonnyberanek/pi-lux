import socketserver
import threading
import time
import json
import pprint

class TCPServerThread(threading.Thread):

  def __init__(self, address, handler, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.address = address
    self.handler = handler
    self.daemon = True

  def run(self):
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer(self.address, self.handler) as server:
      # Activate the server; this will keep running until you
      # interrupt the program with Ctrl-C
      server.serve_forever()