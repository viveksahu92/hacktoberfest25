import time

i = 0
seconds = int(input("How many seconds?: "))

if seconds > 0:
  while i != seconds:
    print(i+1)
    time.sleep(1)
    i+=1