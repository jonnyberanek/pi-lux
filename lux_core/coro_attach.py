import asyncio

event = asyncio.Event()
e_val = None

async def pinger():
  num_loops = 0
  while True:
    await event.wait()
    num_loops += 1
    print(f"ping loop # {num_loops}")
    event.clear()
    await asyncio.sleep(.5)


async def looper():
  # global e_val
  # loop_num = 0
  y_val = None
  out_val = None
  while True:
    y_val = yield f"processed {y_val}"
    if y_val == None:
      print("none")
      continue
    # print(e_val)
    await asyncio.sleep(.5)
    # if y_val == "why":
    #   # out_val = "X why not"
    #   continue
    # out_val = y_val
    # loop_num += 1
    # e_val = None
    # event.clear()
    # yield loop_num

def handle_return(gen, func):
  returned = yield from gen
  func(returned)

async def main():
  global e_val
  
  loop = looper()
  await loop.asend(None)

  # # e_val = "hi"
  # # event.set()
  
  # print(await loop.asend("hi"))
  # await asyncio.sleep(.25)

  # print(await loop.asend("why"))
  # # e_val = "why"
  # # event.set()
  # await asyncio.sleep(.25)

  
  # # e_val = "bye"
  # # event.set()

  # print(await loop.asend("bye"))
  # await asyncio.sleep(.25)

  

  async def send(t):
    global req_nums
    req_nums += 1
    print(f"req # {req_nums}")
    await loop.asend(req_nums)
    await asyncio.sleep(t)

  await send(.6)
  await send(.6)
  await send(.1)
  await send(.1)
  await send(.1)
  await send(.1)
  await send(.1)
  await send(.1)
  await send(.1)

  # event.set()

req_nums = 0
async def main2():

  asyncio.ensure_future(pinger())

  
  async def send(t):
    global req_nums
    req_nums += 1
    print(f"req # {req_nums}")
    event.set()
    await asyncio.sleep(t)

  await send(.6)
  await send(.6)
  await send(.1)
  await send(.1)
  await send(.1)
  await send(.1)
  await send(.1)
  await send(.1)
  await send(.1)

asyncio.run(main())