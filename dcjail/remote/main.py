#!/usr/bin/python3

import os

inp = input('> ')
if any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxy' for c in inp):  # they gave me no blue raspberry dawg
    print('bad. dont even try using lowercase z')
    exit(1)

with open('/tmp/code.txt', 'w') as f:
    f.write(inp)

os.system(f'/usr/bin/dc -f /tmp/code.txt')

print("stop. you're done. get out.")

