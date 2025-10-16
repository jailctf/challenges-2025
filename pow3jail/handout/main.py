#!/usr/local/bin/python3
from Crypto.Util.number import *

p = getPrime(128)

while True:
    n = max(int(input('> ')),0)
    try:
        eval(long_to_bytes(pow(n, 3, p)).decode('latin-1'))
    except Exception as e:
        print('error:', type(e))
