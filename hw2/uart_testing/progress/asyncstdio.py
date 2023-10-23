# https://stackoverflow.com/questions/58454190/python-async-waiting-for-stdin-input-while-doing-other-stuff

import uasyncio as asyncio
import sys, time

async def get_stdin_reader() -> asyncio.StreamReader():
    stream_reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(stream_reader)
    loop = asyncio.get_running_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return stream_reader

async def main():
    stdin_reader = await get_stdin_reader()
    while True:
        print('input: ', end='', flush=True)
        line = await stdin_reader.readline()
        print(f'your input: {line.decode()}')
        time.sleep(0.2)

asyncio.run(main())