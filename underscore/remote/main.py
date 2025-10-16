#!/usr/local/bin/python3
# similar in theme to a previous challenge, get-and-call, for which the source and solution can be found here: https://github.com/jailctf/challenges/tree/main/get-and-call
# not sure if get-and-call will help much tho honestly

class Sandbox:
    def __init__(self):
        print('stinky')
        exit(1)


obj = Sandbox.__call__
getitems_left = 1
calls_left = 2
while True:
    print('obj', obj)
    print('1=getitem, 2=getattr, 3=call')
    inp = int(input('> '))
    inp2 = input('under > ')

    if not inp2[0] == '_':
        print('stinky')
        exit(1)
    if any(c not in '`abcdefghijklmnopqrstuvwxyz_`' for c in inp2):
        print('stinky')
        exit(1)

    if inp == 1:
        obj = obj[inp2]
        if getitems_left == 0:
            print('stinky')
            exit(1)
        getitems_left -= 1
    if inp == 2:
        obj = getattr(obj, inp2)
    if inp == 3:
        obj = obj(inp2)
        if calls_left == 0:
            print('stinky')
            exit(1)
        calls_left -= 1
