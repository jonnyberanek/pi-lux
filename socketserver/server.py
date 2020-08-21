import socketserver
import threading
import time
import json
import pprint

from event_loop import EventLoopThread
from tcp_server import TCPServerThread

global looper_thread
looperThread = None



class Lux():

  # pylint: disable=no-self-argument
  def makeTcpHandler(parent):

    class LuxTCPHandler(socketserver.BaseRequestHandler):
      """
      The request handler class for our server.

      It is instantiated once per connection to the server, and must
      override the handle() method to implement communication to the
      client.
      """

      def handle(self):
        # self.request is the TCP socket connected to the client
        data = json.loads(self.request.recv(1024).strip().decode('utf-8'))
        print("{} wrote:".format(self.client_address[0]))
        print(json.dumps(data, indent=4))
        parent.looper_thread.setNextCommand(data)
        # just send back the same data, but upper-cased
        self.request.sendall(b'Received')
    
    return LuxTCPHandler

  def __init__(self):
    self.server_thread = TCPServerThread(("localhost", 8011), self.makeTcpHandler())
    self.looper_thread = EventLoopThread()

  def start(self):
    print('Starting...')
    try:
      self.server_thread.start()
      print('Server listening at localhost:9999')
      self.looper_thread.start()
      print('Looper thread is ready!')
      while True: time.sleep(99)
    except (KeyboardInterrupt, SystemExit):
      print('All processes have ended')

if __name__ == "__main__":
  luxServer = Lux()
  luxServer.start()