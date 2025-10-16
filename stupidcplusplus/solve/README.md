# writeup for `stupid c++ a-z *;_ only`

the solve script (gen.py) is a huge mess

the general ideas are outlines below

---

we can do multiple lines of code because we have semicolon

we can declare variables but not set them by doing something like `unsigned long long varname;`

the goto statement can be used with variables (as in `goto *varname;`). this allows for easy jumping to wherever 
the varname int is pointing to

we can use alternative operators such as compl, xor, bitand, and, or, bitor, and_eq, or_eq, and xor_eq.

we can use main to zero a variable with `varname and_eq main and not main;`

to get the number 1, we can use the expression `not not main`

`0xffff_ffff_ffff_fffe` and `0xffff_ffff_ffff_ffff` can be formed by using `compl` (`~`, it flips all the bits) on 
the numbers 0 and 1

multiplying `0xffff_ffff_ffff_fffe` and `0xffff_ffff_ffff_ffff` yields the number 2. from this, it is very easy to 
get any other number by simply multiplying powers of two and adding them together

variables that are declared but not initialized are some value on the stack (whatever is there from some previous 
deleted function calls). we can use this to create a variable that has an old address pointing to libc 
(the var is not overwritten with a value, which is why this is possible).


<details>

<summary>offsets finding process (click for explanation)</summary>

we had `#include <iostream>` in the written cpp file contents in an old (first) version of the challenge
but we decided to remove that since it is a massive red herring and could lead to unintendeds as well

this ruined the solve script since all of the offsets were different

to find the actual spacing offsets (padding using `unsigned long long` variables), we used a debug dockerfile that would have
the same ld and libc shared object files so in theory everything is the same, except it wasnt and some of the values on the stack
that allowed us to get libc addresses were not at the same place. what did work was an offset of `rbp-0x270` since it was a 
pointer pointer pointer to the beginning bytes of libc (`'\x7fELF ... etc'`), and was probably left by the ld.so linker

we could dereference pointers using asterisk so we did something like

```
unsigned long long pad0;
unsigned long long pad1;
... more padding variables ...
unsigned long long pad69;
unsigned long long** libcaddrptr;  // useful value on the stack is here. we can deref it (twice since three times would just get the elf start bytes)
unsigned long long libcaddr;
... more stuff ...
libcaddr and_eq main and not main;  // zero the libcaddr
libcaddr or_eq **libcaddrptr;  // deref the libc addr pointer
... rest of exploit ...
```
</details>

i am not sure how the location of variables on the stack is decided. for the solve script, 
it was dependent on their first usages, not their declaration order. however, for a smaller example with just 
two unsigned long long variables, it was dependent on declaration. just trial and error it until you get it.

we can get some pointer number that is an offset of libc (e.g. we can get an unsigned long long with libc_base+whatever).
however, we cannot easily do addition with this pointer (or any numbers) to get some useful offset that we can jump to with goto.

to do addition, we can use a series of [full adders](https://media.geeksforgeeks.org/wp-content/uploads/3-57.png).
we have access to all the necessary components (xor,or,and), so we can just follow the diagram.

to split some 64 bit number into single bits, we can utilize those powers of two from earlier. using bitwise and on a power of two 
and a number will yield either a nonzero value or a zero value. this result can be anded (`&&`, not bitwise) 
with some other nonzero value to yield either 0 or 1 depending on if that nth bit is 0 or 1. with this, we can 
easily get each of the bits used for the full adders.

once we have the sum values from the full adders (see the diagram link), we can multiply them with the powers of two and 
then use either xor or bitwise or to combine them into a new 64 bit number.

now we can add some number to another number. to subtract, we can just overflow the number past 64 bits. 
adding `0xffff_ffff_ffff_ffff` is the same thing as subtracting by 1.

from this, we can get the offset from that leaked libc pointer to some useful value. here, we just use the `one_gadget` utility to 
find easy ways to get a shell. [these](https://i.ibb.co/R30vXPj/image.png) are the one gadgets i found. 
there are some restrictions for these, however. if i recall, none of these constraints were being followed exactly.

at first, i tried to set rdi so that we could just use the system function. however, this is way too much effort and it screwed 
up the position of the libc leak var. we also checked the one gadgets but some of the registers weren't containing the right values
for it to work. however, there was a keyword that saved this challenge

the `register` keyword is listed as being "unused" and "reserved" on cpp 17 and later (chall uses cpp 17). however, it still worked
for some reason (idk why). we can use it to fill all of the registers with the value 0 before doing goto.

```cpp
#include <iostream>

int main() {
    register int a0 = 0;
    register int a1 = 0;
    register int a2 = 0;
    register int a3 = 0;
    register int a4 = 0;
    register int a5 = 0;
    register int a6 = 0;
    register int a7 = 0;
    register int a8 = 0;
    register int a9 = 0;
    register int a10 = 0;
    printf("%d\n", a0+a1+a2+a3+a4+a5+a6+a7+a8+a9+a10);
}
```

g++ does give compile warnings when you use register, but we can just ignore the warnings.
```
test.cpp:14:18: warning: ISO C++17 does not allow ‘register’ storage class specifier [-Wregister]
   14 |     register int a10 = 0;
      |                  ^~~
```

taking a look in gdb:

```
(gdb) disas main
Dump of assembler code for function main:
   0x0000000000001189 <+0>:     endbr64
   0x000000000000118d <+4>:     push   %rbp
   0x000000000000118e <+5>:     mov    %rsp,%rbp
   0x0000000000001191 <+8>:     push   %r15
   0x0000000000001193 <+10>:    push   %r14
   0x0000000000001195 <+12>:    push   %r13
   0x0000000000001197 <+14>:    push   %r12
   0x0000000000001199 <+16>:    push   %rbx
   0x000000000000119a <+17>:    sub    $0x8,%rsp
   0x000000000000119e <+21>:    mov    $0x0,%eax
   0x00000000000011a3 <+26>:    mov    $0x0,%r8d
   0x00000000000011a9 <+32>:    mov    $0x0,%edi
   0x00000000000011ae <+37>:    mov    $0x0,%esi
   0x00000000000011b3 <+42>:    mov    $0x0,%ecx
   0x00000000000011b8 <+47>:    mov    $0x0,%edx
   0x00000000000011bd <+52>:    mov    $0x0,%r15d
   0x00000000000011c3 <+58>:    mov    $0x0,%r14d
   0x00000000000011c9 <+64>:    mov    $0x0,%r13d
   0x00000000000011cf <+70>:    mov    $0x0,%r12d
   0x00000000000011d5 <+76>:    mov    $0x0,%ebx
   0x00000000000011da <+81>:    add    %r8d,%eax
   0x00000000000011dd <+84>:    add    %edi,%eax
   0x00000000000011df <+86>:    add    %esi,%eax
   0x00000000000011e1 <+88>:    add    %ecx,%eax
   0x00000000000011e3 <+90>:    add    %edx,%eax
   0x00000000000011e5 <+92>:    add    %r15d,%eax
   0x00000000000011e8 <+95>:    add    %r14d,%eax
   0x00000000000011eb <+98>:    add    %r13d,%eax
   0x00000000000011ee <+101>:   add    %r12d,%eax
   0x00000000000011f1 <+104>:   add    %ebx,%eax
   0x00000000000011f3 <+106>:   mov    %eax,%esi
   0x00000000000011f5 <+108>:   lea    0xe08(%rip),%rax        # 0x2004
   0x00000000000011fc <+115>:   mov    %rax,%rdi
   0x00000000000011ff <+118>:   mov    $0x0,%eax
   0x0000000000001204 <+123>:   call   0x1070 <printf@plt>
   0x0000000000001209 <+128>:   mov    $0x0,%eax
   0x000000000000120e <+133>:   add    $0x8,%rsp
   0x0000000000001212 <+137>:   pop    %rbx
   0x0000000000001213 <+138>:   pop    %r12
   0x0000000000001215 <+140>:   pop    %r13
   0x0000000000001217 <+142>:   pop    %r14
   0x0000000000001219 <+144>:   pop    %r15
   0x000000000000121b <+146>:   pop    %rbp
   0x000000000000121c <+147>:   ret
End of assembler dump.
```

with this, we can use the 0x4c140 one gadget. rcx and rbx are null, and rsp+0x60 is obviously writable.

after that, we can just use goto and then win.

## amendment

ok apparently you can just use `sizeof` to get numbers pretty easily so ... lol

also we changed this challenge from having `#include <iostream>` to not having that to remove potential red herrings or rabbit holes and omg
it took so long to get a new solve script since all of the offsets and paddings were completely different.

