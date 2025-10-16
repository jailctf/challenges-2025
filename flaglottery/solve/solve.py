from pwn import *
#context.log_level = 'debug'
from time import sleep

while True:
    #io = process(['python3', 'flag_lottery.py'])
    io = remote('localhost', 5000)
    #io = remote('34.41.41.53', 24908)

    if {*eval(io.recvline().split(b": ")[1])} == {*b"[]>^"}:
        break

    io.close()

print("hit!")

def paren(x):
    return f"[{x}][_>_]"

# errors if a>b, otherwise nothing
def cmp(a,b):
    return f"[_][{paren(a)}>{paren(b)}]"

# errors if x>>b is odd, otherwise nothing
def leak(x,b):
    k = f"_[{ns[x]}]" + f">>{paren(ns[1])}"*b
    k1 = k + "^" + paren(ns[1])
    return cmp(k,k1)

def fleak(x):
    p = 0
    bit = 1
    for b in range(8):
        io.sendline(leak(x,b).encode())
        if b"broke." in io.recvuntil(b": "):
            p += bit
        bit <<= 1
    known[x] = p
    return p


for _ in range(100):

    print(_)
    
    ns = {0:"_>_",1:"[_]>[]"}
    known = [-1]*128

    io.recv()
    knowns=[0,1]
    for i in knowns:
        if i < 128:
            a = fleak(i)
            if a not in ns:
                ns[a] = f"_[{ns[i]}]"
            pa = a
            while a:
                if a not in ns:
                    ns[a] = ns[pa] + ">>" + paren(ns[1])
                for j in knowns:
                    c = a ^ j
                    if c not in ns:
                        knowns.append(c)
                        ns[c] = paren(ns[a]) + "^" + paren(ns[j])
                pa = a
                a >>= 1
        else:
            if i>>1 not in ns:
                knowns.append(i>>1)
                ns[i>>1] = paren(ns[i]) + ">>" + paren(ns[1])

    for a,b in enumerate(known):
        if b == -1:
            fleak(a)

    io.sendline(b"submit")
    io.sendline(bytearray(known).hex().encode())
    sleep(0.5)

io.interactive()
