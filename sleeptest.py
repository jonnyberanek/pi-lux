from time import perf_counter, time, sleep

def testSleep(frames):
  s = time()
  for i in range(frames):
    sleep(1/frames)
  f = time()
  return f - s