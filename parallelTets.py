import math
import time
import threading

primes = []
bestPrimeFound = 1
continueThread = True

def findPrimes(N):
    global primes
    global bestPrimeFound
    c = 2
    while c < N:
        p = True
        for i in primes:
            if i > math.sqrt(c):
                break
            if c % i == 0:
                p = False
                break
        if p:
            primes.append(c)
            if c > bestPrimeFound:
                bestPrimeFound = c
        c += 1

def findPrimesThread():
    c = 2
    while continueThread:
        findPrimes(c)
        c *= 2

def findPrimesTimed(t):
    global continueThread
    global bestPrimeFound
    x = threading.Thread(target=findPrimesThread)
    x.start()
    time.sleep(t)
    continueThread = False
    x.join()

    return bestPrimeFound

findPrimesTimed(10)
print(bestPrimeFound)
        
    