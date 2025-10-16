# calc defanged

originally i had the challenge not print it so dunder repr wasn't possible so here is the original payload i guess

```
3and(type('',(),{'\x5f\x5fdel\x5f\x5f':lambda*v:breakpoint()})())
```

the idea here is the match can be bypassed easily as shown in maple's original payload or using `1and(<whatever>)`

then, we can have execution after the audit hook is gone by using either `__repr__` or `__del__`

`__repr__` will trigger on print

`__del__` will trigger on deletion of the object by the gc i think (very useful since no print required)

```
3and(type('',(),{'\x5f\x5frepr\x5f\x5f':lambda*v:breakpoint()})())
```
alt sol with repr

so we use type to create the class with said dunder method and then instantiate it so the dunder methods actually work

um also we use `lambda*v` because there is no space required between the `*` and the `lambda` because python is just
built different i guess (parser doesn't require space there i guess)

umm yeah that it also i guess breakpoint() is easy to escape but you could use os.system maybe if you have enough chars idk

i made the length limit pretty lax for this one so im not considering it a golf challenge but i wanted to prevent
unintendeds

