import uasyncio as asyncio
import time

async def do_nothing(i):
    prev = time.ticks_ms()
    while True:
        current = time.ticks_ms()
        print(f"I: {i}, diff: {current-prev}")
        if current-prev > 1010:
            print(f"Failed at: {i}")
            crash();
        prev = current
        await asyncio.sleep(1)

def loop():
    i = 1
    while True:
        asyncio.create_task(do_nothing(i))
        i += 1
        await asyncio.sleep(0.01)

try:
    asyncio.run(loop())
except KeyboardInterrupt:
    print('Interrupted')
finally:
    asyncio.new_event_loop()  
    print('All set! There will be a clear state now.')
    
