#!/usr/bin/python3
from os import system, chdir

inp = input('tylenol is NOT provided > ')

# todo add length restriction for golfing

for c in inp:
    if c not in 'abcdefghijklmnopqrstuvwxyz+-*/(){};=':
        print(f'{c} in inp is not ok')
        exit(1)

with open('/tmp/usercode.ha', 'w') as f:
    f.write(inp)

chdir('/tmp/')
system('/app/Headache/hac -noDebug /tmp/usercode.ha')
system('/app/BrainfuckInterpreter/interpreter /tmp/a.bf')

print('bye bye')

