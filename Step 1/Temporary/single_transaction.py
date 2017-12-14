import string, random
import hashlib
import sys, os
import time

if sys.version_info < (3, 6):
    import sha3

exampleChallenge = '''*** Bitcoin transaction ***
Serial number: 113923568100810392107501092256693023404
Payer: Erkay Savas
Payee: 9OHYC04SSW
Amount: 367 Satoshi
Previous hash in the chain: First transaction
Nonce: '''

def generateNonce(challenge=exampleChallenge):
    answer = str(random.getrandbits(128))

    attempt = challenge + answer + '\n'
    return attempt



def generateChain():
    found = False
    start = time.time()

    while found == False:
        textWithNonce = generateNonce()
        hash = hashlib.sha3_256(textWithNonce).hexdigest()
        if(hash.startswith('00')):
            print hash
            found = True

    print "time spent:" , time.time() - start

    text_file = open("LongestChain.txt", "w")
    text_file.write(textWithNonce + 'Proof of Work: ' + hash + '\n')
    text_file.close()

generateChain()
