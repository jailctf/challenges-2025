#!/usr/local/bin/python3
import os
os.environ['PWNLIB_NOTERM'] = '1'
from pwn import asm

try:
    shellcode = asm(input('> '), arch='amd64', os='linux')
except Exception as e:
    print('Could not compile shellcode. Exiting...')
    exit()

print('Compiled shellcode to X86!')
print(shellcode.hex(' '))
