#!/usr/local/bin/python3
import sys
inp = input('blindness > ')
sys.stdout.close()
flag = open('flag.txt').read()
eval(inp, {'__builtins__': {}, 'flag': flag})
print('bye bye')
