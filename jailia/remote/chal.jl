#!/usr/local/julia/bin/julia
function check(ex)
    if ex isa Expr
        if ex.head in (:call, :macrocall, :.)
            println("bad expression: $(ex.head)")
            exit()
        end
        for arg in ex.args
            check(arg)
        end
    end
end

print("Input a Julia expression: ")
code = readline()
ex = Meta.parse(code)
check(ex)
eval(ex)
