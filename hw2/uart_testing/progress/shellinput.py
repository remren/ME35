import uselect, sys, time

# spoll=uselect.poll()
# spoll.register(sys.stdin,uselect.POLLIN)
# def read1():
#     return(sys.stdin.read(1) if spoll.poll(0) else None)
# 
# # main loop
# while True:
#     c = read1()
#     if c != None:
#         # process input as needed
#         print(c)
display = True

c = ""

while True:
    if display:
        print("Type!")
        display = False
    else:
        c = sys.stdin.read(1)
        display = True
        time.sleep(0.2)
        print(c, end="")
        print(f"length:{len(c)}")
        
        if c == '\n':
            print("dumb")
    time.sleep(0.2)