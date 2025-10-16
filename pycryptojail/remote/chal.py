#!/usr/local/bin/python3
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
import os
import subprocess

def rsagen():
    p, q = getPrime(768), getPrime(768)
    n = p * q
    e = 0x10001
    d = pow(e, -1, (p - 1) * (q - 1))
    return (n, e)

def rsaenc(pk, msg):
    n, e = pk
    m = bytes_to_long(msg[:192])
    c = pow(m, e, n)
    return long_to_bytes(c)

if __name__ == '__main__':
    secret = os.urandom(8).hex()
    flag = open('flag.txt', 'r').read().strip()

    pk = rsagen()
    while True:
        code = input('>>> ')
        if any(c not in '0123456789abcdefghijklmnopqrstuvwxyz_+-*/ ' for c in code):
            print("You can't do that!")
            continue

        template = f'flag_you_will_never_guess_this_{secret} = {flag!r}\n\nprint({code})'
        output = subprocess.run(
            ['python3', '-c', template],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        ).stdout

        print(rsaenc(pk, output).hex())
