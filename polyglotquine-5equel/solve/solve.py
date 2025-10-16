from pwn import *

context.log_level = 'DEBUG'

#p = remote("localhost", 5000)
p = remote("challs2.pyjail.club", 20797)

POW_ENABLED = 1
if POW_ENABLED:
    p.recvuntil(b"proof of work: ")
    cmd = p.recvline(keepends=False).decode()
    result = os.popen(cmd).read()
    p.sendlineafter(b"solution: ", result.encode())

with open("final.b64", "rb") as f:
    code = f.read()

p.sendlineafter(b"> ", code)

p.interactive()
