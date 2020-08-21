import asyncio 
import time
from threading import Thread

TICK_TIME = 0.015

async def doThing(dur=1.0):
  start = time.time()
  while start > time.time() - dur:
    print("{}%".format((time.time() - start)/dur*100))
    await asyncio.sleep(TICK_TIME)

loop = asyncio.get_event_loop()

run_app = asyncio.ensure_future(doThing(3))

def cancel():
  time.sleep(1)
  run_app.cancel()

Thread(target=cancel).start()

try:

  loop.run_until_complete(run_app)
  print('hello?')

except asyncio.exceptions.CancelledError:
  pass