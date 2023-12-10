import math
import signal
import time

bestPrimeFound = 1

def handleTimeout(signum, frame):
    raise TimeoutError

def findPrimes(N):
    global bestPrimeFound
    primes = []

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

def findPrimesTimed(t):
    global bestPrimeFound
    
    signal.signal(signal.SIGALRM, handleTimeout)
    signal.alarm(t)
    try:
        c = 2
        while True:
            findPrimes(c)
            c *= 2
    except TimeoutError:
        return bestPrimeFound

findPrimesTimed(10)
print(bestPrimeFound)
        
    