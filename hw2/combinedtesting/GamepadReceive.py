import morse_talk as mtalk
# send morse code over UART
# morse_word = [word sent over UART by other pico]
word = mtalk.decode(morse_word)
print("this is the decoded word: ", word)