# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP
 
# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP
 
# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# PubNub keys

subkey = "sub-c-7f2edcde-5668-11ea-b828-26d2a984a2e5"
pubkey = "pub-c-28e6aa14-b430-4a71-ac2c-967cd14eed1b"
