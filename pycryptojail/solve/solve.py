from sage.all import *
from pwn import *
from Crypto.Util.number import bytes_to_long as b2l, long_to_bytes as l2b
from math import gcd
from tqdm import trange

def pgcd(f, g):
    P = f.parent()
    h = P(f._pari_with_name().gcd(g._pari_with_name()))
    c = h.leading_coefficient()
    if c != P(0):
        h /= c
    return h

def run(code):
    io.sendlineafter(b'>>> ', code.encode())
    return b2l(bytes.fromhex(io.recvline().decode()))

#io = process(['python', 'chal.py'])
io = remote('localhost', 5000)

e = 0x10001
n = gcd(run('0') - b2l(b'0\n')**e, run('1') - b2l(b'1\n')**e)
# get rid of small factors
for i in range(2, 10**4):
    while n % i == 0:
        n //= i

def oracle(name):
    template = (
        'Traceback (most recent call last):\n'
        '  File "<string>", line 3, in <module>\n'
        'NameError: name %r is not defined\n'
    ) % name
    return run(name) != pow(b2l(template.encode()), e, n)

secret = ''
for i in range(16):
    for c in range(16):
        pad = 16 + (len(secret) + 2) // 5
        q = 'flag_you_will_never_guess_this_' + secret + '%x' % c + 'z' * pad
        if oracle(q):
            secret += '%x' % c
            break

print(f'{secret = }')
c1 = run('flag_you_will_never_guess_this_' + secret)
c2 = run('flag_you_will_never_guess_this_' + secret + '+__name__')

x = polygen(Zmod(n), 'x')
f1 = (x*256 + 10)**e - c1
f2 = (x*256**9 + b2l(b'__main__\n'))**e - c2
flag = int(-pgcd(f1, f2)[0])
print(l2b(flag))
