from pwn import *
from gmpy2 import iroot
from Crypto.Util.number import *

#p = process(["python3", 'chal.py'])
p = remote('localhost', 5000)

p2 = 0x696969
#p2 = int(p.recvline().decode())
#print('p:', p2)


def expected(n):
    return b'\x00' in long_to_bytes(n**3)


def check(n):
    p.sendline(str(n).encode())
    line = p.recvline()
    if b'SyntaxError' in line:  # there is no null byte
        return False
    elif b'ValueError' in line:  # there is a null byte
        return True
    elif b'NameError' in line:  # idk
        return False
    elif b'IndentationError' in line:  # there is a tab in front, todo handle properly
        return False
    else:
        raise NotImplementedError(line)


p.recvuntil(b'> ')

lower128 = int(iroot(2**127, 3)[0])
upper128 = int(iroot(2**128-1, 3)[0])

lower = lower128
upper = upper128
for _ in range(40):
    trials = []
    for i in range(32):
        center = (lower+upper)//2
        trials.append(check(center-i) == expected(center-i))
    result = all(trials)  # p above center -> result = True -> lower = center
    if result:
        lower = center
    else:
        upper = center
    print(hex(center**3), 'lower' if not result else 'higher')
print('the real slim shady (hex)', hex(p2))
print('the real slim shady', p2)
print('p^(1/3) ==', int(iroot(p2, 3)[0]))
print('p^(1/3) ~=', center)

print('=' * 40)

#p.interactive()

from z3 import *

s = Solver()

p_i = BitVec("p_i", 128)

s.add(center**3 < p_i)
s.add(p_i < (center+100)**3)

i = int(iroot((center**3)+(2**127 + 2**120 + 2**112 + 2**106 + 2**100 + 2**96), 3)[0])
print(hex(i**3))
print(hex(i**3 - p2))
print(hex(i**3 - center**3))
cnt = 0
bads = []
while cnt < 36:
    res = check(i)
    if res:
        bads.append(i)
        stmt = None
        val1 =  i**3
        print(i, hex(val1 - p2), 'ValueError !')
        #s.add(val1 > p_i)
        val2 = val1 - p_i
        for j in range(16):
            if j == 0:
                stmt = val2 % 256 == 0
            else:
                stmt = Or(LShR(val2, 8*j) % 256 == 0, stmt)
        #print(stmt)
        s.add(stmt)
        cnt += 1
    i += 1


print('check', s.check())
pg = int(str(s.model()[p_i]))
print('p2', hex(p2))
print('pg', hex(pg))
for bad in bads:
    print(hex(bad**3 - pg))

print('=' * 40)

jank_sc = f"""
p={pg}
v=30467827262018639703003375657
F.<x> = GF(p)[]
print((x^3 - v).roots())
"""

psage = process(['sage'])
psage.send(jank_sc.encode())
for i in range(4):
    print(i, psage.recvline())
recvd = psage.recvline()
print(recvd)
pl = int(recvd.split(b'(')[1].split(b',')[0])
print(pl)
p.interactive()

