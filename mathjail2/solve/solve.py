from sage.all import *
from pwn import *
from hashlib import sha256
from tqdm import tqdm
import os
import random

n = 256

testcases = []
random.seed(0x1337)
for _ in range(n):
    s = random.randbytes(64)
    x = int.from_bytes(s, 'big')
    output = int.from_bytes(sha256(s).digest(), 'big')
    testcases.append((x, output))

B = 2**256
e = 256*3*n//506|1  # pick large enough constant
print(f'{e = }')

mat = []
target = []

for x, output in tqdm(testcases):
    h = x**e//3
    row = [h>>(3*256*i)&B-1 for i in range(n)]
    mat.append(row)
    target.append(output)

F = Zmod(B)
mat = matrix(F, mat)
target = vector(F, target)
sol = list(map(int, mat.solve_right(target)))

X = 0
for i in range(n):
    X |= B**(3*i%n)*sol[~i]

a = 8**(256*n)//~-2**(256*n)*X
mask = 8**(256*n)//~-8**256*~-2**256

for x, output in testcases:
    h = x**e//3

    s = (h&mask)*(a&mask)
    assert s>>3*256*(n-1)&2**256-1 == output

a = f'8**{256*n}//~-2**{256*n}*{X}'
mask = f'8**{256*n}//~-8**256*~-2**256'
h = f'n**{e}//3'
code = f'({h}&{mask})*({a}&{mask})>>{3*256*(n-1)}&2**256-1'
print(f'{len(code) = }')
print(f'{code = }')

# io = process(['python', 'chal.py'])
io = remote('localhost', 5000)

# solve pow
io.recvline()
cmd = io.recvline().decode().strip()
sol = os.popen(cmd).read().strip()
io.sendlineafter(b'solution: ', sol.encode())

io.sendlineafter(b': ', code.encode())
io.interactive()
