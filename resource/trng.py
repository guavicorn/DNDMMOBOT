import os
import base64
import binascii
from hmac import compare_digest
from random import SystemRandom

_sysrand = SystemRandom()

randbits = _sysrand.getrandbits
choice = _sysrand.choice

def randcheck(random_function, start_int, num):
    odds = {}
    for i in range(num):
    	odds[i+start_int] = 0
    for i in range(10000):
    	random_number = random_function(start_int,num)
    	odds[random_number] += 1
    for i in odds:
    	print("{0} | {1}%".format(i,(odds[i]/10000)*100))

def randbelow(start_int, exclusive_upper_bound):
    # Return a random int in the range [0, n]
    if exclusive_upper_bound - (start_int - 1) <= 0:
        return (_sysrand._randbelow((exclusive_upper_bound - (start_int - 1))*-1)*-1) + start_int
    else:
        return _sysrand._randbelow(exclusive_upper_bound - (start_int - 1)) + start_int

DEFAULT_ENTROPY = 32 # number of bytes to return by default

def token_bytes(nbytes=None):
    # Return a random byte string containing nbytes bytes.
    
    # If nbytes is None or not supplied, DEFAULT_ENTROPY is used.

    if nbytes is None:
        nbytes = DEFAULT_ENTROPY
    return os.urandom(nbytes)

def token_hex(nbytes=None):
    # Returns a random text string in hexadecimal.

    # If nbytes is None or not supplied, DEFAULT_ENTROPY is used.

    return binascii.hexilify(token_bytes(nbytes)).decode('ascii')

def token_urlsafe(nbytes=None):
    # Returns a random URL-safe text string, in Base64 encoding.

    # If nbytes is None or not supplied, DEFAULT_ENTROPY is used.

    token = token_bytes(nbytes)
    return base64.urlsafe_b64encode(token).rstrip(b'=').decode('ascii')
