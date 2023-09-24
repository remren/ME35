import uasyncio as asyncio

import uartmsgs, asyncLEDLightSensor as asyncled, GamepadReceiver, GamepadSend

uart_client	= uartmsgs.UARTMsgs(1, "Bob Ross", "There are no mistakes. Only happy little accidents.")
photo_led	= asyncled.AsyncLED()

async def main():
    global done_check
    while not done_check:
        asyncio.create_task(uart_client.read())			# read task
        asyncio.create_task(uart_sendstdin())	# send stdin task
        asyncio.create_task(photo_led())
        await morse(name)
    print(light_vals)