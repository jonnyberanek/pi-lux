import asyncio

import socket

def tcp_sync():
  clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  clientsocket.connect(('localhost', 8888))

  clientsocket.send("fill:ff00ff;;".encode())
  clientsocket.recv(1024)
  # clientsocket.
  # await writer.drain()

  # data = await reader.read(1024)
  # print(f'Received: {data.decode()!r}')

  clientsocket.send("fill:ffff00;;".encode())
  clientsocket.send("fill:00ffff;;".encode())
  clientsocket.recv(1024)


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        'localhost', 8888)

    writer.write("fill:ff00ff;;".encode())
    await writer.drain()

    # data = await reader.read(1024)
    # print(f'Received: {data.decode()!r}')

    writer.write("fill:ffff00;;".encode())

    await writer.drain()
    writer.write("fill:00ffff;;".encode())
    await writer.drain()

    print((await reader.read(1)).hex())

    # res_code = int.from_bytes(await reader.read(1), 'big')
    # print(f'Received: {res_code}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client('Hello World!'))
# tcp_sync()