from bfi import interpret
from subprocess import check_output
from pwn import *

zero_small = '[[]>[]][[]>[]]>>[[]>[]][[]>[]]'  # bad op precedence
#zero_small = '0'
zero = f'[{zero_small}][{zero_small}]'

one_in_js = f'[++{zero}][{zero_small}]'
one_in_py = f'[[[[]]>[]][[]>[]]>>[[]>[]][[]>[]]][{zero_small}]'

one = f'[{one_in_js}+{one_in_py}][{zero_small}]'

# for js and python
one_hundred_eleven = f'[{"+".join([one]*111)}][{zero_small}]'

subtracting_val = f'-[{"--["*(48//2)}[]>[]][[]>[]]{("]["+zero_small+"]")*(48//2-1)}][{zero_small}]'
print_111_bf = f'+[-[[]>[]][[]>[]]>[[]>[]][[]>[]]>[]{"+["*49}...[{subtracting_val}]{"]"*49}>>[]][[]>[]]>>[[]>[]][[]>[]]'

print(print_111_bf)

code = one_hundred_eleven + f'+[-{print_111_bf}][{zero_small}]'

print('code ===============')
print(code)
print('code ===============')
# print('js', check_output(f'echo \'console.log({code})\' | node', shell=True).strip().decode())
# print('python', eval(code))
# bf_result = interpret(code, input_data='', buffer_output=True)
# print('brainfuck', bf_result if len(bf_result) else 'empty')

p = remote('localhost', 5000)

p.sendline(code.encode())
p.interactive()

