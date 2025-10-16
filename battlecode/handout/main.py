#!/usr/local/bin/python3
from os import system

print('battlecode. end input with __EOF__')

code = ''
while (line := input()) != '__EOF__':
    code += line
    code += '\n'

system('cp -r /battlecode25-scaffold /tmp/battlecode25-scaffold')

with open('/tmp/battlecode25-scaffold/python/src/examplefuncsplayer/bot.py', 'w') as f:
    f.write(code)

system(b'cd /tmp/battlecode25-scaffold/python && /usr/local/bin/python3 /tmp/battlecode25-scaffold/python/run.py run --p1 examplefuncsplayer --p2 examplefuncsplayer')

print('goodbye')

