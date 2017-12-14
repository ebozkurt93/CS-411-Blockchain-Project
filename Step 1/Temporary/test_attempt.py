import string, random
import hashlib
import time

exampleChallenge = 'asdasd1sdadSDFSDsdf'

def generation(challenge=exampleChallenge, size =25):
    answer = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range (size))

    attempt = challenge + answer
    return attempt, answer

shaHash = hashlib.sha256()

def testAttempt():
    found = False
    start = time.time()

    while found == False:
        attempt, answer = generation()
        shaHash.update(attempt)
        solution = shaHash.hexdigest()
        if(solution.startswith('0000')):
            timeTook = time.time() - start
            print solution
            print timeTook
            found = True

    print answer

testAttempt()
