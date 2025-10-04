import random
import time 
pin = str(input("enter your pin: "))
print(pin)
numlist = "1234567890"
def crackpin(pin):
    count = 0

    generatedpin = random.choices(numlist, k =len(pin))
    while(generatedpin != pin):
        count += 1
        generatedpin = random.choices(numlist, k =len(pin))
        generatedpin = "".join(generatedpin)
        print(generatedpin)
    print("success: " + str(generatedpin))
    print(count)
starttime = time.time()
crackpin(pin)
endtime= time.time() - starttime
print(endtime)

