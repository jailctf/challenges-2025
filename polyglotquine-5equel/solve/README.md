# solve

So there's 2 problems to solve with this challenge.

1. How to split the execution of each language up to be able to write normal code
2. How to actually write a quine when all the languages are split up

To answer the first question, this is what I did:

1. Scheme and assembly both use semicolons as comments while bash, C#, and javascript all use them as separators. Start off with a semicolon to temporarily erase scheme and assembly. You might notice that bash throws an error because of invalid syntax (it doesn't like the semicolon being the first character), but you can finesse this by doing `\r;` which all languages interpret as a newline except for bash which will try to run a command named `\r` and then fail (which only writes a message to stderr, execution continues).
2. To separate bash from C# and js, you can use // which C# and js both use for comments, but bash ignores.
3. To separate C# and js, you can use `//\u0085` which C# interprets as `//\n` but javascript doesn't see it as a newline so it'll continue the comment.
4. To separate assembly and scheme, you can use `;\` because assembly sees that as a continued comment on the next line but scheme doesn't care about the backslash.

From there, I implemented a minimal C-style printf function in each language (I don't actually fully know most of these languages so most are shitty AI impls but golfed) so I could have the same template string for each language. Finally, I wrote a script to tie it all together but I lost the script so you're just going to have to trust me here.