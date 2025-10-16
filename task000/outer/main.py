#!/usr/local/bin/python3
import json
from random import shuffle
import subprocess

print('The code is run in an (actual) sandbox.')
print('It is not worth your time to try to break the sandbox rather than solving the golf challenge.')
print('')
print('One example input for clarity is: "703d6c616d62646120673a67"')
print('Decoded, this is "p=lambda g:g", which makes the output be simply the input.')
print('The code is run in an exec, just so you know.')
print('')

#p = subprocess.Popen(['nc', 'localhost', '5000'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
p = subprocess.Popen(['nc', '172.17.0.1', '5000'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
with open('task000.json', 'r') as f:
    testcases = [*enumerate(json.load(f))]

shuffle(testcases)
tc_inp = b'\n'.join([json.dumps(tc[1]['input']).encode().hex().encode() for tc in testcases])
tc_out = b'\n'.join([json.dumps(tc[1]['output']).encode() for tc in testcases]) + b'\n'

inp = input('task000 sol (hex) > ')

res = p.communicate(inp.encode() + b'\n' + str(len(testcases)).encode() + b'\n' + tc_inp + b'\n')[0].split(b'\n')
for i2, (i, tc) in enumerate(testcases):
    try:
        res2 = json.loads(res[i2])
    except Exception as e:
        res2 = "(ERROR)"
    if tc['output'] != res2:
        print(f'fail on tc {i}')
        print('=== EXPECTED ===')
        print(tc['output'])
        print('=== ACTUAL ===')
        print(repr(res2))
        exit()

if len(inp) > 128:
    print('your code works but is too long compared to our solution!!!')
    exit()

with open('flag.txt', 'r') as f:
    print('u win', f.read())

